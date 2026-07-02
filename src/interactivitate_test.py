from datetime import datetime

import streamlit as st

from .evaluare_raspunsuri import evalueaza_raspuns
from .persistenta_rezultate import salveaza_rezultat


LITERE_OPTIUNI = ["A", "B", "C"]


def selecteaza_raspuns(index_optiune: int) -> None:
    quiz = st.session_state["quiz"]
    index_intrebare = st.session_state["index_intrebare"]
    intrebare = quiz[index_intrebare]
    index_corect = intrebare["corect"]

    if evalueaza_raspuns(index_optiune, index_corect):
        st.session_state["scor"] += 1
        st.session_state["feedback_test"] = "Răspuns corect!"
    else:
        litera_corecta = LITERE_OPTIUNI[index_corect]
        st.session_state["feedback_test"] = f"Răspuns greșit. Varianta corectă era {litera_corecta}."

    st.session_state["index_intrebare"] += 1

    if st.session_state["index_intrebare"] >= len(quiz):
        scor_final = f"{st.session_state['scor']}/{len(quiz)}"

        if not st.session_state["rezultat_salvat"]:
            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            salveaza_rezultat(st.session_state["nume_utilizator"], st.session_state["email"], scor_final, data)
            st.session_state["rezultat_salvat"] = True

        st.session_state["scor_final"] = scor_final
        st.session_state["test_activ"] = False

        st.session_state["mesaje"].append({
            "role": "assistant",
            "content": (
                f"**Ai terminat testul!**\n\n"
                f"**Scor final:** {scor_final}\n\n"
                "Rezultatul a fost salvat."
            )
})

def afiseaza_test_interactiv() -> None:

    if not st.session_state["test_activ"]:
        return

    quiz = st.session_state["quiz"]
    index_intrebare = st.session_state["index_intrebare"]
    intrebare = quiz[index_intrebare]

    feedback = st.session_state["feedback_test"] or "Selectează răspunsul corect."
    st.info(feedback)

    st.subheader(f"Întrebarea {index_intrebare + 1}/{len(quiz)}")
    st.write(intrebare["intrebare"])

    for index, optiune in enumerate(intrebare["optiuni"]):
        st.button(
            f"{LITERE_OPTIUNI[index]}. {optiune}",
            key=f"optiune_{index}",
            on_click=selecteaza_raspuns,
            args=(index,),
            use_container_width=True
        )