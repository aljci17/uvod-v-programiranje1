from tekmovalci.ciscenje import obdela_slovensko_sezono
from izvoz_csv.csv_delo import (
    shrani_csv_tekmovalci,
    shrani_csv_drzave
)
from drzave.drzavni_servis import pridobi_drzavo
from tekmovalci.preimenovanja import popravi_porocena_imena
from izvoz_csv.medalje_po_sezonah import ustvari_csv_vseh_sezon


vse_sezone = list(range(2012,2027))

moski = {}
zenske = {}

for leto in vse_sezone:


    sez = obdela_slovensko_sezono(leto)

    if not sez:
        continue

    m, z = sez


    # moški
    for ime, medalje in m.items():

        if not isinstance(medalje, list) or len(medalje) != 3:
            continue
        
        moski.setdefault(ime, [0,0,0])

        for i in range(3):
            moski[ime][i] += medalje[i]

    # ženske
    for ime, medalje in z.items():

        if not isinstance(medalje, list) or len(medalje) != 3:
            continue

        zenske.setdefault(ime, [0,0,0])

        for i in range(3):
            zenske[ime][i] += medalje[i]


def dodaj_skupaj(d):
    return {
        ime: [z, s, b, z+s+b]
        for ime, (z, s, b) in d.items()
    }

moski = dodaj_skupaj(moski)
zenske = dodaj_skupaj(zenske)

moski = popravi_porocena_imena(moski)
zenske = popravi_porocena_imena(zenske)

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
tekmovalec_drzava = {}

for ime, m in skupno.items():

    drzava, drzava_id = pridobi_drzavo(ime)

    if not drzava:
        continue

    if ime not in tekmovalec_drzava:
        tekmovalec_drzava[ime] = drzava_id

    drzave.setdefault(
        drzava_id,
        [drzava, 0,0,0,0]
    )

    for i in range(4):
        drzave[drzava_id][i+1] += m[i]


shrani_csv_tekmovalci("skoki_moski.csv", moski, tekmovalec_drzava)
shrani_csv_tekmovalci("skoki_zenske.csv", zenske, tekmovalec_drzava)
shrani_csv_tekmovalci("skoki_skupno.csv", skupno, tekmovalec_drzava)
shrani_csv_drzave("drzave.csv", drzave)
# Ustvari CSV-je po sezonah (moški + ženske skupaj)
ustvari_csv_vseh_sezon(vse_sezone)

print("\nKončano.")


