def drzava_v_id(drzava):
    if not drzava or drzava == "Neznano":
        return "UNK"

    d = drzava.strip()

    # -----------------------------
    # 1) Mapping slovenskih kratic → angleške IOC/FIS kode
    # -----------------------------
    kratica_mapping = {
        "SLO": "SLO",
        "AVS": "AUT",
        "NEM": "GER",
        "ŠVI": "SUI",
        "SCH": "SUI",
        "KAN": "CAN",
        "ZDA": "USA",
        "JAP": "JPN",
        "CHI": "CHN",
        "SUO": "FIN",
        "ČEŠ": "CZE",
        "ŠVE": "SWE",
        "ROC": "RUS",
        "FIN": "FIN",
        "NOR": "NOR",
        "POL": "POL",
        "FRA": "FRA",
        "ITA": "ITA",
        "RUS": "RUS",
        "GER": "GER",
        "AUT": "AUT",
        "CAN": "CAN",
        "USA": "USA",
        "CZE": "CZE",
        "SWE": "SWE",
        "SUI": "SUI",
        "KOR": "KOR",
        "JPN": "JPN",
        "CHN": "CHN",
    }

    # Če je vnos že kratica (AVS, NEM, SLO …)
    d_upper = d.upper()
    if d_upper in kratica_mapping:
        return kratica_mapping[d_upper]

    # -----------------------------
    # 2) Mapping imen držav → IOC/FIS kode
    # -----------------------------
    mapping = {
        # SLOVENIA
        "slovenija": "SLO", "slovenia": "SLO", "slowenien": "SLO",

        # AUSTRIA
        "avstrija": "AUT", "austria": "AUT", "österreich": "AUT",

        # GERMANY
        "nemčija": "GER", "germany": "GER", "deutschland": "GER",

        # SWITZERLAND
        "švica": "SUI", "switzerland": "SUI", "schweiz": "SUI",
        "suisse": "SUI", "svizzera": "SUI",

        # ITALY
        "italija": "ITA", "italy": "ITA", "italia": "ITA",

        # FRANCE
        "francija": "FRA", "france": "FRA",

        # NORWAY
        "norveška": "NOR", "norway": "NOR", "norge": "NOR",

        # SWEDEN
        "švedska": "SWE", "sweden": "SWE", "sverige": "SWE",

        # FINLAND
        "finska": "FIN", "finland": "FIN", "suomi": "FIN",

        # POLAND
        "poljska": "POL", "poland": "POL", "polska": "POL",

        # CZECHIA
        "češka": "CZE", "czechia": "CZE", "czech republic": "CZE", "česko": "CZE",

        # SLOVAKIA
        "slovaška": "SVK", "slovakia": "SVK", "slovensko": "SVK",

        # RUSSIA
        "rusija": "RUS", "russia": "RUS", "rossiya": "RUS",

        # USA
        "zda": "USA", "usa": "USA",
        "united states": "USA", "united states of america": "USA",

        # CANADA
        "kanada": "CAN", "canada": "CAN",

        # JAPAN
        "japonska": "JPN", "japan": "JPN", "nippon": "JPN",

        # CHINA
        "kitajska": "CHN", "china": "CHN", "zhongguo": "CHN",

        # SOUTH KOREA
        "južna koreja": "KOR", "south korea": "KOR", "korea": "KOR", "hanguk": "KOR",

        # NORTH KOREA
        "severna koreja": "PRK", "north korea": "PRK",

        # NEIGHBORS
        "madžarska": "HUN", "hungary": "HUN", "magyarország": "HUN",
        "hrvaška": "CRO", "croatia": "CRO", "hrvatska": "CRO",

        # BALTICS
        "estonija": "EST", "estonia": "EST",
        "latvija": "LAT", "latvia": "LAT",
        "litva": "LTU", "lithuania": "LTU",

        # BALKANS
        "srbija": "SRB", "serbia": "SRB",
        "bosna in hercegovina": "BIH", "bosnia and herzegovina": "BIH",
        "črna gora": "MNE", "montenegro": "MNE",
        "severna makedonija": "MKD", "north macedonia": "MKD",

        # BENELUX
        "nizozemska": "NED", "netherlands": "NED", "nederland": "NED",
        "belgija": "BEL", "belgium": "BEL",
        "luksemburg": "LUX", "luxembourg": "LUX",

        # UK
        "velika britanija": "GBR", "united kingdom": "GBR",
        "great britain": "GBR", "britain": "GBR",

        # SPAIN & PORTUGAL
        "španija": "ESP", "spain": "ESP", "españa": "ESP",
        "portugalska": "POR", "portugal": "POR",

        # OCEANIA
        "avstralija": "AUS", "australia": "AUS",
        "nova zelandija": "NZL", "new zealand": "NZL",

        # OTHERS
        "kazahstan": "KAZ", "kazakhstan": "KAZ",
        "ukrajina": "UKR", "ukraine": "UKR",
        "belorusija": "BLR", "belarus": "BLR",
        "romunija": "ROU", "romania": "ROU",
        "bolgarija": "BUL", "bulgaria": "BUL",
    }

    d_lower = d.lower()
    if d_lower in mapping:
        return mapping[d_lower]

    # -----------------------------
    # 3) Fallback: prve 3 črke
    # -----------------------------
    return d_upper[:3]
