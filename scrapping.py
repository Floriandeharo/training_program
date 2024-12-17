import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://www.fitmetrics.ch"

def get_soup(url):
    """Récupère et parse le contenu HTML d'une URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Erreur lors du chargement de la page : {url}")
        return None

def get_muscles_links():
    """Récupère tous les liens vers les muscles."""
    url = f"{BASE_URL}/fr/exercices/muscles"
    soup = get_soup(url)
    if not soup:
        return []

    muscle_links = []
    for link in soup.find_all('a', href=True):
        if '/fr/exercices/muscle/' in link['href']:
            muscle_links.append(BASE_URL + link['href'])
    
    return muscle_links

def get_exercises_from_muscle_page(muscle_url):
    """Récupère tous les exercices associés à un muscle."""
    soup = get_soup(muscle_url)
    if not soup:
        return []

    exercises = []
    for link in soup.find_all('a', href=True, class_="group"):
        if '/fr/exercice/' in link['href']:
            exercise_url = BASE_URL + link['href']
            exercises.append(exercise_url)
    
    return exercises

def scrape_exercise_details(exercise_url):
    """Scrape le titre, description et les détails du tableau pour un exercice."""
    soup = get_soup(exercise_url)
    if not soup:
        return None

    # Récupérer le titre
    title_tag = soup.find('h1', class_="reveal")
    title = title_tag.text.strip() if title_tag else "N/A"

    # Récupérer les données du tableau
    details = {"title": title}
    table = soup.find('table', class_="animate-fadeIn")
    if table:
        rows = table.find_all('tr')
        for row in rows:
            # Extraire la clé et la valeur de chaque ligne
            key = row.find('td', class_="pr-2").text.strip() if row.find('td', class_="pr-2") else "N/A"
            value_td = row.find('td', class_=lambda x: x and 'flex' in x or x is None)
            if value_td:
                # Traiter les valeurs multiples (liens ou spans)
                values = [
                    val.text.strip() for val in value_td.find_all(['a', 'span'])
                ]
                details[key] = ", ".join(values)

    # Récupérer la description de l'exercice
    description_div = soup.find('div', class_="wysiwyg-content")
    description = description_div.get_text(separator="\n").strip() if description_div else "N/A"
    details["Description"] = description

    return details

def save_to_csv(data, filename="exercises.csv"):
    """Sauvegarde les données dans un fichier CSV."""
    if not data:
        print("Aucune donnée à sauvegarder.")
        return

    # Déterminer les colonnes à partir des clés
    fieldnames = ["title", "Difficulté", "Focus", "Équipements", "Sports", "Catégories", "Description"]
    
    with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore', delimiter=';')
        writer.writeheader()
        writer.writerows(data)
    print(f"Les données ont été sauvegardées dans {filename}")

def main():
    # Étape 1 : Récupérer tous les muscles
    muscle_links = get_muscles_links()
    print(f"Trouvé {len(muscle_links)} muscles.")

    # Étape 2 : Pour chaque muscle, récupérer les exercices
    all_exercises = []
    for muscle_link in muscle_links:
        print(f"Traitement de la page muscle : {muscle_link}")
        exercise_links = get_exercises_from_muscle_page(muscle_link)
        print(f"  -> {len(exercise_links)} exercices trouvés.")
        all_exercises.extend(exercise_links)

    # Étape 3 : Collecter les détails de chaque exercice
    exercises_details = []
    for index, exercise_link in enumerate(all_exercises):
        print(f"({index + 1}/{len(all_exercises)}) Récupération des détails de : {exercise_link}")
        details = scrape_exercise_details(exercise_link)
        if details:
            exercises_details.append(details)

    # Étape 4 : Sauvegarder les résultats dans un CSV
    save_to_csv(exercises_details)

if __name__ == "__main__":
    main()
