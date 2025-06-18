import customtkinter as ctk
import tkinter as tk
from PIL import Image
from src.interface.storytelling_template import StorytellingTemplate

class Credits(StorytellingTemplate):
    def __init__(self, container):
        super().__init__(container)
        self.next_button.configure(text='Giochiamo di nuovo!', command=self.go_to_start_page)
        self._setup_ui()
        self.robby_img = ctk.CTkImage(
            light_image=Image.open("./rsc/robbi_credits.png").resize((120, 120)),
            size=(120, 120)
        )
        self.robby_container.configure(image=self.robby_img)

        # Avvia animazione titoli di coda
        self.animate_credits()

    def _setup_ui(self):
        # Lista di tuple: (testo, è_ruolo)
        credits_lines = [
            ("Project Manager", True),
            ("Natale Milella", False),
            ("", False),
            ("Design Team", True),
            ("Giovanni Zagaria", False),
            ("Pasquale Fidanza", False),
            ("", False),
            ("Artificial Intelligence Team", True),
            ("Palmina Angelini", False),
            ("Salvatore Patisso", False),
            ("Eleonora Amico", False),
            ("Nicolò Resta", False),
            ("", False),
            ("Interface Team", True),
            ("Daniel Craciun", False),
            ("Lorenzo Martemucci", False),
            ("Giuliano Tarantino", False),
            ("Tommaso Lippolis", False),
            ("", False),
            ("Grazie per aver giocato!", False)
        ]

        self.story.configure(text="")

        self.canvas = tk.Canvas(self, width=450, height=560, bg=self.robby_container._bg_color, highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.41, anchor="center")

        # Font
        bold_font = ("Comic Sans MS", 15, "bold")
        normal_font = ("Comic Sans MS", 15)

        # Inserisci ogni riga come oggetto separato
        self.text_ids = []
        start_y = 600  # posizione iniziale in basso
        line_height = 30  # distanza tra le righe (puoi regolare questo valore)
        for i, (line, is_role) in enumerate(credits_lines):
            font = bold_font if is_role else normal_font
            text_id = self.canvas.create_text(
                228, start_y + i * line_height,
                text=line,
                font=font,
                fill="black",
                justify="center"
            )
            self.text_ids.append(text_id)

    def animate_credits(self):
        speed = 1       # Pixel per frame
        delay = 20      # ms tra i frame

        def step():
            # Prendi la coordinata y della PRIMA riga (quella con indice 0)
            first_coords = self.canvas.coords(self.text_ids[0])
            if first_coords and len(first_coords) >= 2:
                _, first_y = first_coords[:2]
                if first_y > 10:
                    # Muovi tutte le righe verso l'alto
                    for text_id in self.text_ids:
                        self.canvas.move(text_id, 0, -speed)
                    self.after(delay, step)
                # Altrimenti: la prima riga ha toccato il bordo superiore, quindi ferma tutto
            else:
                print("Errore: impossibile ottenere le coordinate della prima riga.")

        step()

    def go_to_start_page(self):
        from src.interface.start_page import StartPage
        start_page = StartPage(self.master)
        start_page.pack(fill="both", expand=True)
        self.destroy()