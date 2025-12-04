import tkinter as tk

class ClickCounter:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Счётчик нажатий")
        self.window.geometry("300x200")
        
        self.count = 0
        
        # Label для отображения счетчика
        self.label = tk.Label(
            self.window, 
            text=str(self.count),
            font=("Arial", 48),
            relief="solid",
            width=10
        )
        self.label.pack(pady=20)
        
        # Кнопка
        self.button = tk.Button(
            self.window,
            text="Нажать",
            command=self.increment,
            font=("Arial", 18),
            bg="#4CAF50",
            fg="white"
        )
        self.button.pack()
        
        # Кнопка сброса
        self.reset_button = tk.Button(
            self.window,
            text="Сбросить",
            command=self.reset,
            font=("Arial", 12)
        )
        self.reset_button.pack(pady=10)
        
    def increment(self):
        self.count += 1
        self.label.config(text=str(self.count))
    
    def reset(self):
        self.count = 0
        self.label.config(text=str(self.count))
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ClickCounter()
    app.run()