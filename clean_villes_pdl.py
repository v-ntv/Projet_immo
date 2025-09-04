#importation des librairies
import os
import json
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
import gdown
import unicodedata
import re

# chemin vers mon secret github (clé json GCP) 
SERVICE_ACCOUNT_FILE = json.loads(os.environ['GCP_SERVICE_ACCOUNT_V'])

# on défini où chercher les fichiers
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# authentification avec le compte GCP 
creds = Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)

# ouverture du fichier csv
sheet = gc.open_by_key("1jswqR4I0L9xW4wVMjDk3TJqxAD03MZo07D0i6E-HoB0").sheet1  
sheet2 = gc.open_by_key("11VsO4-jk8E5Ti3uwilvp9j3CxEug1TI9T07vJbT1kAU").sheet1  

# récupérer toutes les valeurs
data = sheet.get_all_records()

# convertir en DataFrame
df = pd.DataFrame(data)

# fonction pour mettre les villes en minuscules, sans accents et avec des tirets
def slugify_ville(ville: str) -> str:
    if pd.isna(ville):  # gérer les NaN
        return ville
    # minuscules 
    ville = ville.lower()
    # enlever les accents
    ville = ''.join(
        c for c in unicodedata.normalize('NFD', ville)
        if unicodedata.category(c) != 'Mn'
    )
    # remplacer tout ce qui n'est pas lettre/chiffre/espace par un tiret
    ville = re.sub(r"[^a-z0-9\s-]", "-", ville)
    # remplacer les espaces par des tirets
    ville = re.sub(r"\s+", "-", ville)
    # supprimer les tirets multiples
    ville = re.sub(r"-+", "-", ville).strip("-")
    return ville

# application du filtre
df_new = df.copy()
df_new["ville_slug"] = df_new["old_ville"].apply(slugify_ville)


# remplacer les colonnes :
# ville	
# Code_insee	

# par les colonnes :
# #Code_commune_INSEE	
# Lib_MA	
# Nom_de_la_commune_url	
# url

# créer une colonne "ville_finale" qui prend old_ville si dispo, sinon ville
df_new["ville_finale"] = df_new["old_ville"].combine_first(df_new["ville"])

# slugify sur ville_finale
df_new["ville_slug"] = df_new["ville_finale"].apply(slugify_ville)

df_new['#Code_commune_INSEE'] = df_new['old_Code_insee']
df_new['Lib_MA'] = df_new['ville_finale']
base_url = "https://www.meilleursagents.com/prix-immobilier/"
df_new["url"] = base_url + df_new["ville_slug"] + "-" + df_new["old_Code_postal"].astype(str) + "/"

# ré-écriture du fichier csv pour le mettre à jour
set_with_dataframe(sheet2, df_new) 
