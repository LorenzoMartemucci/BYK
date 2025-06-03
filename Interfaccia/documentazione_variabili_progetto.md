# Documentazione del Progetto

---

## Finestra Login

### 🤖 **Elemento 1: immagine robot**
| Campo                      | Descrizione                  |
|----------------------------|------------------------------|
| **Nome elemento**          | `robot.png`                  |
| **Nome variabile nel codice** | `robot_img`               |
| **Tipo di variabile**      | Immagine                     |
| **Formato**                | `.png`                       |
| **Contenuto**              | Immagine del Robot           |
| **Team sorgente**          | Progettazione                |
| **Team di applicazione**   | Interfaccia                  |
| **Percorso/Link**          | `../Progettazione/robot.png` |

---

## Finestra Storyline

### 🤖 **Elemento 1: immagine robot**
| Campo                      | Descrizione                  |
|----------------------------|------------------------------|
| **Nome elemento**          | `robot.png`                  |
| **Nome variabile nel codice** | `robot_img`               |
| **Tipo di variabile**      | Immagine                     |
| **Formato**                | `.png`                       |
| **Contenuto**              | Immagine del Robot           |
| **Team sorgente**          | Progettazione                |
| **Team di applicazione**   | Interfaccia                  |
| **Percorso/Link**          | `../Progettazione/robot.png` |

### 📜 **Elemento 2: storia**
| Campo                      | Descrizione                          |
|----------------------------|--------------------------------------|
| **Nome elemento**          | `storia.txt`                         |
| **Nome variabile nel codice** | `content`                         |
| **Tipo di variabile**      | File testuale                        |
| **Formato**                | `.txt`                               |
| **Contenuto**              | Testo narrativo della storia di Robbi|
| **Team sorgente**          | Progettazione                        |
| **Team di applicazione**   | Interfaccia                          |
| **Percorso/Link**          | `../Progettazione/storia.txt`        |

---

## Finestra Tutorial Chat

### 🤖 **Elemento 1: immagine robot**
| Campo                      | Descrizione                  |
|----------------------------|------------------------------|
| **Nome elemento**          | `Robot_Chat.png`             |
| **Nome variabile nel codice** | `robot_img`               |
| **Tipo di variabile**      | Immagine                     |
| **Formato**                | `.png`                       |
| **Contenuto**              | Immagine del Robot           |
| **Team sorgente**          | Progettazione                |
| **Team di applicazione**   | Interfaccia                  |
| **Percorso/Link**          | `../Progettazione/Robot_Chat_.png` |
| **Note**                   | Immagine del Robot leggermente ruotata |

### 💬 **Elemento 2: prompt utente tutorial**
| Campo                      | Descrizione                          |
|----------------------------|--------------------------------------|
| **Nome variabile nel codice** | `last_user_message`               |
| **Tipo di variabile**      | Stringa                              |
| **Contenuto**              | prompt inserito dall'utente ad ogni richiesta del bot |
| **Team sorgente**          | Interfaccia                          |
| **Team di applicazione**   | LLM                                  |
| **Note**                   | Da passare al team LLM per il controllo sul prompt|

### 📝 **Elemento 3: richieste bot**
| Campo                      | Descrizione                          |
|----------------------------|--------------------------------------|
| **Nome elemento**          | `Episodi_Robbi.csv`                  |
| **Tipo di variabile**      | File testuale                        |
| **Formato**                | `.csv`                               |
| **Contenuto**              | Lista di richieste del bot divise per compito, contesto, formato output, vincoli e challenge finale. |
| **Team sorgente**          | Progettazione                        |
| **Team di applicazione**   | Interfaccia                          |
| **Percorso/Link**          | `../Progettazione/Episodi_Robbi.csv` |
| **Note**                   | file contenente tutte le richieste del bot usato in Tutorial Chat e Final Challenge. Struttura: Ruolo,Episodio,Domanda,Obiettivo. N.B.: l'episodio relativo al ruolo non rientra in quanto la prima domanda è standard. |

### ✅ **Elemento 4: check sul prompt utente**
| Campo                      | Descrizione                          |
|----------------------------|--------------------------------------|
| **Tipo di variabile**      | Booleano                             |
| **Contenuto**              | `True` / `False`                     |
| **Team sorgente**          | LLM                                  |
| **Team di applicazione**   | Interfaccia                          |
| **Note**                   | Esito del controllo sulla correttezza del prompt inserito dall'utente |

### 💬 **Elemento 5: Risposta AI**
| Campo                      | Descrizione                          |
|----------------------------|--------------------------------------|
| **Tipo di variabile**      | Stringa                              |
| **Contenuto**              | Risposta del bot in base al check del prompt utente |
| **Team sorgente**          | LLM                                  |
| **Team di applicazione**   | Interfaccia                          |

---

## Finestra Recap

