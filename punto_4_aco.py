"""
Punto 4.B - ACO simplificado: elección entre tres rutas completas A -> Z.

Cada ruta r tiene una única feromona tau_r (inicialmente 1).
Probabilidad de elegir la ruta r:
    p_r = (tau_r^alpha * (1/L_r)^beta) / sum_s (tau_s^alpha * (1/L_s)^beta)

En cada iteración:
    1. Se calculan las probabilidades con las feromonas actuales.
    2. Las hormigas eligen ruta con esas mismas probabilidades.
    3. Se evapora la feromona de todas las rutas: tau <- (1 - rho) * tau.
    4. Cada hormiga deposita Q / L_r en la ruta que eligió.
"""

import random

import matplotlib
matplotlib.use("Agg")  # backend sin ventana: guarda la figura directamente
import matplotlib.pyplot as plt

# ----------------------------- Parámetros ----------------------------------
RUTAS = {"A-B-Z": 6, "A-C-Z": 8, "A-D-Z": 10}  # nombre -> longitud total L
N_HORMIGAS = 10
N_ITERACIONES = 20
ALPHA = 1
BETA = 2
RHO = 0.2
Q = 10
TAU_INICIAL = 1.0
SEMILLA = 42


# ------------------------------- Funciones ---------------------------------
def calcular_probabilidades(tau, rutas, alpha, beta):
    """Devuelve {ruta: probabilidad} normalizando tau^alpha * (1/L)^beta."""
    pesos = {r: (tau[r] ** alpha) * ((1.0 / L) ** beta) for r, L in rutas.items()}
    total = sum(pesos.values())
    return {r: w / total for r, w in pesos.items()}


def elegir_rutas(probs, n_hormigas):
    """Cada hormiga elige una ruta con las probabilidades dadas."""
    nombres = list(probs.keys())
    pesos = [probs[r] for r in nombres]
    return random.choices(nombres, weights=pesos, k=n_hormigas)


def actualizar_feromonas(tau, elecciones, rutas, rho, q):
    """Evapora todas las rutas y luego suma el depósito Q/L de cada hormiga."""
    for r in tau:                       # 3. evaporación
        tau[r] *= (1.0 - rho)
    for r in elecciones:                # 4. depósito por hormiga
        tau[r] += q / rutas[r]


def ejecutar_aco():
    """Corre el algoritmo completo y devuelve frecuencias, tau final e historial."""
    random.seed(SEMILLA)
    tau = {r: TAU_INICIAL for r in RUTAS}
    frecuencias = {r: 0 for r in RUTAS}
    historial = {r: [tau[r]] for r in RUTAS}  # incluye iteración 0 (estado inicial)

    for it in range(1, N_ITERACIONES + 1):
        probs = calcular_probabilidades(tau, RUTAS, ALPHA, BETA)   # 1.
        elecciones = elegir_rutas(probs, N_HORMIGAS)               # 2.
        for r in elecciones:
            frecuencias[r] += 1
        actualizar_feromonas(tau, elecciones, RUTAS, RHO, Q)       # 3. y 4.
        for r in RUTAS:
            historial[r].append(tau[r])

    return frecuencias, tau, historial


def graficar(historial, archivo="aco_feromonas.png"):
    """Grafica la evolución de tau de cada ruta y guarda la imagen."""
    plt.figure(figsize=(8, 5))
    for r, valores in historial.items():
        plt.plot(range(len(valores)), valores, marker="o", markersize=4,
                 label=f"{r} (L={RUTAS[r]})")
    plt.xlabel("Iteración")
    plt.ylabel("Feromona τ")
    plt.title("Evolución de la feromona por ruta (ACO)")
    plt.xticks(range(0, N_ITERACIONES + 1, 2))
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(archivo, dpi=150)
    plt.close()


# --------------------------------- Main ------------------------------------
if __name__ == "__main__":
    frecuencias, tau_final, historial = ejecutar_aco()
    total = N_HORMIGAS * N_ITERACIONES

    print("Frecuencias de elección (total = %d elecciones):" % total)
    for r, f in frecuencias.items():
        print(f"  {r}: {f:>3}  ({f / total:.1%})")

    print("\nFeromonas finales:")
    for r, t in tau_final.items():
        print(f"  {r}: {t:.4f}")

    mejor_observada = max(frecuencias, key=frecuencias.get)
    print(f"\nMejor ruta observada (más elegida): {mejor_observada} "
          f"(L = {RUTAS[mejor_observada]})")
    print(f"Ruta más corta del problema: {min(RUTAS, key=RUTAS.get)} "
          f"(L = {min(RUTAS.values())})")

    graficar(historial)
    print("\nGráfica guardada como 'aco_feromonas.png'")
