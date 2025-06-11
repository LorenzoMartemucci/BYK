from interface.chat_final import ChatFinal
from interface.storytelling_template import StorytellingTemplate

class RecapPage(StorytellingTemplate):
    def __init__(self, container):
        super().__init__(container, story_text="Inserire il testo recap")
        self.next_button.configure(command=self.go_to_chat_final)

    def go_to_chat_final(self):
        chat_final = ChatFinal(self.master)
        chat_final.pack(fill="both", expand=True)
        self.destroy()
