import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import duckdb
#import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="Projet Immo Le Wagon",
    page_icon="🏛",
    layout="wide"
 )
st.title("Dashboard")

# --- Chargement des données ---
@st.cache_data
def load_data():
    # Charger le fichier GeoJSON des communes
    geojson_path = "communes.geojson" 
    # Charger les données de meilleur agent
    data_MA = "df_MA_clean.csv"
    # Charger les données avec pandas
    communes_df = pd.read_csv(data_MA)

    return geojson_path, communes_df

geojson_path, communes_data = load_data()

# --- SideBar ---
with st.sidebar:
    st.image("Logo_le_wagon.png", caption="Le wagon")
    st.header("Filtres")
    type_de_bien = st.pills(
        "Sélectionnez le type de bien :",
        ["Appartements", "Maisons"],
        default="Appartements"
    )
    ville=st.multiselect(
        "Select Ville",
        options=communes_data['ville'].unique(),
        default=communes_data['ville'][91]
    )
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

# --- Préparation des variables en fonction de la sélection ----
if type_de_bien == "Appartements":
    colonne_valeur = "prix_appartement"
    nom_legende = "Prix moyen des appartements (€/m²)"
elif type_de_bien == "Maisons":
    colonne_valeur = "prix_maison"
    nom_legende = "Prix moyen des maisons (€/m²)"


# --- Préparation des données pour la carte ---
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
    smooth_factor=0.5
).add_to(m)

# Ajout d'une couche de contrôle pour activer/désactiver la carte choroplèthe
folium.LayerControl().add_to(m)

# Affichage de la carte dans Streamlit
st_folium(m, width=1200, height=800)


# Créez le DataFrame filtré
df_filtre = communes_data[communes_data['ville'].isin(ville)]
df_filtre = df_filtre.set_index(['ville'])
df_filtre_apt = df_filtre[['prix_appartement','min_appartement','max_appartement']] 
df_filtre_apt_loc = df_filtre[['loyer_appartement', 'loyer_min_appartement', 'loyer_max_appartement']]
df_filtre_maison = df_filtre[['prix_maison',"min_maison",'max_maison']]
df_filtre_maison_loc = df_filtre[['loyer_maison', 'loyer_min_maison', 'loyer_max_maison']]

with st.expander('Data Preview'):
    st.dataframe(df_filtre)



tab1, tab2, tab3 = st.tabs(["Appartements", "Maisons", "Global"])

with tab1:
    st.subheader("Standart ratio au m2 pour les appartements")
    a, b = st.columns(2)
    c, d = st.columns(2)
    df_filtre_apt['ratio_m2'] = round(((df_filtre['loyer_appartement']*12)/df_filtre['prix_appartement'])*100,2)
    a.metric("Ratio achat/Loc", df_filtre_apt['ratio_m2'], border=True)
    c.bar_chart(df_filtre_apt, y_label="Prix m2 en €",stack=False)
    d.bar_chart(df_filtre_apt_loc, y_label="Loyer m2 en €", color=["#fd0", "#f0f", "#04f"], stack=False)


with tab2:
    st.subheader("Standart ratio au m2 pour les Maison")
    a, b = st.columns(2)
    c, d = st.columns(2)
    c.bar_chart(df_filtre_maison, y_label="Prix m2 en €", stack=False)
    d.bar_chart(df_filtre_maison_loc, y_label="Loyer m2 en €", color=["#fd0", "#f0f", "#04f"], stack=False)








# # Block : Looker
# with st.container():
#     st.header("Dashboard Looker intégré")
#     url = "https://lookerstudio.google.com/embed/reporting/5ba61afc-11d4-47d4-9bd4-81021534e0ef/page/p_fcin9i4nvd"
#     # Insérer avec iframe
#     st.components.v1.iframe(url, width=1200, height=675, scrolling=True)