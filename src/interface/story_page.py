from interface.chat_tutorial import ChatTutorial
from interface.storytelling_template import StorytellingTemplate

class StoryPage(StorytellingTemplate):
    def __init__(self, container):
        super().__init__(container, show_timer=False)
        self.next_button.configure(command=self.got_to_chat_tutorial)
        self.story.configure(text=self.read_story("./rsc/storia.txt"))

    def read_story(self, story_path):
        try:
            with open(story_path, "r") as story_file:
                return story_file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Story file not found at '{story_path}'. Please ensure the file exists and the path is correct.")

    def got_to_chat_tutorial(self):
        chat_page_tutorial = ChatTutorial(self.master)
        chat_page_tutorial.pack(fill="both", expand=True)
        self.destroy()
