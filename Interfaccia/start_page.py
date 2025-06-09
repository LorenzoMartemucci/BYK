"""
start_page.py

This module defines the StartPage class, a custom Tkinter frame that serves as the initial entry screen
for a storytelling or educational application. It allows the user to input their name and proceed to the story section.

Main Features:
- Displays a welcoming interface with a robot illustration.
- Prompts the user to enter their name.
- Stores the name in a shared Person object.
- Includes a 'Play' button to transition to the story selection or gameplay phase.
"""

import customtkinter as ctk
from PIL import Image

class StartPage(ctk.CTkFrame):
    def __init__(self, master, widgets, go_to_story_callback, person, *args, **kwargs):
        # Initialize the StartPage frame
        super().__init__(master, fg_color=widgets['window_bg'], *args, **kwargs)
        self.widgets = widgets
        self.go_to_story_callback = go_to_story_callback
        self.person = person  # Store reference to Person object

        # Main layout container
        self.start_inner_frame = ctk.CTkFrame(self, fg_color=widgets['window_bg'])
        self.start_inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Horizontal layout: robot on the left, box on the right
        self.horizontal_frame = ctk.CTkFrame(self.start_inner_frame, fg_color=widgets['window_bg'])
        self.horizontal_frame.pack(padx=20, pady=20)

        # Robot image
        self.robot_img = Image.open("./Progettazione/robot.png").resize((180, 180))
        self.robot_ctkimage = ctk.CTkImage(light_image=self.robot_img, size=(180, 180))
        self.robot_label = ctk.CTkLabel(self.horizontal_frame, image=self.robot_ctkimage, text="", fg_color="transparent")
        self.robot_label.pack(side="left", padx=10, pady=(20, 0))

        # Input box container
        self.box_frame = ctk.CTkFrame(
            self.horizontal_frame,
            fg_color=widgets['widgets_bg'],
            border_color=widgets['widgets_border_color'],
            border_width=2,
            corner_radius=15
        )
        self.box_frame.pack(side="left", padx=10, pady=10)

        # Prompt label for name input
        self.username_label = ctk.CTkLabel(
            self.box_frame,
            text="COME TI CHIAMI?",
            font=("Comic Sans MS", 18, "bold"),
            text_color=widgets['widgets_fg_text_color'],
            fg_color="transparent"
        )
        self.username_label.pack(pady=(20, 10), padx=20)

        # Name entry field
        self.username_entry = ctk.CTkEntry(
            self.box_frame,
            placeholder_text="Scrivi qui il tuo nome",
            font=widgets['widgets_font'],
            width=200
        )
        self.username_entry.pack(pady=5, padx=20)

        # Start button to go to next phase
        self.start_button = ctk.CTkButton(
            self.box_frame,
            text="GIOCHIAMO",
            command=self.on_prossimo_click,
            fg_color="#FFFFFF",
            text_color=widgets['widgets_fg_text_color'],
            border_color=widgets['widgets_border_color'],
            border_width=2,
            corner_radius=15,
            font=("Comic Sans MS", 14, "bold"),
            width=180,
            height=50
        )
        self.start_button.pack(pady=20)

    def get_username(self):
        """Retrieve and store the username in the Person object."""
        username = self.username_entry.get()
        self.person.set_name(username)
        return username

    def on_prossimo_click(self):
        """Handle the 'Play' button click: store name and transition."""
        username = self.username_entry.get()
        print(f"Username entered: {username}")  # Debug print)
        self.person.set_name(username)
        print("nome persona= ",self.person.get_name())  # Debug print to check if name is set correctly

        self.go_to_story_callback()

