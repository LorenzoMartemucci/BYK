from interface.story_page import StoryPage
from interface.storytelling_template import StorytellingTemplate

class FailPage(StorytellingTemplate):
    def __init__(self, container):
        super().__init__(container, show_timer=False)
        self.next_button.configure(command=self.go_to_story_page)
        self.story.configure(text='Il prompt ideale doveva essere: <promp> Riproviamo!')

    def read_story(self, story_path):
        try:
            with open(story_path, "r") as story_file:
                return story_file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Story file not found at '{story_path}'. Please ensure the file exists and the path is correct.")

    def go_to_story_page(self):
        story_page = StoryPage(self.master)
        story_page.pack(fill="both", expand=True)
        self.destroy()
