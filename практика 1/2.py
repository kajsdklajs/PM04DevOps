import tkinter as tk
from tkinter import ttk, scrolledtext

def add_text_to_memo():
    # Добавляем текст в Memo (ScrolledText)
    memo.insert(tk.END, "Привет, Павел Семенов!\n")
    # Прокручиваем вниз, чтобы была видна новая строка
    memo.see(tk.END)

# Создаем главное окно
root = tk.Tk()
root.title("Memo приложение")
root.geometry("400x300")

# Создаем Memo (ScrolledText)
memo = scrolledtext.ScrolledText(root, width=50, height=15, wrap=tk.WORD)
memo.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Создаем кнопку для добавления текста
button = ttk.Button(root, text="Добавить текст", command=add_text_to_memo)
button.pack(pady=10)

# Запускаем главный цикл
root.mainloop()