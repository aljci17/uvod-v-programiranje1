import requests

def najdi_fis_id(ime):
    if ime in FIS_ID_CACHE:
        return FIS_ID_CACHE[ime]

    parts = ime.split()
    ime_fis = f"{parts[1]}%20{parts[0]}"  # PRIIMEK IME

    url = f"https://www.fis-ski.com/DB/general/athlete-biography/json/search?term={ime_fis}"

    try:
        data = requests.get(url, headers=HEADERS, timeout=15).json()
        results = data.get("items", [])
        if results:
            fis_id = results[0].get("competitorId")
            FIS_ID_CACHE[ime] = fis_id
            return fis_id
    except:
        pass

    FIS_ID_CACHE[ime] = None
    return None
