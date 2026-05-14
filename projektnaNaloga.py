from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv
import re
import time

session = HTMLSession()

# ---------------------------------------------------------
# ČIŠČENJE IMEN
# ---------------------------------------------------------

def pocisti_ime(ime):
    if not ime:
        return None
    ime = re.sub(r"\[\d+\]", "", ime)
    ime = ime.replace("\xa0", " ").strip()
    ime = re.sub(r"[^A-Za-zÀ-ž\s\-]", "", ime)
    ime = re.sub(r"\s+", " ", ime)
    return ime if len(ime) > 1 else None


# ---------------------------------------------------------
# PRAVO IME (2–3 besede, velika začetnica)
# ---------------------------------------------------------

vzorec_ime = re.compile(r"^[A-ZÀ-Ž][a-zà-ž\-]+( [A-ZÀ-Ž][a-zà-ž\-]+){1,2}$")

def je_pravo_ime(ime):
    if not ime:
        return False
    return bool(vzorec_ime.match(ime))


# ---------------------------------------------------------
# NORMALIZACIJA DRŽAV
# ---------------------------------------------------------

def normaliziraj_drzavo(drzava):
    if not drzava:
        return "Neznano"

    d = drzava.strip().lower()
    d = d.replace("(", "").replace(")", "")

    zamenjave = {
        "slovenia": "slovenija",
        "slovene": "slovenija",
        "slovenska": "slovenija",
        "austria": "avstrija",
        "österreich": "avstrija",
        "germany": "nemčija",
        "deutschland": "nemčija",
        "norway": "norveška",
        "norge": "norveška",
        "japan": "japonska",
        "poland": "poljska",
        "finland": "finska",
        "switzerland": "švica",
        "sweden": "švedska",
        "france": "francija",
        "italy": "italija",
        "canada": "kanada",
        "usa": "združene države",
        "united states": "združene države",
        "czech republic": "češka",
        "czechia": "češka",
        "estonia": "estonija",
        "ukraine": "ukrajina",
        "russia": "rusija",
        "belarus": "belorusija",
        "south korea": "južna koreja",
        "korea": "južna koreja",
    }

    if d in zamenjave:
        return zamenjave[d]

    deli = d.split()
    if len(deli) > 1:
        zadnja = deli[-1]
        if zadnja in zamenjave:
            return zamenjave[zadnja]

    return d.capitalize()


# ---------------------------------------------------------
# SAMODEJNO ISKANJE DRŽAVE SKAKALCA NA WIKIPEDIJI
# ---------------------------------------------------------

def najdi_drzavo(ime):
    ime_url = ime.replace(" ", "_")

    urls = [
        f"https://sl.wikipedia.org/wiki/{ime_url}",
        f"https://en.wikipedia.org/wiki/{ime_url}",
        f"https://sl.wikipedia.org/w/index.php?search={ime_url}",
        f"https://en.wikipedia.org/w/index.php?search={ime_url}"
    ]

    for url in urls:
        try:
            r = session.get(url)
            if r.status_code != 200:
                continue

            juha = BeautifulSoup(r.text, "html.parser")
            infobox = juha.find("table", {"class": "infobox"})
            if not infobox:
                continue

            for vrstica in infobox.find_all("tr"):
                glava = vrstica.find("th")
                vrednost = vrstica.find("td")

                if not glava or not vrednost:
                    continue

                naslov = glava.get_text().strip().lower()
                vsebina = vrednost.get_text().strip()

                if "reprezentanca" in naslov:
                    return vsebina
                if "država" in naslov:
                    return vsebina
                if "rojen" in naslov and "," in vsebina:
                    return vsebina.split(",")[-1].strip()

                if "nationality" in naslov:
                    return vsebina
                if "country" in naslov:
                    return vsebina
                if "born" in naslov and "," in vsebina:
                    return vsebina.split(",")[-1].strip()

                if "club" in naslov or "team" in naslov:
                    if "(" in vsebina and ")" in vsebina:
                        drzava = vsebina.split("(")[-1].replace(")", "").strip()
                        return drzava

        except:
            continue

    return "Neznano"


# ---------------------------------------------------------
# IZLOČANJE MEDALJ IZ TABEL
# ---------------------------------------------------------

