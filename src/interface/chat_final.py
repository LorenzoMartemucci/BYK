# from llm.llm_backend import ChatSession
from src.interface.time_bar import TimeBar
from src.interface.chat import Chat
from src.interface.globals import Globals
import random

from src.llm.scorer import Scorer
from src.llm.llm_backend import ChatSession

class ChatFinal(Chat):
    
    def __init__(self, container):
        super().__init__(container)

        self.user_input.bind("<Return>", self._on_enter_pressed)
        self.scorer = Scorer()
        self.llm = ChatSession()
       
        # logic field
        #self.chat_logics = ChatLogics(get_instance_person, self, None) #TODO:Da sistemare 
        self.after(1000, self.add_context_bubble(self.read_quest()))
        self.after(1 ,self.add_time_bar(container))

    def add_time_bar(self, container):
        self.time_bar = TimeBar(container)

    def go_to_fail_page(self):
        from src.interface.fail_page import FailPage
        recap_page = FailPage(self.master)
        recap_page.pack(fill="both", expand=True)
        self.time_bar.destroy_timer()
        self.destroy()

    def go_to_final_request(self):
        from src.interface.final_request_page import FinalRequestPage
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
        self.time_bar.stop_timer()
        if event.state & 0x0001:  # Shift � premuto
            return  # Permetti il normale comportamento di andare a capo
        
        global_instance = Globals()
        ideal_prompt = global_instance.ideal_prompts[global_instance.ideal_prompts['Titolo'] == global_instance.role_story]['Prompt Ideale'].values[0]
        prompt = self.get_message_from_textbox()
        self.user_input.delete("1.0", "end")
        self.add_message_bubble(prompt, is_user=True)
        

        try:
            ideal_role = self.scorer.get_similar_role(global_instance.role_story, prompt)
            if ideal_role is False:
                score = 10
                #self.add_error_bubble(f"Il prompt non è corretto. Riprova!")
                #return "break"
            # prompt minore di 10 caratteri
            elif len(prompt) < 15:
                self.add_error_bubble("Il prompt deve essere lungo almeno 15 caratteri. Riprova!")
                return "break"
            else:
                score = round(self.scorer.get_prompt_score(prompt, ideal_prompt) * 100)

            
            if score >= 65 and score < 90:
                response = self.llm.exec_prompt(prompt)
                self.add_message_bubble("Questo è l'output del tuo prompt: \n" + response, is_user=False)  # self.session.send_message(prompt)
                self.add_recap_bubble(f"Il prompt può essere migliorato. La prossima volta potresti specificare meglio:\n"
                    "Ruolo: 'Agisci come [esperto, docente, consulente, ecc.]'\n"
                    "Compito: 'Devi [fare una cosa specifica]'\n"
                    "Contesto: 'Il contesto è [settore, obiettivo, pubblico, ulteriori dettagli]'\n"
                    "Formato output: '[elenco, paragrafo, codice, tabella, ecc.]'\n"
                    "Vincoli: '[lunghezza, tono, linguaggio, ecc.]'"
            )
                self.add_recap_bubble(f'Un prompt ideale è strutturato come il seguente:\n"{ideal_prompt}')
            elif score >= 90:
                response = self.llm.exec_prompt(prompt)
                self.add_message_bubble("Questo è l'output del tuo prompt: \n" + response, is_user=False)  # self.session.send_message(prompt)
                self.add_recap_bubble(f'Il tuo prompt è perfetto!')
            else:
                self.add_recap_bubble(
                    "Il prompt non è corretto. Ricordati di specificare:\n"
                    "Ruolo: 'Agisci come [esperto, docente, consulente, ecc.]'\n"
                    "Compito: 'Devi [fare una cosa specifica]'\n"
                    "Contesto: 'Il contesto è [settore, obiettivo, pubblico, ulteriori dettagli]'\n"
                    "Formato output: '[elenco, paragrafo, codice, tabella, ecc.]'\n"
                    "Vincoli: '[lunghezza, tono, linguaggio, ecc.]'"
                )

            if  not self.time_bar.is_timedout() and score >=65:
                    score = score + 10 
                    
            def go_to_score_page():
                from src.interface.score_ranking import ScoreRankingPage
                recap_page = ScoreRankingPage(self.master, Globals().user_name, score)
                recap_page.pack(fill="both", expand=True)
                self.time_bar.destroy_timer()
                self.destroy()
            
            self.next_button.configure(
                text='Continua', 
                command=go_to_score_page
                if score >= 65 else self.go_to_fail_page
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
            self.time_bar.destroy_timer()

        return "break"