import streamlit as st
import pandas as pd


# Configuration de la page
st.set_page_config(
    page_title="Projet Immo Le Wagon",
    page_icon="🏛",
    layout="wide"
 )
with st.sidebar:
    st.success("Select a page above")
    st.image("Logo_le_wagon.png", caption="Le wagon")
    st.markdown('*Batch* ***#2043*** *Projet rentabilité immobilère*')

# Votre dictionnaire de glossaire
glossaire = {
    "**Rentabilité Brute**": "Rendement du bien calculé uniquement sur les loyers perçus par rapport au prix d'achat.",
    "**Rentabilité Nette**": "Rendement réel après déduction des charges, impôts et frais.",
    "**GLI** (Garantie Loyers Impayés)": "Assurance couvrant le risque de loyers non payés.",
    "**PNO** (Propriétaire Non Occupant)": "Assurance protégeant un logement loué ou vacant.",
    "**Valeur cadastrale**": "Valeur estimée par l'administration pour calculer les impôts locaux.",
    "**Taux global TFPB** (Taxe Foncière sur les Propriétés Bâties)": "Pourcentage appliqué sur la valeur cadastrale pour calculer la taxe foncière.",
    "**Provisions** (entretien / gros œuvres)": "Sommes mises de côté pour financer réparations et travaux importants.",
    "**Assurance habitation**": "Couverture des risques liés au logement (incendie, dégâts des eaux, etc.).",
    "**Taux d'occupation**": "Proportion de temps où le bien est loué par rapport au temps total.",
    "**Frais de gestion locative**": "Coût facturé par une agence ou un gestionnaire pour s'occuper du bien.",
    "**IDE**": "Environnement de développement."
}

st.title("📒 Glossaire des termes techniques")
st.write("Cliquez sur un terme pour voir sa définition.")

# Boucle pour afficher chaque terme et sa définition
for terme, definition in glossaire.items():
    with st.expander(terme):
        st.write(definition)