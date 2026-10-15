import random


def funcion_objetivo(x, y):
    return x**2 + y**2


def ejecutar_pso():
    random.seed(42)  # Semilla requerida

    numero_particulas = 10
    dimensiones = 2
    iteraciones = 30

    inercia = 0.5
    coeficiente_cognitivo = 1.5
    coeficiente_social = 1.5

    valor_minimo, valor_maximo = -5.0, 5.0

    posiciones = []
    velocidades = []
    mejores_posiciones_personales = []
    mejores_valores_personales = []

    # Inicialización de partículas
    for _ in range(numero_particulas):
        posicion = [
            random.uniform(valor_minimo, valor_maximo),
            random.uniform(valor_minimo, valor_maximo)
        ]

        velocidad = [0.0, 0.0]  # Velocidades iniciales iguales a cero

        posiciones.append(posicion)
        velocidades.append(velocidad)
        mejores_posiciones_personales.append(list(posicion))
        valor = funcion_objetivo(posicion[0], posicion[1])
        mejores_valores_personales.append(valor)

    # Inicializar la mejor posición global
    indice_mejor = mejores_valores_personales.index(
        min(mejores_valores_personales)
    )

    mejor_posicion_global = list(
        mejores_posiciones_personales[indice_mejor]
    )

    mejor_valor_global = mejores_valores_personales[indice_mejor]

    historial_mejor_global = []

    for iteracion in range(iteraciones):
        historial_mejor_global.append(mejor_valor_global)

        for i in range(numero_particulas):
            for dimension in range(dimensiones):
                aleatorio_cognitivo = random.random()
                aleatorio_social = random.random()

                componente_cognitivo = (
                    coeficiente_cognitivo
                    * aleatorio_cognitivo
                    * (
                        mejores_posiciones_personales[i][dimension]
                        - posiciones[i][dimension]
                    )
                )

                componente_social = (
                    coeficiente_social
                    * aleatorio_social
                    * (
                        mejor_posicion_global[dimension]
                        - posiciones[i][dimension]
                    )
                )

                # Actualizar velocidad
                velocidades[i][dimension] = (
                    inercia * velocidades[i][dimension]
                    + componente_cognitivo
                    + componente_social
                )

                # Actualizar posición
                posiciones[i][dimension] += velocidades[i][dimension]

                # Ajustar los límites y poner la velocidad en cero
                if posiciones[i][dimension] < valor_minimo:
                    posiciones[i][dimension] = valor_minimo
                    velocidades[i][dimension] = 0.0

                elif posiciones[i][dimension] > valor_maximo:
                    posiciones[i][dimension] = valor_maximo
                    velocidades[i][dimension] = 0.0

            # Evaluar y actualizar la memoria personal
            valor_actual = funcion_objetivo(
                posiciones[i][0],
                posiciones[i][1]
            )

            if valor_actual < mejores_valores_personales[i]:
                mejores_valores_personales[i] = valor_actual
                mejores_posiciones_personales[i] = list(posiciones[i])

        # Actualizar la memoria global al final de la iteración
        valor_minimo_actual = min(mejores_valores_personales)

        if valor_minimo_actual < mejor_valor_global:
            indice_mejor = mejores_valores_personales.index(
                valor_minimo_actual
            )

            mejor_posicion_global = list(
                mejores_posiciones_personales[indice_mejor]
            )

            mejor_valor_global = valor_minimo_actual

    print('--- Resultados PSO ---')
    print(f'Mejor posición final: {mejor_posicion_global}')
    print(f'Valor de la función (aptitud): {mejor_valor_global}')
    print(
        'Historial de la mejor aptitud global: '
        f'{historial_mejor_global}'
    )


ejecutar_pso()