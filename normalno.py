import re

def normaliziraj_drzavo(raw):
    if not raw:
        return None

    d = raw.strip().lower()

    # odstrani oklepaje
    d = re.sub(r"\(.*?\)", "", d)
    d = re.sub(r"\s+", " ", d).strip()

    # če je v nizu vejica → zadnji del je država
    if "," in d:
        d = d.split(",")[-1].strip()

    # ključne besede → standardizirana država
    mapping = {
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

    # direktni match
    if d in mapping:
        return mapping[d]

    # match po ključnih besedah
    for key, val in mapping.items():
        if key in d:
            return val

    # fallback
    return d.capitalize()
