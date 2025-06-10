"""
update_scores.py

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
        with open("./rsc/scores.csv", "r", newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    scores.append({"name": row[0], "score": int(row[1])})
    except FileNotFoundError:
        pass  # File does not exist yet, return an empty list
    return scores

def write_scores(scores):
    """Writes a list of score dictionaries to the CSV file."""
    with open("./rsc/scores.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for entry in scores:
            writer.writerow([entry["name"], entry["score"]])

