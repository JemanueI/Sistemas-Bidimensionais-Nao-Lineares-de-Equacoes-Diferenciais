import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# --- Parâmetro de Gamma ---
# Escolhemos um valor para garantir que (0.15, 0) seja um Foco Estável:
# Requer: 0 < GAMMA < sqrt(1.11) ≈ 1.054
GAMMA = 0.5


def sistema_vetorial(t, Y, gamma):
    """
    Define o sistema de equações diferenciais:
    x' = -y
    y' = -gamma*y - x(x - 0.15)(x - 2)

    Nota: solve_ivp espera que a função retorne [dY/dt] e tenha a assinatura (t, Y, ...)
    """
    x, y = Y
    dxdt = -y
    dydt = -gamma * y - x * (x - 0.15) * (x - 2)
    return [dxdt, dydt]


def plotar_retrato_de_fase(gamma, filename='retrato_de_fase_v2.png', title='Retrato de Fase (Sistema Não Linear)'):
    """
    Calcula e plota o retrato de fase usando solve_ivp.
    """

    # 1. Definição do Grid e Campos de Vetores
    x_range = np.linspace(-0.5, 2.5, 40)
    y_range = np.linspace(-1.5, 1.5, 40)
    X, Y = np.meshgrid(x_range, y_range)

    # Prepara a entrada para o campo de vetores (reshape para a função)
    Y_flat = np.vstack([X.ravel(), Y.ravel()])

    # Calcula o campo de vetores (o tempo t=0 é irrelevante para sistemas autônomos)
    DY_flat = sistema_vetorial(0, Y_flat, gamma)

    dX = DY_flat[0].reshape(X.shape)
    dY = DY_flat[1].reshape(Y.shape)

    # Normaliza os vetores
    M = np.hypot(dX, dY)
    M_safe = np.where(M == 0, 1.0, M)
    dX_norm = dX / M_safe
    dY_norm = dY / M_safe

    # 2. Plotagem
    plt.figure(figsize=(10, 7))
    plt.quiver(X, Y, dX_norm, dY_norm, M, cmap='viridis', pivot='mid', linewidth=0.5, headwidth=5, headlength=7)

    # 3. Solução de Trajetórias usando solve_ivp

    # Define o tempo de integração
    t_span_fwd = [0, 20]  # Integração para t > 0
    t_span_bwd = [0, -20]  # Integração para t < 0

    # Pontos iniciais para traçar as trajetórias
    initial_points = [
        # Próximo ao Foco Estável P2 (0.15, 0)
        [0.5, 1.0], [1.0, 0.5], [0.5, -0.5],
        # Próximo ao Sela P1 (0, 0)
        [-0.1, 0.1], [0.1, -0.1],
        # Próximo ao Sela P3 (2, 0)
        [2.1, 0.1], [1.9, -0.1], [2.1, 1.0]
    ]

    # Configurações do solver (aumenta a precisão para tentar evitar warnings)
    solver_options = {
        'method': 'RK45',  # Um bom método de uso geral
        'args': (gamma,),
        'rtol': 1e-8,  # Tolerância relativa
        'atol': 1e-8,  # Tolerância absoluta
        'max_step': 0.1  # Limita o tamanho máximo do passo
    }

    for y0 in initial_points:
        # Integração para t > 0 (Aproximação/Trajetória)
        sol_fwd = solve_ivp(sistema_vetorial, t_span_fwd, y0, **solver_options, dense_output=True)
        plt.plot(sol_fwd.y[0, :], sol_fwd.y[1, :], 'r-', alpha=0.5, linewidth=1)

        # Integração para t < 0 (Recuo, útil para mostrar o comportamento de sela)
        # O t_span é [0, -20], forçando a integração para trás no tempo.
        sol_bwd = solve_ivp(sistema_vetorial, t_span_bwd, y0, **solver_options, dense_output=True)
        plt.plot(sol_bwd.y[0, :], sol_bwd.y[1, :], 'b--', alpha=0.3, linewidth=1)  # Linhas azuis tracejadas

    # 4. Plotagem dos Pontos Críticos
    pontos_criticos = [(0, 0), (0.15, 0), (2, 0)]
    labels = ['P1 (Sela)', 'P2 (Foco Estável)', 'P3 (Sela)']
    colors = ['black', 'red', 'black']

    for i, (x_eq, y_eq) in enumerate(pontos_criticos):
        plt.plot(x_eq, y_eq, 'o', color=colors[i], markersize=8, label=labels[i])

    plt.title(f'{title}\n($\\gamma = {gamma}$)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.axhline(0, color='gray', linestyle='-')
    plt.axvline(0, color='gray', linestyle='-')
    plt.legend()
    # plt.axis('equal') # Removendo 'equal' para focar na região de interesse

    # Salva o gráfico
    plt.savefig(filename)
    print(f"Retrato de Fase salvo em: {filename}")


# --- Execução da Função ---
plotar_retrato_de_fase(GAMMA)