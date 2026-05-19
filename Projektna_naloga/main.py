from tekmovalci.ciscenje import obdela_slovensko_sezono
from izvoz_csv.csv_delo import shrani_csv_tekmovalci, shrani_csv_drzave
from drzave.drzavni_servis import pridobi_drzavo

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
tekmovalec_drzava = {}  # NOVO
tekmovalec_drzava = {}  

for ime, m in skupno.items():
    drzava, drzava_id = pridobi_drzavo(ime)

    if drzava is None:
        continue

    # shrani ID države za tekmovalca
    tekmovalec_drzava[ime] = drzava_id

    # seštevanje medalj po državah
    drzave.setdefault(drzava_id, [drzava, 0, 0, 0, 0])
    for i in range(4):
        drzave[drzava_id][i+1] += m[i]



shrani_csv_tekmovalci("skoki_moski.csv", moski, tekmovalec_drzava )
shrani_csv_tekmovalci("skoki_zenske.csv", zenske, tekmovalec_drzava)
shrani_csv_tekmovalci("skoki_skupno.csv", skupno, tekmovalec_drzava)
shrani_csv_drzave("drzave.csv",drzave)

print("Končano.")