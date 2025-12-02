import numpy as np
import matplotlib.pyplot as plt

# --- 1. Definir as Constantes do Sistema ---
# Valores de exemplo que garantem todas as constantes positivas e resultam em P2 como Ponto de Sela
a = 1.0
sigma = 0.5
alpha = 0.8
c = 0.5
gamma = 0.7

# Verificação do tipo de P2: a*gamma (0.7) > c*sigma (0.25) -> P2 é Ponto de Sela

# --- 2. Definir o Sistema de Equações Diferenciais ---
def lotka_volterra_competition(x, y, a, sigma, alpha, c, gamma):
    """
    Calcula as derivadas x' e y' para o sistema:
    x' = x(a - sigma x - alpha y)
    y' = y(-c + gamma x)
    """
    dx_dt = x * (a - sigma * x - alpha * y)
    dy_dt = y * (-c + gamma * x)
    return dx_dt, dy_dt

# --- 3. Definir a Área de Plotagem (Grid) ---
x_max = 3.5
y_max = 3.5
points = 30 # Número de pontos para o campo de vetores
x = np.linspace(0, x_max, points)
y = np.linspace(0, y_max, points)

X, Y = np.meshgrid(x, y)

# Calcular os vetores de direção (U = dx/dt, V = dy/dt)
U, V = lotka_volterra_competition(X, Y, a, sigma, alpha, c, gamma)

# Normalizar os vetores para o campo de vetores ter um tamanho uniforme
M = np.sqrt(U**2 + V**2)
M[M == 0] = 1.0 # Evitar divisão por zero nos pontos de equilíbrio
U = U / M
V = V / M

# --- 4. Encontrar e Marcar os Pontos de Equilíbrio ---
P1 = (0, 0)
P2 = (a / sigma, 0)
# Para referência, o P3 interior (onde o sistema muda de comportamento)
x_star = c / gamma
y_star = (a - sigma * x_star) / alpha
P3 = (x_star, y_star)

# --- 5. Gerar o Gráfico (Retrato de Fase) ---
plt.figure(figsize=(10, 8))

# B. Desenhar as Trajetórias (Stream Plot)
plt.streamplot(X, Y, U, V, density=1.5, linewidth=1, color='blue', arrowsize=1.5)

# C. Marcar os Pontos de Equilíbrio nos eixos
plt.plot(P1[0], P1[1], 'ro', markersize=8, label=f'$P_1 = (0, 0)$ (Sela)')
plt.plot(P2[0], P2[1], 'go', markersize=8, label=f'$P_2 = ({P2[0]:.2f}, 0)$ (Sela)')

# Marcar P3 se estiver no primeiro quadrante (x>0, y>0)
if P3[0] > 0 and P3[1] > 0:
    plt.plot(P3[0], P3[1], 'ko', markersize=8, markerfacecolor='yellow', label=f'$P_3 = ({P3[0]:.2f}, {P3[1]:.2f})$ (Interior)')

# D. Configurações Finais do Gráfico
# CORREÇÃO CRÍTICA: Uso de rf-string para evitar ParseException do Mathtext
plt.title(rf'Retrato de Fase do Sistema de Competição/Predação ($\alpha = {alpha}, \sigma = {sigma}, \gamma = {gamma}$)')
plt.xlabel('$x$ (População 1)')
plt.ylabel('$y$ (População 2)')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.xlim(0, x_max)
plt.ylim(0, y_max)

plt.savefig('retrato_de_fase.png')
