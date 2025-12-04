import tkinter as tk
from tkinter import ttk

def show_greeting():
    """Функция для отображения приветствия в метке"""
    greeting_label.config(text="Привет, Павел Семенов!")

root = tk.Tk()
root.title("Приветствие")
root.geometry("400x200")
root.resizable(False, False)
style = ttk.Style()
style.theme_use('clam')

greeting_label = ttk.Label(
    root, 
    text="", 
    font=("Arial", 12),
    foreground="#2E86C1"
)
greeting_label.pack(pady=20)

greet_button = ttk.Button(
    root,
    text="Поприветствовать",
    command=show_greeting,
    style="Accent.TButton"
)
greet_button.pack(pady=10)

style.configure("Accent.TButton", 
                font=("Arial", 11, "bold"),
                padding=10,
                background="#3498DB",
                foreground="white")


root.mainloop()