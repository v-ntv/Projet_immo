import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import duckdb
import plotly.express as px
import json
import requests
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Projet Immo Le Wagon",
    page_icon="🏛",
    layout="wide"
 )
# --- SideBar ---
with st.sidebar:
    st.success("Selectionner les pages au dessus")
    st.image("Streamlit/Logo_Red&Black.png")
    st.markdown('*Batch* ***#2043*** *Projet rentabilité immobilière*')
    st.subheader('Auteurs')
    st.write('<a href="https://www.linkedin.com/in/amaury-guilbaud-a20950183/" target="_blank">Amaury Guilbaud</a>',unsafe_allow_html=True)
    st.write('<a href="https://www.linkedin.com/in/vincent-verhulst-vntv/" target="_blank">Vincent Verhulst</a>',unsafe_allow_html=True)
    st.write('<a href="https://www.linkedin.com/in/antoine-jard1/" target="_blank">Antoine Jardin</a>',unsafe_allow_html=True)

# --- Chargement des données ---
@st.cache_data
def load_data():
    # Charger les fichiers GeoJSON 
    geojson_filtre = "Streamlit/pays_de_la_loire.geojson"
    # Charger les données de meilleur agent
    data_MA = "Streamlit/df_MA_clean3.csv"
    # Charger les données avec pandas
    communes_data = pd.read_csv(data_MA)
    
    return geojson_filtre, communes_data

geojson_filtre, communes_data = load_data()

#Titre de la page
st.title("🏙️ Simulation par ville")

# Le fichier GeoJSON doit avoir une propriété 'codegeo' qui correspond à la colonne 'code_commune' du CSV.
communes_data['Code_insee'] = communes_data['Code_insee'].astype(str)


#Selection de la ville
ville=st.multiselect(
        "Selectionner la Ville",
        options=communes_data['ville'].unique(),
        default="Nantes",
        max_selections=1
    )

# Créez le DataFrame filtré
df_filtre = communes_data[communes_data['ville'].isin(ville)]
df_filtre = df_filtre.set_index(['ville'])

with st.expander('Data Preview'):
    st.dataframe(df_filtre)

#Création des graphique Plotly
fig_glb = px.bar(
    df_filtre,
    x=df_filtre.index,
    y=['min_global','prix_global','max_global'],
    title = f"Prix m2 à {df_filtre.index[0]}",
    barmode="group",
    text_auto=True
)
fig_glb_loc = px.bar(
    df_filtre,
    x=df_filtre.index,
    y=['loyer_min_global','loyer_global','loyer_max_global'],
    title = f"Prix loc m2 à {df_filtre.index[0]}",
    barmode="group",
    color_discrete_sequence=["#fd0", "#f0f", "#04f"],
    text_auto=True
)
fig_apt = px.bar(
    df_filtre,
    x=df_filtre.index,
    y=['min_appartement','prix_appartement','max_appartement'],
    title = f"Prix m2 à {df_filtre.index[0]}",
    barmode="group",
    text_auto=True
)
fig_apt_loc = px.bar(
    df_filtre,
    x=df_filtre.index,
    y=['loyer_min_appartement','loyer_appartement','loyer_max_appartement'],
    title = f"Prix loc m2 à {df_filtre.index[0]}",
    barmode="group",
    color_discrete_sequence=["#fd0", "#f0f", "#04f"],
    text_auto=True
)
fig_msn = px.bar(
    df_filtre,
    x=df_filtre.index,
    y=['min_maison','prix_maison','max_maison'],
    title = f"Prix m2 à {df_filtre.index[0]}",
    barmode="group",
    text_auto=True
)
fig_msn_loc = px.bar(
    df_filtre,
    x=df_filtre.index,
    y=['loyer_min_maison','loyer_maison','loyer_max_maison'],
    title = f"Prix loc m2 à {df_filtre.index[0]}",
    barmode="group",
    color_discrete_sequence=["#fd0", "#f0f", "#04f"],
    text_auto=True
)

