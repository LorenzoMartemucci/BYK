class ChatLogics:

    chat = Chat()
    llm = Llm()

    @staticmethod
    def keep_chat_on(self, role, prompt):
        response = llm.send(role, prompt)
        if response is key:
            chat.set_next_button_to_next()
        else:
            chat.add_message_bubble(response, is_user=False)

    @staticmethod
    def function(args):
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