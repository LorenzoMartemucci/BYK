from transformers import AutoTokenizer, AutoModelForCausalLM

class LLMInterface:
    def __init__(self, model_name="gpt2"):
        """
        Initialize the LLM interface with a pre-trained model.

        :param model_name: Name of the pre-trained model to load (default is "gpt2").
        """
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def send_prompt(self, prompt, role=None, history=None, context=None, max_length=150, num_return_sequences=1):
        """
        Send a prompt to the LLM and receive the generated text.

        :param prompt: The input prompt to send to the LLM.
        :return: Generated text based on the input prompt.
        """

        # Encode the formatted prompt with attention mask and return tensors
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)

        # Generate text with attention mask
        output = self.model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            pad_token_id=self.tokenizer.eos_token_id
        )

        # Decode the generated output
        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)

        return generated_text

# Example usage
if __name__ == "__main__":
    # Initialize the LLM interface with a specific model
    llm = LLMInterface(model_name="gpt2")

    # Send a prompt and receive the generated text
    prompt = "Hello, how are you?"
    result = llm.send_prompt(prompt)
    print(result)
