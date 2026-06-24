import json

from src import ruleaza_quiz, salveaza_rezultat
from datetime import datetime



'''with open("data/cursuri.json", "r", encoding="utf-8") as file:
    cursuri = json.load(file)'''



with open("data/quiz.json", "r", encoding="utf-8") as file:
    quiz = json.load(file)

while True:
    nume_utilizator = input("Introdu numele tău: ").strip()

    if nume_utilizator:
        break

    print("Numele nu poate fi gol. Te rog să introduci un nume valid.")

scor = ruleaza_quiz(quiz)
salveaza_rezultat(nume_utilizator, scor, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

print(f"\nRezultatul tău a fost salvat cu succes, {nume_utilizator}.")





'''print("CURSURI:")
print(json.dumps(cursuri, ensure_ascii=False, indent=4))

print("\nQUIZ:")
print(json.dumps(quiz, ensure_ascii=False, indent=4))'''