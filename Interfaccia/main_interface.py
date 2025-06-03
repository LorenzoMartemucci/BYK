import tkinter as tk
import tkinter.font as tkFont
import customtkinter as ctk
from PIL import Image, ImageTk
import textwrap

class StorytellingPage(ctk.CTkFrame):
    def __init__(self, master, content, widgets, go_to_chat_callback, *args, **kwargs):
        super().__init__(master, fg_color=widgets['window_bg'], *args, **kwargs)
        self.content = content
        self.widgets = widgets
        self.go_to_chat_callback = go_to_chat_callback

        self.canvas = ctk.CTkCanvas(self, width=400, height=700, bg=widgets['window_bg'], highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        self.image_sides_size = 150
        self.robot_story_img = Image.open("./Progettazione/robot.png").resize((self.image_sides_size, self.image_sides_size))
        self.robot_story_photo = ImageTk.PhotoImage(self.robot_story_img)
        self.robot_label_story = ctk.CTkLabel(self, image=self.robot_story_photo, text="", fg_color=widgets['widgets_bg'])

        self.submit_button = ctk.CTkButton(
            self,
            text='Prossimo',
            command=self.go_to_chat_callback,
            fg_color=widgets['widgets_bg'],
            text_color=widgets['widgets_fg_text_color'],
            border_color=widgets['widgets_border_color'],
            border_width=2,
            corner_radius=15,
            font=widgets['widgets_font'],
            width=160,
            height=60
        )
        self.timer_label = ctk.CTkLabel(self, text="", font=("Comic Sans MS", 14), text_color=widgets['widgets_fg_text_color'])
        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=20, progress_color="#00FF22")

        self.submit_button.place(relx=1.0, rely=1.0, anchor='se', x=-25, y=-25)
        self.timer_label.place(x=25, y=10)
        self.progress_bar.place(x=25, y=40)

        self.canvas.bind("<Configure>", self.on_resize)

    def update_timer(self, time_var, total, callback):
        minutes = time_var[0] // 60
        seconds = time_var[0] % 60
        self.timer_label.configure(text=f"Tempo rimanente: {minutes:02}:{seconds:02}")
        self.progress_bar.set(time_var[0] / total)
        if time_var[0] > 0:
            time_var[0] -= 1
            self.after(1000, lambda: self.update_timer(time_var, total, callback))
        else:
            if callback:
                callback()

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
            border_color=self.widgets['widgets_border_color'],
            fill_color=self.widgets['widgets_bg'],
            text="",
            text_color=self.widgets['widgets_fg_text_color']
        )

        robot_x = 25 + 10
        robot_y = 75 + (height-100) - self.image_sides_size - 10
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
        robot_bottom = robot_y + self.image_sides_size
        robot_right = robot_x + self.image_sides_size

        line_height = 22
        lines = []
        for paragraph in self.content.split('\n'):
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
                    fill=self.widgets['widgets_fg_text_color'],
                    font=self.widgets['widgets_font'],
                    width=text_width - indent
                )
            else:
                self.canvas.create_text(
                    text_x, y,
                    anchor="nw",
                    text=line,
                    fill=self.widgets['widgets_fg_text_color'],
                    font=self.widgets['widgets_font'],
                    width=text_width
                )
            y += line_height

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

        self.robot_chat_img = Image.open("./Progettazione/Robot_Chat.png").resize((150, 150))
        self.robot_chat_photo = ImageTk.PhotoImage(self.robot_chat_img)
        self.robot_chat_label = ctk.CTkLabel(self.center_frame, image=self.robot_chat_photo, text="", fg_color="transparent")
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

class StartPage(ctk.CTkFrame):
    def __init__(self, master, widgets, go_to_story_callback, *args, **kwargs):
        super().__init__(master, fg_color=widgets['window_bg'], *args, **kwargs)
        self.widgets = widgets
        self.go_to_story_callback = go_to_story_callback

        self.start_inner_frame = ctk.CTkFrame(self, fg_color=widgets['window_bg'])
        self.start_inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.horizontal_frame = ctk.CTkFrame(self.start_inner_frame, fg_color=widgets['window_bg'])
        self.horizontal_frame.pack(padx=20, pady=20)

        self.robot_img = Image.open("./Progettazione/robot.png").resize((180, 180))
        self.robot_photo = ImageTk.PhotoImage(self.robot_img)
        self.robot_label = ctk.CTkLabel(self.horizontal_frame, image=self.robot_photo, text="", fg_color="transparent")
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
        return self.username_entry.get()

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

        self.user_data = []
        self.time_remaining = [120]
        self.chat_time_remaining = [180]
        self.welcome_message = "Ciao! Sono il tuo robot amico! Iniziamo un'avventura insieme. "

        self.start_page = StartPage(self.container, self.widgets, self.go_to_story)
        self.start_page.pack(fill="both", expand=True)

        self.storytelling = StorytellingPage(self.container, self.content, self.widgets, self.go_to_chat)
        self.chat_page = ChatPage(self.container, self.widgets, self.welcome_message)

    def go_to_story(self):
        self.user_data.append(self.start_page.get_username())
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

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
