from Interfaccia.storytelling_page import StorytellingPage
from Interfaccia.chat_page_tutorial import ChatPageTutorial
from Interfaccia.start_page import StartPage
from Interfaccia.scoring_ranking import ScoringRankingPage
from Interfaccia.person import Person
from Interfaccia.chat_page_final import ChatPageFinal
from Interfaccia.recap_page import RecapPage
from llm.llama3 import LLMBuilder
from llm.Scorer import Scorer
import customtkinter as ctk
from PIL import Image
import os
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 1 = SYSTEM_DPI_AWARE (comportamento come 100% scala)
except Exception:
    pass



class MainApp:
    def __init__(self):
        story_path = "./Progettazione/storia.txt"
        try:
            with open(story_path, "r") as story:
                self.content = story.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Story file not found at '{story_path}'. "
                "Please ensure the file exists and the path is correct."
            )

        self.widgets = {
            'widgets_bg': "#FFA764",
            'widgets_fg_text_color': "#000000",
            'widgets_border_color': "#BF5200",
            'widgets_font': ("Comic Sans MS", 12),
            'window_bg': "#FFE2CC"
        }

        ctk.set_appearance_mode("light")
        self.root = ctk.CTk(fg_color=self.widgets['window_bg'])
        self.root.geometry("480x640")
        self.root.resizable(False, False)
        self.root.minsize(480, 640)
        self.root.configure(bg=self.widgets['window_bg'])

        self.container = ctk.CTkFrame(self.root, fg_color=self.widgets['window_bg'])
        self.container.pack(fill="both", expand=True)

        self.person = Person()
        self.llm_builder = LLMBuilder()
        self.scorer = Scorer()
        self.time_remaining = [120]
        self.chat_time_remaining = [180]
        self.welcome_message = "Hei io sono Robbi, cosa vuoi che sia oggi? Un cuoco? Un insegnate? Un poeta?"


        # Instantiate all pages, but only pack the start page
        self.start_page = StartPage(self.container, self.widgets, self.go_to_story, person=self.person)
        self.storytelling1 = StorytellingPage(self.container, self.content, self.widgets, self.go_to_chat1)
        self.chat_page1 = ChatPageTutorial(self.container, self.widgets, self.person, self.go_to_story2, llm_builder=self.llm_builder, scorer=self.scorer)
        self.recap_page = RecapPage(self.container, self.person, self.widgets, self.go_to_chat2)
        self.chat_page2 = ChatPageFinal(self.container, self.widgets, self.person, self.go_to_scoring)
        self.scoring_page = ScoringRankingPage(self.container,self.widgets, self.person)

        self.show_start_page()

    # --- Frame swap methods ---
    def show_start_page(self):
        """
        Displays the start page of the application, hiding all other frames.
        """
        self.hide_all_frames()
        self.start_page.pack(fill="both", expand=True)

    def go_to_story(self):
        """
        Switches to the first storytelling page, sets and starts the timer for storytelling,
        and stops the chat timer if it is running.
        """
        self.hide_all_frames()
        self.storytelling1.timer_var = [120]
        self.storytelling1.timer_total = 120  
        self.storytelling1.pack(fill="both", expand=True)
        self.storytelling1.start_timer()
        self.chat_page1.stop_timer()  # Ferma il timer della chat

    def go_to_chat1(self):
        """
        Switches to the first chat page, sets and starts the chat timer,
        clears previous messages, stops the storytelling timer, and shows the welcome message.
        """
        self.hide_all_frames()
        self.chat_page1.timer_var = [180]
        self.chat_page1.pack(fill="both", expand=True)
        self.chat_page1.clear_messages()
        self.chat_page1.start_timer()
        self.storytelling1.stop_timer()  # Ferma il timer dello storytelling
        self.root.after_idle(self.chat_page1.show_welcome)

    def go_to_story2(self):
        """
        Switches to the recap (second storytelling) page and sets the timer for storytelling.
        """
        self.hide_all_frames()
        self.recap_page.timer_var = [120]  # Timer storytelling 2: 120 secondi
        self.recap_page.pack(fill="both", expand=True)

    def go_to_chat2(self):
        """
        Switches to the second chat page, sets and starts the chat timer,
        clears previous messages, and shows the welcome message and the first episode.
        """
        self.hide_all_frames()
        self.chat_page2.timer_var = [180]  # Timer chat 2: 180 secondi
        self.chat_page2.timer_total = 180  
        self.chat_page2.pack(fill="both", expand=True)
        self.chat_page2.clear_messages()
        self.chat_page2.start_timer()      
        self.root.after_idle(self.chat_page2.show_welcome_and_first_episode)

    def go_to_scoring(self):
        self.hide_all_frames()
        self.scoring_page.pack(fill="both", expand=True)

    def hide_all_frames(self):
        for frame in [self.start_page, self.storytelling1, self.chat_page1, self.recap_page, self.chat_page2, self.scoring_page]:
            frame.pack_forget()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
