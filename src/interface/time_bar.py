from src.interface.style import Style
import customtkinter as ctk

class TimeBar:
    def __init__(self, container, timer_total=300):
        self.container = container
        self.chat_timer_label = ctk.CTkLabel(
            self.container,
            text=f"Tempo rimanente: {timer_total}", 
            font=("Comic Sans MS", 14),
            text_color=Style.WIDGETS_FG_TEXT_COLOR,
        )
        self.chat_timer_label.pack()

        self.chat_progress_bar = ctk.CTkProgressBar(
            self.container,
            width=400,
            height=20,
            progress_color=Style.WIDGETS_PROGRESS_BAR_COLOR,
        )
        self.chat_progress_bar.set(1.0)
        self.chat_progress_bar.pack()

        self.timer_var = timer_total
        self.timer_running = False
        self.timer_running = True
        self.update_timer(timer_total)
    
    def update_timer(self, total):
        """Update the timer label and progress bar every second."""
        if not self.timer_running:
            return
        minutes = self.timer_var // 60
        seconds = self.timer_var % 60
        self.chat_timer_label.configure(text=f"Tempo rimanente: {minutes:02d}:{seconds:02d}")
        # INVERTI IL PROGRESSO: 1.0 -> pieno, 0.0 -> vuoto
        progress = max(0, min(1, self.timer_var / total))
        self.chat_progress_bar.set(progress)
        if self.timer_var > 0:
            self.timer_var -= 1
            self.container.after(1000, lambda: self.update_timer(total))

    def stop_timer(self):
        self.timer_running = False

    def destroy_timer(self):
        self.timer_running = False
        self.chat_timer_label.destroy()
        self.chat_progress_bar.destroy()

    def is_timedout(self):
        return self.timer_var == 0