import random
import math
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog

class DataGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор данных")
        self.root.geometry("800x600")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="ГЕНЕРАТОР ДАННЫХ", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Фрейм параметров
        params_frame = ttk.LabelFrame(main_frame, text="Параметры данных", padding="10")
        params_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Первая строка параметров
        row1_frame = ttk.Frame(params_frame)
        row1_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(row1_frame, text="Количество случайных чисел:").pack(side=tk.LEFT)
        self.num_count_var = tk.StringVar(value="10")
        ttk.Entry(row1_frame, textvariable=self.num_count_var, width=10).pack(side=tk.LEFT, padx=(10, 30))
        
        ttk.Label(row1_frame, text="Математическая функция:").pack(side=tk.LEFT)
        self.func_var = tk.StringVar(value="sin")
        func_combo = ttk.Combobox(row1_frame, textvariable=self.func_var, 
                                 values=["sin", "cos", "tan", "x²", "√x"], width=8)
        func_combo.pack(side=tk.LEFT, padx=10)
        
        # Вторая строка параметров
        row2_frame = ttk.Frame(params_frame)
        row2_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(row2_frame, text="Диапазон x:").pack(side=tk.LEFT)
        self.range_start_var = tk.StringVar(value="0")
        ttk.Entry(row2_frame, textvariable=self.range_start_var, width=8).pack(side=tk.LEFT, padx=(10, 5))
        ttk.Label(row2_frame, text="до").pack(side=tk.LEFT)
        self.range_end_var = tk.StringVar(value="6.28")
        ttk.Entry(row2_frame, textvariable=self.range_end_var, width=8).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row2_frame, text="Шаг:").pack(side=tk.LEFT, padx=(20, 0))
        self.step_var = tk.StringVar(value="0.785")
        ttk.Entry(row2_frame, textvariable=self.step_var, width=8).pack(side=tk.LEFT, padx=10)
        
        # Фрейм кнопок
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="Сгенерировать данные", 
                  command=self.generate_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Сохранить в файл", 
                  command=self.save_to_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Очистить", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # Фрейм для отображения данных
        display_frame = ttk.LabelFrame(main_frame, text="Результаты", padding="10")
        display_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Вкладки для разных типов данных
        notebook = ttk.Notebook(display_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка случайных чисел
        random_tab = ttk.Frame(notebook)
        notebook.add(random_tab, text="Случайные числа")
        self.random_text = scrolledtext.ScrolledText(random_tab, width=80, height=8)
        self.random_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Вкладка математической функции
        math_tab = ttk.Frame(notebook)
        notebook.add(math_tab, text="Математическая функция")
        self.math_text = scrolledtext.ScrolledText(math_tab, width=80, height=8)
        self.math_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Вкладка статистики
        stats_tab = ttk.Frame(notebook)
        notebook.add(stats_tab, text="Статистика")
        self.stats_text = scrolledtext.ScrolledText(stats_tab, width=80, height=8)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Данные
        self.random_numbers = []
        self.x_values = []
        self.y_values = []
        self.func_name = ""
        
    def generate_data(self):
        try:
            self.status_var.set("Генерация данных...")
            self.root.update()
            
            # Генерация случайных чисел
            num_count = int(self.num_count_var.get())
            if num_count <= 0:
                messagebox.showerror("Ошибка", "Количество чисел должно быть положительным")
                return
                
            self.random_numbers = [random.uniform(0, 100) for _ in range(num_count)]
            
            # Отображение случайных чисел
            self.random_text.delete(1.0, tk.END)
            self.random_text.insert(tk.END, "СЛУЧАЙНЫЕ ЧИСЛА (0-100):\n")
            self.random_text.insert(tk.END, "=" * 40 + "\n")
            for i, num in enumerate(self.random_numbers, 1):
                self.random_text.insert(tk.END, f"{i:3d}. {num:8.2f}\n")
            
            # Генерация математической функции
            func_mapping = {
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "x²": lambda x: x**2,
                "√x": lambda x: math.sqrt(x) if x >= 0 else float('nan')
            }
            
            func = func_mapping.get(self.func_var.get(), math.sin)
            self.func_name = self.func_var.get()
            
            start = float(self.range_start_var.get())
            end = float(self.range_end_var.get())
            step = float(self.step_var.get())
            
            if step <= 0:
                messagebox.showerror("Ошибка", "Шаг должен быть положительным числом")
                return
            
            self.x_values = []
            self.y_values = []
            
            # Отображение функции
            self.math_text.delete(1.0, tk.END)
            self.math_text.insert(tk.END, f"ФУНКЦИЯ: {self.func_name}(x)\n")
            self.math_text.insert(tk.END, "=" * 40 + "\n")
            self.math_text.insert(tk.END, "   x\t\t|   f(x)\n")
            self.math_text.insert(tk.END, "-" * 40 + "\n")
            
            x = start
            while x <= end:
                try:
                    y = func(x)
                    self.x_values.append(x)
                    self.y_values.append(y)
                    if math.isnan(y):
                        self.math_text.insert(tk.END, f"{x:6.3f}\t| не определена\n")
                    else:
                        self.math_text.insert(tk.END, f"{x:6.3f}\t| {y:10.6f}\n")
                except (ValueError, ZeroDivisionError):
                    self.math_text.insert(tk.END, f"{x:6.3f}\t| не определена\n")
                x += step
                x = round(x, 10)  # Округление для избежания ошибок
            
            # Расчет статистики
            self.calculate_statistics()
            
            self.status_var.set("Данные успешно сгенерированы")
            
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", "Проверьте правильность введенных значений")
            self.status_var.set("Ошибка ввода данных")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
            self.status_var.set("Ошибка при генерации данных")
    
    def calculate_statistics(self):
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, "СТАТИСТИЧЕСКИЕ ДАННЫЕ\n")
        self.stats_text.insert(tk.END, "=" * 40 + "\n\n")
        
        # Статистика по случайным числам
        if self.random_numbers:
            self.stats_text.insert(tk.END, "СЛУЧАЙНЫЕ ЧИСЛА:\n")
            self.stats_text.insert(tk.END, f"  Количество: {len(self.random_numbers)}\n")
            self.stats_text.insert(tk.END, f"  Минимальное: {min(self.random_numbers):.2f}\n")
            self.stats_text.insert(tk.END, f"  Максимальное: {max(self.random_numbers):.2f}\n")
            self.stats_text.insert(tk.END, f"  Среднее: {sum(self.random_numbers)/len(self.random_numbers):.2f}\n")
            self.stats_text.insert(tk.END, f"  Сумма: {sum(self.random_numbers):.2f}\n\n")
        
        # Статистика по функции
        if self.y_values:
            valid_y = [y for y in self.y_values if not math.isnan(y)]
            if valid_y:
                self.stats_text.insert(tk.END, f"ФУНКЦИЯ {self.func_name}(x):\n")
                self.stats_text.insert(tk.END, f"  Количество точек: {len(valid_y)}\n")
                self.stats_text.insert(tk.END, f"  Минимальное значение: {min(valid_y):.6f}\n")
                self.stats_text.insert(tk.END, f"  Максимальное значение: {max(valid_y):.6f}\n")
                self.stats_text.insert(tk.END, f"  Среднее значение: {sum(valid_y)/len(valid_y):.6f}\n")
    
    def save_to_file(self):
        if not self.random_numbers and not self.x_values:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
            title="Сохранить данные"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write("=" * 50 + "\n")
                    file.write("СГЕНЕРИРОВАННЫЕ ДАННЫЕ\n")
                    file.write("=" * 50 + "\n")
                    file.write(f"Дата создания: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    file.write(f"Параметры генерации:\n")
                    file.write(f"  Количество случайных чисел: {len(self.random_numbers)}\n")
                    file.write(f"  Функция: {self.func_name}\n")
                    file.write(f"  Диапазон x: от {self.range_start_var.get()} до {self.range_end_var.get()}\n")
                    file.write(f"  Шаг: {self.step_var.get()}\n\n")
                    
                    # Случайные числа
                    file.write("СЛУЧАЙНЫЕ ЧИСЛА:\n")
                    file.write("-" * 40 + "\n")
                    for i, num in enumerate(self.random_numbers, 1):
                        file.write(f"{i:3d}. {num:8.2f}\n")
                    file.write("\n")
                    
                    # Функция
                    file.write(f"ФУНКЦИЯ {self.func_name}(x):\n")
                    file.write("-" * 40 + "\n")
                    file.write("   x\t\t|   f(x)\n")
                    file.write("-" * 40 + "\n")
                    for x, y in zip(self.x_values, self.y_values):
                        if not math.isnan(y):
                            file.write(f"{x:6.3f}\t| {y:10.6f}\n")
                        else:
                            file.write(f"{x:6.3f}\t| не определена\n")
                    file.write("\n")
                    
                    # Статистика
                    file.write("СТАТИСТИКА:\n")
                    file.write("-" * 40 + "\n")
                    stats_text = self.stats_text.get(1.0, tk.END)
                    file.write(stats_text)
                
                self.status_var.set(f"Файл сохранен: {os.path.basename(filename)}")
                messagebox.showinfo("Успех", f"Данные успешно сохранены в файл:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")
                self.status_var.set("Ошибка при сохранении")
    
    def clear_all(self):
        self.random_text.delete(1.0, tk.END)
        self.math_text.delete(1.0, tk.END)
        self.stats_text.delete(1.0, tk.END)
        self.random_numbers = []
        self.x_values = []
        self.y_values = []
        self.status_var.set("Данные очищены")

def main():
    root = tk.Tk()
    app = DataGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()