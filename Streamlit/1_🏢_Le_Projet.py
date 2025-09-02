import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Projet Immo Le Wagon",
    page_icon="🏛",
    layout="wide"
 )

# --- SideBar ---
with st.sidebar:
    st.success("Selectionner les pages au dessus")
    st.image("Logo_Red&Black.png")
    st.markdown('*Batch* ***#2043*** *Projet rentabilité immobilère*')
    st.subheader('Auteurs')
    st.write('<a href="https://www.linkedin.com/in/amaury-guilbaud-a20950183/" target="_blank">Amaury Guilbaud</a>',unsafe_allow_html=True)
    st.write('<a href="https://www.linkedin.com/in/vincent-verhulst-vntv/" target="_blank">Vincent Verhulst</a>',unsafe_allow_html=True)
    st.write('<a href="https://www.linkedin.com/in/antoine-jard1/" target="_blank">Antoine Jardin</a>',unsafe_allow_html=True)

st.title("Projet sur la rentabilité immobilière")

st.subheader("Le Projet")

st.write("""
    Ce projet a été réalisés dans le cadre de notre formation *Data Analytics* via <a href="https://www.lewagon.com/fr/data-analytics-course" target="_blank">Le Wagon</a>.<br>
    L'objectif est de créer un outil pour faciliter l'investissement immobilier.
    """,
    unsafe_allow_html=True
)

st.subheader("L'outil")

st.write("""
    Cet outil permet de calculer le ratio entre prix d'achat et la mise en location pour identifier la rentabiliter d'un projet.<br>
    Actuellement, cet outil se focalise sur la région des Pays de la Loire.<br>
    Vous pouvez avoir un détail par ville et même comparer plusieurs villes entre elles.
""",
unsafe_allow_html=True
)
