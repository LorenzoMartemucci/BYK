"""
scoring_ranking.py

This module defines the ScoringRankingPage class, a custom Tkinter frame designed to display
user scores and a ranking leaderboard in a stylized card interface. It provides visual feedback
at the end of an activity or game, and includes the option to play again.

Main Features:
- Displays a congratulatory message with the user's score.
- Shows a scrollable, ranked leaderboard sorted by score.
- Renders a card layout with headers, robot avatar, and styled buttons.
- Integrates a 'Play Again' button for restarting the experience.
"""


import tkinter as tk
import customtkinter as ctk
from PIL import Image
from ranking_list import read_scores, write_scores # se avviata da main_interface from Interfaccia.ranking_list
import numpy as np

class ScoringRankingPage(ctk.CTkFrame):
    def __init__(self, master, person, score_value=None, on_play_again=None, *args, **kwargs):
        super().__init__(master, fg_color="#FFE2CC", *args, **kwargs)
        # Theme colors and fonts (match your main interface)
        self.widgets_bg = "#FFA764"
        self.widgets_fg_text_color = "#000000"
        self.widgets_border_color = "#BF5200"
        self.widgets_font = ("Comic Sans MS", 12)
        self.window_bg = "#FFE2CC"
        self.table_header_font = ("Comic Sans MS", 11)
        self.score_font = ("Comic Sans MS", 48, "bold")
        self.title_font = ("Comic Sans MS", 25, "bold")
        self.subtitle_font = ("Comic Sans MS", 22)
        self.button_font = ("Comic Sans MS", 13)
        self.title_xplacement = 190  # Adjusted for right alignment
        self.title_yplacement = 30  # Adjusted for top placement
        self.title_width = 280  # Width for the title label
        
        

        self.is_score_below_minimum = False

        self.score_value = score_value
        self.ranking_data = read_scores()   # Read existing scores

        # Validate the score_value
        if self.score_value is None:
            self.title_text = "ERRORE! Punteggio non fornito!"
        elif not isinstance(self.score_value, int):
            self.title_text = "ERRORE! Punteggio non intero!"
        elif self.score_value < 0 :
            self.title_font = ("Comic Sans MS", 20, "bold")
            self.title_text = "ERRORE! Il Punteggio deve essere positivo!"
        elif self.score_value > 100:
            self.title_font = ("Comic Sans MS", 20, "bold")
            self.title_text = "ERRORE! Il Punteggio deve essere minore o uguale a 100!"
        elif self.score_value < 60:
            self.is_score_below_minimum = True
            self.title_text = "Oh peccato, c'eri quasi! Prova di nuovo!"
        else:
            self.title_text = "Congratulazioni!"
            self.title_font = ("Comic Sans MS", 30, "bold")
            self.title_width = 200  # Width for the title label
            self.title_xplacement = 220  # Adjusted for right alignment
            self.title_yplacement = 60  # Adjusted for top placement
        # Update the ranking data
            self.new_user = "Giocatore"+str(len(self.ranking_data) + 1)  # Example new user
            self.ranking_data.append({"name": self.new_user, "score": self.score_value})  # Example of adding a new score
            self.ranking_data.sort(key=lambda x: x["score"], reverse=True)  # Sort by score descending
            write_scores(self.ranking_data) # Save updated ranking

        
        self.on_play_again = on_play_again

        # Card-like frame
        self.card_frame = ctk.CTkFrame(
            self,
            fg_color=self.widgets_bg,
            border_color=self.widgets_border_color,
            border_width=2,
            corner_radius=20,
            width=500,
            height=550
        )
        self.card_frame.place(relx=0.5, rely=0.45, anchor="center")

        # Robot image (top right, floating)
        image_sides_size = 175
        robot_img = Image.open("./Progettazione/robot.png").resize((image_sides_size, image_sides_size))
        robot_photo = ctk.CTkImage(light_image=robot_img, size=(image_sides_size, image_sides_size))
        robot_label = ctk.CTkLabel(self.card_frame, image=robot_photo, text="", fg_color="transparent")
        robot_label.place(x=25, y=20)

        # Top section: Title, Score (to the right of the robot, aligned right)
        title_label = ctk.CTkLabel(
            self.card_frame,
            text=self.title_text,
            font=self.title_font,
            text_color="#632B00",
            fg_color="transparent",
            anchor="e",
            width=self.title_width,
            wraplength=280
        )
        title_label.place(x=self.title_xplacement,y=self.title_yplacement)

        subtitle_label = ctk.CTkLabel(
            self.card_frame,
            text="Punteggio:",
            font=self.subtitle_font,
            text_color="#632B00",
            fg_color="transparent",
            anchor="e",
            width=150
        )
        subtitle_label.place(x=200, y=140)

        score_label = ctk.CTkLabel(
            self.card_frame,
            text=str(self.score_value),
            font=self.score_font,
            text_color="#112E4B",
            fg_color="transparent",
            anchor="e",
            width=50
        )
        score_label.place(x=360, y=120)

        # Table section
        table_y = 200
        table_height = 270
        table_width = 450
        table_x = 25

        table_frame = ctk.CTkFrame(self.card_frame, fg_color=self.widgets_bg, width=table_width, height=table_height)
        table_frame.place(x=table_x, y=table_y)

        # Table headers
        header_height = 30
        header_frame = ctk.CTkFrame(table_frame, fg_color=self.widgets_bg, width=table_width, height=header_height)
        header_frame.place(x=0, y=0)

        ctk.CTkLabel(
            header_frame, text="Classifica", font=self.table_header_font, text_color=self.widgets_fg_text_color, width=90, anchor="center", fg_color="transparent"
        ).place(x=0, y=5)
        ctk.CTkLabel(
            header_frame, text="Utente", font=self.table_header_font, text_color=self.widgets_fg_text_color, width=180, anchor="center", fg_color="transparent"
        ).place(x=90, y=5)
        ctk.CTkLabel(
            header_frame, text="Punteggio", font=self.table_header_font, text_color=self.widgets_fg_text_color, width=90, anchor="center", fg_color="transparent"
        ).place(x=270, y=5)

        # Scrollable table body
        body_height = table_height - header_height

        # Create canvas and scrollbar
        table_canvas = tk.Canvas(
            table_frame,
            width=table_width,
            height=body_height,
            bg=self.widgets_bg,
            highlightthickness=0,
            bd=0
        )
        table_canvas.place(x=0, y=header_height)

        scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=table_canvas.yview)
        scrollbar.place(x=table_width-15, y=header_height, height=body_height, width=15)

        # Create a frame inside the canvas
        table_body = tk.Frame(table_canvas, bg=self.widgets_bg)
        table_canvas.create_window((0, 0), window=table_body, anchor="nw")

        table_canvas.configure(yscrollcommand=scrollbar.set)

        def on_frame_configure(event):
            table_canvas.configure(scrollregion=table_canvas.bbox("all"))

        table_body.bind("<Configure>", on_frame_configure)

        # Draw vertical lines
        table_canvas.create_line(90, 0, 90, body_height, fill=self.widgets_fg_text_color, width=1)
        table_canvas.create_line(270, 0, 270, body_height, fill=self.widgets_fg_text_color, width=1)
        # Draw horizontal line under headers
        table_canvas.create_line(0, 0, table_width, 0, fill=self.widgets_fg_text_color, width=1)

        # Sort and assign ranks
        # TODO: implementare la logica dello score minimo e ritentare la prova del gioco (+ recap window)
        row_height = 38
        sorted_ranking= self.ranking_data
        for idx, entry in enumerate(sorted_ranking, start=1):
            y = (idx - 1) * row_height + 10
            tk.Label(table_body, text=str(idx), font=self.widgets_font, bg=self.widgets_bg, fg=self.widgets_fg_text_color, width=8, anchor="center").place(x=0, y=y, width=90, height=row_height)
            tk.Label(table_body, text=entry["name"], font=self.widgets_font, bg=self.widgets_bg, fg=self.widgets_fg_text_color, width=20, anchor="center").place(x=90, y=y, width=180, height=row_height)
            tk.Label(table_body, text=str(entry["score"]), font=self.widgets_font, bg=self.widgets_bg, fg=self.widgets_fg_text_color, width=8, anchor="center").place(x=270, y=y, width=90, height=row_height)

        # Optionally, set a minimum size for the table_body frame
        table_body.config(width=table_width-15, height=max(body_height, len(sorted_ranking)*row_height+10))

        # Bottom button
        play_again_button = ctk.CTkButton(
            self,
            text="Giochiamo di nuovo!",
            font=self.button_font,
            fg_color=self.widgets_bg,
            text_color=self.widgets_fg_text_color,
            border_color=self.widgets_border_color,
            border_width=2,
            corner_radius=15,
            width=250,
            height=50,
            command=on_play_again
        )
        play_again_button.place(relx=0.5, rely=0.93, anchor="center")

# Example usage if you want to run this page standalone for testing:
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk(fg_color="#FFE2CC")
    root.resizable(False, False)
    root.minsize(600, 700)
    root.title("Score & Ranking")

    def play_again():
        print("Play again clicked!")

    score_prova=[np.random.randint(60, 101),np.random.randint(0, 60), None, 23.45, -20, 130]
    # self.persona.get_score()
    #portarsi persona nella pagina di scoring
    page = ScoringRankingPage(root,person=None, score_value=score_prova[0], on_play_again=play_again)
    page.pack(fill="both", expand=True)
    root.mainloop()