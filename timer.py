import tkinter as tk
from tkinter import ttk
from datetime import datetime
from play_sound import play_sound


class TimerWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Таймеры")
        self.attributes('-toolwindow', 1)  # Убирает кнопки развернуть и свернуть
        self.geometry("135x600")
        self.resizable(True, True)

        self.timer1 = TimerFrame(self, "Арена")
        self.timer1.pack(side=tk.LEFT, pady=10)

        self.timer2 = TimerFrame(self, "ЛевыйVR")
        self.timer2.pack(side=tk.LEFT, pady=10)

        self.timer3 = TimerFrame(self, "ПравыйVR")
        self.timer3.pack(side=tk.LEFT, pady=10)


class TimerFrame(tk.Frame):
    def __init__(self, parent, timer_name):
        super().__init__(parent)
        self.timer_name = timer_name
        self.time = tk.StringVar()
        self.time.set("00:00:00")
        self.start_time = None

        self.label = ttk.Label(self, text=self.timer_name, font=("Arial", 10))
        self.label.pack(pady=1)

        self.timer_label = ttk.Label(self, textvariable=self.time, font=("Arial", 14))
        self.timer_label.pack(pady=1)

        self.launch_label = ttk.Label(self, text="", font=("Arial", 10))
        self.launch_label.pack(pady=1)

        self.input_minutes = tk.Entry(self)
        self.input_minutes.pack(side=tk.TOP, padx=1, pady=1)

        self.button_add_time = ttk.Button(self, text="Добавить время", command=self.add_time)
        self.button_add_time.pack(side=tk.TOP, padx=1, pady=1)

        self.button_start_stop = ttk.Button(self, text="Старт", command=self.start_stop_timer)
        self.button_start_stop.pack(side=tk.TOP, padx=1, pady=1)

        self.button_reset = ttk.Button(self, text="Сброс", command=self.reset_timer)
        self.button_reset.pack(side=tk.TOP, padx=1, pady=1)

        self.current_timer = None

    def add_time(self):
        minutes = int(self.input_minutes.get())
        self.input_minutes.delete(0, tk.END)  # Удаление содержимого поля ввода
        current_time = self.time.get()
        hh, mm, ss = map(int, current_time.split(":"))
        total_time = ss + mm * 60 + hh * 3600
        total_time += minutes * 60
        new_hh = total_time // 3600
        total_time = total_time % 3600
        new_mm = total_time // 60
        new_ss = total_time % 60
        self.time.set("{:02d}:{:02d}:{:02d}".format(new_hh, new_mm, new_ss))

    def start_stop_timer(self):
        if self.current_timer is None:  # Если таймер не запущен
            self.current_timer = self.after(1000, self.update_timer)
            self.button_start_stop.configure(text="Стоп")
            if self.start_time is None:  # Проверка на то что таймер уже работал
                self.start_time = datetime.now().strftime("%H:%M")  # Сохранение времени старта
                self.launch_label.configure(text=f"Запуск в {self.start_time}")
        else:  # Если таймер уже запущен
            self.after_cancel(self.current_timer)
            self.current_timer = None
            self.button_start_stop.configure(text="Старт")

    def update_timer(self):
        current_time = self.time.get()
        hh, mm, ss = map(int, current_time.split(":"))
        total_time = ss + mm * 60 + hh * 3600
        if total_time == 0:
            self.current_timer = None
            self.button_start_stop.configure(text="Старт")
            play_sound()  # Проигрывание звука после окончания таймера
        else:
            total_time -= 1
            new_hh = total_time // 3600
            total_time = total_time % 3600
            new_mm = total_time // 60
            new_ss = total_time % 60
            self.time.set("{:02d}:{:02d}:{:02d}".format(new_hh, new_mm, new_ss))
            self.current_timer = self.after(1000, self.update_timer)

    def reset_timer(self):
        self.time.set("00:00:00")  # Обнуление таймера
        self.input_minutes.delete(0, tk.END)  # Удаление содержимого поля ввода
        if self.current_timer is not None:  # If timer is running
            self.after_cancel(self.current_timer)
            self.current_timer = None
            self.button_start_stop.configure(text="Старт")
        self.launch_label.configure(text="")  # Очистка поля времени запуска

