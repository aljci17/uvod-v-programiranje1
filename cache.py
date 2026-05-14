import os
import re
from requests_html import HTMLSession

session = HTMLSession()

CACHE_DIR = "shranjene_strani"
os.makedirs(CACHE_DIR, exist_ok=True)

def url_v_ime(url):
    ime = url.replace("https://", "").replace("http://", "")
    ime = ime.replace("/", "_")

    # odstrani prepovedane znake za Windows
    ime = re.sub(r'[<>:"/\\|?*]', "_", ime)

    return ime + ".html"

def preberi_ali_prenesi(url):
    ime = url_v_ime(url)
    pot = os.path.join(CACHE_DIR, ime)

    # če datoteka obstaja → beri lokalno
    if os.path.exists(pot):
        with open(pot, "r", encoding="utf-8") as f:
            return f.read()

    # sicer prenesi
    r = session.get(url)
    if r.status_code != 200:
        return None

    with open(pot, "w", encoding="utf-8") as f:
        f.write(r.text)

    return r.text
