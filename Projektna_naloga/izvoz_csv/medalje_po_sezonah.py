import os
import csv

from tekmovalci.ciscenje import obdela_slovensko_sezono
from drzave.drzavni_servis import pridobi_drzavo


# ============================================
# 1) Izračun medalj po državah za eno sezono
# ============================================

def medalje_po_drzavah_za_sezono(leto):
    """
    Vrne slovar:
    {
        'SLO': [zlato, srebro, bron],
        'JPN': [zlato, srebro, bron],
        ...
    }
    """

    sez = obdela_slovensko_sezono(leto)
    if not sez:
        return None

    moski, zenske = sez

    # filtriraj napačne vnose
    moski = {ime: m for ime, m in moski.items() if isinstance(m, list) and len(m) == 3}
    zenske = {ime: m for ime, m in zenske.items() if isinstance(m, list) and len(m) == 3}

    drzave = {}   # {drzava_id: [zlato, srebro, bron]}

    # moški
    for ime, medalje in moski.items():
        drzava, drzava_id = pridobi_drzavo(ime)
        if not drzava_id:
            drzava_id = "NEZNANO"

        drzave.setdefault(drzava_id, [0, 0, 0])
        for i in range(3):
            drzave[drzava_id][i] += medalje[i]

    # ženske
    for ime, medalje in zenske.items():
        drzava, drzava_id = pridobi_drzavo(ime)
        if not drzava_id:
            drzava_id = "NEZNANO"

        drzave.setdefault(drzava_id, [0, 0, 0])
        for i in range(3):
            drzave[drzava_id][i] += medalje[i]

    return drzave


# ============================================
# 2) Shrani CSV za eno sezono
# ============================================

def shrani_csv_drzave_za_sezono(leto, drzave):
    os.makedirs("sezone_drzave", exist_ok=True)
    pot = f"sezone_drzave/medalje_drzave_{leto}.csv"

    with open(pot, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["DrzavaID", "Zlato", "Srebro", "Bron", "Skupaj"])

        for drzava_id, (z, s, b) in sorted(
            drzave.items(),
            key=lambda x: (x[1][0], x[1][1], x[1][2]),
            reverse=True
        ):
            w.writerow([drzava_id, z, s, b, z + s + b])



# ============================================
# 3) Glavna funkcija – obdela vse sezone
# ============================================

def ustvari_csv_vseh_sezon(vse_sezone):
    for leto in vse_sezone:

        drzave = medalje_po_drzavah_za_sezono(leto)
        if not drzave:
            continue

        shrani_csv_drzave_za_sezono(leto, drzave)

  



