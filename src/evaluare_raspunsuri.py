def evalueaza_raspuns(input_utilizator: int, index_corect: int) -> bool: 
    return input_utilizator == index_corect


def ruleaza_quiz(quiz: list[dict]) -> int:

    scor = 0

    for intrebare in quiz:
        print(f"\n{intrebare['intrebare']}")

        optiuni = intrebare["optiuni"]

        for index, optiune in enumerate(optiuni):
            print(f"{index}. {optiune}")

        while True:
            raspuns_text = input("Alege răspunsul 0, 1 sau 2: ").strip()

            if raspuns_text in {"0", "1", "2"}:
                input_utilizator = int(raspuns_text)
                break

            print("Răspuns invalid. Introdu 0, 1 sau 2.")

        index_corect = intrebare["corect"]

        if evalueaza_raspuns(input_utilizator, index_corect):
            print("Răspuns corect!")
            scor += 1
        else:
            print("Răspuns greșit!")
            print(f"Răspunsul corect era varianta {index_corect}.")

    print("\nTest terminat.")
    print(f"Scor final: {scor}/{len(quiz)}")

    return scor

