# importer les librairies
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os
import json
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
import gdown

url = "https://drive.google.com/uc?id=1hj72ZgbFI0lmB9klZknntpaG2XXrJLOq"
output = "dossier_complet_insee.csv"
#gdown.download(url, output, quiet=False)

df = pd.read_csv('dossier_complet_insee.csv', sep=';')

df["CODE_INSEE"] = df["CODGEO"].astype(str).str.strip().str.zfill(5)   # code commune à 5 chiffres
df["DEP"] = df["CODE_INSEE"].str[:2] 

# Liste des départements à filtrer
Pays_de_la_loire = ['44','49','53','85','72']

# Filtrage
df_pdl = df[df['DEP'].isin(Pays_de_la_loire)]

# On sélectionne uniquement les colonnes intéressantes
df_pdl_filtre = df_pdl.loc[:,['CODE_INSEE',
               'DEP',
               'P22_POP',
                'P22_POP0014',
                'P22_POP1529',
                'P22_POP3044',
                'P22_POP4559',
                'P22_POP6074',
                'P22_POP7589',
                'P22_POP90P',
                'P16_POP',
                'P22_CHOM1564',
                'P22_ACT1564',
                'P22_ACTOCC1564',
                'P22_INACT1564', 
                'P16_POP0014',
                'P16_POP1529',
                'P16_POP3044',
                'P16_POP4559',
                'P16_POP6074',
                'P16_POP7589',
                'P16_POP90P',
                'P11_POP',
                'P11_POP0014',
                'P11_POP1529',
                'P11_POP3044',
                'P11_POP4559',
                'P11_POP6074',
                'P11_POP7589',
                'P11_POP90P',
                'C22_MEN',
                'C16_MEN',
                'C11_MEN',
                'P22_MEN',
                'P22_LOG',
                'P22_RP',
                'P22_RSECOCC',
                'P22_LOGVAC',
                'P22_MAISON',
                'P22_APPART',
                'SUPERF',
                'NAIS1621',
                'NAIS1115',
                'NAIS0610',
                'NAIS9905',
                'NAIS9099',
                'NAIS8290',
                'NAIS7582',
                'NAIS6875',
                'DECE1621',
                'DECE1115',
                'DECE0610',
                'DECE9905',
                'DECE9099',
                'DECE8290',
                'DECE7582',
                'DECE6875',
                'MED21',
                'TP6021',
                'D121',
                'D921',
                'RD21',
                'SNHM22',
                'ENCTOT24',
                'ENCTOT23',
                'ENCTOT22',
                'ENCTOT21',
                'ENCTOT20',
                'ENCTOT19',
                'ENCTOT18',
                'ENCTOT17',
                'ENCTOT16',
                'ENCTOT15',
                'ENCTOT14',
                'ENCTOT13',
                'ENCTOT12',
                'BPE_2024_A501',
                'BPE_2024_B104',
                'BPE_2024_B105',
                'BPE_2024_B201',
                'BPE_2024_B202',
                'BPE_2024_B207',
                'BPE_2024_B316',
                'BPE_2024_B326',
                'BPE_2024_C107',
                'BPE_2024_C108',
                'BPE_2024_C109',
                'BPE_2024_C201',
                'BPE_2024_C301',
                'BPE_2024_C304',
                'BPE_2024_C302',
                'BPE_2024_C303',
                'BPE_2024_C305',
                'BPE_2024_D265',
                'BPE_2024_D277',
                'BPE_2024_D279',
                'BPE_2024_D281',
                'BPE_2024_D250',
                'BPE_2024_D307',
                'BPE_2024_F307',
                'P22_RP_LOCHLMV',
                            ]]


# Nombre de commerces
df_pdl_filtre['NB_COM_22'] = df_pdl_filtre[['BPE_2024_A501',
                                            'BPE_2024_B104',
                                            'BPE_2024_B105',
                                            'BPE_2024_B201',
                                            'BPE_2024_B202',
                                            'BPE_2024_B207',
                                            'BPE_2024_B316',
                                            'BPE_2024_B326',
                                            'BPE_2024_C107',
                                            'BPE_2024_C108',
                                            'BPE_2024_C109',
                                            'BPE_2024_C201',
                                            'BPE_2024_C301',
                                            'BPE_2024_C304',
                                            'BPE_2024_C302',
                                            'BPE_2024_C303',
                                            'BPE_2024_C305',
                                            'BPE_2024_D265',
                                            'BPE_2024_D277',
                                            'BPE_2024_D279',
                                            'BPE_2024_D281',
                                            'BPE_2024_D250',
                                            'BPE_2024_D307',
                                            'BPE_2024_F307']].sum(axis=1)

# densité des logements en 2022
df_pdl_filtre['DENS_LOG_22'] = round((df_pdl_filtre['P22_LOG'] / df_pdl_filtre['SUPERF']),1)

# Répartition maison ou appartement en 2022 en %
df_pdl_filtre['REP_MAISON_22'] = round((df_pdl_filtre['P22_MAISON'] / (df_pdl_filtre['P22_APPART'] + df_pdl_filtre['P22_MAISON'])),1)
df_pdl_filtre['REP_APPART_22'] = round((df_pdl_filtre['P22_APPART'] / (df_pdl_filtre['P22_APPART'] + df_pdl_filtre['P22_MAISON'])),1)

