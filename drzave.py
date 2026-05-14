from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import time

session = HTMLSession()

# -------------------------------
# NORMALIZACIJA DRŽAV
# -------------------------------

def normaliziraj_drzavo(drzava):
    if not drzava:
        return "Neznano"

    d = drzava.strip()

    # odstrani vse v oklepajih
    d = re.sub(r"\(.*?\)", "", d)

    # zamenjaj več presledkov z enim
    d = re.sub(r"\s+", " ", d)

    d = d.strip().lower()

    # če je v nizu vejica, pogosto zadnji del pomeni državo
    if "," in d:
        d = d.split(",")[-1].strip()

    # osnovne zamenjave (ključne besede)
    zamenjave = {
        "sloven": "slovenija",
        "austria": "avstrija",
        "österreich": "avstrija",
        "german": "nemčija",
        "deutschland": "nemčija",
        "norway": "norveška",
        "norge": "norveška",
        "japan": "japonska",
        "poland": "poljska",
        "finland": "finska",
        "switzerland": "švica",
        "sweden": "švedska",
        "france": "francija",
        "italy": "italija",
        "canada": "kanada",
        "czech republic": "češka",
        "czechia": "češka",
        "estonia": "estonija",
        "ukraine": "ukrajina",
        "russia": "rusija",
        "belarus": "belorusija",
        "south korea": "južna koreja",
        "korea": "južna koreja",
        "usa": "združene države",
        "united states": "združene države",
    }

    # najprej direktni match
    if d in zamenjave:
        return zamenjave[d]

    # potem po ključnih besedah v nizu
    for kljuc, cilj in zamenjave.items():
        if kljuc in d:
            return cilj

    # če je več besed, poskusi zadnjo
    deli = d.split()
    if len(deli) > 1:
        zadnja = deli[-1]
        if zadnja in zamenjave:
            return zamenjave[zadnja]

    # prva črka velika
    return d.capitalize() if d else "Neznano"


# -------------------------------
# ISKANJE DRŽAVE NA WIKIPEDIJI
# -------------------------------

def najdi_drzavo(ime):
    ime_url = ime.replace(" ", "_")

    urls = [
        f"https://sl.wikipedia.org/wiki/{ime_url}",
        f"https://en.wikipedia.org/wiki/{ime_url}",
        f"https://sl.wikipedia.org/w/index.php?search={ime_url}",
        f"https://en.wikipedia.org/w/index.php?search={ime_url}"
    ]

    for url in urls:
        try:
            r = session.get(url)
            if r.status_code != 200:
                continue

            juha = BeautifulSoup(r.text, "html.parser")
            infobox = juha.find("table", {"class": "infobox"})
            if not infobox:
                continue

            for vrstica in infobox.find_all("tr"):
                glava = vrstica.find("th")
                vrednost = vrstica.find("td")

                if not glava or not vrednost:
                    continue

                naslov = glava.get_text().strip().lower()
                vsebina = vrednost.get_text().strip()

                # slovenska wiki
                if "reprezentanca" in naslov or "država" in naslov:
                    return normaliziraj_drzavo(vsebina)

                if "rojen" in naslov and "," in vsebina:
                    return normaliziraj_drzavo(vsebina)

                # angleška wiki
                if "nationality" in naslov or "country" in naslov:
                    return normaliziraj_drzavo(vsebina)

                if "born" in naslov and "," in vsebina:
                    return normaliziraj_drzavo(vsebina)

                # klub / ekipa z državo v oklepaju
                if "club" in naslov or "team" in naslov:
                    return normaliziraj_drzavo(vsebina)

        except:
            continue

    return "Neznano"
