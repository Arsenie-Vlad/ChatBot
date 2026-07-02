import csv
import os

PROJECT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPORT_FILE = os.path.join(PROJECT_DIRECTORY, "data", "raport.csv")

RAPORT_HEADER = ["nume", "email", "scor", "data"]

def salveaza_rezultat(nume: str, email: str, scor: str, data: str) -> None:
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)

    fisier_exista = os.path.isfile(REPORT_FILE)

    with open(REPORT_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not fisier_exista or os.path.getsize(REPORT_FILE) == 0:
            writer.writerow(RAPORT_HEADER)
        
        writer.writerow([nume, email, scor, data])