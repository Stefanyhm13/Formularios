# Importar transformados totales de los archivos específicos
from calculosA import transformado_total as transformado_total_A
from calculosB import transformado_total as transformado_total_B
from calculosE import transformado_total as transformado_total_Extralaboral

import openpyxl
from openpyxl.styles import Font
from calculosA import procesar_cuestionario as procesar_cuestionario_A
from calculosB import procesar_cuestionario_B as procesar_cuestionario_B
from calculosE import procesar_cuestionario_extralaboral as procesar_cuestionario_Extralaboral

# Factores de transformación para los cuestionarios combinados
FACTORES_TRANSFORMACION = {
    "A + Extralaboral": 616,
    "B + Extralaboral": 512
}

# Clasificación de riesgo para los cuestionarios combinados
CLASIFICACION_CUESTIONARIOS = {
    "A + Extralaboral": [
        (0.0, 18.8, "Sin riesgo o riesgo despreciable"),
        (18.9, 24.4, "Riesgo bajo"),
        (24.5, 29.5, "Riesgo medio"),
        (29.6, 35.4, "Riesgo alto"),
        (35.5, 100, "Riesgo muy alto")
    ],
    "B + Extralaboral": [
        (0.0, 19.9, "Sin riesgo o riesgo despreciable"),
        (20.0, 24.8, "Riesgo bajo"),
        (24.9, 29.5, "Riesgo medio"),
        (29.6, 35.4, "Riesgo alto"),
        (35.5, 100, "Riesgo muy alto")
    ]
}

# Función para clasificar un puntaje según rangos
def clasificar_puntaje(puntaje, clasificacion_rangos):
    for rango_min, rango_max, nivel in clasificacion_rangos:
        if rango_min <= puntaje <= rango_max:
            return nivel
    return "Clasificación no encontrada"

# Función principal para calcular y clasificar puntajes combinados
def calcular_puntaje_total():
    # Calcular combinaciones de Forma A + Extralaboral y Forma B + Extralaboral
    puntaje_A_Extralaboral = transformado_total_A + transformado_total_Extralaboral
    puntaje_B_Extralaboral = transformado_total_B + transformado_total_Extralaboral

    # Transformar los puntajes
    transformado_A_Extralaboral = round((puntaje_A_Extralaboral / FACTORES_TRANSFORMACION["A + Extralaboral"]) * 100, 1)
    transformado_B_Extralaboral = round((puntaje_B_Extralaboral / FACTORES_TRANSFORMACION["B + Extralaboral"]) * 100, 1)

    # Clasificar los puntajes transformados
    clasificacion_A_Extralaboral = clasificar_puntaje(transformado_A_Extralaboral, CLASIFICACION_CUESTIONARIOS["A + Extralaboral"])
    clasificacion_B_Extralaboral = clasificar_puntaje(transformado_B_Extralaboral, CLASIFICACION_CUESTIONARIOS["B + Extralaboral"])

    return (puntaje_A_Extralaboral, transformado_A_Extralaboral, clasificacion_A_Extralaboral,
            puntaje_B_Extralaboral, transformado_B_Extralaboral, clasificacion_B_Extralaboral)

# Función para generar el archivo Excel
def generar_excel():
    wb = openpyxl.Workbook()

    # Hoja para Cuestionario A
    ws_a = wb.active
    ws_a.title = "Cuestionario A"
    datos_a = procesar_cuestionario_A()  # Obtener datos procesados del cuestionario A
    escribir_datos_cuestionario(ws_a, datos_a, "A")

    # Hoja para Cuestionario B
    ws_b = wb.create_sheet("Cuestionario B")
    datos_b = procesar_cuestionario_B()  # Obtener datos procesados del cuestionario B
    escribir_datos_cuestionario(ws_b, datos_b, "B")

    # Hoja para Cuestionario Extralaboral
    ws_extralaboral = wb.create_sheet("Cuestionario Extralaboral")
    datos_extralaboral = procesar_cuestionario_Extralaboral()  # Obtener datos procesados del cuestionario extralaboral
    escribir_datos_cuestionario(ws_extralaboral, datos_extralaboral, "Extralaboral")

    # Hoja para el Total General
    ws_total = wb.create_sheet("Total General")
    escribir_datos_totales(ws_total)

    # Guardar el archivo
    wb.save("Resultados_Cuestionarios.xlsx")
    print("Archivo Excel generado: Resultados_Cuestionarios.xlsx")

