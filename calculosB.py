# Importar funciones necesarias desde formB
from formB import obtener_respuestas_procesadas1

# Definir los dominios y dimensiones
DOMINIOS = {
    "Liderazgo y relaciones sociales en el trabajo": {
        "Caracteristicas del liderazgo": [49, 50, 51, 52, 53, 54,55, 56, 57, 58, 59, 60, 61],
        "Relaciones sociales en el trabajo": [62, 63, 64, 65, 66, 67,68, 69, 70, 71, 72, 73],
        "Retroalimentacion del desempeño": [74, 75, 76, 77, 78],
        
    },
    "Control sobre el trabajo": {
        "Claridad de rol": [41, 42, 43, 44, 45],
        "Capacitacion": [46, 47, 48],
        "Participacion y manejo del cambio": [38, 39, 40],
        "Oportunidades para el uso y desarrollo de habilidades y conocimientos": [29, 30, 31, 32],
        "Control y autonomia sobre el trabajo": [34, 35, 36],
    },
    "Demandas del trabajo": {
        "Demandas ambientales y de esfuerzo fisico": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11, 12],
        "Demandas emocionales": [89, 90, 91, 92, 93, 94,95, 96, 97],
        "Demandas cuantitativas": [13, 14, 15],
        "Influencia del trabajo sobre el entorno extralaboral": [25, 26, 27, 28],
        "Demandas de carga mental": [16, 17, 18, 19, 20],
        "Demandas de la jornada de trabajo": [21, 22, 23, 24, 33, 37]
    },
    "Recompensas": {
        "Recompensas derivadas de la pertenencia a la organizacion y del trabajo que se realiza": [85, 86, 87, 88],
        "Reconocimiento y compensacion": [79, 80, 81, 82, 83, 84],
    }
}

## Factores de transformación para dimensiones, dominios y puntaje total
FACTORES_DIMENSIONES = {
    "Caracteristicas del liderazgo": 52,
    "Relaciones sociales en el trabajo": 48,
    "Retroalimentacion del desempeño": 20,
    "Claridad de rol": 20,
    "Capacitacion": 12,
    "Participacion y manejo del cambio": 12,
    "Oportunidades para el uso y desarrollo de habilidades y conocimientos": 16,
    "Control y autonomia sobre el trabajo": 12,
    "Demandas ambientales y de esfuerzo fisico": 48,
    "Demandas emocionales": 36,
    "Demandas cuantitativas": 12,
    "Influencia del trabajo sobre el entorno extralaboral": 16,
    "Demandas de carga mental": 20,
    "Demandas de la jornada de trabajo": 24,
    "Recompensas derivadas de la pertenencia a la organizacion y del trabajo que se realiza": 16,
    "Reconocimiento y compensacion": 24,
}

FACTORES_DOMINIOS = {
    "Liderazgo y relaciones sociales en el trabajo": 120,
    "Control sobre el trabajo": 72,
    "Demandas del trabajo": 156,
    "Recompensas": 40,
}

FACTOR_TOTAL_CUESTIONARIO = 388

