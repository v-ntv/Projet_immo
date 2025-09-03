# importer les librairies
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os
import json
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
import gdown
import requests

# récupérer le csv df_MA_clean_v2
import pandas as pd

sheet_id = "1xL4a5Cn6h9JK-36gwi8xrwXAMocrmcpM9oNgcZpiJhk"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

df = pd.read_csv(url)

# mettre les colonnes dans l'ordre
colonnes = ['ville','prix_appartement','min_appartement',
            'max_appartement','prix_maison','min_maison',
            'max_maison','loyer_appartement','loyer_min_appartement',
            'loyer_max_appartement','loyer_maison','loyer_min_maison',
            'loyer_max_maison','prix_global','min_global','max_global',
            'loyer_global','loyer_min_global','loyer_max_global','ratio_m2_apt',
            'ratio_m2_msn','ratio_m2_glb','Taux_Global_TFB','Code_insee',
            'Code_postal','Departement','geo','INDICE_TENSION_LOG','CROI_POP_16_22']

df_clean = df[colonnes]

# export sur le dossier streamlit
df_clean.to_csv('Streamlit/df_MA_clean3.csv')

# Télécharger le GeoJSON complet
url = "https://www.data.gouv.fr/api/1/datasets/r/138844a4-2994-462c-a6da-d636c13692b6"
response = requests.get(url)

# S'assurer que la requête a réussi
response.raise_for_status()
geojson = response.json()

# Filtrer pour la région des Pays de la Loire (code "52")
features_filtrees = [
    feature for feature in geojson["features"]
    if feature["properties"].get("reg") == "52"
]
# Créer un nouveau dictionnaire GeoJSON avec les données filtrées
geojson_filtre = {
    "type": "FeatureCollection",
    "features": features_filtrees
}

# Sauvegarder le GeoJSON filtré dans un fichier local
# Le nom du fichier est une chaîne de caractères (string)
nom_fichier = "Streamlit/pays_de_la_loire.geojson"
try:
    # Utiliser 'w' (write) et la fonction json.dump pour écrire le dictionnaire JSON
    with open(nom_fichier, 'w', encoding='utf-8') as f:
        json.dump(geojson_filtre, f, ensure_ascii=False, indent=2)
    print(f"Le fichier GeoJSON filtré a été sauvegardé sous : {nom_fichier}")
except IOError as e:
    print(f"Erreur lors de l'écriture du fichier : {e}")