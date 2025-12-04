import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
from matplotlib.widgets import Slider, Button, RadioButtons
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import warnings
warnings.filterwarnings('ignore')

class Complex3DVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Визуализатор Комплексных Функций")
        self.root.geometry("1400x900")
        
        self.setup_ui()
        self.create_initial_plot()
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основные фреймы
        self.control_frame = ttk.Frame(self.root, width=350)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.visualization_frame = ttk.Frame(self.root)
        self.visualization_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заголовок
        title_label = ttk.Label(self.control_frame, text="3D Визуализатор", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Выбор функции
        self.setup_function_controls()
        
        # Настройки области определения
        self.setup_domain_controls()
        
        # Настройки визуализации
        self.setup_visualization_controls()
        
        # Кнопки управления
        self.setup_action_buttons()
        
        # Информационная панель
        self.setup_info_panel()
        
        # Инициализация 3D графика
        self.setup_3d_plot()
        
    def setup_function_controls(self):
        """Настройка выбора комплексной функции"""
        func_frame = ttk.LabelFrame(self.control_frame, text="Комплексная функция", padding=10)
        func_frame.pack(pady=10, fill=tk.X)
        
        self.function_var = tk.StringVar(value="sin")
        
        functions = [
            ("sin(z) - Синус", "sin"),
            ("cos(z) - Косинус", "cos"),
            ("exp(z) - Экспонента", "exp"),
            ("z² - Квадрат", "square"),
            ("z³ - Куб", "cube"),
            ("1/z - Обратная", "reciprocal"),
            ("log(z) - Логарифм", "log"),
            ("tan(z) - Тангенс", "tan"),
            ("sinh(z) - Гиперболический синус", "sinh")
        ]
        
        for text, value in functions:
            ttk.Radiobutton(func_frame, text=text, variable=self.function_var, 
                           value=value, command=self.update_plot).pack(anchor=tk.W)
        
    def setup_domain_controls(self):
        """Настройки области определения"""
        domain_frame = ttk.LabelFrame(self.control_frame, text="Область определения", padding=10)
        domain_frame.pack(pady=10, fill=tk.X)
        
        # Диапазон по X (действительная часть)
        ttk.Label(domain_frame, text="Действительная ось (Re):").pack(anchor=tk.W)
        
        x_frame = ttk.Frame(domain_frame)
        x_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(x_frame, text="от").pack(side=tk.LEFT)
        self.x_min_var = tk.DoubleVar(value=-2.0)
        x_min_entry = ttk.Entry(x_frame, textvariable=self.x_min_var, width=6)
        x_min_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(x_frame, text="до").pack(side=tk.LEFT)
        self.x_max_var = tk.DoubleVar(value=2.0)
        x_max_entry = ttk.Entry(x_frame, textvariable=self.x_max_var, width=6)
        x_max_entry.pack(side=tk.LEFT, padx=2)
        
        # Диапазон по Y (мнимая часть)
        ttk.Label(domain_frame, text="Мнимая ось (Im):").pack(anchor=tk.W, pady=(10,0))
        
        y_frame = ttk.Frame(domain_frame)
        y_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(y_frame, text="от").pack(side=tk.LEFT)
        self.y_min_var = tk.DoubleVar(value=-2.0)
        y_min_entry = ttk.Entry(y_frame, textvariable=self.y_min_var, width=6)
        y_min_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(y_frame, text="до").pack(side=tk.LEFT)
        self.y_max_var = tk.DoubleVar(value=2.0)
        y_max_entry = ttk.Entry(y_frame, textvariable=self.y_max_var, width=6)
        y_max_entry.pack(side=tk.LEFT, padx=2)
        
        # Количество точек
        ttk.Label(domain_frame, text="Количество точек:").pack(anchor=tk.W, pady=(10,0))
        self.points_var = tk.IntVar(value=50)
        points_combo = ttk.Combobox(domain_frame, textvariable=self.points_var, 
                                   values=[20, 30, 50, 100, 200], state="readonly")
        points_combo.pack(fill=tk.X, pady=2)
        
        # Привязка событий
        x_min_entry.bind('<Return>', self.update_plot)
        x_max_entry.bind('<Return>', self.update_plot)
        y_min_entry.bind('<Return>', self.update_plot)
        y_max_entry.bind('<Return>', self.update_plot)
        points_combo.bind('<<ComboboxSelected>>', self.update_plot)
        
    def setup_visualization_controls(self):
        """Настройки визуализации"""
        viz_frame = ttk.LabelFrame(self.control_frame, text="Настройки отображения", padding=10)
        viz_frame.pack(pady=10, fill=tk.X)
        
        # Тип поверхности
        ttk.Label(viz_frame, text="Тип поверхности:").pack(anchor=tk.W)
        self.surface_type = tk.StringVar(value="surface")
        surface_combo = ttk.Combobox(viz_frame, textvariable=self.surface_type,
                                    values=["surface", "wireframe", "contour", "scatter"],
                                    state="readonly")
        surface_combo.pack(fill=tk.X, pady=2)
        surface_combo.bind('<<ComboboxSelected>>', self.update_plot)
        
        # Отображаемая компонента
        ttk.Label(viz_frame, text="Отображаемая компонента:").pack(anchor=tk.W, pady=(10,0))
        self.component_var = tk.StringVar(value="magnitude")
        component_combo = ttk.Combobox(viz_frame, textvariable=self.component_var,
                                      values=["magnitude", "real", "imaginary", "phase"],
                                      state="readonly")
        component_combo.pack(fill=tk.X, pady=2)
        component_combo.bind('<<ComboboxSelected>>', self.update_plot)
        
        # Цветовая схема
        ttk.Label(viz_frame, text="Цветовая схема:").pack(anchor=tk.W, pady=(10,0))
        self.colormap_var = tk.StringVar(value="viridis")
        colormap_combo = ttk.Combobox(viz_frame, textvariable=self.colormap_var,
                                     values=["viridis", "plasma", "inferno", "magma", "coolwarm", 
                                             "rainbow", "jet", "hsv"],
                                     state="readonly")
        colormap_combo.pack(fill=tk.X, pady=2)
        colormap_combo.bind('<<ComboboxSelected>>', self.update_plot)
        
        # Прозрачность
        ttk.Label(viz_frame, text="Прозрачность:").pack(anchor=tk.W, pady=(10,0))
        self.alpha_var = tk.DoubleVar(value=0.8)
        alpha_scale = ttk.Scale(viz_frame, from_=0.1, to=1.0, variable=self.alpha_var,
                               orient=tk.HORIZONTAL)
        alpha_scale.pack(fill=tk.X, pady=2)
        alpha_scale.bind("<ButtonRelease-1>", self.update_plot)
        
    def setup_action_buttons(self):
        """Кнопки управления"""
        btn_frame = ttk.Frame(self.control_frame)
        btn_frame.pack(pady=10, fill=tk.X)
        
        ttk.Button(btn_frame, text="Обновить график", 
                  command=self.update_plot).pack(fill=tk.X, pady=2)
        
        ttk.Button(btn_frame, text="Сброс вида", 
                  command=self.reset_view).pack(fill=tk.X, pady=2)
        
        ttk.Button(btn_frame, text="Экспорт графика", 
                  command=self.export_plot).pack(fill=tk.X, pady=2)
        
        ttk.Button(btn_frame, text="Анимация", 
                  command=self.toggle_animation).pack(fill=tk.X, pady=2)
        
    def setup_info_panel(self):
        """Информационная панель"""
        info_frame = ttk.LabelFrame(self.control_frame, text="Информация о функции", padding=10)
        info_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.info_text = tk.Text(info_frame, height=15, width=40, font=('Courier', 9))
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def setup_3d_plot(self):
        """Настройка 3D графика"""
        self.fig = Figure(figsize=(10, 8), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.visualization_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Начальные настройки камеры
        self.ax.view_init(elev=30, azim=45)
        
    def create_initial_plot(self):
        """Создание начального графика"""
        self.update_plot()
        
    def complex_function(self, z, func_type):
        """Вычисление комплексной функции"""
        if func_type == "sin":
            return np.sin(z)
        elif func_type == "cos":
            return np.cos(z)
        elif func_type == "exp":
            return np.exp(z)
        elif func_type == "square":
            return z**2
        elif func_type == "cube":
            return z**3
        elif func_type == "reciprocal":
            # Избегаем деления на ноль
            mask = z != 0
            result = np.zeros_like(z, dtype=complex)
            result[mask] = 1 / z[mask]
            return result
        elif func_type == "log":
            # Логарифм с основной ветвью
            mask = z != 0
            result = np.zeros_like(z, dtype=complex)
            result[mask] = np.log(z[mask])
            return result
        elif func_type == "tan":
            return np.tan(z)
        elif func_type == "sinh":
            return np.sinh(z)
        else:
            return np.sin(z)  # По умолчанию
            
    def compute_function_data(self):
        """Вычисление данных для графика"""
        # Создаем сетку в комплексной плоскости
        x_min, x_max = self.x_min_var.get(), self.x_max_var.get()
        y_min, y_max = self.y_min_var.get(), self.y_max_var.get()
        n_points = self.points_var.get()
        
        x = np.linspace(x_min, x_max, n_points)
        y = np.linspace(y_min, y_max, n_points)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        
        # Вычисляем функцию
        func_type = self.function_var.get()
        W = self.complex_function(Z, func_type)
        
        return X, Y, W, func_type
        
    def update_plot(self, event=None):
        """Обновление графика"""
        try:
            self.ax.clear()
            
            X, Y, W, func_type = self.compute_function_data()
            
            # Выбираем отображаемую компоненту
            component = self.component_var.get()
            if component == "magnitude":
                Z_data = np.abs(W)
                zlabel = "|w|"
                component_desc = "Модуль"
            elif component == "real":
                Z_data = np.real(W)
                zlabel = "Re(w)"
                component_desc = "Действительная часть"
            elif component == "imaginary":
                Z_data = np.imag(W)
                zlabel = "Im(w)"
                component_desc = "Мнимая часть"
            elif component == "phase":
                Z_data = np.angle(W)
                zlabel = "Arg(w)"
                component_desc = "Фаза"
            
            # Создаем визуализацию в зависимости от выбранного типа
            surface_type = self.surface_type.get()
            cmap = self.colormap_var.get()
            alpha = self.alpha_var.get()
            
            if surface_type == "surface":
                surf = self.ax.plot_surface(X, Y, Z_data, cmap=cmap, alpha=alpha,
                                          linewidth=0, antialiased=True)
                self.fig.colorbar(surf, ax=self.ax, shrink=0.5, aspect=5, label=zlabel)
                
            elif surface_type == "wireframe":
                self.ax.plot_wireframe(X, Y, Z_data, color='blue', alpha=alpha,
                                     linewidth=0.5)
                
            elif surface_type == "contour":
                contour = self.ax.contourf(X, Y, Z_data, levels=20, cmap=cmap, alpha=alpha)
                self.ax.contour(X, Y, Z_data, levels=20, colors='black', alpha=0.3, linewidths=0.5)
                self.fig.colorbar(contour, ax=self.ax, shrink=0.5, aspect=5, label=zlabel)
                
            elif surface_type == "scatter":
                # Для scatter преобразуем в 1D массивы
                scatter = self.ax.scatter(X.flatten(), Y.flatten(), Z_data.flatten(),
                                        c=Z_data.flatten(), cmap=cmap, alpha=alpha, s=1)
                self.fig.colorbar(scatter, ax=self.ax, shrink=0.5, aspect=5, label=zlabel)
            
            # Настройки осей
            self.ax.set_xlabel('Re(z)')
            self.ax.set_ylabel('Im(z)')
            self.ax.set_zlabel(zlabel)
            
            # ИСПРАВЛЕНИЕ: используем конкретное название функции вместо f(z)
            function_name = self.get_function_name(func_type)
            title = f"{function_name} - {component_desc}"
            self.ax.set_title(title, fontsize=12, pad=20)
            
            # Обновляем информационную панель
            self.update_info_panel(X, Y, W, func_type)
            
            self.canvas.draw()
            
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Не удалось построить график: {str(e)}")
    
    def get_function_name(self, func_type):
        """Получение читаемого имени функции"""
        names = {
            "sin": "sin(z)",
            "cos": "cos(z)", 
            "exp": "exp(z)",
            "square": "z²",
            "cube": "z³",
            "reciprocal": "1/z",
            "log": "log(z)",
            "tan": "tan(z)",
            "sinh": "sinh(z)"
        }
        return names.get(func_type, "sin(z)")
    
    def update_info_panel(self, X, Y, W, func_type):
        """Обновление информационной панели"""
        # ИСПРАВЛЕНИЕ: используем конкретное название функции вместо f(z)
        function_name = self.get_function_name(func_type)
        info = f"ФУНКЦИЯ: {function_name}\n"
        info += "=" * 40 + "\n\n"
        
        info += "ОБЛАСТЬ ОПРЕДЕЛЕНИЯ:\n"
        info += f"  Re(z): [{self.x_min_var.get():.2f}, {self.x_max_var.get():.2f}]\n"
        info += f"  Im(z): [{self.y_min_var.get():.2f}, {self.y_max_var.get():.2f}]\n"
        info += f"  Точек: {self.points_var.get()}×{self.points_var.get()}\n\n"
        
        # ИСПРАВЛЕНИЕ: используем w вместо f(z) для результатов
        info += "ХАРАКТЕРИСТИКИ ФУНКЦИИ:\n"
        info += f"  Min |w|: {np.abs(W).min():.4f}\n"
        info += f"  Max |w|: {np.abs(W).max():.4f}\n"
        info += f"  Среднее |w|: {np.abs(W).mean():.4f}\n\n"
        
        info += "КОМПЛЕКСНЫЕ СВОЙСТВА:\n"
        real_part = np.real(W)
        imag_part = np.imag(W)
        info += f"  Min Re(w): {real_part.min():.4f}\n"
        info += f"  Max Re(w): {real_part.max():.4f}\n"
        info += f"  Min Im(w): {imag_part.min():.4f}\n"
        info += f"  Max Im(w): {imag_part.max():.4f}\n\n"
        
        # Особые точки для некоторых функций
        if func_type == "reciprocal":
            info += "ОСОБЕННОСТИ:\n"
            info += "  Полюс в точке z = 0\n"
        elif func_type == "log":
            info += "ОСОБЕННОСТИ:\n"
            info += "  Точка ветвления в z = 0\n"
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
    
    def reset_view(self):
        """Сброс вида камеры"""
        self.ax.view_init(elev=30, azim=45)
        self.canvas.draw()
    
    def export_plot(self):
        """Экспорт графика"""
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("SVG files", "*.svg")]
        )
        if file_path:
            try:
                self.fig.savefig(file_path, dpi=300, bbox_inches='tight')
                tk.messagebox.showinfo("Успех", f"График сохранен в {file_path}")
            except Exception as e:
                tk.messagebox.showerror("Ошибка", f"Не удалось сохранить: {str(e)}")
    
    def toggle_animation(self):
        """Переключение анимации вращения"""
        if hasattr(self, 'animation_running') and self.animation_running:
            self.animation_running = False
        else:
            self.animate_rotation()
    
    def animate_rotation(self):
        """Анимация вращения графика"""
        self.animation_running = True
        self.animate_frame(0)
    
    def animate_frame(self, frame):
        """Один кадр анимации"""
        if not hasattr(self, 'animation_running') or not self.animation_running:
            return
            
        # Вращаем камеру
        self.ax.view_init(elev=30, azim=frame)
        self.canvas.draw()
        
        # Следующий кадр
        self.root.after(50, lambda: self.animate_frame((frame + 2) % 360))

# Запуск приложения
if __name__ == "__main__":
    print("Запуск 3D визуализатора комплексных функций...")
    print("Доступные функции:")
    print("- sin(z), cos(z), tan(z) - Тригонометрические")
    print("- exp(z) - Экспоненциальная")
    print("- z², z³ - Степенныe")
    print("- 1/z - Обратная")
    print("- log(z) - Логарифмическая")
    print("- sinh(z) - Гиперболические")
    
    root = tk.Tk()
    app = Complex3DVisualizer(root)
    root.mainloop()