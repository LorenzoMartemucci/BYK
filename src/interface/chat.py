from interface.time_bar import TimeBar
from interface.style import Style

import customtkinter as ctk
from PIL import Image
import tkinter as tk

class Chat(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color=Style.WINDOW_BG)

        self.message_bubbles = []
        self.last_user_message = None

        self.time_bar = TimeBar(self, timer_total=180)

        self.chat = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.chat.pack(fill="both",expand=True)

        self.input_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.input_frame.pack(fill="x", padx=20, pady=(0, 20), side="bottom")

        self.robby_img = ctk.CTkImage(
            light_image=Image.open("./rsc/robot.png").resize(
                (120, 120)
            ),
            size=(120, 120)
        )
        self.robby_label = ctk.CTkLabel(
            self.input_frame,
            image=self.robby_img,
            text=""
        )
        self.robby_label.pack(side="left")

        self.user_input = ctk.CTkTextbox(
            self.input_frame,
            font=Style.WIDGETS_FONT,
            fg_color=Style.WIDGETS_BG,
            text_color=Style.WIDGETS_FG_TEXT_COLOR,
            border_color=Style.WIDGETS_BORDER_COLOR,
            border_width=2,  # Ensure border is visible
            corner_radius=15
        )
        self.user_input.pack(side='left', fill='x', expand=True)

        self.next_button = ctk.CTkButton(
            self.input_frame,
            text="Prossimo",
            command=self.send_message,
            fg_color=Style.WIDGETS_BG,
            text_color=Style.WIDGETS_FG_TEXT_COLOR,
            border_color=Style.WIDGETS_BORDER_COLOR,
            border_width=2,
            corner_radius=15,
            height=70
        )
        self.next_button.pack(side='left', fill='x', expand=True)

        self.next_button.bind("<Button-1>", self.send_message)

    def send_message(self):
        """Handles sending a message from the user input."""
        user_message = self.user_input.get("1.0", "end-1c").strip()
        if user_message:
            self.add_message_bubble(user_message, is_user=True)
            self.last_user_message = user_message
            self.user_input.delete("1.0", "end")  # Clear input field

            # Here you would typically call your LLM or processing function
            # For demonstration, we will simulate a bot response
            bot_response = f"Bot response"
            self.add_message_bubble(bot_response, is_user=False)
    
    def add_message_bubble(self, message, is_user=True):
        """Adds a message bubble to the chat interface."""
        side = "right" if is_user else "left"

        bubble_frame = tk.Frame(self.chat, bg=Style.WINDOW_BG)
        bubble_frame.pack(fill='x', expand=True)

        bubble = ctk.CTkLabel(
            bubble_frame,
            text=message,
            fg_color=Style.USER_BUBBLE_BG if is_user else Style.ROBBY_BUBBLE_BG,
            text_color=Style.WIDGETS_FG_TEXT_COLOR,
            font=Style.WIDGETS_FONT,
            wraplength=300,
            justify="left",
            corner_radius=15
        )
        bubble.pack(side=side, pady=(10, 0), padx=20)
        self.message_bubbles.append(bubble)
        self.chat.update_idletasks()
        self.chat._parent_canvas.yview_moveto(1.0)
    
    def set_next_button_to_next(self):
        # Distruggi il frame di input
        self.input_frame.destroy()
        # Riposiziona il bottone al centro della riga
        self.next_button.pack_forget()
        self.next_button.configure(
            text="Avanti",
            # command=self.go_to_next_storytelling,
            state="normal",
            width=150,  # Set a fixed width for the button
            height=90,
            font=Style.WIDGETS_FONT,
        )
        self.next_button.pack(pady=10, anchor="center")
