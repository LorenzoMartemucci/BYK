from interface.chat_final import ChatFinal
from interface.storytelling_template import StorytellingTemplate
import pandas as pd
import random
from interface.globals import shown_stories as ss

class FinalRequestPage(StorytellingTemplate):
    def __init__(self, container):
        super().__init__(container)
        self.next_button.configure(command=self.go_to_chat_final)
        self.story.configure(text=self.read_quest())

    def go_to_chat_final(self):
        chat_final = ChatFinal(self.master)
        chat_final.pack(fill="both", expand=True)
        self.destroy()

#La funzione deve leggere dal csv una storia causale tra quelle disponibili e salvare in una lista quelle già mostrate. quindi la lista dovrà contenre il titolo della storia, quindi quando si rifà il gioco, la lista contiene magari insegnnte, quello sarà escluso da quelli casuali
# Variabile globale per tenere traccia dei titoli già mostrati

    def read_quest(self):
        rows= len(ss)
        if rows != 0:
            random_number = random.randint(0, rows-1)
            ss_story_local= ss.iloc[random_number, 1]
            ss.drop(random_number)
            return ss_story_local
        else:
            raise ValueError("Tutte le storie sono già state mostrate.")