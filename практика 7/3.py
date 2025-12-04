import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button

class ElectricFieldSimulator:
    def __init__(self):
        self.charges = []  # Список зарядов: (x, y, q)
        self.grid_size = 100
        self.x_range = (-5, 5)
        self.y_range = (-5, 5)
        
        # Создаем сетку для расчета поля
        self.x = np.linspace(self.x_range[0], self.x_range[1], self.grid_size)
        self.y = np.linspace(self.y_range[0], self.y_range[1], self.grid_size)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        
        # Инициализируем поля
        self.Ex = np.zeros_like(self.X)
        self.Ey = np.zeros_like(self.Y)
        self.potential = np.zeros_like(self.X)
        
    def add_charge(self, x, y, q):
        """Добавить точечный заряд"""
        self.charges.append((x, y, q))
        self.calculate_field()
        
    def remove_charge(self, index):
        """Удалить заряд по индексу"""
        if 0 <= index < len(self.charges):
            self.charges.pop(index)
            self.calculate_field()
    
    def clear_charges(self):
        """Очистить все заряды"""
        self.charges.clear()
        self.calculate_field()
    
    def calculate_field(self):
        """Рассчитать электрическое поле и потенциал"""
        # Сбрасываем поля
        self.Ex = np.zeros_like(self.X)
        self.Ey = np.zeros_like(self.Y)
        self.potential = np.zeros_like(self.X)
        
        k = 9e9  # Константа Кулона
        
        for charge in self.charges:
            x0, y0, q = charge
            
            # Вектора от заряда до точек сетки
            dx = self.X - x0
            dy = self.Y - y0
            
            # Расстояние от заряда до точек сетки
            r = np.sqrt(dx**2 + dy**2)
            
            # Избегаем деления на ноль
            r = np.where(r < 0.1, 0.1, r)
            
            # Компоненты электрического поля
            E_magnitude = k * abs(q) / r**2
            E_dir_x = dx / r
            E_dir_y = dy / r
            
            # Учитываем знак заряда
            sign = 1 if q > 0 else -1
            
            self.Ex += sign * E_magnitude * E_dir_x
            self.Ey += sign * E_magnitude * E_dir_y
            
            # Электрический потенциал
            self.potential += k * q / r
    
    def get_field_at_point(self, x, y):
        """Получить поле в конкретной точке"""
        Ex_point, Ey_point = 0, 0
        
        k = 9e9
        for charge in self.charges:
            x0, y0, q = charge
            
            dx = x - x0
            dy = y - y0
            r = np.sqrt(dx**2 + dy**2)
            
            if r < 0.1:
                r = 0.1
                
            E_magnitude = k * abs(q) / r**2
            E_dir_x = dx / r
            E_dir_y = dy / r
            
            sign = 1 if q > 0 else -1
            Ex_point += sign * E_magnitude * E_dir_x
            Ey_point += sign * E_magnitude * E_dir_y
            
        return Ex_point, Ey_point

