from drzave.branje_drzav import pridobi_drzavo_iz_wiki
from drzave.normalno import normaliziraj_drzavo
from drzave.drzave_id import drzava_v_id
from drzave.fis import najdi_fis_povezavo
from drzave.fis_selenium import prestej_fis_podiums_selenium


def obdela_tekmovalca(ime):
    drzava_raw = pridobi_drzavo_iz_wiki(ime)
    drzava = normaliziraj_drzavo(drzava_raw)
    drzava_id = drzava_v_id(drzava)

    fis_url = najdi_fis_povezavo(ime)
    medalje = prestej_fis_podiums_selenium(fis_url)

    return {
        "ime": ime,
        "drzava": drzava,
        "id": drzava_id,
        "zlato": medalje[0],
        "srebro": medalje[1],
        "bron": medalje[2],
        "skupaj": sum(medalje)
    }
