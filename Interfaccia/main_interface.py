import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import textwrap

# Importing the story of the robot
with open("./Progettazione/storia.txt", "r") as story:
    content = story.read()

# Environment colors
widgets_bg = "#FFA764"
widgets_fg_text_color = "#000000"
widgets_border_color = "#BF5200"
widgets_font = ("Comic Sans MS", 12)
window_bg = "#FFE2CC"

ctk.set_appearance_mode("light")
root = ctk.CTk(fg_color=window_bg)
root.minsize(550, 750)
root.configure(bg=window_bg)
canvas = ctk.CTkCanvas(root, width=400, height=700, bg=window_bg, highlightthickness=0)

# Load robot image
image_sides_size = 150
robot_img = Image.open("./Progettazione/robot.png").resize((image_sides_size, image_sides_size))
robot_photo = ImageTk.PhotoImage(robot_img)
robot_label = ctk.CTkLabel(canvas, image=robot_photo, text="", fg_color=widgets_bg)

submit_button = ctk.CTkButton(
    canvas,
    text='Prossimo',
    fg_color=widgets_bg,
    text_color=widgets_fg_text_color,
    border_color=widgets_border_color,
    border_width=2,
    corner_radius=15,
    font=widgets_font,
    width=160,
    height=60
)

def create_rounded_label(canvas, x, y, width, height, radius, border_color, fill_color, text, text_color):
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

def on_resize(event):
    width = event.width
    bottom_padding = 25
    button_height = 40
    button_padding = 20
    height = event.height - bottom_padding - button_height - button_padding

    # Draw the rounded storytelling box
    canvas.delete("all")
    create_rounded_label(
        canvas,
        x=25, y=25,
        width=width-50, height=height-50,
        radius=20,
        border_color=widgets_border_color,
        fill_color=widgets_bg,
        text="",  # We'll draw text separately
        text_color=widgets_fg_text_color
    )

    # Place the robot image at the bottom-left inside the storytelling box
    robot_x = 25 + 10
    robot_y = 25 + (height-50) - image_sides_size - 10
    robot_label.place(x=robot_x, y=robot_y)

    # Text placement and wrapping
    box_x = 25
    box_y = 25
    box_width = width - 50
    box_height = height - 50
    text_padding_x = 20
    text_padding_y = 20
    text_x = box_x + text_padding_x
    text_y = box_y + text_padding_y
    text_width = box_width - 2 * text_padding_x

    # Calculate the y position where the robot starts
    robot_top = robot_y
    robot_bottom = robot_y + image_sides_size
    robot_right = robot_x + image_sides_size

    # Split content into lines that fit the width
    font = (widgets_font[0], widgets_font[1])
    # Estimate line height (not exact, but works for most fonts)
    line_height = 22

    # Split text into lines
    lines = []
    for paragraph in content.split('\n'):
        wrapped = textwrap.wrap(paragraph, width=60)  # Adjust width as needed
        if not wrapped:
            lines.append("")
        else:
            lines.extend(wrapped)

    # Draw each line, indenting if it would overlap the robot
    y = text_y
    for line in lines:
        # If the current y is within the robot's vertical range, indent the line
        if robot_top < y < robot_bottom:
            indent = robot_right - text_x + 10  # 10px extra padding
            canvas.create_text(
                text_x + indent, y,
                anchor="nw",
                text=line,
                fill=widgets_fg_text_color,
                font=widgets_font,
                width=text_width - indent
            )
        else:
            canvas.create_text(
                text_x, y,
                anchor="nw",
                text=line,
                fill=widgets_fg_text_color,
                font=widgets_font,
                width=text_width
            )
        y += line_height

canvas.pack(fill='both', expand=True)
canvas.bind("<Configure>", on_resize)
submit_button.place(relx=1.0, rely=1.0, anchor='se', x=-25, y=-25)

root.mainloop()
