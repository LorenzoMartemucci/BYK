import pandas as pd
import csv
class Globals:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Globals, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.shown_stories = pd.read_csv("./rsc/quest_finali.csv", quoting=csv.QUOTE_ALL)
        self.role_story = ''
        self.user_name = ''
        self.ideal_prompts = pd.read_csv("./rsc/proide.csv", quoting=csv.QUOTE_ALL)