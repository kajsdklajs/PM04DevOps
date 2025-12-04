import random
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class OscilloscopeDataGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор данных для осциллографа EWB")
        self.root.geometry("1000x800")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="ГЕНЕРАТОР ДАННЫХ ДЛЯ ОСЦИЛЛОГРАФА EWB", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Фрейм параметров
        params_frame = ttk.LabelFrame(main_frame, text="Параметры сигнала", padding="10")
        params_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Сетка для параметров
        params_grid = ttk.Frame(params_frame)
        params_grid.pack(fill=tk.X)
        
        # Временные параметры
        ttk.Label(params_grid, text="Шаг по времени (сек):").grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.time_step_var = tk.StringVar(value="0.001")
        ttk.Entry(params_grid, textvariable=self.time_step_var, width=12).grid(row=0, column=1, padx=(0, 20), pady=5)
        
        ttk.Label(params_grid, text="Длительность (сек):").grid(row=0, column=2, sticky=tk.W, padx=(0, 10), pady=5)
        self.duration_var = tk.StringVar(value="0.01")
        ttk.Entry(params_grid, textvariable=self.duration_var, width=12).grid(row=0, column=3, padx=(0, 20), pady=5)
        
        ttk.Label(params_grid, text="Количество бит:").grid(row=0, column=4, sticky=tk.W, padx=(0, 10), pady=5)
        self.num_bits_var = tk.StringVar(value="8")
        ttk.Entry(params_grid, textvariable=self.num_bits_var, width=8).grid(row=0, column=5, pady=5)
        
        # Фрейм для битовой последовательности
        bits_frame = ttk.LabelFrame(params_frame, text="Битовая последовательность", padding="10")
        bits_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Способ ввода битов
        method_frame = ttk.Frame(bits_frame)
        method_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(method_frame, text="Способ формирования:").pack(side=tk.LEFT)
        self.bit_method_var = tk.StringVar(value="random")
        ttk.Radiobutton(method_frame, text="Случайно", variable=self.bit_method_var, 
                       value="random", command=self.toggle_bit_input).pack(side=tk.LEFT, padx=(20, 10))
        ttk.Radiobutton(method_frame, text="Вручную", variable=self.bit_method_var, 
                       value="manual", command=self.toggle_bit_input).pack(side=tk.LEFT, padx=10)
        
        # Поле для ручного ввода битов
        self.manual_bits_frame = ttk.Frame(bits_frame)
        self.manual_bits_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.manual_bits_frame, text="Биты (0 и 1):").pack(side=tk.LEFT)
        self.bits_entry_var = tk.StringVar()
        self.bits_entry = ttk.Entry(self.manual_bits_frame, textvariable=self.bits_entry_var, width=30)
        self.bits_entry.pack(side=tk.LEFT, padx=10)
        
        # Кнопка генерации случайных битов
        ttk.Button(self.manual_bits_frame, text="Сгенерировать", 
                  command=self.generate_random_bits_display).pack(side=tk.LEFT, padx=10)
        
        # Случайные биты изначально скрыты
        self.manual_bits_frame.pack_forget()
        
        # Отображение текущей битовой последовательности
        self.bits_display_frame = ttk.Frame(bits_frame)
        self.bits_display_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.bits_display_frame, text="Текущая последовательность:").pack(side=tk.LEFT)
        self.bits_display_var = tk.StringVar(value="Не сгенерирована")
        bits_display_label = ttk.Label(self.bits_display_frame, textvariable=self.bits_display_var, 
                                      font=('Courier', 10), background='white', relief='sunken')
        bits_display_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Фрейм кнопок
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="Сгенерировать данные", 
                  command=self.generate_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Показать график", 
                  command=self.show_plot).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Сохранить в файл", 
                  command=self.save_to_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Очистить", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # Фрейм для отображения данных и графика
        display_frame = ttk.LabelFrame(main_frame, text="Результаты", padding="10")
        display_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Вкладки
        notebook = ttk.Notebook(display_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка данных
        data_tab = ttk.Frame(notebook)
        notebook.add(data_tab, text="Данные осциллографа")
        self.data_text = scrolledtext.ScrolledText(data_tab, width=80, height=12, font=('Courier', 9))
        self.data_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Вкладка графика
        plot_tab = ttk.Frame(notebook)
        notebook.add(plot_tab, text="График сигнала")
        self.setup_plot_tab(plot_tab)
        
        # Вкладка превью файла
        preview_tab = ttk.Frame(notebook)
        notebook.add(preview_tab, text="Превью файла")
        self.preview_text = scrolledtext.ScrolledText(preview_tab, width=80, height=12, font=('Courier', 9))
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Вкладка информации
        info_tab = ttk.Frame(notebook)
        notebook.add(info_tab, text="Информация")
        self.info_text = scrolledtext.ScrolledText(info_tab, width=80, height=12)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Данные
        self.time_data = []
        self.voltage_data = []
        self.bits = []
        self.filename = ""
        
        # Сгенерировать начальные случайные биты
        self.generate_random_bits_display()
        
    def setup_plot_tab(self, parent):
        """Настройка вкладки с графиком"""
        # Фрейм для управления графиком
        plot_controls_frame = ttk.Frame(parent)
        plot_controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(plot_controls_frame, text="Обновить график", 
                  command=self.update_plot).pack(side=tk.LEFT, padx=5)
        ttk.Button(plot_controls_frame, text="Сохранить график", 
                  command=self.save_plot).pack(side=tk.LEFT, padx=5)
        
        # Настройки отображения
        ttk.Label(plot_controls_frame, text="Стиль линии:").pack(side=tk.LEFT, padx=(20, 5))
        self.line_style_var = tk.StringVar(value="step")
        line_combo = ttk.Combobox(plot_controls_frame, textvariable=self.line_style_var, 
                                 values=["step", "line", "stem"], width=8)
        line_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(plot_controls_frame, text="Цвет:").pack(side=tk.LEFT, padx=(20, 5))
        self.line_color_var = tk.StringVar(value="blue")
        color_combo = ttk.Combobox(plot_controls_frame, textvariable=self.line_color_var, 
                                  values=["blue", "red", "green", "purple", "orange"], width=8)
        color_combo.pack(side=tk.LEFT, padx=5)
        
        # Фрейм для графика
        plot_frame = ttk.Frame(parent)
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Создание фигуры matplotlib
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Холст для графика
        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Начальный пустой график
        self.ax.set_title("График сигнала осциллографа")
        self.ax.set_xlabel("Время (сек)")
        self.ax.set_ylabel("Напряжение (V)")
        self.ax.grid(True, alpha=0.3)
        self.ax.set_ylim(-1, 6)
        self.canvas.draw()
    
    def toggle_bit_input(self):
        """Переключение между ручным и автоматическим вводом битов"""
        if self.bit_method_var.get() == "manual":
            self.manual_bits_frame.pack(fill=tk.X, pady=5)
            # Установить текущие биты в поле ввода
            self.bits_entry_var.set(''.join(str(bit) for bit in self.bits))
        else:
            self.manual_bits_frame.pack_forget()
            self.generate_random_bits_display()
    
    def generate_random_bits_display(self):
        """Генерация и отображение случайных битов"""
        try:
            num_bits = int(self.num_bits_var.get())
            if num_bits <= 0:
                messagebox.showerror("Ошибка", "Количество бит должно быть положительным")
                return
                
            self.bits = [random.randint(0, 1) for _ in range(num_bits)]
            bit_string = ''.join(str(bit) for bit in self.bits)
            self.bits_display_var.set(bit_string)
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное количество бит")
    
    def get_bits_from_input(self):
        """Получение битовой последовательности из выбранного метода"""
        if self.bit_method_var.get() == "manual":
            # Получение битов из ручного ввода
            bit_string = self.bits_entry_var.get().strip()
            if not bit_string:
                messagebox.showerror("Ошибка", "Введите битовую последовательность")
                return None
            
            # Проверка корректности
            if not all(bit in '01' for bit in bit_string):
                messagebox.showerror("Ошибка", "Битовая последовательность должна содержать только 0 и 1")
                return None
            
            expected_bits = int(self.num_bits_var.get())
            if len(bit_string) != expected_bits:
                messagebox.showerror("Ошибка", f"Ожидается {expected_bits} бит, получено {len(bit_string)}")
                return None
            
            self.bits = [int(bit) for bit in bit_string]
            self.bits_display_var.set(bit_string)
        
        return self.bits
    
    def generate_data(self):
        """Генерация данных осциллографа"""
        try:
            self.status_var.set("Генерация данных...")
            self.root.update()
            
            # Получение параметров
            time_step = float(self.time_step_var.get())
            duration = float(self.duration_var.get())
            num_bits = int(self.num_bits_var.get())
            
            if time_step <= 0 or duration <= 0 or num_bits <= 0:
                messagebox.showerror("Ошибка", "Все параметры должны быть положительными")
                return
            
            # Получение битовой последовательности
            bits = self.get_bits_from_input()
            if bits is None:
                return
            
            # Генерация данных времени и напряжения
            self.time_data, self.voltage_data = self.generate_time_voltage_data(bits, time_step, duration)
            
            # Отображение данных
            self.display_data()
            
            # Обновление графика
            self.update_plot()
            
            # Создание превью файла
            self.create_file_preview(time_step, duration, num_bits)
            
            # Обновление информации
            self.update_info(time_step, duration, num_bits)
            
            self.status_var.set("Данные успешно сгенерированы")
            
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", "Проверьте правильность введенных значений")
            self.status_var.set("Ошибка ввода данных")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
            self.status_var.set("Ошибка при генерации данных")
    
    def generate_time_voltage_data(self, bits, time_step, duration):
        """Генерация массивов времени и напряжения"""
        time_data = []
        voltage_data = []
        
        # Расчет времени на один бит
        bit_duration = duration / len(bits)
        
        current_time = 0.0
        while current_time <= duration:
            time_data.append(current_time)
            
            # Определяем текущий бит
            current_bit_index = int(current_time / bit_duration)
            if current_bit_index >= len(bits):
                current_bit_index = len(bits) - 1
            
            # Преобразуем бит в напряжение (0V для 0, 5V для 1)
            voltage = 5.0 if bits[current_bit_index] == 1 else 0.0
            voltage_data.append(voltage)
            
            current_time += time_step
            current_time = round(current_time, 10)  # Округление для избежания ошибок точности
        
        return time_data, voltage_data
    
    def display_data(self):
        """Отображение данных в текстовом поле"""
        self.data_text.delete(1.0, tk.END)
        
        # Заголовок таблицы
        self.data_text.insert(tk.END, f"{'Time (sec)':<12} {'V1 (Volts)':<12}\n")
        self.data_text.insert(tk.END, "-" * 25 + "\n")
        
        # Данные таблицы (первые 50 строк)
        display_count = min(50, len(self.time_data))
        for i in range(display_count):
            time = self.time_data[i]
            voltage = self.voltage_data[i]
            self.data_text.insert(tk.END, f"{time:<12.6f} {voltage:<12.1f}\n")
        
        if len(self.time_data) > display_count:
            self.data_text.insert(tk.END, f"... и еще {len(self.time_data) - display_count} строк\n")
    
    def update_plot(self):
        """Обновление графика сигнала"""
        if not self.time_data or not self.voltage_data:
            return
        
        try:
            self.ax.clear()
            
            # Настройка стиля графика
            line_style = self.line_style_var.get()
            color = self.line_color_var.get()
            
            if line_style == "step":
                # Ступенчатый график для цифровых сигналов
                self.ax.step(self.time_data, self.voltage_data, 
                           where='post', linewidth=2, color=color, label='Цифровой сигнал')
            elif line_style == "stem":
                # Stem plot
                markerline, stemlines, baseline = self.ax.stem(self.time_data, self.voltage_data, 
                                                             basefmt=" ", use_line_collection=True)
                plt.setp(stemlines, 'color', color, 'linewidth', 2)
                plt.setp(markerline, 'color', color, 'markersize', 4)
            else:
                # Обычный линейный график
                self.ax.plot(self.time_data, self.voltage_data, 
                           linewidth=2, color=color, label='Сигнал')
            
            # Настройки графика
            self.ax.set_title(f"Цифровой сигнал: {''.join(str(bit) for bit in self.bits)}", fontsize=12)
            self.ax.set_xlabel("Время (сек)", fontsize=10)
            self.ax.set_ylabel("Напряжение (V)", fontsize=10)
            self.ax.grid(True, alpha=0.3)
            self.ax.set_ylim(-0.5, 5.5)
            
            # Добавление горизонтальных линий для уровней напряжения
            self.ax.axhline(y=5.0, color='green', linestyle='--', alpha=0.5, label='Высокий уровень (5V)')
            self.ax.axhline(y=0.0, color='red', linestyle='--', alpha=0.5, label='Низкий уровень (0V)')
            
            # Легенда
            self.ax.legend(loc='upper right')
            
            # Форматирование осей
            self.ax.tick_params(axis='both', which='major', labelsize=8)
            
            # Автоматическое масштабирование по X
            if self.time_data:
                margin = (self.time_data[-1] - self.time_data[0]) * 0.05
                self.ax.set_xlim(self.time_data[0] - margin, self.time_data[-1] + margin)
            
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Ошибка графика", f"Не удалось построить график: {e}")
    
    def show_plot(self):
        """Показать график в отдельном окне"""
        if not self.time_data:
            messagebox.showwarning("Предупреждение", "Сначала сгенерируйте данные")
            return
        
        try:
            # Создание отдельного окна для графика
            plot_window = tk.Toplevel(self.root)
            plot_window.title("График цифрового сигнала")
            plot_window.geometry("800x600")
            
            # Создание фигуры для отдельного окна
            fig = Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            # Построение графика
            ax.step(self.time_data, self.voltage_data, where='post', linewidth=2, color='blue')
            ax.set_title(f"Цифровой сигнал: {''.join(str(bit) for bit in self.bits)}", fontsize=14)
            ax.set_xlabel("Время (сек)", fontsize=12)
            ax.set_ylabel("Напряжение (V)", fontsize=12)
            ax.grid(True, alpha=0.3)
            ax.set_ylim(-0.5, 5.5)
            
            # Добавление линий уровней
            ax.axhline(y=5.0, color='green', linestyle='--', alpha=0.7, label='Высокий уровень (5V)')
            ax.axhline(y=0.0, color='red', linestyle='--', alpha=0.7, label='Низкий уровень (0V)')
            ax.legend()
            
            # Холст для графика
            canvas = FigureCanvasTkAgg(fig, plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Кнопка сохранения
            save_button = ttk.Button(plot_window, text="Сохранить график", 
                                   command=lambda: self.save_plot_figure(fig))
            save_button.pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать окно графика: {e}")
    
    def save_plot(self):
        """Сохранение текущего графика"""
        if not self.time_data:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения графика")
            return
        
        self.save_plot_figure(self.fig)
    
    def save_plot_figure(self, fig):
        """Сохранение указанной фигуры"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("PDF files", "*.pdf"),
                ("SVG files", "*.svg")
            ],
            title="Сохранить график"
        )
        
        if filename:
            try:
                fig.savefig(filename, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Успех", f"График сохранен в файл:\n{filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить график: {e}")
    
    def create_file_preview(self, time_step, duration, num_bits):
        """Создание превью файла"""
        self.preview_text.delete(1.0, tk.END)
        
        method_name = "Manual" if self.bit_method_var.get() == "manual" else "Random"
        
        self.preview_text.insert(tk.END, "OSCILLOSCOPE DATA FOR EWB\n")
        self.preview_text.insert(tk.END, "=" * 40 + "\n")
        self.preview_text.insert(tk.END, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.preview_text.insert(tk.END, f"Time step: {time_step} sec\n")
        self.preview_text.insert(tk.END, f"Duration: {duration} sec\n")
        self.preview_text.insert(tk.END, f"Number of bits: {num_bits}\n")
        self.preview_text.insert(tk.END, f"Generation method: {method_name}\n")
        self.preview_text.insert(tk.END, f"Bit sequence: {''.join(str(bit) for bit in self.bits)}\n")
        self.preview_text.insert(tk.END, "=" * 40 + "\n\n")
        
        self.preview_text.insert(tk.END, f"{'Time (sec)':<12} {'V1 (Volts)':<12}\n")
        self.preview_text.insert(tk.END, "-" * 25 + "\n")
        
        # Показываем первые 20 строк в превью
        preview_count = min(20, len(self.time_data))
        for i in range(preview_count):
            time = self.time_data[i]
            voltage = self.voltage_data[i]
            self.preview_text.insert(tk.END, f"{time:<12.6f} {voltage:<12.1f}\n")
        
        if len(self.time_data) > preview_count:
            self.preview_text.insert(tk.END, f"... и еще {len(self.time_data) - preview_count} строк\n")
    
    def update_info(self, time_step, duration, num_bits):
        """Обновление информации о данных"""
        self.info_text.delete(1.0, tk.END)
        
        self.info_text.insert(tk.END, "ИНФОРМАЦИЯ О ДАННЫХ\n")
        self.info_text.insert(tk.END, "=" * 40 + "\n\n")
        
        self.info_text.insert(tk.END, f"Общее количество точек: {len(self.time_data)}\n")
        self.info_text.insert(tk.END, f"Длительность сигнала: {duration} сек\n")
        self.info_text.insert(tk.END, f"Шаг дискретизации: {time_step} сек\n")
        self.info_text.insert(tk.END, f"Частота дискретизации: {1/time_step:.1f} Гц\n")
        self.info_text.insert(tk.END, f"Количество бит: {num_bits}\n")
        self.info_text.insert(tk.END, f"Длительность одного бита: {duration/num_bits:.6f} сек\n")
        self.info_text.insert(tk.END, f"Битовая последовательность: {''.join(str(bit) for bit in self.bits)}\n\n")
        
        # Статистика по напряжениям
        high_count = sum(1 for v in self.voltage_data if v == 5.0)
        low_count = sum(1 for v in self.voltage_data if v == 0.0)
        
        self.info_text.insert(tk.END, "СТАТИСТИКА НАПРЯЖЕНИЙ:\n")
        self.info_text.insert(tk.END, f"  Высокий уровень (5V): {high_count} точек ({high_count/len(self.voltage_data)*100:.1f}%)\n")
        self.info_text.insert(tk.END, f"  Низкий уровень (0V): {low_count} точек ({low_count/len(self.voltage_data)*100:.1f}%)\n")
    
    def save_to_file(self):
        """Сохранение данных в файл"""
        if not self.time_data:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
            title="Сохранить данные осциллографа",
            initialfile=f"oscilloscope_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    # Записываем содержимое из превью
                    file_content = self.preview_text.get(1.0, tk.END)
                    file.write(file_content)
                    
                    # Добавляем оставшиеся данные
                    if len(self.time_data) > 20:
                        file.write("\n... ПОЛНЫЕ ДАННЫХ ...\n\n")
                        file.write(f"{'Time (sec)':<12} {'V1 (Volts)':<12}\n")
                        file.write("-" * 25 + "\n")
                        for time, voltage in zip(self.time_data, self.voltage_data):
                            file.write(f"{time:<12.6f} {voltage:<12.1f}\n")
                
                self.filename = filename
                self.status_var.set(f"Файл сохранен: {os.path.basename(filename)}")
                messagebox.showinfo("Успех", f"Данные успешно сохранены в файл:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")
                self.status_var.set("Ошибка при сохранении")
    
    def clear_all(self):
        """Очистка всех данных"""
        self.data_text.delete(1.0, tk.END)
        self.preview_text.delete(1.0, tk.END)
        self.info_text.delete(1.0, tk.END)
        self.time_data = []
        self.voltage_data = []
        self.bits = []
        self.filename = ""
        
        # Очистка графика
        self.ax.clear()
        self.ax.set_title("График сигнала осциллографа")
        self.ax.set_xlabel("Время (сек)")
        self.ax.set_ylabel("Напряжение (V)")
        self.ax.grid(True, alpha=0.3)
        self.ax.set_ylim(-1, 6)
        self.canvas.draw()
        
        self.status_var.set("Данные очищены")

def main():
    # Проверка наличия matplotlib
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Библиотека matplotlib не установлена. Установите её с помощью:")
        print("pip install matplotlib")
        return
    
    root = tk.Tk()
    app = OscilloscopeDataGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()