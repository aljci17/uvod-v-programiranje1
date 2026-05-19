from bs4 import BeautifulSoup
from cache import preberi_ali_prenesi
from tekmovalci.ciscenje import izloci_top3_iz_tabele

def obdela_sezono(leto):
    url = f"https://sl.wikipedia.org/wiki/Svetovni_pokal_v_smu%C4%8Darskih_skokih_{leto}"
    html = preberi_ali_prenesi(url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")

    vsi = set()

    for h in soup.find_all(["h2", "h3"]):
        naslov = h.get_text().lower()

        if "moški" in naslov or "ženske" in naslov:
            tabela = h.find_next("table")
            if tabela:
                top3 = izloci_top3_iz_tabele(tabela)
                for trojica in top3:
                    for ime in trojica:
                        vsi.add(ime)

    return list(vsi)
