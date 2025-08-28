import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import duckdb
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="Projet Immo Le Wagon",
    page_icon="🏛",
    layout="wide"
 )


# --- Chargement des données ---
#@st.cache_data
def load_data():
    # Charger le fichier GeoJSON des communes
    geojson_path = "communes.geojson" 
    # Charger les données de meilleur agent
    data_MA = "df_MA_clean.csv"
    # Charger les données avec pandas
    communes_df = pd.read_csv(data_MA)

    return geojson_path, communes_df

geojson_path, communes_data = load_data()

#Ajout des données global + ratio
communes_data['prix_global'] = (communes_data['prix_appartement']+communes_data['prix_maison'])/2
communes_data['min_global'] = (communes_data['min_appartement']+communes_data['min_maison'])/2
communes_data['max_global'] = (communes_data['max_appartement']+communes_data['max_maison'])/2
communes_data['loyer_global'] = (communes_data['loyer_appartement']+communes_data['loyer_maison'])/2
communes_data['loyer_min_global'] = (communes_data['loyer_min_appartement']+communes_data['loyer_min_maison'])/2
communes_data['loyer_max_global'] = (communes_data['loyer_max_appartement']+communes_data['loyer_max_maison'])/2
communes_data['ratio_m2_apt'] = round(((communes_data['loyer_appartement']*12)/communes_data['prix_appartement'])*100,2)
communes_data['ratio_m2_msn'] = round(((communes_data['loyer_maison']*12)/communes_data['prix_maison'])*100,2)
communes_data['ratio_m2_glb'] = round(((communes_data['loyer_global']*12)/communes_data['prix_global'])*100,2)


# --- SideBar ---
with st.sidebar:
    st.image("Logo_le_wagon.png", caption="Le wagon")
    # st.header("Filtres")
    # type_de_bien = st.pills(
    #     "Sélectionnez le type de bien :",
    #     ["Appartements", "Maisons"],
    #     selection_mode="multi"
    # )
    # ville=st.multiselect(
    #     "Select Ville",
    #     options=communes_data['ville'].unique(),
    #     default=communes_data['ville'][91]
    # )
    nbm2=st.number_input(
        "Surface du projet",
        value=None,
        placeholder="en m2"
        )
    fraisdagence=st.slider(
        "Selectionné les frais d'agences (en %)",
        0.0,
        10.0,
        5.0,
        step=0.5
        )


st.divider()
st.header("Page 1")
st.divider()

#Titre de la page
st.title("Dashboard")

#Selection du type de bien à afficher sur la map
st.markdown("Filtres")
type_de_bien = st.pills(
    "Sélectionnez le type de bien :",
    ["Appartements", "Maisons"],
    selection_mode="multi"
)

# --- Préparation des variables en fonction de la sélection ----
# Vérifiez si les deux options sont sélectionnées
if "Appartements" in type_de_bien and "Maisons" in type_de_bien:
    colonne_valeur = "ratio_m2_glb"
    nom_legende = "Ratio moyen global des biens (€/m²)"
# Sinon, vérifiez quelle option simple est sélectionnée
elif "Appartements" in type_de_bien:
    colonne_valeur = "ratio_m2_apt"
    nom_legende = "Ratio moyen des appartements (€/m²)"
elif "Maisons" in type_de_bien:
    colonne_valeur = "ratio_m2_msn"
    nom_legende = "Ratio moyen des maisons (€/m²)"
else:
    # Cas où rien n'est sélectionné, utilisez les données par défaut ou affichez un message
    colonne_valeur = "ratio_m2_glb"
    nom_legende = "Sélectionnez un type de bien"


# --- Préparation des données pour la carte ----
# Le fichier GeoJSON doit avoir une propriété 'code' qui correspond à la colonne 'code_commune' du CSV.
communes_data['Code_insee'] = communes_data['Code_insee'].astype(str)

# --- Création de la carte Folium ---
# Coordonnées initiales centrées sur Nantes
nantes_coords = [47.216671, -1.55]
m = folium.Map(location=nantes_coords, zoom_start=8)

