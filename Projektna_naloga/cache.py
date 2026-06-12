import os
import re
from requests_html import HTMLSession
import requests

session = HTMLSession() # HTMLSession omogoča pošiljanje HTTP zahtev in enostavno parsanje HTML-ja

CACHE_DIR = "shranjene_strani"
os.makedirs(CACHE_DIR, exist_ok=True)

def url_v_ime(url):
    ime = url.replace("https://", "").replace("http://", "")
    ime = ime.replace("/", "_")

    # odstrani prepovedane znake za Windows
    ime = re.sub(r'[<>:"/\\|?*]', "_", ime)

    return ime + ".html"


session = requests.Session()

# odstrani vse cookie-je, ki jih session nosi s sabo
session.cookies.clear()

session.headers.update({
    "User-Agent": "Edge/148.0.3967.83 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "sl-SI,sl;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
})


def preberi_ali_prenesi(url):
    ime = url_v_ime(url)
    pot = os.path.join(CACHE_DIR, ime)

    # če datoteka obstaja → beri lokalno
    if os.path.exists(pot):
        with open(pot, "r", encoding="utf-8") as f:
            html = f.read()

        # ============================
        # IGNORIRAJ 404 STRANI
        # ============================
        if (
            "404 Not Found" in html or
            "page does not exist" in html or
            "Wikipedija nima članka" in html or
            "Wikipedia does not have an article" in html
        ):
            return None

        return html

    # če datoteka NE obstaja → NE hodi na internet
    return None


