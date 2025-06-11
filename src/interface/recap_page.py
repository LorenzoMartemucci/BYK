from interface.chat_tutorial import ChatTutorial
from interface.storytelling_template import StorytellingTemplate

class RecapPage(StorytellingTemplate):
    def __init__(self, container):
        super().__init__(container, story_text="Inserire il testo recap")
        #self.next_button.configure(command=self.on_prossimo_button_click)

    # def on_prossimo_button_click(self): TODO: implementare CHATFINAL
    #     chat_page_tutorial = ChatTutorial(self.master)
    #     chat_page_tutorial.pack(fill="both", expand=True)
    #     self.destroy()
