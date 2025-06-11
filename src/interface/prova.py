import customtkinter as ctk
from PIL import Image
from interface.style import Style
from logics.update_scores import read_scores, write_scores

class ScoringRankingPage(ctk.CTkFrame):
    def __init__(self, container, username, score_value, on_play_again=None):
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
        header_frame = ctk.CTkFrame(self, fg_color=Style.WIDGETS_BG, corner_radius=20)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)

        # Robot image
        image_robot_size = 80
        robot_img = Image.open("./rsc/robot.png").resize((image_robot_size, image_robot_size))
        robot_photo = ctk.CTkImage(light_image=robot_img, size=(image_robot_size, image_robot_size))
        robot_label = ctk.CTkLabel(header_frame, image=robot_photo, text="")
        robot_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        # Titolo e punteggio
        title_label = ctk.CTkLabel(header_frame, text="Congratulazioni!", font=("Comic Sans MS", 24, "bold"))
        title_label.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 0))
        subtitle_label = ctk.CTkLabel(header_frame, text=f"Punteggio: {self.score_value}", font=("Comic Sans MS", 18))
        subtitle_label.grid(row=1, column=1, sticky="w", padx=10, pady=(0, 10))

        # Tabella classifica trasparente
        table_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=15,
            border_width=2,         # <--- aggiungi questa riga
            border_color="black"    # <--- aggiungi questa riga
        )
        table_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        table_frame.grid_rowconfigure(1, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Header tabella trasparente
        col1_width = 90
        col2_width = 180
        col3_width = 90
        sep_width = 2

        header_table = ctk.CTkFrame(table_frame, fg_color=Style.WINDOW_BG, corner_radius=30,border_color="black")
        header_table.grid(row=0, column=0, sticky="ew")
        header_table.grid_columnconfigure(0, weight=col1_width)
        header_table.grid_columnconfigure(1, weight=0)
        header_table.grid_columnconfigure(2, weight=col2_width)
        header_table.grid_columnconfigure(3, weight=0)
        header_table.grid_columnconfigure(4, weight=col3_width)

        ctk.CTkLabel(header_table, text="Classifica", anchor="center", fg_color="transparent").grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(header_table, text="Utente", anchor="center", fg_color="transparent").grid(row=0, column=2, sticky="nsew")
        ctk.CTkLabel(header_table, text="Punteggio", anchor="center", fg_color="transparent").grid(row=0, column=4, sticky="nsew")

        # Corpo NON scrollabile della tabella trasparente
        table_body_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        table_body_frame.grid(row=1, column=0, sticky="nsew")
        table_body_frame.grid_columnconfigure(0, weight=col1_width)
        table_body_frame.grid_columnconfigure(1, weight=0)
        table_body_frame.grid_columnconfigure(2, weight=col2_width)
        table_body_frame.grid_columnconfigure(3, weight=0)
        table_body_frame.grid_columnconfigure(4, weight=col3_width)

        # Mostra solo la top 10
        for i, entry in enumerate(self.ranking_data[:10], start=1):
            ctk.CTkLabel(table_body_frame, text=str(i), anchor="center", fg_color="transparent").grid(row=i, column=0, sticky="nsew")
            ctk.CTkFrame(table_body_frame, width=sep_width, height=25, fg_color="gray").grid(row=i, column=1, sticky="ns")
            ctk.CTkLabel(table_body_frame, text=entry["name"], anchor="center", fg_color="transparent").grid(row=i, column=2, sticky="nsew")
            ctk.CTkFrame(table_body_frame, width=sep_width, height=25, fg_color="gray").grid(row=i, column=3, sticky="ns")
            ctk.CTkLabel(table_body_frame, text=str(entry["score"]), anchor="center", fg_color="transparent").grid(row=i, column=4, sticky="nsew")

        # Bottone per giocare di nuovo
        play_again_button = ctk.CTkButton(
            self,
            text="Giochiamo di nuovo!",
            font=("Comic Sans MS", 13),
            border_width=2,
            corner_radius=15,
            command=on_play_again if on_play_again else None
        )
        play_again_button.grid(row=3, column=0, sticky="ew", padx=100, pady=(10, 20))