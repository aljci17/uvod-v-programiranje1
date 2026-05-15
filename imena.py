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

import unicodedata

def normaliziraj_ime(ime):
    if not ime:
        return None
    ime = ime.strip()
    ime = unicodedata.normalize("NFKD", ime)
    ime = "".join(c for c in ime if not unicodedata.combining(c))
    ime = ime.replace("  ", " ")
    return ime
