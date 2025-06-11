import pandas as pd

class Globals:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Globals, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.shown_stories = pd.read_csv("./rsc/quest_finali.csv")
        self.role_story = ''
        self.ideal_prompts = pd.read_csv("./rsc/proide.csv")