from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
import re


class ChatSession:
    def __init__(self, endpoint = "https://byk-project-resource.services.ai.azure.com/models", 
        api_key = "C7zq6scqrGBWZQbDZgKRf5dFyPW1gEu6IYpNcYjzKd11mm1iGj16JQQJ99BFACgEuAYXJ3w3AAAAACOGSwgv",
        model_name = "DeepSeek-R1-0528-2", system_prompt_path = "./rsc/system_prompt.txt", max_tokens=2048):

        """"
        Initialize the chat session with Azure DeepSeek model.
        Args:
            endpoint (str): The Azure endpoint for the model.
            api_key (str): The API key for authentication.
            model_name (str): The name of the model to use.
            system_prompt_path (str): Path to the system prompt file.
            max_tokens (int): Maximum number of tokens for the response.
        """
        
        self.endpoint = endpoint
        self.api_key = api_key
        self.model_name = model_name
        self.system_prompt_path = system_prompt_path
        self.max_tokens = max_tokens

        # Set up API client
        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key),
            api_version="2024-05-01-preview"
        )

        # Load system prompt
        self.system_prompt = self._load_system_prompt()

        # Initialize conversation history
        self.conversation_history = [SystemMessage(content=self.system_prompt)]

    def _load_system_prompt(self):
        """
        Loads the system prompt from the file.
        """

        with open(self.system_prompt_path, "r") as file:
            return file.read()

    def send_input(self, user_input) -> str:
        """
        Sends a message to the model and returns the AI's response.
        Args:
            user_input (str): The input message from the user.
        Returns:
            str: The AI's response.
        """
        self.conversation_history.append(UserMessage(content=user_input))
    
        response = self.client.complete(
            messages=self.conversation_history,
            max_tokens=self.max_tokens,
            model=self.model_name,
            temperature=0.2
        )

        ai_message = response.choices[0].message.content
        self.conversation_history.append(AssistantMessage(content=ai_message))

        return self._remove_thoughts(ai_message)

    def exec_prompt(self, prompt: str) -> str:
        """
        Execute a prompt using the LLM session and return the response.
        
        Args:
            prompt (str): The prompt to be sent to the LLM.
        
        Returns:
            str: The response from the LLM.
        """

        system_prompt = f'''
            Esegui il seguente prompt: {prompt}. Rispondi in modo mirato, sintetico e non aggiungere spiegazioni superflue.
            Concludi la risposta entro 1024 token.
            Rispondi in italiano.
        '''
        
        self.conversation_history = []
        return self.send_input(system_prompt)

    def reset_conversation(self):
        """
        Resets the conversation history keeping the system prompt.
        """
        self.conversation_history = [SystemMessage(content=self.system_prompt)]

    def _remove_thoughts(self, text: str) -> str:
        """
        Remove chain of thoughts from the output if present. Chain of thoughts is typically indicated by the tags <think> and </think>.
        Args:
            output (str): The output string from the model.

        """
        if "</think>" in text:
            line = re.sub(r"\s*<think>.*?</think>?\s*", "", text,flags=re.DOTALL)
        else:
            raise ValueError("Chain of thoughts not closed properly in the output!")
        return line


if __name__ == "__main__":
    endpoint = "https://byk-project-resource.services.ai.azure.com/models"
    model_name = "DeepSeek-R1-0528-2"
    api_key = "C7zq6scqrGBWZQbDZgKRf5dFyPW1gEu6IYpNcYjzKd11mm1iGj16JQQJ99BFACgEuAYXJ3w3AAAAACOGSwgv"
    system_prompt_path = "./rsc/system_prompt.txt"

    

    user_name = input("Ciao! Prima di iniziare, come ti chiami? ")

   
    chat_session = ChatSession(endpoint, api_key, model_name, system_prompt_path)
    # print(chat_session.system_prompt)
    
    ai_response = chat_session.send_message(f"Ciao Robbi, sono {user_name}")
    ai_response = chat_session.remove_thoughts(ai_response)
    print(ai_response)

    
    exit_phrase = "è stato bello giocare con te! ciao amico!"

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit": 
            print("Chat terminata manualmente.")
            break

        ai_response = chat_session.send_message(user_input)
        cleaned_response = chat_session.remove_thoughts(ai_response)
        print(cleaned_response)

        if exit_phrase in ai_response.lower():
            print("Conversazione terminata automaticamente da Robbi.")
            break
