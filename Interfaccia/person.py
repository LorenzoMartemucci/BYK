class Person:
    def __init__(self):
        self.name = None
        self.remaining_time = None
        self.score = 0
        self.final_prompt = None

        # Store user prompts for role, task, context, output format, constraint
        self.prompts = {
            "role": None,
            "task": None,
            "context": None,
            "output_format": None,
            "constraint": None
        }

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def update_score(self, score):
        self.score += score

    def get_score(self):
        return self.score

    def set_prompt(self, key, value):
        if key in self.prompts:
            self.prompts[key] = value
        else:
            raise KeyError(f"Invalid prompt key: {key}")

    def get_prompt(self, key):
        return self.prompts.get(key, None)

    def get_final_prompt(self):
        return self.final_prompt

    def set_final_prompt(self, final_prompt):
        self.final_prompt + final_prompt

    def __str__(self):
        return (
            f"Name: {self.name}, Remaining time: {self.remaining_time}, score: {self.score}, "
            f"prompts: {self.prompts}, Final prompt: {self.final_prompt}"
        )