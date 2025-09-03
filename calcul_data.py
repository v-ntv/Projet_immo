# Import libraries 
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

# scope where we need to search files
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# authentification with GCP account
creds = Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)

# open csv files
sheet = gc.open_by_key("1ZwK81NBWhM_xvQgKaSzRp-u7tF0HLd2stJS8F9VNyFY").sheet1  
sheet2 = gc.open_by_key("1r0bFPyZa5a0PgXBB3inwMLj5dpAYrT-yfbkQagG40Xw").sheet1  
sheet3 = gc.open_by_key("1xL4a5Cn6h9JK-36gwi8xrwXAMocrmcpM9oNgcZpiJhk").sheet1  

# get values
data = sheet.get_all_records()
data2 = sheet2.get_all_records()

# convert to DF
df_fiscality = pd.DataFrame(data)
df_MA_clean = pd.DataFrame(data2)

# ajout de la colonne geo sur df_MA_clean
df_MA_clean['geo'] = df_MA_clean['ville'] + ', ' + df_MA_clean['Departement'] + ', France'

# Creating mask to check where 'loyer_maison' contains null values and replacing them with 'loyer_appartement' (because it was inverted in meilleurs-agents)
mask = df_MA_clean['loyer_maison'].isna()

if mask.any(): 
    df_MA_clean.loc[mask, 'loyer_maison'] = df_MA_clean.loc[mask, 'loyer_appartement']
    df_MA_clean.loc[mask, 'loyer_appartement'] = np.nan
    
    df_MA_clean.loc[mask, 'loyer_min_maison'] = df_MA_clean.loc[mask, 'loyer_min_appartement']
    df_MA_clean.loc[mask, 'loyer_min_appartement'] = np.nan
    
    df_MA_clean.loc[mask, 'loyer_max_maison'] = df_MA_clean.loc[mask, 'loyer_max_appartement']
    df_MA_clean.loc[mask, 'loyer_max_appartement'] = np.nan

# Check in df_fiscality the fiscality in every city in the current and last year
today = datetime.today()
current_year = today.year
link_year = current_year - 1

# Filter for current year
df_current = df_fiscality[df_fiscality['EXERCICE'] == current_year]

if not df_current.empty:
    df_fiscality_year = df_current
else:
    df_fiscality_year = df_fiscality[df_fiscality['EXERCICE'] == link_year]

# Select the needed columns
df_fiscality_clean = df_fiscality_year[['Taux_Global_TFB', 'INSEE COM']]

# Join df_MA and df_fiscality by insee code with a left join to keep all rows in df_MA
df_MA_clean['Code_insee'] = df_MA_clean['Code_insee'].astype(str)
df_fiscality_clean['INSEE COM'] = df_fiscality_clean['INSEE COM'].astype(str)

df_merged = df_MA_clean.merge(df_fiscality_clean, how='left', left_on='Code_insee', right_on='INSEE COM')

# Keep all needed columns and divide by 100 'Taux_Global_TFB' for easier calculation later
df_merged_clean = df_merged[['ville','prix_appartement','min_appartement','max_appartement','prix_maison','min_maison','max_maison','loyer_appartement','loyer_min_appartement','loyer_max_appartement','loyer_maison','loyer_min_maison','loyer_max_maison','Taux_Global_TFB','Code_insee','Code_postal','Departement','geo']]
df_merged['Taux_Global_TFB'] = df_merged_clean['Taux_Global_TFB'] / 100

# Create a mask for all departments and fill the NaN values with the average 'Taux_Global_TFB' per department
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

# Load df_norm, but only keep the columns you need + the key for merge
df_norm = pd.read_csv('df_norm.csv', usecols=['CODE_INSEE', 'INDICE_TENSION_LOG', 'CROI_POP_16_22'])

# Convert both keys to string
df_merged_clean['Code_insee'] = df_merged_clean['Code_insee'].astype(str)
df_norm['CODE_INSEE'] = df_norm['CODE_INSEE'].astype(str)

# Merge with df_merged_clean
df_merged_clean_wnorm = df_merged_clean.merge(
    df_norm,
    left_on='Code_insee',
    right_on='CODE_INSEE',
    how='left'
)

# export du csv sur gsheet
sheet3.clear()
set_with_dataframe(sheet3, df_merged_clean_wnorm)