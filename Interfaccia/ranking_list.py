import csv

def read_scores():
    scores = []
    with open("./Progettazione/scores.csv", "r", newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                scores.append({"username": row[0], "punteggio": int(row[1])})
    return scores

def write_scores(scores):
    with open("./Progettazione/scores.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for entry in scores:
            writer.writerow([entry["username"], entry["punteggio"]])



updated_score = read_scores()
updated_score.append({"username": "Nuovo Giocatore", "punteggio": 100})  # Example of adding a new score
updated_score.sort(key=lambda x: x["punteggio"], reverse=True)
write_scores(updated_score)