# Modifier le titre de l'axe Y
fig_glb.update_layout(yaxis_title="Prix en €")
fig_glb_loc.update_layout(yaxis_title="Prix en €")
fig_apt.update_layout(yaxis_title="Prix en €")
fig_apt_loc.update_layout(yaxis_title="Prix en €")
fig_msn.update_layout(yaxis_title="Prix en €")
fig_msn_loc.update_layout(yaxis_title="Prix en €")


tab1, tab2, tab3 = st.tabs(["Global", "Appartements", "Maisons"])

with tab1:
    a, b, x = st.columns(3)
    c, d = st.columns(2)
    a.subheader(f"Rentabilité Brute au m2 à {df_filtre.index[0]}")
    a.metric("Rentabilité Brut moyenne", f"{df_filtre['ratio_m2_glb'][0]} %", border=True)
    b.subheader(f"Evolution de la population à {df_filtre.index[0]} entre 2016 et 2022")
    b.metric("Croissance pop", f"{df_filtre['CROI_POP_16_22'][0]} %", border=True)
    # affichage des graphiques
    c.plotly_chart(fig_glb)
    d.plotly_chart(fig_glb_loc)

    

with tab2:
    a, b, x = st.columns(3)
    c, d = st.columns(2)
    a.subheader(f"Rentabilité Brute pour les appartements au m2 à {df_filtre.index[0]}")
    a.metric("Rentabilité Brut moyenne", f"{df_filtre['ratio_m2_apt'][0]} %", border=True)
    b.subheader(f"Evolution de la population à {df_filtre.index[0]} entre 2016 et 2022")
    b.metric("Croissance pop", f"{df_filtre['CROI_POP_16_22'][0]} %", border=True)
    # affichage des graphiques
    c.plotly_chart(fig_apt)
    d.plotly_chart(fig_apt_loc)
    


with tab3:
    a, b, x = st.columns(3)
    c, d = st.columns(2)
    a.subheader(f"Rentabilité Brute pour les maisons au m2 à {df_filtre.index[0]}")
    a.metric("Rentabilité Brute moyenne", f"{df_filtre['ratio_m2_msn'][0]} %", border=True)
    b.subheader(f"Evolution de la population à {df_filtre.index[0]} entre 2016 et 2022")
    b.metric("Croissance pop", f"{df_filtre['CROI_POP_16_22'][0]} %", border=True)
    # affichage des graphiques
    c.plotly_chart(fig_msn)
    d.plotly_chart(fig_msn_loc)
    

option_map = {
    0: "Appartement",
    1: "Maison",
}

st.subheader(f"Simulation")

selection = st.segmented_control(
    "Type de bien",
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
    default=0
)
bien_choisi = option_map.get(selection)

if "Appartement" in bien_choisi:
    prix, loyer = "prix_appartement", "loyer_appartement"
elif "Maison" in bien_choisi:
    prix, loyer = "prix_maison", "loyer_maison"

e, f, g = st.columns(3)
nbm2 = e.number_input(
    "Surface du projet",
    value=42,
    max_value=1000,
    placeholder="en m2"
    )
frag =e.slider(
    "Selectionner les frais d'agences (en %)",
    0.0,
    10.0,
    5.0,
    step=0.5
    )
# Mappage des options de sélection aux valeurs de taux
taux_par_type = {
    "Ancien": 0.08,
    "Neuf": 0.05
}
annf = e.pills(
    "Sélectionner le type du bien :",
    ["Ancien", "Neuf"],
    default="Ancien"
)
taux_choisi = taux_par_type.get(annf)
pno = f.number_input(
    "Assurance PNO (propriétaire non occupant en €)",
    value=250,
    placeholder="en €"
    )
gli = f.number_input(
    "Assurance GLI (garantie loyers impayés en €)",
    value=300,
    placeholder="en €"
    )
coan = f.number_input(
    "Comptabilité annuelle (en €)",
    value=600,
    placeholder="en €"
    )
aha = g.number_input(
    "Assurance habitation annuelle",
    value=300,
    placeholder="en €"
    )
frgl = g.number_input(
    "Frais de gestion locative (en €)",
    value=200,
    placeholder="en €"
    )
txo = g.slider(
    "Taux d'occupation (en %)",
    0,
    100,
    95,
    step=1
    )

