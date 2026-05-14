import requests
from bs4 import BeautifulSoup
import json

wiki_url = "https://sl.wikipedia.org/wiki/Svetovni_pokal_v_alpskem_smučanju"

headers={"user-Agent": "Mozilla/5.0"} #preprečimo blokiranje wikipedije

print(f"Zajemam stran: {wiki_url}")
odgovor=requests.get(wiki_url, headers=headers)
if odgovor.status_code == 200:
        ime_datoteke="Svetovni_pokal_v_smucarskih_skokih_2026.html"
        with open(ime_datoteke, "w", encoding="utf-8") as f:
            f.write(odgovor.text)
        print(f"Stran je shranjena v datoteko: {ime_datoteke}\n")
        juha=BeautifulSoup(odgovor.text,"html.parser")
        tabela=juha.find("table", {"class":"wikitable"})
        if tabela:
            podatki=[]
            vrstice=tabela.find_all("tr")
            for vrstica in vrstice[1:]:
                stolpci=vrstica.find_all(["td","th"])
                if len(stolpci)>=4:
                    try:
                        ime=stolpci[0].text.strip()
                        ime=ime.split("[")[0].strip() #odstranimo sklicevanja
                        zlato=int(stolpci[1].text.strip())
                        srebro=int(stolpci[2].text.strip())
                        bron=int(stolpci[3].text.strip())
                        podatki.append({
                            "Država": ime,
                            "zlato": zlato,
                            "srebro": srebro,
                            "bron": bron
                        })
                    except (ValueError,IndexError):
                        continue
            if podatki:
                sorted_podatki = sorted(podatki, key=lambda x: (x["zlato"], x["srebro"], x["bron"]), reverse=True)
                print(f"--- Urejeni podatki ---")
                print(f"{'Država':<20} | {'zlato':<6} | {'srebro':<6} | {'bron':<6}")
                print("-" *52)
                for item in sorted_podatki:
                    print(f"['Država':<20] | ['zlato':<6] | ['srebro':<6] | ['bron':<6]")
            else:
                print("V tabeli ni bilo mogoče najti številčnih podatkov.")
        else:
            print("Tabela na strani ni bila najdena")
else:
    print(f"Prišlo je do napake pri nalaganju strani. Statusna koda:{odgovor.status_code}")