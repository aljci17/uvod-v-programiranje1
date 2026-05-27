from bs4 import BeautifulSoup
from cache import preberi_ali_prenesi
import regex as re

# ============================
# PREIMENOVANJA (poročna imena)
# ============================

preimenovanja = {
    "Nika Križnar": "Nika Vodan",
    "Urša Bogataj": "Urša Križnar",
    "Chiara Hölzl": "Chiara Kreuzer",
}

def popravi_preimenovanja(ime):
    ime = ime.strip()
    return preimenovanja.get(ime, ime)


# ============================
# ZDRUŽEVANJE MEDALJ
# ============================

def zdruzi_dvojna_imena(rezultati, preimenovanja):

    skupine = {}

    for staro, novo in preimenovanja.items():
        skupine.setdefault(novo, set()).add(staro)
        skupine[novo].add(novo)

    for glavno_ime, imena_v_skupini in skupine.items():

        if glavno_ime not in rezultati:
            rezultati[glavno_ime] = {"zlato": 0, "srebro": 0, "bron": 0}

        for ime in imena_v_skupini:
            if ime in rezultati:
                for tip in ["zlato", "srebro", "bron"]:
                    rezultati[glavno_ime][tip] += rezultati[ime][tip]

        for ime in imena_v_skupini:
            if ime != glavno_ime and ime in rezultati:
                del rezultati[ime]

    return rezultati


# ============================
# SEZNAM DRŽAV
# ============================

DRZAVE = {
    "Slovenia", "Slovenija", "slovenski", "Slovenci",

    "Austria", "Avstrija", "Österreich", "Austrian",

    "Norway", "Norveška", "Norwegian", "norsk", "Norge",

    "Sweden", "Švedska",

    "Finland", "Finska", "Suomi", "Finnish", "suomalainen",

    "Germany", "Nemčija", "Deutschland", "deutsche",

    "Poland", "Poljska", "poljski", "polski", "Polish", "Polska",

    "Japan", "Japonska", "japanischer", "Japanese", "japonska", "日本",

    "China", "Kitajska",

    "Italy", "Italija", "Italian",

    "France", "Francija",

    "Canada", "Kanada",

    "USA", "ZDA",

    "South Korea", "Južna Koreja",

    "Czech Republic", "Češka", "Čehi", "češki", "česki", "Czechia", "Czech",

    "Switzerland", "Švica", "Schweiz", "Schweizer",

    "Russia", "Rusija", "Russian",

    "Bulgaria", "Bolgarija", "Bulgarian", "България"
}


# ============================
# NORMALIZACIJA PRIDEVNIKOV
# ============================

def normaliziraj_pridevnik(beseda):
    slovar = {
        "slovenski": "Slovenija",
        "slovenska": "Slovenija",
        "slovenci": "Slovenija",

        "češki": "Češka",
        "česki": "Češka",
        "čehi": "Češka",

        "polski": "Poljska",
        "polska": "Poljska",
        "polish": "Poljska",

        "finski": "Finska",
        "finnish": "Finska",

        "japonski": "Japonska",
        "japanischer": "Japonska",
        "japanese": "Japonska",
        "japonska": "Japonska",

        "norwegian": "Norveška",
        "norsk": "Norveška",
        "norge": "Norveška",

        "italian": "Italija",

        "bulgarian": "Bolgarija",

        "russian": "Rusija",
    }

    return slovar.get(beseda.lower())


# ============================
# BRANJE DRŽAVE
# ============================

def branje_drzavo_raw(ime):
    
    ime = popravi_preimenovanja(ime)
    ime_url = ime.replace(" ", "_")

    urls = [
        f"https://sl.wikipedia.org/wiki/{ime_url}",
        f"https://en.wikipedia.org/wiki/{ime_url}",
        f"https://de.wikipedia.org/wiki/{ime_url}",
        f"https://pl.wikipedia.org/wiki/{ime_url}",
        f"https://fi.wikipedia.org/wiki/{ime_url}",
        f"https://no.wikipedia.org/wiki/{ime_url}"
    ]

    for url in urls:

        html = preberi_ali_prenesi(url)
        if not html:
            continue

        soup = BeautifulSoup(html, "html.parser")

        # robusten infobox matcher
        infobox = soup.find(
            "table",
            class_=lambda x: x and (
                ("infobox" in x) if isinstance(x, str)
                else any("infobox" in c for c in x)
            )
        )

        # ============================
        # Fallback 0: če ni infoboxa → prvi odstavek
        # ============================
        if not infobox:

            prvi_p = soup.find("p")
            if prvi_p:
                text = prvi_p.get_text(" ", strip=True)

                # osnovne oblike
                for drzava in DRZAVE:
                    if drzava in text:
                        return drzava

                # pridevniki
                for word in text.split():
                    drz = normaliziraj_pridevnik(word)
                    if drz:
                        return drz

            continue


        # 1) country-name
        country = infobox.find("span", class_="country-name")
        if country:
            a = country.find("a")
            if a:
                return a.get_text(strip=True)

        # 2) pregled vrstic
        for row in infobox.find_all("tr"):
            th = row.find("th")
            td = row.find("td")
            if not th or not td:
                continue

            key = th.get_text(strip=True).lower()
            a = td.find("a")
            val = a.get_text(strip=True) if a else td.get_text(strip=True)

            if (
                "reprezentanca" in key or
                "država" in key or
                "country" in key or
                "nationality" in key or
                "nationalität" in key or
                "staatsangehörigkeit" in key
            ):
                return val

            if (("born" in key or "rojen" in key) and "," in val):
                return val.split(",")[-1].strip()

        # 3) birthplace
        birthplace = infobox.find("div", class_="birthplace")
        if birthplace:
            text = birthplace.get_text(" ", strip=True)
            if "," in text:
                return text.split(",")[-1].strip()

        # 4) infobox-data
        for td in infobox.find_all("td", class_="infobox-data"):
            text = td.get_text(" ", strip=True)
            if text in DRZAVE:
                return text

        # 5) <a> linki
        for a in infobox.find_all("a"):
            text = a.get_text(strip=True)

            if text in DRZAVE:
                return text

            drz = normaliziraj_pridevnik(text)
            if drz:
                return drz

        # 6) title atributi
        for a in infobox.find_all("a"):
            title = a.get("title", "").strip()
            if title in DRZAVE:
                return title

        # 7) href atributi
        for a in infobox.find_all("a"):
            href = a.get("href", "")
            for drzava in DRZAVE:
                if drzava.replace(" ", "_") in href:
                    return drzava

        # 8) pridevniške oblike držav
        for a in infobox.find_all("a"):
            text = a.get_text(strip=True)
            drz = normaliziraj_pridevnik(text)
            if drz:
                return drz

        # 9) fallback: prvi odstavek
        prvi_p = soup.find("p")
        if prvi_p:
            text = prvi_p.get_text(" ", strip=True)

            for drzava in DRZAVE:
                if drzava in text:
                    return drzava

            for word in text.split():
                drz = normaliziraj_pridevnik(word)
                if drz:
                    return drz

    return None