# Pour l'incice de tension
df_pdl_filtre["TX_EMP_22"] = (df_pdl_filtre["P22_ACTOCC1564"] / (df_pdl_filtre["P22_ACT1564"] + df_pdl_filtre["P22_INACT1564"])).round(3)

df_pdl_filtre["CROI_POP_16_22"] = ((df_pdl_filtre["P22_POP"] / df_pdl_filtre["P16_POP"] - 1) * 100).round(2)

df_pdl_filtre["TX_OCCUP_22"] = (1 - (df_pdl_filtre["P22_LOGVAC"] / df_pdl_filtre["P22_LOG"])).round(3)

df_pdl_filtre["LOG_MEN_22"] = (df_pdl_filtre["P22_MEN"] / df_pdl_filtre["P22_LOG"]).round(3)

df_pdl_filtre["PART_1529"] = (df_pdl_filtre["P22_POP1529"] / df_pdl_filtre["P22_POP"]).round(3)

df_pdl_filtre["PART_RES_SECOND"] = (df_pdl_filtre["P22_RSECOCC"] / df_pdl_filtre["P22_LOG"]).round(3)

df_pdl_filtre["PART_HLM"] = (df_pdl_filtre["P22_RP_LOCHLMV"] / df_pdl_filtre["P22_RP"]).round(3)

df_pdl_filtre["DENS_POP_22"] = (df_pdl_filtre["P22_POP"] / df_pdl_filtre["SUPERF"]).round(2)

# Conservation des colonnes qui nous intéressent
df_pdl_filtre_calculs = df_pdl_filtre.loc[:,['CODE_INSEE',
                                            'DEP',
                                            'P22_POP',
                                            'P16_POP',
                                            'SUPERF',
                                            'DENS_LOG_22',
                                            'REP_MAISON_22',
                                            'REP_APPART_22',
                                            'NB_COM_22',
                                            'TX_EMP_22',
                                            'CROI_POP_16_22',
                                            'TX_OCCUP_22',
                                            'LOG_MEN_22',
                                            'PART_1529',
                                            'PART_RES_SECOND',
                                            'PART_HLM',
                                            'DENS_POP_22'
                                            ]]

# Copie pour éviter d'écraser le df original
df_norm = df_pdl_filtre_calculs

# Colonnes à normaliser
indicateurs = [
    "TX_EMP_22","CROI_POP_16_22","TX_OCCUP_22","LOG_MEN_22","PART_RES_SECOND","DENS_POP_22"
]

# Normalisation min-max
scaler = MinMaxScaler()
df_norm_values = scaler.fit_transform(df_norm[indicateurs])

# Ajout des colonnes normalisées avec suffixe _n
for i, col in enumerate(indicateurs):
    df_norm[col + "_n"] = df_norm_values[:, i]
    
    
# Définir les poids pour chaque indicateur normalisé (en fonction de la matrice de corrélation)
poids = {
    "TX_EMP_22_n": 0.25,         # solvabilité -- proportion de la population 15–64 ans en emploi, mesure la solvabilité des habitants.
    "CROI_POP_16_22_n": 0.20,    # demande -- évolution de la population entre 2016 et 2022, reflète la dynamique démographique.
    "TX_OCCUP_22_n": 0.25,       # occupation -- part de logements occupés (inverse de la vacance), indique la pression sur le parc existant.
    "LOG_MEN_22_n": 0.20,        # ménages/logements -- ratio ménages/logements, mesure l’équilibre offre/demande en logement.
    "PART_RES_SECOND_n": 0.10,   # pression touristique -- part de résidences secondaires, traduit la pression touristique ou spéculative.
}

# Normalisation logarithmique de la population
max_pop = df_norm["P22_POP"].max()
df_norm["POP_LOG_norm"] = np.log1p(df_norm["P22_POP"]) / np.log1p(max_pop)

# Calcul pondéré de l’indice
df_norm["INDICE_TENSION_LOG"] = (sum(df_norm[col] * poids[col] for col in poids) * df_norm["POP_LOG_norm"]).round(3)

# Calcul pondéré de l’indice
df_norm["INDICE_TENSION"] = (sum(df_norm[col] * poids[col] for col in poids)).round(3)

# Fonction de catégorisation
def categoriser_tension(x):
    if x <= 0.20:
        return "Très détendu"
    elif x <= 0.40:
        return "Détendu"
    elif x <= 0.60:
        return "Intermédiaire"
    elif x <= 0.80:
        return "Tendu"
    else:
        return "Très tendu"

# Application au DataFrame
df_norm["CATEG_TENSION"] = df_norm["INDICE_TENSION"].apply(categoriser_tension)

# --- 1. Sélectionner les 10 plus grandes villes ---
top10_villes = df_norm.nlargest(10, "P22_POP")

# Mapping Code INSEE -> Nom de la commune
map_villes = {
    "44109": "Nantes",
    "49007": "Angers",
    "72181": "Le Mans",
    "44184": "Saint-Nazaire",
    "85191": "La Roche-sur-Yon",
    "49099": "Cholet",
    "44162": "Rezé",
    "53130": "Laval",
    "85194": "Les Sables-d’Olonne",
    "44143": "Saint-Herblain"
}

# Ajouter une colonne NOM_COMMUNE
top10_villes["CODE_INSEE"] = top10_villes["CODE_INSEE"].astype(str).str.zfill(5)
top10_villes["NOM_COMMUNE"] = top10_villes["CODE_INSEE"].map(map_villes)

df_norm.to_csv('df_norm.csv')