import tkinter as tk
from tkinter import ttk
import random

class RandomNumbersGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Семенов Павел")
        self.root.geometry("600x500")
        
        self.label_count = tk.Label(root, text="Количество чисел: 100", font=("Arial", 12, "bold"))
        self.label_count.pack(pady=15)
        
        self.trackbar_frame = tk.Frame(root)
        self.trackbar_frame.pack(fill=tk.X, padx=30, pady=10)
        
        self.trackbar = ttk.Scale(self.trackbar_frame, from_=1, to=1000, value=100, 
                                 command=self.update_count_display, length=400)
        self.trackbar.pack()
        
        self.scale_labels = tk.Frame(root)
        self.scale_labels.pack(fill=tk.X, padx=30)
        
        tk.Label(self.scale_labels, text="1", font=("Arial", 9)).pack(side=tk.LEFT)
        tk.Label(self.scale_labels, text="500", font=("Arial", 9)).pack(side=tk.LEFT, expand=True)
        tk.Label(self.scale_labels, text="1000", font=("Arial", 9)).pack(side=tk.RIGHT)
        
        self.generate_button = tk.Button(root, text="Сгенерировать числа", 
                                        command=self.generate_numbers,
                                        font=("Arial", 12), 
                                        bg="#4CAF50", 
                                        fg="white",
                                        height=2,
                                        width=20)
        self.generate_button.pack(pady=20)
        
        self.text_frame = tk.Frame(root)
        self.text_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.text_area = tk.Text(self.text_frame, height=15, width=70, font=("Consolas", 10))
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = tk.Scrollbar(self.text_frame, command=self.text_area.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        
        self.stats_label = tk.Label(root, text="", font=("Arial", 10))
        self.stats_label.pack(pady=5)

    def update_count_display(self, value):
        count = int(float(value))
        self.label_count.config(text=f"Количество чисел: {count}")

    def generate_numbers(self):
        self.text_area.delete(1.0, tk.END)
        count = int(self.trackbar.get())
        
        numbers = []
        for i in range(count):
            numbers.append(random.randint(0, 999999))
            
            if (i + 1) % 10 == 0 or i == count - 1:
                line = " ".join(f"{num:06d}" for num in numbers[-min(10, len(numbers)):])
                self.text_area.insert(tk.END, line + "\n")
                
            if i % 50 == 0:
                self.root.update()
        
        min_val = min(numbers)
        max_val = max(numbers)
        avg_val = sum(numbers) / len(numbers)
        
        self.stats_label.config(
            text=f"Сгенерировано: {count} чисел | Мин: {min_val} | Макс: {max_val} | Среднее: {avg_val:.2f}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomNumbersGenerator(root)
    root.mainloop()