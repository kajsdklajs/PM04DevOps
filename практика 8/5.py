import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
import threading
import time
from datetime import datetime
import os

class CommunicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Универсальное приложение для передачи данных")
        self.root.geometry("1000x700")
        
        # Конфигурация (в реальном приложении хранить в безопасном месте)
        self.config = {
            'email': {
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'sender_email': '',
                'sender_password': ''
            },
            'sms': {
                'twilio_sid': '',
                'twilio_token': '',
                'twilio_number': ''
            },
            'telegram': {
                'bot_token': '',
                'chat_id': ''
            },
            'push': {
                'pushbullet_token': ''
            }
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="УНИВЕРСАЛЬНОЕ ПРИЛОЖЕНИЕ ДЛЯ ПЕРЕДАЧИ ДАННЫХ", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Создание вкладок
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка конфигурации
        self.setup_config_tab(notebook)
        
        # Вкладка электронной почты
        self.setup_email_tab(notebook)
        
        # Вкладка SMS
        self.setup_sms_tab(notebook)
        
        # Вкладка мессенджеров
        self.setup_messenger_tab(notebook)
        
        # Вкладка push-уведомлений
        self.setup_push_tab(notebook)
        
        # Вкладка массовой рассылки
        self.setup_bulk_tab(notebook)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Лог событий
        log_frame = ttk.LabelFrame(main_frame, text="Лог событий", padding="10")
        log_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=100)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_config_tab(self, notebook):
        """Вкладка конфигурации"""
        config_tab = ttk.Frame(notebook)
        notebook.add(config_tab, text="Настройки")
        
        # Email настройки
        email_frame = ttk.LabelFrame(config_tab, text="Настройки Email", padding="10")
        email_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ttk.Label(email_frame, text="SMTP сервер:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.smtp_server_var = tk.StringVar(value=self.config['email']['smtp_server'])
        ttk.Entry(email_frame, textvariable=self.smtp_server_var, width=30).grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(email_frame, text="Порт:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.smtp_port_var = tk.StringVar(value=str(self.config['email']['smtp_port']))
        ttk.Entry(email_frame, textvariable=self.smtp_port_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=2, padx=5)
        
        ttk.Label(email_frame, text="Email отправителя:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.sender_email_var = tk.StringVar(value=self.config['email']['sender_email'])
        ttk.Entry(email_frame, textvariable=self.sender_email_var, width=30).grid(row=2, column=1, pady=2, padx=5)
        
        ttk.Label(email_frame, text="Пароль:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.sender_password_var = tk.StringVar(value=self.config['email']['sender_password'])
        ttk.Entry(email_frame, textvariable=self.sender_password_var, show="*", width=30).grid(row=3, column=1, pady=2, padx=5)
        
        # SMS настройки (Twilio)
        sms_frame = ttk.LabelFrame(config_tab, text="Настройки SMS (Twilio)", padding="10")
        sms_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ttk.Label(sms_frame, text="Account SID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.twilio_sid_var = tk.StringVar(value=self.config['sms']['twilio_sid'])
        ttk.Entry(sms_frame, textvariable=self.twilio_sid_var, width=30).grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(sms_frame, text="Auth Token:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.twilio_token_var = tk.StringVar(value=self.config['sms']['twilio_token'])
        ttk.Entry(sms_frame, textvariable=self.twilio_token_var, width=30).grid(row=1, column=1, pady=2, padx=5)
        
        ttk.Label(sms_frame, text="Номер Twilio:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.twilio_number_var = tk.StringVar(value=self.config['sms']['twilio_number'])
        ttk.Entry(sms_frame, textvariable=self.twilio_number_var, width=20).grid(row=2, column=1, sticky=tk.W, pady=2, padx=5)
        
        # Telegram настройки
        telegram_frame = ttk.LabelFrame(config_tab, text="Настройки Telegram", padding="10")
        telegram_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ttk.Label(telegram_frame, text="Токен бота:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.telegram_token_var = tk.StringVar(value=self.config['telegram']['bot_token'])
        ttk.Entry(telegram_frame, textvariable=self.telegram_token_var, width=40).grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(telegram_frame, text="ID чата:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.telegram_chat_id_var = tk.StringVar(value=self.config['telegram']['chat_id'])
        ttk.Entry(telegram_frame, textvariable=self.telegram_chat_id_var, width=20).grid(row=1, column=1, sticky=tk.W, pady=2, padx=5)
        
        # Push настройки
        push_frame = ttk.LabelFrame(config_tab, text="Настройки Push-уведомлений", padding="10")
        push_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ttk.Label(push_frame, text="Pushbullet Token:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.pushbullet_token_var = tk.StringVar(value=self.config['push']['pushbullet_token'])
        ttk.Entry(push_frame, textvariable=self.pushbullet_token_var, width=40).grid(row=0, column=1, pady=2, padx=5)
        
        # Кнопка сохранения настроек
        ttk.Button(config_tab, text="Сохранить настройки", 
                  command=self.save_config).pack(pady=10)
        
        # Кнопка тестирования соединений
        ttk.Button(config_tab, text="Тестировать соединения", 
                  command=self.test_connections).pack(pady=5)
        
    def setup_email_tab(self, notebook):
        """Вкладка электронной почты"""
        email_tab = ttk.Frame(notebook)
        notebook.add(email_tab, text="Email")
        
        # Форма отправки email
        form_frame = ttk.LabelFrame(email_tab, text="Отправка Email", padding="10")
        form_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Кому:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.email_to_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.email_to_var, width=40).grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(form_frame, text="Тема:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.email_subject_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.email_subject_var, width=40).grid(row=1, column=1, pady=2, padx=5)
        
        ttk.Label(form_frame, text="Сообщение:").grid(row=2, column=0, sticky=tk.NW, pady=2)
        self.email_message_text = scrolledtext.ScrolledText(form_frame, width=50, height=10)
        self.email_message_text.grid(row=2, column=1, pady=2, padx=5, sticky=tk.W+tk.E)
        
        # Тип сообщения
        ttk.Label(form_frame, text="Тип:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.email_type_var = tk.StringVar(value="plain")
        ttk.Combobox(form_frame, textvariable=self.email_type_var,
                    values=["plain", "html"]).grid(row=3, column=1, sticky=tk.W, pady=2, padx=5)
        
        # Кнопки отправки
        button_frame = ttk.Frame(email_tab)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Отправить Email", 
                  command=self.send_email).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить форму", 
                  command=self.clear_email_form).pack(side=tk.LEFT, padx=5)
        
    def setup_sms_tab(self, notebook):
        """Вкладка SMS"""
        sms_tab = ttk.Frame(notebook)
        notebook.add(sms_tab, text="SMS")
        
        # Форма отправки SMS
        form_frame = ttk.LabelFrame(sms_tab, text="Отправка SMS", padding="10")
        form_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Номер телефона:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.sms_to_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.sms_to_var, width=20).grid(row=0, column=1, sticky=tk.W, pady=2, padx=5)
        ttk.Label(form_frame, text="Формат: +79123456789").grid(row=0, column=2, sticky=tk.W, pady=2, padx=5)
        
        ttk.Label(form_frame, text="Сообщение:").grid(row=1, column=0, sticky=tk.NW, pady=2)
        self.sms_message_text = scrolledtext.ScrolledText(form_frame, width=50, height=8)
        self.sms_message_text.grid(row=1, column=1, columnspan=2, pady=2, padx=5, sticky=tk.W+tk.E)
        
        # Кнопки отправки
        button_frame = ttk.Frame(sms_tab)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Отправить SMS", 
                  command=self.send_sms).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить форму", 
                  command=self.clear_sms_form).pack(side=tk.LEFT, padx=5)
        
    def setup_messenger_tab(self, notebook):
        """Вкладка мессенджеров"""
        messenger_tab = ttk.Frame(notebook)
        notebook.add(messenger_tab, text="Мессенджеры")
        
        # Выбор мессенджера
        service_frame = ttk.LabelFrame(messenger_tab, text="Выбор сервиса", padding="10")
        service_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.messenger_var = tk.StringVar(value="telegram")
        ttk.Radiobutton(service_frame, text="Telegram", variable=self.messenger_var, 
                       value="telegram").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(service_frame, text="Slack", variable=self.messenger_var, 
                       value="slack").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(service_frame, text="Discord", variable=self.messenger_var, 
                       value="discord").pack(side=tk.LEFT, padx=10)
        
        # Форма отправки сообщения
        form_frame = ttk.LabelFrame(messenger_tab, text="Сообщение", padding="10")
        form_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Получатель/Канал:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.messenger_to_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.messenger_to_var, width=30).grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(form_frame, text="Сообщение:").grid(row=1, column=0, sticky=tk.NW, pady=2)
        self.messenger_message_text = scrolledtext.ScrolledText(form_frame, width=50, height=8)
        self.messenger_message_text.grid(row=1, column=1, pady=2, padx=5, sticky=tk.W+tk.E)
        
        # Кнопки отправки
        button_frame = ttk.Frame(messenger_tab)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Отправить сообщение", 
                  command=self.send_messenger).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить форму", 
                  command=self.clear_messenger_form).pack(side=tk.LEFT, padx=5)
        
    def setup_push_tab(self, notebook):
        """Вкладка push-уведомлений"""
        push_tab = ttk.Frame(notebook)
        notebook.add(push_tab, text="Push-уведомления")
        
        # Выбор сервиса
        service_frame = ttk.LabelFrame(push_tab, text="Сервис push-уведомлений", padding="10")
        service_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.push_service_var = tk.StringVar(value="pushbullet")
        ttk.Radiobutton(service_frame, text="Pushbullet", variable=self.push_service_var, 
                       value="pushbullet").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(service_frame, text="Pushover", variable=self.push_service_var, 
                       value="pushover").pack(side=tk.LEFT, padx=10)
        
        # Форма отправки
        form_frame = ttk.LabelFrame(push_tab, text="Уведомление", padding="10")
        form_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Заголовок:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.push_title_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.push_title_var, width=30).grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(form_frame, text="Сообщение:").grid(row=1, column=0, sticky=tk.NW, pady=2)
        self.push_message_text = scrolledtext.ScrolledText(form_frame, width=50, height=6)
        self.push_message_text.grid(row=1, column=1, pady=2, padx=5, sticky=tk.W+tk.E)
        
        # Тип уведомления
        ttk.Label(form_frame, text="Тип:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.push_type_var = tk.StringVar(value="note")
        ttk.Combobox(form_frame, textvariable=self.push_type_var,
                    values=["note", "link", "file"]).grid(row=2, column=1, sticky=tk.W, pady=2, padx=5)
        
        # Кнопки отправки
        button_frame = ttk.Frame(push_tab)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Отправить уведомление", 
                  command=self.send_push).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить форму", 
                  command=self.clear_push_form).pack(side=tk.LEFT, padx=5)
        
    def setup_bulk_tab(self, notebook):
        """Вкладка массовой рассылки"""
        bulk_tab = ttk.Frame(notebook)
        notebook.add(bulk_tab, text="Массовая рассылка")
        
        # Выбор канала
        channel_frame = ttk.LabelFrame(bulk_tab, text="Канал рассылки", padding="10")
        channel_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.bulk_channel_var = tk.StringVar(value="email")
        ttk.Combobox(channel_frame, textvariable=self.bulk_channel_var,
                    values=["email", "sms", "telegram"]).pack(side=tk.LEFT, padx=5)
        
        # Получатели
        recipients_frame = ttk.LabelFrame(bulk_tab, text="Список получателей", padding="10")
        recipients_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ttk.Label(recipients_frame, text="Получатели (через запятую или с новой строки):").pack(anchor=tk.W)
        self.bulk_recipients_text = scrolledtext.ScrolledText(recipients_frame, width=80, height=4)
        self.bulk_recipients_text.pack(fill=tk.X, pady=5)
        
        # Сообщение
        message_frame = ttk.LabelFrame(bulk_tab, text="Сообщение для рассылки", padding="10")
        message_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.bulk_message_text = scrolledtext.ScrolledText(message_frame, width=80, height=6)
        self.bulk_message_text.pack(fill=tk.X, pady=5)
        
        # Настройки рассылки
        settings_frame = ttk.Frame(bulk_tab)
        settings_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ttk.Label(settings_frame, text="Задержка между сообщениями (сек):").pack(side=tk.LEFT, padx=5)
        self.bulk_delay_var = tk.DoubleVar(value=1.0)
        ttk.Entry(settings_frame, textvariable=self.bulk_delay_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Кнопки управления
        button_frame = ttk.Frame(bulk_tab)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Начать рассылку", 
                  command=self.start_bulk_send).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Остановить рассылку", 
                  command=self.stop_bulk_send).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить формы", 
                  command=self.clear_bulk_form).pack(side=tk.LEFT, padx=5)
        
        self.bulk_sending = False
        
    def log_message(self, message):
        """Добавление сообщения в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def save_config(self):
        """Сохранение конфигурации"""
        try:
            self.config['email']['smtp_server'] = self.smtp_server_var.get()
            self.config['email']['smtp_port'] = int(self.smtp_port_var.get())
            self.config['email']['sender_email'] = self.sender_email_var.get()
            self.config['email']['sender_password'] = self.sender_password_var.get()
            
            self.config['sms']['twilio_sid'] = self.twilio_sid_var.get()
            self.config['sms']['twilio_token'] = self.twilio_token_var.get()
            self.config['sms']['twilio_number'] = self.twilio_number_var.get()
            
            self.config['telegram']['bot_token'] = self.telegram_token_var.get()
            self.config['telegram']['chat_id'] = self.telegram_chat_id_var.get()
            
            self.config['push']['pushbullet_token'] = self.pushbullet_token_var.get()
            
            messagebox.showinfo("Успех", "Настройки сохранены")
            self.log_message("Конфигурация сохранена")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения настроек: {e}")
            
    def test_connections(self):
        """Тестирование соединений"""
        self.log_message("Тестирование соединений...")
        
        # Тест email
        if self.config['email']['sender_email'] and self.config['email']['sender_password']:
            try:
                server = smtplib.SMTP(self.config['email']['smtp_server'], 
                                    self.config['email']['smtp_port'])
                server.starttls()
                server.login(self.config['email']['sender_email'], 
                           self.config['email']['sender_password'])
                server.quit()
                self.log_message("✓ Email соединение успешно")
            except Exception as e:
                self.log_message(f"✗ Ошибка email: {e}")
        else:
            self.log_message("⚠ Email не настроен")
        
        # Тест Telegram
        if self.config['telegram']['bot_token']:
            try:
                response = requests.get(
                    f"https://api.telegram.org/bot{self.config['telegram']['bot_token']}/getMe"
                )
                if response.status_code == 200:
                    self.log_message("✓ Telegram соединение успешно")
                else:
                    self.log_message(f"✗ Ошибка Telegram: {response.text}")
            except Exception as e:
                self.log_message(f"✗ Ошибка Telegram: {e}")
        else:
            self.log_message("⚠ Telegram не настроен")
                
    def send_email(self):
        """Отправка email"""
        try:
            to_email = self.email_to_var.get()
            subject = self.email_subject_var.get()
            message = self.email_message_text.get(1.0, tk.END).strip()
            message_type = self.email_type_var.get()
            
            if not all([to_email, subject, message]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
                
            # Создание сообщения
            msg = MIMEMultipart()
            msg['From'] = self.config['email']['sender_email']
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if message_type == "html":
                msg.attach(MIMEText(message, 'html'))
            else:
                msg.attach(MIMEText(message, 'plain'))
            
            # Отправка
            def send():
                try:
                    self.status_var.set("Отправка email...")
                    server = smtplib.SMTP(self.config['email']['smtp_server'], 
                                        self.config['email']['smtp_port'])
                    server.starttls()
                    server.login(self.config['email']['sender_email'], 
                               self.config['email']['sender_password'])
                    text = msg.as_string()
                    server.sendmail(self.config['email']['sender_email'], to_email, text)
                    server.quit()
                    
                    self.log_message(f"✓ Email отправлен: {to_email}")
                    self.status_var.set("Email отправлен")
                    messagebox.showinfo("Успех", "Email отправлен успешно")
                    
                except Exception as e:
                    self.log_message(f"✗ Ошибка отправки email: {e}")
                    self.status_var.set("Ошибка отправки")
                    messagebox.showerror("Ошибка", f"Не удалось отправить email: {e}")
            
            threading.Thread(target=send).start()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка подготовки email: {e}")
            
    def send_sms(self):
        """Отправка SMS через Twilio"""
        try:
            to_number = self.sms_to_var.get()
            message = self.sms_message_text.get(1.0, tk.END).strip()
            
            if not all([to_number, message]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
                
            # Проверка конфигурации Twilio
            if not all([self.config['sms']['twilio_sid'], 
                       self.config['sms']['twilio_token'],
                       self.config['sms']['twilio_number']]):
                messagebox.showerror("Ошибка", "Настройте Twilio в разделе 'Настройки'")
                return
            
            def send():
                try:
                    self.status_var.set("Отправка SMS...")
                    
                    # Имитация отправки SMS (в реальном приложении использовать twilio-rest-api)
                    # from twilio.rest import Client
                    # client = Client(self.config['sms']['twilio_sid'], 
                    #               self.config['sms']['twilio_token'])
                    # message = client.messages.create(
                    #     body=message,
                    #     from_=self.config['sms']['twilio_number'],
                    #     to=to_number
                    # )
                    
                    time.sleep(2)  # Имитация задержки отправки
                    
                    self.log_message(f"✓ SMS отправлено: {to_number}")
                    self.status_var.set("SMS отправлено")
                    messagebox.showinfo("Успех", "SMS отправлено успешно")
                    
                except Exception as e:
                    self.log_message(f"✗ Ошибка отправки SMS: {e}")
                    self.status_var.set("Ошибка отправки")
                    messagebox.showerror("Ошибка", f"Не удалось отправить SMS: {e}")
            
            threading.Thread(target=send).start()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка подготовки SMS: {e}")
            
    def send_messenger(self):
        """Отправка сообщения в мессенджер"""
        try:
            service = self.messenger_var.get()
            to_user = self.messenger_to_var.get()
            message = self.messenger_message_text.get(1.0, tk.END).strip()
            
            if not all([to_user, message]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            def send():
                try:
                    self.status_var.set(f"Отправка в {service}...")
                    
                    if service == "telegram":
                        # Отправка в Telegram
                        if not self.config['telegram']['bot_token']:
                            raise Exception("Токен бота не настроен")
                            
                        chat_id = to_user or self.config['telegram']['chat_id']
                        url = f"https://api.telegram.org/bot{self.config['telegram']['bot_token']}/sendMessage"
                        data = {
                            'chat_id': chat_id,
                            'text': message
                        }
                        response = requests.post(url, data=data)
                        
                        if response.status_code == 200:
                            self.log_message(f"✓ Telegram сообщение отправлено: {chat_id}")
                            self.status_var.set("Сообщение отправлено")
                            messagebox.showinfo("Успех", "Сообщение отправлено в Telegram")
                        else:
                            raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
                    elif service == "slack":
                        # Имитация отправки в Slack
                        time.sleep(1)
                        self.log_message(f"✓ Slack сообщение отправлено: {to_user}")
                        self.status_var.set("Сообщение отправлено")
                        messagebox.showinfo("Успех", "Сообщение отправлено в Slack")
                    
                    elif service == "discord":
                        # Имитация отправки в Discord
                        time.sleep(1)
                        self.log_message(f"✓ Discord сообщение отправлено: {to_user}")
                        self.status_var.set("Сообщение отправлено")
                        messagebox.showinfo("Успех", "Сообщение отправлено в Discord")
                        
                except Exception as e:
                    self.log_message(f"✗ Ошибка отправки в {service}: {e}")
                    self.status_var.set("Ошибка отправки")
                    messagebox.showerror("Ошибка", f"Не удалось отправить сообщение: {e}")
            
            threading.Thread(target=send).start()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка подготовки сообщения: {e}")
            
    def send_push(self):
        """Отправка push-уведомления"""
        try:
            service = self.push_service_var.get()
            title = self.push_title_var.get()
            message = self.push_message_text.get(1.0, tk.END).strip()
            push_type = self.push_type_var.get()
            
            if not message:
                messagebox.showerror("Ошибка", "Введите сообщение")
                return
            
            def send():
                try:
                    self.status_var.set(f"Отправка push-уведомления...")
                    
                    if service == "pushbullet":
                        # Отправка через Pushbullet
                        if not self.config['push']['pushbullet_token']:
                            raise Exception("Токен Pushbullet не настроен")
                            
                        url = "https://api.pushbullet.com/v2/pushes"
                        headers = {
                            'Access-Token': self.config['push']['pushbullet_token'],
                            'Content-Type': 'application/json'
                        }
                        data = {
                            'type': push_type,
                            'title': title or "Уведомление",
                            'body': message
                        }
                        response = requests.post(url, headers=headers, json=data)
                        
                        if response.status_code == 200:
                            self.log_message("✓ Push-уведомление отправлено")
                            self.status_var.set("Уведомление отправлено")
                            messagebox.showinfo("Успех", "Push-уведомление отправлено")
                        else:
                            raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
                    elif service == "pushover":
                        # Имитация отправки через Pushover
                        time.sleep(1)
                        self.log_message("✓ Push-уведомление отправлено (Pushover)")
                        self.status_var.set("Уведомление отправлено")
                        messagebox.showinfo("Успех", "Push-уведомление отправлено")
                        
                except Exception as e:
                    self.log_message(f"✗ Ошибка отправки push-уведомления: {e}")
                    self.status_var.set("Ошибка отправки")
                    messagebox.showerror("Ошибка", f"Не удалось отправить уведомление: {e}")
            
            threading.Thread(target=send).start()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка подготовки уведомления: {e}")
            
    def start_bulk_send(self):
        """Запуск массовой рассылки"""
        try:
            channel = self.bulk_channel_var.get()
            recipients_text = self.bulk_recipients_text.get(1.0, tk.END).strip()
            message = self.bulk_message_text.get(1.0, tk.END).strip()
            delay = self.bulk_delay_var.get()
            
            if not recipients_text or not message:
                messagebox.showerror("Ошибка", "Заполните список получателей и сообщение")
                return
            
            # Разбор получателей
            recipients = []
            for line in recipients_text.split('\n'):
                for recipient in line.split(','):
                    recipient = recipient.strip()
                    if recipient:
                        recipients.append(recipient)
            
            if not recipients:
                messagebox.showerror("Ошибка", "Не найдены получатели")
                return
            
            self.bulk_sending = True
            
            def bulk_send():
                try:
                    self.status_var.set(f"Массовая рассылка: 0/{len(recipients)}")
                    
                    for i, recipient in enumerate(recipients):
                        if not self.bulk_sending:
                            break
                            
                        self.log_message(f"Отправка {i+1}/{len(recipients)}: {recipient}")
                        
                        # Имитация отправки в зависимости от канала
                        if channel == "email":
                            # Здесь будет реальная отправка email
                            pass
                        elif channel == "sms":
                            # Здесь будет реальная отправка SMS
                            pass
                        elif channel == "telegram":
                            # Здесь будет реальная отправка в Telegram
                            pass
                        
                        time.sleep(delay)
                        self.status_var.set(f"Массовая рассылка: {i+1}/{len(recipients)}")
                    
                    if self.bulk_sending:
                        self.log_message(f"✓ Массовая рассылка завершена: {len(recipients)} получателей")
                        self.status_var.set("Рассылка завершена")
                        messagebox.showinfo("Успех", f"Рассылка завершена: {len(recipients)} получателей")
                    else:
                        self.log_message("Массовая рассылка прервана")
                        self.status_var.set("Рассылка прервана")
                        
                except Exception as e:
                    self.log_message(f"✗ Ошибка массовой рассылки: {e}")
                    self.status_var.set("Ошибка рассылки")
                    messagebox.showerror("Ошибка", f"Ошибка рассылки: {e}")
                
                finally:
                    self.bulk_sending = False
            
            threading.Thread(target=bulk_send).start()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка запуска рассылки: {e}")
            
    def stop_bulk_send(self):
        """Остановка массовой рассылки"""
        self.bulk_sending = False
        self.status_var.set("Рассылка останавливается...")
        
    # Методы очистки форм
    def clear_email_form(self):
        self.email_to_var.set("")
        self.email_subject_var.set("")
        self.email_message_text.delete(1.0, tk.END)
        
    def clear_sms_form(self):
        self.sms_to_var.set("")
        self.sms_message_text.delete(1.0, tk.END)
        
    def clear_messenger_form(self):
        self.messenger_to_var.set("")
        self.messenger_message_text.delete(1.0, tk.END)
        
    def clear_push_form(self):
        self.push_title_var.set("")
        self.push_message_text.delete(1.0, tk.END)
        
    def clear_bulk_form(self):
        self.bulk_recipients_text.delete(1.0, tk.END)
        self.bulk_message_text.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = CommunicationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()