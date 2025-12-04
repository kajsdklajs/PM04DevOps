import tkinter as tk
from tkinter import ttk
import random
import threading
import time

class RandomNumberGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Семенов Павел")
        self.root.geometry("500x450")
        
        self.running = False
        self.update_thread = None
        
        self.min_value = 0
        self.max_value = 100
        
        self.min_label = tk.Label(root, text="Минимум: 0", font=("Arial", 11))
        self.min_label.pack(pady=(20, 5))
        
        self.min_trackbar = ttk.Scale(root, from_=0, to=1000, value=0, command=self.update_min_label)
        self.min_trackbar.pack(fill=tk.X, padx=30, pady=5)
        
        self.max_label = tk.Label(root, text="Максимум: 100", font=("Arial", 11))
        self.max_label.pack(pady=5)
        
        self.max_trackbar = ttk.Scale(root, from_=0, to=1000, value=100, command=self.update_max_label)
        self.max_trackbar.pack(fill=tk.X, padx=30, pady=5)
        
        self.number_frame = tk.Frame(root)
        self.number_frame.pack(pady=20)
        
        self.number_label = tk.Label(self.number_frame, text="0", font=("Digital-7", 48), fg="#2E8B57")
        self.number_label.pack()
        
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=10)
        
        self.manual_button = tk.Button(self.control_frame, text="Вручную", command=self.manual_generate, 
                                      font=("Arial", 11), width=10)
        self.manual_button.pack(side=tk.LEFT, padx=5)
        
        self.timer_button = tk.Button(self.control_frame, text="Старт таймер", command=self.toggle_timer, 
                                     font=("Arial", 11), width=12)
        self.timer_button.pack(side=tk.LEFT, padx=5)
        
        self.speed_label = tk.Label(root, text="Скорость: 1 сек", font=("Arial", 10))
        self.speed_label.pack(pady=5)
        
        self.speed_trackbar = ttk.Scale(root, from_=0.1, to=3.0, value=1.0, command=self.update_speed_label)
        self.speed_trackbar.pack(fill=tk.X, padx=30, pady=5)
        
        self.update_delay = 1.0
        
        self.status_label = tk.Label(root, text="Готово", font=("Arial", 10))
        self.status_label.pack(pady=10)

    def update_min_label(self, value):
        self.min_value = int(float(value))
        self.min_label.config(text=f"Минимум: {self.min_value}")
        if self.min_value > self.max_value:
            self.max_trackbar.set(self.min_value)
            self.max_value = self.min_value
            self.max_label.config(text=f"Максимум: {self.max_value}")

    def update_max_label(self, value):
        self.max_value = int(float(value))
        self.max_label.config(text=f"Максимум: {self.max_value}")
        if self.max_value < self.min_value:
            self.min_trackbar.set(self.max_value)
            self.min_value = self.max_value
            self.min_label.config(text=f"Минимум: {self.min_value}")

    def update_speed_label(self, value):
        self.update_delay = float(value)
        self.speed_label.config(text=f"Скорость: {self.update_delay:.1f} сек")

    def generate_number(self):
        if self.min_value <= self.max_value:
            return random.randint(self.min_value, self.max_value)
        return self.min_value

    def manual_generate(self):
        number = self.generate_number()
        self.number_label.config(text=str(number))
        self.status_label.config(text=f"Сгенерировано: {number}")

    def timer_update(self):
        while self.running:
            number = self.generate_number()
            self.root.after(0, self.update_number_display, number)
            time.sleep(self.update_delay)

    def update_number_display(self, number):
        self.number_label.config(text=str(number))
        self.status_label.config(text=f"Таймер: {number}")

    def toggle_timer(self):
        if not self.running:
            self.running = True
            self.timer_button.config(text="Стоп таймер")
            self.manual_button.config(state=tk.DISABLED)
            self.update_thread = threading.Thread(target=self.timer_update, daemon=True)
            self.update_thread.start()
            self.status_label.config(text="Таймер запущен")
        else:
            self.running = False
            self.timer_button.config(text="Старт таймер")
            self.manual_button.config(state=tk.NORMAL)
            if self.update_thread:
                self.update_thread.join(timeout=0.1)
            self.status_label.config(text="Таймер остановлен")

    def on_closing(self):
        self.running = False
        if self.update_thread:
            self.update_thread.join(timeout=0.5)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomNumberGenerator(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()