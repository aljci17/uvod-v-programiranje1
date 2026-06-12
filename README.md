# Projektna naloga za podatke o smučarskih skokih za sezone (2012-2026)

Ta projekt obravnava celovit pristop k avtomatiziranemu zbiranju, obdelavi in analizi podatkov o rezultatih svetovnega pokala v smučarskih skokih. Glavni cilj je vzpostaviti sistem, ki omogoča natančno, ponovljivo in pregledno obdelavo podatkov skozi dve desetletij tekmovanj.

Ta python projekt avtomatizira:
            * pridobivanje podatkov o rezultatih svetovnega pokala v smučarskih skokih (2012-2026)
            * lokalno shranjevanje (sranjevanje html datotek na računalnik) html datotek (cache)
            * čiščenje in obdelavo podatkov 
            * izluščanje medalj iz tabele
            * določanje države vsakega tekmovalca
            * normalizacija držav in dodelitev ID-jev (SLO, JPN)
            * izračun medalj po državah in tekmovalcih
            * izvoz rezultatov v csv datoteke


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
|     |--preimenovanja.py
|  
|  |--cache.py
|  |--csv_delo.py
|  |--main.py

## Zagon programa
Celoten sistem se zažene preko glavne datoteke main.py, ki povezuje vse module in skrbi za zaporedno izvajanje posameznih korakov — od pridobivanja podatkov do končnega izvoza.

## Motivacija za izbiro teme
Za to temo sem se odločila, ker sem velika navdušenka zimskih športov, še posebej smučarskih skokov. Projekt mi je omogočil združiti osebno zanimanje s programerskim znanjem ter ustvariti orodje, ki lahko analizira več kot štiri desetletja rezultatov tega športa.