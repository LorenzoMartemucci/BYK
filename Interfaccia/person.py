class Person:
    def __init__(self, name=None):
        self.name = name
        self.remaining_time = None
        self.score = 0

    def set_name(self, name):
        self.name = name

    def update_score(self, score):
        self.score += score

    def __str__(self):
        return f"Name: {self.name}, Remaining time: {self.remaining_time}, score: {self.score}"