from cache import preberi_ali_prenesi
from bs4 import BeautifulSoup
from .imena import pocisti_ime, je_pravo_ime, normaliziraj_ime



def izloci_medalje_iz_tabele(tabela):
    medalje = {}

    for vrstica in tabela.find_all("tr"):
        celice = vrstica.find_all("td")

        if len(celice) < 3:
            continue

        kandidati = [c.get_text(strip=True) for c in celice]

        filtrirani = []
        for x in kandidati:
            if any(kw in x.lower() for kw in [
                "hs", "team", "ekip", "odpoved", "prestavlj", "dq", "dnf",
                "slo ", "aut ", "nor ", "ger ", "pol ", "jpn ", "usa ", "can ",
                "l788", "n161", "f141", "nižni tagil"
            ]):
                continue
            if len(x) < 3:
                continue
            filtrirani.append(x)

        imena = []
        for x in filtrirani:
            x = pocisti_ime(x)
            x = normaliziraj_ime(x)
            if x and je_pravo_ime(x):
                imena.append(x)

        if len(imena) != 3:
            continue

        for i, ime in enumerate(imena):
            medalje.setdefault(ime, [0, 0, 0])
            medalje[ime][i] += 1

    return medalje



def obdela_slovensko_sezono(leto):
    
    url = (
        f"https://sl.wikipedia.org/wiki/"
        f"Svetovni_pokal_v_smu%C4%8Darskih_skokih_{leto}"
    )

    html = preberi_ali_prenesi(url)

    if not html:
        return None

    juha = BeautifulSoup(html, "html.parser")

    moski = {}
    zenske = {}

    trenutni_spol = None

    for el in juha.find_all(["h2", "h3", "table"]):

        if el.name in ["h2", "h3"]:
            naslov = el.get_text(" ", strip=True).lower()

            if "moški" in naslov:
                trenutni_spol = "M"

            elif "ženske" in naslov or "ženski" in naslov:
                trenutni_spol = "Z"

        elif el.name == "table":

            medalje = izloci_medalje_iz_tabele(el)

            if not medalje:
                continue

            if trenutni_spol == "M":
                for ime, m in medalje.items():
                    moski.setdefault(ime, [0,0,0])
                    for i in range(3):
                        moski[ime][i] += m[i]

            elif trenutni_spol == "Z":
                for ime, m in medalje.items():
                    zenske.setdefault(ime, [0,0,0])
                    for i in range(3):
                        zenske[ime][i] += m[i]

    return moski, zenske