import tkinter as tk
from tkinter import ttk

def update_label(value):
    label.config(text=f"Значение: {value}")

root = tk.Tk()
root.title("TrackBar Example")
root.geometry("300x150")

# Создаем TrackBar (Scale в Tkinter)
scale = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=update_label)
scale.pack(pady=20)

# Метка для отображения значения
label = tk.Label(root, text="Значение: 0", font=("Arial", 12))
label.pack(pady=10)

# Entry для отображения и ввода значения
entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 12), justify='center')
entry.pack(pady=10)

def update_entry(value):
    entry_var.set(value)

scale.config(command=update_entry)

root.mainloop()