import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
import json
import csv
from datetime import datetime

class RandomNumberGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Семенов Павел")
        self.root.geometry("700x600")
        
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        settings_frame = tk.LabelFrame(main_frame, text="Настройки генерации", padx=10, pady=10)
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(settings_frame, text="Количество чисел:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.count_var = tk.IntVar(value=100)
        self.count_spin = tk.Spinbox(settings_frame, from_=1, to=10000, textvariable=self.count_var, width=15)
        self.count_spin.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(settings_frame, text="От:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.min_var = tk.IntVar(value=0)
        self.min_spin = tk.Spinbox(settings_frame, from_=-1000000, to=1000000, textvariable=self.min_var, width=15)
        self.min_spin.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(settings_frame, text="До:").grid(row=1, column=2, sticky=tk.W, pady=5, padx=(20,0))
        self.max_var = tk.IntVar(value=100)
        self.max_spin = tk.Spinbox(settings_frame, from_=-1000000, to=1000000, textvariable=self.max_var, width=15)
        self.max_spin.grid(row=1, column=3, pady=5, padx=5)
        
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.generate_btn = tk.Button(button_frame, text="Сгенерировать", command=self.generate_numbers,
                                     bg="#4CAF50", fg="white", font=("Arial", 11), width=15)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_json_btn = tk.Button(button_frame, text="Сохранить JSON", command=self.save_json,
                                      bg="#2196F3", fg="white", font=("Arial", 11), width=15)
        self.save_json_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_csv_btn = tk.Button(button_frame, text="Сохранить CSV", command=self.save_csv,
                                     bg="#FF9800", fg="white", font=("Arial", 11), width=15)
        self.save_csv_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_txt_btn = tk.Button(button_frame, text="Сохранить TXT", command=self.save_txt,
                                     bg="#9C27B0", fg="white", font=("Arial", 11), width=15)
        self.save_txt_btn.pack(side=tk.LEFT, padx=5)
        
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_area = tk.Text(text_frame, height=15, font=("Consolas", 10))
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=scrollbar.set)
        
        stats_frame = tk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.stats_label = tk.Label(stats_frame, text="", font=("Arial", 10))
        self.stats_label.pack()
        
        self.generated_numbers = []
        
        self.save_json_btn.config(state=tk.DISABLED)
        self.save_csv_btn.config(state=tk.DISABLED)
        self.save_txt_btn.config(state=tk.DISABLED)

    def generate_numbers(self):
        try:
            count = self.count_var.get()
            min_val = self.min_var.get()
            max_val = self.max_var.get()
            
            if min_val > max_val:
                min_val, max_val = max_val, min_val
                self.min_var.set(min_val)
                self.max_var.set(max_val)
            
            self.generated_numbers = [random.randint(min_val, max_val) for _ in range(count)]
            
            self.text_area.delete(1.0, tk.END)
            
            for i in range(0, len(self.generated_numbers), 10):
                chunk = self.generated_numbers[i:i+10]
                line = " ".join(f"{num:8}" for num in chunk)
                self.text_area.insert(tk.END, line + "\n")
            
            self.update_stats()
            
            self.save_json_btn.config(state=tk.NORMAL)
            self.save_csv_btn.config(state=tk.NORMAL)
            self.save_txt_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def update_stats(self):
        if not self.generated_numbers:
            return
        
        min_val = min(self.generated_numbers)
        max_val = max(self.generated_numbers)
        avg_val = sum(self.generated_numbers) / len(self.generated_numbers)
        sum_val = sum(self.generated_numbers)
        
        stats_text = (f"Количество: {len(self.generated_numbers)} | "
                     f"Мин: {min_val} | Макс: {max_val} | "
                     f"Среднее: {avg_val:.2f} | Сумма: {sum_val}")
        self.stats_label.config(text=stats_text)

    def save_json(self):
        if not self.generated_numbers:
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"numbers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if filename:
            try:
                data = {
                    "metadata": {
                        "generated": datetime.now().isoformat(),
                        "count": len(self.generated_numbers),
                        "range": [self.min_var.get(), self.max_var.get()]
                    },
                    "numbers": self.generated_numbers,
                    "statistics": {
                        "min": min(self.generated_numbers),
                        "max": max(self.generated_numbers),
                        "average": sum(self.generated_numbers) / len(self.generated_numbers),
                        "sum": sum(self.generated_numbers)
                    }
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Успех", f"Данные сохранены в {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def save_csv(self):
        if not self.generated_numbers:
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"numbers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    
                    writer.writerow(["Дата генерации", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                    writer.writerow(["Количество чисел", len(self.generated_numbers)])
                    writer.writerow(["Диапазон", f"{self.min_var.get()} - {self.max_var.get()}"])
                    writer.writerow([])
                    writer.writerow(["Номер", "Значение"])
                    
                    for i, num in enumerate(self.generated_numbers, 1):
                        writer.writerow([i, num])
                    
                    writer.writerow([])
                    writer.writerow(["Статистика", ""])
                    writer.writerow(["Минимальное", min(self.generated_numbers)])
                    writer.writerow(["Максимальное", max(self.generated_numbers)])
                    writer.writerow(["Среднее", sum(self.generated_numbers) / len(self.generated_numbers)])
                    writer.writerow(["Сумма", sum(self.generated_numbers)])
                
                messagebox.showinfo("Успех", f"Данные сохранены в {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def save_txt(self):
        if not self.generated_numbers:
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"numbers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("=" * 50 + "\n")
                    f.write(f"Сгенерированные числа (Семенов Павел)\n")
                    f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Количество: {len(self.generated_numbers)}\n")
                    f.write(f"Диапазон: {self.min_var.get()} - {self.max_var.get()}\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for i in range(0, len(self.generated_numbers), 10):
                        chunk = self.generated_numbers[i:i+10]
                        line = " ".join(f"{num:8}" for num in chunk)
                        f.write(line + "\n")
                    
                    f.write("\n" + "=" * 50 + "\n")
                    f.write("СТАТИСТИКА:\n")
                    f.write(f"Минимальное: {min(self.generated_numbers)}\n")
                    f.write(f"Максимальное: {max(self.generated_numbers)}\n")
                    f.write(f"Среднее: {sum(self.generated_numbers) / len(self.generated_numbers):.2f}\n")
                    f.write(f"Сумма: {sum(self.generated_numbers)}\n")
                    f.write("=" * 50 + "\n")
                
                messagebox.showinfo("Успех", f"Данные сохранены в {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomNumberGeneratorApp(root)
    root.mainloop()