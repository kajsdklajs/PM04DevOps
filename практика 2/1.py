import tkinter as tk
from math import cos, sin, pi, sqrt
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

class ShapedButton(tk.Canvas):
    """Базовый класс для кнопок произвольной формы"""
    
    def __init__(self, parent, text="Кнопка", command=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command
        self.text = text
        self.state = "normal"
        self.hovered = False

        self.normal_color = "#4A90E2"
        self.hover_color = "#357ABD"
        self.active_color = "#2C649D"
        self.disabled_color = "#CCCCCC"
        self.text_color = "white"
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        
        self.draw_button()
    
    def draw_button(self):
        """Абстрактный метод - должен быть переопределен в дочерних классах"""
        pass
    
    def on_enter(self, event):
        if self.state == "normal":
            self.hovered = True
            self.draw_button()
    
    def on_leave(self, event):
        self.hovered = False
        self.draw_button()
    
    def on_press(self, event):
        if self.state == "normal":
            self.draw_button(pressed=True)
    
    def on_release(self, event):
        if self.state == "normal":
            self.hovered = True
            self.draw_button()
            if self.command:
                self.command()
    
    def configure_state(self, state):
        self.state = state
        self.draw_button()
    
    def get_fill_color(self):
        if self.state == "disabled":
            return self.disabled_color
        elif self.state == "active" or self.hovered:
            return self.hover_color
        else:
            return self.normal_color

class TriangularButton(ShapedButton):
    """Треугольная кнопка"""
    
    def __init__(self, parent, text="▶", command=None, direction="right", **kwargs):
        self.direction = direction
        super().__init__(parent, text, command, **kwargs)
    
    def draw_button(self, pressed=False):
        self.delete("all")
        
        width = self.winfo_width() or 60
        height = self.winfo_height() or 60

        if self.direction == "right":
            points = [10, 10, width-10, height//2, 10, height-10]
        elif self.direction == "left":
            points = [width-10, 10, 10, height//2, width-10, height-10]
        elif self.direction == "up":
            points = [10, height-10, width//2, 10, width-10, height-10]
        elif self.direction == "down":
            points = [10, 10, width//2, height-10, width-10, 10]
        else:  
            points = [10, 10, width-10, height//2, 10, height-10]

        fill_color = self.get_fill_color()

        self.create_polygon(points, 
                           fill=fill_color, 
                           outline="#2C649D", 
                           width=2,
                           tags="button")

        self.create_text(width//2, height//2, 
                        text=self.text, 
                        fill=self.text_color,
                        font=("Arial", 12, "bold"),
                        tags="text")

class StarButton(ShapedButton):
    """Кнопка в виде звезды"""
    
    def draw_button(self, pressed=False):
        self.delete("all")
        
        width = self.winfo_width() or 60
        height = self.winfo_height() or 60
        center_x, center_y = width//2, height//2
        radius = min(width, height)//2 - 10

        points = []
        for i in range(10):
            angle = pi/2 + 2*pi*i/10
            if i % 2 == 0:
                r = radius
            else:
                r = radius * 0.4
            x = center_x + r * cos(angle)
            y = center_y + r * sin(angle)
            points.extend([x, y])
        
        fill_color = self.get_fill_color()
        
        self.create_polygon(points,
                           fill=fill_color,
                           outline="#2C649D",
                           width=2,
                           tags="button")
        
        self.create_text(center_x, center_y,
                        text=self.text,
                        fill=self.text_color,
                        font=("Arial", 10),
                        tags="text")

class HexagonalButton(ShapedButton):
    """Шестиугольная кнопка"""
    
    def draw_button(self, pressed=False):
        self.delete("all")
        
        width = self.winfo_width() or 80
        height = self.winfo_height() or 80
        center_x, center_y = width//2, height//2
        radius = min(width, height)//2 - 10
        
        points = []
        for i in range(6):
            angle = pi/6 + 2*pi*i/6
            x = center_x + radius * cos(angle)
            y = center_y + radius * sin(angle)
            points.extend([x, y])
        
        fill_color = self.get_fill_color()
        
        self.create_polygon(points,
                           fill=fill_color,
                           outline="#2C649D",
                           width=2,
                           tags="button")
        
        self.create_text(center_x, center_y,
                        text=self.text,
                        fill=self.text_color,
                        font=("Arial", 12, "bold"),
                        tags="text")

class OctagonalButton(ShapedButton):
    """Восьмиугольная кнопка"""
    
    def draw_button(self, pressed=False):
        self.delete("all")
        
        width = self.winfo_width() or 80
        height = self.winfo_height() or 80
        center_x, center_y = width//2, height//2
        radius = min(width, height)//2 - 10
        
        points = []
        for i in range(8):
            angle = pi/8 + 2*pi*i/8
            x = center_x + radius * cos(angle)
            y = center_y + radius * sin(angle)
            points.extend([x, y])
        
        fill_color = self.get_fill_color()
        
        self.create_polygon(points,
                           fill=fill_color,
                           outline="#2C649D",
                           width=2,
                           tags="button")
        
        self.create_text(center_x, center_y,
                        text=self.text,
                        fill=self.text_color,
                        font=("Arial", 11, "bold"),
                        tags="text")

class OvalDoubleButton(ShapedButton):
    """Двойная овальная кнопка"""
    
    def draw_button(self, pressed=False):
        self.delete("all")
        
        width = self.winfo_width() or 100
        height = self.winfo_height() or 50
        
        fill_color = self.get_fill_color()

        self.create_oval(5, 5, width-5, height-5,
                        fill=fill_color,
                        outline="#2C649D",
                        width=2,
                        tags="button")

        self.create_oval(15, 15, width-15, height-15,
                        outline=self.text_color,
                        width=1,
                        tags="button")
        
        self.create_text(width//2, height//2,
                        text=self.text,
                        fill=self.text_color,
                        font=("Arial", 12, "bold"),
                        tags="text")

class ModernRoundedButton(ShapedButton):
    """Современная кнопка со скругленными углами"""
    
    def draw_button(self, pressed=False):
        self.delete("all")
        
        width = self.winfo_width() or 120
        height = self.winfo_height() or 40
        radius = 15
        
        fill_color = self.get_fill_color()

        self.create_round_rect(5, 5, width-5, height-5, radius,
                              fill=fill_color,
                              outline="#2C649D",
                              width=2)
        
        self.create_text(width//2, height//2,
                        text=self.text,
                        fill=self.text_color,
                        font=("Arial", 12, "bold"),
                        tags="text")
    
    def create_round_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Создает прямоугольник со скругленными углами"""
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1,
            x1+radius, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

def create_example_app():
    """Создание демонстрационного приложения"""
    root = tk.Tk()
    root.title("Семенов Павел")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    title = tk.Label(root, text="Кнопки различных геометрических форм", 
                     font=("Arial", 16, "bold"), bg="#f0f0f0")
    title.pack(pady=20)

    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    buttons_info = [
        (TriangularButton, "Треугольная кнопка", {"direction": "right"}),
        (StarButton, "Звезда", {}),
        (HexagonalButton, "Шестиугольник", {}),
        (OctagonalButton, "Восьмиугольник", {}),
        (OvalDoubleButton, "Двойная овальная", {}),
        (ModernRoundedButton, "Скругленная", {})
    ]

    for i, (btn_class, text, kwargs) in enumerate(buttons_info):
        row = i // 3
        col = i % 3

        btn_frame = tk.Frame(frame, bg="#f0f0f0")
        btn_frame.grid(row=row*2, column=col, padx=20, pady=20)

        btn = btn_class(btn_frame, 
                       text=text.split()[0], 
                       command=lambda t=text: print(f"Нажата {t}"),
                       width=100, 
                       height=100,
                       **kwargs)
        btn.pack()

        label = tk.Label(btn_frame, text=text, bg="#f0f0f0", font=("Arial", 10))
        label.pack(pady=5)

    def disable_all():
        for widget in frame.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, ShapedButton):
                    child.configure_state("disabled")
    
    def enable_all():
        for widget in frame.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, ShapedButton):
                    child.configure_state("normal")
    
    control_frame = tk.Frame(root, bg="#f0f0f0")
    control_frame.pack(pady=20)
    
    tk.Button(control_frame, text="Отключить все кнопки", 
              command=disable_all, bg="#FF6B6B", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="Включить все кнопки", 
              command=enable_all, bg="#4ECDC4", fg="white").pack(side=tk.LEFT, padx=5)

    info = tk.Label(root, 
                    text="Наведите курсор и кликните на кнопки для демонстрации hover-эффекта",
                    bg="#f0f0f0", 
                    font=("Arial", 10, "italic"))
    info.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    create_example_app()