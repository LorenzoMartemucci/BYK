"""
update_scores.py

This module manages reading, updating, sorting, and saving user scores in a CSV file.
It provides a single function to update the ranking with a new entry and persist the changes.

Main Features:
- Reads scores from a CSV file into a list of dictionaries.
- Adds a new user score to the list.
- Sorts the list by score in descending order.
- Writes the updated and sorted list back to the CSV file.
- Returns the updated ranking list.
"""

import csv

def update_ranking_list(username, score_value, file_path="./rsc/scores.csv"):
    """
    Reads the current scores from a CSV file, adds a new user score,
    sorts the list in descending order by score, writes the updated list
    back to the CSV file, and returns the updated ranking list.

    Args:
        username (str): The name of the user to add to the ranking.
        score_value (int): The score value to add for the user.
        file_path (str, optional): The path to the CSV file. Defaults to './rsc/scores.csv'.

    Returns:
        list[dict]: The updated and sorted list of scores, each as a dictionary
                    with keys 'name' and 'score'.
    """
    if not isinstance(score_value, int):
        raise ValueError("score_value must be an integer")

    scores = []
    try:
        with open(file_path, "r", newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    scores.append({"name": row[0], "score": int(row[1])})
    except FileNotFoundError:
        # If the file does not exist, start with an empty list
        pass

    # Add the new user score
    scores.append({"name": username, "score": score_value})
    # Sort the list by score in descending order
    scores.sort(key=lambda x: x["score"], reverse=True)

    # Write the updated and sorted list back to the CSV file
    with open(file_path, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for entry in scores:
            writer.writerow([entry["name"], entry["score"]])

    return scores