# Función para escribir datos de un cuestionario en una hoja
def escribir_datos_cuestionario(ws, datos, cuestionario):
    puntajes, puntaje_total, puntajes_transformados, clasificaciones, transformado_total, clasificacion_total = datos

    # Encabezados
    ws.append(["Cuestionario", cuestionario])
    ws.append(["Dimensión/Dominio", "Bruto", "Transformado", "Clasificación"])
    ws.append(["-" * 4] * 4)

    # Si el cuestionario tiene dominios
    if isinstance(next(iter(puntajes.values())), dict):
        # Desglosar dominios y dimensiones
        for dominio, dimensiones in puntajes.items():
            # Calcular total del dominio (si está presente en los datos)
            total_bruto_dominio = sum(dimensiones.values())
            total_transformado_dominio = puntajes_transformados[dominio]["TOTAL_DOMINIO"]
            clasificacion_dominio = clasificaciones[dominio]["TOTAL_DOMINIO"]

            # Escribir los resultados del dominio
            ws.append([f"Dominio: {dominio}", total_bruto_dominio, total_transformado_dominio, clasificacion_dominio])

            # Escribir las dimensiones dentro del dominio
            for dimension, bruto in dimensiones.items():
                if dimension != "TOTAL_DOMINIO":  # Ignorar el total del dominio aquí
                    transformado = puntajes_transformados[dominio][dimension]
                    clasificacion = clasificaciones[dominio][dimension]
                    ws.append([f"  Dimensión: {dimension}", bruto, transformado, clasificacion])
    else:
        # Si no hay dominios, solo dimensiones
        for dimension, bruto in puntajes.items():
            if bruto is not None:
                transformado = puntajes_transformados[dimension]
                clasificacion = clasificaciones[dimension]
                ws.append([dimension, bruto, transformado, clasificacion])

    # Total del cuestionario
    ws.append(["TOTAL", puntaje_total, transformado_total, clasificacion_total])


# Función para escribir los datos totales combinados en una hoja
def escribir_datos_totales(ws):
    # Calcular combinaciones de A + Extralaboral y B + Extralaboral
    puntaje_A_Extralaboral = transformado_total_A + transformado_total_Extralaboral
    puntaje_B_Extralaboral = transformado_total_B + transformado_total_Extralaboral

    transformado_A_Extralaboral = round((puntaje_A_Extralaboral / FACTORES_TRANSFORMACION["A + Extralaboral"]) * 100, 1)
    transformado_B_Extralaboral = round((puntaje_B_Extralaboral / FACTORES_TRANSFORMACION["B + Extralaboral"]) * 100, 1)

    clasificacion_A_Extralaboral = clasificar_puntaje(transformado_A_Extralaboral, CLASIFICACION_CUESTIONARIOS["A + Extralaboral"])
    clasificacion_B_Extralaboral = clasificar_puntaje(transformado_B_Extralaboral, CLASIFICACION_CUESTIONARIOS["B + Extralaboral"])

    # Encabezados
    ws.append(["Combinación", "Bruto", "Transformado", "Clasificación"])
    ws.append(["A + Extralaboral", puntaje_A_Extralaboral, transformado_A_Extralaboral, clasificacion_A_Extralaboral])
    ws.append(["B + Extralaboral", puntaje_B_Extralaboral, transformado_B_Extralaboral, clasificacion_B_Extralaboral])

# Función principal para calcular puntaje total y generar Excel
if __name__ == "__main__":
    calcular_puntaje_total()  # Realizar cálculos para los cuestionarios A y B
    generar_excel()  # Crear el archivo Excel con los resultados
