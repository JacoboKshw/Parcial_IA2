import random

def aptitud(cromosoma):
    valor = int(cromosoma, 2)
    return valor**2


def decodificar(cromosoma):
    return int(cromosoma, 2)


def seleccion_ruleta(poblacion, aptitudes):
    aptitud_total = sum(aptitudes)

    if aptitud_total == 0:
        return random.choice(poblacion)

    seleccion = random.uniform(0, aptitud_total)
    acumulado = 0

    for individuo, aptitud_individuo in zip(poblacion, aptitudes):
        acumulado += aptitud_individuo

        if acumulado >= seleccion:
            return individuo

    return poblacion[-1]


def cruce(padre1, padre2, probabilidad_cruce=0.8):
    if random.random() < probabilidad_cruce and len(padre1) > 1:
        punto_cruce = random.randint(1, len(padre1) - 1)

        hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
        hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]

        return hijo1, hijo2

    return padre1, padre2


def mutacion(cromosoma, probabilidad_mutacion=0.05):
    cromosoma_mutado = list(cromosoma)

    for posicion in range(len(cromosoma_mutado)):
        if random.random() < probabilidad_mutacion:
            cromosoma_mutado[posicion] = (
                '1' if cromosoma_mutado[posicion] == '0' else '0'
            )

    return ''.join(cromosoma_mutado)


def algoritmo_genetico():
    random.seed(42)  # Semilla requerida

    poblacion = ['00101', '01100', '10010', '11001']
    numero_generaciones = 20
    historial_mejor_aptitud = []

    for generacion in range(numero_generaciones):
        aptitudes = [aptitud(individuo) for individuo in poblacion]

        # Elitismo: conservar el mejor individuo
        indice_mejor = aptitudes.index(max(aptitudes))
        mejor_individuo = poblacion[indice_mejor]
        mejor_aptitud = aptitudes[indice_mejor]

        historial_mejor_aptitud.append(mejor_aptitud)

        nueva_poblacion = [mejor_individuo]

        while len(nueva_poblacion) < len(poblacion):
            padre1 = seleccion_ruleta(poblacion, aptitudes)
            padre2 = seleccion_ruleta(poblacion, aptitudes)

            hijo1, hijo2 = cruce(
                padre1, padre2, probabilidad_cruce=0.8
            )

            hijo1 = mutacion(hijo1, probabilidad_mutacion=0.05)
            hijo2 = mutacion(hijo2, probabilidad_mutacion=0.05)

            nueva_poblacion.append(hijo1)

            if len(nueva_poblacion) < len(poblacion):
                nueva_poblacion.append(hijo2)

        poblacion = nueva_poblacion

    # Evaluación final
    aptitudes_finales = [
        aptitud(individuo) for individuo in poblacion
    ]

    indice_mejor = aptitudes_finales.index(max(aptitudes_finales))
    mejor_cromosoma = poblacion[indice_mejor]
    mejor_valor = decodificar(mejor_cromosoma)
    mejor_aptitud_final = aptitudes_finales[indice_mejor]

    print('--- RESULTADOS DEL ALGORITMO GENÉTICO ---')
    print(f'Mejor cromosoma final: {mejor_cromosoma}')
    print(f'Valor de x: {mejor_valor}')
    print(f'Aptitud: {mejor_aptitud_final}')
    print(
        'Historial de la mejor aptitud por generación: '
        f'{historial_mejor_aptitud}'
    )

algoritmo_genetico()