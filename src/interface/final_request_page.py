from interface.chat_final import ChatFinal
from interface.storytelling_template import StorytellingTemplate
import pandas as pd
import random
import customtkinter as ctk
from PIL import Image

class FinalRequestPage(StorytellingTemplate):
    def __init__(self, container):
        super().__init__(container)
        self.next_button.configure(command=self.go_to_chat_final)
        self.story.configure(text="Adesso è arrivato il momento di metterti alla prova!\n"+
                             " Ti verrà fornito un problema da risolvere insieme a Robbi.\n"+
                             " Ricorda, avrai a disposizione 2 minuti per ottenere un punteggio bonus.\n"+
                             " Buona fortuna e buon lavoro!\n",
                             font=("Comic Sans MS", 20))
        self.robby_img = ctk.CTkImage(
            light_image=Image.open("./rsc/robot.png").resize((120, 120)),
            size=(120, 120)
        )

        self.robby_container.configure(image=self.robby_img)

    def go_to_chat_final(self):
        chat_final = ChatFinal(self.master)
        chat_final.pack(fill="both", expand=True)
        self.destroy()

#La funzione deve leggere dal csv una storia causale tra quelle disponibili e salvare in una lista quelle già mostrate. quindi la lista dovrà contenre il titolo della storia, quindi quando si rifà il gioco, la lista contiene magari insegnnte, quello sarà escluso da quelli casuali
# Variabile globale per tenere traccia dei titoli già mostrati
