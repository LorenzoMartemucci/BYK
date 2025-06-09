import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
import re
import langid


class ChatSession:
    def __init__(self, endpoint = "https://byk-project-resource.services.ai.azure.com/models", 
        api_key = "C7zq6scqrGBWZQbDZgKRf5dFyPW1gEu6IYpNcYjzKd11mm1iGj16JQQJ99BFACgEuAYXJ3w3AAAAACOGSwgv",
        model_name = "DeepSeek-R1-0528-2", system_prompt_path = "llm/system_prompt.txt", max_tokens=1024):

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

    def send_message(self, user_input ):
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
            temperature=0.4
        )

        ai_message = response.choices[0].message.content
        self.conversation_history.append(AssistantMessage(content=ai_message))

        return ai_message

    def reset_conversation(self):
        """
        Resets the conversation history keeping the system prompt.
        """
        self.conversation_history = [SystemMessage(content=self.system_prompt)]

    def remove_thoughts(self, text: str) -> str:
        """
        Remove chain of thoughts from the output if present. Chain of thoughts is typically indicated by the tags <think> and </think>.
        Args:
            output (str): The output string from the model.

        """
        line = re.sub(r"\s*<think>.*?</think>\s*", "", text,flags=re.DOTALL)
        return line

    def remove_fully_english_paragraphs(self, text: str, threshold: float = 0.80) -> str:
        """
        Removes paragraphs that are classified with high confidence as English.
        Keeps Italian paragraphs even if they contain some English words.
        
        Args:
            text (str): The model output to clean.
            threshold (float): Confidence threshold to consider a paragraph fully English.
        
        Returns:
            str: Cleaned text.
        """
        paragraphs = text.split('\n')
        filtered_paragraphs = []

        for paragraph in paragraphs:
            cleaned_paragraph = paragraph.strip()
            if not cleaned_paragraph:
                continue

            lang, prob = langid.classify(cleaned_paragraph)

            # Only remove paragraph if it's confidently classified as English
            if lang == 'en' and prob >= threshold:
                continue  # skip this paragraph (fully English)
            else:
                filtered_paragraphs.append(cleaned_paragraph)

        return '\n'.join(filtered_paragraphs)

    def clean_response(self, text: str) -> str:
        """
        Apply full cleaning pipeline:
        - Remove <think> tags
        - Remove fully English paragraphs
        """
        text_no_thoughts = self.remove_thoughts(text)
        text_no_english = self.remove_fully_english_paragraphs(text_no_thoughts)
        return text_no_english

# ESEMPIO DI USO:

if __name__ == "__main__":
    # Parametri di configurazione
    endpoint = "https://byk-project-resource.services.ai.azure.com/models"
    model_name = "DeepSeek-R1-0528-2"
    api_key = "C7zq6scqrGBWZQbDZgKRf5dFyPW1gEu6IYpNcYjzKd11mm1iGj16JQQJ99BFACgEuAYXJ3w3AAAAACOGSwgv"
    system_prompt_path = "llm/system_prompt.txt"

    # Creazione della sessione
    chat_session = ChatSession(endpoint, api_key, model_name, system_prompt_path)

    # Simulazione ciclo conversazione
    exit_phrase = "è stato bello giocare con te! ciao amico!"

    user_name = input('Inserisci il tuo nome: ')
    ai_response = chat_session.send_message(f"Ciao Robbi, sono {user_name}")
    print(chat_session.remove_thoughts(ai_response))

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chat terminata manualmente.")
            break

        ai_response = chat_session.send_message(user_input)
        cleaned_response = chat_session.clean_response(ai_response)
        print(cleaned_response)


        if exit_phrase in ai_response.lower():
            print("Conversazione terminata automaticamente da Robbi.")
            break
