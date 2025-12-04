import tkinter as tk
from tkinter import ttk
import random

class RandomProgressApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Случайные числа + ProgressBar")
        self.root.geometry("400x250")

        self.random_value = tk.IntVar(value=0)

        self.progress_max = 100
        
        self.create_widgets()
        self.reset_progress()
    
    def create_widgets(self):
        self.value_label = ttk.Label(
            self.root, 
            text="Случайное число: 0",
            font=('Arial', 12)
        )
        self.value_label.pack(pady=10)
        
        self.progress = ttk.Progressbar(
            self.root, 
            length=300,
            mode='determinate',
            maximum=self.progress_max
        )
        self.progress.pack(pady=10)

        self.trackbar_label = ttk.Label(
            self.root, 
            text="Максимальное значение: 100",
            font=('Arial', 10)
        )
        self.trackbar_label.pack(pady=5)

        self.trackbar = ttk.Scale(
            self.root,
            from_=10, 
            to=200,   
            orient='horizontal',
            command=self.update_trackbar
        )
        self.trackbar.set(100) 
        self.trackbar.pack(pady=10, padx=20, fill='x')
        
        # Кнопка "Сброс"
        self.reset_button = ttk.Button(
            self.root,
            text="Сброс (Новое случайное число)",
            command=self.reset_progress
        )
        self.reset_button.pack(pady=20)
    
    def update_trackbar(self, value):
        """Обновление максимального значения при изменении TrackBar"""
        max_value = int(float(value))
        self.trackbar_label.config(text=f"Максимальное значение: {max_value}")

        if max_value > 0:
            current = self.random_value.get()
            self.progress['maximum'] = max_value
            self.progress['value'] = min(current, max_value)
    
    def reset_progress(self):
        """Генерация нового случайного числа и обновление ProgressBar"""
        max_value = int(self.trackbar.get())

        new_random = random.randint(0, max_value)
        self.random_value.set(new_random)

        self.value_label.config(text=f"Случайное число: {new_random}")
        
        self.progress['maximum'] = max_value
        self.progress['value'] = new_random

def main():
    root = tk.Tk()
    app = RandomProgressApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()