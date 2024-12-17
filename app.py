import mysql.connector
import random
from flask import Flask, request, jsonify
import itertools

# Connexion à la base de données MySQL
def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sportia"
    )
    return connection

# Récupérer les exercices en fonction des préférences utilisateur
def fetch_exercises(preferences):
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT e.id, e.title, e.description, d.level AS difficulte, eq.name AS equipment, c.name AS category
    FROM exercice e
    JOIN difficulte d ON e.difficulte_id = d.id
    LEFT JOIN exercice_equipements ee ON e.id = ee.exercice_id
    LEFT JOIN equipements eq ON ee.equipement_id = eq.id
    LEFT JOIN exercice_categories ec ON e.id = ec.exercice_id
    LEFT JOIN categories c ON ec.category_id = c.id
    WHERE d.level = %s
      AND (eq.name LIKE %s OR eq.name IS NULL)
      AND c.name LIKE %s
    """
    params = (
        preferences['difficulty'],
        f"%{preferences['equipment']}%",
        f"%{preferences['categories']}%"
    )
    cursor.execute(query, params)
    exercises = cursor.fetchall()

    connection.close()
    return exercises
import itertools

# Répartir les exercices sur plusieurs jours
def generate_program(preferences, days_per_week):
    exercises = fetch_exercises(preferences)

    if not exercises:
        return {"error": "Aucun exercice ne correspond à vos critères."}

    # Mélanger les exercices pour plus de variété
    random.shuffle(exercises)

    # Répartir les exercices en évitant les doublons dans une journée
    program = {}
    exercise_cycle = itertools.cycle(exercises)  # Boucle infinie sur les exercices
    total_exercises = len(exercises)

    for day in range(1, days_per_week + 1):
        used_in_day = set()  # Suivi des exercices utilisés pour ce jour
        day_exercises = []

        # Remplir avec le maximum possible d'exercices uniques
        for _ in range(min(5, total_exercises)):  # Pas plus de 5 par jour, mais limité au total restant
            exercise = next(exercise_cycle)
            if exercise['id'] not in used_in_day:
                day_exercises.append(exercise)
                used_in_day.add(exercise['id'])

        # Ajouter les IDs au programme
        program[f"Jour {day}"] = [exercise['id'] for exercise in day_exercises]

        # Si tous les exercices uniques ont été utilisés, réinitialiser
        if len(used_in_day) == total_exercises:
            used_in_day.clear()

    return program

# Application Flask
app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Récupérer les préférences utilisateur depuis la requête
        data = request.json
        preferences = data.get('preferences', {})
        days_per_week = data.get('days_per_week', 3)

        # Générer le programme
        program = generate_program(preferences, days_per_week)

        # Retourner le programme
        return jsonify({"success": True, "program": program})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