def izloci_medalje_iz_tabele(tabela):
    medalje = {}

    for vrstica in tabela.find_all("tr"):
        celice = vrstica.find_all("td")
        if len(celice) < 7:
            continue

        w = pocisti_ime(celice[4].get_text())
        s = pocisti_ime(celice[5].get_text())
        b = pocisti_ime(celice[6].get_text())

        for i, ime in enumerate([w, s, b]):
            if ime and je_pravo_ime(ime):
                medalje.setdefault(ime, [0, 0, 0])
                medalje[ime][i] += 1

    return medalje


# ---------------------------------------------------------
# OBRAVNAVA ENE SEZONE
# ---------------------------------------------------------

def obdela_slovensko_sezono(leto):
    url = f"https://sl.wikipedia.org/wiki/Svetovni_pokal_v_smu%C4%8Darskih_skokih_{leto}"
    r = session.get(url)

    if r.status_code != 200:
        return None

    juha = BeautifulSoup(r.text, "html.parser")

    moski = {}
    zenske = {}

    for h in juha.find_all(["h2", "h3"]):
        naslov = h.get_text().lower()

        if "moški" in naslov:
            tabela = h.find_next("table")
            if tabela:
                moski = izloci_medalje_iz_tabele(tabela)

        if "ženske" in naslov:
            tabela = h.find_next("table")
            if tabela:
                zenske = izloci_medalje_iz_tabele(tabela)

    return moski, zenske


# ---------------------------------------------------------
# GLAVNI PROGRAM – SEZONE 1980–2026
# ---------------------------------------------------------

vse_sezone = list(range(1980, 2027))

moski_vse = {}
zenske_vse = {}

for leto in vse_sezone:
    rezultat = obdela_slovensko_sezono(leto)
    if rezultat is None:
        continue

    moski, zenske = rezultat

    for ime, m in moski.items():
        moski_vse.setdefault(ime, [0, 0, 0])
        for i in range(3):
            moski_vse[ime][i] += m[i]

    for ime, m in zenske.items():
        zenske_vse.setdefault(ime, [0, 0, 0])
        for i in range(3):
            zenske_vse[ime][i] += m[i]


# ---------------------------------------------------------
# DODAJ SKUPAJ
# ---------------------------------------------------------

def dodaj_skupaj(podatki):
    novi = {}
    for ime, (z, s, b) in podatki.items():
        novi[ime] = [z, s, b, z + s + b]
    return novi

moski_vse = dodaj_skupaj(moski_vse)
zenske_vse = dodaj_skupaj(zenske_vse)


# ---------------------------------------------------------
# SKUPNI CSV (moški + ženske)
# ---------------------------------------------------------

skupno = {}

for ime, m in moski_vse.items():
    skupno.setdefault(ime, [0, 0, 0, 0])
    for i in range(4):
        skupno[ime][i] += m[i]

for ime, m in zenske_vse.items():
    skupno.setdefault(ime, [0, 0, 0, 0])
    for i in range(4):
        skupno[ime][i] += m[i]


# ---------------------------------------------------------
# CSV PO DRŽAVAH (z normalizacijo)
# ---------------------------------------------------------

drzave = {}

for ime, m in skupno.items():
    drzava_raw = najdi_drzavo(ime)
    drzava = normaliziraj_drzavo(drzava_raw)
    time.sleep(0.3)

    drzave.setdefault(drzava, [0, 0, 0, 0])
    for i in range(4):
        drzave[drzava][i] += m[i]


# ---------------------------------------------------------
# SHRANI CSV
# ---------------------------------------------------------

def shrani_csv(ime, podatki):
    with open(ime, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Ime", "Zlato", "Srebro", "Bron", "Skupaj"])
        for k, m in sorted(podatki.items(), key=lambda x: x[1][3], reverse=True):
            w.writerow([k, m[0], m[1], m[2], m[3]])

shrani_csv("skoki_moski.csv", moski_vse)
shrani_csv("skoki_zenske.csv", zenske_vse)
shrani_csv("skoki_skupno.csv", skupno)

with open("skoki_drzave.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Država", "Zlato", "Srebro", "Bron", "Skupaj"])
    for k, m in sorted(drzave.items(), key=lambda x: x[1][3], reverse=True):
        w.writerow([k, m[0], m[1], m[2], m[3]])

print("Končano → ustvarjeni so skoki_moski.csv, skoki_zenske.csv, skoki_skupno.csv, skoki_drzave.csv")
