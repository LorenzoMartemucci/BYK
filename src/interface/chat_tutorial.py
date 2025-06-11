from interface.style import Style
from interface.chat import Chat
import customtkinter as ctk
from logics.chat_logics import ChatLogics

class ChatTutorial(Chat):
    
    def __init__(self, container):
        super().__init__(container)

        # TODO: impostare la logica di chat per il tutorial dalla classe di logica
        self.user_input.bind("<Return>", self._on_enter_pressed)
        
        self.next_button.configure(command=self.go_to_recap_page)
        # logic field
        #self.chat_logics = ChatLogics(get_instance_person, self, None) #TODO:Da sistemare 

    def go_to_recap_page(self):
        from interface.recap_page import RecapPage
        recap_page = RecapPage(self.master)
        recap_page.pack(fill="both", expand=True)
        self.destroy()


    def _on_enter_pressed(self, event):
        if event.state & 0x0001:  # Shift � premuto
            return  # Permetti il normale comportamento di andare a capo
        
        if self.get_message_from_textbox() == "test":
                # Distruggi il frame di input
                self.user_input.destroy()
                # Riposiziona il bottone al centro della riga
                self.next_button.pack(side='left', padx=20, pady=(0, 20), anchor='center')

        self.add_message_bubble(self.get_message_from_textbox(), is_user=True)
        self.user_input.delete("1.0", "end")
        return "break"