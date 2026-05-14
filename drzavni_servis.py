import time
from branje_drzav import beri_drzavo_raw
from normalno import normaliziraj_državo

def pridobi_drzavo(ime):
    raw = beri_drzavo_raw(ime)
    drzava = normaliziraj_državo(raw)

    if drzava is None:
        return None

    if drzava.lower() == "neznano":
        return None

    time.sleep(0.3)
    return drzava
