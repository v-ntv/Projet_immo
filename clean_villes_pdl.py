import pandas as pd
import unicodedata
import re
import gdown

# importation du fichier csv
file_id = "1jswqR4I0L9xW4wVMjDk3TJqxAD03MZo07D0i6E"
gdown.download(f"https://drive.google.com/uc?export=download&id={file_id}", "df_pdl.csv", quiet=False)

df = pd.read_csv("df_pdl.csv")

# Fonction pour mettre en minuscules et avec des tirets les villes
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

# Exemple : ton DataFrame avec 1200 lignes
# Ici je simule quelques données
df = pd.DataFrame({
    "ville": ["Évry Courcouronnes", "Aix-en-Provence", "Saint Étienne", "Nîmes", "L'Haÿ-les-Roses"]
})

# Création de la nouvelle colonne
df["ville_slug"] = df["ville"].apply(slugify_ville)

print(df.head())
