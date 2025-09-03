# Importation des librairies 
import pandas as pd
import numpy as np
import random
from datetime import datetime
import os
import json
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
import gdown

SERVICE_ACCOUNT_FILE = json.loads(os.environ['GCP_SERVICE_ACCOUNT_V'])

# Définir où chercher les fichiers
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# authentification avec le compte GCP 
creds = Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)

# ouverture des fichiers csv 
sheet = gc.open_by_key("1ZwK81NBWhM_xvQgKaSzRp-u7tF0HLd2stJS8F9VNyFY").sheet1  
sheet2 = gc.open_by_key("1r0bFPyZa5a0PgXBB3inwMLj5dpAYrT-yfbkQagG40Xw").sheet1  
sheet3 = gc.open_by_key("1xL4a5Cn6h9JK-36gwi8xrwXAMocrmcpM9oNgcZpiJhk").sheet1  

# obtenir les données des csv
data = sheet.get_all_records()
data2 = sheet2.get_all_records()

# convertir les csv en dataframe
df_fiscality = pd.DataFrame(data)
df_MA_temp = pd.DataFrame(data2)

# Convertir les codes en str
df_MA_temp['Code_postal'] = df_MA_temp['Code_postal'].astype(str)
df_MA_temp['Code_insee'] = df_MA_temp['Code_insee'].astype(str)

# GroupBy avec aggregation personnalisée
df_MA_clean = df_MA_temp.groupby('ville', as_index=False).agg({
    'Code_postal': 'first',  
    'Code_insee': 'first',   
    'Departement': 'first',
    # on prend la moyenne des anciennes colonnes pour les mettre sur la nouvelle avec les bonnes infos
    **{col: 'mean' for col in df_MA_temp.select_dtypes(include='number').columns}
})

# ajout de la colonne geo sur df_MA_clean
df_MA_clean['geo'] = df_MA_clean['ville'] + ', ' + df_MA_clean['Departement'] + ', France'

# création d'un masque pour vérifier si 'loyer_maison' contient des valeurs null et si oui les remplacer par celle de 'loyer_appartement' (parce que c'est inversé sur le site meilleurs-agents)
mask = df_MA_clean['loyer_maison'].isna()

if mask.any(): 
    df_MA_clean.loc[mask, 'loyer_maison'] = df_MA_clean.loc[mask, 'loyer_appartement']
    df_MA_clean.loc[mask, 'loyer_appartement'] = np.nan
    
    df_MA_clean.loc[mask, 'loyer_min_maison'] = df_MA_clean.loc[mask, 'loyer_min_appartement']
    df_MA_clean.loc[mask, 'loyer_min_appartement'] = np.nan
    
    df_MA_clean.loc[mask, 'loyer_max_maison'] = df_MA_clean.loc[mask, 'loyer_max_appartement']
    df_MA_clean.loc[mask, 'loyer_max_appartement'] = np.nan

# Vérification dans df_fiscality: la fiscalité dans chaque ville sur l'année actuelle et l'année passée
today = datetime.today()
current_year = today.year
link_year = current_year - 1

# filtre sur l'année actuelle 
df_current = df_fiscality[df_fiscality['EXERCICE'] == current_year]

if not df_current.empty:
    df_fiscality_year = df_current
else:
    df_fiscality_year = df_fiscality[df_fiscality['EXERCICE'] == link_year]

# Sélection des colonnes nécessaires 
df_fiscality_clean = df_fiscality_year[['Taux_Global_TFB', 'INSEE COM']]

# Merging du df_MA et df_fiscality par le code INSEE avec un left join pour garder toutes les lignes de df_MA 
df_MA_clean['Code_insee'] = df_MA_clean['Code_insee'].astype(str)
df_fiscality_clean['INSEE COM'] = df_fiscality_clean['INSEE COM'].astype(str)

df_merged = df_MA_clean.merge(df_fiscality_clean, how='left', left_on='Code_insee', right_on='INSEE COM')

# On garde toutes les colonnes nécessaires et on divise par 100 la colonne 'Taux_Global_TFB' pour faciliter les calculs plus tard
df_merged_clean = df_merged[['ville','prix_appartement','min_appartement','max_appartement','prix_maison','min_maison','max_maison','loyer_appartement','loyer_min_appartement','loyer_max_appartement','loyer_maison','loyer_min_maison','loyer_max_maison','Taux_Global_TFB','Code_insee','Code_postal','Departement','geo']]
df_merged['Taux_Global_TFB'] = df_merged_clean['Taux_Global_TFB'] / 100

