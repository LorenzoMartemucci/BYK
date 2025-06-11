from interface.start_page import StartPage
from interface.storytelling_template import StorytellingTemplate
from interface.globals import Globals
import customtkinter as ctk
from PIL import Image

class FailPage(StorytellingTemplate):
    def __init__(self, container):
        super().__init__(container, show_timer=False)
        self.next_button.configure(command=self.go_to_start_page)
        self.story.configure(text=f'Il prompt ideale doveva essere: {self.ideal_prompt()} Riproviamo!')
        self.robby_img = ctk.CTkImage(
            light_image=Image.open("./rsc/sad_bot.png").resize((120, 120)),
            size=(120, 120)
        )
        self.robby_container.configure(image=self.robby_img)

    def ideal_prompt(self):
        global_instance= Globals()
        # Trova il prompt ideale per il ruolo corrente
        ideal_prompt = global_instance.ideal_prompts[global_instance.ideal_prompts['Titolo'] == global_instance.role_story]['Prompt Ideale'].values[0]
        return ideal_prompt

    def go_to_start_page(self):
        story_page = StartPage(self.master)
        story_page.pack(fill="both", expand=True)
        self.destroy()
