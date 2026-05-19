from sezona.sezona import obdela_sezono
from tekmovalci.tekmovalec import obdela_tekmovalca
from izvoz_csv.csv_delo import shrani_csv_tekmovalci, shrani_csv_drzave

def glavni():
    vsi = set()

    for leto in range(1980, 2026 + 1):
        print(f"Obdelujem sezono {leto} ...")
        for ime in obdela_sezono(leto):
            vsi.add(ime)

    print(f"Najdenih tekmovalcev: {len(vsi)}")

    rezultati = {}
    for ime in vsi:
        print(f"Obdelujem tekmovalca: {ime}")
        rezultati[ime] = obdela_tekmovalca(ime)

    shrani_csv_tekmovalci("skoki_vsi_tekmovalci.csv", rezultati)
    shrani_csv_drzave("skoki_vse_drzave.csv", rezultati)

    print("Končano!")

if __name__ == "__main__":
    glavni()
