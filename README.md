# Comment ça marche ?

Notre produit permet d’analyser et de visualiser des données immobilières de manière simple et interactive grâce à une interface web conviviale.  

Il aide à affiner votre analyse de marché pour un projet immobilier potentiel.

## Installation

### 1. Installation de Python
Installez Python depuis le site officiel : [Python.org](https://www.python.org/downloads/)

### 2. Installation des dépendances
Ouvrez votre terminal et installez les dépendances nécessaires :  

```bash
pip install gdown scikit-learn selenium selenium-stealth beautifulsoup4 pandas
```

# Utilisation

1. **Cloner le repository**  
   Clonez le projet sur votre PC en local en utilisant VSCode, et il faut également l’héberger sur votre propre repository GitHub.

2. **Lancer le script "meilleur agent"**  
   Exécutez le script `run_meilleur_agent.py` et laissez-le tourner jusqu'à la fin.  
   ⚠️ Ne bougez pas la souris pendant son exécution, sauf pour valider le captcha si demandé.

3. **Récupérer les autres données et effectuer les calculs**  
   Allez sur **GitHub Actions** et lancez le workflow `run_script`.  
   Cela permettra de récupérer toutes les données restantes et de réaliser tous les calculs nécessaires pour obtenir les fichiers finaux.

4. **Mettre à jour l’application Streamlit**  
   Lancez ensuite le script `run_script_streamlit.py` pour mettre à jour le dossier Streamlit avec les nouvelles données.

5. **Étude de marché**  
   Enfin, ouvrez le lien de l’application Streamlit et utilisez l’interface pour réaliser votre étude de marché pour votre projet.


# Liens

[Présentation du projet](https://www.canva.com/design/DAGxz5uTLsU/yF08Sh8I61jE7CnCyM3XDQ/edit?utm_content=DAGxz5uTLsU&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

[Streamlit Cloud](https://projet-immo.streamlit.app/)