### 🤖 **Elemento 1: immagine robot**
| Campo                      | Descrizione                  |
|----------------------------|------------------------------|
| **Nome elemento**          | `robot.png`                  |
| **Nome variabile nel codice** | `robot_img`               |
| **Tipo di variabile**      | Immagine                     |
| **Formato**                | `.png`                       |
| **Contenuto**              | Immagine del Robot           |
| **Team sorgente**          | Progettazione                |
| **Team di applicazione**   | Interfaccia                  |
| **Percorso/Link**          | `../Progettazione/robot.png` |

### 📝 **Elemento 2: key word del prompt riassuntivo**
| Campo                      | Descrizione                          |
|----------------------------|--------------------------------------|
| **Tipo di variabile**      | Stringa                              |
| **Contenuto**              | key word estratta per ogni punto del prompt |
| **Team sorgente**          | LLM                                  |
| **Team di applicazione**   | Interfaccia                          |
| **Note**                   | Stringa estratta dall'LLM dal prompt inserito nel tutorial dall'utente |

---

## Finestra Final Challenge

### 🤖 **Elemento 1: immagine robot**
| Campo                      | Descrizione                  |
|----------------------------|------------------------------|
| **Nome elemento**          | `Robot_Chat.png`             |
| **Nome variabile nel codice** | `robot_img`               |
| **Tipo di variabile**      | Immagine                     |
| **Formato**                | `.png`                       |
| **Contenuto**              | Immagine del Robot           |
| **Team sorgente**          | Progettazione                |
| **Team di applicazione**   | Interfaccia                  |
| **Percorso/Link**          | `../Progettazione/Robot_Chat_.png` |
| **Note**                   | Immagine del Robot leggermente ruotata |

### 📝 **Elemento 2: richieste bot**
| Campo                      | Descrizione                          |
|----------------------------|--------------------------------------|
| **Nome elemento**          | `Episodi_Robbi.csv`                  |
| **Tipo di variabile**      | File testuale                        |
| **Formato**                | `.csv`                               |
| **Contenuto**              | Richieste del bot (compito, contesto, formato output, vincoli e challenge finale.) |
| **Team sorgente**          | Progettazione                        |
| **Team di applicazione**   | Interfaccia                          |
| **Percorso/Link**          | `../Progettazione/Episodi_Robbi.csv` |
| **Note**                   | file contenente tutte le richieste del bot usato in Tutorial Chat e Final Challenge. Struttura: Ruolo,Episodio,Domanda,Obiettivo. N.B.: l'episodio relativo al ruolo non rientra in quanto la prima domanda è standard. |

### 💬 **Elemento 3: prompt utente challenge**
| Campo                      | Descrizione                          |
|----------------------------|--------------------------------------|
| **Nome variabile nel codice** | `last_user_message`               |
| **Tipo di variabile**      | Stringa                              |
| **Contenuto**              | Prompt creato dall'utente nella challenge finale |
| **Team sorgente**          | Interfaccia                          |
| **Team di applicazione**   | LLM                                  |
| **Note**                   | Da passare al team LLM per il controllo sul prompt e per la generazione dell'output |

### 💬 **Elemento 4: risposta bot challenge finale**
| Campo                      | Descrizione                          |
|----------------------------|--------------------------------------|
| **Tipo di variabile**      | Stringa                              |
| **Contenuto**              | Risposta al prompt finale generata dal bot |
| **Team sorgente**          | LLM                                  |
| **Team di applicazione**   | Interfaccia                          |

---

## Finestra Scores

### 🤖 **Elemento 1: immagine robot**
| Campo                      | Descrizione                  |
|----------------------------|------------------------------|
| **Nome elemento**          | `robot.png`                  |
| **Nome variabile nel codice** | `robot_img`               |
| **Tipo di variabile**      | Immagine                     |
| **Formato**                | `.png`                       |
| **Contenuto**              | Immagine del Robot           |
| **Team sorgente**          | Progettazione                |
| **Team di applicazione**   | Interfaccia                  |
| **Percorso/Link**          | `../Progettazione/robot.png` |
| **Note**                   | finestra Punteggi            |

### 🏆 **Elemento 2: lista_punteggi**
| Campo                      | Descrizione                          |
|----------------------------|--------------------------------------|
| **Nome elemento**          | `scores.csv`                         |
| **Nome variabile nel codice** | `ranking_data`                    |
| **Tipo di variabile**      | File testuale                        |
| **Formato**                | `.csv`                               |
| **Contenuto**              | Lista degli user e dei punteggi salvati |
| **Team sorgente**          | Progettazione                        |
| **Team di applicazione**   | Interfaccia                          |
| **Percorso/Link**          | `../Progettazione/scores.csv`        |
| **Note**                   | File csv della Classifica, ovvero una lista di dizionari con nomi degli user e i loro punteggi |

### 🏆 **Elemento 3: punteggio_llm**
| Campo                      | Descrizione                          |
|----------------------------|--------------------------------------|
| **Nome variabile nel codice** | `score_value`                     |
| **Tipo di variabile**      | Intero                               |
| **Contenuto**              | Punteggio finale dell'utente corrente |
| **Team sorgente**          | LLM                                  |
| **Team di applicazione**   | Interfaccia                          |
| **Note**                   | valore calcolato dalla sezione LLM sul prompt della challenge |
