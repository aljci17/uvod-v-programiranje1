import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
        wiki_url = "https://sl.wikipedia.org/wiki/Svetovni_pokal_v_smu%C4%8Darskih_skokih_2026"
        print(f"Zajem podatkov s strani: {wiki_url}")

def uredi_medalje(wiki_url):
    headers={"user-Agent": "Mozilla/5.0"} #preprečimo blokiranje wikipedije
    odgovor=requests.get(wiki_url, headers=headers)
    if odgovor.status_code != 200:
        print("Napaka pri nalaganju strani")
        return
    