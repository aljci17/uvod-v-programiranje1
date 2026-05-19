from bs4 import BeautifulSoup
from cache import preberi_ali_prenesi

def pridobi_drzavo_iz_wiki(ime):
    ime_url = ime.replace(" ", "_")

    urls = [
        f"https://sl.wikipedia.org/wiki/{ime_url}",
        f"https://en.wikipedia.org/wiki/{ime_url}",
    ]

    for url in urls:
        html = preberi_ali_prenesi(url)
        if not html:
            continue

        soup = BeautifulSoup(html, "html.parser")
        infobox = soup.find("table", {"class": "infobox"})
        if not infobox:
            continue

        for row in infobox.find_all("tr"):
            th = row.find("th")
            td = row.find("td")
            if not th or not td:
                continue

            key = th.get_text(strip=True).lower()
            val = td.get_text(strip=True)

            if "reprezentanca" in key or "država" in key:
                return val

            if "nationality" in key or "country" in key:
                return val

            # Born: Oslo, Norway → vzemi zadnji del
            if ("born" in key or "rojen" in key) and "," in val:
                return val.split(",")[-1].strip()

    return None
