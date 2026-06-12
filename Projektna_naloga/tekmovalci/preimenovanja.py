# ============================================
# PRENOS MEDALJ IN BRISANJE STARIH IMEN
# ============================================

# Mapa poročnih preimenovanj
PREIMENOVANJA = {
    "Nika Križnar": "Nika Vodan",
    "Urša Bogataj": "Urša Križnar",
    "Chiara Hölzl": "Chiara Kreuzer",
}

def _se_ujemata_strukturi(vrednost):
    """
    Vrne 'dict' ali 'list' glede na strukturo medalj.
    """
    if isinstance(vrednost, dict):
        return "dict"
    if isinstance(vrednost, list):
        return "list"
    return None


def _dodaj_medalje(cilj, vir):
    """
    Sešteje medalje med dvema zapisoma.
    Podpira obe tvoji strukturi:
    - dict: {"zlato": x, "srebro": y, "bron": z}
    - list: [zlato, srebro, bron, ...]
    """

    tip = _se_ujemata_strukturi(cilj)

    if tip == "dict":
        cilj["zlato"] += vir.get("zlato", 0)
        cilj["srebro"] += vir.get("srebro", 0)
        cilj["bron"] += vir.get("bron", 0)

    elif tip == "list":
        for i in range(min(len(cilj), len(vir))):
            cilj[i] += vir[i]

    return cilj


def popravi_porocena_imena(rezultati):
    """
    - spremeni priimke trem skakalkam
    - prenese medalje iz starega imena na novo
    - izbriše stare zapise
    - deluje na tvoji strukturi rezultatov
    """

    for staro, novo in PREIMENOVANJA.items():

        # Če starega imena sploh ni, preskoči
        if staro not in rezultati:
            continue

        # Če novega imena še ni, ga ustvari z isto strukturo
        if novo not in rezultati:
            struktura = rezultati[staro]
            if isinstance(struktura, dict):
                rezultati[novo] = {"zlato": 0, "srebro": 0, "bron": 0}
            else:
                rezultati[novo] = [0] * len(struktura)

        # Prenesi medalje
        rezultati[novo] = _dodaj_medalje(rezultati[novo], rezultati[staro])

        # Izbriši staro ime
        del rezultati[staro]

    return rezultati
