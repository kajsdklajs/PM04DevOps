import tkinter as tk

class SimpleFontApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Изменение размера шрифта")
        self.root.geometry("400x300")
        
        self.font_size = 14
        
        # Создаем интерфейс
        self.create_widgets()
    
    def create_widgets(self):
        # Кнопки управления
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Уменьшить (-)", width=15,
                 command=self.decrease_font).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Увеличить (+)", width=15,
                 command=self.increase_font).pack(side='left', padx=5)
        
        # Метка с примером текста
        self.label = tk.Label(self.root, 
                             text="Пример текста в Label",
                             font=('Arial', self.font_size))
        self.label.pack(pady=20)
        
        # Многострочное текстовое поле
        self.text = tk.Text(self.root, height=5, font=('Arial', self.font_size))
        self.text.pack(pady=10, padx=20, fill='both', expand=True)
        self.text.insert('1.0', "Павел Семенов")
        
        # Метка с текущим размером
        self.size_label = tk.Label(self.root, text=f"Размер шрифта: {self.font_size}")
        self.size_label.pack(pady=5)
    
    def increase_font(self):
        self.font_size += 2
        self.update_font()
    
    def decrease_font(self):
        if self.font_size > 8:
            self.font_size -= 2
            self.update_font()
    
    def update_font(self):
        new_font = ('Arial', self.font_size)
        self.label.config(font=new_font)
        self.text.config(font=new_font)
        self.size_label.config(text=f"Размер шрифта: {self.font_size}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleFontApp(root)
    root.mainloop()