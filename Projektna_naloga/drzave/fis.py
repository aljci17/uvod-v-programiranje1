from bs4 import BeautifulSoup
from cache import preberi_ali_prenesi

# in-memory cache za FIS strani v enem zagonu
_fis_cache = {}

def najdi_fis_povezavo(ime):
    ime_url = ime.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{ime_url}"

    html = preberi_ali_prenesi(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    for a in soup.find_all("a", href=True):
        href = a["href"]

        # ignoriraj sidra
        if href.startswith("#"):
            continue

        # ignoriraj slike
        if href.endswith(".jpg") or href.endswith(".png"):
            continue

        low = href.lower()

        # PRAVI FIS PROFILI
        if "fis-ski" in low and "athlete" in low:
            if href.startswith("//"):
                return "https:" + href
            if href.startswith("/"):
                return "https://en.wikipedia.org" + href
            return href

    return None


from bs4 import BeautifulSoup
from cache import preberi_ali_prenesi

_fis_cache = {}

def prestej_fis_podiums(fis_url):
    if not fis_url:
        return [0, 0, 0]

    if fis_url in _fis_cache:
        return _fis_cache[fis_url]

    html = preberi_ali_prenesi(fis_url)
    if not html:
        _fis_cache[fis_url] = [0, 0, 0]
        return [0, 0, 0]

    soup = BeautifulSoup(html, "html.parser")

    zlato = srebro = bron = 0

    def varno_int(v):
        v = "".join(ch for ch in v if ch.isdigit())
        return int(v) if v else 0

    # poiščemo tabelo World Cup Podiums Individual
    ciljna = None
    for table in soup.find_all("table"):
        caption = table.find("caption")
        if not caption:
            continue
        cap = caption.get_text(strip=True).lower()
        if "world cup podiums" in cap:
            ciljna = table
            break


    if not ciljna:
        _fis_cache[fis_url] = [0, 0, 0]
        return [0, 0, 0]

    # header vrstica
    header_row = ciljna.find("tr")
    headers = [h.get_text(strip=True).lower() for h in header_row.find_all(["th", "td"])]

    def najdi_indeks(iskano):
        for i, h in enumerate(headers):
            if iskano in h:
                return i
        return None

    idx_p1 = najdi_indeks("position 1")
    idx_p2 = najdi_indeks("position 2")
    idx_p3 = najdi_indeks("position 3")

    if idx_p1 is None or idx_p2 is None or idx_p3 is None:
        _fis_cache[fis_url] = [0, 0, 0]
        return [0, 0, 0]

    # gremo po vrsticah s sezonami
    for row in ciljna.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) <= max(idx_p1, idx_p2, idx_p3):
            continue

        zlato += varno_int(cells[idx_p1].get_text(strip=True))
        srebro += varno_int(cells[idx_p2].get_text(strip=True))
        bron += varno_int(cells[idx_p3].get_text(strip=True))

    rezultat = [zlato, srebro, bron]
    _fis_cache[fis_url] = rezultat
    return rezultat
