#!/usr/bin/env python3
"""raw.json -> orriak jaten duen formatu trinkoa.

Animalia bakoitza zenbaki-ilara bat bihurtzen da, eta etiketak behin bakarrik
gordetzen dira zerrenda banatan. Iturriak maiuskula/minuskula nahasten ditu
(«AVES» eta «Aves», «Abejero Europeo» eta «Abejero europeo») eta kodeak Excel
moduan biltzen ditu (`="48"`); hemen bateratzen da dena.
"""
import json, os, re, collections, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))

F_DATE = "JASOTZE DATA/FECHA RECEPCION"
F_CLASS = "KLASE/CLASE"
F_SUB = "AZPIKLASE/SUBCLASE"
F_EU = "ESPEZIE_EU/ESPECIE_EU"
F_ES = "ESPEZIE_CAS/ESPECIE_CAS"
F_SCI = "IZEN ZIENTIFIKOA/NOMBRE CIENTIFICO"
F_CAUSE = "SARTZEKO ARRAZOIA/CAUSA INGRESO"
F_STATE = "SARTZEKO EGOERA/ESTADO INGRESO"
F_MUN = "BILDUTAKO UDALERRIA/MUNICIPIO RECOGIDA"
F_PROV = "BILDUTAKO PROBINTZIA/PROVINCIA RECOGIDA"
F_OUT = "BILAKAERA/EVOLUCION"
F_RMUN = "ASKATUTAKO UDALERRIA/MUNICIPIO SUELTA"

def clean(s):
    """Zuriune bikoitzak, ertzak eta Excelen `="…"` bilgarria kendu."""
    s = re.sub(r'^="?|"?"$', "", str(s or "").strip())
    return re.sub(r"\s+", " ", s).strip()

def key(s):
    """Konparatzeko gakoa: maiuskulaz eta azenturik gabe."""
    s = clean(s).upper()
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")

def title(s):
    """«GAVIOTA PATIAMARILLA» -> «Gaviota patiamarilla»."""
    s = clean(s)
    return s[0].upper() + s[1:].lower() if s else s

# --- taldekatzeak ---------------------------------------------------------
# Zergatik iritsi den. «Kentzeko» taldea ez da erreskate bat: norbaitek
# animalia hori hortik kendu nahi zuen.
REMOVAL = {"CONTROL POBLACIONAL", "BATIDA", "DESCASTE O ELIMINACION DE LA ESPECIE",
           "CONTROL EPIDEMIOLOGICO", "DECOMISADO", "CONTROL CETRERIA"}
# Gure eskua zuzenean duten arrazoiak.
HUMAN = {"ATROPELLO", "DISPARO", "ELECTROCUCION", "COLISION LINEA ELECTRICA O AEROGENERADOR",
         "BARRERAS ARTIFICIALES", "INTOXICACION", "TRAMPAS", "PETROLEADO", "ANZUELO",
         "ARTES DE PESCA", "CAUTIVIDAD", "AHOGAMIENTO"}

OUT_GROUP = {   # bilakaera -> talde laburra
    "LIBERADOS": "free", "MUERTO": "dead", "SACRIFICADO": "put",
    "INSTALACIONES DEL CENTRO": "kept", "DEJADO PARA CRIA": "kept",
    "CEDIDO": "kept", "DEVUELTO AL DUENO": "kept", "FUGADO DE LAS INSTALACIONES.": "kept",
    "NO ENTRA EN EL CENTRO-INTERVENCION GUARDERIA": "none",
}

def cause_group(c):
    k = key(c)
    if not k: return "unk"
    if k in REMOVAL: return "remove"
    if k in HUMAN: return "human"
    if k == "CRIA": return "young"
    return "other"

if __name__ == "__main__":
    raw = json.load(open(os.path.join(HERE, "data", "raw.json")))
    R = raw["records"]

    # Espezie-taula: gaztelaniazko izen normalizatua da gakoa (7.637/7.649
    # beteta). Euskarazkoa eta zientifikoa gako horri lotzen zaizkio, eta
    # aldaera ohikoena hartzen da: iturriak tarteka letra larriz idazten du.
    best = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    seen = collections.Counter()
    for r in R:
        k = key(r.get(F_ES)) or key(r.get(F_SCI)) or "?"
        seen[k] += 1
        for f, lab in ((F_ES, "es"), (F_EU, "eu"), (F_SCI, "sci"), (F_CLASS, "cls"), (F_SUB, "sub")):
            v = clean(r.get(f))
            if v: best[k][lab][v] += 1

    sp_keys = [k for k, _ in seen.most_common()]
    sp_ix = {k: i for i, k in enumerate(sp_keys)}
    def pick(k, lab):
        c = best[k][lab]
        return title(c.most_common(1)[0][0]) if c else ""

    species = [{"es": pick(k, "es"), "eu": pick(k, "eu"), "sci": pick(k, "sci")} for k in sp_keys]
    cls_of = [key(pick(k, "cls")) for k in sp_keys]
    sub_of = [title(pick(k, "sub")) for k in sp_keys]

    classes = sorted({c for c in cls_of if c})
    subs = sorted({s for s in sub_of if s})
    causes, muns, outs = {}, {}, {}
    def idx(d, v):
        if v not in d: d[v] = len(d)
        return d[v]

    rows, nodate = [], 0
    for r in R:
        d = clean(r.get(F_DATE))
        if len(d) < 10:
            nodate += 1
            continue
        k = key(r.get(F_ES)) or key(r.get(F_SCI)) or "?"
        prov = key(r.get(F_PROV))
        rows.append([
            d[:10],                                               # 0 eguna
            int(d[11:13]) if len(d) >= 13 and d[11:13].isdigit() else -1,   # 1 ordua
            sp_ix[k],                                             # 2 espeziea
            idx(causes, title(r.get(F_CAUSE)) or "—"),            # 3 arrazoia
            1 if "VIVO" in key(r.get(F_STATE)) else 0,            # 4 bizirik iritsi da?
            idx(outs, title(r.get(F_OUT)) or "—"),                # 5 bilakaera
            idx(muns, title(r.get(F_MUN)) or "—") if prov == "BIZKAIA" else -1,  # 6 non jasoa
            idx(muns, title(r.get(F_RMUN))) if clean(r.get(F_RMUN)) else -1,     # 7 non askatua
        ])

    inv = lambda d: [k for k, _ in sorted(d.items(), key=lambda kv: kv[1])]
    payload = {
        "species": species,
        "spClass": [classes.index(c) if c in classes else -1 for c in cls_of],
        "spSub": [subs.index(s) if s in subs else -1 for s in sub_of],
        "classes": classes, "subs": subs,
        "causes": inv(causes), "outs": inv(outs), "muns": inv(muns),
        "causeGroup": [cause_group(c) for c in inv(causes)],
        "outGroup": [OUT_GROUP.get(key(o), "unk") for o in inv(outs)],
        "rows": rows,
    }
    path = os.path.join(HERE, "data", "fauna.json")
    with open(path, "w") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))

    no_eu = sum(1 for s in species if not s["eu"])
    print(f"animaliak    : {len(rows):,}" + (f"  (+{nodate} datarik gabe)" if nodate else ""))
    print(f"espezieak    : {len(species):,}  ({no_eu} euskarazko izenik gabe)")
    print(f"klaseak      : {len(classes)} · azpiklaseak: {len(subs)}")
    print(f"arrazoiak    : {len(causes)} · bilakaerak: {len(outs)} · udalerriak: {len(muns)}")
    print(f"fitxategia   : {os.path.getsize(path):,} byte")
