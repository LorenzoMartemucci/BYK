import tkinter as tk
import tkinter.font as tkFont
import customtkinter as ctk
from PIL import Image, ImageTk
import textwrap


class MainApplication:
    def __init__(self, root):
        self.root = root
        self.setup_root()
        self.user_data = []
        self.time_remaining = [120]
        self.chat_time_remaining = [180]
        self.message_bubbles = []
        self.last_user_message = None
        self.welcome_message = "Ciao! Sono il tuo robot amico! Iniziamo un'avventura insieme. "

        # Load resources
        self.load_resources()

        # Create container and pages
        self.container = ctk.CTkFrame(self.root, fg_color=self.window_bg)
        self.container.pack(fill="both", expand=True)

        self.start_page = StartPage(self)
        self.storytelling_page = StorytellingPage(self)
        self.chat_page = ChatPage(self)

        # Show the start page
        self.start_page.show()

    def setup_root(self):
        self.window_bg = "#FFE2CC"
        ctk.set_appearance_mode("light")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.root.minsize(600, 400)
        self.root.configure(bg=self.window_bg)

    def load_resources(self):
        self.widgets_bg = "#FFA764"
        self.widgets_fg_text_color = "#000000"
        self.widgets_border_color = "#BF5200"
        self.widgets_font = ("Comic Sans MS", 12)

        with open("./Progettazione/storia.txt", "r") as story:
            self.story_content = story.read()

        self.robot_img = Image.open("./Progettazione/robot.png").resize((180, 180))
        self.robot_photo = ImageTk.PhotoImage(self.robot_img)

        self.robot_story_img = Image.open("./Progettazione/robot.png").resize((150, 150))
        self.robot_story_photo = ImageTk.PhotoImage(self.robot_story_img)

        self.robot_chat_img = Image.open("./Progettazione/Robot_Chat.png").resize((150, 150))
        self.robot_chat_photo = ImageTk.PhotoImage(self.robot_chat_img)

    def update_generic_timer(self, time_var, label, progress, total, callback):
        minutes = time_var[0] // 60
        seconds = time_var[0] % 60
        label.configure(text=f"Tempo rimanente: {minutes:02}:{seconds:02}")
        progress.set(time_var[0] / total)
        if time_var[0] > 0:
            time_var[0] -= 1
            self.root.after(1000, lambda: self.update_generic_timer(time_var, label, progress, total, callback))
        elif callback:
            callback()


class StartPage:
    def __init__(self, app):
        self.app = app
        self.frame = ctk.CTkFrame(app.container, fg_color=app.window_bg)

        # Inner frame
        start_inner_frame = ctk.CTkFrame(self.frame, fg_color=app.window_bg)
        start_inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Horizontal layout
        horizontal_frame = ctk.CTkFrame(start_inner_frame, fg_color=app.window_bg)
        horizontal_frame.pack(padx=20, pady=20)

        # Robot image
        robot_label = ctk.CTkLabel(horizontal_frame, image=app.robot_photo, text="", fg_color="transparent")
        robot_label.pack(side="left", padx=10, pady=(20, 0))

        # Box frame
        box_frame = ctk.CTkFrame(
            horizontal_frame,
            fg_color=app.widgets_bg,
            border_color=app.widgets_border_color,
            border_width=2,
            corner_radius=15
        )
        box_frame.pack(side="left", padx=10, pady=10)

        username_label = ctk.CTkLabel(
            box_frame,
            text="COME TI CHIAMI?",
            font=("Comic Sans MS", 18, "bold"),
            text_color=app.widgets_fg_text_color,
            fg_color="transparent"
        )
        username_label.pack(pady=(20, 10), padx=20)

        self.username_entry = ctk.CTkEntry(
            box_frame,
            placeholder_text="Scrivi qui il tuo nome",
            font=app.widgets_font,
            width=200
        )
        self.username_entry.pack(pady=5, padx=20)

        start_button = ctk.CTkButton(
            box_frame,
            text="GIOCHIAMO",
            command=self.go_to_story,
            fg_color="#FFFFFF",
            text_color=app.widgets_fg_text_color,
            border_color=app.widgets_border_color,
            border_width=2,
            corner_radius=15,
            font=("Comic Sans MS", 14, "bold"),
            width=180,
            height=50
        )
        start_button.pack(pady=20)

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()

    def go_to_story(self):
        self.app.user_data.append(self.username_entry.get())
        self.hide()
        self.app.root.resizable(True, True)
        self.app.root.minsize(550, 500)
        self.app.storytelling_page.show()
        self.app.time_remaining[0] = 120
        self.app.update_generic_timer(
            self.app.time_remaining,
            self.app.storytelling_page.timer_label,
            self.app.storytelling_page.progress_bar,
            120,
            None
        )


