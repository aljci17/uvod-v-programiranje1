from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

_fis_cache = {}

def prestej_fis_podiums_selenium(fis_url):
    if not fis_url:
        return [0, 0, 0]

    if fis_url in _fis_cache:
        return _fis_cache[fis_url]

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get(fis_url)
    time.sleep(2)

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    zlato = srebro = bron = 0

    def varno_int(v):
        v = "".join(ch for ch in v if ch.isdigit())
        return int(v) if v else 0

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
