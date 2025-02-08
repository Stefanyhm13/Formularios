# Importar funciones necesarias desde IntraA
from backend.IntraA import  obtener_respuestas_procesadas

# Definir los dominios y dimensiones
DOMINIOS = {
    "Liderazgo y relaciones sociales en el trabajo": {
        "Caracteristicas del liderazgo": [63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75],
        "Relaciones sociales en el trabajo": [76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89],
        "Retroalimentacion del desempeño": [90, 91, 92, 93, 94],
        "Relacion con los colaboradores": [115, 116, 117, 118, 119, 120, 121, 122, 123],
    },
    "Control sobre el trabajo": {
        "Claridad de rol": [53, 54, 55, 56, 57, 58, 59],
        "Capacitacion": [60, 61, 62],
        "Participacion y manejo del cambio": [48, 49, 50, 51],
        "Oportunidades para el uso y desarrollo de habilidades y conocimientos": [39, 40, 41, 42],
        "Control y autonomia sobre el trabajo": [44, 45, 46],
    },
    "Demandas del trabajo": {
        "Demandas ambientales y de esfuerzo fisico": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "Demandas emocionales": [106, 107, 108, 109, 110, 111, 112, 113, 114],
        "Demandas cuantitativas": [13, 14, 15, 32, 43, 47],
        "Influencia del trabajo sobre el entorno extralaboral": [35, 36, 37, 38],
        "Exigencias de responsabilidad del cargo": [19, 22, 23, 24, 25, 26],
        "Demandas de carga mental": [16, 17, 18, 20, 21],
        "Consistencia de rol": [27, 28, 29, 30, 52],
        "Demandas de la jornada de trabajo": [31, 33, 34],
    },
    "Recompensas": {
        "Recompensas derivadas de la pertenencia a la organizacion y del trabajo que se realiza": [95, 102, 103, 104, 105],
        "Reconocimiento y compensacion": [96, 97, 98, 99, 100, 101],
    }
}

## Factores de transformación para dimensiones, dominios y puntaje total
FACTORES_DIMENSIONES = {
    "Caracteristicas del liderazgo": 52,
    "Relaciones sociales en el trabajo": 56,
    "Retroalimentacion del desempeño": 20,
    "Relacion con los colaboradores": 36,
    "Claridad de rol": 28,
    "Capacitacion": 12,
    "Participacion y manejo del cambio": 16,
    "Oportunidades para el uso y desarrollo de habilidades y conocimientos": 16,
    "Control y autonomia sobre el trabajo": 12,
    "Demandas ambientales y de esfuerzo fisico": 48,
    "Demandas emocionales": 36,
    "Demandas cuantitativas": 24,
    "Influencia del trabajo sobre el entorno extralaboral": 16,
    "Exigencias de responsabilidad del cargo": 24,
    "Demandas de carga mental": 20,
    "Consistencia de rol": 20,
    "Demandas de la jornada de trabajo": 12,
    "Recompensas derivadas de la pertenencia a la organizacion y del trabajo que se realiza": 20,
    "Reconocimiento y compensacion": 24,
}

FACTORES_DOMINIOS = {
    "Liderazgo y relaciones sociales en el trabajo": 164,
    "Control sobre el trabajo": 84,
    "Demandas del trabajo": 200,
    "Recompensas": 44,
}

FACTOR_TOTAL_CUESTIONARIO = 492

