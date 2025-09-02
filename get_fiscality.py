#Import subprocess and sys
import subprocess
import sys
import os
import json
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
import gdown

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
sheet = gc.open_by_key("1ZwK81NBWhM_xvQgKaSzRp-u7tF0HLd2stJS8F9VNyFY").sheet1  

# récupérer toutes les valeurs
data = sheet.get_all_records()

# convertir en DataFrame
df = pd.DataFrame(data)

# Import pandas, requests and io
import pandas as pd
import requests
from io import StringIO

# Get content by ignoring SSL
url = 'https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/fiscalite-locale-des-particuliers/exports/csv?lang=fr&timezone=Europe%2FParis&use_labels=true&delimiter=%3B'

response = requests.get(url, verify=False)

# Load in a DF
df_fiscality = pd.read_csv(StringIO(response.text), delimiter=';')

chunk_size = 5000  # 5000 lignes par batch
for start in range(0, len(df_fiscality), chunk_size):
    end = min(start + chunk_size, len(df_fiscality))
    chunk = df_fiscality.iloc[start:end]

    # inclure les entêtes seulement pour le premier batch
    set_with_dataframe(sheet, chunk, row=start+1, include_column_header=(start==0))
