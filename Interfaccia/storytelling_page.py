"""
storytelling_page.py

This module defines the StorytellingPage class, a custom Tkinter frame used to present narrative content
in a storytelling or educational application. It displays story text within a rounded panel and includes
a countdown timer, robot image, and navigation button.

Main Features:
- Shows story content with dynamic layout and text wrapping.
- Displays a timer and progress bar to track time remaining.
- Includes a 'Next' button to continue to the chat or next phase.
- Automatically resizes content to fit various screen dimensions.
"""

import tkinter as tk
import customtkinter as ctk
from PIL import Image
import textwrap

class StorytellingPage(ctk.CTkFrame):
    def __init__(self, master, content, widgets, go_to_chat_callback, *args, **kwargs):
        # Initialize storytelling page frame
        super().__init__(master, fg_color=widgets['window_bg'], *args, **kwargs)
        self.go_to_chat_callback = go_to_chat_callback
        self.content = content
        self.widgets = widgets

        self.scale = widgets.get('scale', 1.0)

        # --- Responsive sizes ---
        self.image_sides_size = int(150 * self.scale)
        self.button_width = int(160 * self.scale)
        self.button_height = int(60 * self.scale)
        self.progress_height = int(20 * self.scale)
        self.progress_padx = int(25 * self.scale)
        self.progress_pady = int(40 * self.scale)
        self.timer_font = ("Comic Sans MS", max(10, int(14 * self.scale)))
        self.line_height = int(22 * self.scale)
        self.text_font = (widgets['widgets_font'][0], max(10, int(widgets['widgets_font'][1] * self.scale)))

        # Canvas per il box arrotondato e il testo
        self.canvas = ctk.CTkCanvas(self, bg=widgets['window_bg'], highlightthickness=0)
        self.canvas.place(relx=0, rely=0.12, relwidth=1, relheight=0.75)

        # Immagine robot
        self.robot_story_img = Image.open("./Progettazione/robot.png").resize(
            (self.image_sides_size, self.image_sides_size)
        )
        self.robot_story_ctkimage = ctk.CTkImage(light_image=self.robot_story_img, size=(self.image_sides_size, self.image_sides_size))
        # Cambia master da self a self.canvas
        self.robot_label_story = ctk.CTkLabel(self.canvas, image=self.robot_story_ctkimage, text="", fg_color=widgets['widgets_bg'])

        # Bottone "Prossimo"
        self.submit_button = ctk.CTkButton(
            self,
            text='Prossimo',
            command=self.go_to_chat_callback,
            fg_color=widgets['widgets_bg'],
            text_color=widgets['widgets_fg_text_color'],
            border_color=widgets['widgets_border_color'],
            border_width=2,
            corner_radius=int(15 * self.scale),
            font=self.text_font,
            width=self.button_width,
            height=self.button_height
        )
        self.submit_button.place(relx=0.75, rely=0.90, relwidth=0.22, relheight=0.09)

        # Timer e barra di progresso
        self.timer_label = ctk.CTkLabel(self, text="", font=self.timer_font, text_color=widgets['widgets_fg_text_color'])
        self.timer_label.place(relx=0.02, rely=0.03)

        self.progress_bar = ctk.CTkProgressBar(self, height=self.progress_height, progress_color="#00FF22")
        self.progress_bar.place(relx=0.02, rely=0.08, relwidth=0.96)

        self.canvas.bind("<Configure>", self.on_resize)
        self.text_canvas_id = None  # Per gestire il testo dinamico

    def update_timer(self, time_var, total, callback):
        # Update timer and progress bar every second
        if not self.timer_running:
            return
        minutes = time_var[0] // 60
        seconds = time_var[0] % 60
        self.timer_label.configure(text=f"Tempo rimanente: {minutes:02}:{seconds:02}")
        progress = time_var[0] / total
        progress = max(0, min(1, progress))
        self.progress_bar.set(progress)
        self.update_idletasks()
        if time_var[0] > 0:
            time_var[0] -= 1
            self.after(1000, lambda: self.update_timer(time_var, total, callback))
        else:
            if callback:
                callback()

    def start_timer(self):
        # Start the countdown timer
        self.timer_running = True
        self.update_timer(self.timer_var, self.timer_total, None)

    def stop_timer(self):
        # Stop the countdown timer
        self.timer_running = False

    def create_rounded_label(self, canvas, x, y, width, height, radius, border_color, fill_color):
        # Draw a rounded rectangle
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

    def on_resize(self, event):
        width = event.width
        height = event.height

        # Box arrotondato
        box_x = int(10 * self.scale)
        box_y = int(10 * self.scale)
        box_width = width - 2 * box_x
        box_height = height - 2 * box_y
        radius = int(15 * self.scale)

        self.canvas.delete("all")
        self.create_rounded_label(
            self.canvas,
            x=box_x, y=box_y,
            width=box_width, height=box_height,
            radius=radius,
            border_color=self.widgets['widgets_border_color'],
            fill_color=self.widgets['widgets_bg']
        )

        # --- Calcolo dinamico dimensione robot ---
        min_robot_size = int(48 * self.scale)
        max_robot_size = int(box_height * 0.3)
        available_height = box_height - int(20 * self.scale)  # padding sopra e sotto
        robot_size = min(self.image_sides_size, max_robot_size, available_height)
        robot_size = max(min_robot_size, robot_size)

        # Aggiorna immagine robot se necessario
        if not hasattr(self, "_last_robot_size") or robot_size != self._last_robot_size:
            robot_img = self.robot_story_img.resize((int(robot_size), int(robot_size)))
            self.robot_story_ctkimage = ctk.CTkImage(light_image=robot_img, size=(int(robot_size), int(robot_size)))
            self.robot_label_story.configure(image=self.robot_story_ctkimage)
            self._last_robot_size = robot_size

        robot_x = box_x + int(10 * self.scale)
        # Spazio verticale disponibile sotto il testo
        text_padding_y = int(20 * self.scale)
        text_height = box_height - robot_size - 2 * text_padding_y
        # Se lo spazio per il testo è troppo poco, riduci ancora il robot
        if text_height < int(60 * self.scale):
            robot_size = max(min_robot_size, box_height // 4)
            robot_img = self.robot_story_img.resize((int(robot_size), int(robot_size)))
            self.robot_story_ctkimage = ctk.CTkImage(light_image=robot_img, size=(int(robot_size), int(robot_size)))
            self.robot_label_story.configure(image=self.robot_story_ctkimage)
            self._last_robot_size = robot_size
            text_height = box_height - robot_size - 2 * text_padding_y

        # Centra verticalmente il robot nello spazio in basso
        robot_y = box_y + box_height - robot_size - int(10 * self.scale)
        if robot_y < box_y + int(10 * self.scale):
            robot_y = box_y + int(10 * self.scale)

        self.canvas.create_window(
            robot_x, robot_y,
            anchor="nw",
            window=self.robot_label_story,
            width=robot_size,
            height=robot_size
        )

        # --- Testo adattivo sopra il robot ---
        text_padding_x = int(20 * self.scale)
        text_padding_y = int(20 * self.scale)
        text_x = box_x + text_padding_x
        text_y = box_y + text_padding_y
        text_width = box_width - 2 * text_padding_x
        # L'altezza massima del testo è fino al bordo superiore del robot meno padding
        text_height = robot_y - box_y - text_padding_y

        # Cancella testo precedente
        if self.text_canvas_id:
            self.canvas.delete(self.text_canvas_id)

        # Wrapping manuale per il testo
        font = self.text_font
        chars_per_line = max(10, int(text_width // (font[1] * 0.6)))
        lines = []
        for paragraph in self.content.split('\n'):
            lines.extend(textwrap.wrap(paragraph, width=chars_per_line))
            if paragraph.strip() == "":
                lines.append("")

        # Calcola quante righe ci stanno
        max_lines = max(1, int(text_height // self.line_height))
        visible_lines = lines[:max_lines]
        if len(lines) > max_lines:
            # Aggiungi "..." se il testo è stato troncato
            if visible_lines:
                visible_lines[-1] = visible_lines[-1][:-3] + "..."

        # Unisci le righe per il canvas
        display_text = "\n".join(visible_lines)
        self.text_canvas_id = self.canvas.create_text(
            text_x, text_y,
            anchor="nw",
            text=display_text,
            fill=self.widgets['widgets_fg_text_color'],
            font=font,
            width=text_width
        )
