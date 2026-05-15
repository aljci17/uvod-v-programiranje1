import time
from branje_drzav import branje_drzavo_raw
from normalno import normaliziraj_drzavo

def pridobi_drzavo(ime):
    raw = branje_drzavo_raw(ime)
    drzava = normaliziraj_drzavo(raw)

    if drzava is None:
        return None

    if drzava.lower() == "neznano":
        return None

    time.sleep(0.2)
    return drzava
