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
from PIL import Image, ImageTk
import textwrap

class StorytellingPage(ctk.CTkFrame):
    def __init__(self, master, content, widgets, go_to_chat_callback, *args, **kwargs):
        # Initialize storytelling page frame
        super().__init__(master, fg_color=widgets['window_bg'], *args, **kwargs)
        self.go_to_chat_callback = go_to_chat_callback
        self.content = content
        self.widgets = widgets

        # Setup canvas for background and text
        self.canvas = ctk.CTkCanvas(self, width=400, height=700, bg=widgets['window_bg'], highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        # Load robot image
        self.image_sides_size = 150
        self.robot_story_img = Image.open("./Progettazione/robot.png").resize((self.image_sides_size, self.image_sides_size))
        self.robot_story_ctkimage = ctk.CTkImage(light_image=self.robot_story_img, size=(self.image_sides_size, self.image_sides_size))
        self.robot_label_story = ctk.CTkLabel(self, image=self.robot_story_ctkimage, text="", fg_color=widgets['widgets_bg'])

        # 'Next' button to continue
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

        # Timer and progress bar setup
        self.timer_label = ctk.CTkLabel(self, text="", font=("Comic Sans MS", 14), text_color=widgets['widgets_fg_text_color'])
        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=20, progress_color="#00FF22")

        self.submit_button.place(relx=1.0, rely=1.0, anchor='se', x=-25, y=-25)
        self.timer_label.place(x=25, y=10)
        self.progress_bar.place(x=25, y=40)

        self.canvas.bind("<Configure>", self.on_resize)

        self.timer_running = False
        self.timer_total = 60  # total time in seconds
        self.timer_var = [self.timer_total]  # mutable time tracker

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

    def create_rounded_label(self, canvas, x, y, width, height, radius, border_color, fill_color, text, text_color):
        # Draw a rounded rectangle with optional text (centered)
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
        # Redraw all components upon resizing
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

        # Position robot image at bottom-left
        robot_x = 25 + 10
        robot_y = 75 + (height-100) - self.image_sides_size - 10
        self.robot_label_story.place(x=robot_x, y=robot_y)

        # Text wrapping and layout
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
