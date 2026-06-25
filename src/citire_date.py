import json

def citeste_fisier(cale_fisier: str):
    with open(cale_fisier, "r", encoding="utf-8") as file:
        return json.load(file)
