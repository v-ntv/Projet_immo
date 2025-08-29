#Import subprocess and sys
import subprocess
import sys

# Install requests
subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

# Import pandas, requests and io
import pandas as pd
import requests
from io import StringIO

# Get content by ignoring SSL
url = 'https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/fiscalite-locale-des-particuliers/exports/csv?lang=fr&timezone=Europe%2FParis&use_labels=true&delimiter=%3B'

response = requests.get(url, verify=False)

# Load in a DF
df_fiscality = pd.read_csv(StringIO(response.text), delimiter=';')

# Save file to a csv
df_fiscality.to_csv('df_fiscality.csv')