# Clasificación de riesgo
CLASIFICACION_DIMENSIONES = {
    "Caracteristicas del liderazgo": [(0.0, 3.8, "Sin riesgo o riesgo despreciable"),
                                      (3.9, 15.4, "Riesgo bajo"),
                                      (15.5, 30.8, "Riesgo medio"),
                                      (30.9, 46.2, "Riesgo alto"),
                                      (46.3, 100, "Riesgo muy alto")],

    "Relaciones sociales en el trabajo": [(0.0, 5.4, "Sin riesgo o riesgo despreciable"),
                                          (5.5, 16.1, "Riesgo bajo"),
                                          (16.2, 25.0, "Riesgo medio"),
                                          (25.1, 37.5, "Riesgo alto"),
                                          (37.6, 100, "Riesgo muy alto")],

    "Retroalimentacion del desempeño": [(0.0, 10.0, "Sin riesgo o riesgo despreciable"),
                                        (10.1, 25.0, "Riesgo bajo"),
                                        (25.1, 40.0, "Riesgo medio"),
                                        (40.1, 55.0, "Riesgo alto"),
                                        (55.1, 100, "Riesgo muy alto")],

    "Relacion con los colaboradores": [(0.0, 13.9, "Sin riesgo o riesgo despreciable"),
                                       (14.0, 25.0, "Riesgo bajo"),
                                       (25.1, 33.3, "Riesgo medio"),
                                       (33.4, 47.2, "Riesgo alto"),
                                       (47.3, 100, "Riesgo muy alto")],

    "Claridad de rol": [(0.0, 0.9, "Sin riesgo o riesgo despreciable"),
                        (1.0, 10.7, "Riesgo bajo"),
                        (10.8, 21.4, "Riesgo medio"),
                        (21.5, 39.3, "Riesgo alto"),
                        (39.4, 100, "Riesgo muy alto")],

    "Capacitacion": [(0.0, 0.9, "Sin riesgo o riesgo despreciable"),
                     (1.0, 16.7, "Riesgo bajo"),
                     (16.8, 33.3, "Riesgo medio"),
                     (33.4, 50.0, "Riesgo alto"),
                     (50.1, 100, "Riesgo muy alto")],

    "Participacion y manejo del cambio": [(0.0, 12.5, "Sin riesgo o riesgo despreciable"),
                                          (12.6, 25.0, "Riesgo bajo"),
                                          (25.1, 37.5, "Riesgo medio"),
                                          (37.6, 50.0, "Riesgo alto"),
                                          (50.1, 100, "Riesgo muy alto")],

    "Oportunidades para el uso y desarrollo de habilidades y conocimientos": 
                                          [(0.0, 0.9, "Sin riesgo o riesgo despreciable"),
                                          (1.0, 6.3, "Riesgo bajo"),
                                          (6.4, 18.8, "Riesgo medio"),
                                          (18.9, 31.3, "Riesgo alto"),
                                          (31.4, 100, "Riesgo muy alto")],

    "Control y autonomia sobre el trabajo": [(0.0, 8.3, "Sin riesgo o riesgo despreciable"),
                                             (8.4, 25.0, "Riesgo bajo"),
                                             (25.1, 41.7, "Riesgo medio"),
                                             (41.8, 58.3, "Riesgo alto"),
                                             (58.4, 100, "Riesgo muy alto")],

    "Demandas ambientales y de esfuerzo fisico": [(0.0, 14.6, "Sin riesgo o riesgo despreciable"),
                                                  (14.7, 22.9, "Riesgo bajo"),
                                                  (23.0, 31.3, "Riesgo medio"),
                                                  (31.4, 39.6, "Riesgo alto"),
                                                  (39.7, 100, "Riesgo muy alto")],

    "Demandas emocionales": [(0.0, 16.7, "Sin riesgo o riesgo despreciable"),
                             (16.8, 25.0, "Riesgo bajo"),
                             (25.1, 33.3, "Riesgo medio"),
                             (33.4, 47.2, "Riesgo alto"),
                             (47.3, 100, "Riesgo muy alto")],

    "Demandas cuantitativas": [(0.0, 25.0, "Sin riesgo o riesgo despreciable"),
                               (25.1, 33.3, "Riesgo bajo"),
                               (33.4, 45.8, "Riesgo medio"),
                               (45.9, 54.2, "Riesgo alto"),
                               (54.3, 100, "Riesgo muy alto")],

    "Influencia del trabajo sobre el entorno extralaboral": [(0.0, 18.8, "Sin riesgo o riesgo despreciable"),
                                                            (18.9, 31.3, "Riesgo bajo"),
                                                            (31.4, 43.8, "Riesgo medio"),
                                                            (43.9, 50.0, "Riesgo alto"),
                                                            (50.1, 100, "Riesgo muy alto")],

    "Exigencias de responsabilidad del cargo": [(0.0, 37.5, "Sin riesgo o riesgo despreciable"),
                                                (37.6, 54.2, "Riesgo bajo"),
                                                (54.3, 66.7, "Riesgo medio"),
                                                (66.8, 79.2, "Riesgo alto"),
                                                (79.3, 100, "Riesgo muy alto")],

    "Demandas de carga mental": [(0.0, 60.0, "Sin riesgo o riesgo despreciable"),
                                 (60.1, 70.0, "Riesgo bajo"),
                                 (70.1, 80.0, "Riesgo medio"),
                                 (80.1, 90.0, "Riesgo alto"),
                                 (90.1, 100, "Riesgo muy alto")],

    "Consistencia de rol": [(0.0, 15.0, "Sin riesgo o riesgo despreciable"),
                            (15.1, 25.0, "Riesgo bajo"),
                            (25.1, 35.0, "Riesgo medio"),
                            (35.1, 45.0, "Riesgo alto"),
                            (45.1, 100, "Riesgo muy alto")],

    "Demandas de la jornada de trabajo": [(0.0, 8.3, "Sin riesgo o riesgo despreciable"),
                                          (8.4, 25.0, "Riesgo bajo"),
                                          (25.1, 33.3, "Riesgo medio"),
                                          (33.4, 50.0, "Riesgo alto"),
                                          (50.1, 100, "Riesgo muy alto")],

    "Recompensas derivadas de la pertenencia a la organizacion y del trabajo que se realiza": [
        (0.0, 0.9, "Sin riesgo o riesgo despreciable"),
        (1.0, 5.0, "Riesgo bajo"),
        (5.1, 10.0, "Riesgo medio"),
        (10.1, 20.0, "Riesgo alto"),
        (20.1, 100, "Riesgo muy alto")
    ],

    "Reconocimiento y compensacion": [(0.0, 4.2, "Sin riesgo o riesgo despreciable"),
                                      (4.3, 16.7, "Riesgo bajo"),
                                      (16.8, 25.0, "Riesgo medio"),
                                      (29.9 , 40.5,  "Riesgo alto"),
                                      (37.6, 100, "Riesgo muy alto")]
}

