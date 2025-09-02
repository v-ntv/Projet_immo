import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Projet Immo Le Wagon",
    page_icon="🏛",
    layout="wide"
 )

# --- SideBar ---
with st.sidebar:
    st.success("Select a page above")
    st.image("Logo_le_wagon.png", caption="Le wagon")
    st.markdown('*Batch* ***#2043*** *Projet rentabilité immobilère*')


st.title("Présentation projet")
st.subheader("Outils")
st.subheader('Sources')


