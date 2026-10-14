VALORES = [1, 4, 7, 5, 3, 6, 9, 8, 5]


def ascenso_colinas(valores, inicio):
    """Devuelve el estado final y la trayectoria."""
    x = inicio
    trayectoria = [x]
    while True:
        vecinos = [v for v in (x - 1, x + 1) if 0 <= v < len(valores)]
        mejor = max(vecinos, key=lambda v: valores[v])
        if valores[mejor] > valores[x]:  # solo mejora estricta
            x = mejor
            trayectoria.append(x)
        else:
            return x, trayectoria


if __name__ == "__main__":
    print(f"{'Inicio':<7}{'Trayectoria':<16}{'Final':<7}{'f(final)':<8}")
    global_max = max(VALORES)
    aciertos = 0
    for inicio in range(len(VALORES)):
        final, tray = ascenso_colinas(VALORES, inicio)
        print(f"{inicio:<7}{'->'.join(map(str, tray)):<16}{final:<7}{VALORES[final]:<8}")
        aciertos += VALORES[final] == global_max
    n = len(VALORES)
    print(f"\nLlegan al máximo global: {aciertos}/{n} = {aciertos / n:.1%}")
