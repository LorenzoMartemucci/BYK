from interface.chat_final import ChatFinal
from interface.storytelling_template import StorytellingTemplate

class RecapPage(StorytellingTemplate):
    def __init__(self, container):
        super().__init__(container)
        self.next_button.configure(command=self.go_to_chat_final)
        self.story.configure(self.read_story("./rsc/storia.txt"))

    #La funzione deve leggere dal csv una storia causale tra quelle disponibili e salvare in una lista quelle già mostrate per ruolo

    def go_to_chat_final(self):
        chat_final = ChatFinal(self.master)
        chat_final.pack(fill="both", expand=True)
        self.destroy()
