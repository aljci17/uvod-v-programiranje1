# Projektna naloga za podatke o smučarskih skokih za sezone (1980-2026)

Ta python projekt avtomatizira:
            * pridobivanje podatkov o rezultatih svetovnega pokala v smučarskih skokih
            * lokalno shranjevanje (sranjevanje html datotek na računalnik) html datotek (cache)
            * čiščenje in obdelavo podatkov 
            * izluščanje medalj iz tabele
            * določanje države vsakega tekmovalca
            * normalizacija držav in dodelitev ID-jev (SLO, JPN)
            * izračun medalj po državah in tekmovalcih
            izvoz rezultatov v csv datoteke


## Struktura projekta

uvod-v-programiranje1/
|
|--Projektna_naloga/
|  |--drzave/
|     |--branje_drzav.py
|     |--drzave_id.py
|     |--drzavni_servis.py
|     |--normalno.py
|  |--tekmovalci/
|     |--ciscenje.py
|     |--imena.py
|  
|  |--cache.py
|  |--csv_delo.py
|  |--min.py