# Documentazione del Progetto

## Schermata Login

### 🖼️ **Elemento 1: immagine_robot**
| Campo                 | Descrizione                                      |
|-----------------------|--------------------------------------------------|
| **Nome elemento**     | `robot_img`                                      |
| **Tipo di variabile** | Immagine                                         |
| **Formato**           | `.png`                                           |
| **Contenuto**         | Immagine di sfondo del Robot                     |
| **Team di riferimento** | Progettazione                                  |
| **Percorso/Link**     | `../Progettazione/robot.png`                     |
| **Note**              |                                                  |

---

## Schermata Storyline

### 🖼️ **Elemento 1: immagine_robot**
| Campo                 | Descrizione                                      |
|-----------------------|--------------------------------------------------|
| **Nome elemento**     | `robot_img`                                      |
| **Tipo di variabile** | Immagine                                         |
| **Formato**           | `.png`                                           |
| **Contenuto**         | Immagine di sfondo del Robot                     |
| **Team di riferimento** | Progettazione                                  |
| **Percorso/Link**     | `../Progettazione/robot.png`                     |
| **Note**              |                                                  |

### 📜 **Elemento 2: storia_storyline**
| Campo                 | Descrizione                                      |
|-----------------------|--------------------------------------------------|
| **Nome elemento**     | `content`                                        |
| **Tipo di variabile** | File testuale                                    |
| **Formato**           | `.csv`                                           |
| **Contenuto**         | Testo narrativo della storia                     |
| **Team di riferimento** | Progettazione                                  |
| **Percorso/Link**     | (Progettazione deve ancora crearlo in csv)       |
| **Note**              |                                                  |

---

## Schermata Tutorial_Chat

### 🖼️ **Elemento 1: immagine_robot**
| Campo                 | Descrizione                                      |
|-----------------------|--------------------------------------------------|
| **Nome elemento**     | `robot_chat_img`                                 |
| **Tipo di variabile** | Immagine                                         |
| **Formato**           | `.png`                                           |
| **Contenuto**         | Immagine di sfondo della schermata tutorial chat |
| **Team di riferimento** | Progettazione                                  |
| **Percorso/Link**     | `../Progettazione/Robot_Chat_.png`               |
| **Note**              | Immagine del robot leggermente ruotata           |

### ✅ **Elemento 2: risposta_check_bot**
| Campo                 | Descrizione                                      |
|-----------------------|--------------------------------------------------|
| **Nome elemento**     | `risposta_check_bot`                             |
| **Tipo di variabile** | Booleano                                         |
| **Formato**           | `True` / `False`                                 |
| **Contenuto**         | Esito del controllo risposta del bot             |
| **Team di riferimento** | LLM                                            |
| **Percorso/Link**     |                                                  |
| **Note**              |                                                  |

---

## Schermata Recap

### 🖼️ **Elemento 1: immagine_robot**
| Campo                 | Descrizione                                      |
|-----------------------|--------------------------------------------------|
| **Nome elemento**     | `robot_img`                                      |
| **Tipo di variabile** | Immagine                                         |
| **Formato**           | `.png`                                           |
| **Contenuto**         | Immagine di sfondo della schermata recap         |
| **Team di riferimento** | Progettazione                                  |
| **Percorso/Link**     | `../Progettazione/robot.png`                     |
| **Note**              |                                                  |

### 📝 **Elemento 2: prompt_riassuntivo**
| Campo                 | Descrizione                                      |
|-----------------------|--------------------------------------------------|
| **Nome elemento**     |                                                  |
| **Tipo di variabile** | File testuale                                    |
| **Formato**           | `.csv`                                           |
| **Contenuto**         | Prompt completo riassuntivo del tutorial         |
| **Team di riferimento** | Progettazione                                  |
| **Percorso/Link**     |                                                  |
| **Note**              |                                                  |

---

## Schermata Final_Challenge

### 🖼️ **Elemento 1: immagine_robot**
| Campo                 | Descrizione                                      |
|-----------------------|--------------------------------------------------|
| **Nome elemento**     | `robot_img`                                      |
| **Tipo di variabile** | Immagine                                         |
| **Formato**           | `.png`                                           |
| **Contenuto**         | Immagine di sfondo della schermata final challenge|
| **Team di riferimento** | Progettazione                                  |
| **Percorso/Link**     | `../Progettazione/robot.png`                     |
| **Note**              |                                                  |

### 📜 **Elemento 2: storia_final_challenge**
| Campo                 | Descrizione                                      |
|-----------------------|--------------------------------------------------|
| **Nome elemento**     | `storia_final_challenge`                         |
| **Tipo di variabile** | File testuale                                    |
| **Formato**           | `.csv`                                           |
| **Contenuto**         | Nuova storia per la challenge finale             |
| **Team di riferimento** | Progettazione                                  |
| **Percorso/Link**     | `./Progettazione/final_challenge.csv`            |
| **Note**              |                                                  |

### 💬 **Elemento 3: risposta_bot_final_challenge**
| Campo                 | Descrizione                                      |
|-----------------------|--------------------------------------------------|
| **Nome elemento**     |                                                  |
| **Tipo di variabile** | Stringa o file testuale                          |
| **Formato**           |                                                  |
| **Contenuto**         | Risposta generata dal bot                        |
| **Team di riferimento** | LLM                                            |
| **Percorso/Link**     |                                                  |
| **Note**              |                                                  |

---

## Schermata Scores

### 🖼️ **Elemento 1: immagine_robot**
| Campo                 | Descrizione                                      |
|-----------------------|--------------------------------------------------|
| **Nome elemento**     | `robot_img`                                      |
| **Tipo di variabile** | Immagine                                         |
| **Formato**           | `.png`                                           |
| **Contenuto**         | Immagine di sfondo della schermata punteggi      |
| **Team di riferimento** | Progettazione                                  |
| **Percorso/Link**     | `../Progettazione/robot.png`                     |
| **Note**              |                                                  |

### 🏆 **Elemento 2: lista_punteggi**
| Campo                 | Descrizione                                      |
|-----------------------|--------------------------------------------------|
| **Nome elemento**     |                                                  |
| **Tipo di variabile** | Lista di stringhe                                |
| **Formato**           | `.csv`                                           |
| **Contenuto**         | Lista dei punteggi salvati                       |
| **Team di riferimento** | Progettazione                                  |
| **Percorso/Link**     | `../Progettazione/scores.csv`                    |
| **Note**              |                                                  |

### 🤖 **Elemento 3: punteggio_llm**
| Campo                 | Descrizione                                      |
|-----------------------|--------------------------------------------------|
| **Nome elemento**     |                                                  |
| **Tipo di variabile** | Numero intero                                    |
| **Formato**           |                                                  |
| **Contenuto**         | Punteggio assegnato dalla sezione LLM            |
| **Team di riferimento** | LLM                                            |
| **Percorso/Link**     |                                                  |
| **Note**              | Valore calcolato restituito dal modello LLM      |
