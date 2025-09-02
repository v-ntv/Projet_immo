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
with st.sidebar:
    st.success("Select a page above")
    st.image("Logo_le_wagon.png", caption="Le wagon")
    st.markdown('Vincent - Amaury - Antoine')

# --- Chargement des données ---
def load_data():
    # Charger les fichiers GeoJSON 
    geojson = requests.get("https://www.data.gouv.fr/api/1/datasets/r/138844a4-2994-462c-a6da-d636c13692b6").json()
    # Charger les données de meilleur agent
    data_MA = "df_MA_clean3.csv"
    # Charger les données avec pandas
    communes_data = pd.read_csv(data_MA)
    

    return geojson, communes_data

geojson, communes_data = load_data()

#Titre de la page
st.title("🏙️ Simulation par ville")

# Filtrer aux pays de la loire
features_filtrees = [
    feature for feature in geojson["features"]
    if feature["properties"].get("reg") == "52"
]
# Créer un nouveau GeoJSON
geojson_filtre = {
    "type": "FeatureCollection",
    "features": features_filtrees
}


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
    title = f"Prix m2 à {df_filtre.index[0]}",
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
    title = f"Prix m2 à {df_filtre.index[0]}",
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
    title = f"Prix m2 à {df_filtre.index[0]}",
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
    a.metric("Rentabilité Brut moyenne", f"{df_filtre['ratio_m2_msn'][0]} %", border=True)
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
    "Selectionné les frais d'agences (en %)",
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
    "Sélectionnez le type du bien :",
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
    df_simu['Prix au m2']= df_filtre[prix]
    df_simu['Surface en m2']= nbm2
    df_simu['Prix net vendeur'] = df_simu['Prix au m2']*df_simu['Surface en m2']
    df_simu["Frais d'agence en %"] = frag/100 # slider
    df_simu["Frais de notaire en %"] = taux_choisi # 3% sur neuf 8% sur ancien
    df_simu["Frais d'agence en €"] = df_simu["Prix net vendeur"]*df_simu["Frais d'agence en %"]
    df_simu["Frais de notaire en €"] = df_simu["Prix net vendeur"]*df_simu["Frais de notaire en %"]
    df_simu["Loyer m2"] = df_filtre[loyer]
    df_simu["Taux d'occupation"] = txo # slider
    df_simu["Loyer mensuel"] = df_simu['Surface en m2']*df_simu["Loyer m2"]*df_simu["Taux d'occupation"]
    df_simu["Loyer annuel"] = df_simu["Loyer mensuel"]*12
    df_simu["Assurance annuelle PNO"] = pno # à remplir
    df_simu["GLI annuelle (Garantie Loyers Impayés)"] = gli #0.03*df_simu["Loyer annuel"] # à mettre par défaut
    df_simu["Comptabilité annuelle"] = coan # à remplir
    df_simu["Valeur cadastrale"] = df_simu['Surface en m2']*df_simu["Loyer m2"]
    df_simu["Taux global TFPB"] = df_filtre['Taux_Global_TFB']
    df_simu["Taxe foncière annuelle"] = (df_simu["Valeur cadastrale"]*0.5)*df_simu["Taux global TFPB"]
    df_simu["provisions entretien annuel"] = df_simu['Loyer annuel']*0.02
    df_simu["provisions gros oeuvres annuel"] = df_simu['Prix net vendeur']*0.005
    df_simu["Assurance habitation annuelle"] = aha #à remplir
    df_simu["Frais de gestion locative annuel"] = df_simu['Loyer mensuel']*0.07*12
    df_simu["Prix achat total"] = df_simu["Prix net vendeur"]+df_simu["Frais d'agence en €"]+df_simu["Frais de notaire en €"]
    df_simu['Rentabilité Brute'] = round(df_simu['Loyer annuel']/df_simu["Prix achat total"],2)
    df_simu['Charges Annuelles'] = round(df_simu["Assurance annuelle PNO"]+df_simu["GLI annuelle (Garantie Loyers Impayés)"]+df_simu["Comptabilité annuelle"]+df_simu["Taux global TFPB"]+df_simu["provisions entretien annuel"]+df_simu["provisions gros oeuvres annuel"]+df_simu["Assurance habitation annuelle"]+df_simu["Frais de gestion locative annuel"],2)
    df_simu['Rentabilité Net'] = round((df_simu['Loyer annuel']-df_simu['Charges Annuelles'])/df_simu["Prix achat total"],2)
    return df_simu

df_simu= df_simulation(prix, loyer)

with st.expander('Data Simulation'):
    st.dataframe(df_simu)

with st.expander('Data Indicateurs'):
    st.dataframe(df_simu[['Prix achat total','Rentabilité Brute','Charges Annuelles','Rentabilité Net']])

h, i, j = st.columns(3)
h.metric("Prix d'achat total", f"{int(df_simu['Prix achat total'])} €", border=True) 
i.metric("Ratio achat/loc Brut", f"{df_simu['Rentabilité Brute'][0]} %", border=True) 
j.metric("Ratio achat/loc Net", f"{df_simu['Rentabilité Net'][0]} %",border=True)