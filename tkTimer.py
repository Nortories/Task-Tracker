import tkinter as tk
from datetime import datetime, timedelta

class TimerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.timer_label = tk.Label(self, text="00:00:00")
        self.timer_label.pack()

        self.start_time = None
        self.timer_running = False
        self.elapsed_time = timedelta()

        # Start/Stop Button
        self.toggle_button = tk.Button(self, text="Start Timer", command=self.toggle_timer)
        self.toggle_button.pack()

        # Update the timer every 1000ms (1 second)
        self.update_timer()

    def toggle_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.toggle_button.config(text="Start Timer")
        else:
            self.timer_running = True
            if not self.start_time:
                self.start_time = datetime.now()
            self.toggle_button.config(text="Stop Timer")

    def update_timer(self):
        if self.timer_running:
            now = datetime.now()
            self.elapsed_time += now - self.start_time
            self.start_time = now
            self.timer_label.config(text=str(self.elapsed_time).split('.')[0])
        self.after(1000, self.update_timer)

if __name__ == "__main__":
    app = TimerApp()
    app.mainloop()
