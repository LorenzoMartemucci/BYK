from src.interface.final_request_page import FinalRequestPage
from src.interface.storytelling_template import StorytellingTemplate
from src.interface.globals import Globals
import customtkinter as ctk
from PIL import Image

class FailPage(StorytellingTemplate):
    def __init__(self, container):
        super().__init__(container, show_timer=False)
        self.next_button.configure(text="Riprova" ,command=self.go_to_final_request_page)
        self.story.configure(text=f'Peccato! Il tuo punteggio \u00e8 minore di 65 punti.\n'
                                f'Il prompt ideale doveva essere:\n\n {self.ideal_prompt()} \n\nRiproviamo!',
                             font=("Comic Sans MS", 18))
        self.robby_img = ctk.CTkImage(
            light_image=Image.open("./rsc/sad_bot.png").resize((130, 130)),
            size=(130, 130)
        )
        self.robby_container.configure(image=self.robby_img)

    def ideal_prompt(self):
        global_instance= Globals()
        # Trova il prompt ideale per il ruolo corrente
        ideal_prompt = global_instance.ideal_prompts[global_instance.ideal_prompts['Titolo'] == global_instance.role_story]['Prompt Ideale'].values[0]
        return ideal_prompt

    def go_to_final_request_page(self):
        story_page = FinalRequestPage(self.master)
        story_page.pack(fill="both", expand=True)
        self.destroy()
