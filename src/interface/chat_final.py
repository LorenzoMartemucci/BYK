# from llm.llm_backend import ChatSession
from interface.style import Style
from interface.chat import Chat
import customtkinter as ctk
from logics.chat_logics import ChatLogics
from interface.globals import Globals
import random

class ChatFinal(Chat):
    
    def __init__(self, container):
        super().__init__(container)

        # self.session = ChatSession()
        # TODO: impostare la logica di chat per il tutorial dalla classe di logica
        self.user_input.bind("<Return>", self._on_enter_pressed)
        
        # logic field
        #self.chat_logics = ChatLogics(get_instance_person, self, None) #TODO:Da sistemare 
        self.after(1000, self.add_message_bubble(self.read_quest(), is_user=False))

    def go_to_final_page(self):
        # from interface.final_page import FinalPage
        # recap_page = FinalPage(self.master)
        # recap_page.pack(fill="both", expand=True)
        # self.destroy()
        pass

    def go_to_fail_page(self):
        from interface.fail_page import FailPage
        recap_page = FailPage(self.master)
        recap_page.pack(fill="both", expand=True)
        self.destroy()

    def read_quest(self):
        #Inizializziamo le variabili globali
        global_instance= Globals()
        rows= len(global_instance.shown_stories)
        if rows != 0:
            random_number = random.randint(0, rows-1)
            ss_story_local= global_instance.shown_stories.iloc[random_number, 1]
            global_instance.role_story = global_instance.shown_stories.iloc[random_number, 0]
            global_instance.shown_stories.drop(random_number)
            return ss_story_local
        else:
            raise ValueError("Tutte le storie sono già state mostrate.")

    def _on_enter_pressed(self, event):
        if event.state & 0x0001:  # Shift � premuto
            return  # Permetti il normale comportamento di andare a capo
        
        if self.get_message_from_textbox() == "test":
                score = 59
                if score > 60:
                    self.next_button.configure(command=self.go_to_final_page)
                    # Distruggi il frame di input
                    self.user_input.destroy()
                    # Riposiziona il bottone al centro della riga
                    self.next_button.pack(side='left', padx=20, pady=(0, 20), anchor='center')
                else:
                    self.next_button.configure(command=self.go_to_fail_page)
                    # Distruggi il frame di input
                    self.user_input.destroy()
                    # Riposiziona il bottone al centro della riga
                    self.next_button.pack(side='left', padx=20, pady=(0, 20), anchor='center')

        prompt = self.get_message_from_textbox()
        self.add_message_bubble(prompt, is_user=True)
        self.user_input.delete("1.0", "end")
        #self.add_message_bubble(self.session.send_message(prompt), is_user=False) # self.session.send_message(prompt)
        # return "break"