from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()

def beri_drzavo_raw(name):
    name_url = name.replace(" ", "_")

    urls = [
        f"https://sl.wikipedia.org/wiki/{name_url}",
        f"https://en.wikipedia.org/wiki/{name_url}",
        f"https://sl.wikipedia.org/w/index.php?search={name_url}",
        f"https://en.wikipedia.org/w/index.php?search={name_url}"
    ]

    for url in urls:
        try:
            r = session.get(url)
            if r.status_code != 200:
                continue

            soup = BeautifulSoup(r.text, "html.parser")
            infobox = soup.find("table", {"class": "infobox"})
            if not infobox:
                continue

            for row in infobox.find_all("tr"):
                th = row.find("th")
                td = row.find("td")
                if not th or not td:
                    continue

                key = th.get_text().strip().lower()
                val = td.get_text().strip()

                if "reprezentanca" in key or "država" in key:
                    return val
                if "nationality" in key or "country" in key:
                    return val
                if "born" in key and "," in val:
                    return val.split(",")[-1].strip()

                if "club" in key or "team" in key:
                    return val

        except:
            continue

    return None
