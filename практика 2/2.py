import tkinter as tk

class SwitchButton:
    def __init__(self, root):
        self.root = root
        self.root.title("Семенов Павел")
        self.root.geometry("400x300")
        self.root.configure(bg='#2c3e50')
        
        self.state = False
        
        self.canvas = tk.Canvas(
            root, 
            width=200, 
            height=100, 
            bg='#2c3e50',
            highlightthickness=0
        )
        self.canvas.pack(expand=True)
        
        self.draw_switch()
        
        self.canvas.bind("<Button-1>", self.toggle_switch)
        
        self.label = tk.Label(
            root, 
            text="ВЫКЛ", 
            font=("Arial", 18, "bold"),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        self.label.pack(pady=20)
        
        self.animate()

    def draw_switch(self):
        self.canvas.delete("all")
        
        bg_color = '#7f8c8d' if not self.state else '#2ecc71'
        
        self.canvas.create_rectangle(
            10, 10, 190, 90,
            fill=bg_color,
            outline='#34495e',
            width=3,
            tags="bg"
        )
        
        circle_x = 50 if not self.state else 150
        
        self.canvas.create_oval(
            circle_x-40, 15,
            circle_x+40, 85,
            fill='#ecf0f1',
            outline='#bdc3c7',
            width=2,
            tags="circle"
        )
        
        inner_color = '#e74c3c' if not self.state else '#27ae60'
        self.canvas.create_oval(
            circle_x-30, 25,
            circle_x+30, 75,
            fill=inner_color,
            outline='',
            tags="inner"
        )

    def toggle_switch(self, event):
        self.state = not self.state
        
        for i in range(10):
            self.root.after(i*20, self.animate_step, i)
        
        self.label.config(text="ВКЛ" if self.state else "ВЫКЛ")
        self.label.config(fg='#27ae60' if self.state else '#e74c3c')

    def animate_step(self, step):
        progress = step / 9
        
        if not self.state:
            progress = 1 - progress
        
        circle_x = 50 + (progress * 100)
        
        self.canvas.delete("circle")
        self.canvas.delete("inner")
        
        self.canvas.create_oval(
            circle_x-40, 15,
            circle_x+40, 85,
            fill='#ecf0f1',
            outline='#bdc3c7',
            width=2,
            tags="circle"
        )
        
        inner_color = self.interpolate_color('#e74c3c', '#27ae60', progress)
        bg_color = self.interpolate_color('#7f8c8d', '#2ecc71', progress)
        
        self.canvas.create_oval(
            circle_x-30, 25,
            circle_x+30, 75,
            fill=inner_color,
            outline='',
            tags="inner"
        )
        
        self.canvas.itemconfig("bg", fill=bg_color)

    def interpolate_color(self, color1, color2, t):
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        
        return f'#{r:02x}{g:02x}{b:02x}'

    def animate(self):
        self.root.after(100, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = SwitchButton(root)
    root.mainloop()