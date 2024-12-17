README.md
### Projet : Générateur de Programmes d'Entraînement
Ce projet permet de scraper des exercices d'entraînement, de nettoyer les données, de les stocker dans une base de données MySQL, puis de proposer une API pour générer des programmes d'entraînement personnalisés en fonction des préférences utilisateur.

### Pré-requis
Avant de commencer, assurez-vous d'avoir installé :

Python (version 3.8 ou supérieure)
MySQL installé et configuré
Dépendances Python :


# pip install requests bs4 pandas mysql-connector-python flask
Étapes pour Exécuter le Projet
## 1. Scraper les Données
Le script scrapping.py récupère les données d'exercices depuis un site web et les sauvegarde dans un fichier CSV.

Commandes :



# python scrapping.py
Sortie :

Le fichier fitmetrics_exercises.csv sera généré avec les données scrappées.
## 2. Nettoyer les Données
Le script cleaned_scrap.py nettoie le fichier CSV généré précédemment en supprimant les doublons et en traitant les valeurs manquantes.

Commandes :



# python cleaned_scrap.py
Sortie :

Le fichier fitmetrics_exercises_cleaned.csv sera généré.
## 3. Créer la Base de Données et Importer les Données
Le script connexiontest.py crée la base de données MySQL et les tables nécessaires, puis insère les données nettoyées dans les tables.

Commandes :



# python connexiontest.py
Configuration :

Assurez-vous que MySQL est en marche.
Modifiez les paramètres de connexion dans connexiontest.py si nécessaire :
python

host="localhost",
user="root",
password="",
database="sportia"
Sortie :

Base de données sportia avec les tables remplies.
## 4. Lancer l'API Flask
Le script app.py démarre une API Flask pour générer des programmes d'entraînement.

Commandes :



# python app.py
Sortie :

L'API est accessible à l'adresse : http://127.0.0.1:5000/generate
Utiliser l'API
Méthode : POST
URL :
arduino

http://127.0.0.1:5000/generate
Exemple de Requête JSON :
json

{
    "preferences": {
        "difficulty": "Débutant",
        "equipment": "Poulie",
        "categories": "Haut du corps"
    },
    "days_per_week": 3
}
Exemple de Réponse JSON :
json

{
    "success": true,
    "program": {
        "Jour 1": [1, 2, 3, 4, 5],
        "Jour 2": [6, 7, 8, 9, 10],
        "Jour 3": [11, 12, 13, 14, 15]
    }
}
Ordre d'Exécution des Scripts
Scraping des données :



# python scrapping.py
Nettoyage des données :



# python cleaned_scrap.py
Création de la base de données et insertion :



# python connexiontest.py
Lancement de l'API :



# python app.py
Problèmes Courants
## 1. Erreur de connexion à MySQL
Assurez-vous que le serveur MySQL est démarré.
Vérifiez les paramètres de connexion dans connexiontest.py et app.py.
## 2. Dépendances manquantes
Installez les dépendances manquantes avec :


# pip install requests bs4 pandas mysql-connector-python flask

## 3. Port de l'API déjà utilisé
Changez le port dans app.py :
python

app.run(debug=True, port=5001)
Conclusion
Ce projet vous permet de générer des programmes d'entraînement personnalisés en fonction des préférences utilisateur. Pour toute amélioration ou problème, n'hésitez pas à ouvrir une issue ou à poser vos questions.

