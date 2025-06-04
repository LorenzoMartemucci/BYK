import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import textwrap

class RecapPage(ctk.CTkFrame):
    def __init__(self, master, person, widgets, go_to_chat_callback, *args, **kwargs):
        super().__init__(master, fg_color=widgets['window_bg'], *args, **kwargs)
        self.go_to_chat_callback = go_to_chat_callback
        self.person = person
        self.widgets = widgets

        self.canvas = ctk.CTkCanvas(self, width=400, height=700, bg=widgets['window_bg'], highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        self.image_sides_size = 150
        self.robot_story_img = Image.open("./Progettazione/robot.png").resize((self.image_sides_size, self.image_sides_size))
        self.robot_story_ctkimage = ctk.CTkImage(light_image=self.robot_story_img, size=(self.image_sides_size, self.image_sides_size))
        self.robot_label_story = ctk.CTkLabel(self, image=self.robot_story_ctkimage, text="", fg_color=widgets['widgets_bg'])

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
        self.submit_button.place(relx=1.0, rely=1.0, anchor='se', x=-25, y=-25)

        self.canvas.bind("<Configure>", self.on_resize)

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

    def get_person_recap(self):
        prompt_labels = {
            "role": "Ruolo",
            "task": "Compito",
            "context": "Contesto",
            "output_format": "Formato output",
            "constraint": "Vincoli"
        }
        lines = []
        for key in ["role", "task", "context", "output_format", "constraint"]:
            label = prompt_labels.get(key, key.capitalize())
            value = self.person.prompts.get(key, None)
            lines.append(f"{label}:")
            lines.append(f"{value if value else 'N/A'}")
        return "\n".join(lines)

    def on_resize(self, event):
        width = event.width
        bottom_padding = 25
        button_height = 40
        button_padding = 20
        height = event.height - bottom_padding - button_height - button_padding

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

        # --- NUOVO BLOCCO: Messaggio iniziale ---
        intro_message = "Perfetto hai completato il tutorial! Ecco un piccolo recap di quello che hai scritto prima:"
        recap_text = self.get_person_recap()
        outro_message = "Adesso mettiti alla prova con un test finale!"

        # Prepara tutte le linee da visualizzare
        lines = []
        # Messaggio iniziale
        lines.extend(textwrap.wrap(intro_message, width=60))
        lines.append("")  # Riga vuota

        # Recap
        for paragraph in recap_text.split('\n'):
            wrapped = textwrap.wrap(paragraph, width=60)
            if not wrapped:
                lines.append("")
            else:
                lines.extend(wrapped)
        lines.append("")  # Riga vuota

        # Messaggio finale
        lines.extend(textwrap.wrap(outro_message, width=60))

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