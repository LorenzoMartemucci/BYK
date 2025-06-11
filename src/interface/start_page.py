from interface.story_page import StoryPage
from interface.storytelling_template import StorytellingTemplate
from interface.style import Style
import customtkinter as ctk
from PIL import Image

class StartPage(ctk.CTkFrame):
    def __init__(self, container):
        # Initialize the StartPage frame
        super().__init__(container, fg_color=Style.WINDOW_BG)

        # Main layout container
        self.horizontal_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.horizontal_frame.pack(fill="both", expand=True, side="left", padx=10, pady=10)

        # Robot image
        self.robot_img = Image.open("./rsc/robot.png").resize((180, 180))
        self.robot_ctkimage = ctk.CTkImage(light_image=self.robot_img, size=(180, 180))
        self.robot_label = ctk.CTkLabel(
            self.horizontal_frame,
            image=self.robot_ctkimage,
            text=""
        )
        self.robot_label.pack(side="left", padx=10, pady=(20, 0))

        # Input box container
        self.box_frame = ctk.CTkFrame(
            self.horizontal_frame,
            fg_color="transparent",
            # border_color=Style.WIDGETS_BORDER_COLOR,
            # border_width=2,
            # corner_radius=15
        )
        self.box_frame.pack(fill="x", expand=True, side="left", padx=10, pady=10)

        # Prompt label for name input
        # self.username_label = ctk.CTkLabel(
        #     self.box_frame,
        #     text="COME TI CHIAMI?",
        #     font=("Comic Sans MS", 18, "bold"),
        #     text_color=Style.WIDGETS_FG_TEXT_COLOR,
        #     # fg_color="transparent"
        # )
        # self.username_label.pack(pady=(20, 10), padx=20)

        # Name entry field
        # self.username_entry = ctk.CTkEntry(
        #     self.box_frame,
        #     placeholder_text="Scrivi qui il tuo nome",
        #     font=Style.WIDGETS_FONT,
        #     width=200
        # )
        # self.username_entry.pack(pady=5, padx=20)

        # Start button to go to next phase
        self.start_button = ctk.CTkButton(
            self.box_frame,
            text="GIOCHIAMO",
            command=self.go_to_story_page,
            fg_color=Style.WIDGETS_BG,
            text_color=Style.WIDGETS_FG_TEXT_COLOR,
            border_color=Style.WIDGETS_BORDER_COLOR,
            border_width=2,
            corner_radius=15,
            font=("Comic Sans MS", 14, "bold"),
            width=180,
            height=50
        )
        self.start_button.pack(pady=20)
        self.pack(fill="both", expand=True)

    # def get_username(self):
    #     """Retrieve and store the username in the Person object."""
    #     username = self.username_entry.get()
    #     return username

    def go_to_story_page(self):
        """Handle the 'Play' button click: store name and transition."""
        # username = self.username_entry.get()
        # self.master is the parent container of this frame
        storytelling_page = StoryPage(self.master)
        storytelling_page.pack(fill="both", expand=True)
        self.destroy()  # Remove the StartPage frame after transition



