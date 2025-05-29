import tkinter as tk
import tkinter.font as tkFont
import customtkinter as ctk
from PIL import Image, ImageTk
import textwrap

#%% Setup
with open("./Progettazione/storia.txt", "r") as story:
    content = story.read()

widgets_bg = "#FFA764"
widgets_fg_text_color = "#000000"
widgets_border_color = "#BF5200"
widgets_font = ("Comic Sans MS", 12)
window_bg = "#FFE2CC"

ctk.set_appearance_mode("light")
root = ctk.CTk(fg_color=window_bg)
root.geometry("600x400")
root.resizable(False, False)
root.minsize(600, 400)
root.configure(bg=window_bg)

container = ctk.CTkFrame(root, fg_color=window_bg)
container.pack(fill="both", expand=True)

user_data = []

#%% --- Start Page ---
start_page = ctk.CTkFrame(container, fg_color=window_bg)
start_page.pack(fill="both", expand=True)

start_inner_frame = ctk.CTkFrame(start_page, fg_color=window_bg)
start_inner_frame.place(relx=0.5, rely=0.5, anchor="center")

# Layout orizzontale
horizontal_frame = ctk.CTkFrame(start_inner_frame, fg_color=window_bg)
horizontal_frame.pack(padx=20, pady=20)

# Robot a sinistra (più in basso)
robot_img = Image.open("./Progettazione/robot.png").resize((180, 180))
robot_photo = ImageTk.PhotoImage(robot_img)
robot_label = ctk.CTkLabel(horizontal_frame, image=robot_photo, text="", fg_color="transparent")
robot_label.pack(side="left", padx=10, pady=(20, 0))  # Abbassato leggermente

# Riquadro a destra
box_frame = ctk.CTkFrame(horizontal_frame, fg_color=widgets_bg, border_color=widgets_border_color, border_width=2, corner_radius=15)
box_frame.pack(side="left", padx=10, pady=10)

username_label = ctk.CTkLabel(box_frame, text="COME TI CHIAMI?", font=("Comic Sans MS", 18, "bold"), text_color=widgets_fg_text_color, fg_color="transparent")
username_label.pack(pady=(20, 10), padx=20)

username_entry = ctk.CTkEntry(box_frame, placeholder_text="Scrivi qui il tuo nome", font=widgets_font, width=200)
username_entry.pack(pady=5, padx=20)

time_remaining = [120] 
chat_time_remaining = [180]

def go_to_story():
    user_data.append(username_entry.get())
    start_page.pack_forget()
    root.geometry("550x800")
    root.resizable(True, True)
    root.minsize(400, 600)
    storytelling.pack(fill="both", expand=True)
    time_remaining[0] = 120
    update_generic_timer(time_remaining, timer_label, progress_bar, 120, None)

def go_to_chat():
    storytelling.pack_forget()
    chat_page.pack(fill="both", expand=True)
    chat_time_remaining[0] = 180
    update_generic_timer(chat_time_remaining, chat_timer_label, chat_progress_bar, 180, None)

start_button = ctk.CTkButton(
    box_frame,
    text="GIOCHIAMO",
    command=go_to_story,
    fg_color="#FFFFFF",
    text_color=widgets_fg_text_color,
    border_color=widgets_border_color,
    border_width=2,
    corner_radius=15,
    font=("Comic Sans MS", 14, "bold"),
    width=180,
    height=50
)
start_button.pack(pady=20)

#%% --- Storytelling Page ---
storytelling = ctk.CTkFrame(container, fg_color=window_bg)

canvas = ctk.CTkCanvas(storytelling, width=400, height=700, bg=window_bg, highlightthickness=0)
canvas.pack(fill='both', expand=True)

image_sides_size = 150
robot_story_img = Image.open("./Progettazione/robot.png").resize((image_sides_size, image_sides_size))
robot_story_photo = ImageTk.PhotoImage(robot_story_img)
robot_label_story = ctk.CTkLabel(storytelling, image=robot_story_photo, text="", fg_color=widgets_bg)

submit_button = ctk.CTkButton(
    storytelling,
    text='Prossimo',
    command=go_to_chat,
    fg_color=widgets_bg,
    text_color=widgets_fg_text_color,
    border_color=widgets_border_color,
    border_width=2,
    corner_radius=15,
    font=widgets_font,
    width=160,
    height=60
)

timer_label = ctk.CTkLabel(storytelling, text="", font=("Comic Sans MS", 14), text_color=widgets_fg_text_color)
progress_bar = ctk.CTkProgressBar(storytelling, width=400, height=20, progress_color="#00FF22")

def update_generic_timer(time_var, label, progress, total, callback):
    minutes = time_var[0] // 60
    seconds = time_var[0] % 60
    label.configure(text=f"Tempo rimanente: {minutes:02}:{seconds:02}")
    progress.set(time_var[0] / total)
    if time_var[0] > 0:
        time_var[0] -= 1
        root.after(1000, lambda: update_generic_timer(time_var, label, progress, total, callback))
    else:
        if callback:
            callback()

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

    progress_bar.configure(width=width - 50)
    progress_bar.place(x=25, y=40)
    timer_label.place(x=25, y=10)

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

    robot_x = 25 + 10
    robot_y = 75 + (height-100) - image_sides_size - 10
    robot_label_story.place(x=robot_x, y=robot_y)

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

#%% --- Interactive Chat Page ---
chat_page = ctk.CTkFrame(container, fg_color=window_bg)

# Timer e barra in alto (dinamici)
chat_timer_label = ctk.CTkLabel(chat_page, text="Tempo rimanente: 180", font=("Comic Sans MS", 14), text_color=widgets_fg_text_color)
chat_timer_label.place(x=25, y=10)

