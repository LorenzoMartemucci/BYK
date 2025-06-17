from interface.chat_tutorial import ChatTutorial
from interface.storytelling_template import StorytellingTemplate
import customtkinter as ctk
from PIL import Image

class StoryPage(StorytellingTemplate):
    def __init__(self, container):
        super().__init__(container, show_timer=False)
        self.next_button.configure(text='Vai al tutorial' ,command=self.got_to_chat_tutorial)
        self.story.configure(text=self.read_story("./rsc/storia.txt"))

        self.robby_img = ctk.CTkImage(
            light_image=Image.open("./rsc/robot.png").resize((120, 120)),
            size=(120, 120)
        )

        self.robby_container.configure(image=self.robby_img)

    def read_story(self, story_path):
        try:
            with open(story_path, "r", encoding="utf-8") as story_file:
                return story_file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Story file not found at '{story_path}'. Please ensure the file exists and the path is correct.")

    def got_to_chat_tutorial(self):
        chat_page_tutorial = ChatTutorial(self.master) # ChatTutorial(self.master)
        chat_page_tutorial.pack(fill="both", expand=True)
        self.destroy()
