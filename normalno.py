import re

def normaliziraj_državo(raw):
    if not raw:
        return None

    d = raw.strip().lower()
    d = re.sub(r"\(.*?\)", "", d)
    d = re.sub(r"\s+", " ", d)

    if "," in d:
        d = d.split(",")[-1].strip()

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

    for key, val in mapping.items():
        if key in d:
            return val

    return d.capitalize()
