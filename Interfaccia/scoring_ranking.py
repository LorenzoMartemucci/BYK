import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

# Theme colors and fonts (match your main interface)
widgets_bg = "#FFA764"
widgets_fg_text_color = "#000000"
widgets_border_color = "#BF5200"
widgets_font = ("Comic Sans MS", 12)
window_bg = "#FFE2CC"
table_header_font = ("Comic Sans MS", 11)
score_font = ("Comic Sans MS", 64, "bold")
title_font = ("Comic Sans MS", 28, "bold")
subtitle_font = ("Comic Sans MS", 22)
button_font = ("Comic Sans MS", 13)

ctk.set_appearance_mode("light")
root = ctk.CTk(fg_color=window_bg)
root.minsize(600, 700)
root.title("Score & Ranking")

# Main frame
main_frame = ctk.CTkFrame(root, fg_color=window_bg)
main_frame.pack(fill="both", expand=True)

# Card-like frame
card_frame = ctk.CTkFrame(
    main_frame,
    fg_color=widgets_bg,
    border_color=widgets_border_color,
    border_width=2,
    corner_radius=20,
    width=500,
    height=550
)
card_frame.place(relx=0.5, rely=0.45, anchor="center")

# Robot image (top right, floating)
image_sides_size = 175
robot_img = Image.open("./Progettazione/robot.png").resize((image_sides_size, image_sides_size))
robot_photo = ctk.CTkImage(light_image=robot_img, size=(image_sides_size, image_sides_size))
robot_label = ctk.CTkLabel(card_frame, image=robot_photo, text="", fg_color="transparent")
robot_label.place(x=25, y=20)

# Top section: Title, Score (to the right of the robot, aligned right)
title_label = ctk.CTkLabel(
    card_frame,
    text="Congratulazioni!",
    font=title_font,
    text_color="#FFFFFF",
    fg_color="transparent",
    anchor="e",  # align text to the right
    width=250
)
title_label.place(x=220, y=30)  # Adjust x to be to the right of the robot

subtitle_label = ctk.CTkLabel(
    card_frame,
    text="Punteggio:",
    font=subtitle_font,
    text_color="#FFFFFF",
    fg_color="transparent",
    anchor="e",  # align text to the right
    width=250
)
subtitle_label.place(x=220, y=75)

score_value = 83  # Replace with your actual score variable
score_label = ctk.CTkLabel(
    card_frame,
    text=str(score_value),
    font=score_font,
    text_color="#FFFFFF",
    fg_color="transparent",
    anchor="e",  # align text to the right
    width=250
)
score_label.place(x=220, y=110)

# Table section
table_y = 200
table_height = 270
table_width = 450
table_x = 25

table_frame = ctk.CTkFrame(card_frame, fg_color=widgets_bg, width=table_width, height=table_height)
table_frame.place(x=table_x, y=table_y)

# Table headers
header_height = 30
header_frame = ctk.CTkFrame(table_frame, fg_color=widgets_bg, width=table_width, height=header_height)
header_frame.place(x=0, y=0)

ctk.CTkLabel(
    header_frame, text="Classifica", font=table_header_font, text_color=widgets_fg_text_color, width=90, anchor="center", fg_color="transparent"
).place(x=0, y=5)
ctk.CTkLabel(
    header_frame, text="Utente", font=table_header_font, text_color=widgets_fg_text_color, width=180, anchor="center", fg_color="transparent"
).place(x=90, y=5)
ctk.CTkLabel(
    header_frame, text="Punteggio", font=table_header_font, text_color=widgets_fg_text_color, width=90, anchor="center", fg_color="transparent"
).place(x=270, y=5)

# Table lines (vertical and horizontal)
table_canvas = tk.Canvas(
    table_frame,
    width=table_width,
    height=table_height - header_height,
    bg=widgets_bg,
    highlightthickness=0,
)
table_canvas.place(x=0, y=header_height)

# Draw vertical lines
table_canvas.create_line(90, 0, 90, table_height - header_height, fill=widgets_fg_text_color, width=1)
table_canvas.create_line(270, 0, 270, table_height - header_height, fill=widgets_fg_text_color, width=1)
# Draw horizontal line under headers
table_canvas.create_line(0, 0, table_width, 0, fill=widgets_fg_text_color, width=1)

# Example ranking data
ranking_data = [
    {"name": "Alice", "score": 95},
    {"name": "Bob", "score": 90},
    {"name": "Carlo", "score": 88},
    {"name": "Dario", "score": 83},
    {"name": "Elena", "score": 80},
]

# Sort and assign ranks
ranking_data = sorted(ranking_data, key=lambda x: x["score"], reverse=True)
row_height = 38
for idx, entry in enumerate(ranking_data, start=1):
    y = 10 + idx * row_height
    table_canvas.create_text(45, y, text=str(idx), font=widgets_font, fill=widgets_fg_text_color)
    table_canvas.create_text(180, y, text=entry["name"], font=widgets_font, fill=widgets_fg_text_color)
    table_canvas.create_text(315, y, text=str(entry["score"]), font=widgets_font, fill=widgets_fg_text_color)

# Bottom button
play_again_button = ctk.CTkButton(
    main_frame,
    text="Giochiamo di nuovo!",
    font=button_font,
    fg_color=widgets_bg,
    text_color=widgets_fg_text_color,
    border_color=widgets_border_color,
    border_width=2,
    corner_radius=15,
    width=250,
    height=50,
)
play_again_button.place(relx=0.5, rely=0.93, anchor="center")

root.mainloop()