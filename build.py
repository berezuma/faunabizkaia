#!/usr/bin/env python3
"""Basa-faunaren errekuperazio-zentroko datuak jaitsi eta bateratu.

Iturria: Open Data Bizkaia, `centro-recuperacion-fauna` datu-multzoa, CKAN
datastore APIaren bidez. Baliabide bat urteko; denak batera ekartzen dira.

Oharra: atariaren suebakiak `Mozilla/5.0` User-Agenta ukatzen du eta HTML bat
itzultzen du JSONaren ordez. Python-en lehenetsia onartzen du.
"""
import json, os, sys, urllib.request

API = "https://www.opendatabizkaia.eus/es/api/3/action"
HERE = os.path.dirname(os.path.abspath(__file__))
DATASET = "centro-recuperacion-fauna"
PAGE = 10000

def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return json.load(r)
        except Exception as e:
            if i == tries - 1:
                raise
            print(f"  berriro saiatzen ({e})", file=sys.stderr)

def fetch():
    pkg = get(f"{API}/package_show?id={DATASET}")["result"]
    out, fields = [], None
    for res in pkg["resources"]:
        if not res.get("datastore_active"):
            continue
        off, got = 0, 0
        while True:
            r = get(f"{API}/datastore_search?resource_id={res['id']}"
                    f"&limit={PAGE}&offset={off}")["result"]
            if fields is None:
                fields = [f["id"] for f in r["fields"] if f["id"] != "_id"]
            recs = r["records"]
            if not recs:
                break
            out += recs
            got += len(recs)
            off += PAGE
            if off >= r.get("total", 0):
                break
        print(f"  {res['id'][:8]}… {got:,} erregistro")
    return fields, out

if __name__ == "__main__":
    fields, recs = fetch()
    path = os.path.join(HERE, "data", "raw.json")
    with open(path, "w") as f:
        json.dump({"fields": fields, "records": recs}, f, ensure_ascii=False)
    print(f"guztira      : {len(recs):,} erregistro")
    print(f"eremuak      : {len(fields)}")
    print(f"fitxategia   : {os.path.getsize(path):,} byte")
