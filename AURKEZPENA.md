# Dokumentazio teknikoa · Documentación técnica

**Proiektua / Proyecto:** «Zer iristen den» — Bizkaiko basa-faunaren
errekuperazio-zentroa, animaliaz animalia

**Kategoria / Categoría:** 1 · Datuen bistaratzea / Visualización de datos

**Egilea / Autor:** Beñat

**Deialdia:** 73/2026 Foru Dekretua, Datu Kazetaritzaren Erronkaren Sariak 2026
(BAO 141, 2026-07-27). Aurkezpen-epea: 2026-11-20. Izapidea: 3104.

---

# EUSKARAZ

## 1 · Erabilitako datu-iturriak

**Open Data Bizkaia ataria, `centro-recuperacion-fauna` datu-multzoa.**
https://www.opendatabizkaia.eus/es/catalogo/centro-recuperacion-fauna

Bost baliabide erabili dira, urte bana (2021, 2022, 2023, 2024, 2025), CKAN
`datastore_search` APIaren bidez eskuratuak. Guztira **7.649 erregistro eta 19
eremu**. Ez da beste iturririk erabili: proiektu osoa datu-multzo horretatik
ateratzen da.

Erabilitako eremu nagusiak: jasotze-data (ordua barne), espeziea (euskaraz,
gaztelaniaz eta izen zientifikoa), klasea eta azpiklasea, sartzeko arrazoia,
sartzeko egoera (bizirik/hilda), jasotako udalerria, bilakaera, eta askatutako
udalerria.

## 2 · Lan-prozesua

**Eskuratzea.** `build.py` script batek datu-multzoaren bost baliabideak
jaisten ditu CKAN APItik, orrikatuta, eta fitxategi bakarrean batzen. Oharra:
atariaren suebakiak `Mozilla/5.0` User-Agenta ukatzen du eta HTML bat itzultzen
du JSONaren ordez; Pythonen lehenetsiak funtzionatzen du.

**Garbiketa eta bateratzea.** `compact.py` script batek hiru arazo konpontzen
ditu:

- *Maiuskulak eta minuskulak nahastuta.* Iturriak «AVES» eta «Aves», «Abejero
  Europeo» eta «Abejero europeo» idazten ditu, eta horrek espezie bera birritan
  zenbatzea eragiten du. Gaztelaniazko izen normalizatua hartu da gako gisa eta
  euskarazkoa eta zientifikoa hari lotu: **380 etiketa → 294 espezie**.
- *Kodeak Excel moduan bilduta* (`="48"`), kendu egin dira.
- *Formatu trinkoa.* Animalia bakoitza zenbaki-ilara bat bihurtzen da eta
  etiketak behin bakarrik gordetzen dira: 7 MB → **272 KB**, orriak datu guztiak
  barruan eraman ditzan, eskaera gehigarririk gabe.

**Analisia.** Bizirauteko ehunekoak **bizirik iritsi eta emaitza ezaguna
dutenen** gainean bakarrik kalkulatzen dira (4.033 kasu). Bestela zentroari
leporatuko genioke ailegatu aurretik gertatutakoa. Sartzeko arrazoiak lau
taldetan bildu dira: txitak, gure eskua duten arrazoiak (harrapaketa, tiroa,
elektrokuzioa, pozoia, hesiak), kentzeko iritsitakoak (populazio-kontrola,
batidak, espezie-ezabaketa) eta gainerakoak.

**Egiaztapena.** Orrian argitaratutako zifra bakoitza iturri gordinetik berriro
kalkulatu da, trinkotze-prozesutik independenteki: 18 zifra, bat banan-banan.
Prozesu horrek akats bat aurkitu zuen argitaratu aurretik (ehuneko oker bat
amaierako atalean) eta zuzendu egin zen.

## 3 · Tresnak eta teknikak

**Datuak:** Python 3, liburutegi gehigarririk gabe (`urllib`, `json`,
`collections`, `re`, `unicodedata`).

**Bistaratzea:** HTML, CSS eta JavaScript eskuz idatziak, **kanpo-liburutegirik
gabe**. Eszena nagusia `<canvas>` bat da: 7.649 laukizuzen marrazten dira
fotograma bakoitzean, eta animaliak ez dira inoiz berriro sortzen — dauden
lekutik mugitzen dira beti, jarraitutasunak argudioa eusten baitu. Grafiko
estatikoak SVG dira, koordenatu-sistema pantailaren zabalerara egokitzen dutenak
testua irakurgarri izan dadin edozein neurritan.

**Hiru dimentsioko irudiak:** Blender 5.2, EEVEE motorrarekin. Espezie
bakoitzeko 36 fotograma, kamera eta argiak objektuaren inguruan biratuta
(argiak kamerarekin batera doaz, fotograma guztiak berdin argiztatuta egon
daitezen). PNG gardenak → WebP, 2 MB guztira 108 irudirentzat. Ez da WebGL:
irudi-sekuentzia bat da, eta horrek errendatze-kalitatea ematen du
kanpo-liburutegirik gabe.

Modeloen jatorria eta lizentziak orriaren metodologian aitortzen dira:
*Bubo bubo* (MNHN Paris, pierreyves.gagnier, CC BY), *Columba livia* (kenchoo,
CC BY), *Emys orbicularis* (arribadaclub, CC BY). Orrian esplizituki esaten da
irudikapenak direla eta ez animalia horien argazkiak.

**Errepikagarritasuna:** script bat datuentzat, beste bat garbiketarako, beste
bat orria muntatzeko. Prozesu osoa hutsetik errepika daiteke.

