import tkinter as tk
from tkinter import ttk

def update_color(*args):
    """Обновление цвета и текста при изменении TrackBar"""
    r = trackbar_r.get()
    g = trackbar_g.get()
    b = trackbar_b.get()
    
    color_hex = f'#{r:02x}{g:02x}{b:02x}'
    canvas.config(bg=color_hex)
    
    color_text.set(f'RGB({r}, {g}, {b})')

root = tk.Tk()
root.title("RGB Color Picker")
root.geometry("400x500")

trackbar_r = tk.IntVar(value=120)
trackbar_g = tk.IntVar(value=45)
trackbar_b = tk.IntVar(value=200)

color_text = tk.StringVar(value="RGB(120, 45, 200)")


canvas = tk.Canvas(root, width=350, height=150, bg='#7832c8')
canvas.pack(pady=20)

label_color = tk.Label(root, textvariable=color_text, font=('Arial', 14))
label_color.pack(pady=10)

frame_trackbars = tk.Frame(root)
frame_trackbars.pack(pady=20, padx=20)

label_r = tk.Label(frame_trackbars, text="Red:", fg='red', font=('Arial', 10))
label_r.grid(row=0, column=0, sticky='w', pady=5)
trackbar_r_slider = ttk.Scale(frame_trackbars, from_=0, to=255, 
                              variable=trackbar_r, command=update_color,
                              length=300)
trackbar_r_slider.grid(row=0, column=1, padx=10)
label_r_value = tk.Label(frame_trackbars, textvariable=trackbar_r, 
                         font=('Arial', 10), width=3)
label_r_value.grid(row=0, column=2)

label_g = tk.Label(frame_trackbars, text="Green:", fg='green', font=('Arial', 10))
label_g.grid(row=1, column=0, sticky='w', pady=5)
trackbar_g_slider = ttk.Scale(frame_trackbars, from_=0, to=255, 
                              variable=trackbar_g, command=update_color,
                              length=300)
trackbar_g_slider.grid(row=1, column=1, padx=10)
label_g_value = tk.Label(frame_trackbars, textvariable=trackbar_g, 
                         font=('Arial', 10), width=3)
label_g_value.grid(row=1, column=2)

label_b = tk.Label(frame_trackbars, text="Blue:", fg='blue', font=('Arial', 10))
label_b.grid(row=2, column=0, sticky='w', pady=5)
trackbar_b_slider = ttk.Scale(frame_trackbars, from_=0, to=255, 
                              variable=trackbar_b, command=update_color,
                              length=300)
trackbar_b_slider.grid(row=2, column=1, padx=10)
label_b_value = tk.Label(frame_trackbars, textvariable=trackbar_b, 
                         font=('Arial', 10), width=3)
label_b_value.grid(row=2, column=2)

info_label = tk.Label(root, text="Измените положение ползунков,\nчтобы изменить цвет", 
                      font=('Arial', 10), fg='gray')
info_label.pack(pady=20)

root.mainloop()