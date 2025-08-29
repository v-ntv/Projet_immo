# Import pandas, numpy and random libraries 
import pandas as pd
import numpy as np
import random
from datetime import datetime

# Loading all DF
df_fiscality = pd.read_csv('df_fiscality.csv')
df_MA_temp = pd.read_csv('df_MA_clean.csv')

# Droping column with false values
df_MA_clean = df_MA_temp.drop(columns=['Taux_Global_TFB'])

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
df_merged_clean = df_merged[['ville','prix_appartement','min_appartement','max_appartement','prix_maison','min_maison','max_maison','loyer_appartement','loyer_min_appartement','loyer_max_appartement','loyer_maison','loyer_min_maison','loyer_max_maison','Taux_Global_TFB','Code_insee','Departement','geo']]
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

# Save the final df to a csv
df_merged_clean.to_csv('df_MA_calcul.csv',index=False)