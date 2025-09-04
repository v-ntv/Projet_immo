# importation des librairies
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import re, time, random

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
sheet = gc.open_by_key("11VsO4-jk8E5Ti3uwilvp9j3CxEug1TI9T07vJbT1kAU").sheet1  
sheet2 = gc.open_by_key("1r0bFPyZa5a0PgXBB3inwMLj5dpAYrT-yfbkQagG40Xw").sheet1

# récupérer toutes les valeurs
data = sheet.get_all_records()

# convertir en DataFrame
df_data_villes_clean = pd.DataFrame(data)

# lignes 0 → 49 (50 lignes)
df_data_villes_clean = df_data_villes_clean.iloc[0:50]    

def extract_number(text):
    """Nettoyer le texte et transformer en float"""
    clean_text = text.replace("\u202f", "").replace("\xa0", "").replace("€", "").strip()
    clean_text = clean_text.replace(",", ".")
    return float(clean_text)

# Setup de Selenium (Chrome est auto-géré par Selenium Manager; Chrome doit être installé)
options = webdriver.ChromeOptions()
options.add_argument("--lang=fr-FR")
options.add_argument("--disable-blink-features=AutomationControlled")
# Décommenter la ligne ci-dessous pour faire persister les cookies de la session entre chaque run:
# options.add_argument(r"--user-data-dir=C:\Users\Dell\AppData\Local\Google\Chrome\User Data\ScrapeProfile")

driver = webdriver.Chrome(options=options)
stealth(driver,
    languages=["fr-FR", "fr"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)
driver.set_window_size(1366, 768)

# Lancer le navigateur
driver.get("https://www.meilleursagents.com/prix-immobilier/")

# Liste pour stocker toutes les données
all_data = []
error_data = []

for index, row in df_data_villes_clean.iterrows():
    city = row['Lib_MA']+" ("+row['Code_postal']+")"
    try:
        # Simuler un comportement humain 
        time.sleep(random.uniform(1.8, 3.6))

        # Trouver la barre de recherche
        search_box = driver.find_element(By.NAME, "q")

        # Simuler une frappe clavier, caractère par caractère
        for y in city:
            search_box.clear()
            search_box.send_keys(y)
            time.sleep(0.05)  # petite pause pour rendre la frappe réaliste

        # Valider avec la touche Entrée
        time.sleep(1)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        raw_text3 = soup.find_all("ul", class_="prices-summary__price-range")
        data_dict = {}

        # condition pour clear la barre de recherche si il ne trouve pas la ville
        if not raw_text3 :
            driver.refresh()
            time.sleep(3)
        else:
            # Ajouter la ville
            title_text = soup.find("title").get_text().strip()
            ville = title_text.split("Prix immobilier")[1].split("(")[0].strip()
            data_dict["ville"] = ville

            for ul in raw_text3:
                li_items = ul.find_all("li")
                label = li_items[0].get_text().strip().lower()
                main_value = extract_number(li_items[1].get_text())

                # Nettoyer le texte pour récupérer min et max correctement
                range_text = li_items[2].get_text()
                range_text = range_text.replace("\u202f", "").replace("\xa0", "").replace(",", ".")

                # Extraire tous les nombres sous forme de float
                numbers_in_range = [float(n) for n in re.findall(r"[\d\.]+", range_text)]
                if "prix" in label:
                    if "prix_appartement" not in data_dict:
                        data_dict["prix_appartement"] = main_value
                        data_dict["min_appartement"] = numbers_in_range[0]
                        data_dict["max_appartement"] = numbers_in_range[1]
                    else:
                        data_dict["prix_maison"] = main_value
                        data_dict["min_maison"] = numbers_in_range[0]
                        data_dict["max_maison"] = numbers_in_range[1]
                elif "loyer" in label:
                    if "loyer_appartement" not in data_dict:
                        data_dict["loyer_appartement"] = main_value
                        data_dict["loyer_min_appartement"] = numbers_in_range[0]
                        data_dict["loyer_max_appartement"] = numbers_in_range[1]
                    else:
                        data_dict["loyer_maison"] = main_value
                        data_dict["loyer_min_maison"] = numbers_in_range[0]
                        data_dict["loyer_max_maison"] = numbers_in_range[1]

            # Ajouter l'URL pour référence
            data_dict["city"] = city
            all_data.append(data_dict)
            print(f"Datas ajoutées pour la ville : {ville}")

    except Exception as e:
        print(f"Erreur pour la ville {city}: {e}")
        error_data.append({
        "city": city,
        "erreur": str(e)})

    # Pause pour ne pas surcharger le site
    time.sleep(random.uniform(1.8, 3.6))

driver.quit()

# Convertir en DataFrame
# df_scraped = pd.DataFrame(all_data)
# df_scraped.head()

driver.quit()

df_meilleur_agent = pd.DataFrame(all_data)

set_with_dataframe(sheet2, df_meilleur_agent) 
