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
st.title("📌 Zoom Pays de la Loire")
st.subheader("Carte des Pays de la Loire ")

#Ajout de feuillet pour les différents indicateurs
tab1, tab2 = st.tabs(["Tension Locative", "Ratio Achat/Loc"])

with tab1:
    st.subheader('Tension Locative')
    # --- Préparation des données pour la carte ----
    # Le fichier GeoJSON doit avoir une propriété 'codegeo' qui correspond à la colonne 'code_commune' du CSV.
    communes_data['Code_insee'] = communes_data['Code_insee'].astype(str)


    # --- Création de la carte Folium ----
    # Coordonnées initiales centrées sur Pays de la Loire
    m = folium.Map(location=[47.2, -0.6], zoom_start=8)

    # Création de la carte choroplèthe
    folium.Choropleth(
        geo_data=geojson_filtre, # Le fichier GeoJSON
        name="choropleth",
        data=communes_data,
        columns=["Code_insee", 'INDICE_TENSION_LOG'], # Colonnes pour lier les données
        key_on="properties.codgeo", # Clé de liaison dans le GeoJSON
        fill_color="RdYlGn_r", # Palette de couleurs (ex: YellowOrangeRed)
        nan_fill_color="grey",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Indice de la tension locative', # Nom de la légende dynamique
        highlight=True,
        smooth_factor=0.5,
        zoom_on_click=True
    ).add_to(m)

    # Ajout d'une couche de contrôle pour activer/désactiver la carte choroplèthe
    folium.LayerControl().add_to(m)

    # Affichage de la carte dans Streamlit
    st_folium(m, width=1200, height=800)


with tab2:
    st.subheader('Ratio Achat/Loc')
    type_de_bien = st.pills(
        "Sélectionnez le type de bien :",
        ["Appartements", "Maisons"],
        selection_mode="multi"
    )

    # --- Préparation des variables en fonction de la sélection ----
    # Vérifiez si les deux options sont sélectionnées
    if "Appartements" in type_de_bien and "Maisons" in type_de_bien:
        colonne_valeur = "ratio_m2_glb"
        nom_legende = "Ratio Achat/Loc global"
    # Sinon, vérifiez quelle option simple est sélectionnée
    elif "Appartements" in type_de_bien:
        colonne_valeur = "ratio_m2_apt"
        nom_legende = "Ratio Achat/Loc des appartements"
    elif "Maisons" in type_de_bien:
        colonne_valeur = "ratio_m2_msn"
        nom_legende = "Ratio Achat/Loc des maisons"
    else:
        # Cas où rien n'est sélectionné, utilisez les données par défaut ou affichez un message
        colonne_valeur = "ratio_m2_glb"
        nom_legende = "Sélectionnez un type de bien"


    # --- Préparation des données pour la carte ----
    # Le fichier GeoJSON doit avoir une propriété 'codegeo' qui correspond à la colonne 'code_commune' du CSV.
    communes_data['Code_insee'] = communes_data['Code_insee'].astype(str)

    # --- Création de la carte Folium ---
    # Coordonnées initiales centrées sur Pays de la Loire
    m = folium.Map(location=[47.2, -0.6], zoom_start=8)

    # Création de la carte choroplèthe
    folium.Choropleth(
        geo_data=geojson_filtre, # Le fichier GeoJSON
        name="choropleth",
        data=communes_data,
        columns=["Code_insee", colonne_valeur], # Colonnes pour lier les données
        key_on="properties.codgeo", # Clé de liaison dans le GeoJSON
        fill_color="RdYlGn_r", # Palette de couleurs 
        nan_fill_color="grey",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=nom_legende, # Nom de la légende dynamique
        smooth_factor=0.5,
        zoom_on_click=True
    ).add_to(m)

    # Ajout d'une couche de contrôle pour activer/désactiver la carte choroplèthe
    folium.LayerControl().add_to(m)

    # Affichage de la carte dans Streamlit
    st_folium(m, width=1200, height=800)


# Block : Looker
with st.container():
    st.header("KPI Départements")
    url = "https://lookerstudio.google.com/embed/reporting/664389ba-e673-461b-88b2-1eb27c02248e/page/p_fcin9i4nvd"
    # Insérer avec iframe
    st.components.v1.iframe(url, width=1200, height=1000, scrolling=True)
