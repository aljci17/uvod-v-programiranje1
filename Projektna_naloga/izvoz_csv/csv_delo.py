import csv

def shrani_csv_tekmovalci(ime_datoteke, tekmovalci):
    with open(ime_datoteke, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Ime (ID)", "Zlato", "Srebro", "Bron", "Skupaj"])

        for ime, d in sorted(tekmovalci.items(), key=lambda x: x[1]["skupaj"], reverse=True):
            oznaka = f'{ime} ({d.get("id") or "UNK"})' if d["id"] else ime
            w.writerow([oznaka, d["zlato"], d["srebro"], d["bron"], d["skupaj"]])


def shrani_csv_drzave(ime_datoteke, tekmovalci):
    drzave = {}

    for d in tekmovalci.values():
        if not d["id"]:
            continue

        if d["id"] not in drzave:
            drzave[d["id"]] = [d["drzava"], 0, 0, 0, 0]

        drzave[d["id"]][1] += d["zlato"]
        drzave[d["id"]][2] += d["srebro"]
        drzave[d["id"]][3] += d["bron"]
        drzave[d["id"]][4] += d["skupaj"]

    with open(ime_datoteke, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["DrzavaID", "Drzava", "Zlato", "Srebro", "Bron", "Skupaj"])

        for idd, podatki in sorted(drzave.items(), key=lambda x: x[1][4], reverse=True):
            w.writerow([idd] + podatki)
