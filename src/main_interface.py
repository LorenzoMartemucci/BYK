from interface.start_page import StartPage
from interface.style import Style
import customtkinter as ctk
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 1 = SYSTEM_DPI_AWARE (comportamento come 100% scala)
except Exception:
    pass

class MainApp:
    def __init__(self):
        ctk.set_appearance_mode("light")
        self.root = ctk.CTk(fg_color=Style.WINDOW_BG)
        self.root.geometry("480x640")
        # self.root.resizable(False, False)
        self.root.minsize(480, 640)
        self.root.configure(bg=Style.WINDOW_BG)
        self.username = None
        
        self.start_page = StartPage(self.root)
        self.start_page.pack(fill="both", expand=True)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