chat_progress_bar = ctk.CTkProgressBar(chat_page, width=400, height=20, progress_color="#00FF22")
chat_progress_bar.set(1.0)
chat_progress_bar.place(x=25, y=40)

def on_chat_resize(event):
    new_width = max(100, event.width - 50)  # imposta una larghezza minima
    chat_progress_bar.configure(width=new_width)
chat_page.bind("<Configure>", on_chat_resize)

# Frame centrale per messaggi e robot
center_frame = ctk.CTkFrame(chat_page, fg_color=window_bg)
center_frame.pack(fill="both", expand=True, padx=20, pady=(70, 20))  # spazio sopra per timer

# Canvas per i messaggi (fumetti)
chat_canvas = tk.Canvas(center_frame, bg=window_bg, highlightthickness=0, bd=0)
chat_canvas.pack(side="left", fill="both", expand=True)

chat_scrollbar = tk.Scrollbar(center_frame, orient="vertical", command=chat_canvas.yview)
chat_scrollbar.pack(side="right", fill="y")

chat_frame = tk.Frame(chat_canvas, bg=window_bg)
chat_canvas.create_window((0, 0), window=chat_frame, anchor="nw")
chat_canvas.configure(yscrollcommand=chat_scrollbar.set)

def on_frame_configure(event):
    chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
chat_frame.bind("<Configure>", on_frame_configure)

# Funzione per aggiungere messaggi a fumetto con coda
def add_message(text, sender="user"):
    bubble_color = "#FFA764" if sender == "user" else "#AEE4FF"
    anchor = "e" if sender == "user" else "w"
    justify = "right" if sender == "user" else "left"
    padx = (60, 10) if sender == "user" else (10, 60)
    # Bubble frame
    bubble_frame = tk.Frame(chat_frame, bg=window_bg)
    bubble_frame.pack(anchor=anchor, pady=8, padx=padx, fill="x")
    # Bubble label
    bubble = ctk.CTkLabel(
        bubble_frame,
        text=text,
        font=widgets_font,
        text_color=widgets_fg_text_color,
        fg_color=bubble_color,
        corner_radius=18,
        anchor="w",
        justify=justify,
        wraplength=260,
        width=260,
        height=50
    )
    bubble.pack(side="top", anchor=anchor)
    # Bubble tail (triangolo)
    tail_canvas = tk.Canvas(bubble_frame, width=20, height=15, bg=window_bg, highlightthickness=0)
    if sender == "user":
        tail_canvas.pack(side="right", anchor="e")
        tail_canvas.create_polygon(20, 0, 0, 7, 20, 15, fill=bubble_color, outline=bubble_color)
    else:
        tail_canvas.pack(side="left", anchor="w")
        tail_canvas.create_polygon(0, 0, 20, 7, 0, 15, fill=bubble_color, outline=bubble_color)

# Input in basso (stile come da esempio)
input_outer_frame = ctk.CTkFrame(
    chat_page,
    fg_color=window_bg,
    border_width=0,
    corner_radius=0
)
input_outer_frame.pack(fill="x", padx=20, pady=(0, 20), side="bottom")

input_frame = ctk.CTkFrame(
    input_outer_frame,
    fg_color=widgets_bg,
    border_color=widgets_border_color,
    border_width=2,
    corner_radius=15
)
input_frame.pack(side="left", fill="x", expand=True, padx=(0, 20))

# Calcola l'altezza per 3 righe
font = widgets_font
f = tkFont.Font(font=font)
line_height = f.metrics("linespace") + 2
fixed_height = line_height * 3 + 12  # padding

user_input = ctk.CTkTextbox(
    input_frame,
    font=widgets_font,
    fg_color=widgets_bg,
    text_color=widgets_fg_text_color,
    border_color=widgets_border_color,
    border_width=0,
    corner_radius=15,
    width=320,
    height=fixed_height
)
user_input.pack(side="left", fill="both", expand=True, padx=10, pady=(8, 8))
user_input.insert("1.0", "")

def send_message():
    msg = user_input.get("1.0", "end-1c").strip()
    if msg:
        add_message(msg, sender="user")
        user_input.delete("1.0", "end")
        root.after(500, lambda: add_message("Risposta del robot a: " + msg, sender="bot"))
        # Scroll automatico in fondo
        chat_canvas.yview_moveto(1.0)

def send_message_event(event=None):
    if event and (event.state & 0x0001):  # Shift premuto
        return
    send_message()
    return "break"

user_input.bind("<Return>", send_message_event)
user_input.bind("<Shift-Return>", lambda e: None)  # Permetti newline con Shift+Invio


send_button = ctk.CTkButton(
    input_outer_frame,
    text="Invio",
    command=send_message,
    fg_color=widgets_bg,
    text_color=widgets_fg_text_color,
    border_color=widgets_border_color,
    border_width=2,
    corner_radius=15,
    width=90,
    height=40
)
send_button.pack(side="right", padx=(0, 0), pady=10)

# Robot che sbuca dalla chat (solo testa e mano, immagine PNG trasparente consigliata)
robot_head_img = Image.open("./Progettazione/robot.png").resize((110, 90))
robot_head_photo = ImageTk.PhotoImage(robot_head_img)
robot_head_label = ctk.CTkLabel(chat_page, image=robot_head_photo, text="", fg_color="transparent")
robot_head_label.place(x=0, rely=1.0, anchor="sw", y=-input_frame.winfo_reqheight() + 30)


root.mainloop()
