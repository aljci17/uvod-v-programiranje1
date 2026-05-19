import csv

def shrani_csv_tekmovalci(ime_datoteke, podatki, drzave_tekmovalcev):
    with open(ime_datoteke, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Ime (ID)", "Zlato", "Srebro", "Bron", "Skupaj", "DrzavaID"])
        w.writerow(["Ime (ID)", "Zlato", "Srebro", "Bron", "Skupaj"])
        for ime, m in sorted(podatki.items(), key=lambda x: x[1][3], reverse=True):
            drzava_id = drzave_tekmovalcev.get(ime, "")
            ime_z_id=f"{ime} ({drzava_id})" if drzava_id else ime
            w.writerow([ime_z_id, m[0], m[1], m[2], m[3]])


def shrani_csv_drzave(ime_datoteke, drzave):
    with open(ime_datoteke, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["DrzavaID", "Drzava", "Zlato", "Srebro", "Bron", "Skupaj"])
        for drzava_id, podatki in sorted(drzave.items(), key=lambda x: x[1][4], reverse=True):
            ime_drzave = podatki[0]
            zlato, srebro, bron, skupaj = podatki[1], podatki[2], podatki[3], podatki[4]
            w.writerow([drzava_id, ime_drzave, zlato, srebro, bron, skupaj])
