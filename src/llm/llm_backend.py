from openai import AzureOpenAI


class ChatSession:
    def __init__(self,
                 endpoint="https://byk-project-resource.cognitiveservices.azure.com/",
                 api_key="C7zq6scqrGBWZQbDZgKRf5dFyPW1gEu6IYpNcYjzKd11mm1iGj16JQQJ99BFACgEuAYXJ3w3AAAAACOGSwgv",
                 deployment="gpt-4.1-mini",
                 system_prompt_path="./rsc/system_prompt.txt",
                 api_version="2024-12-01-preview",
                 max_tokens=800):
        """
        Inizializza la sessione chat con GPT-4.1-mini su Azure OpenAI.
        """
        self.endpoint = endpoint
        self.api_key = api_key
        self.deployment = deployment
        self.api_version = api_version
        self.system_prompt_path = system_prompt_path
        self.max_tokens = max_tokens

        self.client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=self.endpoint,
            api_key=self.api_key
        )

        self.system_prompt = self._load_system_prompt()
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]

    def _load_system_prompt(self):
        """
        Carica il prompt di sistema da file.
        """
        with open(self.system_prompt_path, "r") as file:
            return file.read()

    def send_input(self, user_input: str) -> str:
        """
        Invia un messaggio al modello e restituisce la risposta.
        """
        self.conversation_history.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            messages=self.conversation_history,
            max_completion_tokens=self.max_tokens,
            temperature=0.2,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            model=self.deployment
        )

        ai_message = response.choices[0].message.content
        #self.conversation_history.append({"role": "assistant", "content": ai_message}) #TODO vedere se serve o meno
        return ai_message

    def exec_prompt(self, prompt: str) -> str:
        """
        Esegue un prompt con istruzioni specifiche.
        """
        system_prompt = f'''
            Esegui il seguente prompt: {prompt}. Rispondi in modo mirato, sintetico e non aggiungere spiegazioni superflue.
            Concludi la risposta entro 1024 token.
            Rispondi in italiano.
        '''
        self.conversation_history = [{"role": "system", "content": system_prompt}]
        return self.send_input(prompt)

    def reset_conversation(self):
        """
        Resetta la conversazione mantenendo il system prompt originale.
        """
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]

