from ciscenje import obdela_slovensko_sezono
from csv_delo import shrani_csv
from drzavni_servis import pridobi_drzavo

vse_sezone = list(range(1980, 2027))

moski = {}
zenske = {}

for leto in vse_sezone:
    sez = obdela_slovensko_sezono(leto)
    if sez is None:
        continue

    m, z = sez

    for ime, medalje in m.items():
        moski.setdefault(ime, [0,0,0])
        for i in range(3):
            moski[ime][i] += medalje[i]

    for ime, medalje in z.items():
        zenske.setdefault(ime, [0,0,0])
        for i in range(3):
            zenske[ime][i] += medalje[i]

def dodaj_skupaj(d):
    return {ime: [z, s, b, z+s+b] for ime, (z,s,b) in d.items()}

moski = dodaj_skupaj(moski)
zenske = dodaj_skupaj(zenske)

skupno = {}
for ime, m in moski.items():
    skupno.setdefault(ime, [0,0,0,0])
    for i in range(4):
        skupno[ime][i] += m[i]

for ime, m in zenske.items():
    skupno.setdefault(ime, [0,0,0,0])
    for i in range(4):
        skupno[ime][i] += m[i]

drzave = {}

for ime, m in skupno.items():
    drzava = pridobi_drzavo(ime)

    if drzava is None:
        continue

    drzave.setdefault(drzava, [0,0,0,0])
    for i in range(4):
        drzave[drzava][i] += m[i]

shrani_csv("skoki_moski.csv", moski)
shrani_csv("skoki_zenske.csv", zenske)
shrani_csv("skoki_skupno.csv", skupno)

import csv
with open("skoki_drzave.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Država", "Zlato", "Srebro", "Bron", "Skupaj"])
    for k, m in sorted(drzave.items(), key=lambda x: x[1][3], reverse=True):
        w.writerow([k, m[0], m[1], m[2], m[3]])

print("Končano.")
