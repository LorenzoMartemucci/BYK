from interface.chat_tutorial import ChatTutorial
from interface.storytelling_template import StorytellingTemplate

class StoryPage(StorytellingTemplate):
    def __init__(self, container):
        super().__init__(container, story_path="./rsc/storia.txt")
        self.next_button.configure(command=self.got_to_chat_tutorial)


    def got_to_chat_tutorial(self):
        chat_page_tutorial = ChatTutorial(self.master)
        chat_page_tutorial.pack(fill="both", expand=True)
        self.destroy()
