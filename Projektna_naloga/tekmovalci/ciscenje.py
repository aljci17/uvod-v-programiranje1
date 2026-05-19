from cache import preberi_ali_prenesi
from bs4 import BeautifulSoup
from .imena import pocisti_ime, je_pravo_ime, normaliziraj_ime



def izloci_medalje_iz_tabele(tabela):
    medalje = {}

    for vrstica in tabela.find_all("tr"):
        celice = vrstica.find_all("td")

        # preskoči vrstice brez rezultatov
        if len(celice) < 3:
            continue

        kandidati = [c.get_text(strip=True) for c in celice]

        # filtriraj ven očitno napačne vnose
        filtrirani = []
        for x in kandidati:
            if any(kw in x.lower() for kw in [
                "hs", "team", "ekip", "odpoved", "prestavlj", "dq", "dnf",
                "slo ", "aut ", "nor ", "ger ", "pol ", "jpn ", "usa ", "can ",
                "l788", "n161", "f141"
            ]):
                continue
            if len(x) < 3:
                continue
            filtrirani.append(x)

        # iščemo 3 imena zapored
        imena = []
        for x in filtrirani:
            x = pocisti_ime(x)
            x = normaliziraj_ime(x)
            if x and je_pravo_ime(x):
                imena.append(x)

        if len(imena) != 3:
            continue

        # dodaj medalje
        for i, ime in enumerate(imena):
            medalje.setdefault(ime, [0, 0, 0])
            medalje[ime][i] += 1

    return medalje




def obdela_slovensko_sezono(leto):
    url = f"https://sl.wikipedia.org/wiki/Svetovni_pokal_v_smu%C4%8Darskih_skokih_{leto}"
    html = preberi_ali_prenesi(url)
    if not html:
        return None


    juha = BeautifulSoup(html, "html.parser")

    moski = {}
    zenske = {}

    for h in juha.find_all(["h2", "h3"]):
        naslov = h.get_text().lower()

        if "moški" in naslov:
            tabela = h.find_next("table")
            if tabela:
                moski = izloci_medalje_iz_tabele(tabela)

        if "ženske" in naslov:
            tabela = h.find_next("table")
            if tabela:
                zenske = izloci_medalje_iz_tabele(tabela)

    return moski, zenske



def izloci_top3_iz_tabele(tabela):
    """
    Iz tabele na Wikipediji izlušči točno 3 imena (1., 2., 3. mesto).
    Vrne seznam trojic: [ [ime1, ime2, ime3], ... ]
    """
    rezultati = []

    for vrstica in tabela.find_all("tr"):
        celice = vrstica.find_all("td")

        # tabela mora imeti vsaj 3 stolpce
        if len(celice) < 3:
            continue

        kandidati = [c.get_text(strip=True) for c in celice]

        imena = []
        for x in kandidati:
            x = pocisti_ime(x)
            x = normaliziraj_ime(x)
            if x and je_pravo_ime(x):
                imena.append(x)

        # iščemo točno 3 imena (1., 2., 3. mesto)
        if len(imena) == 3:
            rezultati.append(imena)

    return rezultati
