from src.interface.time_bar import TimeBar
from src.interface.style import Style

import customtkinter as ctk


class StorytellingTemplate(ctk.CTkFrame):
    def __init__(self, container,show_timer=False):
        super().__init__(container, fg_color=Style.WINDOW_BG)

        img_size = 130
        button_width = 160
        button_height = 60

        if show_timer:
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

        self.story = ctk.CTkLabel(
            self.story_container,
            text="",
            font=Style.WIDGETS_FONT,
            text_color=Style.WIDGETS_FG_TEXT_COLOR,
            wraplength=380,
            fg_color="transparent",
            justify="left",
        )
        self.story.pack(padx=15, pady=30, fill="both")

        self.bottom_container = ctk.CTkFrame(self.story_container, fg_color='transparent')
        self.bottom_container.pack(fill="x", padx=20, pady=(0, 20), side="bottom")

        self.robby_container = ctk.CTkLabel(
            self.bottom_container,
            text="",
            fg_color='transparent'
        )
        self.robby_container.pack(side="left")

        self.next_button = ctk.CTkButton(
            self.bottom_container,
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