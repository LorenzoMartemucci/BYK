import customtkinter as ctk
from PIL import Image

class StartPage(ctk.CTkFrame):
    def __init__(self, master, widgets, go_to_story_callback, person, *args, **kwargs):
        super().__init__(master, fg_color=widgets['window_bg'], *args, **kwargs)
        self.widgets = widgets
        self.go_to_story_callback = go_to_story_callback
        self.person = person  # Store the Person object

        self.start_inner_frame = ctk.CTkFrame(self, fg_color=widgets['window_bg'])
        self.start_inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.horizontal_frame = ctk.CTkFrame(self.start_inner_frame, fg_color=widgets['window_bg'])
        self.horizontal_frame.pack(padx=20, pady=20)

        self.robot_img = Image.open("./Progettazione/robot.png").resize((180, 180))
        self.robot_ctkimage = ctk.CTkImage(light_image=self.robot_img, size=(180, 180))
        self.robot_label = ctk.CTkLabel(self.horizontal_frame, image=self.robot_ctkimage, text="", fg_color="transparent")
        self.robot_label.pack(side="left", padx=10, pady=(20, 0))

        self.box_frame = ctk.CTkFrame(self.horizontal_frame, fg_color=widgets['widgets_bg'], border_color=widgets['widgets_border_color'], border_width=2, corner_radius=15)
        self.box_frame.pack(side="left", padx=10, pady=10)

        self.username_label = ctk.CTkLabel(self.box_frame, text="COME TI CHIAMI?", font=("Comic Sans MS", 18, "bold"), text_color=widgets['widgets_fg_text_color'], fg_color="transparent")
        self.username_label.pack(pady=(20, 10), padx=20)

        self.username_entry = ctk.CTkEntry(self.box_frame, placeholder_text="Scrivi qui il tuo nome", font=widgets['widgets_font'], width=200)
        self.username_entry.pack(pady=5, padx=20)

        self.start_button = ctk.CTkButton(
            self.box_frame,
            text="GIOCHIAMO",
            command=self.go_to_story_callback,
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
        username = self.username_entry.get()
        if self.person is not None:
            self.person.set_name(username)
        return username