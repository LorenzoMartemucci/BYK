# from llm.llm_backend import ChatSession
from interface.time_bar import TimeBar
from interface.chat import Chat
from interface.globals import Globals
import customtkinter as ctk
from interface.style import Style
import random

from llm.scorer import Scorer
from llm.llm_backend import ChatSession

class ChatFinal(Chat):
    
    def __init__(self, container):
        super().__init__(container)

        # self.session = ChatSession()
        # TODO: impostare la logica di chat per il tutorial dalla classe di logica
        self.user_input.bind("<Return>", self._on_enter_pressed)
        self.scorer = Scorer()
        self.llm = ChatSession()
        
        self.time_bar = TimeBar(self, timer_total=300)
        
        # logic field
        #self.chat_logics = ChatLogics(get_instance_person, self, None) #TODO:Da sistemare 
        self.after(1000, self.add_context_bubble(self.read_quest()))
        self.chat_timer_label = ctk.CTkLabel(
            self.container,
            text="Tempo rimanente: 180", 
            font=("Comic Sans MS", 14),
            text_color=Style.WIDGETS_FG_TEXT_COLOR,
        )
        self.chat_timer_label.pack()

        self.chat_progress_bar = ctk.CTkProgressBar(
            self.container,
            width=400,
            height=20,
            progress_color=Style.WIDGETS_PROGRESS_BAR_COLOR,
        )
        self.chat_progress_bar.set(1.0)
        self.chat_progress_bar.pack()

        self.timer_var = [300]
        self.timer_running = False
        self.timer_running = True
        self.update_timer(self.timer_var, self.timer_var, None)
    
    def update_timer(self, time_var, total, callback):
        """Update the timer label and progress bar every second."""
        if not self.timer_running:
            return
        minutes = time_var[0] // 60
        seconds = time_var[0] % 60
        self.chat_timer_label.configure(text=f"Tempo rimanente: {minutes:02d}:{seconds:02d}")
        # INVERTI IL PROGRESSO: 1.0 -> pieno, 0.0 -> vuoto
        progress = max(0, min(1, time_var[0] / total))
        self.chat_progress_bar.set(progress)
        if time_var[0] > 0:
            time_var[0] -= 1
            self.after(1000, lambda: self.update_timer(time_var, total, callback))
        else:
            if callback:
                callback()
                
    def stop_timer(self):
        """Stop the timer when _on_enter_pressed function is called."""
        self.timer_running = False
        self.chat_timer_label.configure(text="Tempo scaduto!" if self.timer_var[0] <= 0 else "Timer fermato")
        

    def go_to_fail_page(self):
        from interface.fail_page import FailPage
        recap_page = FailPage(self.master)
        recap_page.pack(fill="both", expand=True)
        self.destroy()

    def go_to_final_request(self):
        from interface.final_request_page import FinalRequestPage
        request_page = FinalRequestPage(self.master)
        request_page.pack(fill="both", expand=True)
        self.destroy()

    def read_quest(self):
        #Inizializziamo le variabili globali
        global_instance= Globals()
        rows = len(global_instance.shown_stories)
        if rows != 0:
            random_number = random.randint(0, rows-1)
            ss_story_local = global_instance.shown_stories.iloc[random_number, 1]
            global_instance.role_story = global_instance.shown_stories.iloc[random_number, 0]
            global_instance.shown_stories.drop(random_number)
            return ss_story_local
        else:
            raise ValueError("Tutte le storie sono già state mostrate.")

    def _on_enter_pressed(self, event):
        if event.state & 0x0001:  # Shift � premuto
            return  # Permetti il normale comportamento di andare a capo
        
        global_instance = Globals()
        ideal_prompt = global_instance.ideal_prompts[global_instance.ideal_prompts['Titolo'] == global_instance.role_story]['Prompt Ideale'].values[0]
        prompt = self.get_message_from_textbox()
        self.user_input.delete("1.0", "end")
        self.add_message_bubble(prompt, is_user=True)
        

        try:
            response = self.llm.exec_prompt(prompt)
            self.add_message_bubble(response, is_user=False)  # self.session.send_message(prompt)
            score = round(self.scorer.get_prompt_score(prompt, ideal_prompt) * 100)

            def go_to_score_page():
                from interface.score_ranking import ScoreRankingPage
                recap_page = ScoreRankingPage(self.master, Globals().user_name, score)
                recap_page.pack(fill="both", expand=True)
                self.destroy()
            
            self.next_button.configure(
                command=go_to_score_page
                if score >= 60 else self.go_to_fail_page
            )
            # Distruggi il frame di input
            self.user_input.destroy()
            # Riposiziona il bottone al centro della riga
            self.next_button.pack(side='left', padx=20, pady=(0, 20), anchor='center')
        except Exception as e:
            self.add_error_bubble(f"Errore durante l'esecuzione del prompt finale: {str(e)}. Clicca il bottone per tornare alla pagina della storia e riprovare il tutorial!")
            self.user_input.destroy()
            self.next_button.configure(text='Torna indietro', command=self.go_to_final_request)
            self.next_button.pack(side='left', padx=20, pady=(0, 20), anchor='center')

        return "break"