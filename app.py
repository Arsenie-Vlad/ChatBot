import streamlit as st

from src.comenzi import comanda_curs, comanda_test
from src.interactivitate_test import afiseaza_test_interactiv


st.set_page_config(page_title="GuardOT", page_icon="assets/scut.png")

st.sidebar.title("Meniu GuardOT")
st.sidebar.info("ajshdb")
st.sidebar.markdown("**Comenzi disponibile**\n\n- `/curs` — afișează cursurile\n- `/test` — începe testul")

st.session_state.setdefault("nume_utilizator", None)
st.session_state.setdefault("mesaje", [{
    "role": "assistant",
    "content": "Salut! Sunt GuardOT, un asistent virtual care te va ghida prin cursurile și testul de securitate. Te rog să introduci numele tău pentru a începe."
}])
st.session_state.setdefault("test_activ", False)
st.session_state.setdefault("test_finalizat", False)
st.session_state.setdefault("quiz", [])
st.session_state.setdefault("index_intrebare", 0)
st.session_state.setdefault("scor", 0)
st.session_state.setdefault("scor_final", "")
st.session_state.setdefault("feedback_test", "")
st.session_state.setdefault("rezultat_salvat", False)


def proceseaza_mesaj() -> None:
    if st.session_state["test_activ"]:
        return

    input_utilizator = (st.session_state.get("camp_chat") or "").strip()

    if not input_utilizator:
        return

    st.session_state["mesaje"].append({
        "role": "user",
        "content": input_utilizator
    })

    if st.session_state["nume_utilizator"] is None:
        st.session_state["nume_utilizator"] = input_utilizator
        raspuns_bot = f"Salut, {input_utilizator}! Scrie `/curs` pentru cursuri sau `/test` pentru a începe testul."
    else:
        comanda = input_utilizator.lower().split()[0]

        if comanda == "/curs":
            st.session_state["test_finalizat"] = False

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
                    st.session_state["test_finalizat"] = False
                    st.session_state["test_activ"] = True
                    raspuns_bot = "Testul a început. Selectează una dintre variantele de mai jos."

            except FileNotFoundError:
                raspuns_bot = "Fișierul `data/quiz.json` nu a fost găsit."
            except ValueError as eroare:
                raspuns_bot = f"Eroare: {eroare}"

        else:
            raspuns_bot = "Comandă necunoscută. Scrie `/curs` sau `/test`."

    st.session_state["mesaje"].append({
        "role": "assistant",
        "content": raspuns_bot
    })


if st.sidebar.button("Resetează conversația"):
    st.session_state.clear()
    st.rerun()

st.image("assets/scut.png", width=100)
st.title("GuardOT")
st.write("Acesta este prototipul interfeței pentru GuardOT.")

for mesaj in st.session_state["mesaje"]:
    with st.chat_message(mesaj["role"]):
        st.markdown(mesaj["content"])

if st.session_state["nume_utilizator"] is None:
    text_ajutator = "Introdu numele tău aici..."
elif st.session_state["test_activ"]:
    text_ajutator = "Test în desfășurare..."
else:
    text_ajutator = "Scrie comanda /curs sau /test"

st.chat_input(
    text_ajutator,
    key="camp_chat",
    on_submit=proceseaza_mesaj,
    disabled=st.session_state["test_activ"]
)

afiseaza_test_interactiv()