import tkinter as tk
import random
import math

class RandomVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Семенов Павел")
        self.root.geometry("800x650")
        
        self.control_frame = tk.Frame(root, bg='#1a1a2e')
        self.control_frame.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(self.control_frame, text="Количество:", font=("Arial", 11), bg='#1a1a2e', fg='white').pack(side=tk.LEFT, padx=5)
        
        self.count_var = tk.IntVar(value=100)
        self.count_spinbox = tk.Spinbox(self.control_frame, from_=1, to=1000, textvariable=self.count_var, 
                                       width=10, font=("Arial", 11))
        self.count_spinbox.pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.control_frame, text="От:", font=("Arial", 11), bg='#1a1a2e', fg='white').pack(side=tk.LEFT, padx=(20,5))
        
        self.min_var = tk.IntVar(value=0)
        self.min_spinbox = tk.Spinbox(self.control_frame, from_=-1000, to=1000, textvariable=self.min_var, 
                                     width=10, font=("Arial", 11))
        self.min_spinbox.pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.control_frame, text="До:", font=("Arial", 11), bg='#1a1a2e', fg='white').pack(side=tk.LEFT, padx=(20,5))
        
        self.max_var = tk.IntVar(value=100)
        self.max_spinbox = tk.Spinbox(self.control_frame, from_=-1000, to=1000, textvariable=self.max_var, 
                                     width=10, font=("Arial", 11))
        self.max_spinbox.pack(side=tk.LEFT, padx=5)
        
        self.generate_button = tk.Button(self.control_frame, text="Генерировать", 
                                        command=self.generate_and_plot,
                                        font=("Arial", 11, "bold"),
                                        bg='#4361ee',
                                        fg='white',
                                        padx=20)
        self.generate_button.pack(side=tk.LEFT, padx=20)
        
        self.canvas = tk.Canvas(root, bg='#0f0f23', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,10))
        
        self.info_label = tk.Label(root, text="", font=("Arial", 10), bg='#1a1a2e', fg='white')
        self.info_label.pack(pady=5)
        
        self.canvas_width = 760
        self.canvas_height = 500
        
        self.draw_empty_graph()

    def draw_empty_graph(self):
        self.canvas.delete("all")
        
        grid_color = '#2d2d44'
        axis_color = '#4cc9f0'
        
        self.canvas.create_line(50, self.canvas_height - 50, self.canvas_width - 50, self.canvas_height - 50, 
                               fill=axis_color, width=2)
        self.canvas.create_line(50, 50, 50, self.canvas_height - 50, fill=axis_color, width=2)
        
        for i in range(0, 11):
            x_pos = 50 + (i * (self.canvas_width - 100) / 10)
            self.canvas.create_line(x_pos, self.canvas_height - 55, x_pos, self.canvas_height - 45, 
                                   fill=axis_color, width=2)
            
            y_pos = self.canvas_height - 50 - (i * (self.canvas_height - 100) / 10)
            self.canvas.create_line(45, y_pos, 55, y_pos, fill=axis_color, width=2)

    def generate_and_plot(self):
        try:
            count = self.count_var.get()
            min_val = self.min_var.get()
            max_val = self.max_var.get()
            
            if count > 1000:
                count = 1000
                self.count_var.set(1000)
            
            if min_val >= max_val:
                max_val = min_val + 1
                self.max_var.set(max_val)
            
            numbers = [random.randint(min_val, max_val) for _ in range(count)]
            
            self.visualize_numbers(numbers, min_val, max_val)
            
            avg = sum(numbers) / len(numbers)
            min_num = min(numbers)
            max_num = max(numbers)
            
            self.info_label.config(
                text=f"Чисел: {count} | Диапазон: [{min_val}, {max_val}] | "
                     f"Среднее: {avg:.2f} | Мин: {min_num} | Макс: {max_num}"
            )
            
        except Exception:
            pass

    def visualize_numbers(self, numbers, min_val, max_val):
        self.draw_empty_graph()
        
        if max_val == min_val:
            max_val = min_val + 1
        
        colors = ['#f72585', '#4361ee', '#4cc9f0', '#7209b7', '#00ff9d']
        width = self.canvas_width - 100
        height = self.canvas_height - 100
        
        bar_width = max(1, width / len(numbers))
        
        for i, value in enumerate(numbers):
            normalized = (value - min_val) / (max_val - min_val)
            
            x = 50 + (i * width / len(numbers))
            bar_height = normalized * height
            
            color = colors[i % len(colors)]
            
            if bar_height > 0:
                self.canvas.create_rectangle(
                    x, self.canvas_height - 50 - bar_height,
                    x + bar_width, self.canvas_height - 50,
                    fill=color, outline='', width=0
                )
            
            if len(numbers) <= 50 and i % max(1, len(numbers)//20) == 0:
                self.canvas.create_text(
                    x + bar_width/2, self.canvas_height - 35,
                    text=str(value), font=("Arial", 7), fill='white',
                    angle=45 if len(numbers) > 20 else 0
                )
            
            if i % 100 == 0:
                self.root.update()
        
        avg_value = sum(numbers) / len(numbers)
        avg_normalized = (avg_value - min_val) / (max_val - min_val)
        avg_y = self.canvas_height - 50 - (avg_normalized * height)
        
        self.canvas.create_line(
            50, avg_y, self.canvas_width - 50, avg_y,
            fill='#ff0000', width=2, dash=(5, 3)
        )
        
        self.canvas.create_text(
            self.canvas_width - 40, avg_y - 10,
            text=f"Ср: {avg_value:.1f}", font=("Arial", 9, "bold"), fill='#ff0000'
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomVisualizer(root)
    root.mainloop()