import tkinter as tk
from playsound import playsound

class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("Configurable Pomodoro Timer")

        self.work = 25*60  # 25 minutes
        self.rest = 5*60   # 5 minutes
        self.long_rest = 15*60  # 15 minutes
        self.running = False
        self.cycle = 0
        self.current_time = self.work

        self.time_label = tk.Label(master, text=self.format_time(self.current_time), font=("Arial", 48))
        self.time_label.pack(pady=10)

        self.status_label = tk.Label(master, text="Time to work!", font=("Arial", 24))
        self.status_label.pack(pady=10)

        button_frame = tk.Frame(master)
        button_frame.pack(pady=(0, 20))

        self.start_button = tk.Button(button_frame, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=20)

        self.pause_button = tk.Button(button_frame, text="Pause", command=self.pause_timer, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=20)

        self.settings_button = tk.Button(button_frame, text="Settings", command=self.open_settings)
        self.settings_button.pack(side=tk.LEFT, padx=20)

        bottom_padding = tk.Frame(master, height=10)
        bottom_padding.pack(side=tk.BOTTOM, fill=tk.X)

    def format_time(self, seconds):
        minutes, secs = divmod(seconds, 60)
        return f"{minutes:02d}:{secs:02d}"

    def start_timer(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.update_timer()

    def pause_timer(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)

    def update_status(self, period):
        if period == "work":
            self.status_label.config(text="Time to work!")
            self.current_time = self.work
        elif period == "rest":
            self.status_label.config(text="Time to take a short break!")
            self.current_time = self.rest
        else:  # long rest
            self.status_label.config(text="Time to take a long break!")
            self.current_time = self.long_rest
        self.time_label.config(text=self.format_time(self.current_time))
        self.pause_timer()  # Automatically pause before starting new period

    def update_timer(self):
        if self.running:
            if self.current_time > 0:
                self.time_label.config(text=self.format_time(self.current_time))
                self.current_time -= 1
                self.master.after(1000, self.update_timer)
            else:
                playsound("alarm.mp3")
                self.cycle += 1
                if self.cycle in [1, 3, 5, 7]:
                    self.update_status("rest")
                elif self.cycle == 8:
                    self.update_status("long rest")
                    self.cycle = 0
                else:
                    self.update_status("work")

    def open_settings(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Timer Settings")

        tk.Label(settings_window, text="Work duration (minutes):").grid(row=0, column=0, padx=5, pady=5)
        work_entry = tk.Entry(settings_window)
        work_entry.insert(0, str(self.work // 60))
        work_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(settings_window, text="Rest duration (minutes):").grid(row=1, column=0, padx=5, pady=5)
        rest_entry = tk.Entry(settings_window)
        rest_entry.insert(0, str(self.rest // 60))
        rest_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(settings_window, text="Long rest duration (minutes):").grid(row=2, column=0, padx=5, pady=5)
        long_rest_entry = tk.Entry(settings_window)
        long_rest_entry.insert(0, str(self.long_rest // 60))
        long_rest_entry.grid(row=2, column=1, padx=5, pady=5)

        def save_settings():
            try:
                self.work = int(work_entry.get()) * 60
                self.rest = int(rest_entry.get()) * 60
                self.long_rest = int(long_rest_entry.get()) * 60
                self.current_time = self.work
                self.time_label.config(text=self.format_time(self.current_time))
                settings_window.destroy()
            except ValueError:
                tk.messagebox.showerror("Invalid Input", "Please enter valid numbers for all durations.")

        save_button = tk.Button(settings_window, text="Save", command=save_settings)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

def main():
    root = tk.Tk()
    timer_app = TimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
