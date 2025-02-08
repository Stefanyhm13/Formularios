# Importar funciones necesarias desde Extra
from backend.Extra import obtener_respuestas_procesadas3

# Definir las dimensiones del cuestionario extralaboral
DIMENSIONES = {
    "Tiempo fuera del trabajo": [14, 15, 16, 17],
    "Relaciones familiares": [22, 25, 27],
    "Comunicación y relaciones interpersonales": [18, 19, 20, 21, 23],
    "Situación económica del grupo familiar": [29, 30, 31],
    "Características de la vivienda y de su entorno": [5, 6, 7, 8, 9, 10, 11, 12, 13],
    "Influencia del entorno extralaboral sobre el trabajo": [24, 26, 28],
    "Desplazamiento vivienda trabajo vivienda": [1, 2, 3, 4]
}

# Factores de transformación para dimensiones y cuestionario total
FACTORES_DIMENSIONES = {
    "Tiempo fuera del trabajo": 16,
    "Relaciones familiares": 12,
    "Comunicación y relaciones interpersonales": 20,
    "Situación económica del grupo familiar": 12,
    "Características de la vivienda y de su entorno": 36,
    "Influencia del entorno extralaboral sobre el trabajo": 12,
    "Desplazamiento vivienda trabajo vivienda": 16
}

FACTOR_TOTAL_CUESTIONARIO = 124

# Clasificación de riesgo por dimensiones y cuestionario total
CLASIFICACION_DIMENSIONES = {
    "Tiempo fuera del trabajo": [(0.0, 6.3, "Sin riesgo o riesgo despreciable"),
                                 (6.4, 25.0, "Riesgo bajo"),
                                 (25.1, 37.5, "Riesgo medio"),
                                 (37.6, 50.0, "Riesgo alto"),
                                 (50.1, 100, "Riesgo muy alto")],
    "Relaciones familiares": [(0.0, 8.3, "Sin riesgo o riesgo despreciable"),
                              (8.4, 25.0, "Riesgo bajo"),
                              (25.1, 33.3, "Riesgo medio"),
                              (33.4, 50.0, "Riesgo alto"),
                              (50.1, 100, "Riesgo muy alto")],
    "Comunicación y relaciones interpersonales": [(0.0, 0.9, "Sin riesgo o riesgo despreciable"),
                                                  (1.0, 10.0, "Riesgo bajo"),
                                                  (10.1, 20.0, "Riesgo medio"),
                                                  (20.1, 30.0, "Riesgo alto"),
                                                  (30.1, 100, "Riesgo muy alto")],
    "Situación económica del grupo familiar": [(0.0, 8.3, "Sin riesgo o riesgo despreciable"),
                                               (8.4, 25.0, "Riesgo bajo"),
                                               (25.1, 33.3, "Riesgo medio"),
                                               (33.4, 50.0, "Riesgo alto"),
                                               (50.1, 100, "Riesgo muy alto")],
    "Características de la vivienda y de su entorno": [(0.0, 5.6, "Sin riesgo o riesgo despreciable"),
                                                       (5.7, 11.1, "Riesgo bajo"),
                                                       (11.2, 13.9, "Riesgo medio"),
                                                       (14.0, 22.2, "Riesgo alto"),
                                                       (22.3, 100, "Riesgo muy alto")],
    "Influencia del entorno extralaboral sobre el trabajo": [(0.0, 8.3, "Sin riesgo o riesgo despreciable"),
                                                            (8.4, 16.7, "Riesgo bajo"),
                                                            (16.8, 25.0, "Riesgo medio"),
                                                            (25.1, 41.7, "Riesgo alto"),
                                                            (41.8, 100, "Riesgo muy alto")],
    "Desplazamiento vivienda trabajo vivienda": [(0.0, 0.9, "Sin riesgo o riesgo despreciable"),
                                                 (1.0, 12.5, "Riesgo bajo"),
                                                 (12.6, 25.0, "Riesgo medio"),
                                                 (25.1, 43.8, "Riesgo alto"),
                                                 (43.9, 100, "Riesgo muy alto")]
}

CLASIFICACION_CUESTIONARIO = [
    (0.0, 11.3, "Sin riesgo o riesgo despreciable"),
    (11.4, 16.9, "Riesgo bajo"),
    (17.0, 22.6, "Riesgo medio"),
    (22.7, 29.0, "Riesgo alto"),
    (29.1, 100, "Riesgo muy alto"),
]

# Dimensiones que permiten un ítem sin respuesta
DIMENSIONES_UN_ITEM_SIN_RESPUESTA = {"Características de la vivienda y de su entorno"}

# Función para clasificar un puntaje según rangos
def clasificar_riesgo(puntaje, clasificacion):
   
    for rango_min, rango_max, nivel in clasificacion:
        if rango_min <= puntaje <= rango_max:
            return nivel
    return "Clasificación no encontrada"


