import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.interface.start_page import StartPage
from src.interface.final_request_page import FinalRequestPage 
from src.interface.style import Style
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
        self.root.minsize(480, 720)  # Set minimum size to 480x720
        self.root.title('Robbi')
        self.root.iconbitmap('rsc/robot_icon.ico')
        self.root.configure(bg=Style.WINDOW_BG)
        self.root.title("Robbi")
        try:
            self.root.iconbitmap("./rsc/robot_icon.ico")
        except Exception:
            pass
        #self.start_page = StartPage(self.root)
        self.start_page = FinalRequestPage(self.root)


        self.start_page.pack(fill="both", expand=True)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()