import streamlit as st
from src.comenzi import comanda_curs, comanda_test, formateaza_intrebare
from src.evaluare_raspunsuri import evalueaza_raspuns
from src import salveaza_rezultat
from datetime import datetime

st.set_page_config(page_title="GuardOT", page_icon="assets/scut.png")

st.sidebar.title("Meniu GuardOT")
st.sidebar.info("ajshdb")
st.sidebar.markdown("**Comenzi disponibile**\n\n- `/curs` — afișează cursurile\n- `/test` — începe testul")

if "nume_utilizator" not in st.session_state:
    st.session_state.nume_utilizator = None

if "mesaje" not in st.session_state:
    st.session_state.mesaje = [{
        "role": "assistant",
        "content": "Salut! Sunt GuardOT, un asistent virtual care te va ghida prin cursurile și testul de securitate. Te rog să introduci numele tău pentru a începe."
    }]

if "test_activ" not in st.session_state:
    st.session_state.test_activ = False

if "quiz" not in st.session_state:
    st.session_state.quiz = []

if "index_intrebare" not in st.session_state:
    st.session_state.index_intrebare = 0

if "scor" not in st.session_state:
    st.session_state.scor = 0

if "rezultat_salvat" not in st.session_state:
    st.session_state.rezultat_salvat = False

if st.sidebar.button("Resetează conversația"):
    st.session_state.clear()
    st.rerun()

st.image("assets/scut.png", width=100)
st.title("GuardOT")
st.write("Acesta este prototipul interfeței pentru GuardOT.")

for mesaj in st.session_state.mesaje:
    with st.chat_message(mesaj["role"]):
        st.markdown(mesaj["content"])

if st.session_state.nume_utilizator is None:
    text_ajutator = "Introdu numele tău aici..."
elif st.session_state.test_activ:
    text_ajutator = "Introdu numărul răspunsului..."
else:
    text_ajutator = "Scrie comanda /curs sau /test"

input_utilizator = st.chat_input(text_ajutator, key="camp_chat")

if input_utilizator:
    input_utilizator = input_utilizator.strip()

    if not input_utilizator:
        st.stop()

    st.session_state.mesaje.append({"role": "user", "content": input_utilizator})

    with st.chat_message("user"):
        st.markdown(input_utilizator)

    if st.session_state.nume_utilizator is None:
        st.session_state.nume_utilizator = input_utilizator
        raspuns_bot = f"Salut, {input_utilizator}! Scrie `/curs` pentru cursuri sau `/test` pentru a începe testul."

    elif st.session_state.test_activ:
        quiz = st.session_state.quiz
        index_intrebare = st.session_state.index_intrebare
        intrebare_curenta = quiz[index_intrebare]
        optiuni = intrebare_curenta["optiuni"]

        if not input_utilizator.isdigit():
            raspuns_bot = "Răspuns invalid. Introdu doar numărul variantei."
        else:
            raspuns_utilizator = int(input_utilizator)

            if not 0 <= raspuns_utilizator < len(optiuni):
                raspuns_bot = f"Introdu un număr între 0 și {len(optiuni) - 1}."
            else:
                raspuns_corect = intrebare_curenta["corect"]

                if evalueaza_raspuns(raspuns_utilizator, raspuns_corect):
                    st.session_state.scor += 1
                    mesaj_rezultat = "Răspuns corect!"
                else:
                    mesaj_rezultat = f"Răspuns greșit. Varianta corectă era {raspuns_corect}."

                st.session_state.index_intrebare += 1

                if st.session_state.index_intrebare < len(quiz):
                    urmatoarea_intrebare = quiz[st.session_state.index_intrebare]
                    raspuns_bot = f"{mesaj_rezultat}\n\n{formateaza_intrebare(urmatoarea_intrebare, st.session_state.index_intrebare + 1, len(quiz))}"
                else:
                    st.session_state.test_activ = False
                    scor_formatat = f"{st.session_state.scor}/{len(quiz)}"

                    if not st.session_state.rezultat_salvat:
                        salveaza_rezultat(st.session_state.nume_utilizator, scor_formatat, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        st.session_state.rezultat_salvat = True

                    raspuns_bot = f"{mesaj_rezultat}\n\n### Test terminat\n\nScor final: {scor_formatat}\n\nRezultatul a fost salvat."

    else:
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
                    raspuns_bot = "Fișierul `quiz.json` nu conține întrebări."
                else:
                    st.session_state.quiz = quiz
                    st.session_state.index_intrebare = 0
                    st.session_state.scor = 0
                    st.session_state.test_activ = True
                    st.session_state.rezultat_salvat = False
                    raspuns_bot = f"Testul a început!\n\n{formateaza_intrebare(quiz[0], 1, len(quiz))}"

            except FileNotFoundError:
                raspuns_bot = "Fișierul `data/quiz.json` nu a fost găsit."
            except ValueError as eroare:
                raspuns_bot = f"Eroare: {eroare}"

        else:
            raspuns_bot = "Comandă necunoscută. Scrie `/curs` sau `/test`."

    st.session_state.mesaje.append({"role": "assistant", "content": raspuns_bot})

    with st.chat_message("assistant"):
        st.markdown(raspuns_bot)