# Función para asignar valores a las respuestas
def asignar_valor(pregunta_num, respuesta):
    preguntas_invertidas = {1, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14,
                            15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 27, 29}

    if respuesta == "ANULADA":
        return 0

    if pregunta_num in preguntas_invertidas:
        valores = {'Siempre': 0, 'Casi siempre': 1, 'Algunas veces': 2, 'Casi nunca': 3, 'Nunca': 4}
    else:
        valores = {'Siempre': 4, 'Casi siempre': 3, 'Algunas veces': 2, 'Casi nunca': 1, 'Nunca': 0}

    return valores.get(respuesta, 0)

# Validar respuestas mínimas en una dimensión
def validar_dimension(preguntas, respuestas):
    respuestas_validas = sum(1 for p in preguntas if respuestas.get(p, "ANULADA") != "ANULADA")
    if len(preguntas) in DIMENSIONES_UN_ITEM_SIN_RESPUESTA and respuestas_validas >= len(preguntas) - 1:
        return True
    return respuestas_validas == len(preguntas)

# Calcular puntajes brutos
def calcular_puntajes(respuestas_procesadas):
    puntajes = {}
    puntaje_total = 0
    dimensiones_validas = set()

    for dimension, preguntas in DIMENSIONES.items():
        if not validar_dimension(preguntas, respuestas_procesadas):
            print(f"\n Dimensión '{dimension}' inválida por falta de respuestas suficientes.")
            puntajes[dimension] = None  # Marcar dimensión como inválida
            continue

        # Calcular puntaje bruto de la dimensión
        valores_dimension = [asignar_valor(p, respuestas_procesadas.get(p, "ANULADA")) for p in preguntas]
        puntaje_dimension = sum(valores_dimension)
        puntajes[dimension] = puntaje_dimension
        puntaje_total += puntaje_dimension
        dimensiones_validas.add(dimension)

    return puntajes, puntaje_total, dimensiones_validas

# Calcular transformados y clasificar riesgos
def calcular_transformados_y_clasificar(puntajes, puntaje_total):
    puntajes_transformados = {}
    clasificaciones = {}

    for dimension, puntaje_bruto in puntajes.items():
        if puntaje_bruto is None:  # Dimensión inválida
            puntajes_transformados[dimension] = "Sin puntaje válido"
            clasificaciones[dimension] = "Sin puntaje válido"
            continue

        # Calcular puntaje transformado y clasificación
        factor = FACTORES_DIMENSIONES.get(dimension, 1)
        transformado = round((puntaje_bruto / factor) * 100, 1)
        transformado = min(max(transformado, 0), 100)
        puntajes_transformados[dimension] = transformado

        clasificacion_dimension = clasificar_riesgo(transformado, CLASIFICACION_DIMENSIONES.get(dimension, []))
        clasificaciones[dimension] = clasificacion_dimension

    # Calcular clasificación del cuestionario
    transformado_total = round((puntaje_total / FACTOR_TOTAL_CUESTIONARIO) * 100, 1)
    transformado_total = min(max(transformado_total, 0), 100)
    clasificacion_total = clasificar_riesgo(transformado_total, CLASIFICACION_CUESTIONARIO)

    return puntajes_transformados, clasificaciones, transformado_total, clasificacion_total

# Función principal para procesar el cuestionario
def procesar_cuestionario_extralaboral(respuestas_procesadas):
    respuestas_procesadas = obtener_respuestas_procesadas3(respuestas_procesadas)
    puntajes, puntaje_total, dimensiones_validas = calcular_puntajes(respuestas_procesadas)
    puntajes_transformados, clasificaciones, transformado_total, clasificacion_total = calcular_transformados_y_clasificar(
        puntajes, puntaje_total
    )
    return list((puntajes, puntaje_total, puntajes_transformados, clasificaciones, transformado_total, clasificacion_total))

'''# Asignar transformado_total como variable exportable
transformado_total = procesar_cuestionario_extralaboral()[4]  # Índice 4 corresponde al transformado_tot


# Reporte final si se ejecuta como script principal
if __name__ == "__main__":
    (puntajes, puntaje_total, puntajes_transformados, clasificaciones,
     transformado_total, clasificacion_total) = procesar_cuestionario_extralaboral()

    print("**Resultados por Dimensión**\n")
    for dimension, puntaje_bruto in puntajes.items():
        if puntaje_bruto is not None:
            transformado = puntajes_transformados[dimension]
            clasificacion = clasificaciones[dimension]
            print(f"  {dimension}: Bruto: {puntaje_bruto}, Transformado: {transformado}, Clasificación: {clasificacion}")
        else:
            print(f"  {dimension}: Sin puntaje válido")

    print(f"Puntaje Total del Cuestionario: Bruto: {puntaje_total}, Transformado: {transformado_total}, Clasificación: {clasificacion_total}")'''