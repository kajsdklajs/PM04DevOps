import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def simple_metal_model():
    """Простая модель металла"""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(-1, 1)
    
    # Начальные позиции 20 электронов
    electrons = np.random.rand(20, 2) * [9, 1.8] + [0.5, -0.9]
    scatter = ax.scatter(electrons[:, 0], electrons[:, 1], c='blue', s=30)
    
    ax.set_title('Движение электронов в металле')
    ax.grid(True, alpha=0.3)
    
    def update(frame):
        # Простое движение с дрейфом
        electrons[:, 0] += 0.1 + 0.05 * np.random.randn(20)
        
        # Возврат через границу
        mask = electrons[:, 0] > 10
        electrons[mask, 0] = 0
        
        scatter.set_offsets(electrons)
        return scatter,
    
    anim = FuncAnimation(fig, update, frames=100, interval=100, blit=True)
    plt.show()

def simple_electrolyte_model():
    """Простая модель электролита"""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(-1, 1)
    
    # Катионы и анионы
    cations = np.random.rand(10, 2) * [8, 1.8] + [1, -0.9]
    anions = np.random.rand(10, 2) * [8, 1.8] + [1, -0.9]
    
    cations_scatter = ax.scatter(cations[:, 0], cations[:, 1], c='red', s=40, label='Катионы (+)')
    anions_scatter = ax.scatter(anions[:, 0], anions[:, 1], c='blue', s=40, label='Анионы (-)')
    
    ax.set_title('Движение ионов в электролите')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    def update(frame):
        # Катионы движутся к катоду, анионы - к аноду
        cations[:, 0] += 0.08 + 0.03 * np.random.randn(10)
        anions[:, 0] -= 0.08 + 0.03 * np.random.randn(10)
        
        # Граничные условия
        cations[cations[:, 0] > 9.5, 0] = 1
        anions[anions[:, 0] < 0.5, 0] = 9
        
        cations_scatter.set_offsets(cations)
        anions_scatter.set_offsets(anions)
        return cations_scatter, anions_scatter
    
    anim = FuncAnimation(fig, update, frames=100, interval=100, blit=True)
    plt.show()

# Запуск простых моделей
print("Запуск простой модели металла...")
simple_metal_model()

print("Запуск простой модели электролита...")
simple_electrolyte_model()