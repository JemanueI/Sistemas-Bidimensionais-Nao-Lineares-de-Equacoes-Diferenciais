import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# 1. Definir o Sistema de EDOs
def system_b(Z, t):
    x, y = Z
    dxdt = x * (1 - x + 0.5 * y)
    dydt = y * (2.5 - 1.5 * y + 0.25 * x)
    return [dxdt, dydt]


# 2. Configuração do Plot
fig, ax = plt.subplots(figsize=(8, 8))
x_max, y_max = 3.5, 3.5
ax.set_title('Retrato de Fase - Sistema (b): Nó Atrator em (2, 2)')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_xlim(0, x_max)
ax.set_ylim(0, y_max)
ax.grid(True, linestyle='--')

# 3. Campo de Vetores (usando quiver)
n_points = 25
X, Y = np.meshgrid(np.linspace(0.01, x_max, n_points), np.linspace(0.01, y_max, n_points))
dX, dY = system_b([X, Y], 0)
M = np.hypot(dX, dY)
M[M == 0] = 1.0
ax.quiver(X, Y, dX / M, dY / M, color='blue', alpha=0.6, headwidth=5, scale_units='xy', scale=1.5, minlength=0.1)

# 4. Pontos de Equilíbrio
equilibria_b = [
    (0, 0, 'Nó Repulsor'),
    (0, 5 / 3, 'Sela'),
    (1, 0, 'Sela'),
    (2, 2, 'Nó Atrator')
]
for x_eq, y_eq, label in equilibria_b:
    ax.plot(x_eq, y_eq, 'ko', markersize=7, label='Ponto de Equilíbrio')
    ax.annotate(f'({round(x_eq, 2)}, {round(y_eq, 2)})\n{label}', (x_eq + 0.05, y_eq + 0.05), fontsize=9)

# 5. Trajetórias Amostrais (usando odeint)
t_span = np.linspace(0, 15, 500)
conditions = [(0.1, 0.1), (0.1, 3.0), (3.0, 0.1), (1.0, 1.0), (3.0, 3.0), (2.5, 1.5)]
for x0, y0 in conditions:
    sol = odeint(system_b, [x0, y0], t_span)

    # Filtrar valores para manter dentro do limite de plotagem
    sol[sol < 0] = np.nan
    sol[sol > x_max + 0.5] = np.nan
    ax.plot(sol[:, 0], sol[:, 1], 'r-', linewidth=1.5, alpha=0.8)

# 6. Mostrar o gráfico
plt.savefig('retrato_de_fase_sistema_b.png')