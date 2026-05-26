from bs4 import BeautifulSoup
from cache import preberi_ali_prenesi



def branje_drzavo_raw(ime):
    
    ime_url = ime.replace(" ", "_")

    urls = [
        f"https://sl.wikipedia.org/wiki/{ime_url}",
        f"https://en.wikipedia.org/wiki/{ime_url}",
    ]

    for url in urls:

        html = preberi_ali_prenesi(url)

        if not html:
            continue

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        infobox = soup.find(
            "table",
            class_=lambda x: x and "infobox" in x
        )

        if not infobox:
            continue

        # 1. najprej country-name
        country = infobox.find(
            "span",
            class_="country-name"
        )

        if country:

            a = country.find("a")

            if a:

                drzava = a.get_text(
                    strip=True
                )

                if drzava:
                    return drzava

        # 2. fallback
        for row in infobox.find_all("tr"):

            th = row.find("th")
            td = row.find("td")

            if not th or not td:
                continue

            key = th.get_text(
                strip=True
            ).lower()

            a = td.find("a")

            if a:
                val = a.get_text(
                    strip=True
                )
            else:
                val = td.get_text(
                    strip=True
                )

            # reprezentanca / država
            if (
                "reprezentanca" in key or
                "država" in key or
                "country" in key or
                "nationality" in key
            ):
                return val

            # fallback iz rojstva
            if (
                ("born" in key or "rojen" in key)
                and "," in val
            ):
                return val.split(",")[-1].strip()

    return None