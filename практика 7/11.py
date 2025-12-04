import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime, timedelta
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class WeatherVisualizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Визуализация Метеорологических Данных")
        self.root.geometry("1600x1000")
        
        self.weather_data = None
        self.current_city = "Москва"
        
        self.setup_ui()
        self.load_sample_data()  # Загрузка демо-данных при старте
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основные фреймы
        self.control_frame = ttk.Frame(self.root, width=300)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.visualization_frame = ttk.Frame(self.root)
        self.visualization_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заголовок
        title_label = ttk.Label(self.control_frame, text="Метео Визуализатор", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Выбор города
        self.setup_city_controls()
        
        # Настройки визуализации
        self.setup_visualization_controls()
        
        # Кнопки управления
        self.setup_action_buttons()
        
        # Информационная панель
        self.setup_info_panel()
        
        # Инициализация области визуализации
        self.setup_visualization_area()
        
    def setup_city_controls(self):
        """Настройка выбора города"""
        city_frame = ttk.LabelFrame(self.control_frame, text="Выбор города", padding=10)
        city_frame.pack(pady=10, fill=tk.X)
        
        self.city_var = tk.StringVar(value="Москва")
        
        cities = [
            "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань",
            "Нижний Новгород", "Челябинск", "Самара", "Омск", "Ростов-на-Дону"
        ]
        
        city_combo = ttk.Combobox(city_frame, textvariable=self.city_var, 
                                 values=cities, state="readonly")
        city_combo.pack(fill=tk.X, pady=5)
        city_combo.bind('<<ComboboxSelected>>', self.on_city_change)
        
    def setup_visualization_controls(self):
        """Настройки визуализации"""
        viz_frame = ttk.LabelFrame(self.control_frame, text="Тип визуализации", padding=10)
        viz_frame.pack(pady=10, fill=tk.X)
        
        self.viz_type = tk.StringVar(value="area_temp")
        
        visualizations = [
            ("Температура (область)", "area_temp"),
            ("Осадки (область)", "area_precipitation"),
            ("Тепловая карта температуры", "heatmap_temp"),
            ("Тепловая карта осадков", "heatmap_precip"),
            ("Сравнение городов", "city_comparison"),
            ("Климатические зоны", "climate_zones")
        ]
        
        for text, value in visualizations:
            ttk.Radiobutton(viz_frame, text=text, variable=self.viz_type, 
                           value=value, command=self.update_visualization).pack(anchor=tk.W)
        
        # Настройки цветовой схемы
        ttk.Label(viz_frame, text="Цветовая схема:").pack(anchor=tk.W, pady=(10,0))
        self.color_scheme = tk.StringVar(value="viridis")
        color_combo = ttk.Combobox(viz_frame, textvariable=self.color_scheme, 
                                  values=['viridis', 'plasma', 'coolwarm', 'YlOrRd', 'Blues', 'RdYlBu'],
                                  state="readonly")
        color_combo.pack(fill=tk.X, pady=2)
        color_combo.bind('<<ComboboxSelected>>', self.update_visualization)
        
    def setup_action_buttons(self):
        """Кнопки управления"""
        btn_frame = ttk.Frame(self.control_frame)
        btn_frame.pack(pady=10, fill=tk.X)
        
        ttk.Button(btn_frame, text="Обновить данные", 
                  command=self.load_sample_data).pack(fill=tk.X, pady=2)
        
        ttk.Button(btn_frame, text="Экспорт графика", 
                  command=self.export_plot).pack(fill=tk.X, pady=2)
        
        ttk.Button(btn_frame, text="Статистика", 
                  command=self.show_statistics).pack(fill=tk.X, pady=2)
        
    def setup_info_panel(self):
        """Информационная панель"""
        info_frame = ttk.LabelFrame(self.control_frame, text="Информация о данных", padding=10)
        info_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.info_text = tk.Text(info_frame, height=12, width=35, font=('Courier', 9))
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def setup_visualization_area(self):
        """Настройка области визуализации"""
        # Создаем notebook для вкладок
        self.notebook = ttk.Notebook(self.visualization_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка для основного графика
        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Основная визуализация")
        
        # Вкладка для дополнительной информации
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="Детальная статистика")
        
        # Инициализация графиков
        self.setup_main_plot()
        self.setup_stats_plot()
        
    def setup_main_plot(self):
        """Настройка основного графика"""
        self.main_fig = Figure(figsize=(12, 8), dpi=100)
        self.main_canvas = FigureCanvasTkAgg(self.main_fig, master=self.main_tab)
        self.main_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def setup_stats_plot(self):
        """Настройка графика статистики"""
        self.stats_fig = Figure(figsize=(12, 6), dpi=100)
        self.stats_canvas = FigureCanvasTkAgg(self.stats_fig, master=self.stats_tab)
        self.stats_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def generate_sample_weather_data(self):
        """Генерация демонстрационных метеорологических данных"""
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        
        # Создаем данные для разных городов с различными климатическими характеристиками
        cities_data = {}
        
        # Москва - умеренный климат
        base_temp = 5
        cities_data['Москва'] = {
            'temperature': base_temp + 15 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 3, len(dates)),
            'precipitation': np.random.gamma(2, 2, len(dates)) * (1 + 0.5 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)),
            'humidity': 70 + 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 5, len(dates)),
            'pressure': 1013 + 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 2, len(dates))
        }
        
        # Санкт-Петербург - более влажный
        cities_data['Санкт-Петербург'] = {
            'temperature': base_temp + 12 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 2, len(dates)),
            'precipitation': np.random.gamma(3, 2, len(dates)) * (1 + 0.7 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)),
            'humidity': 75 + 15 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 4, len(dates)),
            'pressure': 1010 + 8 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 2, len(dates))
        }
        
        # Сочи - теплый климат
        cities_data['Сочи'] = {
            'temperature': 15 + 8 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 2, len(dates)),
            'precipitation': np.random.gamma(4, 1.5, len(dates)) * (1 + 0.3 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)),
            'humidity': 75 + 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 3, len(dates)),
            'pressure': 1015 + 5 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 1, len(dates))
        }
        
        # Собираем все данные в один DataFrame
        all_data = []
        for city, metrics in cities_data.items():
            for i, date in enumerate(dates):
                all_data.append({
                    'date': date,
                    'city': city,
                    'temperature': metrics['temperature'][i],
                    'precipitation': metrics['precipitation'][i],
                    'humidity': metrics['humidity'][i],
                    'pressure': metrics['pressure'][i],
                    'month': date.month,
                    'season': (date.month % 12 + 3) // 3  # 1-зима, 2-весна, 3-лето, 4-осень
                })
        
        return pd.DataFrame(all_data)
    
    def load_sample_data(self):
        """Загрузка демонстрационных данных"""
        try:
            self.weather_data = self.generate_sample_weather_data()
            self.update_info_panel()
            self.update_visualization()
            messagebox.showinfo("Успех", "Данные успешно загружены!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
    
    def on_city_change(self, event=None):
        """Обработчик изменения города"""
        self.current_city = self.city_var.get()
        self.update_visualization()
    
    def update_info_panel(self):
        """Обновление информационной панели"""
        if self.weather_data is not None:
            city_data = self.weather_data[self.weather_data['city'] == self.current_city]
            
            info = f"ГОРОД: {self.current_city}\n"
            info += f"Период: {city_data['date'].min().strftime('%d.%m.%Y')} - {city_data['date'].max().strftime('%d.%m.%Y')}\n"
            info += f"Записей: {len(city_data)}\n\n"
            
            info += "СТАТИСТИКА ТЕМПЕРАТУРЫ:\n"
            info += f"  Средняя: {city_data['temperature'].mean():.1f}°C\n"
            info += f"  Максимальная: {city_data['temperature'].max():.1f}°C\n"
            info += f"  Минимальная: {city_data['temperature'].min():.1f}°C\n\n"
            
            info += "СТАТИСТИКА ОСАДКОВ:\n"
            info += f"  Средние: {city_data['precipitation'].mean():.1f} мм\n"
            info += f"  Сумма за год: {city_data['precipitation'].sum():.1f} мм\n\n"
            
            info += "СЕЗОННАЯ ИНФОРМАЦИЯ:\n"
            seasons = {1: 'Зима', 2: 'Весна', 3: 'Лето', 4: 'Осень'}
            for season_num, season_name in seasons.items():
                season_data = city_data[city_data['season'] == season_num]
                if len(season_data) > 0:
                    info += f"  {season_name}: {season_data['temperature'].mean():.1f}°C\n"
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info)
    
    def update_visualization(self, event=None):
        """Обновление визуализации"""
        if self.weather_data is None:
            return
            
        viz_type = self.viz_type.get()
        
        try:
            self.main_fig.clear()
            
            if viz_type == "area_temp":
                self.create_temperature_area_plot()
            elif viz_type == "area_precipitation":
                self.create_precipitation_area_plot()
            elif viz_type == "heatmap_temp":
                self.create_temperature_heatmap()
            elif viz_type == "heatmap_precip":
                self.create_precipitation_heatmap()
            elif viz_type == "city_comparison":
                self.create_city_comparison()
            elif viz_type == "climate_zones":
                self.create_climate_zones_plot()
            
            self.main_canvas.draw()
            self.update_stats_visualization()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать визуализацию: {str(e)}")
    
    def create_temperature_area_plot(self):
        """Создание графика температуры с областями"""
        city_data = self.weather_data[self.weather_data['city'] == self.current_city].copy()
        city_data = city_data.set_index('date').sort_index()
        
        # Агрегируем по месяцам
        monthly_data = city_data.resample('M').agg({
            'temperature': ['mean', 'min', 'max'],
            'precipitation': 'sum'
        })
        
        dates = monthly_data.index
        temp_mean = monthly_data[('temperature', 'mean')]
        temp_min = monthly_data[('temperature', 'min')]
        temp_max = monthly_data[('temperature', 'max')]
        
        ax = self.main_fig.add_subplot(111)
        
        # Заполняем область между минимальной и максимальной температурой
        ax.fill_between(dates, temp_min, temp_max, alpha=0.3, 
                       color='red', label='Диапазон температур')
        
        # Линия средней температуры
        ax.plot(dates, temp_mean, color='darkred', linewidth=2, 
               label='Средняя температура')
        
        # Настройки графика
        ax.set_title(f'Температура в {self.current_city} (2024 год)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Температура (°C)', fontsize=12)
        ax.set_xlabel('Месяц', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Форматирование дат
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        self.main_fig.autofmt_xdate()
        
    def create_precipitation_area_plot(self):
        """Создание графика осадков с областями"""
        city_data = self.weather_data[self.weather_data['city'] == self.current_city].copy()
        city_data = city_data.set_index('date').sort_index()
        
        # Агрегируем по неделям для более гладкого графика
        weekly_data = city_data.resample('W').agg({
            'precipitation': 'sum',
            'temperature': 'mean'
        })
        
        ax = self.main_fig.add_subplot(111)
        
        # График осадков с заполнением
        ax.fill_between(weekly_data.index, 0, weekly_data['precipitation'], 
                       alpha=0.6, color='blue', label='Осадки')
        
        # Линия температуры (второстепенная ось)
        ax2 = ax.twinx()
        ax2.plot(weekly_data.index, weekly_data['temperature'], 
                color='red', linewidth=1, alpha=0.7, label='Температура')
        
        ax.set_title(f'Осадки и температура в {self.current_city}', fontsize=14, fontweight='bold')
        ax.set_ylabel('Осадки (мм/неделю)', fontsize=12, color='blue')
        ax2.set_ylabel('Температура (°C)', fontsize=12, color='red')
        ax.set_xlabel('Дата', fontsize=12)
        
        # Объединенная легенда
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        ax.grid(True, alpha=0.3)
        
    def create_temperature_heatmap(self):
        """Создание тепловой карты температуры"""
        city_data = self.weather_data[self.weather_data['city'] == self.current_city].copy()
        
        # Создаем pivot таблицу: дни по строкам, месяцы по столбцам
        city_data['day'] = city_data['date'].dt.day
        city_data['month'] = city_data['date'].dt.month
        
        pivot_data = city_data.pivot_table(
            values='temperature', 
            index='day', 
            columns='month', 
            aggfunc='mean'
        )
        
        ax = self.main_fig.add_subplot(111)
        
        # Создаем тепловую карту
        im = ax.imshow(pivot_data.values, cmap=self.color_scheme.get(), aspect='auto', 
                      extent=[1, 12, 31, 1])
        
        # Настройки осей
        ax.set_xlabel('Месяц', fontsize=12)
        ax.set_ylabel('День месяца', fontsize=12)
        ax.set_title(f'Тепловая карта температуры в {self.current_city}', 
                    fontsize=14, fontweight='bold')
        
        # Добавляем цветовую шкалу
        cbar = self.main_fig.colorbar(im, ax=ax)
        cbar.set_label('Температура (°C)', fontsize=12)
        
        # Подписи месяцев
        months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 
                 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
        ax.set_xticks(np.arange(1.5, 13.5, 1))
        ax.set_xticklabels(months)
        
    def create_precipitation_heatmap(self):
        """Создание тепловой карты осадков"""
        city_data = self.weather_data[self.weather_data['city'] == self.current_city].copy()
        
        # Создаем pivot таблицу
        city_data['day'] = city_data['date'].dt.day
        city_data['month'] = city_data['date'].dt.month
        
        pivot_data = city_data.pivot_table(
            values='precipitation', 
            index='day', 
            columns='month', 
            aggfunc='sum'
        )
        
        ax = self.main_fig.add_subplot(111)
        
        # Тепловая карта осадков
        im = ax.imshow(pivot_data.values, cmap='Blues', aspect='auto', 
                      extent=[1, 12, 31, 1])
        
        ax.set_xlabel('Месяц', fontsize=12)
        ax.set_ylabel('День месяца', fontsize=12)
        ax.set_title(f'Тепловая карта осадков в {self.current_city}', 
                    fontsize=14, fontweight='bold')
        
        cbar = self.main_fig.colorbar(im, ax=ax)
        cbar.set_label('Сумма осадков (мм)', fontsize=12)
        
        months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 
                 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
        ax.set_xticks(np.arange(1.5, 13.5, 1))
        ax.set_xticklabels(months)
        
    def create_city_comparison(self):
        """Сравнение городов"""
        ax = self.main_fig.add_subplot(111)
        
        # Агрегируем данные по городам и месяцам
        monthly_avg = self.weather_data.groupby(['city', 'month']).agg({
            'temperature': 'mean',
            'precipitation': 'sum'
        }).reset_index()
        
        # Создаем subplot для каждого города
        cities = self.weather_data['city'].unique()
        n_cities = len(cities)
        
        self.main_fig.clear()
        
        for i, city in enumerate(cities, 1):
            ax = self.main_fig.add_subplot(2, 2, i)
            city_data = monthly_avg[monthly_avg['city'] == city]
            
            # Двойная ось Y
            ax2 = ax.twinx()
            
            # Температура (линия)
            ax.plot(city_data['month'], city_data['temperature'], 
                   color='red', linewidth=2, marker='o', label='Температура')
            
            # Осадки (столбцы)
            ax2.bar(city_data['month'], city_data['precipitation'], 
                   alpha=0.5, color='blue', label='Осадки')
            
            ax.set_title(city, fontweight='bold')
            ax.set_xlabel('Месяц')
            ax.set_ylabel('Температура (°C)', color='red')
            ax2.set_ylabel('Осадки (мм)', color='blue')
            ax.set_xticks(range(1, 13))
            ax.set_xticklabels(['Я', 'Ф', 'М', 'А', 'М', 'И', 'И', 'А', 'С', 'О', 'Н', 'Д'])
            ax.grid(True, alpha=0.3)
            
            # Легенда
            lines1, labels1 = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        self.main_fig.suptitle('Сравнение климатических показателей по городам', 
                              fontsize=16, fontweight='bold')
        self.main_fig.tight_layout()
        
    def create_climate_zones_plot(self):
        """Визуализация климатических зон"""
        ax = self.main_fig.add_subplot(111)
        
        # Агрегируем данные по городам
        city_stats = self.weather_data.groupby('city').agg({
            'temperature': ['mean', 'std'],
            'precipitation': ['mean', 'sum']
        }).round(1)
        
        # Создаем scatter plot
        cities = city_stats.index
        avg_temp = city_stats[('temperature', 'mean')]
        total_precip = city_stats[('precipitation', 'sum')]
        temp_std = city_stats[('temperature', 'std')]
        
        scatter = ax.scatter(avg_temp, total_precip, s=temp_std * 50, 
                           c=avg_temp, cmap=self.color_scheme.get(), 
                           alpha=0.7, edgecolors='black')
        
        # Подписи городов
        for i, city in enumerate(cities):
            ax.annotate(city, (avg_temp[i], total_precip[i]), 
                       xytext=(5, 5), textcoords='offset points', fontsize=9)
        
        ax.set_xlabel('Средняя годовая температура (°C)', fontsize=12)
        ax.set_ylabel('Суммарные годовые осадки (мм)', fontsize=12)
        ax.set_title('Климатические зоны городов', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Цветовая шкала
        cbar = self.main_fig.colorbar(scatter, ax=ax)
        cbar.set_label('Температура (°C)', fontsize=12)
        
        # Добавляем пояснение о размере точек
        ax.text(0.02, 0.98, 'Размер точки = изменчивость температуры', 
               transform=ax.transAxes, fontsize=10,
               bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
               verticalalignment='top')
    
    def update_stats_visualization(self):
        """Обновление статистической визуализации"""
        if self.weather_data is None:
            return
            
        self.stats_fig.clear()
        
        city_data = self.weather_data[self.weather_data['city'] == self.current_city]
        
        # Создаем несколько subplots для детальной статистики
        ax1 = self.stats_fig.add_subplot(2, 2, 1)
        ax2 = self.stats_fig.add_subplot(2, 2, 2)
        ax3 = self.stats_fig.add_subplot(2, 2, 3)
        ax4 = self.stats_fig.add_subplot(2, 2, 4)
        
        # 1. Распределение температуры
        ax1.hist(city_data['temperature'], bins=30, alpha=0.7, color='red', edgecolor='black')
        ax1.set_xlabel('Температура (°C)')
        ax1.set_ylabel('Частота')
        ax1.set_title('Распределение температуры')
        ax1.grid(True, alpha=0.3)
        
        # 2. Распределение осадков
        ax2.hist(city_data['precipitation'], bins=30, alpha=0.7, color='blue', edgecolor='black')
        ax2.set_xlabel('Осадки (мм)')
        ax2.set_ylabel('Частота')
        ax2.set_title('Распределение осадков')
        ax2.grid(True, alpha=0.3)
        
        # 3. Корреляция температура-осадки
        ax3.scatter(city_data['temperature'], city_data['precipitation'], 
                   alpha=0.5, c=city_data['temperature'], cmap='coolwarm')
        ax3.set_xlabel('Температура (°C)')
        ax3.set_ylabel('Осадки (мм)')
        ax3.set_title('Корреляция: температура vs осадки')
        ax3.grid(True, alpha=0.3)
        
        # 4. Сезонные колебания
        seasonal_avg = city_data.groupby('season').agg({
            'temperature': 'mean',
            'precipitation': 'mean'
        })
        seasons = ['Зима', 'Весна', 'Лето', 'Осень']
        
        x = np.arange(len(seasons))
        width = 0.35
        
        ax4.bar(x - width/2, seasonal_avg['temperature'], width, label='Температура', color='red')
        ax4_twin = ax4.twinx()
        ax4_twin.bar(x + width/2, seasonal_avg['precipitation'], width, label='Осадки', color='blue', alpha=0.7)
        
        ax4.set_xlabel('Сезон')
        ax4.set_ylabel('Температура (°C)', color='red')
        ax4_twin.set_ylabel('Осадки (мм)', color='blue')
        ax4.set_xticks(x)
        ax4.set_xticklabels(seasons)
        ax4.set_title('Сезонные показатели')
        ax4.legend(loc='upper left')
        ax4_twin.legend(loc='upper right')
        
        self.stats_fig.suptitle(f'Детальная статистика: {self.current_city}', 
                               fontsize=14, fontweight='bold')
        self.stats_fig.tight_layout()
        self.stats_canvas.draw()
    
    def export_plot(self):
        """Экспорт графика в файл"""
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.main_fig.savefig(file_path, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Успех", f"График сохранен в {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить график: {str(e)}")
    
    def show_statistics(self):
        """Показать расширенную статистику"""
        if self.weather_data is None:
            return
            
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Расширенная статистика")
        stats_window.geometry("600x400")
        
        stats_text = tk.Text(stats_window, font=('Courier', 10))
        scrollbar = ttk.Scrollbar(stats_window, orient=tk.VERTICAL, command=stats_text.yview)
        stats_text.configure(yscrollcommand=scrollbar.set)
        
        stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Генерируем расширенную статистику
        stats = self.generate_detailed_statistics()
        stats_text.insert(1.0, stats)
    
    def generate_detailed_statistics(self):
        """Генерация детальной статистики"""
        city_data = self.weather_data[self.weather_data['city'] == self.current_city]
        
        stats = f"ДЕТАЛЬНАЯ СТАТИСТИКА: {self.current_city}\n"
        stats += "=" * 50 + "\n\n"
        
        stats += "ТЕМПЕРАТУРА:\n"
        stats += f"  Средняя: {city_data['temperature'].mean():.2f}°C\n"
        stats += f"  Медиана: {city_data['temperature'].median():.2f}°C\n"
        stats += f"  Стандартное отклонение: {city_data['temperature'].std():.2f}°C\n"
        stats += f"  Минимум: {city_data['temperature'].min():.2f}°C\n"
        stats += f"  Максимум: {city_data['temperature'].max():.2f}°C\n\n"
        
        stats += "ОСАДКИ:\n"
        stats += f"  Средние: {city_data['precipitation'].mean():.2f} мм/день\n"
        stats += f"  Сумма за год: {city_data['precipitation'].sum():.0f} мм\n"
        stats += f"  Максимум за день: {city_data['precipitation'].max():.1f} мм\n"
        stats += f"  Дней без осадков: {(city_data['precipitation'] == 0).sum()}\n\n"
        
        stats += "СЕЗОННЫЕ ХАРАКТЕРИСТИКИ:\n"
        seasons = {1: 'Зима', 2: 'Весна', 3: 'Лето', 4: 'Осень'}
        for season_num, season_name in seasons.items():
            season_data = city_data[city_data['season'] == season_num]
            if len(season_data) > 0:
                stats += f"  {season_name}:\n"
                stats += f"    Температура: {season_data['temperature'].mean():.1f}°C\n"
                stats += f"    Осадки: {season_data['precipitation'].sum():.0f} мм\n\n"
        
        return stats

# Запуск приложения
if __name__ == "__main__":
    print("Запуск приложения для визуализации метеорологических данных...")
    print("Возможности:")
    print("- Графики с областями для температуры и осадков")
    print("- Тепловые карты для детального анализа")
    print("- Сравнение климатических показателей городов")
    print("- Статистический анализ и экспорт графиков")
    
    root = tk.Tk()
    app = WeatherVisualizationApp(root)
    root.mainloop()