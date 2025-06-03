import tkinter as tk
import tkinter.font as tkFont
import customtkinter as ctk
from PIL import Image, ImageTk

class ChatPage(ctk.CTkFrame):
    def __init__(self, master, widgets, welcome_message, *args, **kwargs):
        super().__init__(master, fg_color=widgets['window_bg'], *args, **kwargs)
        self.widgets = widgets
        self.welcome_message = welcome_message
        self.message_bubbles = []
        self.last_user_message = None
        self.robby_output_llm = 'Ciao output'

        self.chat_timer_label = ctk.CTkLabel(self, text="Tempo rimanente: 180", font=("Comic Sans MS", 14), text_color=widgets['widgets_fg_text_color'])
        self.chat_timer_label.place(x=25, y=10)

        self.chat_progress_bar = ctk.CTkProgressBar(self, width=400, height=20, progress_color="#00FF22")
        self.chat_progress_bar.set(1.0)
        self.chat_progress_bar.place(x=25, y=40)

        self.bind("<Configure>", self.on_chat_resize)

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

        self.user_input.bind("<Return>", self.send_message_event)
        self.user_input.bind("<Shift-Return>", lambda e: None)

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

        # Load, rotate, and use CTkImage for the robot image
        self.robot_chat_img = Image.open("./Progettazione/robot.png").resize((150, 150))
        self.robot_chat_img = self.robot_chat_img.rotate(-15, expand=True)  # Rotate 15 degrees to the right
        self.robot_chat_ctkimage = ctk.CTkImage(light_image=self.robot_chat_img, size=(150, 150))
        self.robot_chat_label = ctk.CTkLabel(self.center_frame, image=self.robot_chat_ctkimage, text="", fg_color="transparent")
        self.robot_chat_label.place(relx=0.0, rely=1.0, anchor="sw", x=-43, y=0)

    def on_chat_resize(self, event):
        new_width = max(100, event.width - 50)
        self.chat_progress_bar.configure(width=new_width)

    def on_frame_configure(self, event):
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        if self.chat_frame.winfo_reqwidth() != self.chat_canvas.winfo_width():
            self.chat_canvas.itemconfigure(self.chat_window, width=self.chat_canvas.winfo_width())

    def on_canvas_configure(self, event):
        self.chat_canvas.itemconfigure(self.chat_window, width=event.width)

    def add_message(self, text, sender="user"):
        bubble_color = "#FFA764" if sender == "user" else "#AEE4FF"
        anchor = "e" if sender == "user" else "w"
        justify = "right" if sender == "user" else "left"
        padx = (60, 10) if sender == "user" else (87, 60)
        max_width = max(200, self.chat_canvas.winfo_width() - 100)

        bubble_frame = tk.Frame(self.chat_frame, bg=self.widgets['window_bg'])
        bubble_frame.pack(anchor=anchor, pady=8, padx=padx, fill="x")

        bubble = ctk.CTkLabel(
            bubble_frame,
            text=text,
            font=self.widgets['widgets_font'],
            text_color=self.widgets['widgets_fg_text_color'],
            fg_color=bubble_color,
            corner_radius=18,
            anchor="w",
            justify=justify,
            wraplength=max_width,
            padx=10,
            pady=10
        )
        bubble.pack(anchor=anchor, fill="none")

        self.message_bubbles.append((bubble, sender))

    def update_bubble_widths(self, event=None):
        max_width = max(200, self.chat_canvas.winfo_width() - 100)
        for bubble, sender in self.message_bubbles:
            bubble.configure(wraplength=max_width)

    def _on_mousewheel(self, event):
        self.chat_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def send_message(self):
        msg = self.user_input.get("1.0", "end-1c").strip()
        if msg:
            self.last_user_message = msg
            self.add_message(msg, sender="user")
            self.user_input.delete("1.0", "end")
            self.after(500, lambda: self.add_message("Risposta del robot a: " + self.robby_output_llm, sender="bot"))
            self.chat_canvas.yview_moveto(1.0)

    def send_message_event(self, event=None):
        if event and (event.state & 0x0001):
            return
        self.send_message()
        return "break"

    def show_welcome(self):
        self.chat_canvas.update_idletasks()
        self.add_message(self.welcome_message, sender="bot")
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(0.0)

    def clear_messages(self):
        for bubble, _ in self.message_bubbles:
            bubble.master.destroy()
        self.message_bubbles.clear()

    def update_timer(self, time_var, total, callback):
        minutes = time_var[0] // 60
        seconds = time_var[0] % 60
        self.chat_timer_label.configure(text=f"Tempo rimanente: {minutes:02}:{seconds:02}")
        self.chat_progress_bar.set(time_var[0] / total)
        if time_var[0] > 0:
            time_var[0] -= 1
            self.after(1000, lambda: self.update_timer(time_var, total, callback))
        else:
            if callback:
                callback()