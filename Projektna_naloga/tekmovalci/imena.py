import re

vzorec_ime = re.compile(r"^[A-ZÀ-Ž][a-zà-ž\-]+( [A-ZÀ-Ž][a-zà-ž\-]+){1,2}$")

def pocisti_ime(ime):
    if not ime:
        return None
    ime = re.sub(r"\[\d+\]", "", ime)
    ime = ime.replace("\xa0", " ").strip()
    ime = re.sub(r"[^A-Za-zÀ-ž\s\-]", "", ime)
    ime = re.sub(r"\s+", " ", ime)
    return ime if len(ime) > 1 else None

def je_pravo_ime(ime):
    if not ime:
        return False
    return bool(vzorec_ime.match(ime))

import re
import unicodedata

def normaliziraj_ime(ime):
    if not ime:
        return None

    # odstrani reference [1], [2] …
    ime = re.sub(r"\[\d+\]", "", ime)

    # odstrani oklepaje
    ime = re.sub(r"\(.*?\)", "", ime)

    # odstrani unicode naglase
    ime = unicodedata.normalize("NFKD", ime).encode("ascii", "ignore").decode()

    # odstrani inicialke
    ime = re.sub(r"^[A-Z]\.\s*", "", ime)

    # odstrani dvojne presledke
    ime = " ".join(ime.split())

    return ime.strip()

