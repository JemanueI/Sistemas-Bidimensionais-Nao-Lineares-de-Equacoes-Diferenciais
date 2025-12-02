import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#Definindo o sistema de EDO's
def system_a(Z, t):
    x, y = Z
    dxdt = x * (1 - x - y)
    dydt = y * (1.5 - y - x)
    return [dxdt, dydt]

#Configurando o plot
fig, ax = plt.subplots(figsize=(8, 8))
x_max, y_max = 2.0, 2.0
ax.set_title('Retrato de Fase - Sistema (a): Nó Atrator em (0, 1.5)')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_xlim(0, x_max)
ax.set_ylim(0, y_max)
ax.grid(True, linestyle='--')

#Para o campo de vetores
n_points = 20
X, Y = np.meshgrid(np.linspace(0.01, x_max, n_points), np.linspace(0.01, y_max, n_points))
dX, dY = system_a([X, Y], 0)
M = np.hypot(dX, dY)
M[M == 0] = 1.0
ax.quiver(X, Y, dX/M, dY/M, color='blue', alpha=0.6, headwidth=5, scale_units='xy', scale=1.5, minlength=0.1)

#Dos pontos de equilibrio
equilibria_a = [
    (0, 0, 'Nó Repulsor'),
    (0, 1.5, 'Nó Atrator'),
    (1, 0, 'Ponto de Sela')
]
for x_eq, y_eq, label in equilibria_a:
    ax.plot(x_eq, y_eq, 'ko', markersize=7, label='Ponto de Equilíbrio')
    ax.annotate(f'({x_eq}, {y_eq})\n{label}', (x_eq + 0.05, y_eq + 0.05), fontsize=9)

#Aplicando condições no sistema
t = np.linspace(0, 10, 500)
conditions = [(0.1, 0.1), (0.1, 1.8), (1.5, 0.1), (0.5, 0.5), (0.8, 1.2)]
for x0, y0 in conditions:
    sol = odeint(system_a, [x0, y0], t)
    #filtrando para um limite de plotagem
    sol[sol < 0] = np.nan
    sol[sol > x_max + 0.5] = np.nan
    ax.plot(sol[:, 0], sol[:, 1], 'r-', linewidth=1.5, alpha=0.8)

#Salvar o grafico em .png
plt.savefig('retrato_de_fase_sistema_a.png')