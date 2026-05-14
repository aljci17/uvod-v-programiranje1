import csv

def shrani_csv(ime, podatki):
    with open(ime, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Ime", "Zlato", "Srebro", "Bron", "Skupaj"])
        for k, m in sorted(podatki.items(), key=lambda x: x[1][3], reverse=True):
            w.writerow([k, m[0], m[1], m[2], m[3]])

