import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import wave
import pyaudio
import threading
import time
import requests
import io
from scipy import signal
import warnings
warnings.filterwarnings('ignore')

class AudioApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Универсальное аудио приложение")
        self.root.geometry("1200x800")
        
        # Инициализация переменных
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.recording = False
        self.playing = False
        self.generating = False
        self.radio_playing = False
        
        # Параметры генерации сигнала
        self.frequency = 440.0
        self.amplitude = 0.5
        self.waveform = "sine"
        self.duration = 2.0
        self.sample_rate = 44100
        
        # Параметры импульсов
        self.pulse_count = 5
        self.pulse_duration = 0.1
        self.pulse_interval = 0.2
        
        self.setup_ui()
        
    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="УНИВЕРСАЛЬНОЕ АУДИО ПРИЛОЖЕНИЕ", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Создание вкладок
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка воспроизведения и записи
        self.setup_playback_tab(notebook)
        
        # Вкладка онлайн-радио
        self.setup_radio_tab(notebook)
        
        # Вкладка генератора сигналов
        self.setup_generator_tab(notebook)
        
        # Вкладка визуализации
        self.setup_visualization_tab(notebook)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
    def setup_playback_tab(self, notebook):
        """Вкладка воспроизведения и записи"""
        playback_tab = ttk.Frame(notebook)
        notebook.add(playback_tab, text="Воспроизведение/Запись")
        
        # Фрейм управления файлами
        file_frame = ttk.LabelFrame(playback_tab, text="Управление файлами", padding="10")
        file_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ttk.Button(file_frame, text="Открыть аудиофайл", 
                  command=self.open_audio_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Начать запись", 
                  command=self.start_recording).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Остановить запись", 
                  command=self.stop_recording).pack(side=tk.LEFT, padx=5)
        
        self.record_button = ttk.Button(file_frame, text="Запись", state=tk.DISABLED)
        self.record_button.pack(side=tk.LEFT, padx=5)
        
        # Фрейм воспроизведения
        play_frame = ttk.LabelFrame(playback_tab, text="Воспроизведение", padding="10")
        play_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ttk.Button(play_frame, text="Воспроизвести", 
                  command=self.play_audio).pack(side=tk.LEFT, padx=5)
        ttk.Button(play_frame, text="Пауза", 
                  command=self.pause_audio).pack(side=tk.LEFT, padx=5)
        ttk.Button(play_frame, text="Стоп", 
                  command=self.stop_audio).pack(side=tk.LEFT, padx=5)
        
        # Прогресс бар
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(play_frame, variable=self.progress_var, maximum=100)
        progress_bar.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Информация о файле
        self.file_info_var = tk.StringVar(value="Файл не выбран")
        file_info_label = ttk.Label(playback_tab, textvariable=self.file_info_var)
        file_info_label.pack(pady=5)
        
        # Визуализация для воспроизведения
        fig = Figure(figsize=(10, 3))
        self.playback_ax = fig.add_subplot(111)
        self.playback_canvas = FigureCanvasTkAgg(fig, playback_tab)
        self.playback_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.playback_ax.set_title("Аудио сигнал")
        self.playback_ax.set_xlabel("Время (с)")
        self.playback_ax.set_ylabel("Амплитуда")
        self.playback_ax.grid(True, alpha=0.3)
        
    def setup_radio_tab(self, notebook):
        """Вкладка онлайн-радио"""
        radio_tab = ttk.Frame(notebook)
        notebook.add(radio_tab, text="Онлайн-радио")
        
        # Список радиостанций
        radio_frame = ttk.LabelFrame(radio_tab, text="Радиостанции", padding="10")
        radio_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.radio_stations = {
            "Европа Плюс": "http://ep256.hostingradio.ru:8052/europaplus256.mp3",
            "Русское Радио": "http://rusradio.hostingradio.ru:8000/rusradio128.mp3",
            "Дорожное Радио": "http://dorognoe.hostingradio.ru:8000/dorognoe",
            "Ретро FM": "http://retro.hostingradio.ru:8014/retro256.mp3",
            "Вести FM": "http://icecast.vgtrk.cdnvideo.ru/vestifm_mp3_192kbps",
        }
        
        self.radio_var = tk.StringVar()
        radio_combo = ttk.Combobox(radio_frame, textvariable=self.radio_var, 
                                  values=list(self.radio_stations.keys()), width=30)
        radio_combo.pack(side=tk.LEFT, padx=5)
        radio_combo.set("Европа Плюс")
        
        ttk.Button(radio_frame, text="Воспроизвести", 
                  command=self.play_radio).pack(side=tk.LEFT, padx=5)
        ttk.Button(radio_frame, text="Остановить", 
                  command=self.stop_radio).pack(side=tk.LEFT, padx=5)
        
        # Громкость радио
        volume_frame = ttk.Frame(radio_tab)
        volume_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ttk.Label(volume_frame, text="Громкость:").pack(side=tk.LEFT)
        self.radio_volume_var = tk.DoubleVar(value=0.7)
        volume_scale = ttk.Scale(volume_frame, from_=0.0, to=1.0, 
                                variable=self.radio_volume_var, orient=tk.HORIZONTAL)
        volume_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Статус радио
        self.radio_status_var = tk.StringVar(value="Радио не запущено")
        radio_status_label = ttk.Label(radio_tab, textvariable=self.radio_status_var)
        radio_status_label.pack(pady=5)
        
    def setup_generator_tab(self, notebook):
        """Вкладка генератора сигналов"""
        generator_tab = ttk.Frame(notebook)
        notebook.add(generator_tab, text="Генератор сигналов")
        
        # Основные параметры
        params_frame = ttk.LabelFrame(generator_tab, text="Параметры сигнала", padding="10")
        params_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Частота
        freq_frame = ttk.Frame(params_frame)
        freq_frame.pack(fill=tk.X, pady=2)
        ttk.Label(freq_frame, text="Частота (Гц):").pack(side=tk.LEFT)
        self.freq_var = tk.DoubleVar(value=440.0)
        freq_scale = ttk.Scale(freq_frame, from_=20, to=2000, variable=self.freq_var, 
                              orient=tk.HORIZONTAL)
        freq_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        freq_entry = ttk.Entry(freq_frame, textvariable=self.freq_var, width=8)
        freq_entry.pack(side=tk.LEFT, padx=5)
        
        # Амплитуда
        amp_frame = ttk.Frame(params_frame)
        amp_frame.pack(fill=tk.X, pady=2)
        ttk.Label(amp_frame, text="Амплитуда:").pack(side=tk.LEFT)
        self.amp_var = tk.DoubleVar(value=0.5)
        amp_scale = ttk.Scale(amp_frame, from_=0.1, to=1.0, variable=self.amp_var, 
                             orient=tk.HORIZONTAL)
        amp_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        amp_entry = ttk.Entry(amp_frame, textvariable=self.amp_var, width=8)
        amp_entry.pack(side=tk.LEFT, padx=5)
        
        # Форма волны
        wave_frame = ttk.Frame(params_frame)
        wave_frame.pack(fill=tk.X, pady=2)
        ttk.Label(wave_frame, text="Форма волны:").pack(side=tk.LEFT)
        self.wave_var = tk.StringVar(value="sine")
        wave_combo = ttk.Combobox(wave_frame, textvariable=self.wave_var,
                                 values=["sine", "square", "sawtooth", "triangle", "noise"])
        wave_combo.pack(side=tk.LEFT, padx=5)
        
        # Длительность
        duration_frame = ttk.Frame(params_frame)
        duration_frame.pack(fill=tk.X, pady=2)
        ttk.Label(duration_frame, text="Длительность (с):").pack(side=tk.LEFT)
        self.duration_var = tk.DoubleVar(value=2.0)
        duration_scale = ttk.Scale(duration_frame, from_=0.1, to=10.0, variable=self.duration_var,
                                  orient=tk.HORIZONTAL)
        duration_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        duration_entry = ttk.Entry(duration_frame, textvariable=self.duration_var, width=8)
        duration_entry.pack(side=tk.LEFT, padx=5)
        
        # Параметры импульсов
        pulse_frame = ttk.LabelFrame(generator_tab, text="Пакеты импульсов", padding="10")
        pulse_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Количество импульсов
        pulse_count_frame = ttk.Frame(pulse_frame)
        pulse_count_frame.pack(fill=tk.X, pady=2)
        ttk.Label(pulse_count_frame, text="Количество импульсов:").pack(side=tk.LEFT)
        self.pulse_count_var = tk.IntVar(value=5)
        pulse_count_spin = ttk.Spinbox(pulse_count_frame, from_=1, to=100, 
                                      textvariable=self.pulse_count_var, width=5)
        pulse_count_spin.pack(side=tk.LEFT, padx=5)
        
        # Длительность импульса
        pulse_dur_frame = ttk.Frame(pulse_frame)
        pulse_dur_frame.pack(fill=tk.X, pady=2)
        ttk.Label(pulse_dur_frame, text="Длительность импульса (с):").pack(side=tk.LEFT)
        self.pulse_dur_var = tk.DoubleVar(value=0.1)
        pulse_dur_scale = ttk.Scale(pulse_dur_frame, from_=0.01, to=1.0, variable=self.pulse_dur_var,
                                   orient=tk.HORIZONTAL)
        pulse_dur_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Интервал между импульсами
        pulse_int_frame = ttk.Frame(pulse_frame)
        pulse_int_frame.pack(fill=tk.X, pady=2)
        ttk.Label(pulse_int_frame, text="Интервал между импульсами (с):").pack(side=tk.LEFT)
        self.pulse_int_var = tk.DoubleVar(value=0.2)
        pulse_int_scale = ttk.Scale(pulse_int_frame, from_=0.01, to=2.0, variable=self.pulse_int_var,
                                   orient=tk.HORIZONTAL)
        pulse_int_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Управление генерацией
        control_frame = ttk.Frame(generator_tab)
        control_frame.pack(pady=10)
        
        ttk.Button(control_frame, text="Воспроизвести сигнал", 
                  command=self.play_generated_signal).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Остановить", 
                  command=self.stop_generated_signal).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Сохранить в файл", 
                  command=self.save_generated_signal).pack(side=tk.LEFT, padx=5)
        
        # График сгенерированного сигнала
        fig = Figure(figsize=(10, 3))
        self.generator_ax = fig.add_subplot(111)
        self.generator_canvas = FigureCanvasTkAgg(fig, generator_tab)
        self.generator_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.generator_ax.set_title("Сгенерированный сигнал")
        self.generator_ax.set_xlabel("Время (с)")
        self.generator_ax.set_ylabel("Амплитуда")
        self.generator_ax.grid(True, alpha=0.3)
        
    def setup_visualization_tab(self, notebook):
        """Вкладка визуализации"""
        viz_tab = ttk.Frame(notebook)
        notebook.add(viz_tab, text="Визуализация")
        
        # Управление визуализацией
        control_frame = ttk.Frame(viz_tab)
        control_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ttk.Button(control_frame, text="Начать визуализацию", 
                  command=self.start_visualization).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Остановить", 
                  command=self.stop_visualization).pack(side=tk.LEFT, padx=5)
        
        # Графики
        fig = Figure(figsize=(10, 6))
        self.viz_ax1 = fig.add_subplot(211)  # Осциллограмма
        self.viz_ax2 = fig.add_subplot(212)  # Спектр
        
        self.viz_canvas = FigureCanvasTkAgg(fig, viz_tab)
        self.viz_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.viz_ax1.set_title("Осциллограмма в реальном времени")
        self.viz_ax1.set_xlabel("Время (с)")
        self.viz_ax1.set_ylabel("Амплитуда")
        self.viz_ax1.grid(True, alpha=0.3)
        
        self.viz_ax2.set_title("Спектрограмма")
        self.viz_ax2.set_xlabel("Частота (Гц)")
        self.viz_ax2.set_ylabel("Амплитуда")
        self.viz_ax2.grid(True, alpha=0.3)
        
        self.visualizing = False
        
    # Методы для воспроизведения и записи
    def open_audio_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.audio_file = wave.open(filename, 'rb')
                self.file_info_var.set(f"Файл: {filename}")
                self.plot_audio_file(filename)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")
    
    def plot_audio_file(self, filename):
        try:
            with wave.open(filename, 'rb') as wav_file:
                frames = wav_file.readframes(-1)
                signal_data = np.frombuffer(frames, dtype=np.int16)
                sample_rate = wav_file.getframerate()
                time = np.linspace(0, len(signal_data) / sample_rate, num=len(signal_data))
                
                self.playback_ax.clear()
                self.playback_ax.plot(time, signal_data, linewidth=0.5)
                self.playback_ax.set_title("Аудио сигнал")
                self.playback_ax.set_xlabel("Время (с)")
                self.playback_ax.set_ylabel("Амплитуда")
                self.playback_ax.grid(True, alpha=0.3)
                self.playback_canvas.draw()
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось визуализировать файл: {e}")
    
    def start_recording(self):
        self.recording = True
        self.recorded_frames = []
        
        def record():
            stream = self.audio.open(format=pyaudio.paInt16, channels=1,
                                   rate=44100, input=True, frames_per_buffer=1024)
            
            while self.recording:
                data = stream.read(1024)
                self.recorded_frames.append(data)
                
            stream.stop_stream()
            stream.close()
            
            # Сохранение записи
            self.save_recording()
        
        self.record_thread = threading.Thread(target=record)
        self.record_thread.start()
        self.status_var.set("Запись...")
    
    def stop_recording(self):
        self.recording = False
        self.status_var.set("Запись остановлена")
    
    def save_recording(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav")]
        )
        if filename:
            wf = wave.open(filename, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.recorded_frames))
            wf.close()
            messagebox.showinfo("Успех", f"Запись сохранена: {filename}")
    
    def play_audio(self):
        if hasattr(self, 'audio_file'):
            def play():
                stream = self.audio.open(
                    format=self.audio.get_format_from_width(self.audio_file.getsampwidth()),
                    channels=self.audio_file.getnchannels(),
                    rate=self.audio_file.getframerate(),
                    output=True
                )
                
                data = self.audio_file.readframes(1024)
                while data and self.playing:
                    stream.write(data)
                    data = self.audio_file.readframes(1024)
                
                stream.stop_stream()
                stream.close()
            
            self.playing = True
            self.play_thread = threading.Thread(target=play)
            self.play_thread.start()
            self.status_var.set("Воспроизведение...")
    
    def pause_audio(self):
        self.playing = False
        self.status_var.set("Пауза")
    
    def stop_audio(self):
        self.playing = False
        if hasattr(self, 'audio_file'):
            self.audio_file.rewind()
        self.status_var.set("Воспроизведение остановлено")
    
    # Методы для радио
    def play_radio(self):
        if not self.radio_playing:
            station_name = self.radio_var.get()
            if station_name in self.radio_stations:
                self.radio_playing = True
                self.radio_status_var.set(f"Воспроизведение: {station_name}")
                self.status_var.set(f"Радио: {station_name}")
            else:
                messagebox.showerror("Ошибка", "Выберите радиостанцию из списка")
    
    def stop_radio(self):
        self.radio_playing = False
        self.radio_status_var.set("Радио остановлено")
        self.status_var.set("Радио выключено")
    
    # Методы для генератора сигналов
    def generate_waveform(self, waveform, freq, amp, duration, sample_rate=44100):
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        
        if waveform == "sine":
            signal = amp * np.sin(2 * np.pi * freq * t)
        elif waveform == "square":
            signal = amp * signal.square(2 * np.pi * freq * t)
        elif waveform == "sawtooth":
            signal = amp * signal.sawtooth(2 * np.pi * freq * t)
        elif waveform == "triangle":
            signal = amp * signal.sawtooth(2 * np.pi * freq * t, width=0.5)
        elif waveform == "noise":
            signal = amp * np.random.normal(0, 1, len(t))
        else:
            signal = amp * np.sin(2 * np.pi * freq * t)
        
        return t, signal
    
    def generate_pulse_train(self):
        pulse_count = self.pulse_count_var.get()
        pulse_duration = self.pulse_dur_var.get()
        pulse_interval = self.pulse_int_var.get()
        total_duration = pulse_count * (pulse_duration + pulse_interval)
        
        t = np.linspace(0, total_duration, int(44100 * total_duration), endpoint=False)
        signal = np.zeros_like(t)
        
        for i in range(pulse_count):
            start_time = i * (pulse_duration + pulse_interval)
            end_time = start_time + pulse_duration
            
            start_idx = int(start_time * 44100)
            end_idx = int(end_time * 44100)
            
            if end_idx <= len(signal):
                pulse_signal = self.amplitude * np.sin(2 * np.pi * self.frequency * 
                                                     (t[start_idx:end_idx] - start_time))
                signal[start_idx:end_idx] = pulse_signal
        
        return t, signal
    
    def play_generated_signal(self):
        if not self.generating:
            self.generating = True
            
            # Получение параметров
            freq = self.freq_var.get()
            amp = self.amp_var.get()
            waveform = self.wave_var.get()
            duration = self.duration_var.get()
            
            # Генерация сигнала
            if waveform == "pulse":
                t, audio_signal = self.generate_pulse_train()
            else:
                t, audio_signal = self.generate_waveform(waveform, freq, amp, duration)
            
            # Визуализация
            self.generator_ax.clear()
            self.generator_ax.plot(t, audio_signal, linewidth=1)
            self.generator_ax.set_title(f"Сгенерированный сигнал: {waveform} {freq}Гц")
            self.generator_ax.set_xlabel("Время (с)")
            self.generator_ax.set_ylabel("Амплитуда")
            self.generator_ax.grid(True, alpha=0.3)
            self.generator_ax.set_ylim(-1.1, 1.1)
            self.generator_canvas.draw()
            
            # Воспроизведение
            def play_signal():
                stream = self.audio.open(format=pyaudio.paFloat32, channels=1,
                                       rate=44100, output=True)
                
                # Конвертация в байты
                audio_bytes = (audio_signal * 32767).astype(np.int16).tobytes()
                
                chunk_size = 1024
                for i in range(0, len(audio_bytes), chunk_size):
                    if not self.generating:
                        break
                    stream.write(audio_bytes[i:i + chunk_size])
                
                stream.stop_stream()
                stream.close()
                self.generating = False
            
            self.generate_thread = threading.Thread(target=play_signal)
            self.generate_thread.start()
            self.status_var.set(f"Воспроизведение: {waveform} {freq}Гц")
    
    def stop_generated_signal(self):
        self.generating = False
        self.status_var.set("Генерация остановлена")
    
    def save_generated_signal(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav")]
        )
        if filename:
            try:
                # Генерация сигнала для сохранения
                freq = self.freq_var.get()
                amp = self.amp_var.get()
                waveform = self.wave_var.get()
                duration = self.duration_var.get()
                
                if waveform == "pulse":
                    t, audio_signal = self.generate_pulse_train()
                else:
                    t, audio_signal = self.generate_waveform(waveform, freq, amp, duration)
                
                # Сохранение в WAV
                audio_int = (audio_signal * 32767).astype(np.int16)
                with wave.open(filename, 'w') as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(44100)
                    wav_file.writeframes(audio_int.tobytes())
                
                messagebox.showinfo("Успех", f"Сигнал сохранен: {filename}")
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить сигнал: {e}")
    
    # Методы для визуализации
    def start_visualization(self):
        if not self.visualizing:
            self.visualizing = True
            self.viz_data = []
            
            def visualize():
                stream = self.audio.open(format=pyaudio.paInt16, channels=1,
                                       rate=44100, input=True, frames_per_buffer=1024)
                
                while self.visualizing:
                    try:
                        data = stream.read(1024, exception_on_overflow=False)
                        audio_data = np.frombuffer(data, dtype=np.int16)
                        self.viz_data.extend(audio_data)
                        
                        # Ограничение размера данных для визуализации
                        if len(self.viz_data) > 44100:  # 1 секунда данных
                            self.viz_data = self.viz_data[-44100:]
                        
                        # Обновление графиков
                        self.update_visualization()
                        
                        time.sleep(0.1)
                        
                    except Exception as e:
                        print(f"Ошибка визуализации: {e}")
                        break
                
                stream.stop_stream()
                stream.close()
            
            self.viz_thread = threading.Thread(target=visualize)
            self.viz_thread.start()
            self.status_var.set("Визуализация...")
    
    def stop_visualization(self):
        self.visualizing = False
        self.status_var.set("Визуализация остановлена")
    
    def update_visualization(self):
        if len(self.viz_data) > 1024:
            # Осциллограмма
            self.viz_ax1.clear()
            time_axis = np.linspace(0, len(self.viz_data) / 44100, len(self.viz_data))
            self.viz_ax1.plot(time_axis, self.viz_data, linewidth=0.5)
            self.viz_ax1.set_title("Осциллограмма в реальном времени")
            self.viz_ax1.set_xlabel("Время (с)")
            self.viz_ax1.set_ylabel("Амплитуда")
            self.viz_ax1.grid(True, alpha=0.3)
            self.viz_ax1.set_ylim(-32768, 32767)
            
            # Спектрограмма
            self.viz_ax2.clear()
            fft_data = np.fft.fft(self.viz_data)
            freqs = np.fft.fftfreq(len(fft_data), 1/44100)
            magnitude = np.abs(fft_data)
            
            # Только положительные частоты
            positive_freq_idx = freqs > 0
            self.viz_ax2.plot(freqs[positive_freq_idx], magnitude[positive_freq_idx], linewidth=0.5)
            self.viz_ax2.set_title("Спектрограмма")
            self.viz_ax2.set_xlabel("Частота (Гц)")
            self.viz_ax2.set_ylabel("Амплитуда")
            self.viz_ax2.grid(True, alpha=0.3)
            self.viz_ax2.set_xlim(0, 5000)
            
            self.viz_canvas.draw()
    
    def __del__(self):
        if hasattr(self, 'audio'):
            self.audio.terminate()

def main():
    try:
        import pyaudio
    except ImportError:
        print("Библиотека pyaudio не установлена. Установите её с помощью:")
        print("pip install pyaudio")
        return
    
    try:
        import numpy as np
    except ImportError:
        print("Библиотека numpy не установлена. Установите её с помощью:")
        print("pip install numpy")
        return
    
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Библиотека matplotlib не установлена. Установите её с помощью:")
        print("pip install matplotlib")
        return
    
    try:
        from scipy import signal
    except ImportError:
        print("Библиотека scipy не установлена. Установите её с помощью:")
        print("pip install scipy")
        return
    
    root = tk.Tk()
    app = AudioApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()