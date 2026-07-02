from pathlib import Path

import pandas as pd
import streamlit as st
from .email_service import trimite_rapoarte

PROJECT_DIRECTORY = Path(__file__).resolve().parent.parent
REPORT_FILE = PROJECT_DIRECTORY / "data" / "raport.csv"

def afiseaza_dashboard() -> None:
    st.title("Dashboard de securitate")
    st.write("Analiza rezultatelor obținute la testul de securitate.")

    if not REPORT_FILE.exists() or REPORT_FILE.stat().st_size == 0:
        st.warning("Nu există încă rezultate salvate.")
        return
    
    try:
        raport = pd.read_csv(REPORT_FILE, encoding="utf-8-sig")
    except pd.errors.EmptyDataError:
        st.warning("Fișierul raport.csv este gol.")
        return
    
    coloane_necesare = {"nume", "email", "scor", "data"}

    if not coloane_necesare.issubset(raport.columns):
        st.error("Fișierul raport.csv nu conține coloanele necesare.")
        return
    
    scoruri = raport["scor"].astype(str).str.split('/', n=1, expand = True)

    if scoruri.shape[1] != 2:
        st.error("Scorurile din raport.csv nu au formatul corect.")
        return
    
    raport["puncte"] = pd.to_numeric(scoruri[0], errors="coerce")
    raport["total"] = pd.to_numeric(scoruri[1], errors="coerce")
    raport = raport.dropna(subset=["puncte", "total"])
    raport = raport[raport["total"] > 0]

    if raport.empty:
        st.warning("Nu există rezultate valide în raport.csv.")
        return
    
    raport["procent"] = raport["puncte"] / raport["total"] * 100
    raport["rezultat"] = raport["procent"].gt(50).map({
        True: "Promovat",
        False: "Nepromovat"
    })

    total_teste = len(raport)
    promovati = int((raport["procent"] > 50).sum())
    nepromovati = total_teste - promovati
    rata_promovare = promovati / total_teste * 100

    coloana1, coloana2, coloana3 = st.columns(3)
    coloana1.metric("Teste efectuate", total_teste)
    coloana2.metric("Teste promovate", promovati)
    coloana3.metric("Rata de promovare", f"{rata_promovare:.1f}%")

    st.subheader("Promovabilitatea testelor")

    date_grafic = pd.DataFrame({
    "Categorie": ["Promovat", "Nepromovat"],
    "Număr": [promovati, nepromovati],
    "Culoare": ["#94f594", "#d03939"],
    })

    st.bar_chart(
        date_grafic,
        x="Categorie",
        y="Număr",
        color="Culoare",
    )

    st.subheader("Rezultate individuale")

    tabel = raport[["nume", "email", "scor", "procent", "rezultat", "data"]].copy()
    tabel["procent"] = tabel["procent"].round(1).astype(str) + "%"

    tabel.columns = [
        "Nume",
        "Email",
        "Scor",
        "Procent",
        "Rezultat",
        "Data"
    ]

    st.dataframe(tabel, use_container_width=True)

    st.divider()

    st.subheader("Administrare")

    if st.button("Trimite rapoarte pe e-mail", use_container_width=True):
        try:
            trimite_rapoarte()
            st.success("Toate rapoartele au fost trimise.")
        except Exception as eroare:
            st.error(f"Eroare: {eroare}")