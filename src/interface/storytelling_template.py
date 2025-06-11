from interface.time_bar import TimeBar
from interface.style import Style
from interface.chat import Chat
from interface.chat_tutorial import ChatTutorial
import customtkinter as ctk
from PIL import Image
import tkinter as tk
import textwrap

class StorytellingTemplate(ctk.CTkFrame):
    def __init__(self, container, story_path=None, story_text=None):
        super().__init__(container, fg_color=Style.WINDOW_BG)

        img_size = 130
        button_width = 160
        button_height = 60

        self.time_container = ctk.CTkFrame(self, fg_color=Style.WINDOW_BG)
        self.time_container.pack(fill="x")
        self.time_bar = TimeBar(self.time_container)

        self.story_container = ctk.CTkFrame(
            self,
            fg_color=Style.WIDGETS_BG,
            border_color=Style.WIDGETS_BORDER_COLOR,
            border_width=2,
            corner_radius=15
        )
        self.story_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Caricamento contenuto
        if story_text is not None:
            self.content = story_text
        elif story_path is not None:
            try:
                with open(story_path, "r") as story:
                    self.content = story.read()
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"Story file not found at '{story_path}'. "
                    "Please ensure the file exists and the path is correct."
                )
        else:
            raise ValueError("You must provide either 'story_path' or 'story_text'.")

        self.story = ctk.CTkLabel(
            self.story_container,
            text=textwrap.fill(self.content),
            font=Style.WIDGETS_FONT,
            text_color=Style.WIDGETS_FG_TEXT_COLOR,
            fg_color="transparent",
            justify="left",
        )
        self.story.pack(padx=15, pady=30, fill="both")

        self.bottom_container = ctk.CTkFrame(self.story_container, fg_color='transparent')
        self.bottom_container.pack(fill="x", padx=20, pady=(0, 20), side="bottom")

        self.robby_img = ctk.CTkImage(
            light_image=Image.open("./rsc/robot.png").resize((img_size, img_size)),
            size=(img_size, img_size)
        )
        self.robby_container = ctk.CTkLabel(
            self.bottom_container,
            image=self.robby_img,
            text="",
            fg_color='transparent'
        )
        self.robby_container.pack(side="left")

        self.next_button = ctk.CTkButton(
            self.bottom_container,
            text='Giochiamo!',
            fg_color=Style.WINDOW_BG,
            text_color=Style.WIDGETS_FG_TEXT_COLOR,
            border_color=Style.WIDGETS_BORDER_COLOR,
            border_width=2,
            corner_radius=15,
            font=Style.WIDGETS_FONT,
            width=button_width,
            height=button_height
        )
        self.next_button.pack(side="right", anchor='s')