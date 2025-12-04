import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Set up the time base for simulation
t = np.linspace(0, 0.1, 1000)  # 100 milliseconds
angular_freq_0 = 2 * np.pi * 50  # Initial frequency of 50 Hz

# Create the figure and axis for plotting
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.3)  # Make room for sliders at the bottom

# Calculate initial circuit parameters (Series RLC)
# Source Voltage: V = V0 * sin(omega * t)
source_voltage = 5 * np.sin(angular_freq_0 * t)

# Component values (Initial state)
R0 = 100.0  # Resistance in Ohms
L0 = 0.1    # Inductance in Henries
C0 = 100e-6 # Capacitance in Farads (100 uF)

# Calculate impedance and current
Z0 = np.sqrt(R0**2 + (angular_freq_0 * L0 - 1/(angular_freq_0 * C0))**2)
current_0 = source_voltage / Z0

# Plot the initial signals
voltage_line, = plt.plot(t * 1000, source_voltage, lw=2, color='red', label='Source Voltage (V)')
current_line, = plt.plot(t * 1000, current_0 * 1000, lw=2, color='blue', label='Current (mA)')

plt.xlabel('Time (milliseconds)')
plt.ylabel('Amplitude')
plt.title('AC Circuit Simulation: RLC Series Circuit')
plt.legend()
plt.grid(True)

# Create sliders for interactive component value adjustment
ax_resistor = plt.axes([0.2, 0.2, 0.6, 0.03])
ax_inductor = plt.axes([0.2, 0.15, 0.6, 0.03])
ax_capacitor = plt.axes([0.2, 0.1, 0.6, 0.03])

slider_R = Slider(ax_resistor, 'Resistance (Ω)', 10.0, 500.0, valinit=R0)
slider_L = Slider(ax_inductor, 'Inductance (H)', 0.01, 1.0, valinit=L0)
slider_C = Slider(ax_capacitor, 'Capacitance (uF)', 1.0, 500.0, valinit=C0*1e6)

# Update function called when slider values change
def update(val):
    R = slider_R.val
    L = slider_L.val
    C = slider_C.val * 1e-6  # Convert from uF to F
    
    # Recalculate impedance and current with new values
    Z = np.sqrt(R**2 + (angular_freq_0 * L - 1/(angular_freq_0 * C))**2)
    current = source_voltage / Z
    
    # Update the current data on the plot
    current_line.set_ydata(current * 1000)  # Convert to mA for plotting
    fig.canvas.draw_idle()

# Register the update function with each slider
slider_R.on_changed(update)
slider_L.on_changed(update)
slider_C.on_changed(update)

# Add a reset button
reset_ax = plt.axes([0.8, 0.025, 0.1, 0.04])
reset_button = Button(reset_ax, 'Reset', hovercolor='0.975')

def reset(event):
    slider_R.reset()
    slider_L.reset()
    slider_C.reset()

reset_button.on_clicked(reset)

plt.show()