## 4 · Erabilgarritasuna

Elebiduna (euskara/gaztelania), egoera URLan gordetzen duena esteka
partekagarrietarako, teklatuz nabigagarria, CSV gisa deskargagarria, pantaila
txikietara egokitua (390 px-tik gora probatuta) eta paperean inprimagarria.
Mugimendua murriztea eskatzen duten erabiltzaileentzat (`prefers-reduced-motion`)
animazioak eten egiten dira. JavaScriptik gabe, albistearen laburpena agertzen da.

---

# EN CASTELLANO

## 1 · Fuentes de datos utilizadas

Se indica expresamente el **conjunto de datos del portal Open Data Bizkaia**
utilizado, que es el único empleado en el proyecto:

**`centro-recuperacion-fauna`** — Centro de recuperación de fauna silvestre de
Bizkaia.
https://www.opendatabizkaia.eus/es/catalogo/centro-recuperacion-fauna

Se han utilizado los cinco recursos del conjunto, uno por año (2021, 2022, 2023,
2024, 2025), obtenidos mediante la API CKAN `datastore_search`. En total **7.649
registros y 19 campos**. No se ha empleado ninguna otra fuente: todo el proyecto
sale de ese conjunto de datos.

Campos principales utilizados: fecha de recepción (con hora), especie (euskera,
castellano y nombre científico), clase y subclase, causa de ingreso, estado de
ingreso (vivo/muerto), municipio de recogida, evolución y municipio de suelta.

## 2 · Proceso de trabajo

**Obtención.** Un script `build.py` descarga los cinco recursos del conjunto
desde la API CKAN, paginando, y los unifica en un solo fichero. Nota: el
cortafuegos del portal rechaza el User-Agent `Mozilla/5.0` y devuelve HTML en
lugar de JSON; el agente por defecto de Python sí funciona.

**Selección.** De los 19 campos del conjunto se han retenido los diez que
sostienen el relato (fecha, especie en tres nomenclaturas, clase y subclase,
causa de ingreso, estado de ingreso, municipio de recogida, evolución y
municipio de suelta). Se descartan los códigos internos de provincia y las
fechas de extracción, que no aportan información al lector.

**Tratamiento: limpieza y unificación.** Un script `compact.py` resuelve tres
problemas:

- *Mayúsculas y minúsculas mezcladas.* La fuente escribe «AVES» y «Aves»,
  «Abejero Europeo» y «Abejero europeo», lo que hace contar dos veces la misma
  especie. Se ha usado el nombre castellano normalizado como clave, colgando de
  él el euskera y el científico: **380 etiquetas → 294 especies**.
- *Códigos envueltos al estilo Excel* (`="48"`), eliminados.
- *Formato compacto.* Cada animal pasa a ser una fila de números y las etiquetas
  se guardan una sola vez: 7 MB → **272 KB**, para que la página lleve todos los
  datos dentro sin peticiones adicionales.

**Análisis.** Los porcentajes de supervivencia se calculan únicamente sobre los
animales que **llegaron vivos y tienen desenlace anotado** (4.033 casos). Si no,
estaríamos atribuyendo al centro lo que ocurrió antes de llegar. Las causas de
ingreso se han agrupado en cuatro categorías: pollos, causas directamente
humanas (captura, disparo, electrocución, veneno, barreras), ingresos para
retirada (control poblacional, batidas, eliminación de especie) y el resto.

**Verificación.** Cada cifra publicada en la página se ha recalculado desde la
fuente en bruto, de forma independiente al proceso de compactación: 18 cifras,
una a una. Ese proceso detectó un error antes de la publicación (un porcentaje
incorrecto en la sección final) y se corrigió.

## 3 · Herramientas y técnicas

**Datos:** Python 3, sin librerías adicionales (`urllib`, `json`, `collections`,
`re`, `unicodedata`).

**Visualización:** HTML, CSS y JavaScript escritos a mano, **sin librerías
externas**. La escena principal es un `<canvas>`: se dibujan 7.649 rectángulos
en cada fotograma, y los animales nunca se recrean — siempre se mueven desde
donde están, porque la continuidad es lo que sostiene el argumento. Los gráficos
estáticos son SVG cuyo sistema de coordenadas se adapta al ancho de pantalla
para que el texto siga siendo legible a cualquier tamaño.

**Imágenes en tres dimensiones:** Blender 5.2 con el motor EEVEE. 36 fotogramas
por especie, con cámara y luces girando alrededor del objeto (las luces
acompañan a la cámara para que todos los fotogramas tengan la misma
iluminación). PNG con transparencia → WebP, 2 MB en total para 108 imágenes. No
es WebGL: es una secuencia de imágenes, lo que da calidad de render sin
librerías externas.

El origen y las licencias de los modelos se acreditan en la metodología de la
página: *Bubo bubo* (MNHN París, pierreyves.gagnier, CC BY), *Columba livia*
(kenchoo, CC BY), *Emys orbicularis* (arribadaclub, CC BY). En la página se dice
explícitamente que son representaciones y no fotografías de esos animales.

**Reproducibilidad:** un script para los datos, otro para la limpieza, otro para
montar la página. Todo el proceso puede repetirse desde cero.

## 4 · Usabilidad

Bilingüe (euskera/castellano), con el estado guardado en la URL para poder
compartir enlaces, navegable con teclado, descargable en CSV, adaptada a
pantallas pequeñas (probada desde 390 px) e imprimible en papel. Para quienes
piden movimiento reducido (`prefers-reduced-motion`) las animaciones se detienen.
Sin JavaScript, se muestra el resumen de la noticia.
