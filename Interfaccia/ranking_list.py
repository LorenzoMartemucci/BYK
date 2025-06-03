import csv

def read_scores():
    scores = []
    try:
        with open("./Progettazione/scores.csv", "r", newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    scores.append({"username": row[0], "punteggio": int(row[1])})
    except FileNotFoundError:
        pass  # Il file non esiste ancora, restituisci lista vuota
    return scores

def write_scores(scores):
    with open("./Progettazione/scores.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for entry in scores:
            writer.writerow([entry["username"], entry["punteggio"]])



updated_score = read_scores()
print("Classifica :", updated_score)
new_user= "Nuovo Giocatore"
new_score= 20
if new_user.lower() in [entry["username"].lower() for entry in updated_score]:
    print(f"L'utente '{new_user}' e' gia' presente nella classifica. Inserisci un nome diverso.")
else: 
    updated_score.append({"username": new_user, "punteggio": new_score})  # Example of adding a new score
    updated_score.sort(key=lambda x: x["punteggio"], reverse=True)
    write_scores(updated_score)
