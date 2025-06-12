"""
score_ranking.py

This module defines the ScoreRankingPage class, a custom Tkinter frame designed to display
user scores and a ranking leaderboard in a stylized card interface. It provides visual feedback
at the end of an activity or game, and includes the option to play again.

Main Features:
- Displays a congratulatory message with the user's score.
- Shows a scrollable, ranked leaderboard sorted by score.
- Renders a card layout with headers, robot avatar, and styled buttons.
- Integrates a 'Play Again' button for restarting the experience.
"""

import customtkinter as ctk
from PIL import Image
from interface.style import Style
from logics.update_scores import read_scores, write_scores
from interface.start_page import StartPage
from interface.credits import Credits

class ScoreRankingPage(ctk.CTkFrame):
    def __init__(self, container, username, score_value):
        super().__init__(container, fg_color=Style.WINDOW_BG)
        self.score_value = score_value
        self.username = username

        # Aggiorna classifica
        self.ranking_data = read_scores()
        self.ranking_data.append({"name": self.username, "score": self.score_value})
        self.ranking_data.sort(key=lambda x: x["score"], reverse=True)
        write_scores(self.ranking_data)

        # Layout principale
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header con robot e titolo
        header_frame = ctk.CTkFrame(self, 
                                    fg_color=Style.WIDGETS_BG, 
                                    corner_radius=20, 
                                    border_color=Style.WIDGETS_BORDER_COLOR,
                                    border_width=2,)
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)

        # Robot image
        image_robot_size = 100
        robot_img = Image.open("./rsc/robot.png").resize((image_robot_size, image_robot_size))
        robot_photo = ctk.CTkImage(light_image=robot_img, size=(image_robot_size, image_robot_size))
        robot_label = ctk.CTkLabel(header_frame, image=robot_photo, text="")
        robot_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        # Titolo e punteggio
        title_label = ctk.CTkLabel(header_frame, text="Congratulazioni!", font=("Comic Sans MS", 24, "bold"))
        title_label.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 0))
        subtitle_label = ctk.CTkLabel(header_frame, text=f"Punteggio: {self.score_value}", font=("Comic Sans MS", 22))
        subtitle_label.grid(row=1, column=1, sticky="w", padx=10, pady=(0, 10))

        # Tabella classifica
        table_frame = ctk.CTkFrame(
            self,
            fg_color=Style.WIDGETS_BG,
            corner_radius=20,
            border_color=Style.WIDGETS_BORDER_COLOR,
            border_width=2,
            bg_color='transparent'
        )
        table_frame.grid(row=2, column=0, sticky="nsew", padx=30, pady=20)
        table_frame.grid_columnconfigure(0, weight=90)
        table_frame.grid_columnconfigure(1, weight=0)
        table_frame.grid_columnconfigure(2, weight=180)
        table_frame.grid_columnconfigure(3, weight=0)
        table_frame.grid_columnconfigure(4, weight=90)

        sep_width = 2
        row_height = 30

        # Header (riga 0)
        ctk.CTkLabel(table_frame, text="Classifica", font=("Comic Sans MS", 14), anchor="center", fg_color="transparent",bg_color="transparent").grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        ctk.CTkLabel(table_frame, text="", width=1, height=row_height, fg_color="gray").grid(row=0, column=1, sticky="ns", pady=(5,0))
        ctk.CTkLabel(table_frame, text="Utente", font=("Comic Sans MS", 14), anchor="center", fg_color="transparent",bg_color="transparent").grid(row=0, column=2, sticky="nsew", padx=10, pady=5)
        ctk.CTkLabel(table_frame, text="", width=1, height=row_height, fg_color="gray").grid(row=0, column=3, sticky="ns", pady=(5,0))
        ctk.CTkLabel(table_frame, text="Punteggio", font=("Comic Sans MS", 14), anchor="center", fg_color="transparent", bg_color="transparent").grid(row=0, column=4, sticky="nsew", padx=10, pady=5)

        # Righe classifica (dalla riga 1 in poi)
        for i, entry in enumerate(self.ranking_data[:10], start=1):
            ctk.CTkLabel(table_frame, text=str(i), font=("Comic Sans MS", 12), anchor="center", fg_color="#FFBF94", height=row_height).grid(row=i, column=0, sticky="nsew", padx=(2,0))
            ctk.CTkFrame(table_frame, width=sep_width, height=row_height, fg_color="gray").grid(row=i, column=1, sticky="ns")
            ctk.CTkLabel(table_frame, text=entry["name"], font=("Comic Sans MS", 12), anchor="center", fg_color="#FFBF94", height=row_height).grid(row=i, column=2, sticky="nsew")
            ctk.CTkFrame(table_frame, width=sep_width, height=row_height, fg_color="gray").grid(row=i, column=3, sticky="ns")
            ctk.CTkLabel(table_frame, text=str(entry["score"]), font=("Comic Sans MS", 12), anchor="center", fg_color="#FFBF94", height=row_height).grid(row=i, column=4, sticky="nsew", padx=(0,2))

        # Bottone per giocare di nuovo
        play_again_button = ctk.CTkButton(
            self,
            text="Giochiamo di nuovo!",
            font=("Comic Sans MS", 20),
            fg_color=Style.WIDGETS_BG,
            text_color=Style.WIDGETS_FG_TEXT_COLOR,
            border_width=2,
            corner_radius=15,
            border_color=Style.WIDGETS_BORDER_COLOR,
            command=self.go_to_start_page
        )
        play_again_button.grid(row=3, column=0, sticky="ew", padx=100, pady=5)
        
        play_again_button = ctk.CTkButton(
            self,
            text="Riconoscimenti!",
            font=("Comic Sans MS", 20),
            fg_color=Style.WIDGETS_BG,
            text_color=Style.WIDGETS_FG_TEXT_COLOR,
            border_width=2,
            corner_radius=15,
            border_color=Style.WIDGETS_BORDER_COLOR,
            command=self.go_to_credits_page
        )
        play_again_button.grid(row=4, column=0, sticky="ew", padx=100, pady=(5,10))
        
    def go_to_credits_page(self):
        credits_page = Credits(self.master)
        credits_page.pack(fill="both", expand=True)
        self.destroy()
    
    def go_to_start_page(self):
        story_page = StartPage(self.master)
        story_page.pack(fill="both", expand=True)
        self.destroy()
