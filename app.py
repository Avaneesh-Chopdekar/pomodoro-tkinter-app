import time
import threading
import tkinter as tk
from tkinter import ttk


class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x300")
        self.root.title("Pomodoro Timer")

        self.default_font_family = "Arial"
        self.base_font = (self.default_font_family, 14)
        self.label_font = (self.default_font_family, 42)

        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font=self.base_font)
        self.s.configure("TButton", font=self.base_font)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", pady=10, expand=True)

        self.tab1 = ttk.Frame(self.tabs, width=500, height=100)
        self.tab2 = ttk.Frame(self.tabs, width=500, height=100)
        self.tab3 = ttk.Frame(self.tabs, width=500, height=100)

        self.pomo_timer_label = ttk.Label(self.tab1, text="25:00", font=self.label_font)
        self.pomo_timer_label.pack(pady=20)

        self.short_timer_label = ttk.Label(self.tab2, text="5:00", font=self.label_font)
        self.short_timer_label.pack(pady=20)

        self.long_timer_label = ttk.Label(self.tab3, text="15:00", font=self.label_font)
        self.long_timer_label.pack(pady=20)

        self.tabs.add(self.tab1, text="Pomodoro")
        self.tabs.add(self.tab2, text="Small Break")
        self.tabs.add(self.tab3, text="Long Break")

        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)
        self.start_btn = ttk.Button(
            self.grid_layout, text="Start", command=self.start_timer_thread
        )
        self.start_btn.grid(row=0, column=0)

        self.skip_btn = ttk.Button(
            self.grid_layout, text="Skip", command=self.skip_timer
        )
        self.skip_btn.grid(row=0, column=1)

        self.reset_btn = ttk.Button(
            self.grid_layout, text="Reset", command=self.reset_timer
        )
        self.reset_btn.grid(row=0, column=2)

        self.pomodoros = 0
        self.pomodoro_counter_label = ttk.Label(
            self.grid_layout, text=f"Pomodoros: {self.pomodoros}", font=self.base_font
        )
        self.pomodoro_counter_label.grid(row=1, column=1, pady=10)

        self.stopped = False
        self.skipped = False
        self.running = False

        self.root.mainloop()

    def start_timer_thread(self):
        if not self.running:
            t = threading.Thread(target=self.start_timer)
            t.start()
            self.running = True

    def start_timer(self):
        self.stopped = False
        self.skipped = False
        timer_id = self.tabs.index(self.tabs.select()) + 1

        if timer_id == 1:
            full_seconds = 60 * 25
            # full_seconds = 5
            while full_seconds > 0 and not self.stopped:
                mins, secs = divmod(full_seconds, 60)
                self.pomo_timer_label.config(text=f"{mins:02.0f}:{secs:02.0f}")
                self.root.update()
                time.sleep(0.1)
                full_seconds -= 0.1
            if not self.stopped or self.skipped:
                self.pomodoros += 1
                self.pomodoro_counter_label.config(text=f"Pomodoros: {self.pomodoros}")
                if self.pomodoros % 4 == 0:
                    self.tabs.select(2)
                else:
                    self.tabs.select(1)
                self.start_timer()
        elif timer_id == 2:
            full_seconds = 60 * 5
            # full_seconds = 5
            while full_seconds > 0 and not self.stopped:
                mins, secs = divmod(full_seconds, 60)
                self.short_timer_label.config(text=f"{mins:02.0f}:{secs:02.0f}")
                self.root.update()
                time.sleep(0.1)
                full_seconds -= 0.1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()
        elif timer_id == 3:
            full_seconds = 60 * 15
            # full_seconds = 5
            while full_seconds > 0 and not self.stopped:
                mins, secs = divmod(full_seconds, 60)
                self.long_timer_label.config(text=f"{mins:02.0f}:{secs:02.0f}")
                self.root.update()
                time.sleep(0.1)
                full_seconds -= 0.1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()
        else:
            print("Invalid Timer Id")

    def reset_timer(self):
        self.stopped = True
        self.ski = False
        self.pomodoros = 0
        self.pomo_timer_label.config(text="25:00")
        self.short_timer_label.config(text="5:00")
        self.long_timer_label.config(text="15:00")
        self.pomodoro_counter_label.config(text="Pomodoros: 0")
        self.running = False

    def skip_timer(self):
        current_tab = self.tabs.index(self.tabs.select())
        if current_tab == 0:
            self.pomo_timer_label.config(text="25:00")
        elif current_tab == 1:
            self.short_timer_label.config(text="05:00")
        elif current_tab == 2:
            self.long_timer_label.config(text="15:00")
        self.skipped = True
        self.stopped = True


PomodoroTimer()
