from requests_html import HTMLSession
from bs4 import BeautifulSoup


session = HTMLSession()

def normaliziraj_drzavo(drzava):
    if not drzava:
        return "Neznano"

    d = drzava.strip().lower()
    d = d.replace("(", "").replace(")", "")

    zamenjave = {
        "slovenia": "slovenija",
        "slovene": "slovenija",
        "slovenska": "slovenija",
        "austria": "avstrija",
        "österreich": "avstrija",
        "germany": "nemčija",
        "deutschland": "nemčija",
        "norway": "norveška",
        "norge": "norveška",
        "japan": "japonska",
        "usa": "združene države",
        "united states": "združene države",
        "czech republic": "češka",
        "czechia": "češka",
    }

    if d in zamenjave:
        return zamenjave[d]

    deli = d.split()
    if len(deli) > 1:
        zadnja = deli[-1]
        if zadnja in zamenjave:
            return zamenjave[zadnja]

    return d.capitalize()


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

                if "reprezentanca" in naslov:
                    return normaliziraj_drzavo(vsebina)
                if "država" in naslov:
                    return normaliziraj_drzavo(vsebina)
                if "rojen" in naslov and "," in vsebina:
                    return normaliziraj_drzavo(vsebina.split(",")[-1].strip())

                if "nationality" in naslov:
                    return normaliziraj_drzavo(vsebina)
                if "country" in naslov:
                    return normaliziraj_drzavo(vsebina)
                if "born" in naslov and "," in vsebina:
                    return normaliziraj_drzavo(vsebina.split(",")[-1].strip())

                if "club" in naslov or "team" in naslov:
                    if "(" in vsebina and ")" in vsebina:
                        drzava = vsebina.split("(")[-1].replace(")", "").strip()
                        return normaliziraj_drzavo(drzava)

        except:
            continue

    return "Neznano"