# Clasificación de riesgo
CLASIFICACION_DIMENSIONES = {
    "Caracteristicas del liderazgo": [(0.0, 3.8, "Sin riesgo o riesgo despreciable"),
                                      (3.9, 13.5, "Riesgo bajo"),
                                      (13.6, 25.0, "Riesgo medio"),
                                      (25.1, 38.5, "Riesgo alto"),
                                      (38.6, 100, "Riesgo muy alto")],

    "Relaciones sociales en el trabajo": [(0.0, 6.3, "Sin riesgo o riesgo despreciable"),
                                          (6.4, 14.6, "Riesgo bajo"),
                                          (14.7, 27.1, "Riesgo medio"),
                                          (27.2, 37.5, "Riesgo alto"),
                                          (37.6, 100, "Riesgo muy alto")],

    "Retroalimentacion del desempeño": [(0.0, 5.0, "Sin riesgo o riesgo despreciable"),
                                        (5.1, 20.0, "Riesgo bajo"),
                                        (20.1, 30.0, "Riesgo medio"),
                                        (30.1, 50.0, "Riesgo alto"),
                                        (50.1, 100, "Riesgo muy alto")],

    "Claridad de rol": [(0.0, 0.9, "Sin riesgo o riesgo despreciable"),
                        (1.0, 5.0, "Riesgo bajo"),
                        (5.1, 15.0, "Riesgo medio"),
                        (15.1, 30.0, "Riesgo alto"),
                        (30.1, 100, "Riesgo muy alto")],

    "Capacitacion": [(0.0, 0.9, "Sin riesgo o riesgo despreciable"),
                     (1.0, 16.7, "Riesgo bajo"),
                     (16.8, 25.0, "Riesgo medio"),
                     (25.1, 50.0, "Riesgo alto"),
                     (50.1, 100, "Riesgo muy alto")],

    "Participacion y manejo del cambio": [(0.0, 16.7, "Sin riesgo o riesgo despreciable"),
                                          (16.8, 33.3, "Riesgo bajo"),
                                          (33.4, 41.7, "Riesgo medio"),
                                          (41.8, 58.3, "Riesgo alto"),
                                          (58.4, 100, "Riesgo muy alto")],

    "Oportunidades para el uso y desarrollo de habilidades y conocimientos": 
                                          [(0.0, 12.5, "Sin riesgo o riesgo despreciable"),
                                          (12.6, 25.0, "Riesgo bajo"),
                                          (25.1, 37.5, "Riesgo medio"),
                                          (37.6, 56.3, "Riesgo alto"),
                                          (56.4, 100, "Riesgo muy alto")],

    "Control y autonomia sobre el trabajo": [(0.0, 33.3, "Sin riesgo o riesgo despreciable"),
                                             (33.4, 50.0, "Riesgo bajo"),
                                             (50.1, 66.7, "Riesgo medio"),
                                             (66.8, 75.0, "Riesgo alto"),
                                             (75.1, 100, "Riesgo muy alto")],

    "Demandas ambientales y de esfuerzo fisico": [(0.0, 22.9, "Sin riesgo o riesgo despreciable"),
                                                  (23.0, 31.3, "Riesgo bajo"),
                                                  (31.4, 39.6, "Riesgo medio"),
                                                  (39.7, 47.9, "Riesgo alto"),
                                                  (48.0, 100, "Riesgo muy alto")],

    "Demandas emocionales": [(0.0, 19.4, "Sin riesgo o riesgo despreciable"),
                             (19.5, 27.8, "Riesgo bajo"),
                             (27.9, 38.9, "Riesgo medio"),
                             (39.0, 47.2, "Riesgo alto"),
                             (47.3, 100, "Riesgo muy alto")],

    "Demandas cuantitativas": [(0.0, 16.7, "Sin riesgo o riesgo despreciable"),
                               (16.8, 33.3, "Riesgo bajo"),
                               (33.4, 41.7, "Riesgo medio"),
                               (41.8, 50.0, "Riesgo alto"),
                               (50.1, 100, "Riesgo muy alto")],

    "Influencia del trabajo sobre el entorno extralaboral": [(0.0, 12.5, "Sin riesgo o riesgo despreciable"),
                                                            (12.6, 25.0, "Riesgo bajo"),
                                                            (25.1, 31.3, "Riesgo medio"),
                                                            (31.4, 50.0, "Riesgo alto"),
                                                            (50.1, 100, "Riesgo muy alto")],

    "Demandas de carga mental": [(0.0, 50.0, "Sin riesgo o riesgo despreciable"),
                                 (50.1, 65.0, "Riesgo bajo"),
                                 (65.1, 75.0, "Riesgo medio"),
                                 (75.1, 85.0, "Riesgo alto"),
                                 (85.1, 100, "Riesgo muy alto")],

    "Demandas de la jornada de trabajo": [(0.0, 25.0, "Sin riesgo o riesgo despreciable"),
                                          (25.1, 37.5, "Riesgo bajo"),
                                          (37.6, 45.8, "Riesgo medio"),
                                          (45.9, 58.3, "Riesgo alto"),
                                          (58.4, 100, "Riesgo muy alto")],

    "Recompensas derivadas de la pertenencia a la organizacion y del trabajo que se realiza": [
        (0.0, 0.9, "Sin riesgo o riesgo despreciable"),
        (1.0, 6.3, "Riesgo bajo"),
        (6.4, 12.5, "Riesgo medio"),
        (12.6, 18.8, "Riesgo alto"),
        (18.9, 100, "Riesgo muy alto")
    ],

    "Reconocimiento y compensacion": [(0.0, 0.9, "Sin riesgo o riesgo despreciable"),
                                      (1.0, 12.5, "Riesgo bajo"),
                                      (12.6, 25.0, "Riesgo medio"),
                                      (25.1, 37.5, "Riesgo alto"),
                                      (37.6, 100, "Riesgo muy alto")]
}


