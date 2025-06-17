import customtkinter as ctk
import tkinter as tk
from PIL import Image
from interface.storytelling_template import StorytellingTemplate

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
        self.credits_text = (
            "Project Manager\n"
            "Natale Milella\n\n"
            "Design Team\n"
            "Giovanni Zagaria\n"
            "Pasquale Fidanza\n\n"
            "Artificial Intelligence Team\n"
            "Palmina Angelini\n"
            "Salvatore Patisso\n"
            "Eleonora Amico\n"
            "Nicolò Resta\n\n"
            "Interface Team\n"
            "Daniel Craciun\n"
            "Lorenzo Martemucci\n"
            "Giuliano Tarantino\n"
            "Tommaso Lippolis\n\n"
            "Grazie per aver giocato!"
        )
        # Nascondi il testo originale
        self.story.configure(text="")

        # Usa il Canvas di Tkinter standard
        self.canvas = tk.Canvas(self, width=450, height=560, bg=self.robby_container._bg_color, highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.41, anchor="center")

        # Inserisci il testo fuori dalla finestra (in basso)
        self.text_id = self.canvas.create_text(
            250, 720,  # x, y (y > height per partire da sotto)
            text=self.credits_text,
            font=("Comic Sans MS", 15),
            fill="black",
            justify="center"
        )

    def animate_credits(self):
        speed = 1       # Pixel per frame
        delay = 20      # ms tra i frame

        # Calcola l'altezza del testo per sapere quando fermarsi
        bbox = self.canvas.bbox(self.text_id)
        text_height = bbox[3] - bbox[1] if bbox else 0

        def step():
            coords = self.canvas.coords(self.text_id)
            if coords and len(coords) >= 2:
                x, y = coords[:2]
                # Ferma quando la PRIMA riga arriva in alto (y - text_height/2 <= 0)
                if y - text_height / 2 > 0:
                    self.canvas.move(self.text_id, 0, -speed)
                    self.after(delay, step)
            else:
                print("Errore: impossibile ottenere le coordinate del testo.")

        step()

    def go_to_start_page(self):
        from interface.start_page import StartPage
        start_page = StartPage(self.master)
        start_page.pack(fill="both", expand=True)
        self.destroy()