class ChatLogics:

    def __init__(self, person, chat, llm):
        self.chat = chat
        self.llm = llm
        self.person = person

    @staticmethod
    def keep_chat_on(self, role, prompt, key):
        """Handles the logic for sending a message and receiving a response from the LLM."""
        response = self.llm.send(role, prompt)
        if response is key:
            self.chat.change_input_field_with_button() # TODO: Change input field to button 
        else:
            self.chat.add_message_bubble(response, is_user=False)

    @staticmethod
    def save_role_into_person(self):
        pass

    @staticmethod
    def function():
        pass
    """
    user_message = self.user_input.get("1.0", "end-1c").strip()
        if user_message:
            self.add_message_bubble(user_message, is_user=True)
            self.last_user_message = user_message
            self.user_input.delete("1.0", "end")  # Clear input field

            # Here you would typically call your LLM or processing function
            # For demonstration, we will simulate a bot response
            bot_response = f"Bot response"
            self.add_message_bubble(bot_response, is_user=False)
    """