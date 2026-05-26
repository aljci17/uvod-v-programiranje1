from bs4 import BeautifulSoup
from cache import preberi_ali_prenesi
import regex as re

# ============================
# PREIMENOVANJA (poročna imena)
# ============================

preimenovanja = {
    "Nika Križnar": "Nika Vodan",
    "Urša Bogataj": "Urša Križnar",
    "Chiara Hölzl": "Chiara Kreuzer",
}

def popravi_preimenovanja(ime):
    ime = ime.strip()
    if ime in preimenovanja:
        print(f"🔄 preimenovanja: '{ime}' → '{preimenovanja[ime]}'")
    return preimenovanja.get(ime, ime)


# ============================
# ZDRUŽEVANJE MEDALJ
# ============================

def zdruzi_dvojna_imena(rezultati, preimenovanja):

    print("\n🔧 Začenjam združevanje dvojnih imen...")

    skupine = {}

    for staro, novo in preimenovanja.items():
        skupine.setdefault(novo, set()).add(staro)
        skupine[novo].add(novo)

    for glavno_ime, imena_v_skupini in skupine.items():

        print(f"\n🔄 Združujem skupino: {imena_v_skupini}")
        print(f"➡️ Glavno ime: {glavno_ime}")

        if glavno_ime not in rezultati:
            rezultati[glavno_ime] = {"zlato": 0, "srebro": 0, "bron": 0}

        for ime in imena_v_skupini:
            if ime in rezultati:
                print(f"   • prenašam medalje iz: {ime}")
                for tip in ["zlato", "srebro", "bron"]:
                    rezultati[glavno_ime][tip] += rezultati[ime][tip]

        for ime in imena_v_skupini:
            if ime != glavno_ime and ime in rezultati:
                print(f"   ❌ brišem staro ime: {ime}")
                del rezultati[ime]

    print("\n✅ Združevanje končano.")
    return rezultati


# ============================
# SEZNAM DRŽAV
# ============================

DRZAVE = {
    "Slovenia", "Slovenija",
    "Austria", "Avstrija",
    "Norway", "Norveška",
    "Sweden", "Švedska",
    "Finland", "Finska",
    "Germany", "Nemčija", "Deutschland",
    "Poland", "Poljska",
    "Japan", "Japonska",
    "China", "Kitajska",
    "Italy", "Italija",
    "France", "Francija",
    "Canada", "Kanada",
    "USA", "ZDA",
    "South Korea", "Južna Koreja",
    "Czech Republic", "Češka",
    "Switzerland", "Švica",
    "Russia", "Rusija"
}


# ============================
# BRANJE DRŽAVE
# ============================

def branje_drzavo_raw(ime):
    
    print("\n=======================================")
    print(f"🏁 Začenjam iskanje države za: {ime}")

    ime = popravi_preimenovanja(ime)
    ime_url = ime.replace(" ", "_")

    urls = [
        f"https://sl.wikipedia.org/wiki/{ime_url}",
        f"https://en.wikipedia.org/wiki/{ime_url}",
        f"https://de.wikipedia.org/wiki/{ime_url}",
    ]

    for url in urls:

        print(f"\n🌐 Preverjam URL: {url}")

        html = preberi_ali_prenesi(url)
        if not html:
            print("❌ Ni HTML-ja (napaka ali 404)")
            continue

        soup = BeautifulSoup(html, "html.parser")

        # robusten infobox matcher
        infobox = soup.find(
            "table",
            class_=lambda x: x and (
                ("infobox" in x) if isinstance(x, str)
                else any("infobox" in c for c in x)
            )
        )

        # 1) najprej preveri, ali infobox sploh obstaja
        if not infobox:
            print("❌ Infobox NI najden")
            continue

        print("✅ Infobox najden")

        # 2) preveri, ali gre za kraj (geografski infobox)
        infobox_classes = infobox.get("class", [])

        if isinstance(infobox_classes, str):
            infobox_classes = infobox_classes.split()

        if any(c in infobox_classes for c in [
            "geography", "settlement", "place", "country", "municipality", "location"
        ]):
            print("⚠️ Stran ni oseba (geografski infobox) → preskočim")
            continue

        # -------------------------
        # 1) country-name
        # -------------------------
        country = infobox.find("span", class_="country-name")
        if country:
            a = country.find("a")
            if a:
                drz = a.get_text(strip=True)
                print(f"🎯 Fallback 1: country-name → {drz}")
                return drz

        # -------------------------
        # 2) pregled vrstic
        # -------------------------
        print("🔍 Fallback 2: pregled vrstic")
        for row in infobox.find_all("tr"):

            th = row.find("th")
            td = row.find("td")
            if not th or not td:
                continue

            key = th.get_text(strip=True).lower()
            a = td.find("a")
            val = a.get_text(strip=True) if a else td.get_text(strip=True)

            print(f"   • key='{key}', val='{val}'")

            if (
                "reprezentanca" in key or
                "država" in key or
                "country" in key or
                "nationality" in key or
                "nationalität" in key or
                "staatsangehörigkeit" in key
            ):
                print(f"🎯 Fallback 2: najdena država → {val}")
                return val

            if (("born" in key or "rojen" in key) and "," in val):
                drz = val.split(",")[-1].strip()
                print(f"🎯 Fallback 2: iz rojstva → {drz}")
                return drz

        # -------------------------
        # 3) birthplace
        # -------------------------
        print("🔍 Fallback 3: birthplace")
        birthplace = infobox.find("div", class_="birthplace")
        if birthplace:
            text = birthplace.get_text(" ", strip=True)
            print(f"   • birthplace: '{text}'")
            if "," in text:
                drz = text.split(",")[-1].strip()
                print(f"🎯 Fallback 3: iz birthplace → {drz}")
                return drz

        # -------------------------
        # 4) infobox-data
        # -------------------------
        print("🔍 Fallback 4: infobox-data")
        for td in infobox.find_all("td", class_="infobox-data"):
            text = td.get_text(" ", strip=True)
            print(f"   • infobox-data: '{text}'")
            if text in DRZAVE:
                print(f"🎯 Fallback 4: najdena država → {text}")
                return text

        # -------------------------
        # 5) <a> linki
        # -------------------------
        print("🔍 Fallback 5: <a> linki")
        for a in infobox.find_all("a"):
            text = a.get_text(strip=True)
            if text in DRZAVE:
                print(f"🎯 Fallback 5: najdena država → {text}")
                return text

        # -------------------------
        # 6) title atributi
        # -------------------------
        print("🔍 Fallback 6: title atributi")
        for a in infobox.find_all("a"):
            title = a.get("title", "").strip()
            if title in DRZAVE:
                print(f"🎯 Fallback 6: najdena država → {title}")
                return title

        # -------------------------
        # 7) href atributi
        # -------------------------
        print("🔍 Fallback 7: href atributi")
        for a in infobox.find_all("a"):
            href = a.get("href", "")
            for drzava in DRZAVE:
                if drzava.replace(" ", "_") in href:
                    print(f"🎯 Fallback 7: najdena država → {drzava}")
                    return drzava

        print("⚠️ Noben fallback ni našel države na tem URL-ju")

    print("❌ Država NI najdena")
    return None
