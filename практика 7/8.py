import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox, RadioButtons
import matplotlib.animation as animation
from scipy import integrate

class CalculusGrapher:
    def __init__(self):
        self.x = np.linspace(-5, 5, 1000)
        self.function_str = "np.sin(x)"
        self.current_function = lambda x: np.sin(x)
        
        # Параметры для анимации
        self.animation_running = False
        self.anim = None
        
        self.setup_ui()
        
    def numerical_derivative(self, func, x, dx=1e-6):
        """Численная производная"""
        return (func(x + dx) - func(x - dx)) / (2 * dx)
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса с рациональным размещением"""
        self.fig = plt.figure(figsize=(16, 12))
        
        # Создаем сетку 4x4 для лучшего контроля над размещением
        # Графики занимают левую часть, управление - правую
        self.ax_func = plt.subplot2grid((4, 4), (0, 0), colspan=3, rowspan=1)
        self.ax_deriv = plt.subplot2grid((4, 4), (1, 0), colspan=3, rowspan=1)
        self.ax_integral = plt.subplot2grid((4, 4), (2, 0), colspan=3, rowspan=1)
        self.ax_controls = plt.subplot2grid((4, 4), (3, 0), colspan=4, rowspan=1)
        
        # Панель управления справа
        self.ax_panel = plt.subplot2grid((4, 4), (0, 3), colspan=1, rowspan=3)
        
        # Настройка осей графиков
        for ax in [self.ax_func, self.ax_deriv, self.ax_integral]:
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='k', linewidth=0.5)
            ax.axvline(x=0, color='k', linewidth=0.5)
            ax.set_xlim(-5, 5)
        
        self.ax_func.set_ylabel('f(x)', fontsize=12)
        self.ax_func.set_title('ФУНКЦИЯ', fontweight='bold', pad=15, fontsize=14)
        
        self.ax_deriv.set_ylabel("f'(x)", fontsize=12)
        self.ax_deriv.set_title('ПРОИЗВОДНАЯ', fontweight='bold', pad=15, fontsize=14)
        
        self.ax_integral.set_ylabel('∫f(x)dx', fontsize=12)
        self.ax_integral.set_xlabel('x', fontsize=12)
        self.ax_integral.set_title('ИНТЕГРАЛ', fontweight='bold', pad=15, fontsize=14)
        
        # Инициализация графиков
        self.func_line, = self.ax_func.plot(self.x, self.current_function(self.x), 
                                          'b-', linewidth=2, label='f(x)')
        
        self.deriv_line, = self.ax_deriv.plot(self.x, [self.numerical_derivative(self.current_function, xi) for xi in self.x], 
                                            'r-', linewidth=2, label="f'(x)")
        
        self.integral_line, = self.ax_integral.plot(self.x, [self.calculate_integral(xi) for xi in self.x], 
                                                  'g-', linewidth=2, label='∫f(x)dx')
        
        # Точки для визуализации
        self.point_func, = self.ax_func.plot([], [], 'ro', markersize=8, zorder=5)
        self.point_deriv, = self.ax_deriv.plot([], [], 'ro', markersize=8, zorder=5)
        self.point_integral, = self.ax_integral.plot([], [], 'ro', markersize=8, zorder=5)
        
        # Линии для визуализации связи
        self.vline_func = self.ax_func.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
        self.vline_deriv = self.ax_deriv.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
        self.vline_integral = self.ax_integral.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
        
        # Тангенс в точке
        self.tangent_line, = self.ax_func.plot([], [], 'orange', linewidth=2, alpha=0.7, label='Касательная')
        
        # Настройка панели управления
        self.ax_panel.axis('off')
        
        self.setup_controls()
        self.update_crosshair(0)
        
        # Настройка нижней панели управления
        self.ax_controls.axis('off')
        
        plt.tight_layout()
        plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.15, hspace=0.4)
        
    def setup_controls(self):
        """Настройка элементов управления с правильным позиционированием"""
        
        # === ПРАВАЯ ПАНЕЛЬ УПРАВЛЕНИЯ ===
        
        # Текстовое поле для ввода функции (вверху справа)
        ax_textbox = plt.axes([0.75, 0.82, 0.22, 0.04])
        self.text_box = TextBox(ax_textbox, 'f(x):', initial='sin(x)')
        self.text_box.on_submit(self.update_function)
        
        # Радио-кнопки для выбора предустановленных функций (под текстовым полем)
        ax_radio = plt.axes([0.75, 0.65, 0.22, 0.15])
        self.radio = RadioButtons(ax_radio, 
                                ['sin(x)', 'cos(x)', 'x^2', 'x^3 - x', 'exp(x)', '1/(1+x^2)'],
                                active=0)
        self.radio.on_clicked(self.select_preset)
        
        # Информационная панель (под радио-кнопками)
        self.info_text = self.ax_panel.text(0.05, 0.45, '', transform=self.ax_panel.transAxes,
                                          fontsize=10, verticalalignment='top',
                                          bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))
        
        # === НИЖНЯЯ ПАНЕЛЬ УПРАВЛЕНИЯ ===
        
        # Слайдер для выбора точки (слева внизу)
        ax_slider = plt.axes([0.15, 0.08, 0.3, 0.03])
        self.slider = Slider(ax_slider, 'Точка анализа x', -5, 5, valinit=0, valfmt='%.2f')
        self.slider.on_changed(self.update_crosshair)
        
        # Слайдер для диапазона (справа от слайдера точки)
        ax_range = plt.axes([0.15, 0.03, 0.3, 0.03])
        self.range_slider = Slider(ax_range, 'Диапазон графика', 1, 10, valinit=5, valfmt='%.1f')
        self.range_slider.on_changed(self.update_range)
        
        # Кнопки управления (центр внизу)
        ax_animate = plt.axes([0.55, 0.08, 0.1, 0.04])
        self.animate_btn = Button(ax_animate, '▶ Анимация')
        self.animate_btn.on_clicked(self.toggle_animation)
        
        ax_reset = plt.axes([0.66, 0.08, 0.1, 0.04])
        self.reset_btn = Button(ax_reset, 'Сброс')
        self.reset_btn.on_clicked(self.reset_view)
        
        # Легенда на графиках
        self.ax_func.legend(loc='upper right', fontsize=10)
        self.ax_deriv.legend(loc='upper right', fontsize=10)
        self.ax_integral.legend(loc='upper right', fontsize=10)
        
    def parse_function(self, func_str):
        """Парсинг строки функции с обработкой ошибок"""
        original_str = func_str
        try:
            # Заменяем математические обозначения
            func_str = func_str.replace('^', '**')
            func_str = func_str.replace('sin', 'np.sin')
            func_str = func_str.replace('cos', 'np.cos')
            func_str = func_str.replace('tan', 'np.tan')
            func_str = func_str.replace('exp', 'np.exp')
            func_str = func_str.replace('log', 'np.log')
            func_str = func_str.replace('sqrt', 'np.sqrt')
            func_str = func_str.replace('abs', 'np.abs')
            
            # Проверяем наличие np. для математических функций
            if 'np.' not in func_str and any(op in func_str for op in ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt']):
                for func in ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt']:
                    func_str = func_str.replace(func, f'np.{func}')
            
            # Создаем лямбда-функцию
            func = lambda x: eval(func_str)
            # Тестируем функцию
            test_val = func(0)
            self.function_str = original_str
            return func
        except Exception as e:
            print(f"Ошибка в функции: {e}")
            return self.current_function
    
    def calculate_derivative(self, x):
        """Вычисление производной"""
        try:
            return self.numerical_derivative(self.current_function, x)
        except:
            return 0
    
    def calculate_integral(self, x):
        """Вычисление интеграла от -5 до x"""
        try:
            result, _ = integrate.quad(self.current_function, -5, x)
            return result
        except:
            return 0
    
    def update_function(self, text):
        """Обновление функции"""
        self.current_function = self.parse_function(text)
        self.update_plots()
    
    def update_range(self, val):
        """Обновление диапазона"""
        range_val = self.range_slider.val
        self.x = np.linspace(-range_val, range_val, 1000)
        
        for ax in [self.ax_func, self.ax_deriv, self.ax_integral]:
            ax.set_xlim(-range_val, range_val)
        
        self.update_plots()
    
    def update_plots(self):
        """Обновление всех графиков"""
        # Функция
        y_func = self.current_function(self.x)
        self.func_line.set_data(self.x, y_func)
        y_range = np.max(y_func) - np.min(y_func) if len(y_func) > 0 else 1
        y_min = np.min(y_func) if len(y_func) > 0 else -1
        y_max = np.max(y_func) if len(y_func) > 0 else 1
        self.ax_func.set_ylim(y_min - 0.1*y_range, y_max + 0.1*y_range)
        
        # Производная
        y_deriv = np.array([self.calculate_derivative(xi) for xi in self.x])
        self.deriv_line.set_data(self.x, y_deriv)
        if len(y_deriv) > 0:
            y_deriv_range = np.max(y_deriv) - np.min(y_deriv) if np.max(y_deriv) != np.min(y_deriv) else 2
            y_deriv_min = np.min(y_deriv)
            y_deriv_max = np.max(y_deriv)
            self.ax_deriv.set_ylim(y_deriv_min - 0.1*y_deriv_range, 
                                 y_deriv_max + 0.1*y_deriv_range)
        
        # Интеграл
        y_integral = np.array([self.calculate_integral(xi) for xi in self.x])
        self.integral_line.set_data(self.x, y_integral)
        if len(y_integral) > 0:
            y_integral_range = np.max(y_integral) - np.min(y_integral) if np.max(y_integral) != np.min(y_integral) else 2
            y_integral_min = np.min(y_integral)
            y_integral_max = np.max(y_integral)
            self.ax_integral.set_ylim(y_integral_min - 0.1*y_integral_range, 
                                    y_integral_max + 0.1*y_integral_range)
        
        self.update_crosshair(self.slider.val)
        self.fig.canvas.draw_idle()
    
    def update_crosshair(self, val):
        """Обновление перекрестия и точек"""
        if val is None:
            return
            
        x_point = val if isinstance(val, (int, float)) else self.slider.val
        
        # Обновление вертикальных линий
        self.vline_func.set_xdata([x_point, x_point])
        self.vline_deriv.set_xdata([x_point, x_point])
        self.vline_integral.set_xdata([x_point, x_point])
        
        # Обновление точек
        y_func = self.current_function(x_point)
        y_deriv = self.calculate_derivative(x_point)
        y_integral = self.calculate_integral(x_point)
        
        self.point_func.set_data([x_point], [y_func])
        self.point_deriv.set_data([x_point], [y_deriv])
        self.point_integral.set_data([x_point], [y_integral])
        
        # Обновление касательной
        self.update_tangent(x_point, y_func, y_deriv)
        
        self.update_info(x_point, y_func, y_deriv, y_integral)
        self.fig.canvas.draw_idle()
    
    def update_tangent(self, x_point, y_func, derivative):
        """Обновление линии касательной"""
        tangent_length = 1.0
        x_tangent = np.array([x_point - tangent_length, x_point + tangent_length])
        y_tangent = y_func + derivative * (x_tangent - x_point)
        self.tangent_line.set_data(x_tangent, y_tangent)
    
    def update_info(self, x_point, y_func, y_deriv, y_integral):
        """Обновление информационной панели"""
        info = (f'АНАЛИЗ В ТОЧКЕ:\n'
                f'x = {x_point:.3f}\n'
                f'f(x) = {y_func:.3f}\n'
                f"f'(x) = {y_deriv:.3f}\n"
                f'∫f(x)dx = {y_integral:.3f}\n\n'
                f'ТЕКУЩАЯ ФУНКЦИЯ:\n{self.function_str}')
        
        self.info_text.set_text(info)
    
    def select_preset(self, label):
        """Выбор предустановленной функции"""
        presets = {
            'sin(x)': 'sin(x)',
            'cos(x)': 'cos(x)', 
            'x^2': 'x**2',
            'x^3 - x': 'x**3 - x',
            'exp(x)': 'exp(x)',
            '1/(1+x^2)': '1/(1+x**2)'
        }
        
        self.text_box.set_val(presets[label])
        self.update_function(presets[label])
    
    def toggle_animation(self, event):
        """Переключение анимации"""
        if self.anim is None:
            # Создаем анимацию
            self.anim = animation.FuncAnimation(
                self.fig, self.animate, frames=200, interval=50, blit=False
            )
            self.animation_running = True
            self.animate_btn.label.set_text('❚❚ Стоп')
        else:
            if self.animation_running:
                self.anim.event_source.stop()
                self.animate_btn.label.set_text('▶ Анимация')
            else:
                self.anim.event_source.start()
                self.animate_btn.label.set_text('❚❚ Стоп')
            
            self.animation_running = not self.animation_running
        
        self.fig.canvas.draw_idle()
    
    def animate(self, frame):
        """Анимация движения точки"""
        if self.animation_running:
            # Плавное движение вперед-назад
            t = (frame / 200) * 2 * np.pi
            x_point = 4 * np.sin(t)
            self.slider.set_val(x_point)
    
    def reset_view(self, event):
        """Сброс вида"""
        self.slider.set_val(0)
        self.range_slider.set_val(5)
        self.update_function('sin(x)')
        self.text_box.set_val('sin(x)')
        self.radio.set_active(0)
        
        if self.anim is not None and self.animation_running:
            self.toggle_animation(None)

# Запуск программы
if __name__ == "__main__":
    print("Запуск Calculus Grapher с улучшенным интерфейсом...")
    print("Расположение элементов:")
    print("- Графики: левая часть экрана")
    print("- Управление функцией: правая панель") 
    print("- Слайдеры и кнопки: нижняя панель")
    
    try:
        grapher = CalculusGrapher()
        plt.show()
    except Exception as e:
        print(f"Ошибка: {e}")
        print("Проверьте установленные библиотеки: numpy, matplotlib, scipy")