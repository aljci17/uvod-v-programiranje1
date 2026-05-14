from ciscenje import obdela_slovensko_sezono
from drzave import najdi_drzavo
from csv_delo import shrani_csv
import time
import csv

# SEZONE
vse_sezone = list(range(1980, 2027))

moski_vse = {}
zenske_vse = {}

# CISCENJE
for leto in vse_sezone:
    rezultat = obdela_slovensko_sezono(leto)
    if rezultat is None:
        continue

    moski, zenske = rezultat

    for ime, m in moski.items():
        moski_vse.setdefault(ime, [0, 0, 0])
        for i in range(3):
            moski_vse[ime][i] += m[i]

    for ime, m in zenske.items():
        zenske_vse.setdefault(ime, [0, 0, 0])
        for i in range(3):
            zenske_vse[ime][i] += m[i]


# DODAJ SKUPAJ
def dodaj_skupaj(podatki):
    novi = {}
    for ime, (z, s, b) in podatki.items():
        novi[ime] = [z, s, b, z + s + b]
    return novi

moski_vse = dodaj_skupaj(moski_vse)
zenske_vse = dodaj_skupaj(zenske_vse)

# SKUPNO
skupno = {}

for ime, m in moski_vse.items():
    skupno.setdefault(ime, [0, 0, 0, 0])
    for i in range(4):
        skupno[ime][i] += m[i]

for ime, m in zenske_vse.items():
    skupno.setdefault(ime, [0, 0, 0, 0])
    for i in range(4):
        skupno[ime][i] += m[i]


# DRŽAVE
drzave = {}

for ime, m in skupno.items():
    drzava = najdi_drzavo(ime)
    time.sleep(0.3)

    #preskoči vse, kjer je država Neznano
    if drzava == "Neznano":
        continue

    drzave.setdefault(drzava, [0, 0, 0, 0])
    for i in range(4):
        drzave[drzava][i] += m[i]

# SHRANI CSV
shrani_csv("skoki_moski.csv", moski_vse)
shrani_csv("skoki_zenske.csv", zenske_vse)
shrani_csv("skoki_skupno.csv", skupno)

with open("skoki_drzave.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Država", "Zlato", "Srebro", "Bron", "Skupaj"])
    for k, m in sorted(drzave.items(), key=lambda x: x[1][3], reverse=True):
        w.writerow([k, m[0], m[1], m[2], m[3]])

print("Končano — vsi CSV-ji so ustvarjeni.")
