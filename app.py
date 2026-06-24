import json

with open("cursuri.json", "r", encoding="utf-8") as file:
    cursuri = json.load(file)

with open("quiz.json", "r", encoding="utf-8") as file:
    quiz = json.load(file)

print("CURSURI:")
print(json.dumps(cursuri, ensure_ascii=False, indent=4))

print("\nQUIZ:")
print(json.dumps(quiz, ensure_ascii=False, indent=4))
