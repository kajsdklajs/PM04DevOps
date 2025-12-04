import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
from scipy.spatial import KDTree
import matplotlib.colors as mcolors

class AdvancedSwarmModel:
    def __init__(self, N=200, L=20, v0=2.0, R=1.5, eta=0.3, dt=0.1):
        self.N = N
        self.L = L
        self.v0 = v0
        self.R = R
        self.eta = eta
        self.dt = dt
        
        # Инициализация частиц
        self.reset_particles()
        
        # Параметры дополнительных взаимодействий
        self.alignment_strength = 1.0
        self.cohesion_strength = 0.1
        self.separation_strength = 0.5
        self.separation_distance = 0.8
        
    def reset_particles(self):
        """Сброс частиц в случайное состояние"""
        self.x = np.random.rand(self.N) * self.L
        self.y = np.random.rand(self.N) * self.L
        self.theta = 2 * np.pi * np.random.rand(self.N)
        self.velocity = np.ones(self.N) * self.v0
        
        # Дополнительные параметры для визуализации
        self.energy = np.zeros(self.N)
        self.neighbor_count = np.zeros(self.N)
        
    def update_swarm(self):
        """Обновление состояния роя с улучшенной физикой"""
        # Создаем KD-дерево для эффективного поиска соседей
        points = np.column_stack([self.x, self.y])
        tree = KDTree(points)
        
        new_theta = np.copy(self.theta)
        
        for i in range(self.N):
            # Находим всех соседей в радиусе R
            neighbors = tree.query_ball_point([self.x[i], self.y[i]], self.R)
            neighbors = [n for n in neighbors if n != i]  # Исключаем саму частицу
            
            self.neighbor_count[i] = len(neighbors)
            
            if len(neighbors) > 0:
                # Выравнивание (Alignment)
                alignment_angle = self.calculate_alignment(i, neighbors)
                
                # Когезия (Cohesion) - стремление к центру масс
                cohesion_angle = self.calculate_cohesion(i, neighbors)
                
                # Разделение (Separation) - избегание столкновений
                separation_angle = self.calculate_separation(i, neighbors)
                
                # Комбинируем все взаимодействия
                combined_angle = (
                    self.alignment_strength * alignment_angle +
                    self.cohesion_strength * cohesion_angle +
                    self.separation_strength * separation_angle
                )
                
                # Нормализуем и добавляем шум
                if np.linalg.norm(combined_angle) > 0:
                    new_direction = np.arctan2(combined_angle[1], combined_angle[0])
                    new_theta[i] = new_direction + self.eta * (np.random.random() - 0.5)
                
                # Расчет "энергии" взаимодействия
                self.energy[i] = len(neighbors) / 10.0
        
        self.theta = new_theta
        
        # Обновление позиций
        self.x += self.velocity * np.cos(self.theta) * self.dt
        self.y += self.velocity * np.sin(self.theta) * self.dt
        
        # Периодические граничные условия
        self.x = self.x % self.L
        self.y = self.y % self.L
        
        # Динамическое изменение скорости на основе локальной плотности
        self.velocity = self.v0 * (1 - 0.1 * self.neighbor_count / 10)
        self.velocity = np.clip(self.velocity, 0.5 * self.v0, 2 * self.v0)
    
    def calculate_alignment(self, i, neighbors):
        """Расчет выравнивания с соседями"""
        if not neighbors:
            return np.array([0, 0])
        
        avg_cos = np.mean(np.cos(self.theta[neighbors]))
        avg_sin = np.mean(np.sin(self.theta[neighbors]))
        return np.array([avg_cos, avg_sin])
    
    def calculate_cohesion(self, i, neighbors):
        """Расчет стремления к центру масс соседей"""
        if not neighbors:
            return np.array([0, 0])
        
        center_x = np.mean(self.x[neighbors])
        center_y = np.mean(self.y[neighbors])
        
        dx = center_x - self.x[i]
        dy = center_y - self.y[i]
        dist = np.sqrt(dx**2 + dy**2)
        
        if dist > 0:
            return np.array([dx/dist, dy/dist])
        return np.array([0, 0])
    
    def calculate_separation(self, i, neighbors):
        """Расчет разделения для избегания столкновений"""
        if not neighbors:
            return np.array([0, 0])
        
        separation_force = np.array([0.0, 0.0])
        
        for neighbor in neighbors:
            dx = self.x[i] - self.x[neighbor]
            dy = self.y[i] - self.y[neighbor]
            dist = np.sqrt(dx**2 + dy**2)
            
            if dist < self.separation_distance and dist > 0:
                # Сила отталкивания обратно пропорциональна расстоянию
                force = 1.0 / dist
                separation_force[0] += dx / dist * force
                separation_force[1] += dy / dist * force
        
        return separation_force

    def calculate_order_parameter(self):
        """Расчет параметра порядка (степени когерентности)"""
        vx = np.mean(np.cos(self.theta))
        vy = np.mean(np.sin(self.theta))
        return np.sqrt(vx**2 + vy**2)

