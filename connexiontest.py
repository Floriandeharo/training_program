import mysql.connector
import pandas as pd

# Connexion à MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sportia"
)
cursor = connection.cursor()

# Charger le fichier CSV
file_path = 'exercises_cleaned.csv'
df = pd.read_csv(file_path, delimiter=';', encoding='utf-8-sig')

# Création des tables si elles n'existent pas déjà
cursor.execute("""
CREATE TABLE IF NOT EXISTS difficulte (
    id INT AUTO_INCREMENT PRIMARY KEY,
    level VARCHAR(255) UNIQUE
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS exercice (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    difficulte_id INT,
    FOREIGN KEY (difficulte_id) REFERENCES difficulte(id)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS equipements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS exercice_sports (
    exercice_id INT,
    sport_id INT,
    FOREIGN KEY (exercice_id) REFERENCES exercice(id),
    FOREIGN KEY (sport_id) REFERENCES sports(id),
    PRIMARY KEY (exercice_id, sport_id)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS exercice_categories (
    exercice_id INT,
    category_id INT,
    FOREIGN KEY (exercice_id) REFERENCES exercice(id),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    PRIMARY KEY (exercice_id, category_id)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS exercice_equipements (
    exercice_id INT,
    equipement_id INT,
    FOREIGN KEY (exercice_id) REFERENCES exercice(id),
    FOREIGN KEY (equipement_id) REFERENCES equipements(id),
    PRIMARY KEY (exercice_id, equipement_id)
)""")

# Fonction pour insérer des valeurs uniques et récupérer leur ID
def insert_unique_value(table_name, value):
    cursor.execute(f"INSERT IGNORE INTO {table_name} (name) VALUES (%s)", (value,))
    cursor.execute(f"SELECT id FROM {table_name} WHERE name = %s", (value,))
    return cursor.fetchone()[0]

# Insérer les niveaux de difficulté
difficulty_ids = {}
for difficulty in df['Difficulté'].unique():
    cursor.execute("INSERT IGNORE INTO difficulte (level) VALUES (%s)", (difficulty,))
    cursor.execute("SELECT id FROM difficulte WHERE level = %s", (difficulty,))
    difficulty_ids[difficulty] = cursor.fetchone()[0]

# Insérer les données dans les tables
for _, row in df.iterrows():
    # Associer la difficulté
    difficulte_id = difficulty_ids[row['Difficulté']]
    
    # Insérer dans la table exercice avec difficulte_id
    cursor.execute("INSERT INTO exercice (title, description, difficulte_id) VALUES (%s, %s, %s)", 
                   (row['title'], row['Description'], difficulte_id))
    exercice_id = cursor.lastrowid  # Récupérer l'ID de l'exercice inséré

    # Insérer dans la table sports et établir la relation
    sports_list = row['Sports'].split(", ")
    for sport in sports_list:
        sport_id = insert_unique_value("sports", sport)
        cursor.execute("INSERT IGNORE INTO exercice_sports (exercice_id, sport_id) VALUES (%s, %s)", 
                       (exercice_id, sport_id))

    # Insérer dans la table categories et établir la relation
    categories_list = row['Catégories'].split(", ")
    for category in categories_list:
        category_id = insert_unique_value("categories", category)
        cursor.execute("INSERT IGNORE INTO exercice_categories (exercice_id, category_id) VALUES (%s, %s)", 
                       (exercice_id, category_id))

    # Insérer dans la table equipements et établir la relation
    equipements_list = row['Équipements'].split(", ")
    for equipement in equipements_list:
        equipement_id = insert_unique_value("equipements", equipement)
        cursor.execute("INSERT IGNORE INTO exercice_equipements (exercice_id, equipement_id) VALUES (%s, %s)", 
                       (exercice_id, equipement_id))

# Valider les modifications
connection.commit()

# Fermer la connexion
cursor.close()
connection.close()

print("Les données ont été insérées avec succès.")
