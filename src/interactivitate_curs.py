from pathlib import Path

import streamlit as st

PROJECT_DIRECTORY = Path(__file__).resolve().parent.parent
CERTIFICAT = PROJECT_DIRECTORY / "assets" / "certificat_guardot.png"


def urmatorul_curs() -> None:
    st.session_state["index_curs"] += 1

    if st.session_state["index_curs"] >= len(st.session_state["cursuri"]):
        st.session_state["curs_activ"] = False
        st.session_state["curs_finalizat"] = True


def afiseaza_curs() -> None:

    if st.session_state["curs_finalizat"]:

        st.success("Felicitări! Ai parcurs toate cursurile.")

        st.image(
            str(CERTIFICAT),
            use_container_width=True
        )

        with open(CERTIFICAT, "rb") as fisier:
            st.download_button(
                "Descarcă certificatul",
                data=fisier,
                file_name="certificat_guardot.png",
                mime="image/png",
                use_container_width=True
            )

        return

    if not st.session_state["curs_activ"]:
        return

    curs = st.session_state["cursuri"][st.session_state["index_curs"]]

    st.subheader(curs["titlu"])

    continut = curs["continut"]

    if isinstance(continut, list):
        for paragraf in continut:
            st.markdown(paragraf)
    else:
        st.markdown(continut)

    st.button(
        "Next",
        on_click=urmatorul_curs,
        use_container_width=True
    )