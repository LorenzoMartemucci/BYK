from src.interface.style import Style
from src.interface.chat import Chat
import customtkinter as ctk

class ChatTutorial(Chat):
    
    def __init__(self, container):
        super().__init__(container)

        # TODO: impostare la logica di chat per il tutorial dalla classe di logica
        self.user_input.bind("<Return>", self._on_enter_pressed)
        
        self.next_button.configure(command=self.go_to_recap_page)
        # logic field

    # function to handle the specific enter of the prompt
    
    def go_to_recap_page(self):
        pass
        # # Distruggi il frame di input
        # self.user_input.destroy()
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

    def _on_enter_pressed(self, event):
        if event.state & 0x0001:  # Shift � premuto
            return  # Permetti il normale comportamento di andare a capo
        self.add_message_bubble(self.get_message_from_textbox(), is_user=True)
        self.user_input.delete("1.0", "end")
        return "break"