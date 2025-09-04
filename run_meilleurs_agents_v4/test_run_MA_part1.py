import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
import re, random, os

# ===========================
# Configuration
# ===========================
CSV_INPUT = r'run_meilleurs_agents_v4\data_test.csv'
CSV_OUTPUT = r'run_meilleurs_agents_v4\data_test_clean.csv'
STORAGE_STATE = 'state.json'  # fichier pour session persistante
PROXY = None  # ex: "http://user:pass@proxy_ip:port" ou None
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

# ===========================
# Charger les données
# ===========================
df_data_villes_clean = pd.read_csv(CSV_INPUT)
df_data_villes_clean = df_data_villes_clean.iloc[0:50]
df_data_villes_clean['Code_postal'] = df_data_villes_clean['Code_postal'].astype(str)

# ===========================
# Fonction pour nettoyer les nombres
# ===========================
def extract_number(text):
    clean_text = text.replace("\u202f", "").replace("\xa0", "").replace("€", "").strip()
    clean_text = clean_text.replace(",", ".")
    return float(clean_text)

# ===========================
# Fonction async principale
# ===========================
async def scrape_ma():
    async with async_playwright() as p:
        browser_args = {
            "headless": False,
            "executable_path": BRAVE_PATH
        }
        if PROXY:
            browser_args["proxy"] = {"server": PROXY}

        browser = await p.chromium.launch(**browser_args)

        # Session persistante
        context_args = {
            "locale": "fr-FR",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/116.0.0.0 Safari/537.36"
        }
        if os.path.exists(STORAGE_STATE):
            context_args["storage_state"] = STORAGE_STATE

        context = await browser.new_context(**context_args)
        page = await context.new_page()

        await page.goto("https://www.meilleursagents.com/prix-immobilier/")

        all_data = []

        for index, row in df_data_villes_clean.iterrows():
            city = f"{row['Lib_MA']} ({row['Code_postal']})"
            try:
                # Pause aléatoire pour simuler humain
                await asyncio.sleep(random.uniform(3, 7))
                await page.evaluate(f"window.scrollBy(0, {random.randint(100,500)});")
                await asyncio.sleep(random.uniform(1, 2))

                # Barre de recherche
                search_box = page.locator("input[name='q']")
                await search_box.wait_for(state="visible", timeout=60000)
                await search_box.fill("")

                # Typing humain
                for char in city:
                    await search_box.type(char, delay=random.randint(50, 120))
                await search_box.press("Enter")
                await asyncio.sleep(random.uniform(4, 7))

                html = await page.content()
                soup = BeautifulSoup(html, 'html.parser')
                raw_text3 = soup.find_all("ul", class_="prices-summary__price-range")
                data_dict = {}

                if raw_text3:
                    title_text = soup.find("title").get_text().strip()
                    ville = title_text.split("Prix immobilier")[1].split("(")[0].strip()
                    data_dict["ville"] = ville

                    for ul in raw_text3:
                        li_items = ul.find_all("li")
                        label = li_items[0].get_text().strip().lower()
                        main_value = extract_number(li_items[1].get_text())
                        range_text = li_items[2].get_text().replace("\u202f", "").replace("\xa0", "").replace(",", ".")
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

                    data_dict["city"] = city
                    all_data.append(data_dict)
                    print(f"✅ Datas ajoutées pour : {ville}")
                else:
                    await page.reload()
                    await asyncio.sleep(random.uniform(3,5))

            except Exception as e:
                print(f"❌ Erreur pour {city}: {e}")

        # Sauvegarder état de session
        await context.storage_state(path=STORAGE_STATE)
        await browser.close()

        # Export CSV
        df_meilleur_agent = pd.DataFrame(all_data)
        df_meilleur_agent.to_csv(CSV_OUTPUT, index=False)
        print("Scraping terminé. CSV enregistré !")

# ===========================
# Exécuter l’async
# ===========================
if __name__ == "__main__":
    asyncio.run(scrape_ma())
