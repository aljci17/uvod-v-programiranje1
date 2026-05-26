import regex as re
import unicodedata

# ============================
# 1) REGEX za preverjanje imen
# ============================

vzorec_ime = re.compile(
    r"^[\p{Lu}][\p{Ll}\p{M}\-']+( [\p{Lu}][\p{Ll}\p{M}\-']+){1,2}$",
    re.UNICODE
)

# ============================
# 2) Funkcija: pocisti_ime
# ============================

def pocisti_ime(ime):
    if not ime:
        return None

    # Normalizacija Unicode (KLJUČNO!)
    ime = unicodedata.normalize("NFC", ime)

    # odstrani reference [1], [2] …
    ime = re.sub(r"\[\d+\]", "", ime)

    # odstrani nevidne presledke
    ime = ime.replace("\xa0", " ")

    # dovoli vse črke, kombinacijske znake, presledke, pomišljaje, apostrofe
    ime = re.sub(r"[^\p{Letter}\p{Mark}\s\-']", "", ime)

    # odstrani dvojne presledke
    ime = re.sub(r"\s+", " ", ime).strip()

    return ime if len(ime) > 1 else None

# ============================
# 3) Funkcija: je_pravo_ime
# ============================

def je_pravo_ime(ime):
    if not ime:
        return False
    return bool(vzorec_ime.match(ime))

# ============================
# 4) Funkcija: normaliziraj_ime
# ============================

def normaliziraj_ime(ime):
    if not ime:
        return None

    ime = unicodedata.normalize("NFC", ime)

    # odstrani reference
    ime = re.sub(r"\[\d+\]", "", ime)

    # odstrani oklepaje
    ime = re.sub(r"\(.*?\)", "", ime)

    # odstrani inicialke (npr. "K. Geiger")
    ime = re.sub(r"^[A-Z]\.\s*", "", ime)

    # normaliziraj presledke
    ime = " ".join(ime.split())

    # ============================
    # POSEBNI POPRAVKI (override)
    # ============================

    posebni_popravki = {
        # Nozomi — Wikipedia ima napačno verzijo
        "Nozomi Marujama": "Nozomi Maruyama",
        
        # Ryoyu / Ryōyū Kobayashi — različne napačne variante
        "Rjoju Kobajaši": "Ryoyu Kobayashi",
        
        "Jūki Itō": "Juki Ito",
        "Juki Itō": "Juki Ito"
    }

    if ime in posebni_popravki:
        ime = posebni_popravki[ime]

    return ime.strip()
