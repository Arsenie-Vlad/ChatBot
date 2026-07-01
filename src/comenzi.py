from pathlib import Path

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
