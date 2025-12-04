import tkinter as tk
import math

class RadioTuner:
    def __init__(self, root):
        self.root = root
        self.root.title("Семенов Павел")
        self.root.geometry("600x500")
        self.root.configure(bg='#1a1a2e')
        
        self.current_freq = 90.0
        self.target_freq = 90.0
        self.animation_id = None
        
        self.canvas = tk.Canvas(
            root,
            width=500,
            height=400,
            bg='#1a1a2e',
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        
        self.label = tk.Label(
            root,
            text="90.0 МГц",
            font=("Digital-7", 32, "bold"),
            fg='#00ff9d',
            bg='#1a1a2e'
        )
        self.label.pack()
        
        self.create_scale()
        self.draw_arrow()
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        
        self.animate_arrow()

    def create_scale(self):
        center_x, center_y = 250, 200
        radius = 180
        
        for i in range(0, 101, 10):
            freq = 88 + (i * 0.32)
            angle = math.radians(135 + i * 2.7)
            
            x1 = center_x + (radius - 20) * math.cos(angle)
            y1 = center_y + (radius - 20) * math.sin(angle)
            x2 = center_x + radius * math.cos(angle)
            y2 = center_y + radius * math.sin(angle)
            
            self.canvas.create_line(x1, y1, x2, y2, width=3, fill='#4cc9f0')
            
            if i % 20 == 0:
                label_x = center_x + (radius + 25) * math.cos(angle)
                label_y = center_y + (radius + 25) * math.sin(angle)
                self.canvas.create_text(
                    label_x, label_y,
                    text=f"{freq:.1f}",
                    font=("Arial", 12, "bold"),
                    fill='#f72585',
                    angle=math.degrees(angle) + 90
                )
        
        for i in range(0, 101, 2):
            angle = math.radians(135 + i * 2.7)
            length = 15 if i % 10 == 0 else 8
            x1 = center_x + (radius - length) * math.cos(angle)
            y1 = center_y + (radius - length) * math.sin(angle)
            x2 = center_x + radius * math.cos(angle)
            y2 = center_y + radius * math.sin(angle)
            
            color = '#7209b7' if i % 10 == 0 else '#3a0ca3'
            self.canvas.create_line(x1, y1, x2, y2, width=1, fill=color)
        
        self.canvas.create_oval(
            center_x - 10, center_y - 10,
            center_x + 10, center_y + 10,
            fill='#4361ee',
            outline='#4cc9f0',
            width=3
        )

    def calculate_angle(self, freq):
        return math.radians(135 + ((freq - 88) / 0.32) * 2.7)

    def draw_arrow(self):
        center_x, center_y = 250, 200
        angle = self.calculate_angle(self.current_freq)
        radius = 150
        
        tip_x = center_x + radius * math.cos(angle)
        tip_y = center_y + radius * math.sin(angle)
        
        side_angle1 = angle + math.radians(160)
        side_angle2 = angle - math.radians(160)
        
        side1_x = center_x + 40 * math.cos(side_angle1)
        side1_y = center_y + 40 * math.sin(side_angle1)
        side2_x = center_x + 40 * math.cos(side_angle2)
        side2_y = center_y + 40 * math.sin(side_angle2)
        
        self.canvas.delete("arrow")
        
        self.arrow_tip = self.canvas.create_polygon(
            tip_x, tip_y,
            side1_x, side1_y,
            side2_x, side2_y,
            fill='#f72585',
            outline='#ff006e',
            width=2,
            tags="arrow"
        )
        
        self.arrow_line = self.canvas.create_line(
            center_x, center_y,
            tip_x - (tip_x - center_x) * 0.3,
            tip_y - (tip_y - center_y) * 0.3,
            width=6,
            fill='#4361ee',
            tags="arrow"
        )

    def set_frequency(self, freq):
        self.target_freq = max(88.0, min(108.0, freq))
        self.start_animation()

    def on_click(self, event):
        self.set_frequency_from_click(event.x, event.y)

    def on_drag(self, event):
        self.set_frequency_from_click(event.x, event.y)

    def set_frequency_from_click(self, x, y):
        center_x, center_y = 250, 200
        dx = x - center_x
        dy = y - center_y
        angle = math.atan2(dy, dx)
        
        if angle < math.radians(135):
            angle += math.radians(360)
        
        if math.radians(135) <= angle <= math.radians(405):
            freq = 88 + ((angle - math.radians(135)) / math.radians(2.7)) * 0.32
            self.set_frequency(freq)

    def start_animation(self):
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
        self.animate_to_target()

    def animate_to_target(self):
        diff = self.target_freq - self.current_freq
        
        if abs(diff) < 0.01:
            self.current_freq = self.target_freq
        else:
            self.current_freq += diff * 0.15
        
        self.draw_arrow()
        self.label.config(text=f"{self.current_freq:.1f} МГц")
        
        if abs(self.current_freq - self.target_freq) > 0.01:
            self.animation_id = self.root.after(20, self.animate_to_target)

    def animate_arrow(self):
        self.draw_arrow()
        self.root.after(16, self.animate_arrow)

if __name__ == "__main__":
    root = tk.Tk()
    app = RadioTuner(root)
    root.mainloop()