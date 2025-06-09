"""
person.py

This module defines the Person class, which stores user-related data and manages their interaction state
in the context of an educational or storytelling application.

Main Features:
- Stores the user's name, remaining time, score, and a set of categorized prompts.
- Allows setting and retrieving prompts related to role, task, context, output format, and constraint.
- Supports updating the score and tracking a final composite prompt for evaluation or submission.
"""

class Person:

    def __init__(self):
        # Initialize the user profile with default values
        self.name = None
        self.remaining_time = None
        self.score = 0
        self.final_prompt = None

        # Dictionary to store specific categorized prompts
        self.prompts = {
            "role": None,
            "task": None,
            "context": None,
            "output_format": None,
            "constraint": None
        }

    def set_name(self, name):
        # Set the user's name
        self.name = name

    def get_name(self):
        # Retrieve the user's name
        return self.name

    def update_score(self, score):
        # Add to the user's current score
        self.score += score

    def get_score(self):
        # Retrieve the current score
        return self.score

    def set_prompt(self, key, value):
        # Set a prompt value by key (e.g., "role", "task")
        if key in self.prompts:
            self.prompts[key] = value
        else:
            raise KeyError(f"Invalid prompt key: {key}")

    def get_prompt(self, key):
        # Retrieve a prompt by its key
        return self.prompts.get(key, None)

    def get_final_prompt(self):
        # Get the final assembled prompt
        return self.final_prompt

    def set_final_prompt(self, final_prompt):
        # Set the final prompt (should replace previous value)
        self.final_prompt = final_prompt

    def __str__(self):
        # String representation of the user's state
        return (
            f"Name: {self.name}, Remaining time: {self.remaining_time}, score: {self.score}, "
            f"prompts: {self.prompts}, Final prompt: {self.final_prompt}"
        )
