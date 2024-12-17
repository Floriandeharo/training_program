import pandas as pd

# Charger le fichier CSV avec gestion du BOM
file_path = 'exercises.csv'

try:
    # Lire avec UTF-8-SIG pour enlever le BOM automatiquement
    df = pd.read_csv(file_path, delimiter=';', encoding='utf-8-sig')
except UnicodeDecodeError:
    # Si UTF-8 échoue, utiliser ISO-8859-1
    df = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')

# Renommer proprement les colonnes pour corriger les caractères
df.columns = df.columns.str.strip()  # Enlever les espaces
df.columns = df.columns.str.replace('Ã©', 'é')  # Remplacer caractères erronés
df.columns = df.columns.str.replace('Ã', 'à')  # Corriger les "à"
df.columns = df.columns.str.replace('Ã©quipements', 'Équipements')  # Corriger équipement manuellement

# Afficher les colonnes après nettoyage
print("Colonnes nettoyées :", df.columns)

# Nettoyage des doublons
df_cleaned = df.drop_duplicates(subset=['title']).copy()

# Remplacer les valeurs manquantes dans 'Équipements' par 'Sans matériels'
df_cleaned['Équipements'] = df_cleaned['Équipements'].fillna('Sans matériels')
df_cleaned.fillna("Non spécifié", inplace=True)  # Remplace NaN par "Non spécifié"

# Enregistrer le fichier nettoyé
cleaned_file_path = 'exercises_cleaned.csv'
df_cleaned.to_csv(cleaned_file_path, index=False, sep=';', encoding='utf-8-sig')

print(f"Fichier nettoyé enregistré sous : {cleaned_file_path}")