CLASIFICACION_DOMINIOS = {
    "Liderazgo y relaciones sociales en el trabajo": [
        (0.0, 8.3, "Sin riesgo o riesgo despreciable"),
        (8.4, 17.5, "Riesgo bajo"),
        (17.6, 26.7, "Riesgo medio"),
        (26.8, 38.3, "Riesgo alto"),
        (38.4, 100, "Riesgo muy alto")
    ],

    "Control sobre el trabajo": [
        (0.0, 19.4, "Sin riesgo o riesgo despreciable"),
        (19.5, 26.4, "Riesgo bajo"),
        (26.5, 34.7, "Riesgo medio"),
        (34.8, 43.1, "Riesgo alto"),
        (43.2, 100, "Riesgo muy alto")
    ],

    "Demandas del trabajo": [
        (0.0, 26.9, "Sin riesgo o riesgo despreciable"),
        (27.0, 33.3, "Riesgo bajo"),
        (33.4, 37.8, "Riesgo medio"),
        (37.9, 44.2, "Riesgo alto"),
        (44.3, 100, "Riesgo muy alto")
    ],

    "Recompensas": [
        (0.0, 2.5, "Sin riesgo o riesgo despreciable"),
        (2.6, 10.0, "Riesgo bajo"),
        (10.1, 17.5, "Riesgo medio"),
        (17.6, 27.5, "Riesgo alto"),
        (27.6, 100, "Riesgo muy alto")
    ]
}

CLASIFICACION_CUESTIONARIO = [
    (0.0 , 19.9, "Sin riesgo o riesgo despreciable"),
    (20.0 , 24.8, "Riesgo bajo"),
    (24.9 , 29.5, "Riesgo medio"),
    (29.6 , 35.4, "Riesgo alto"),
    (35.5 , 100, "Riesgo muy alto"),
]
# Dimensiones que permiten un ítem sin respuesta
DIMENSIONES_UN_ITEM_SIN_RESPUESTA = {"Caracteristicas del liderazgo", "Relaciones sociales en el trabajo",
                                      "Demandas ambientales y de esfuerzo fisico"}

# Función para clasificar un puntaje según rangos
def clasificar_riesgo(puntaje, clasificacion):
    for rango_min, rango_max, nivel in clasificacion:
        if rango_min <= puntaje <= rango_max:
            return nivel
    return "Clasificación no encontrada"

# Función para asignar valores a las respuestas
def asignar_valor(pregunta_num, respuesta):
    preguntas_invertidas = { ... }  # Mantén el conjunto de preguntas invertidas como en el código original

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

    for dominio, dimensiones in DOMINIOS.items():
        puntajes[dominio] = {}
        for dimension, preguntas in dimensiones.items():
            if not validar_dimension(preguntas, respuestas_procesadas):
                print(f"\n Dimensión '{dimension}' inválida por falta de respuestas suficientes.")
                continue
            
            valores_dimension = [asignar_valor(p, respuestas_procesadas.get(p, "ANULADA")) for p in preguntas]
            puntaje_dimension = sum(valores_dimension)
            puntajes[dominio][dimension] = puntaje_dimension
            puntaje_total += puntaje_dimension
            dimensiones_validas.add(dimension)
    
    return puntajes, puntaje_total, dimensiones_validas

