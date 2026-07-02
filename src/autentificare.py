import streamlit as st


def proceseaza_login(input_utilizator: str) -> str:
    email = input_utilizator.strip().lower()

    if "@" not in email or "." not in email:
        return "Introdu o adresă de e-mail validă."

    st.session_state["email"] = email
    st.session_state["nume_utilizator"] = email.split("@")[0]

    return (
        f"Salut, {st.session_state['nume_utilizator']}! "
        "Scrie `/curs` pentru cursuri sau `/test` pentru test."
    )