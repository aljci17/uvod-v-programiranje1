import time
from .branje_drzav import branje_drzavo_raw
from .normalno import normaliziraj_drzavo
from .drzave_id import drzava_v_id


def pridobi_drzavo(ime):
    raw = branje_drzavo_raw(ime)
    drzava = normaliziraj_drzavo(raw)

    if drzava is None or drzava.lower() == "neznano":
        return "Neznana", -1

    time.sleep(0.2)
    return drzava,drzava_v_id(drzava)