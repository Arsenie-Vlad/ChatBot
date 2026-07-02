from pathlib import Path
import smtplib
from email.message import EmailMessage

import pandas as pd

from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

PROJECT_DIRECTORY = Path(__file__).resolve().parent.parent
REPORT_FILE = PROJECT_DIRECTORY / "data" / "raport.csv"


def trimite_rapoarte() -> None:
    raport = pd.read_csv(REPORT_FILE)

    scoruri = raport["scor"].str.split("/", expand=True)
    raport["puncte"] = scoruri[0].astype(int)
    raport["total"] = scoruri[1].astype(int)
    raport["procent"] = raport["puncte"] / raport["total"] * 100

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        for email, utilizator in raport.groupby("email"):
            nume = utilizator.iloc[0]["nume"]

            nr_teste = len(utilizator)
            media = utilizator["procent"].mean()
            maxim = utilizator["procent"].max()
            minim = utilizator["procent"].min()
            ultimul = utilizator.iloc[-1]["procent"]

            mesaj = f"""
Salut, {nume}!

Acesta este raportul tău GuardOT.

Număr teste efectuate: {nr_teste}
Media rezultatelor: {media:.1f}%
Cel mai bun rezultat: {maxim:.1f}%
Cel mai slab rezultat: {minim:.1f}%
Ultimul rezultat: {ultimul:.1f}%

Mulțumim pentru utilizarea GuardOT!
"""

            mail = EmailMessage()
            mail["Subject"] = "Raport GuardOT"
            mail["From"] = EMAIL_ADDRESS
            mail["To"] = email

            mail.set_content(mesaj)

            smtp.send_message(mail)