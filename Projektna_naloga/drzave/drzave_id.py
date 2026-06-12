def drzava_v_id(drzava):
    if not drzava:
        return None
    if not drzava or drzava == "Neznano":
        return "UNK"  # unknown

    d = drzava.lower()

    mapping = {
        "slovenija": "SLO",
        "avstrija": "AUT",
        "nemčija": "GER",
        "norveška": "NOR",
        "japonska": "JPN",
        "poljska": "POL",
        "finska": "FIN",
        "švica": "SUI",
        "švedska": "SWE",
        "francija": "FRA",
        "italija": "ITA",
        "kanada": "CAN",
        "češka": "CZE",
        "estonija": "EST",
        "ukrajina": "UKR",
        "rusija": "RUS",
        "belorusija": "BLR",
        "južna koreja": "KOR",
        "združene države": "USA",
        "jugoslavija": "YUG",
    }

    if d in mapping:
        return mapping[d]

    # fallback: prve 3 črke
    return d[:3].upper()