# Création de la carte choroplèthe
folium.Choropleth(
    geo_data=geojson_path, # Le fichier GeoJSON
    name="choropleth",
    data=communes_data,
    columns=["Code_insee", colonne_valeur], # Colonnes pour lier les données
    key_on="feature.properties.code", # Clé de liaison dans le GeoJSON
    fill_color="YlOrRd", # Palette de couleurs (ex: YellowOrangeRed)
    nan_fill_color="purple",
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

st.divider()
st.header("Page 2")
st.divider()

#Selection des villes
ville=st.multiselect(
        "Selectionner la Ville",
        options=communes_data['ville'].unique(),
        default=communes_data['ville'][91]
    )

# Créez le DataFrame filtré
df_filtre = communes_data[communes_data['ville'].isin(ville)]
df_filtre = df_filtre.set_index(['ville'])
df_filtre_apt = df_filtre[['prix_appartement','min_appartement','max_appartement','ratio_m2_apt']] 
df_filtre_apt_loc = df_filtre[['loyer_appartement', 'loyer_min_appartement', 'loyer_max_appartement']]
df_filtre_maison = df_filtre[['prix_maison',"min_maison",'max_maison','ratio_m2_msn']]
df_filtre_maison_loc = df_filtre[['loyer_maison', 'loyer_min_maison', 'loyer_max_maison']]
df_filtre_glb = df_filtre[['prix_global',"min_global",'max_global','ratio_m2_glb']]
df_filtre_glb_loc = df_filtre[['loyer_global', 'loyer_min_global', 'loyer_max_global']]
Code_postal = df_filtre['Code_postal']

with st.expander('Data Preview'):
    st.dataframe(df_filtre)



tab1, tab2, tab3 = st.tabs(["Appartements", "Maisons", "Global"])

with tab1:
    a, b = st.columns(2)
    c, d = st.columns(2)
    a.subheader("Rantabilité Brute moyenne au m2 pour les maisons")
    a.metric("Rentabilité Brut", df_filtre_maison['ratio_m2_msn'], border=True)
    b.subheader("Rantabilité Brute moyenne au m2 pour les appartements")
    b.metric("Rentabilité Brut", df_filtre_apt['ratio_m2_apt'], border=True)
    c.subheader(f'Prix immobilier à {df_filtre.index[0]}')
    c.bar_chart(df_filtre_apt, y_label="Prix m2 en €",stack=False)
    d.subheader(f'Loyer mensuel à {df_filtre.index[0]}')
    d.bar_chart(df_filtre_apt_loc, y_label="Loyer m2 en €", color=["#fd0", "#f0f", "#04f"], stack=False)
    

with tab2:
    st.subheader("Standart ratio au m2 pour les Maisons")
    a, b = st.columns(2)
    c, d = st.columns(2)
    a.metric("Rentabilité Brut Loc", df_filtre_maison['ratio_m2_msn'], border=True)
    c.bar_chart(df_filtre_maison, y_label="Prix m2 en €", stack=False)
    d.bar_chart(df_filtre_maison_loc, y_label="Loyer m2 en €", color=["#fd0", "#f0f", "#04f"], stack=False)

with tab3:
    st.subheader("Standart ratio au m2 pour la ville")
    a, b = st.columns(2)
    c, d = st.columns(2)
    a.metric("Rentabilité Brut", df_filtre_glb['ratio_m2_glb'], border=True)
    c.bar_chart(df_filtre_maison, y_label="Prix m2 en €", stack=False)
    d.bar_chart(df_filtre_maison_loc, y_label="Loyer m2 en €", color=["#fd0", "#f0f", "#04f"], stack=False)



st.divider()
st.header("Page 3")
st.divider()

# with st.container():
#     st.header('Test map')
#     m2 = folium.Map(location=nantes_coords, zoom_start=8)
#     folium.GeoJson(geojson_path).add_to(m)
#     m2


# # Block : Looker
# with st.container():
#     st.header("Dashboard Looker intégré")
#     url = "https://lookerstudio.google.com/embed/reporting/5ba61afc-11d4-47d4-9bd4-81021534e0ef/page/p_fcin9i4nvd"
#     # Insérer avec iframe
#     st.components.v1.iframe(url, width=1200, height=675, scrolling=True)