import numpy as np
import matplotlib.pyplot as plt


def fase_a():
    # 1. Definição do sistema
    def sistema_a(X, t):
        x, y = X
        dxdt = x ** 2
        dydt = y
        return [dxdt, dydt]

    # 2. Definição do Grid
    # Região de interesse (vizinha ao ponto fixo (0, 0))
    x_min, x_max = -2, 2
    y_min, y_max = -2, 2

    X, Y = np.meshgrid(np.linspace(x_min, x_max, 20),
                       np.linspace(y_min, y_max, 20))

    # Cálculo dos vetores U (dx/dt) e V (dy/dt) no grid
    U = X ** 2
    V = Y

    # 3. Plotagem
    plt.figure(figsize=(7, 7))

    # Desenho do campo de vetores
    # density: ajusta a densidade das linhas de fluxo.
    # color: 'blue' para as linhas de fluxo.
    plt.streamplot(X, Y, U, V, density=1.5, color='blue', linewidth=1, arrowsize=1.5)

    # Adicionar o ponto de equilíbrio
    plt.plot(0, 0, 'ro', label='Ponto de Equilíbrio (0, 0)')

    # Configurações do gráfico
    plt.title(r'Retrato de Fase: $x\' = x^2, y\' = y$')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()

    # Salvar a figura conforme solicitado
    plt.savefig('retrato_de_fase_A.png')
    print("O retrato de fase para o sistema (a) foi salvo como 'retrato_de_fase_A.png'")


# Executar a função para o sistema (a)
fase_a()
