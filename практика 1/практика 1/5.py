import tkinter as tk
from tkinter import ttk

class VerticalProgressBar:
    def __init__(self, root):
        self.root = root
        self.root.title("Vertical Volume Control")
        self.root.geometry("200x400")

        self.progress = ttk.Progressbar(
            root,
            orient="vertical",
            length=300,
            mode="determinate"
        )
        self.progress.pack(pady=20, padx=20)

        self.progress.config(maximum=100)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="+", command=self.increase_volume, 
                 width=5, height=2).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="-", command=self.decrease_volume,
                 width=5, height=2).pack(side=tk.LEFT, padx=5)

        self.label = tk.Label(root, text="Volume: 0%", font=("Arial", 12))
        self.label.pack(pady=10)

        self.scale = tk.Scale(
            root,
            from_=100,
            to=0,
            orient="vertical",
            length=200,
            command=self.update_from_scale
        )
        self.scale.pack(pady=10)

        self.volume = 0
        
    def increase_volume(self):
        if self.volume < 100:
            self.volume += 10
            self.update_display()
    
    def decrease_volume(self):
        if self.volume > 0:
            self.volume -= 10
            self.update_display()
    
    def update_from_scale(self, value):
        self.volume = 100 - int(value) 
        self.update_display()
    
    def update_display(self):
        self.progress['value'] = self.volume
        self.label.config(text=f"Volume: {self.volume}%")
        self.scale.set(100 - self.volume) 

if __name__ == "__main__":
    root = tk.Tk()
    app = VerticalProgressBar(root)
    root.mainloop()