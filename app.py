import streamlit as st

from src.comenzi import proceseaza_comanda
from src.interactivitate_test import afiseaza_test_interactiv
from src.dashboard_admin import afiseaza_dashboard
from src.autentificare import proceseaza_login

from config import ADMIN_EMAIL


st.set_page_config(page_title="GuardOT", page_icon="assets/scut.png")

st.session_state.setdefault("nume_utilizator", None)
st.session_state.setdefault("email", None)
st.session_state.setdefault("mesaje", [{
    "role": "assistant",
    "content": "Salut! Sunt GuardOT, un asistent virtual care te va ghida prin cursurile și testul de securitate. Te rog să introduci adresa ta de e-mail pentru a începe."
}])
st.session_state.setdefault("test_activ", False)
st.session_state.setdefault("quiz", [])
st.session_state.setdefault("index_intrebare", 0)
st.session_state.setdefault("scor", 0)
st.session_state.setdefault("scor_final", "")
st.session_state.setdefault("feedback_test", "")
st.session_state.setdefault("rezultat_salvat", False)

with st.sidebar:
    st.image("assets/scut.png", width=80)

    st.title("GuardOT")
    st.caption("Asistent pentru instruire în securitate")

    st.divider()

    st.subheader("👤 Utilizator")

    if st.session_state["email"]:
        st.success(st.session_state["email"])
    else:
        st.info("Neautentificat")

    st.divider()

    st.subheader("Comenzi")
    st.markdown("""
- `/curs` — Afișează cursurile
- `/test` — Începe testul
""")

    if st.session_state["test_activ"]:
        st.divider()
        st.subheader("Progres")

        st.metric("Scor", st.session_state["scor"])

        st.progress(
            st.session_state["index_intrebare"] /
            len(st.session_state["quiz"])
        )
        st.divider()


    if st.session_state["email"] == ADMIN_EMAIL:
        st.divider()
        pagina = st.radio(
            "Navigare",
            ["Chat", "Analytics"]
        )
        st.divider()
    else:
        pagina = "Chat"


    if st.button("Resetează conversația", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.caption("GuardOT v1.3")

if pagina == "Analytics":
    afiseaza_dashboard()
    st.stop()

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

    if st.session_state["email"] is None:
        raspuns_bot = proceseaza_login(input_utilizator)
    else:
        raspuns_bot = proceseaza_comanda(input_utilizator)

    st.session_state["mesaje"].append({
        "role": "assistant",
        "content": raspuns_bot
    })
    
st.image("assets/scut.png", width=100)
st.title("GuardOT")
st.write("Acesta este prototipul interfeței pentru GuardOT.")

for mesaj in st.session_state["mesaje"]:
    with st.chat_message(mesaj["role"]):
        st.markdown(mesaj["content"])

if st.session_state["email"] is None:
    text_ajutator = "Introdu adresa ta de e-mail..."
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