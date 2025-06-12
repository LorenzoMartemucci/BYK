from interface.storytelling_template import StorytellingTemplate
import customtkinter as ctk
from PIL import Image

class Credits (StorytellingTemplate):
    def __init__(self, container):
        super().__init__(container)
        self.next_button.configure(command=self.go_to_start_page)
        self._setup_ui()
        self.robby_img = ctk.CTkImage(
            light_image=Image.open("./rsc/robbi_credits.png").resize((120, 120)),
            size=(120, 120)
        )

        self.robby_container.configure(image=self.robby_img)

    def _setup_ui(self):
        credits_text = (
        "Project Manager:\n"
        "Natale Milella\n\n"
        "Design Team:\n"
        "Giovanni Zagaria\n"
        "Pasquale Fidanza\n\n"
        "Artificial Intelligence Team:\n"
        "Palmina Angelini\n"
        "Salvatore Patisso\n"
        "Eleonora Amico\n"
        "Nicolò Resta\n\n"
        "Interface Team:\n"
        "Daniel Craciun\n"
        "Lorenzo Martemucci\n"
        "Giuliano Tarantino\n"
        "Tommaso Lippolis\n\n"
        "Grazie per aver giocato!"
        )
        self.story.configure(
            text=credits_text,
            font=("Comic Sans MS", 15),
            justify="center"
        )
        self.next_button.configure(text="Giochiamo di nuovo!")

    def go_to_start_page(self):
        from interface.start_page import StartPage
        start_page = StartPage(self.master)
        start_page.pack(fill="both", expand=True)
        self.destroy()