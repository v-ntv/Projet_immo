# Télécharger le GeoJSON complet
url = "https://www.data.gouv.fr/api/1/datasets/r/138844a4-2994-462c-a6da-d636c13692b6"
response = requests.get(url)
# S'assurer que la requête a réussi
response.raise_for_status()
geojson = response.json()
# Filtrer pour la région des Pays de la Loire (code "52")
features_filtrees = [
    feature for feature in geojson["features"]
    if feature["properties"].get("reg") == "52"
]
# Créer un nouveau dictionnaire GeoJSON avec les données filtrées
geojson_filtre = {
    "type": "FeatureCollection",
    "features": features_filtrees
}
# Sauvegarder le GeoJSON filtré dans un fichier local
# Le nom du fichier est une chaîne de caractères (string)
nom_fichier = "pays_de_la_loire.geojson"
try:
    # Utiliser 'w' (write) et la fonction json.dump pour écrire le dictionnaire JSON
    with open(nom_fichier, 'w', encoding='utf-8') as f:
        json.dump(geojson_filtre, f, ensure_ascii=False, indent=2)
    print(f"Le fichier GeoJSON filtré a été sauvegardé sous : {nom_fichier}")
except IOError as e:
    print(f"Erreur lors de l'écriture du fichier : {e}")