#Création du DataFrame Simulation
def df_simulation(prix, loyer):

    df_simu = pd.DataFrame()
    df_simu['Prix au m2 en €']= df_filtre[prix]
    df_simu['Surface en m2']= nbm2
    df_simu['Prix net vendeur en €'] = df_simu['Prix au m2 en €']*df_simu['Surface en m2']
    df_simu["Frais d'agence"] = frag/100 # slider
    df_simu["Frais de notaire"] = taux_choisi # 3% sur neuf 8% sur ancien
    df_simu["Frais d'agence en €"] = df_simu["Prix net vendeur en €"]*df_simu["Frais d'agence"]
    df_simu["Frais de notaire en €"] = df_simu["Prix net vendeur en €"]*df_simu["Frais de notaire"]
    df_simu["Loyer m2 en €"] = df_filtre[loyer]
    df_simu["Taux d'occupation"] = txo/100 # slider
    df_simu["Loyer mensuel en €"] = df_simu['Surface en m2']*df_simu["Loyer m2 en €"]*df_simu["Taux d'occupation"]
    df_simu["Loyer annuel en €"] = df_simu["Loyer mensuel en €"]*12
    df_simu["Assurance annuelle PNO en €"] = pno # à remplir
    df_simu["GLI annuelle (Garantie Loyers Impayés) en €"] = gli #0.03*df_simu["Loyer annuel"] # à mettre par défaut
    df_simu["Comptabilité annuelle en €"] = coan # à remplir
    df_simu["Valeur cadastrale en €"] = df_simu['Surface en m2']*df_simu["Loyer m2 en €"]*12*0.5
    df_simu["Taux global TFPB"] = df_filtre['Taux_Global_TFB']
    df_simu["Taxe foncière annuelle en €"] = round((df_simu["Valeur cadastrale en €"])*df_simu["Taux global TFPB"],2)
    df_simu["Provisions entretien annuel en €"] = df_simu['Loyer annuel en €']*0.02
    df_simu["Provisions gros oeuvres annuel en €"] = df_simu['Prix net vendeur en €']*0.005
    df_simu["Assurance habitation annuelle en €"] = aha #à remplir
    df_simu["Frais de gestion locative annuel en €"] = df_simu['Loyer mensuel en €']*0.07*12
    df_simu["Prix achat total en €"] = df_simu["Prix net vendeur en €"]+df_simu["Frais d'agence en €"]+df_simu["Frais de notaire en €"]
    df_simu['Rentabilité Brute en %'] = round(df_simu['Loyer annuel en €']/df_simu["Prix achat total en €"]*100,2)
    df_simu['Charges Annuelles en €'] = round(df_simu["Assurance annuelle PNO en €"]+df_simu["GLI annuelle (Garantie Loyers Impayés) en €"]+df_simu["Comptabilité annuelle en €"]+df_simu["Taux global TFPB"]+df_simu["Provisions entretien annuel en €"]+df_simu["Provisions gros oeuvres annuel en €"]+df_simu["Assurance habitation annuelle en €"]+df_simu["Frais de gestion locative annuel en €"],2)
    df_simu['Rentabilité Nette en %'] = round((df_simu['Loyer annuel en €']-df_simu['Charges Annuelles en €'])/df_simu["Prix achat total en €"]*100,2)
    return df_simu

df_simu= df_simulation(prix, loyer)

with st.expander('Data Simulation'):
    st.dataframe(df_simu[['Prix net vendeur en €',"Frais d'agence en €","Frais de notaire en €","Loyer annuel en €","Valeur cadastrale en €","Provisions entretien annuel en €","Provisions gros oeuvres annuel en €","Frais de gestion locative annuel en €"]])

h, i, j = st.columns(3)
h.metric("Prix d'achat total", f"{round(df_simu['Prix achat total en €'][0])} €", border=True) 
i.metric("Rentabilité Brute", f"{df_simu['Rentabilité Brute en %'][0]} %", border=True) 
j.metric("Rentabilité Nette", f"{df_simu['Rentabilité Nette en %'][0]} %",border=True)
