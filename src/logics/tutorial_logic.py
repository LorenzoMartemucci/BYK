from src.interface.globals import Globals
from src.logics.fsm import FSM
from src.llm.llm_backend import ChatSession
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
import json



class TutorialLogic:
    def __init__(self):
        """
        Initialize the Robby instance with a finite state machine and a chat session.
        
        Args:
            fsm_file (str): Path to the finite state machine definition file.
            llm_session (ChatSession): An instance of ChatSession for handling LLM interactions.
        """
        self.fsm = FSM()
        self.llm_session = ChatSession()
        self.user_data = {}

    def exec_prompt(self, prompt: str) -> str:
        """
        Execute a prompt using the LLM session and return the response.
        
        Args:
            prompt (str): The prompt to be sent to the LLM.
        
        Returns:
            str: The response from the LLM.
        """
        return self.llm_session.exec_prompt(prompt)
    
    def process_input(self, user_input: str) -> str:
        """
        Process user input through the FSM and return the response from the LLM.
        
        Args:
            user_input (str): The input string from the user.
        
        Returns:
            str: The response from the LLM based on the current FSM state.
        """

        current_state = self.fsm.get_current_state()
        
        
        prompt = f"""

        Sei nello stato: "{current_state}".
        Classifica l'input in base alla coerenza con le informazioni precedenti e alla rilevanza per lo stato attuale.
        Devi determinare se l'input è valido o non valido in questo contesto.
        

        Input utente : "{user_input}"
        
        Risposte precedenti: {json.dumps(self.user_data, ensure_ascii=False)}
        
        Se {current_state} è "get_task" classifica come "invalid" un compito non testuale. 
        Se {current_state} è "get_context" classifica come "invalid" il contesto se troppo generico o ambiguo. 
        Se {current_state} è "get_output_format" e l'utente fornisce un formato non testuale classificalo come invalid.
        
        Rispondi esclusivamente con questa struttura:
        
        {{
                "label": "invalid"|"valid",
                "message": "motivazione ed esempi solo se label è invalid"
        }}
        

        """.strip()



        response = self.llm_session.send_input(prompt)
       
        parsed = json.loads(response)
        label = parsed.get("label")

        if label == "valid":
            self.user_data[self.fsm.get_current_state()] = user_input
            self.fsm.next_step(label)
            return self.fsm.state_questions.get(self.fsm.get_current_state(), "")
        elif label == "invalid":
            self.fsm.next_step(label)
            return parsed.get("message", "")
        else:
            raise ValueError(f"Unexpected label: {label}. Expected 'valid' or 'invalid'.")
    
    def start_game(self) -> str:
        """
        Start the game by returning the first question.
        Returns:
            str: The first question from the FSM.
        """
        return self.fsm.state_questions.get("get_name")
    
    def is_tutorial_completed(self) -> bool:
        """
        Check if the tutorial is completed by verifying if the FSM is in an accepting state.
        
        Returns:
            bool: True if the FSM is in an accepting state, False otherwise.
        """
        return self.fsm.is_in_accepting_state()

    def prompt_recap(self) -> str:

        ''' This method returns the prompt recap.'''
        label_map = {
            "get_role": "RUOLO",
            "get_task": "COMPITO",
            "get_context": "CONTESTO",
            "get_output_format": "FORMATO OUTPUT",
            "get_constraints": "VINCOLI"
        }


        recap = []
        user_name = self.user_data['get_name']
        Globals().user_name = user_name
        for key in ["get_role", "get_task", "get_context", "get_output_format", "get_constraints"]:
            value = self.user_data.get(key, "[Non specificato]")
            label = label_map.get(key, key)
            recap.append(f"- {label}: {value}")

        return "\n".join(recap)

    def rewrite_prompt(self) -> str:
        recap_text = self.prompt_recap()

        system_prompt = '''
            Sei un assistente che riceve un riepilogo di risposte da un utente.
            Il tuo compito è trasformare queste informazioni in un prompt chiaro
            coerente e pronto all'esecuzione da parte di un modello di linguaggio
            '''
    

        user_prompt = f"""
            Ecco il riepilogo da trasformare in un prompt:

            {recap_text}

            Riscrivi il prompt in maniera discorsiva utilizzando SOLO le informazioni del riepilogo.
            Rispondi in italiano. 

            """
        
        self.llm_session.conversation_history = []
        
        self.llm_session.conversation_history = [SystemMessage(content=system_prompt)]
        response = self.llm_session.send_input(user_prompt)
        
        return response