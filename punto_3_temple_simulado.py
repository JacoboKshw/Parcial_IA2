import math
import random


def energia(x):
    return x ** 2


def casos_manuales():
    print("Casos A, B, C")
    casos = [("A", 3, 2, 5, 0.70), ("B", 2, 3, 5, 0.30), ("C", 2, 3, 1, 0.30)]
    for nombre, act, cand, T, u in casos:
        dE = energia(cand) - energia(act)
        p = 1.0 if dE <= 0 else math.exp(-dE / T)
        decision = "ACEPTA" if (dE <= 0 or u < p) else "RECHAZA"
        print(f"  {nombre}: dE={dE:+d}  P={p:.4f}  u={u:.2f}  -> {decision}")
    print()


def temple_simulado(x0=5, T0=10.0, alfa=0.90, iteraciones=100, semilla=42):
    random.seed(semilla)
    x, T = x0, T0
    mejor = x
    hist_T, hist_E = [], []
    for _ in range(iteraciones):
        vecinos = [v for v in (x - 1, x + 1) if -5 <= v <= 5]
        cand = random.choice(vecinos)
        dE = energia(cand) - energia(x)
        if dE <= 0 or random.random() < math.exp(-dE / T):
            x = cand
        if energia(x) < energia(mejor):
            mejor = x
        hist_T.append(T)
        hist_E.append(energia(x))
        T *= alfa
    return mejor, hist_T, hist_E


if __name__ == "__main__":
    casos_manuales()
    mejor, hist_T, hist_E = temple_simulado()
    print(f"Mejor solución: x = {mejor}")
    print(f"Energía mínima: E = {energia(mejor)}")
    print("Historial de temperatura:", [round(t, 4) for t in hist_T])
    print("Historial de energía:", hist_E)
