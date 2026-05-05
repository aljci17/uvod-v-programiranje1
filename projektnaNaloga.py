import requests
from bs4 import BeautifulSoup
import json

wiki_url = "https://sl.wikipedia.org/wiki/Svetovni_pokal_v_smučarskih_skokih_2026"

headers={"user-Agent": "Mozilla/5.0"} #preprečimo blokiranje wikipedije

print(f"Zajemam stran: {wiki_url}")
odgovor=requests.get(wiki_url, headers=headers)
if odgovor.status_code == 200:
        ime_datoteke="Svetovni_pokal_v_smucarskih_skokih_2026.html"
        with open(ime_datoteke, "w", encoding="utf-8") as f:
            f.write(odgovor.text)
        print(f"Stran je shranjena v datoteko: {ime_datoteke}\n")
        juha=BeautifulSoup(odgovor.text,"html.parser")