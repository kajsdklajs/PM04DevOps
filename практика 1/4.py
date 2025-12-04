import tkinter as tk
from tkinter import ttk

def update_progressbar(value):
    progress_var.set(float(value))

root = tk.Tk()
root.title("TrackBar → ProgressBar")
root.geometry("400x200")

progress_var = tk.DoubleVar()
progressbar = ttk.Progressbar(
    root,
    variable=progress_var,
    maximum=100,
    length=300,
    mode='determinate'
)
progressbar.pack(pady=20)

trackbar = ttk.Scale(
    root,
    from_=0,
    to=100,
    orient='horizontal',
    length=300,
    command=update_progressbar
)
trackbar.pack(pady=20)

value_label = ttk.Label(root, text="0%")
value_label.pack(pady=10)

def update_label(value):
    value_label.config(text=f"{float(value):.1f}%")

trackbar.configure(command=lambda v: [update_progressbar(v), update_label(v)])

root.mainloop()