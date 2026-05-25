import regex as re   # POZOR: uporabi "regex" knjižnico, ne "re"
import unicodedata
vzorec_ime = re.compile(r"^[\p{Lu}][\p{Ll}\p{M}\-]+( [\p{Lu}][\p{Ll}\p{M}\-]+){1,2}$",re.UNICODE)

def pocisti_ime(ime):
    if not ime:
        return None

    ime = re.sub(r"\[\d+\]", "", ime)      # odstrani reference
    ime = ime.replace("\xa0", " ")         # non-breaking space
    ime = re.sub(r"[^\p{L}\s\-]", "", ime) # pusti vse črke vseh jezikov
    ime = re.sub(r"\s+", " ", ime).strip()

    return ime if len(ime) > 1 else None


def je_pravo_ime(ime):
    if not ime:
        return False
    return bool(vzorec_ime.match(ime))


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

