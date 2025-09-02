# Projet_immo

## pour utiliser les données 
il va falloir faire:

pip install gdown scikit-learn.......

pip install selenium selenium-stealth beautifulsoup4 pandas



V: automatisation:  github, github actions,  ipynb to py, csv to gsheet to looker avec python
Hébergement https://huggingface.co/spaces ou streamlit cloud 
1 Github Action pour run tous les GA
1 GA pour automatiser le looker

# liste de nos datasets

https://www.insee.fr/fr/statistiques/5359146
meilleurs-agents

# 5W+H

What → Dashboard interactif permettant de confronter un projet au marché et repérer des endroits intéressants.

Who → investisseur immo

When → mise à jour au dernier chargement des données de MA

Where → pays de la loire

Why → gain de temps sur la recherche de bien et l'analyse du marché

How → 
Sources principales: meilleurs-agents, dgfip, insee, 
Sources secondaires: selectra, comparatif de charges immo (assurance...), cabinet expertise comptable

Un dashboard interactif dédié aux investisseurs immobiliers, basé sur des données fiables (Meilleurs Agents, DVF, DGFiP, INSEE, Agences immobilières…), qui met à jour mensuellement l’analyse du marché des Pays de la Loire afin de repérer rapidement les zones attractives et gagner du temps dans la recherche et l’évaluation des biens.


# outils utilisés
duckdb
streamlit
python
github
google drive
trello
looker studio


# sources
cabinet expertise comptable

calcul TAEG
https://www.mozzeno.com/fr/blog/taeg/#methode-de-calcul-du-taeg

garantie loyers impayés
https://www.empruntis.com/financement/investissement-locatif/gli-garantie-loyer-impaye.php#t_4

calcul taxe foncière
https://www.economie.gouv.fr/particuliers/impots-et-fiscalite/gerer-mes-impots-locaux/taxe-fonciere-mode-de-calcul-et-reductions#quel-est-le-montant-de-la-taxe-f_2

assurance PNO
https://selectra.info/assurance/assurance-habitation/proprietaire-non-occupant/prix

garantie loyers impayés
https://www.empruntis.com/financement/investissement-locatif/gli-garantie-loyer-impaye.php#t_4

calcul taxe foncière
https://www.economie.gouv.fr/particuliers/impots-et-fiscalite/gerer-mes-impots-locaux/taxe-fonciere-mode-de-calcul-et-reductions#quel-est-le-montant-de-la-taxe-f_2

source: selectra
https://selectra.info/assurance/assurance-habitation/proprietaire-non-occupant/prix

calcul de la valeur cadastrale
https://www.nexity.fr/guide-immobilier/conseils-investissement/investissement-locatif/calcul-valeur-locative-cadastrale

prix assurance habitation
https://www.lesfurets.com/assurance-habitation/contrat/prix

frais de gestion locative
https://www.manda.fr/ressources/articles/frais-de-gestion-locative#comment-sont-calcul%C3%A9s-les-frais-de-gestion-locative--

# Jour 1 :
## établissement du plan de travail

# J1:
scraping: Création du script meilleur_agentv3 pour pouvoir scraper toutes les villes de pays de la loire sur le site MA

Creation github, 
drive, 
pages d’infos… 
(le template);
+
création de get fiscality
création de credit rate 

scraping:

Objectifs
Avoir un template 

# J2:
## Scraping 
Scraping :finalisation du web scraping

test de visualisation streamlit

Comparaison dataset datagouv.fr et meilleurs-agents pour choix final;
+
Test de visualisation sur looker studio

Maquette Canva

## ojbectif:
Scraper meilleur agent

maquette


# J3:
Création / développement du streamlit

Contrôle, clean data MA 
+
Création des colonnes calculées
+
Visualisation avec paramètres finaux sur looker 
Contrôle data DVF
+
Définir charges (niveau France)
+
Passage sur les calculs une fois looker terminé

obj:
Choisir outils de visualisation

Définir charges

Création des colonnes calculées
# J4:
Création / développement du streamlit
Contrôle, clean data MA 
+
Création des colonnes calculées
+
Visualisation avec paramètres finaux sur looker 
Contrôle data DVF
+
Définir charges (niveau France)
+
Passage sur les calculs une fois looker terminé
Création outils visualisation


# J5: colonnes calculées + calculs variables sur streamlit

Création outils visualisation
# J6:



Création outils visualisation
# J7:



Création outils visualisation

Remplir le readme du github

Axes d’améliorations
# J8:
Vulgarisation projet / préparation présentation

# J9:
préparation présentation


# J10:
présentation
