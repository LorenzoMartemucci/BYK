class Person:
    def __init__(self, name=None):
        self.name = name
        self.remaining_time = None
        self.score = 0

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

    def update_score(self, score):
        self.score += score

    def set_prompt(self, key, value):
        if key in self.prompts:
            self.prompts[key] = value
        else:
            raise KeyError(f"Invalid prompt key: {key}")

    def get_prompt(self, key):
        return self.prompts.get(key, None)

    def __str__(self):
        return (
            f"Name: {self.name}, Remaining time: {self.remaining_time}, score: {self.score}, "
            f"prompts: {self.prompts}"
        )