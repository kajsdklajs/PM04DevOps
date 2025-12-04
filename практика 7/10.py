import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.widgets import Button, RadioButtons, Slider
import tkinter as tk
from tkinter import filedialog, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import warnings
warnings.filterwarnings('ignore')

class DataVisualizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализатор и Визуализатор Данных")
        self.root.geometry("1400x900")
        
        self.data = None
        self.current_chart_type = "line"
        self.current_x_column = None
        self.current_y_column = None
        self.color_palette = "viridis"
        
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основные фреймы
        self.control_frame = ttk.Frame(self.root, width=300)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заголовок
        title_label = ttk.Label(self.control_frame, text="Визуализатор Данных", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Кнопка загрузки данных
        self.load_btn = ttk.Button(self.control_frame, text="Загрузить CSV файл", 
                                  command=self.load_data)
        self.load_btn.pack(pady=5, fill=tk.X)
        
        # Информация о данных
        self.data_info = ttk.Label(self.control_frame, text="Данные не загружены", 
                                  font=('Arial', 10))
        self.data_info.pack(pady=5)
        
        # Выбор типа диаграммы
        self.setup_chart_controls()
        
        # Выбор колонок
        self.setup_column_controls()
        
        # Настройки визуализации
        self.setup_visualization_controls()
        
        # Кнопка генерации графика
        self.generate_btn = ttk.Button(self.control_frame, text="Создать график", 
                                      command=self.generate_plot)
        self.generate_btn.pack(pady=10, fill=tk.X)
        
        # Область для статистики
        self.setup_statistics_frame()
        
        # Инициализация области для графика
        self.setup_plot_area()
        
    def setup_chart_controls(self):
        """Настройка выбора типа диаграммы"""
        chart_frame = ttk.LabelFrame(self.control_frame, text="Тип диаграммы", padding=10)
        chart_frame.pack(pady=10, fill=tk.X)
        
        self.chart_var = tk.StringVar(value="line")
        
        charts = [
            ("Линейный график", "line"),
            ("Столбчатая диаграмма", "bar"),
            ("Гистограмма", "hist"),
            ("Диаграмма рассеяния", "scatter"),
            ("Круговая диаграмма", "pie"),
            ("Ящик с усами", "box"),
            ("Тепловая карта", "heatmap"),
            ("Парные диаграммы", "pairplot"),
            ("График плотности", "kde")
        ]
        
        for text, value in charts:
            ttk.Radiobutton(chart_frame, text=text, variable=self.chart_var, 
                           value=value, command=self.on_chart_change).pack(anchor=tk.W)
    
    def setup_column_controls(self):
        """Настройка выбора колонок"""
        self.column_frame = ttk.LabelFrame(self.control_frame, text="Выбор данных", padding=10)
        self.column_frame.pack(pady=10, fill=tk.X)
        
        # X-axis
        ttk.Label(self.column_frame, text="Ось X:").pack(anchor=tk.W)
        self.x_var = tk.StringVar()
        self.x_combo = ttk.Combobox(self.column_frame, textvariable=self.x_var, state="readonly")
        self.x_combo.pack(fill=tk.X, pady=2)
        
        # Y-axis
        ttk.Label(self.column_frame, text="Ось Y:").pack(anchor=tk.W, pady=(10,0))
        self.y_var = tk.StringVar()
        self.y_combo = ttk.Combobox(self.column_frame, textvariable=self.y_var, state="readonly")
        self.y_combo.pack(fill=tk.X, pady=2)
        
        # Для гистограмм и круговых диаграмм
        ttk.Label(self.column_frame, text="Для гистограммы/круговой:").pack(anchor=tk.W, pady=(10,0))
        self.single_var = tk.StringVar()
        self.single_combo = ttk.Combobox(self.column_frame, textvariable=self.single_var, state="readonly")
        self.single_combo.pack(fill=tk.X, pady=2)
    
    def setup_visualization_controls(self):
        """Настройки визуализации"""
        viz_frame = ttk.LabelFrame(self.control_frame, text="Настройки отображения", padding=10)
        viz_frame.pack(pady=10, fill=tk.X)
        
        # Цветовая палитра
        ttk.Label(viz_frame, text="Цветовая схема:").pack(anchor=tk.W)
        self.color_var = tk.StringVar(value="viridis")
        color_combo = ttk.Combobox(viz_frame, textvariable=self.color_var, state="readonly")
        color_combo['values'] = ['viridis', 'plasma', 'inferno', 'magma', 'coolwarm', 'Set1', 'Set2', 'Set3']
        color_combo.pack(fill=tk.X, pady=2)
        
        # Размер графика
        ttk.Label(viz_frame, text="Размер графика:").pack(anchor=tk.W, pady=(10,0))
        self.size_var = tk.StringVar(value="medium")
        size_combo = ttk.Combobox(viz_frame, textvariable=self.size_var, state="readonly")
        size_combo['values'] = ['small', 'medium', 'large', 'x-large']
        size_combo.pack(fill=tk.X, pady=2)
        
        # Прозрачность
        ttk.Label(viz_frame, text="Прозрачность:").pack(anchor=tk.W, pady=(10,0))
        self.alpha_var = tk.DoubleVar(value=0.7)
        alpha_scale = ttk.Scale(viz_frame, from_=0.1, to=1.0, variable=self.alpha_var, 
                               orient=tk.HORIZONTAL)
        alpha_scale.pack(fill=tk.X, pady=2)
    
    def setup_statistics_frame(self):
        """Настройка области статистики"""
        stats_frame = ttk.LabelFrame(self.control_frame, text="Статистика данных", padding=10)
        stats_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.stats_text = tk.Text(stats_frame, height=15, width=35, font=('Courier', 9))
        scrollbar = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=scrollbar.set)
        
        self.stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_plot_area(self):
        """Настройка области для графиков"""
        self.fig = Figure(figsize=(10, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Начальное сообщение
        self.show_welcome_message()
    
    def show_welcome_message(self):
        """Показать приветственное сообщение"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.text(0.5, 0.5, 'Добро пожаловать в Визуализатор Данных!\n\n'
                         'Загрузите CSV файл для начала работы.\n'
                         'Поддерживаемые типы диаграмм:\n'
                         '• Линейные графики\n• Столбчатые диаграммы\n• Гистограммы\n'
                         '• Диаграммы рассеяния\n• Круговые диаграммы\n• Ящики с усами\n'
                         '• Тепловые карты\n• Парные диаграммы\n• Графики плотности',
               horizontalalignment='center', verticalalignment='center',
               transform=ax.transAxes, fontsize=14, 
               bbox=dict(boxstyle="round,pad=1", facecolor="lightblue"))
        ax.set_axis_off()
        self.canvas.draw()
    
    def load_data(self):
        """Загрузка данных из CSV файла"""
        file_path = filedialog.askopenfilename(
            title="Выберите CSV файл",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                self.update_data_info()
                self.update_column_combos()
                self.update_statistics()
                self.show_data_preview()
            except Exception as e:
                tk.messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")
    
    def update_data_info(self):
        """Обновление информации о данных"""
        if self.data is not None:
            info_text = f"Данные: {len(self.data)} строк × {len(self.data.columns)} колонок\n"
            info_text += f"Колонки: {', '.join(self.data.columns[:5])}"
            if len(self.data.columns) > 5:
                info_text += "..."
            self.data_info.config(text=info_text)
    
    def update_column_combos(self):
        """Обновление выпадающих списков колонок"""
        if self.data is not None:
            columns = list(self.data.columns)
            self.x_combo['values'] = columns
            self.y_combo['values'] = columns
            self.single_combo['values'] = columns
            
            # Автовыбор первых колонок
            if len(columns) >= 1:
                self.x_var.set(columns[0])
                if len(columns) >= 2:
                    self.y_var.set(columns[1])
                self.single_var.set(columns[0])
    
    def update_statistics(self):
        """Обновление статистики"""
        if self.data is not None:
            stats = "СТАТИСТИКА ДАННЫХ:\n\n"
            stats += f"Размер: {self.data.shape[0]} × {self.data.shape[1]}\n"
            stats += f"Типы данных:\n"
            
            for col in self.data.columns:
                dtype = self.data[col].dtype
                null_count = self.data[col].isnull().sum()
                stats += f"  {col}: {dtype} (пустых: {null_count})\n"
            
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                stats += f"\nЧисловые колонки ({len(numeric_cols)}):\n"
                for col in numeric_cols[:5]:  # Показываем первые 5
                    col_stats = self.data[col].describe()
                    stats += f"  {col}:\n"
                    stats += f"    Мин: {col_stats['min']:.2f}\n"
                    stats += f"    Макс: {col_stats['max']:.2f}\n"
                    stats += f"    Среднее: {col_stats['mean']:.2f}\n"
            
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, stats)
    
    def show_data_preview(self):
        """Показать предварительный просмотр данных"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        # Показываем первые несколько строк данных
        preview_data = self.data.head(10)
        
        # Создаем таблицу
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=preview_data.values,
                        colLabels=preview_data.columns,
                        cellLoc='center',
                        loc='center')
        
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1.2, 1.5)
        
        ax.set_title('Предварительный просмотр данных (первые 10 строк)', 
                    fontsize=14, pad=20)
        
        self.canvas.draw()
    
    def on_chart_change(self):
        """Обработчик изменения типа диаграммы"""
        chart_type = self.chart_var.get()
        
        # Скрываем/показываем соответствующие элементы управления
        if chart_type in ['hist', 'pie', 'kde']:
            self.y_combo.config(state='disabled')
            self.single_combo.config(state='readonly')
        else:
            self.y_combo.config(state='readonly')
            self.single_combo.config(state='disabled')
    
    def generate_plot(self):
        """Генерация графика"""
        if self.data is None:
            tk.messagebox.showwarning("Предупреждение", "Сначала загрузите данные!")
            return
        
        try:
            self.fig.clear()
            chart_type = self.chart_var.get()
            
            if chart_type == "line":
                self.create_line_plot()
            elif chart_type == "bar":
                self.create_bar_plot()
            elif chart_type == "hist":
                self.create_histogram()
            elif chart_type == "scatter":
                self.create_scatter_plot()
            elif chart_type == "pie":
                self.create_pie_chart()
            elif chart_type == "box":
                self.create_box_plot()
            elif chart_type == "heatmap":
                self.create_heatmap()
            elif chart_type == "pairplot":
                self.create_pairplot()
            elif chart_type == "kde":
                self.create_kde_plot()
            
            self.canvas.draw()
            
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Не удалось создать график: {str(e)}")
    
    def create_line_plot(self):
        """Создание линейного графика"""
        x_col = self.x_var.get()
        y_col = self.y_var.get()
        
        ax = self.fig.add_subplot(111)
        
        # Пытаемся преобразовать к числовому типу если нужно
        try:
            x_data = pd.to_numeric(self.data[x_col])
        except:
            x_data = self.data[x_col]
        
        y_data = pd.to_numeric(self.data[y_col])
        
        ax.plot(x_data, y_data, alpha=self.alpha_var.get(), 
               linewidth=2, marker='o', markersize=4)
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f'Линейный график: {y_col} vs {x_col}')
        ax.grid(True, alpha=0.3)
        ax.legend([f'{y_col} vs {x_col}'])
    
    def create_bar_plot(self):
        """Создание столбчатой диаграммы"""
        x_col = self.x_var.get()
        y_col = self.y_var.get()
        
        ax = self.fig.add_subplot(111)
        
        # Группируем данные для столбцов
        bar_data = self.data.groupby(x_col)[y_col].mean()
        
        bars = ax.bar(bar_data.index, bar_data.values, alpha=self.alpha_var.get(),
                     color=plt.cm.get_cmap(self.color_var.get())(np.linspace(0, 1, len(bar_data))))
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(f'Среднее {y_col}')
        ax.set_title(f'Столбчатая диаграмма: {y_col} по {x_col}')
        ax.tick_params(axis='x', rotation=45)
        
        # Добавляем значения на столбцы
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}', ha='center', va='bottom')
    
    def create_histogram(self):
        """Создание гистограммы"""
        col = self.single_var.get()
        
        ax = self.fig.add_subplot(111)
        
        numeric_data = pd.to_numeric(self.data[col], errors='coerce').dropna()
        
        ax.hist(numeric_data, bins=20, alpha=self.alpha_var.get(), 
               color=plt.cm.get_cmap(self.color_var.get())(0.5),
               edgecolor='black')
        
        ax.set_xlabel(col)
        ax.set_ylabel('Частота')
        ax.set_title(f'Гистограмма: распределение {col}')
        ax.grid(True, alpha=0.3)
    
    def create_scatter_plot(self):
        """Создание диаграммы рассеяния"""
        x_col = self.x_var.get()
        y_col = self.y_var.get()
        
        ax = self.fig.add_subplot(111)
        
        x_data = pd.to_numeric(self.data[x_col], errors='coerce')
        y_data = pd.to_numeric(self.data[y_col], errors='coerce')
        
        scatter = ax.scatter(x_data, y_data, alpha=self.alpha_var.get(), 
                           c=np.arange(len(x_data)), cmap=self.color_var.get())
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f'Диаграмма рассеяния: {y_col} vs {x_col}')
        ax.grid(True, alpha=0.3)
        
        # Добавляем цветовую шкалу
        plt.colorbar(scatter, ax=ax, label='Индекс точки')
    
    def create_pie_chart(self):
        """Создание круговой диаграммы"""
        col = self.single_var.get()
        
        ax = self.fig.add_subplot(111)
        
        value_counts = self.data[col].value_counts().head(8)  # Ограничиваем до 8 категорий
        
        colors = plt.cm.get_cmap(self.color_var.get())(np.linspace(0, 1, len(value_counts)))
        
        wedges, texts, autotexts = ax.pie(value_counts.values, labels=value_counts.index,
                                         autopct='%1.1f%%', colors=colors,
                                         startangle=90, shadow=True)
        
        # Улучшаем читаемость текста
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title(f'Круговая диаграмма: распределение {col}')
        ax.axis('equal')  # Чтобы круг был круглым
    
    def create_box_plot(self):
        """Создание ящика с усами"""
        x_col = self.x_var.get()
        y_col = self.y_var.get()
        
        ax = self.fig.add_subplot(111)
        
        # Группируем данные для boxplot
        plot_data = []
        labels = []
        for category in self.data[x_col].unique()[:10]:  # Ограничиваем количество категорий
            subset = self.data[self.data[x_col] == category][y_col]
            if len(subset) > 0:
                plot_data.append(pd.to_numeric(subset, errors='coerce').dropna())
                labels.append(str(category))
        
        box_plot = ax.boxplot(plot_data, labels=labels, patch_artist=True)
        
        # Раскрашиваем ящики
        colors = plt.cm.get_cmap(self.color_var.get())(np.linspace(0, 1, len(plot_data)))
        for patch, color in zip(box_plot['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(self.alpha_var.get())
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f'Ящик с усами: {y_col} по {x_col}')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)
    
    def create_heatmap(self):
        """Создание тепловой карты корреляций"""
        ax = self.fig.add_subplot(111)
        
        # Выбираем только числовые колонки
        numeric_data = self.data.select_dtypes(include=[np.number])
        
        if len(numeric_data.columns) < 2:
            raise ValueError("Нужно как минимум 2 числовые колонки для тепловой карты")
        
        # Вычисляем корреляционную матрицу
        corr_matrix = numeric_data.corr()
        
        # Создаем heatmap
        im = ax.imshow(corr_matrix, cmap=self.color_var.get(), aspect='auto')
        
        # Настройки осей
        ax.set_xticks(np.arange(len(corr_matrix.columns)))
        ax.set_yticks(np.arange(len(corr_matrix.columns)))
        ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
        ax.set_yticklabels(corr_matrix.columns)
        
        # Добавляем значения в ячейки
        for i in range(len(corr_matrix.columns)):
            for j in range(len(corr_matrix.columns)):
                ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                       ha="center", va="center", color="black" if abs(corr_matrix.iloc[i, j]) < 0.5 else "white")
        
        ax.set_title('Тепловая карта корреляций')
        plt.colorbar(im, ax=ax, label='Коэффициент корреляции')
    
    def create_pairplot(self):
        """Создание парных диаграмм"""
        numeric_data = self.data.select_dtypes(include=[np.number])
        
        if len(numeric_data.columns) < 2:
            raise ValueError("Нужно как минимум 2 числовые колонки для парных диаграмм")
        
        # Ограничиваем количество колонок для производительности
        if len(numeric_data.columns) > 5:
            numeric_data = numeric_data.iloc[:, :5]
        
        n_cols = len(numeric_data.columns)
        
        for i, col1 in enumerate(numeric_data.columns):
            for j, col2 in enumerate(numeric_data.columns):
                ax = self.fig.add_subplot(n_cols, n_cols, i * n_cols + j + 1)
                
                if i == j:
                    # Диагональ - гистограммы
                    ax.hist(numeric_data[col1], bins=15, alpha=0.7)
                    ax.set_title(col1, fontsize=10)
                else:
                    # Вне диагонали - scatter plots
                    ax.scatter(numeric_data[col2], numeric_data[col1], 
                              alpha=0.6, s=20)
                
                if i == n_cols - 1:
                    ax.set_xlabel(col2, fontsize=8)
                if j == 0:
                    ax.set_ylabel(col1, fontsize=8)
                
                ax.tick_params(labelsize=6)
        
        self.fig.suptitle('Парные диаграммы числовых признаков', fontsize=16)
        self.fig.tight_layout()
    
    def create_kde_plot(self):
        """Создание графика плотности распределения"""
        col = self.single_var.get()
        
        ax = self.fig.add_subplot(111)
        
        numeric_data = pd.to_numeric(self.data[col], errors='coerce').dropna()
        
        numeric_data.plot.kde(ax=ax, linewidth=2)
        ax.hist(numeric_data, bins=30, density=True, alpha=0.3)
        
        ax.set_xlabel(col)
        ax.set_ylabel('Плотность')
        ax.set_title(f'График плотности распределения: {col}')
        ax.grid(True, alpha=0.3)
        ax.legend(['KDE', 'Гистограмма'])

# Запуск приложения
if __name__ == "__main__":
    print("Запуск приложения для визуализации данных...")
    print("Возможности:")
    print("- Загрузка CSV файлов")
    print("- 9 типов диаграмм и графиков")
    print("- Интерактивный выбор данных")
    print("- Статистический анализ")
    print("- Настройка внешнего вида")
    
    root = tk.Tk()
    app = DataVisualizationApp(root)
    root.mainloop()