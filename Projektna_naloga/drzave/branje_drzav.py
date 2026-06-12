from bs4 import BeautifulSoup
from cache import preberi_ali_prenesi
from urllib.parse import quote

DRZAVE = {
    "Slovenia": "Slovenija", "Slovenian": "Slovenija", "Slovenija": "Slovenija", "slovenska":"Slovenija",
    "slovenski": "Slovenija",

    "Austria": "Avstrija", "Österreich": "Avstrija", "Austrian": "Avstrija",
    "avstrijska":"Avstrija", "avstrijski":"Avstrija",

    "Norway": "Norveška", "Norwegian": "Norveška", "Norge": "Norveška", "norveški":"Norveška",

    "Sweden": "Švedska",

    "Finland": "Finska", "Suomi": "Finska", "suomalainen":"Finska",

    "Germany": "Nemčija", "Deutschland": "Nemčija", "German":"Nemčija", "nemška":"Nemčija",

    "Poland": "Poljska", "Polska": "Poljska", "Polish": "Poljska",
    "polski":"Poljska", "Polski":"Poljska",

    "Japan": "Japonska", "Japanese": "Japonska", "日本": "Japonska", "japonska":"Japonska",

    "China": "Kitajska",

    "Italy": "Italija", "Italian": "Italija",

    "France": "Francija",

    "Canada": "Kanada",

    "USA": "ZDA",

    "South Korea": "Južna Koreja",

    "Czech Republic": "Češka", "Czechia": "Češka", "Czech": "Češka",
    "český": "Češka", "češki":"Češka",

    "Switzerland": "Švica", "Schweiz": "Švica", "Schweizer":"Švica", "Swiss":"Švica",

    "Russia": "Rusija", "Russian": "Rusija", "ruski":"Rusija",

    "Bulgaria": "Bolgarija", "България": "Bolgarija"
}


def normaliziraj_drzavo(beseda):
    beseda = beseda.strip()
    if beseda in DRZAVE:
        return DRZAVE[beseda]
    if beseda.capitalize() in DRZAVE:
        return DRZAVE[beseda.capitalize()]
    return None


def branje_drzavo_raw(ime):

    # PRAVILNO kodiranje URL-ja
    ime_url = quote(ime.replace(" ", "_"))

    urls = [
        f"https://sl.wikipedia.org/wiki/{ime_url}",
        f"https://en.wikipedia.org/wiki/{ime_url}",
        f"https://de.wikipedia.org/wiki/{ime_url}",
        f"https://pl.wikipedia.org/wiki/{ime_url}",
        f"https://fi.wikipedia.org/wiki/{ime_url}",
        f"https://no.wikipedia.org/wiki/{ime_url}",
        f"https://cs.wikipedia.org/wiki/{ime_url}",
        f"https://en.wikipedia.org/wiki/{ime_url}_(ski_jumper)"
    ]

    for url in urls:

        html = preberi_ali_prenesi(url)
        if not html:
            continue

        soup = BeautifulSoup(html, "html.parser")

        infobox = soup.find("table", class_=lambda x:
            x and "infobox" in " ".join(x) if isinstance(x, list)
            else x and "infobox" in x
        )

        # 1) title atribut
        if infobox:
            for a in infobox.find_all("a"):
                drz = normaliziraj_drzavo(a.get("title", ""))
                if drz:
                    return drz

        # 2) tekst v <a>
        if infobox:
            for a in infobox.find_all("a"):
                drz = normaliziraj_drzavo(a.get_text(strip=True))
                if drz:
                    return drz

        # 3) nationality
        if infobox:
            for row in infobox.find_all("tr"):
                th = row.find("th")
                td = row.find("td")
                if not th or not td:
                    continue
                key = th.get_text(strip=True).lower()
                val = td.get_text(" ", strip=True)
                if "nationality" in key:
                    for word in val.split():
                        drz = normaliziraj_drzavo(word)
                        if drz:
                            return drz

        # 4) born → zadnji del
        if infobox:
            for row in infobox.find_all("tr"):
                th = row.find("th")
                td = row.find("td")
                if not th or not td:
                    continue
                key = th.get_text(strip=True).lower()
                val = td.get_text(" ", strip=True)
                if "born" in key or "rojen" in key:
                    if "," in val:
                        zadnji = val.split(",")[-1].strip()
                        drz = normaliziraj_drzavo(zadnji)
                        if drz:
                            return drz

        # 5) prvi odstavek (fallback)
        prvi = soup.find("p")
        if prvi:
            text = prvi.get_text(" ", strip=True)
            for drzava in DRZAVE:
                if drzava in text:
                    return DRZAVE[drzava]
            for word in text.split():
                drz = normaliziraj_drzavo(word)
                if drz:
                    return drz

    return None
