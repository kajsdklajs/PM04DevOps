import tkinter as tk
from tkinter import ttk
import random

class RandomNumbersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Семенов Павел")
        self.root.geometry("600x500")
        
        self.label_count = tk.Label(root, text="Количество: 1000", font=("Arial", 12))
        self.label_count.pack(pady=10)
        
        self.trackbar = ttk.Scale(root, from_=1, to=10000, value=1000, command=self.update_label)
        self.trackbar.pack(fill=tk.X, padx=20, pady=5)
        
        self.button = tk.Button(root, text="Сгенерировать числа", command=self.generate_numbers, font=("Arial", 12), height=2)
        self.button.pack(pady=10)
        
        self.memo = tk.Text(root, height=20, width=70, font=("Courier New", 10))
        self.memo.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(self.memo)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.memo.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.memo.yview)
        
        self.status_label = tk.Label(root, text="", font=("Arial", 10))
        self.status_label.pack(pady=5)

    def update_label(self, value):
        count = int(float(value))
        self.label_count.config(text=f"Количество: {count}")

    def generate_numbers(self):
        self.memo.delete(1.0, tk.END)
        count = int(self.trackbar.get())
        
        self.status_label.config(text="Генерация...")
        self.root.update()
        
        numbers_per_line = 10
        numbers = []
        
        for i in range(count):
            numbers.append(str(random.randint(0, 999999)).rjust(6))
            
            if (i + 1) % numbers_per_line == 0 or i == count - 1:
                self.memo.insert(tk.END, " ".join(numbers) + "\n")
                numbers = []
                
            if i % 100 == 0:
                self.root.update()
        
        self.status_label.config(text=f"Сгенерировано {count} чисел")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomNumbersApp(root)
    root.mainloop()