class InteractiveSwarmVisualizer:
    def __init__(self, model):
        self.model = model
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        plt.subplots_adjust(bottom=0.3)
        
        self.animation = None
        self.paused = False
        self.setup_controls()
        self.setup_visualization()
        
    def setup_controls(self):
        """Настройка интерактивных элементов управления"""
        # Создаем слайдеры
        slider_y = 0.18
        slider_height = 0.03
        slider_width = 0.6
        
        ax_velocity = plt.axes([0.25, 0.12, slider_width, slider_height])
        ax_radius = plt.axes([0.25, 0.08, slider_width, slider_height])
        ax_noise = plt.axes([0.25, 0.04, slider_width, slider_height])
        
        ax_align = plt.axes([0.25, 0.20, slider_width, slider_height])
        ax_cohesion = plt.axes([0.25, 0.16, slider_width, slider_height])
        ax_separation = plt.axes([0.25, 0.24, slider_width, slider_height])
        
        self.slider_velocity = Slider(ax_velocity, 'Скорость', 0.1, 5.0, valinit=self.model.v0)
        self.slider_radius = Slider(ax_radius, 'Радиус', 0.5, 5.0, valinit=self.model.R)
        self.slider_noise = Slider(ax_noise, 'Шум', 0.0, 1.0, valinit=self.model.eta)
        
        self.slider_align = Slider(ax_align, 'Выравнивание', 0.0, 2.0, valinit=self.model.alignment_strength)
        self.slider_cohesion = Slider(ax_cohesion, 'Когезия', 0.0, 1.0, valinit=self.model.cohesion_strength)
        self.slider_separation = Slider(ax_separation, 'Разделение', 0.0, 2.0, valinit=self.model.separation_strength)
        
        # Кнопки управления анимацией
        ax_reset = plt.axes([0.05, 0.12, 0.12, 0.04])
        ax_pause = plt.axes([0.05, 0.07, 0.12, 0.04])
        ax_resume = plt.axes([0.05, 0.02, 0.12, 0.04])
        ax_restart_anim = plt.axes([0.18, 0.02, 0.15, 0.04])
        
        self.button_reset = Button(ax_reset, 'Сброс частиц')
        self.button_pause = Button(ax_pause, 'Пауза')
        self.button_resume = Button(ax_resume, 'Продолжить')
        self.button_restart_anim = Button(ax_restart_anim, 'Перезапуск анимации')
        
        # Привязка событий
        self.slider_velocity.on_changed(self.update_parameters)
        self.slider_radius.on_changed(self.update_parameters)
        self.slider_noise.on_changed(self.update_parameters)
        self.slider_align.on_changed(self.update_parameters)
        self.slider_cohesion.on_changed(self.update_parameters)
        self.slider_separation.on_changed(self.update_parameters)
        
        self.button_reset.on_clicked(self.reset_simulation)
        self.button_pause.on_clicked(self.pause_animation)
        self.button_resume.on_clicked(self.resume_animation)
        self.button_restart_anim.on_clicked(self.restart_animation)
        
    def setup_visualization(self):
        """Настройка визуализации"""
        self.ax.clear()
        self.ax.set_xlim(0, self.model.L)
        self.ax.set_ylim(0, self.model.L)
        self.ax.set_xlabel('X координата')
        self.ax.set_ylabel('Y координата')
        self.ax.set_title('Улучшенная модель роевого поведения частиц\nАнимация активна', 
                         fontsize=14, fontweight='bold')
        self.ax.grid(True, alpha=0.3)
        
        # Цветовая карта для энергии
        self.norm = mcolors.Normalize(vmin=0, vmax=3)
        self.cmap = plt.cm.viridis
        
        # Визуализация частиц с цветом по энергии
        self.scatter = self.ax.scatter(self.model.x, self.model.y, 
                                     c=self.model.energy, cmap=self.cmap, 
                                     s=40, alpha=0.8, edgecolors='black', linewidth=0.5)
        
        # Векторы скорости (изначально пустые)
        self.quiver = self.ax.quiver(self.model.x, self.model.y,
                                   np.cos(self.model.theta), np.sin(self.model.theta),
                                   color='red', scale=25, width=0.004, alpha=0.6)
        
        # Статистика
        self.stats_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes, 
                                      verticalalignment='top', fontsize=11,
                                      bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))
        
        # Индикатор состояния анимации
        self.status_text = self.ax.text(0.98, 0.98, '▶ АНИМАЦИЯ', transform=self.ax.transAxes,
                                       verticalalignment='top', horizontalalignment='right',
                                       fontsize=12, fontweight='bold', color='green',
                                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Цветовая шкала
        plt.colorbar(self.scatter, ax=self.ax, label='Энергия взаимодействия', 
                     shrink=0.8, pad=0.02)
    
    def update_parameters(self, val):
        """Обновление параметров модели"""
        self.model.v0 = self.slider_velocity.val
        self.model.R = self.slider_radius.val
        self.model.eta = self.slider_noise.val
        self.model.alignment_strength = self.slider_align.val
        self.model.cohesion_strength = self.slider_cohesion.val
        self.model.separation_strength = self.slider_separation.val
    
    def reset_simulation(self, event):
        """Сброс симуляции"""
        self.model.reset_particles()
        self.update_display()
    
    def pause_animation(self, event):
        """Пауза анимации"""
        if self.animation and not self.paused:
            self.animation.event_source.stop()
            self.paused = True
            self.status_text.set_text('❚❚ ПАУЗА')
            self.status_text.set_color('red')
            self.ax.set_title('Улучшенная модель роевого поведения частиц\nАнимация на паузе', 
                             fontsize=14, fontweight='bold')
            plt.draw()
    
    def resume_animation(self, event):
        """Продолжение анимации"""
        if self.animation and self.paused:
            self.animation.event_source.start()
            self.paused = False
            self.status_text.set_text('▶ АНИМАЦИЯ')
            self.status_text.set_color('green')
            self.ax.set_title('Улучшенная модель роевого поведения частиц\nАнимация активна', 
                             fontsize=14, fontweight='bold')
            plt.draw()
    
    def restart_animation(self, event):
        """Перезапуск анимации"""
        if self.animation:
            self.animation.event_source.stop()
        
        # Пересоздаем анимацию
        self.start_animation()
        self.paused = False
        self.status_text.set_text('▶ АНИМАЦИЯ')
        self.status_text.set_color('green')
        plt.draw()
    
    def update_display(self):
        """Обновление отображения без шага симуляции"""
        # Обновление scatter plot
        colors = self.cmap(self.norm(self.model.energy))
        self.scatter.set_offsets(np.column_stack([self.model.x, self.model.y]))
        self.scatter.set_array(self.model.energy)
        
        # Обновление векторов скорости
        self.quiver.set_offsets(np.column_stack([self.model.x, self.model.y]))
        self.quiver.set_UVC(self.model.velocity * np.cos(self.model.theta),
                          self.model.velocity * np.sin(self.model.theta))
        
        # Обновление статистики
        avg_neighbors = np.mean(self.model.neighbor_count)
        order_parameter = self.model.calculate_order_parameter()
        stats = (f'Частиц: {self.model.N}\n'
                f'Среднее соседей: {avg_neighbors:.1f}\n'
                f'Параметр порядка: {order_parameter:.3f}\n'
                f'Средняя скорость: {np.mean(self.model.velocity):.2f}\n'
                f'Уровень шума: {self.model.eta:.2f}')
        self.stats_text.set_text(stats)
    
    def update_animation(self, frame):
        """Обновление анимации"""
        if not self.paused:
            self.model.update_swarm()
        
        self.update_display()
        
        return self.scatter, self.quiver, self.stats_text, self.status_text
    
    def start_animation(self):
        """Запуск анимации"""
        self.animation = FuncAnimation(
            self.fig, 
            self.update_animation,
            frames=1000,  # Большое количество кадров
            interval=50,   # Интервал в миллисекундах
            blit=False,
            repeat=True
        )

# Демонстрационная функция с разными сценариями
def demonstrate_swarm_scenarios():
    """Демонстрация различных сценариев роевого поведения"""
    
    scenarios = [
        {
            'name': 'Высокая когерентность',
            'params': {'N': 150, 'eta': 0.1, 'alignment_strength': 1.5, 'cohesion_strength': 0.2}
        },
        {
            'name': 'Хаотическое движение', 
            'params': {'N': 150, 'eta': 0.8, 'alignment_strength': 0.3, 'cohesion_strength': 0.05}
        },
        {
            'name': 'Образование кластеров',
            'params': {'N': 200, 'eta': 0.2, 'cohesion_strength': 0.3, 'separation_strength': 0.8}
        }
    ]
    
    for i, scenario in enumerate(scenarios):
        print(f"Запуск сценария: {scenario['name']}")
        
        # Создаем модель с параметрами сценария
        model = AdvancedSwarmModel(**scenario['params'])
        visualizer = InteractiveSwarmVisualizer(model)
        visualizer.start_animation()
        
        # Запускаем анимацию
        plt.show()

# Основная программа
if __name__ == "__main__":
    print("Запуск интерактивной анимации роевого поведения...")
    print("Управление:")
    print(" - 'Пауза' - остановка анимации")
    print(" - 'Продолжить' - возобновление анимации") 
    print(" - 'Перезапуск анимации' - полный перезапуск")
    print(" - 'Сброс частиц' - случайное распределение частиц")
    print(" - Слайдеры - изменение параметров в реальном времени")
    
    # Создаем основную модель
    swarm_model = AdvancedSwarmModel(N=250, L=25, v0=2.0, R=2.0, eta=0.2)
    
    # Создаем визуализатор
    visualizer = InteractiveSwarmVisualizer(swarm_model)
    visualizer.start_animation()
    
    # Показываем интерфейс
    plt.show()
    
    # Раскомментируйте для демонстрации разных сценариев:
    # demonstrate_swarm_scenarios()