# Création de masques en fonction de chaque département, on rempli les valeurs null avec la valeur moyenne de 'Taux_Global_TFB' pour chaque département
mask_dep44 = (df_merged_clean['Departement'] == 'Loire-Atlantique')
mask_dep85 = (df_merged_clean['Departement'] == 'Vendée')
mask_dep49 = (df_merged_clean['Departement'] == 'Maine-et-Loire')
mask_dep53 = (df_merged_clean['Departement'] == 'Mayenne')
mask_dep72 = (df_merged_clean['Departement'] == 'Sarthe')

if (df_merged_clean.loc[mask_dep44, 'Taux_Global_TFB'].isna().any()):
    mean_value = df_merged_clean.loc[mask_dep44, 'Taux_Global_TFB'].mean()
    df_merged_clean.loc[mask_dep44 & df_merged_clean['Taux_Global_TFB'].isna(), 'Taux_Global_TFB'] = mean_value

if (df_merged_clean.loc[mask_dep85, 'Taux_Global_TFB'].isna().any()):
    mean_value = df_merged_clean.loc[mask_dep85, 'Taux_Global_TFB'].mean()
    df_merged_clean.loc[mask_dep85 & df_merged_clean['Taux_Global_TFB'].isna(), 'Taux_Global_TFB'] = mean_value

if (df_merged_clean.loc[mask_dep49, 'Taux_Global_TFB'].isna().any()):
    mean_value = df_merged_clean.loc[mask_dep49, 'Taux_Global_TFB'].mean()
    df_merged_clean.loc[mask_dep49 & df_merged_clean['Taux_Global_TFB'].isna(), 'Taux_Global_TFB'] = mean_value

if (df_merged_clean.loc[mask_dep53, 'Taux_Global_TFB'].isna().any()):
    mean_value = df_merged_clean.loc[mask_dep53, 'Taux_Global_TFB'].mean()
    df_merged_clean.loc[mask_dep53 & df_merged_clean['Taux_Global_TFB'].isna(), 'Taux_Global_TFB'] = mean_value

if (df_merged_clean.loc[mask_dep72, 'Taux_Global_TFB'].isna().any()):
    mean_value = df_merged_clean.loc[mask_dep72, 'Taux_Global_TFB'].mean()
    df_merged_clean.loc[mask_dep72 & df_merged_clean['Taux_Global_TFB'].isna(), 'Taux_Global_TFB'] = mean_value

# convertir en numériques 
cols_to_numeric = [
    'prix_appartement', 'prix_maison',
    'min_appartement', 'min_maison',
    'max_appartement', 'max_maison',
    'loyer_appartement', 'loyer_maison',
    'loyer_min_appartement', 'loyer_min_maison',
    'loyer_max_appartement', 'loyer_max_maison'
]

for col in cols_to_numeric:
    df_merged_clean[col] = pd.to_numeric(df_merged_clean[col], errors='coerce')

# Ajout des données global + ratio en Python
df_merged_clean['prix_global'] = (df_merged_clean['prix_appartement']+df_merged_clean['prix_maison'])/2
df_merged_clean['min_global'] = (df_merged_clean['min_appartement']+df_merged_clean['min_maison'])/2
df_merged_clean['max_global'] = (df_merged_clean['max_appartement']+df_merged_clean['max_maison'])/2
df_merged_clean['loyer_global'] = (df_merged_clean['loyer_appartement']+df_merged_clean['loyer_maison'])/2
df_merged_clean['loyer_min_global'] = (df_merged_clean['loyer_min_appartement']+df_merged_clean['loyer_min_maison'])/2
df_merged_clean['loyer_max_global'] = (df_merged_clean['loyer_max_appartement']+df_merged_clean['loyer_max_maison'])/2
df_merged_clean['ratio_m2_apt'] = round(((df_merged_clean['loyer_appartement']*12)/df_merged_clean['prix_appartement'])*100,2)
df_merged_clean['ratio_m2_msn'] = round(((df_merged_clean['loyer_maison']*12)/df_merged_clean['prix_maison'])*100,2)
df_merged_clean['ratio_m2_glb'] = round(((df_merged_clean['loyer_global']*12)/df_merged_clean['prix_global'])*100,2)

# Chargement de df_norm en gardant seulement les colonnes nécessaires et la clé de merge (code INSEE)
df_norm = pd.read_csv('df_norm.csv', usecols=['CODE_INSEE', 'INDICE_TENSION_LOG', 'CROI_POP_16_22'])

# On converti les clés des 2 DF en string
df_merged_clean['Code_insee'] = df_merged_clean['Code_insee'].astype(str)
df_norm['CODE_INSEE'] = df_norm['CODE_INSEE'].astype(str)

# Merge avec df_merged_clean
df_merged_clean_wnorm = df_merged_clean.merge(
    df_norm,
    left_on='Code_insee',
    right_on='CODE_INSEE',
    how='left'
)

# export du csv sur gsheet
sheet3.clear()
set_with_dataframe(sheet3, df_merged_clean_wnorm)