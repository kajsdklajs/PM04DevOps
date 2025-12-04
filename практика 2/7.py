import tkinter as tk
import random
import math

class RandomGraphPlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("Семенов Павел")
        self.root.geometry("700x600")
        
        self.canvas = tk.Canvas(root, bg='#0f0f23', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.button = tk.Button(root, text="Сгенерировать график", 
                               command=self.plot_random_numbers,
                               font=("Arial", 12, "bold"),
                               bg='#00ff9d',
                               fg='#0f0f23',
                               relief=tk.RAISED,
                               bd=3)
        self.button.pack(pady=10)
        
        self.info_label = tk.Label(root, text="1000 случайных точек (0-100)", 
                                  font=("Arial", 10),
                                  fg='#00ff9d',
                                  bg='#0f0f23')
        self.info_label.pack()
        
        self.canvas_width = 680
        self.canvas_height = 500
        self.margin = 50
        
        self.draw_grid()
        self.plot_random_numbers()

    def draw_grid(self):
        self.canvas.delete("all")
        
        grid_color = '#1a1a2e'
        axis_color = '#4cc9f0'
        text_color = '#f72585'
        
        for x in range(0, 11):
            x_pos = self.margin + (x * (self.canvas_width - 2 * self.margin) / 10)
            self.canvas.create_line(x_pos, self.margin, x_pos, self.canvas_height, fill=grid_color, width=1)
            self.canvas.create_text(x_pos, self.canvas_height + 20, text=str(x*10), fill=text_color, font=("Arial", 9))
        
        for y in range(0, 11):
            y_pos = self.canvas_height - (y * (self.canvas_height - 2 * self.margin) / 10)
            self.canvas.create_line(self.margin, y_pos, self.canvas_width, y_pos, fill=grid_color, width=1)
            self.canvas.create_text(self.margin - 25, y_pos, text=str(y*10), fill=text_color, font=("Arial", 9))
        
        self.canvas.create_line(self.margin, self.margin, self.margin, self.canvas_height, fill=axis_color, width=2)
        self.canvas.create_line(self.margin, self.canvas_height, self.canvas_width, self.canvas_height, fill=axis_color, width=2)
        
        self.canvas.create_text(self.margin - 40, self.margin - 20, text="Y", fill=axis_color, font=("Arial", 12, "bold"))
        self.canvas.create_text(self.canvas_width + 20, self.canvas_height + 10, text="X", fill=axis_color, font=("Arial", 12, "bold"))

    def plot_random_numbers(self):
        self.draw_grid()
        
        points = []
        colors = ['#f72585', '#4361ee', '#4cc9f0', '#00ff9d', '#ff9e00']
        
        for i in range(1000):
            x = random.uniform(0, 100)
            y = random.uniform(0, 100)
            points.append((x, y))
            
            canvas_x = self.margin + (x * (self.canvas_width - 2 * self.margin) / 100)
            canvas_y = self.canvas_height - (y * (self.canvas_height - 2 * self.margin) / 100)
            
            color = colors[i % len(colors)]
            
            size = 3 + math.sin(i * 0.1) * 1.5
            
            self.canvas.create_oval(canvas_x - size, canvas_y - size,
                                   canvas_x + size, canvas_y + size,
                                   fill=color, outline='', width=0, tags="point")
            
            if i % 100 == 0:
                self.root.update()
        
        self.calculate_statistics(points)

    def calculate_statistics(self, points):
        x_vals = [p[0] for p in points]
        y_vals = [p[1] for p in points]
        
        avg_x = sum(x_vals) / len(x_vals)
        avg_y = sum(y_vals) / len(y_vals)
        
        canvas_avg_x = self.margin + (avg_x * (self.canvas_width - 2 * self.margin) / 100)
        canvas_avg_y = self.canvas_height - (avg_y * (self.canvas_height - 2 * self.margin) / 100)
        
        self.canvas.create_oval(canvas_avg_x - 8, canvas_avg_y - 8,
                               canvas_avg_x + 8, canvas_avg_y + 8,
                               fill='#ff0000', outline='white', width=2, tags="avg")
        
        self.canvas.create_text(canvas_avg_x, canvas_avg_y - 20, 
                               text=f"Среднее: ({avg_x:.1f}, {avg_y:.1f})", 
                               fill='white', font=("Arial", 9, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomGraphPlotter(root)
    root.mainloop()