CLASIFICACION_DOMINIOS = {
    "Liderazgo y relaciones sociales en el trabajo": [(0.0, 9.1, "Sin riesgo o riesgo despreciable"),
                                                     (9.2, 17.7, "Riesgo bajo"),
                                                     (17.8, 25.6, "Riesgo medio"),
                                                     (25.7, 34.8, "Riesgo alto"),
                                                     (34.9 , 100, "Riesgo muy alto")],
   

    "Control sobre el trabajo": [( 0.0 , 10.7 , "Sin riesgo o riesgo despreciable"),
                                (10.8 , 19.0, "Riesgo bajo"),
                                (19.1 , 29.8, "Riesgo medio"),
                                (29.9 , 40.5,  "Riesgo alto"),
                                (40.6 , 100, "Riesgo muy alto")],

    "Demandas del trabajo":    [(0.0 , 28.5, "Sin riesgo o riesgo despreciable"),
                               ( 28.6 , 35.0, "Riesgo bajo"),
                               ( 35.1 , 41.5, "Riesgo medio"),
                               (41.6 , 47.5,  "Riesgo alto"),
                               (47.6 , 100, "Riesgo muy alto")],

    "Recompensas":    [(0.0 , 4.5, "Sin riesgo o riesgo despreciable"),
                      ( 4.6 , 11.4, "Riesgo bajo"),
                      ( 11.5 , 20.5, "Riesgo medio"),
                      (20.6 , 29.5,   "Riesgo alto"),
                      (29.6 , 100, "Riesgo muy alto")],                           


}
CLASIFICACION_CUESTIONARIO = [
    (0.0, 19.7, "Sin riesgo o riesgo despreciable"),
    (19.8, 25.8, "Riesgo bajo"),
    (25.9, 31.5, "Riesgo medio"),
    (31.6, 38.0, "Riesgo alto"),
    (38.1, 100, "Riesgo muy alto"),
]
# Dimensiones que permiten un ítem sin respuesta
DIMENSIONES_UN_ITEM_SIN_RESPUESTA = {"Caracteristicas del liderazgo", "Relaciones sociales en el trabajo",
                                     "Relacion con los colaboradores", "Demandas ambientales y de esfuerzo fisico"}

# Función para asignar valores a las respuestas
def asignar_valor(pregunta_num, respuesta):
    preguntas_invertidas = {4, 5, 6, 9, 12, 14, 32, 34, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,
                            53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72,
                            73, 74, 75, 76, 77, 78, 79, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93,
                            94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105}

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

def clasificar_riesgo(puntaje, clasificacion):
    for rango_min, rango_max, nivel in clasificacion:
        if rango_min <= puntaje <= rango_max:
            return nivel
    return "Clasificación no encontrada"

# Función principal para procesar el cuestionario y exportar los resultados
def procesar_cuestionario(respuestas_procesadas):
    respuestas_procesadas = obtener_respuestas_procesadas(respuestas_procesadas)

    # Mostrar respuestas procesadas y valores
    print("\n**Respuestas Procesadas y sus Valores:**")
    for pregunta, respuesta in respuestas_procesadas.items():
        valor = asignar_valor(pregunta, respuesta)
        print(f"Pregunta {pregunta}: Respuesta '{respuesta}' -> Valor: {valor}")

    # Calcular puntajes y transformados
    puntajes, puntaje_total, dimensiones_validas = calcular_puntajes(respuestas_procesadas)
    puntajes_transformados, clasificaciones, transformado_total, clasificacion_total = calcular_transformados_y_clasificar(
        puntajes, puntaje_total, dimensiones_validas
    )

    # Mostrar resultados detallados
    print("\n**Resultados por Dominio y Dimensión**\n")
    for dominio, dimensiones in puntajes.items():
        print(f"Dominio: {dominio}")
        total_bruto_dominio = 0

        for dimension, puntaje_bruto in dimensiones.items():
            if dimension in dimensiones_validas:
                transformado = puntajes_transformados[dominio][dimension]
                clasificacion = clasificaciones[dominio][dimension]
                print(f"  {dimension}: Bruto: {puntaje_bruto}, Transformado: {transformado}, Clasificación: {clasificacion}")
                total_bruto_dominio += puntaje_bruto
            else:
                print(f"  {dimension}: Sin puntaje válido")

        if total_bruto_dominio > 0:
            total_transformado = puntajes_transformados[dominio]["TOTAL_DOMINIO"]
            clasificacion_total_dominio = clasificaciones[dominio]["TOTAL_DOMINIO"]
            print(f"  TOTAL_DOMINIO: Bruto: {total_bruto_dominio}, Transformado: {total_transformado}, Clasificación: {clasificacion_total_dominio}")
        else:
            print(f"  TOTAL_DOMINIO: Sin puntaje válido")
        print()

    print(f"Puntaje Total del Cuestionario: Bruto: {puntaje_total}, Transformado: {transformado_total}, Clasificación: {clasificacion_total}")
    
    return list((puntajes, puntaje_total, puntajes_transformados, clasificaciones, transformado_total, clasificacion_total))
    
