import csv

def ranking_update(username, score):
    with open("./Progettazione/scores.csv", "a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([username, score])

ranking_update("user1", 100)
ranking_update("user2", 80)
