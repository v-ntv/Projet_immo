import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px
import plotly.graph_objects as go
import json
import requests
import numpy as np
from sklearn.preprocessing import MinMaxScaler


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
st.title("🕵️‍♂️ Comparaison entre plusieurs villes")

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


st.subheader('Comparaison')

# Le fichier GeoJSON doit avoir une propriété 'codegeo' qui correspond à la colonne 'code_commune' du CSV.
communes_data['Code_insee'] = communes_data['Code_insee'].astype(str)


#Selection de la ville
ville2=st.multiselect(
        "Selectionner les Villes à comparer",
        options=communes_data['ville'].unique(),
        default=["Nantes","Angers","Vertou"],
        max_selections=6
    )

# Créez le DataFrame filtré
df_filtre2 = communes_data[communes_data['ville'].isin(ville2)]
df_filtre2 = df_filtre2.set_index(['ville'])

with st.expander('Data Preview 2'):
    st.dataframe(df_filtre2)

#Init couleurs
couleurs_palette = px.colors.qualitative.Plotly


#Création des graphique Plotly
fig_prixm2 = px.bar(
    df_filtre2,
    x=df_filtre2.index,
    y=['prix_global'],
    title = f"Prix m2 à {df_filtre2.index[0]}",
    barmode="group",
    color=df_filtre2.index,
    color_discrete_sequence=couleurs_palette
)

fig_loyerm2 = px.bar(
    df_filtre2,
    x=df_filtre2.index,
    y=['loyer_global'],
    title = f"Loyer m2 à {df_filtre2.index[0]}",
    barmode="group",
    color=df_filtre2.index,
    color_discrete_sequence=couleurs_palette
)

fig_ratiom2 = px.bar(
    df_filtre2,
    x=df_filtre2.index,
    y=['ratio_m2_glb'],
    title = f"Ratio en l'achat et la mise en location en m2",
    barmode="group",
    color=df_filtre2.index,
    color_discrete_sequence=couleurs_palette
)

fig_tension = px.bar(
    df_filtre2,
    x=df_filtre2.index,
    y=['INDICE_TENSION_LOG'],
    title = f"Tension locative",
    barmode="group",
    color=df_filtre2.index,
    color_discrete_sequence=couleurs_palette
)

fig_croipop = px.bar(
    df_filtre2,
    x=df_filtre2.index,
    y=['CROI_POP_16_22'],
    title = f"Croissance de la population",
    barmode="group",
    color=df_filtre2.index,
    color_discrete_sequence=couleurs_palette
)

#Afficher le graphique dans Streamlit
a, b, c = st.columns(3)
a.plotly_chart(fig_prixm2)
b.plotly_chart(fig_loyerm2)
c.plotly_chart(fig_ratiom2)
a.plotly_chart(fig_tension)
b.plotly_chart(fig_croipop)