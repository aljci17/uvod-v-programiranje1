import time
from branje_drzav import beri_drzavo_raw
from normalno import normaliziraj_drzavo

def pridobi_drzavo(ime):
    raw = beri_drzavo_raw(ime)
    drzava = normaliziraj_drzavo(raw)

    # če ni države → preskoči
    if drzava is None:
        return None

    # če je neznano → preskoči
    if drzava.lower() == "neznano":
        return None

    # pavza, da ne preobremenimo Wikipedije
    time.sleep(0.3)

    return drzava

