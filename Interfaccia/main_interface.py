import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import textwrap

#%% Prima pagina
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
root.minsize(550, 800)
root.configure(bg=window_bg)

# Container frame for all pages
container = ctk.CTkFrame(root, fg_color=window_bg)
container.pack(fill="both", expand=True)

# --- First page frame ---
storytelling = ctk.CTkFrame(container, fg_color=window_bg)
storytelling.pack(fill="both", expand=True)

canvas = ctk.CTkCanvas(storytelling, width=400, height=700, bg=window_bg, highlightthickness=0)
canvas.pack(fill='both', expand=True)

# Load robot image
image_sides_size = 150
robot_img = Image.open("./Progettazione/robot.png").resize((image_sides_size, image_sides_size))
robot_photo = ImageTk.PhotoImage(robot_img)
robot_label = ctk.CTkLabel(storytelling, image=robot_photo, text="", fg_color=widgets_bg)

submit_button = ctk.CTkButton(
    storytelling,
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

# Timer variables
time_remaining = 120  # 2 minutes in seconds
timer_label = ctk.CTkLabel(storytelling, text="", font=("Comic Sans MS", 14), text_color=widgets_fg_text_color)
progress_bar = ctk.CTkProgressBar(storytelling, width=400, height=20, progress_color="#00FF22")

def update_timer():
    global time_remaining
    minutes = time_remaining // 60
    seconds = time_remaining % 60
    timer_label.configure(text=f"Tempo rimanente: {minutes:02}:{seconds:02}")
    progress_bar.set(time_remaining / 120)
    if time_remaining > 0:
        time_remaining -= 1
        root.after(1000, update_timer)

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

    # Update progress bar and timer position
    progress_bar.configure(width=width - 50)
    progress_bar.place(x=25, y=40)
    timer_label.place(x=25, y=10)

    # Redraw the story box
    canvas.delete("all")
    create_rounded_label(
        canvas,
        x=25, y=75,
        width=width-50, height=height-100,
        radius=20,
        border_color=widgets_border_color,
        fill_color=widgets_bg,
        text="",
        text_color=widgets_fg_text_color
    )

    # Place the robot image
    robot_x = 25 + 10
    robot_y = 75 + (height-100) - image_sides_size - 10
    robot_label.place(x=robot_x, y=robot_y)

    # Text placement
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
    robot_bottom = robot_y + image_sides_size
    robot_right = robot_x + image_sides_size

    font = (widgets_font[0], widgets_font[1])
    line_height = 22

    lines = []
    for paragraph in content.split('\n'):
        wrapped = textwrap.wrap(paragraph, width=60)
        if not wrapped:
            lines.append("")
        else:
            lines.extend(wrapped)

    y = text_y
    for line in lines:
        if robot_top < y < robot_bottom:
            indent = robot_right - text_x + 10
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

canvas.bind("<Configure>", on_resize)
submit_button.place(relx=1.0, rely=1.0, anchor='se', x=-25, y=-25)
timer_label.place(x=25, y=10)
progress_bar.place(x=25, y=40)
update_timer()

root.mainloop()