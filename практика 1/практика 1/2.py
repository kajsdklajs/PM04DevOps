import tkinter as tk
from tkinter import ttk, scrolledtext

def add_text_to_memo():
    memo.insert(tk.END, "Привет, Павел Семенов!\n")
    memo.see(tk.END)

root = tk.Tk()
root.title("Memo приложение")
root.geometry("400x300")

memo = scrolledtext.ScrolledText(root, width=50, height=15, wrap=tk.WORD)
memo.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

button = ttk.Button(root, text="Добавить текст", command=add_text_to_memo)
button.pack(pady=10)

root.mainloop()