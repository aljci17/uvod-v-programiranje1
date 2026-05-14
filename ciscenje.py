from requests_html import HTMLSession
from bs4 import BeautifulSoup
from imena import pocisti_ime, je_pravo_ime

session = HTMLSession()

def izloci_medalje_iz_tabele(tabela):
    medalje = {}

    for vrstica in tabela.find_all("tr"):
        celice = vrstica.find_all("td")
        if len(celice) < 7:
            continue

        w = pocisti_ime(celice[4].get_text())
        s = pocisti_ime(celice[5].get_text())
        b = pocisti_ime(celice[6].get_text())

        for i, ime in enumerate([w, s, b]):
            if ime and je_pravo_ime(ime):
                medalje.setdefault(ime, [0, 0, 0])
                medalje[ime][i] += 1

    return medalje


def obdela_slovensko_sezono(leto):
    url = f"https://sl.wikipedia.org/wiki/Svetovni_pokal_v_smu%C4%8Darskih_skokih_{leto}"
    r = session.get(url)

    if r.status_code != 200:
        return None

    juha = BeautifulSoup(r.text, "html.parser")

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
