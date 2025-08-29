import os
import json
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials

print("The directory where I'm is :")
print(os.getcwd())

df = pd.read_csv('df_MA_calcul.csv')

mask_dep44 = (df['Departement'] == 'Loire-Atlantique')
mask_dep85 = (df['Departement'] == 'Vendée')
mask_dep49 = (df['Departement'] == 'Maine-et-Loire')
mask_dep53 = (df['Departement'] == 'Mayenne')
mask_dep72 = (df['Departement'] == 'Sarthe')

df_dep44 = df.loc[mask_dep44]
df_dep85 = df.loc[mask_dep85]
df_dep49 = df.loc[mask_dep49]
df_dep53 = df.loc[mask_dep53]
df_dep72 = df.loc[mask_dep72]

# Path to the service account JSON key
SERVICE_ACCOUNT_FILE = json.loads(os.environ['GCP_SERVICE_ACCOUNT_V'])

# Define scopes
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Authenticate with the service account
creds = Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)

# Open the Google Sheet by name
for_df_dep44 = gc.open_by_key("1wqVyh3TCP974SMXgXuWFHaRbfjqR0rJYMTwIB7b8_OA").sheet1  
for_df_dep85 = gc.open_by_key("1C8ymzz8WQyHDPLHe46LpgeMjIdhRU5jg9o8nDE1fo4I").sheet1  
for_df_dep49 = gc.open_by_key("1CMqbKjtg4JyDSMVNZ_GA2yZYGdQs181R9kaJ4vILTaQ").sheet1  
for_df_dep53 = gc.open_by_key("1nNOct3dPJiUzBjAc70ohY0wq8TsVIqgBN-kR_1zE0LI").sheet1  
for_df_dep72 = gc.open_by_key("1R9lCZZh_1ABlZYPqnXatAfpMO0tTNb1I1-yAzBZrVZM").sheet1  

# Write DataFrame to the sheet (overwrites)
set_with_dataframe(for_df_dep44, df_dep44)
set_with_dataframe(for_df_dep85, df_dep85)
set_with_dataframe(for_df_dep49, df_dep49)
set_with_dataframe(for_df_dep53, df_dep53)
set_with_dataframe(for_df_dep72, df_dep72)