class StorytellingPage:
    def __init__(self, app):
        self.app = app
        self.frame = ctk.CTkFrame(app.container, fg_color=app.window_bg)

        # Canvas
        self.canvas = ctk.CTkCanvas(self.frame, width=400, height=700, bg=app.window_bg, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        # Robot image
        self.robot_label_story = ctk.CTkLabel(self.frame, image=app.robot_story_photo, text="", fg_color=app.widgets_bg)

        # Submit button
        self.submit_button = ctk.CTkButton(
            self.frame,
            text='Prossimo',
            command=self.go_to_chat,
            fg_color=app.widgets_bg,
            text_color=app.widgets_fg_text_color,
            border_color=app.widgets_border_color,
            border_width=2,
            corner_radius=15,
            font=app.widgets_font,
            width=160,
            height=60
        )
        self.submit_button.place(relx=1.0, rely=1.0, anchor='se', x=-25, y=-25)

        # Timer and progress bar
        self.timer_label = ctk.CTkLabel(self.frame, text="", font=("Comic Sans MS", 14), text_color=app.widgets_fg_text_color)
        self.progress_bar = ctk.CTkProgressBar(self.frame, width=400, height=20, progress_color="#00FF22")
        self.timer_label.place(x=25, y=10)
        self.progress_bar.place(x=25, y=40)

        self.canvas.bind("<Configure>", self.on_resize)

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()

    def go_to_chat(self):
        self.hide()
        self.app.chat_page.show()
        self.app.root.resizable(False, False)
        self.app.root.minsize(600, 800)
        self.app.chat_time_remaining[0] = 180
        self.app.update_generic_timer(
            self.app.chat_time_remaining,
            self.app.chat_page.chat_timer_label,
            self.app.chat_page.chat_progress_bar,
            180,
            None
        )

    def on_resize(self, event):
        width = event.width
        bottom_padding = 25
        button_height = 40
        button_padding = 20
        height = event.height - bottom_padding - button_height - button_padding

        self.progress_bar.configure(width=width - 50)
        self.progress_bar.place(x=25, y=40)
        self.timer_label.place(x=25, y=10)

        self.canvas.delete("all")
        self.create_rounded_label(
            self.canvas,
            x=25, y=75,
            width=width-50, height=height-100,
            radius=20,
            border_color=self.app.widgets_border_color,
            fill_color=self.app.widgets_bg,
            text="",
            text_color=self.app.widgets_fg_text_color
        )

        robot_x = 25 + 10
        robot_y = 75 + (height-100) - 150 - 10
        self.robot_label_story.place(x=robot_x, y=robot_y)

        box_x = 25
        box_y = 75
        box_width = width - 50
        box_height = height - 100
        text_padding_x = 20
        text_padding_y = 20
        text_x = box_x + text_padding_x
        text_y = box_y + text_padding_y
        text_width = box_width - 2 * text_padding_x
        robot_top = robot_y
        robot_bottom = robot_y + 150
        robot_right = robot_x + 150

        line_height = 22
        lines = []
        for paragraph in self.app.story_content.split('\n'):
            wrapped = textwrap.wrap(paragraph, width=60)
            if not wrapped:
                lines.append("")
            else:
                lines.extend(wrapped)

        y = text_y
        for line in lines:
            if robot_top < y < robot_bottom:
                indent = robot_right - text_x + 10
                self.canvas.create_text(
                    text_x + indent, y,
                    anchor="nw",
                    text=line,
                    fill=self.app.widgets_fg_text_color,
                    font=self.app.widgets_font,
                    width=text_width - indent
                )
            else:
                self.canvas.create_text(
                    text_x, y,
                    anchor="nw",
                    text=line,
                    fill=self.app.widgets_fg_text_color,
                    font=self.app.widgets_font,
                    width=text_width
                )
            y += line_height

    def create_rounded_label(self, canvas, x, y, width, height, radius, border_color, fill_color, text, text_color):
        points = [
            x+radius, y,
            x+width-radius, y,
            x+width, y,
            x+width, y+radius,
            x+width, y+height-radius,
            x+width, y+height,
            x+width-radius, y+height,
            x+radius, y+height,
            x, y+height,
            x, y+height-radius,
            x, y+radius,
            x, y
        ]
        canvas.create_polygon(points, smooth=True, fill=fill_color, outline=border_color, width=2)
        canvas.create_text(x+width/2, y+height/2, text=text, fill=text_color, font=("Comic Sans MS", 12))


class ChatPage:
    def __init__(self, app):
        self.app = app
        self.frame = ctk.CTkFrame(app.container, fg_color=app.window_bg)

        # Timer and progress bar
        self.chat_timer_label = ctk.CTkLabel(self.frame, text="Tempo rimanente: 180", font=("Comic Sans MS", 14), text_color=app.widgets_fg_text_color)
        self.chat_timer_label.place(x=25, y=10)

        self.chat_progress_bar = ctk.CTkProgressBar(self.frame, width=400, height=20, progress_color="#00FF22")
        self.chat_progress_bar.set(1.0)
        self.chat_progress_bar.place(x=25, y=40)

        # Center frame for chat
        self.center_frame = ctk.CTkFrame(self.frame, fg_color=app.window_bg)
        self.center_frame.pack(fill="both", expand=True, padx=20, pady=(70, 20))

        # Chat canvas
        self.chat_canvas = tk.Canvas(self.center_frame, bg=app.window_bg, highlightthickness=0, bd=0)
        self.chat_canvas.pack(side="left", fill="both", expand=True)

        self.chat_scrollbar = tk.Scrollbar(self.center_frame, orient="vertical", command=self.chat_canvas.yview)
        self.chat_scrollbar.pack(side="right", fill="y")

        self.chat_frame = tk.Frame(self.chat_canvas, bg=app.window_bg)
        self.chat_window = self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")

        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)

        # Input frame
        self.input_outer_frame = ctk.CTkFrame(self.frame, fg_color=app.window_bg, border_width=0, corner_radius=0)
        self.input_outer_frame.pack(fill="x", padx=20, pady=(0, 20), side="bottom")

        self.input_frame = ctk.CTkFrame(
            self.input_outer_frame,
            fg_color=app.widgets_bg,
            border_color=app.widgets_border_color,
            border_width=2,
            corner_radius=15
        )
        self.input_frame.pack(side="left", fill="x", expand=True, padx=(0, 20))

        self.user_input = ctk.CTkTextbox(
            self.input_frame,
            font=app.widgets_font,
            fg_color=app.widgets_bg,
            text_color=app.widgets_fg_text_color,
            border_color=app.widgets_border_color,
            border_width=0,
            corner_radius=15,
            width=320,
            height=60
        )
        self.user_input.pack(side="left", fill="both", expand=True, padx=10, pady=(8, 8))
        self.user_input.insert("1.0", "")

        self.send_button = ctk.CTkButton(
            self.input_outer_frame,
            text="Invio",
            command=self.send_message,
            fg_color=app.widgets_bg,
            text_color=app.widgets_fg_text_color,
            border_color=app.widgets_border_color,
            border_width=2,
            corner_radius=15,
            width=90,
            height=70
        )
        self.send_button.pack(side="right", padx=(0, 0), pady=10)

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()

    def send_message(self):
        msg = self.user_input.get("1.0", "end-1c").strip()
        if msg:
            self.app.last_user_message = msg
            self.add_message(msg, sender="user")
            self.user_input.delete("1.0", "end")
            self.app.root.after(500, lambda: self.add_message("Risposta del robot a: " + self.app.welcome_message, sender="bot"))
            self.chat_canvas.yview_moveto(1.0)

    def add_message(self, text, sender="user"):
        bubble_color = "#FFA764" if sender == "user" else "#AEE4FF"
        anchor = "e" if sender == "user" else "w"
        justify = "right" if sender == "user" else "left"
        padx = (60, 10) if sender == "user" else (87, 60)
        max_width = max(200, self.chat_canvas.winfo_width() - 100)

        bubble_frame = tk.Frame(self.chat_frame, bg=self.app.window_bg)
        bubble_frame.pack(anchor=anchor, pady=8, padx=padx, fill="x")

        bubble = ctk.CTkLabel(
            bubble_frame,
            text=text,
            font=self.app.widgets_font,
            text_color=self.app.widgets_fg_text_color,
            fg_color=bubble_color,
            corner_radius=18,
            anchor="w",
            justify=justify,
            wraplength=max_width,
            padx=10,
            pady=10
        )
        bubble.pack(anchor=anchor, fill="none")

        self.app.message_bubbles.append((bubble, sender))


if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApplication(root)
    root.mainloop()
