"""
scoring_ranking.py

This module defines the ScoringRankingPage class, a custom Tkinter frame designed to display
user scores and a ranking leaderboard in a stylized card interface. It provides visual feedback
at the end of an activity or game, and includes the option to play again.

Main Features:
- Displays a congratulatory message with the user's score.
- Shows a scrollable, ranked leaderboard sorted by score.
- Renders a card layout with headers, robot avatar, and styled buttons.
- Integrates a 'Play Again' button for restarting the experience.
"""

import customtkinter as ctk
from PIL import Image
from interface.style import Style
from logics.update_scores import read_scores, write_scores

class ScoringRankingPage(ctk.CTkFrame):
    def __init__(self, container, username, score_value):
        super().__init__(container, fg_color=Style.WINDOW_BG)
        # Theme colors and fonts (match your main interface)
        self.widgets_bg = "#FFA764"
        self.widgets_fg_text_color = "#000000"
        self.widgets_border_color = "#BF5200"
        self.widgets_font = ("Comic Sans MS", 12)
        self.table_header_font = ("Comic Sans MS", 11)
        self.score_font = ("Comic Sans MS", 48, "bold")
        self.title_font = ("Comic Sans MS", 25, "bold")
        self.subtitle_font = ("Comic Sans MS", 22)
        self.button_font = ("Comic Sans MS", 13)
        self.title_text = "Congratulazioni!"
        self.title_font = ("Comic Sans MS", 30, "bold")
        self.title_width = 200  # Width for the title label
        self.title_xplacement = 220  # Adjusted for right alignment
        self.title_yplacement = 60  # Adjusted for top placement


        self.image_robot_size = 175
        
        #Da portare in logics.update_scores.py
        self.score_value = score_value
        self.ranking_data = read_scores()   # Read existing scores
        self.username = username  # Example new user
        self.ranking_data.append({"name": self.username, "score": self.score_value})  # Example of adding a new score
        self.ranking_data.sort(key=lambda x: x["score"], reverse=True)  # Sort by score descending
        write_scores(self.ranking_data) # Save updated ranking


        # Background frame
        self.background_frame = ctk.CTkFrame(
            self,
            fg_color=Style.WIDGETS_BG,
            border_color=Style.WIDGETS_BORDER_COLOR,
            border_width=2,
            corner_radius=20,
            width=500,
            height=550
        )
        self.background_frame.pack(fill="both", expand=True, padx=10, pady=10)


            # Header Frame
        self.header_Frame = ctk.CTkFrame(
            self.background_frame,
            height=self.image_robot_size,
            fg_color="#FFFF00"          #"transparent",            
        )
        self.header_Frame.pack(expand=True,fill="both", anchor='n', padx=20, pady=20)

         # Frame per tabella classifica e scrollbar
        self.container_frame = ctk.CTkFrame(
            self.background_frame,
            fg_color='red',
        )
        self.container_frame.pack(expand=True,fill="both", padx=20, pady=20)
        
        # Frame per tabella classifica
        self.center_frame = ctk.CTkFrame(
            self.container_frame,
            fg_color='pink',
        )
        self.center_frame.pack(expand=True,fill="both", side='left', padx=10, pady=20)


           # frame titoli colonna_n.calssificato, username e score
        self.center_header_frame = ctk.CTkFrame(
            self.center_frame,
            fg_color='orange'
            )
        self.center_header_frame.pack(fill='both', expand=True, anchor='n', padx=(0,25) )

        # Frame della scrollbar
        self.scrollbar_frame=ctk.CTkScrollableFrame(
            self.center_frame, 
            fg_color="blue")
        self.scrollbar_frame.pack(expand=True, fill='both')

        # frame per colonna_n.calssificato
        self.n_classified_frame = ctk.CTkFrame(
            self.scrollbar_frame,
            fg_color='gray'
            )
        self.n_classified_frame.pack(fill='y', expand=True, side='left' )

         # frame per nome utente
        self.username_frame = ctk.CTkFrame(
            self.scrollbar_frame,
            fg_color='green'
            )
        self.username_frame.pack(fill='y', expand=True, side='left' )

         # frame per gli score
        self.score_frame = ctk.CTkFrame(
            self.scrollbar_frame,
            fg_color='gray'
            )
        self.score_frame.pack(fill='y', expand=True, side='left' )

        # Frame per bottone
        self.bottom_frame = ctk.CTkFrame(
            self.background_frame,
            fg_color='green'
        )
        self.bottom_frame.pack(expand=True,fill="both", padx=20, pady=20)


        # Robot image (top right, floating)
        robot_img = Image.open("./rsc/robot.png").resize((self.image_robot_size, self.image_robot_size))
        robot_photo = ctk.CTkImage(light_image=robot_img, size=(self.image_robot_size, self.image_robot_size))
        robot_label = ctk.CTkLabel(self.header_Frame, image=robot_photo, text="", fg_color='white')
        robot_label.pack(expand=True, side='left')

        # Top right section: Congratulazioni
        self.top_right_header = ctk.CTkFrame(
            self.header_Frame,
            fg_color='blue',
        )
        self.top_right_header.pack(expand=True, fill='both',side='top')

        # bottom right section: Punteggio, score
        self.bottom_right_header = ctk.CTkFrame(
            self.header_Frame,
            fg_color= 'red'
        )
        self.bottom_right_header.pack(expand=True,fill='both',side='left')

        # Title label
        self.title_label = ctk.CTkLabel(
            self.top_right_header,
            text="Congratulazioni!",
            fg_color="yellow",
        )
        self.title_label.pack(expand=True)

        # Subtitle label
        self.subtitle_label = ctk.CTkLabel(
            self.bottom_right_header,
            text="Punteggio:",
            fg_color="#00F000",
        )
        self.subtitle_label.pack(expand=True, side='left')

        # Score label
        self.score_label = ctk.CTkLabel(
            self.bottom_right_header,
            text=str(self.score_value),
            text_color="#112E4B",
            fg_color="#FFFFFF",
        )
        self.score_label.pack(expand=True, side='left')
        
        # Create header labels
        # Classifica header
        ctk.CTkLabel(
            self.center_header_frame, 
            text="Classifica", 
            anchor="center", 
            fg_color="red"
        ).pack(fill='x',expand=True, side='left')
        
        # User header
        ctk.CTkLabel(
            self.center_header_frame, 
            text="Utente", 
            anchor="center", 
            fg_color="blue"
        ).pack(fill='x',expand=True, side='left')

        # Score header
        ctk.CTkLabel(
            self.center_header_frame, 
            text="Punteggio", 
            anchor="center", 
            fg_color="yellow"
        ).pack(fill='x',expand=True, side='left')     



        # # Create a frame inside the canvas
        # table_body = tk.Frame(table_canvas)
        # table_canvas.create_window((0, 0), window=table_body, anchor="nw")

        # #table_canvas.configure(yscrollcommand=scrollbar.set)

        # def on_frame_configure(event):
        #     table_canvas.configure(scrollregion=table_canvas.bbox("all"))

        # table_body.bind("<Configure>", on_frame_configure)

        # # Draw vertical lines
        # table_canvas.create_line(90, 0, 90, body_height, fill=self.widgets_fg_text_color, width=1)
        # table_canvas.create_line(270, 0, 270, body_height, fill=self.widgets_fg_text_color, width=1)
        # # Draw horizontal line under headers
        # table_canvas.create_line(0, 0, table_width, 0, fill=self.widgets_fg_text_color, width=1)

        # # Sort and assign ranks
        # row_height = 38
        # sorted_ranking= self.ranking_data
        # for idx, entry in enumerate(sorted_ranking, start=1):
        #     y = (idx - 1) * row_height + 10
        #     tk.Label(table_body, text=str(idx), font=self.widgets_font, bg=self.widgets_bg, fg=self.widgets_fg_text_color, width=8, anchor="center").place(x=0, y=y, width=90, height=row_height)
        #     tk.Label(table_body, text=entry["name"], font=self.widgets_font, bg=self.widgets_bg, fg=self.widgets_fg_text_color, width=20, anchor="center").place(x=90, y=y, width=180, height=row_height)
        #     tk.Label(table_body, text=str(entry["score"]), font=self.widgets_font, bg=self.widgets_bg, fg=self.widgets_fg_text_color, width=8, anchor="center").place(x=270, y=y, width=90, height=row_height)

        # # Optionally, set a minimum size for the table_body frame
        # table_body.config(width=table_width-15, height=max(body_height, len(sorted_ranking)*row_height+10))


        # Bottom button
        play_again_button = ctk.CTkButton(
            self.bottom_frame,
            text="Giochiamo di nuovo!",
            border_width=2,
            corner_radius=15,
            #command="go to start page"  # inserire il comando per tornare alla pagina iniziale
        )
        play_again_button.pack(fill='both',expand=True )



    
    # score_prova=[np.random.randint(60, 101),np.random.randint(0, 60), None, 23.45, -20, 130]
    # page = ScoringRankingPage(root,username=new_user="Giocatore"+str(len(read_scores()) + 1), score_value=np.random.randint(60, 101))
    