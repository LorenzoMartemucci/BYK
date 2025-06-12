from llm.llm_backend import ChatSession
from interface.style import Style
from interface.chat import Chat
import customtkinter as ctk
from logics.chat_logics import ChatLogics


class ChatTutorial(Chat):
    
    def __init__(self, container):
        super().__init__(container)

        self.session = ChatSession()
        # TODO: impostare la logica di chat per il tutorial dalla classe di logica
        self.user_input.bind("<Return>", self._on_enter_pressed)
        
        # logic field
        #self.chat_logics = ChatLogics(get_instance_person, self, None) #TODO:Da sistemare 
        self.next_button.configure(command=self.go_to_final_request)

        self.after(1000, self.add_message_bubble("Ciao sono Robbi. Tu come ti chiami?", is_user=False))
        self.after(1000, self.add_message_bubble("Scrivi il tuo messaggio nel riquadro arancione e premi invio per mandarlo.", is_user=False))

    def go_to_final_request(self):
        from interface.final_request_page import FinalRequestPage
        request_page = FinalRequestPage(self.master)
        request_page.pack(fill="both", expand=True)
        self.destroy()

    def _on_enter_pressed(self, event):
        if event.state & 0x0001:  # Shift � premuto
            return # Permetti il normale comportamento di andare a capo
        
        if self.get_message_from_textbox() == "test":
            # Distruggi il frame di input
            self.user_input.destroy()
            # Riposiziona il bottone al centro della riga
            self.next_button.pack(side='left', padx=20, pady=(0, 20), anchor='center')
            return "break"
        
        prompt = self.get_message_from_textbox()
        self.add_message_bubble(prompt, is_user=True)
        self.user_input.delete("1.0", "end")
        self.add_message_bubble(self.session.send_message(prompt), is_user=False) # self.session.send_message(prompt)
        return "break"