# Calcular transformados y clasificar riesgos
def calcular_transformados_y_clasificar(puntajes, puntaje_total, dimensiones_validas):
    puntajes_transformados = {}
    clasificaciones = {}

    for dominio, dimensiones in puntajes.items():
        puntajes_transformados[dominio] = {}
        clasificaciones[dominio] = {}

        for dimension, puntaje_bruto in dimensiones.items():
            if dimension not in dimensiones_validas:
                continue

            factor = FACTORES_DIMENSIONES.get(dimension, 1)
            transformado = round((puntaje_bruto / factor) * 100, 1)
            transformado = min(max(transformado, 0), 100)
            puntajes_transformados[dominio][dimension] = transformado

            clasificacion_dimension = clasificar_riesgo(transformado, CLASIFICACION_DIMENSIONES.get(dimension, []))
            clasificaciones[dominio][dimension] = clasificacion_dimension

        total_bruto_dominio = sum(dimensiones.values())
        factor_dominio = FACTORES_DOMINIOS.get(dominio, 1)
        transformado_dominio = round((total_bruto_dominio / factor_dominio) * 100, 1)
        transformado_dominio = min(max(transformado_dominio, 0), 100)
        clasificacion_dominio = clasificar_riesgo(transformado_dominio, CLASIFICACION_DOMINIOS.get(dominio, []))

        puntajes_transformados[dominio]["TOTAL_DOMINIO"] = transformado_dominio
        clasificaciones[dominio]["TOTAL_DOMINIO"] = clasificacion_dominio

    transformado_total = round((puntaje_total / FACTOR_TOTAL_CUESTIONARIO) * 100, 1)
    transformado_total = min(max(transformado_total, 0), 100)
    clasificacion_total = clasificar_riesgo(transformado_total, CLASIFICACION_CUESTIONARIO)

    return puntajes_transformados, clasificaciones, transformado_total, clasificacion_total

# Función principal para procesar el cuestionario
def procesar_cuestionario_B():
    # Obtener respuestas procesadas desde formB
    respuestas_procesadas1 = obtener_respuestas_procesadas1()

    # Imprimir las respuestas procesadas y sus valores
    print("\n**Respuestas Procesadas y sus Valores:**")
    for pregunta, respuesta in respuestas_procesadas1.items():
        valor = asignar_valor(pregunta, respuesta)
        print(f"Pregunta {pregunta}: Respuesta '{respuesta}' -> Valor: {valor}")

    # Calcular puntajes brutos
    puntajes, puntaje_total, dimensiones_validas = calcular_puntajes(respuestas_procesadas1)

    # Calcular transformados y clasificaciones
    puntajes_transformados, clasificaciones, transformado_total, clasificacion_total = calcular_transformados_y_clasificar(
        puntajes, puntaje_total, dimensiones_validas
    )

    # Imprimir los resultados por dominio y dimensión
    print("\n**Resultados por Dominio y Dimensión**\n")
    for dominio, dimensiones in puntajes.items():
        print(f"Dominio: {dominio}")
        total_bruto_dominio = 0  # Inicializamos el puntaje bruto del dominio

        for dimension, puntaje_bruto in dimensiones.items():
            if dimension == "TOTAL_BRUTO_DOMINIO":
                continue  # El total del dominio será mostrado al final

            if dimension in dimensiones_validas:
                transformado = puntajes_transformados[dominio][dimension]
                clasificacion = clasificaciones[dominio][dimension]
                print(f"  {dimension}: Bruto: {puntaje_bruto}, Transformado: {transformado}, Clasificación: {clasificacion}")
                total_bruto_dominio += puntaje_bruto
            else:
                print(f"  {dimension}: Sin puntaje válido")

        # Imprimir el total del dominio si tiene puntajes válidos
        if total_bruto_dominio > 0:
            total_transformado = puntajes_transformados[dominio]["TOTAL_DOMINIO"]
            clasificacion_total_dominio = clasificaciones[dominio]["TOTAL_DOMINIO"]
            print(f"  TOTAL_DOMINIO: Bruto: {total_bruto_dominio}, Transformado: {total_transformado}, Clasificación: {clasificacion_total_dominio}")
        else:
            print(f"  TOTAL_DOMINIO: Sin puntaje válido")
        print()

    # Imprimir el puntaje total del cuestionario (bruto y transformado)
    print(f"Puntaje Total del Cuestionario: Bruto: {puntaje_total}, Transformado: {transformado_total}, Clasificación: {clasificacion_total}")

    # Retornar todos los resultados
    return puntajes, puntaje_total, puntajes_transformados, clasificaciones, transformado_total, clasificacion_total

# Asignar transformado_total como variable exportable
transformado_total = procesar_cuestionario_B()[4]  # Índice 4 corresponde al transformado_total



# Ejecutar como script principal
if __name__ == "__main__":
    procesar_cuestionario_B()

else:
    (puntajes, puntaje_total, puntajes_transformados, clasificaciones, 
     transformado_total, clasificacion_total) = procesar_cuestionario_B()    
