from storytelling_page import StorytellingPage
from chat_page import ChatPageTutorial
from start_page import StartPage
from scoring_ranking import ScoringRankingPage
from person import Person
import customtkinter as ctk
from PIL import Image
import os

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
        self.root.geometry("600x800")
        self.root.resizable(False, False)
        self.root.minsize(600, 800)
        self.root.configure(bg=self.widgets['window_bg'])

        self.container = ctk.CTkFrame(self.root, fg_color=self.widgets['window_bg'])
        self.container.pack(fill="both", expand=True)

        self.person = Person()
        self.time_remaining = [120]
        self.chat_time_remaining = [180]
        self.welcome_message = "Hei io sono Robbi, cosa vuoi che sia oggi? Un cuoco? Un insegnate? Un poeta?"

        # Instantiate all pages, but only pack the start page
        self.start_page = StartPage(self.container, self.widgets, self.go_to_story, person=self.person)
        self.storytelling1 = StorytellingPage(self.container, self.content, self.widgets, self.go_to_chat1)
        self.chat_page1 = ChatPageTutorial(self.container, self.widgets, self.person, self.go_to_story2)
        self.storytelling2 = StorytellingPage(self.container, self.content, self.widgets, self.go_to_chat2)
        self.chat_page2 = ChatPageTutorial(self.container, self.widgets, self.person, self.go_to_scoring)
        self.scoring_page = ScoringRankingPage(self.container)

        self.show_start_page()

    # --- Frame swap methods ---
    def show_start_page(self):
        self.hide_all_frames()
        self.start_page.pack(fill="both", expand=True)

    def go_to_story(self):
        self.hide_all_frames()
        self.storytelling1.pack(fill="both", expand=True)
        self.storytelling1.update_timer(self.time_remaining, 120, None)

    def go_to_chat1(self):
        self.hide_all_frames()
        self.chat_page1.pack(fill="both", expand=True)
        self.chat_page1.clear_messages()
        self.root.after_idle(self.chat_page1.show_welcome)

    def go_to_story2(self):
        self.hide_all_frames()
        self.storytelling2.pack(fill="both", expand=True)
        self.storytelling2.update_timer(self.time_remaining, 120, None)

    def go_to_chat2(self):
        self.hide_all_frames()
        self.chat_page2.pack(fill="both", expand=True)
        self.chat_page2.clear_messages()
        self.root.after_idle(self.chat_page2.show_welcome)

    def go_to_scoring(self):
        self.hide_all_frames()
        self.scoring_page.pack(fill="both", expand=True)

    def hide_all_frames(self):
        for frame in [self.start_page, self.storytelling1, self.chat_page1, self.storytelling2, self.chat_page2, self.scoring_page]:
            frame.pack_forget()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
