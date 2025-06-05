"""
chat_page_final.py

This module defines the ChatPageFinal class, a custom Tkinter frame designed for the final stage of a chat interaction within the application.
It provides the user interface, manages input/output messages, processes user responses, and controls the flow of an interactive episode.

Main Features:
- Loads episode questions and objectives from a CSV file based on the selected role.
- Displays messages in a scrollable chat format with user and bot bubbles.
- Handles message input, sending, and response evaluation.
- Implements a countdown timer and progress bar for session management.
- Manages UI layout, including message resizing and avatar positioning.
- Triggers the transition to the next storytelling phase when the episode ends.
"""

import tkinter as tk
import tkinter.font as tkFont
import customtkinter as ctk
from PIL import Image
import pandas as pd
import os

class ChatPageFinal(ctk.CTkFrame):
    def __init__(
        self,
        master,
        widgets,
        person,
        go_to_next_storytelling,
        *args, **kwargs
    ):
        # Initialize the main chat frame
        super().__init__(master, fg_color=widgets['window_bg'], *args, **kwargs)
        self.person = person
        self.go_to_next_storytelling = go_to_next_storytelling

        self.widgets = widgets
        self.check_prompt_relevance_fn = True  # Placeholder for relevance checking function
        self.extract_role_from_prompt_fn = "None"  # Placeholder for role extraction function

        # Load episode data from CSV file with error handling
        csv_path = "./Progettazione/Episodi_Robbi.csv"
        try:
            self.episodes = pd.read_csv(csv_path)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"CSV file not found at '{csv_path}'. "
                "Please ensure the file exists and the path is correct."
            )

        # Initialize internal state variables
        self.current_role = None
        self.current_index = 0
        self.last_domanda = ""
        self.last_obiettivo = ""
        self.message_bubbles = []
        self.last_user_message = None

        # Create chat timer label and progress bar
        self.chat_timer_label = ctk.CTkLabel(self, text="Tempo rimanente: 180", font=("Comic Sans MS", 14), text_color=widgets['widgets_fg_text_color'])
        self.chat_timer_label.place(x=25, y=10)

        self.chat_progress_bar = ctk.CTkProgressBar(self, width=400, height=20, progress_color="#00FF22")
        self.chat_progress_bar.set(1.0)
        self.chat_progress_bar.place(x=25, y=40)

        self.bind("<Configure>", self.on_chat_resize)

        # Main container for chat messages
        self.center_frame = ctk.CTkFrame(self, fg_color=widgets['window_bg'])
        self.center_frame.pack(fill="both", expand=True, padx=20, pady=(70, 20))

        self.chat_canvas = tk.Canvas(self.center_frame, bg=widgets['window_bg'], highlightthickness=0, bd=0)
        self.chat_canvas.pack(side="left", fill="both", expand=True)

        self.chat_scrollbar = tk.Scrollbar(self.center_frame, orient="vertical", command=self.chat_canvas.yview)
        self.chat_scrollbar.pack(side="right", fill="y")

        self.chat_frame = tk.Frame(self.chat_canvas, bg=widgets['window_bg'])
        self.chat_window = self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")

        self.chat_frame.bind("<Configure>", self.on_frame_configure)
        self.chat_canvas.bind("<Configure>", self.on_canvas_configure)
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)
        self.chat_canvas.bind("<Configure>", self.update_bubble_widths)

        # Input field container
        self.input_outer_frame = ctk.CTkFrame(
            self,
            fg_color=widgets['window_bg'],
            border_width=0,
            corner_radius=0
        )
        self.input_outer_frame.pack(fill="x", padx=20, pady=(0, 20), side="bottom")

        self.input_frame = ctk.CTkFrame(
            self.input_outer_frame,
            fg_color=widgets['widgets_bg'],
            border_color=widgets['widgets_border_color'],
            border_width=2,
            corner_radius=15
        )
        self.input_frame.pack(side="left", fill="x", expand=True, padx=(0, 20))

        # Dynamically calculate height for multi-line textbox
        font = widgets['widgets_font']
        f = tkFont.Font(font=font)
        line_height = f.metrics("linespace") + 2
        fixed_height = line_height * 3 + 12

        self.user_input = ctk.CTkTextbox(
            self.input_frame,
            font=widgets['widgets_font'],
            fg_color=widgets['widgets_bg'],
            text_color=widgets['widgets_fg_text_color'],
            border_color=widgets['widgets_border_color'],
            border_width=0,
            corner_radius=15,
            width=320,
            height=fixed_height
        )
        self.user_input.pack(side="left", fill="both", expand=True, padx=10, pady=(8, 8))
        self.user_input.insert("1.0", "")

        self.user_input.bind("<Return>", self.send_message_event)  # Send on Enter
        self.user_input.bind("<Shift-Return>", lambda e: None)     # Prevent newline on Shift+Enter

        self.send_button = ctk.CTkButton(
            self.input_outer_frame,
            text="Invio",
            command=self.send_message,
            fg_color=widgets['widgets_bg'],
            text_color=widgets['widgets_fg_text_color'],
            border_color=widgets['widgets_border_color'],
            border_width=2,
            corner_radius=15,
            width=90,
            height=70
        )
        self.send_button.pack(side="right", padx=(0, 0), pady=10)

        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)
        self.chat_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Load and display robot image
        self.robot_chat_img = Image.open("./Progettazione/robot.png").resize((150, 150))
        self.robot_chat_img = self.robot_chat_img.rotate(-15, expand=True)
        self.robot_chat_ctkimage = ctk.CTkImage(light_image=self.robot_chat_img, size=(150, 150))
        self.robot_chat_label = ctk.CTkLabel(self.center_frame, image=self.robot_chat_ctkimage, text="", fg_color="transparent")
        self.robot_chat_label.place(relx=0.0, rely=1.0, anchor="sw", x=-43, y=0)

        # Welcome message and trigger first episode
        self.welcome_message = "Hei io sono Robbi, cosa vuoi che sia oggi? Un cuoco? Un insegnate? Un poeta?"
        self.after(100, self.show_welcome_and_first_episode)

        # Timer configuration
        self.timer_total = 180
        self.timer_var = [self.timer_total]
        self.timer_running = False
