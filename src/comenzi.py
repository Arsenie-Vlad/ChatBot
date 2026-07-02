from pathlib import Path
import streamlit as st

from .citire_date import citeste_fisier

PROJECT_DIRECTORY = Path(__file__).resolve().parent.parent

CURSURI_FILE = PROJECT_DIRECTORY / "data" / "cursuri.json"
QUIZ_FILE = PROJECT_DIRECTORY / "data" / "quiz.json"

def comanda_curs() -> str:

    cursuri = citeste_fisier(str(CURSURI_FILE))
    randuri_raspuns = []

    for curs in cursuri.values():
        randuri_raspuns.append(
            f"### {curs['titlu']}"
        )

        continut = curs["continut"]

        if isinstance(continut, list):
            for paragraf in continut:
                randuri_raspuns.append(paragraf)
        else:
            randuri_raspuns.append(continut)

        randuri_raspuns.append("---")

    return "\n\n".join(randuri_raspuns)

def comanda_test() -> list:

    quiz = citeste_fisier(str(QUIZ_FILE))

    if not isinstance(quiz, list):
        raise ValueError(
            "Fișierul quiz.json trebuie să conțină o listă."
        )

    return quiz

def proceseaza_comanda(input_utilizator: str) -> str:
    comanda = input_utilizator.lower().split()[0]

    if comanda == "/curs":

        try:
            raspuns_bot = comanda_curs()
        except FileNotFoundError:
            raspuns_bot = "Fișierul `data/cursuri.json` nu a fost găsit."

    elif comanda == "/test":
        try:
            quiz = comanda_test()

            if not quiz:
                raspuns_bot = "Fișierul `data/quiz.json` nu conține întrebări."
            else:
                st.session_state["quiz"] = quiz
                st.session_state["index_intrebare"] = 0
                st.session_state["scor"] = 0
                st.session_state["scor_final"] = ""
                st.session_state["feedback_test"] = ""
                st.session_state["rezultat_salvat"] = False
                st.session_state["test_activ"] = True

                raspuns_bot = (
                    "Testul a început. "
                    "Selectează una dintre variantele de mai jos."
                )

        except FileNotFoundError:
            raspuns_bot = "Fișierul `data/quiz.json` nu a fost găsit."

        except ValueError as eroare:
            raspuns_bot = f"Eroare: {eroare}"

    else:
        raspuns_bot = (
            "Comandă necunoscută. "
            "Scrie `/curs` sau `/test`."
        )

    return raspuns_bot