class FieldVisualizer:
    def __init__(self, simulator):
        self.simulator = simulator
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(bottom=0.2)
        
        self.quiver = None
        self.contour = None
        self.charge_artists = []
        
        # Создаем слайдеры для добавления зарядов
        axcolor = 'lightgoldenrodyellow'
        ax_x = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
        ax_y = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)
        ax_q = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
        
        self.slider_x = Slider(ax_x, 'X', -4.0, 4.0, valinit=0)
        self.slider_y = Slider(ax_y, 'Y', -4.0, 4.0, valinit=0)
        self.slider_q = Slider(ax_q, 'Заряд', -2.0, 2.0, valinit=1.0)
        
        # Кнопки
        ax_add = plt.axes([0.1, 0.02, 0.1, 0.04])
        ax_clear = plt.axes([0.8, 0.02, 0.1, 0.04])
        ax_toggle = plt.axes([0.45, 0.02, 0.1, 0.04])
        
        self.button_add = Button(ax_add, 'Добавить')
        self.button_clear = Button(ax_clear, 'Очистить')
        self.button_toggle = Button(ax_toggle, 'Переключить')
        
        self.button_add.on_clicked(self.add_charge)
        self.button_clear.on_clicked(self.clear_charges)
        self.button_toggle.on_clicked(self.toggle_visualization)
        
        self.visualization_mode = 'field_lines'  # 'field_lines' или 'potential'
        
        # Обработка кликов мыши
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
        self.update_plot()
        
    def add_charge(self, event):
        """Добавить заряд по значениям слайдеров"""
        x = self.slider_x.val
        y = self.slider_y.val
        q = self.slider_q.val
        self.simulator.add_charge(x, y, q)
        self.update_plot()
        
    def clear_charges(self, event):
        """Очистить все заряды"""
        self.simulator.clear_charges()
        self.update_plot()
        
    def on_click(self, event):
        """Обработка клика мыши для добавления/удаления зарядов"""
        if event.inaxes != self.ax:
            return
            
        if event.button == 1:  # Левый клик - добавить положительный заряд
            self.simulator.add_charge(event.xdata, event.ydata, 1.0)
        elif event.button == 3:  # Правый клик - добавить отрицательный заряд
            self.simulator.add_charge(event.xdata, event.ydata, -1.0)
            
        self.update_plot()
        
    def toggle_visualization(self, event):
        """Переключить режим визуализации"""
        if self.visualization_mode == 'field_lines':
            self.visualization_mode = 'potential'
        else:
            self.visualization_mode = 'field_lines'
        self.update_plot()
        
    def update_plot(self):
        """Обновить график"""
        self.ax.clear()
        
        if self.visualization_mode == 'field_lines':
            # Визуализация силовых линий
            stream = self.ax.streamplot(self.simulator.X, self.simulator.Y, 
                                      self.simulator.Ex, self.simulator.Ey,
                                      linewidth=1, color='blue',
                                      density=2, arrowstyle='->', arrowsize=1.5)
            
        else:
            # Визуализация эквипотенциальных линий
            contour = self.ax.contour(self.simulator.X, self.simulator.Y, 
                                    self.simulator.potential, 20, cmap='RdYlBu')
            self.ax.clabel(contour, inline=True, fontsize=8)
            
            # Также показываем поле стрелками
            self.ax.quiver(self.simulator.X[::3, ::3], self.simulator.Y[::3, ::3],
                         self.simulator.Ex[::3, ::3], self.simulator.Ey[::3, ::3],
                         scale=30, color='black', alpha=0.7)
        
        # Отображаем заряды
        for i, (x, y, q) in enumerate(self.simulator.charges):
            color = 'red' if q > 0 else 'blue'
            circle = Circle((x, y), 0.1, color=color, alpha=0.7)
            self.ax.add_patch(circle)
            
            # Подписываем заряды
            sign = '+' if q > 0 else '-'
            self.ax.text(x, y + 0.15, f'{sign}{abs(q):.1f}', 
                        ha='center', va='center', fontweight='bold')
        
        self.ax.set_xlim(self.simulator.x_range)
        self.ax.set_ylim(self.simulator.y_range)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        
        title_mode = 'Силовые линии' if self.visualization_mode == 'field_lines' else 'Эквипотенциальные линии'
        self.ax.set_title(f'Симулятор электрического поля - {title_mode}')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_aspect('equal')
        
        plt.draw()

def test_simulator():
    """Тестовая функция для демонстрации работы симулятора"""
    simulator = ElectricFieldSimulator()
    
    # Добавляем тестовые заряды
    simulator.add_charge(-1, 0, 1.0)   # Положительный заряд
    simulator.add_charge(1, 0, -1.0)   # Отрицательный заряд
    
    # Создаем визуализатор
    visualizer = FieldVisualizer(simulator)
    
    plt.show()
    
    return simulator, visualizer

# Дополнительная функция для анимации движения заряда
def animate_test_charge():
    """Анимация движения пробного заряда в поле"""
    simulator = ElectricFieldSimulator()
    simulator.add_charge(0, 0, 2.0)  # Центральный положительный заряд
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Инициализация пробного заряда
    test_charge = {'pos': np.array([3.0, 0.0]), 'q': -0.1, 'trajectory': []}
    dt = 0.01
    
    def animate(frame):
        ax.clear()
        
        # Рассчитываем поле
        simulator.calculate_field()
        
        # Визуализация поля
        stream = ax.streamplot(simulator.X, simulator.Y, simulator.Ex, simulator.Ey,
                             linewidth=1, color='blue', density=2)
        
        # Отображаем заряды
        for x, y, q in simulator.charges:
            color = 'red' if q > 0 else 'blue'
            circle = Circle((x, y), 0.1, color=color, alpha=0.7)
            ax.add_patch(circle)
        
        # Расчет силы и движение пробного заряда
        Ex, Ey = simulator.get_field_at_point(test_charge['pos'][0], test_charge['pos'][1])
        Fx = test_charge['q'] * Ex
        Fy = test_charge['q'] * Ey
        
        # Обновление позиции (упрощенная физика)
        test_charge['pos'][0] += Fx * dt
        test_charge['pos'][1] += Fy * dt
        
        test_charge['trajectory'].append(test_charge['pos'].copy())
        
        # Рисуем траекторию
        if len(test_charge['trajectory']) > 1:
            trajectory = np.array(test_charge['trajectory'])
            ax.plot(trajectory[:, 0], trajectory[:, 1], 'g-', linewidth=2)
        
        # Рисуем пробный заряд
        ax.plot(test_charge['pos'][0], test_charge['pos'][1], 'go', markersize=8)
        
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Движение пробного заряда в электрическом поле')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        return []
    
    anim = animation.FuncAnimation(fig, animate, frames=200, interval=50, blit=False)
    plt.show()

if __name__ == "__main__":
    # Запуск основной программы
    simulator, visualizer = test_simulator()