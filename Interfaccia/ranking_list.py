"""
ranking_list.py

This module handles reading from and writing to a CSV file that stores user scores.
It provides functions to load current rankings and update them by adding new entries.

Main Features:
- Reads scores from a CSV file into a list of dictionaries.
- Writes a list of user scores back to the CSV file.
- Ensures new usernames are unique before adding a new score.
"""

import csv

def read_scores():
    """Reads the scores from a CSV file and returns a list of dictionaries."""
    scores = []
    try:
        with open("./Progettazione/scores.csv", "r", newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    scores.append({"username": row[0], "punteggio": int(row[1])})
    except FileNotFoundError:
        pass  # File does not exist yet, return an empty list
    return scores

def write_scores(scores):
    """Writes a list of score dictionaries to the CSV file."""
    with open("./Progettazione/scores.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for entry in scores:
            writer.writerow([entry["username"], entry["punteggio"]])

# Load existing scores
updated_score = read_scores()
print("Classifica :", updated_score)

# Add a new user score if not already present
new_user = "Nuovo Giocatore"
new_score = 20

if new_user.lower() in [entry["username"].lower() for entry in updated_score]:
    print(f"L'utente '{new_user}' e' gia' presente nella classifica. Inserisci un nome diverso.")
else:
    updated_score.append({"username": new_user, "punteggio": new_score})
    updated_score.sort(key=lambda x: x["punteggio"], reverse=True)  # Sort by score descending
    write_scores(updated_score)  # Save the updated ranking
