from bs4 import BeautifulSoup
from cache import preberi_ali_prenesi

DRZAVE = {
    "Slovenia": "Slovenija", "Slovenian": "Slovenija", "Slovenija": "Slovenija", "slovenska":"Slovenija",

    "Austria": "Avstrija", "Österreich": "Avstrija", "Austrian": "Avstrija", "avstrijska":"Avstrija",

    "Norway": "Norveška", "Norwegian": "Norveška", "Norge": "Norveška",

    "Sweden": "Švedska",

    "Finland": "Finska", "Suomi": "Finska",

    "Germany": "Nemčija", "Deutschland": "Nemčija", "German":"Nemčija", "nemška":"Nemčija",

    "Poland": "Poljska", "Polska": "Poljska", "Polish": "Poljska", "polski":"Poljska", "Polski":"Poljska",

    "Japan": "Japonska", "Japanese": "Japonska", "日本": "Japonska", "japonska":"Japonska",

    "China": "Kitajska",

    "Italy": "Italija", "Italian": "Italija",

    "France": "Francija",

    "Canada": "Kanada",

    "USA": "ZDA",

    "South Korea": "Južna Koreja",

    "Czech Republic": "Češka", "Czechia": "Češka", "Czech": "Češka",

    "Switzerland": "Švica", "Schweiz": "Švica", "Schweizer":"Švica",

    "Russia": "Rusija", "Russian": "Rusija",

    "Bulgaria": "Bolgarija", "България": "Bolgarija"
}

def normaliziraj_drzavo(beseda):
    beseda = beseda.strip()
    if beseda in DRZAVE:
        return DRZAVE[beseda]
    if beseda.capitalize() in DRZAVE:
        return DRZAVE[beseda.capitalize()]
    return None

def normaliziraj(beseda):
    beseda = beseda.strip()
    if beseda in DRZAVE:
        return DRZAVE[beseda]
    # če je pridevnik (npr. Austrian)
    if beseda.capitalize() in DRZAVE:
        return DRZAVE[beseda.capitalize()]
    return None


def branje_drzavo_raw(ime):

    ime_url = ime.replace(" ", "_")

    urls = [
        f"https://sl.wikipedia.org/wiki/{ime_url}",
        f"https://en.wikipedia.org/wiki/{ime_url}",
        f"https://de.wikipedia.org/wiki/{ime_url}",
        f"https://pl.wikipedia.org/wiki/{ime_url}",
        f"https://fi.wikipedia.org/wiki/{ime_url}",
        f"https://no.wikipedia.org/wiki/{ime_url}",
        f"https://en.wikipedia.org/wiki/{ime_url}_(ski_jumper)"
    ]

    for url in urls:

        html = preberi_ali_prenesi(url)
        if not html:
            continue

        soup = BeautifulSoup(html, "html.parser")

        # bolj robustno iskanje infoboxa
        infobox = soup.find("table", class_=lambda x: x and "infobox" in " ".join(x) if isinstance(x, list) else x and "infobox" in x)
        if not infobox:
            continue

        # 1) Najprej title atribut (najbolj zanesljivo)
        for a in infobox.find_all("a"):
            drz = normaliziraj(a.get("title", ""))
            if drz:
                return drz

        # 2) Nato tekst v <a>
        for a in infobox.find_all("a"):
            drz = normaliziraj(a.get_text(strip=True))
            if drz:
                return drz

        # 3) Nationality vrstica
        for row in infobox.find_all("tr"):
            th = row.find("th")
            td = row.find("td")
            if not th or not td:
                continue

            key = th.get_text(strip=True).lower()
            val = td.get_text(" ", strip=True)

            if "nationality" in key:
                for word in val.split():
                    drz = normaliziraj(word)
                    if drz:
                        return drz

        # 4) Born → zadnji del
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
                    drz = normaliziraj(zadnji)
                    if drz:
                        return drz

        
        # Zadnji fallback: prvi odstavek, tudi če infobox obstaja
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


    print(f"❗ Ni našel države za: {ime}")
    return None
