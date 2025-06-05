import csv

def read_scores():
    scores = []
    try:
        with open("./Progettazione/scores.csv", "r", newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    scores.append({"name": row[0], "score": int(row[1])})
    except FileNotFoundError:
        pass  # Il file non esiste ancora, restituisci lista vuota
    return scores

def write_scores(scores):
    with open("./Progettazione/scores.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for entry in scores:
            writer.writerow([entry["name"], entry["score"]])




# if new_user.lower() in [entry["name"].lower() for entry in updated_score]:
#     print(f"L'utente '{new_user}' e' gia' presente nella classifica. Inserisci un nome diverso.")

