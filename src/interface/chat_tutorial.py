from src.interface.chat import Chat

class ChatTutorial(Chat):
    
    def __init__(self, container):
        super().__init__(container)
        self.next_button = ctk.CTkButton(
            self.input_frame,
            text="Prossimo",
            command=self.go_to_recap_page,
            fg_color=Style.WIDGETS_BG,
            text_color=Style.WIDGETS_FG_TEXT_COLOR,
            border_color=Style.WIDGETS_BORDER_COLOR,
            border_width=2,
            corner_radius=15,
            height=70
        )
        self.next_button.pack(side='left', fill='x', expand=True)

        self.next_button.bind("<Button-1>", self.get_message_from_textbox)
        # logic field
    
    def go_to_recap_page(self):

        # def set_send_button_to_next(self):
        # # Distruggi il frame di input
        # self.input_frame.destroy()
        # # Riposiziona il bottone al centro della riga
        # self.next_button.pack_forget()
        # self.next_button.configure(
        #     text="Avanti",
        #     command = self.go_to_next_page, # TODO: Set the command to go to the next page
        #     state="normal",
        #     width=150,  # Set a fixed width for the button
        #     height=90,
        #     font=Style.WIDGETS_FONT,
        # )
        # self.next_button.pack(pady=10, anchor="center")