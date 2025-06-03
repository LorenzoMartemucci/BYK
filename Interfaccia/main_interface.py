from storytelling_page import StorytellingPage
from chat_page import ChatPage
from start_page import StartPage
from person import Person
import customtkinter as ctk
from PIL import Image

class MainApp:
    def __init__(self):
        with open("./Progettazione/storia.txt", "r") as story:
            self.content = story.read()

        self.widgets = {
            'widgets_bg': "#FFA764",
            'widgets_fg_text_color': "#000000",
            'widgets_border_color': "#BF5200",
            'widgets_font': ("Comic Sans MS", 12),
            'window_bg': "#FFE2CC"
        }

        ctk.set_appearance_mode("light")
        self.root = ctk.CTk(fg_color=self.widgets['window_bg'])
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.root.minsize(600, 400)
        self.root.configure(bg=self.widgets['window_bg'])

        self.container = ctk.CTkFrame(self.root, fg_color=self.widgets['window_bg'])
        self.container.pack(fill="both", expand=True)

        self.person = Person()
        self.time_remaining = [120]
        self.chat_time_remaining = [180]
        self.welcome_message = "Ciao! Sono Robbi! Come posso esserti utile?"

        self.start_page = StartPage(self.container, self.widgets, self.go_to_story)
        self.start_page.pack(fill="both", expand=True)

        self.storytelling = StorytellingPage(self.container, self.content, self.widgets, self.go_to_chat)
        self.chat_page = ChatPage(self.container, self.widgets, self.welcome_message)

    def go_to_story(self):
        name = self.start_page.get_username()
        self.person.set_name(name)  # Save the name in the Person class
        self.start_page.pack_forget()
        self.root.resizable(True, True)
        self.root.minsize(550, 500)
        self.storytelling.pack(fill="both", expand=True)
        self.time_remaining[0] = 120
        self.storytelling.update_timer(self.time_remaining, 120, None)

    def go_to_chat(self):
        self.storytelling.pack_forget()
        self.chat_page.pack(fill="both", expand=True)
        self.root.resizable(False, False)
        self.root.minsize(600, 800)
        self.chat_time_remaining[0] = 180
        self.chat_page.update_timer(self.chat_time_remaining, 180, None)
        self.chat_page.clear_messages()
        self.root.after_idle(self.chat_page.show_welcome)
        # Example: update the score when entering chat
        # self.person.update_score(10)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
