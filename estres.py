from pdf2image import convert_from_path
import cv2
import numpy as np
import os
from rutas import ruta_pdf_cuestionario_estres

# Ruta completa de poppler
poppler_path = r'C:\Users\practicante.rrhh\Desktop\poppler-24.08.0\Library\bin'

# Rutas principales
directorio_base = r'C:\Users\practicante.rrhh\Desktop\cuestio_extralab'
directorio_plantillas = os.path.join(directorio_base, 'plantillasD')
ruta_pdf_referencia = os.path.join(directorio_base, 'refes.pdf')

# Crear la carpeta de plantillas si no existe
if not os.path.exists(directorio_plantillas):
    os.makedirs(directorio_plantillas)

# Verificar que el archivo de referencia existe
if not os.path.exists(ruta_pdf_referencia):
    raise FileNotFoundError(f"El archivo de referencia {ruta_pdf_referencia} no existe.")

# Generar plantilla desde el PDF de referencia
print("Generando plantilla desde el PDF de referencia...")
try:
    paginas_referencia = convert_from_path(ruta_pdf_referencia, poppler_path=poppler_path)
except Exception as e:
    print(f"Error al convertir el PDF de referencia: {e}")
    raise

# Suponiendo que solo hay una plantilla
plantilla = cv2.cvtColor(np.array(paginas_referencia[0]), cv2.COLOR_RGB2BGR)

# Guardar la plantilla
ruta_plantilla = os.path.join(directorio_plantillas, 'plantilla.png')
cv2.imwrite(ruta_plantilla, plantilla)
print("La plantilla ha sido generada correctamente.")

def alinear_con_plantilla(imagen, plantilla):
    # Convertir ambas imágenes a escala de grises
    imagen_gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    plantilla_gray = cv2.cvtColor(plantilla, cv2.COLOR_BGR2GRAY)

    # Detectar puntos clave y descriptores
    orb = cv2.ORB_create(5000)
    kp1, des1 = orb.detectAndCompute(imagen_gray, None)
    kp2, des2 = orb.detectAndCompute(plantilla_gray, None)

    # Verificar si se encontraron descriptores válidos
    if des1 is None or des2 is None:
        raise ValueError("No se encontraron suficientes puntos clave en una de las imágenes.")

    # Emparejar puntos clave usando BFMatcher con Hamming
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    # Ordenar los emparejamientos por distancia
    matches = sorted(matches, key=lambda x: x.distance)

    # Calcular homografía si hay suficientes coincidencias
    if len(matches) > 10:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

        M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        altura, ancho = plantilla.shape[:2]
        return cv2.warpPerspective(imagen, M, (ancho, altura))
    else:
        raise ValueError("No se encontraron suficientes coincidencias para alinear la imagen.")

# Convertir el PDF del cuestionario a procesar a imágenes
ruta_pdf_cuestionario = ruta_pdf_cuestionario_estres
print(f"Ruta del PDF del cuestionario: {ruta_pdf_cuestionario}")
try:
    paginas_cuestionario = convert_from_path(ruta_pdf_cuestionario, poppler_path=poppler_path)
    print("Cuestionario convertido a imágenes. Procesando alineación...")
except Exception as e:
    print(f"Error al convertir el PDF del cuestionario: {e}")
    raise

imagenes_alineadas = []
for i, pagina in enumerate(paginas_cuestionario):
    imagen_cv = cv2.cvtColor(np.array(pagina), cv2.COLOR_RGB2BGR)
    
    try:
        # Alinear con la única plantilla disponible
        imagen_alineada = alinear_con_plantilla(imagen_cv, plantilla)
        imagenes_alineadas.append(imagen_alineada)

    except ValueError as e:
        print(f"Error al alinear la página {i + 1}: {e}")

# Integrar imágenes alineadas en el resto del procesamiento
paginas = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in imagenes_alineadas]

# Inicialización de las variables de desplazamiento
desplazamiento_x, desplazamiento_y = 0, 0

# Función para contar píxeles negros en un área cuadrada especificada por las coordenadas
def contar_pixeles_negros(imagen, x1, y1, x2, y2):
    region = imagen[y1:y2, x1:x2]
    gris = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    _, binarizada = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)
    pixeles_negros = np.sum(binarizada == 0)
    return pixeles_negros


# Coordenadas para las preguntas y respuestas desde la 1 hasta la 10
coordenadas_pagina_1 = {
    1: {'Siempre': ((956, 657), (1085, 689)), 'Casi siempre': ((1093, 656), (1223, 688)), 'A veces': ((1230, 657), (1351, 688)), 'Nunca': ((1360, 656), (1480, 687))},
    2: {'Siempre': ((955, 697), (1085, 750)), 'Casi siempre': ((1094, 697), (1223, 749)), 'A veces': ((1232, 699), (1351, 746)), 'Nunca': ((1361, 697), (1478, 746))},
    3: {'Siempre': ((958, 759), (1084, 789)), 'Casi siempre': ((1094, 758), (1222, 788)), 'A veces': ((1233, 759), (1350, 788)), 'Nunca': ((1361, 758), (1478, 786))},
    4: {'Siempre': ((957, 799), (1084, 829)), 'Casi siempre': ((1095, 799), (1221, 828)), 'A veces': ((1232, 799), (1352, 827)), 'Nunca': ((1361, 798), (1478, 828))},
    5: {'Siempre': ((957, 840), (1084, 889)), 'Casi siempre': ((1095, 840), (1222, 889)), 'A veces': ((1232, 839), (1351, 889)),'Nunca': ((1362, 839), (1480, 887))},
    6: {'Siempre': ((957, 900), (1085, 930)), 'Casi siempre': ((1095, 901), (1221, 929)), 'A veces': ((1234, 901), (1351, 929)),'Nunca': ((1363, 900), (1479, 930))},
    7: {'Siempre': ((956, 941), (1085, 971)), 'Casi siempre': ((1095, 942), (1224, 970)), 'A veces': ((1234, 941), (1352, 970)), 'Nunca': ((1362, 940), (1479, 969))},
    8: {'Siempre': ((958, 981), (1086, 1031)), 'Casi siempre': ((1096, 980), (1222, 1032)), 'A veces': ((1235, 982), (1353, 1031)),'Nunca': ((1362, 982), (1479, 1031))},
    9: {'Siempre': ((959, 1043), (1083, 1072)), 'Casi siempre': ((1095, 1042), (1223, 1070)), 'A veces': ((1235, 1042), (1350, 1070)),'Nunca': ((1362, 1042), (1479, 1070))},
    10: {'Siempre': ((959, 1083), (1085, 1133)), 'Casi siempre': ((1098, 1083), (1223, 1130)), 'A veces': ((1234, 1082), (1351, 1129)),'Nunca': ((1365, 1081), (1479, 1130))},
    11: {'Siempre': ((959, 1144), (1085, 1173)), 'Casi siempre': ((1098, 1144), (1224, 1173)), 'A veces': ((1236, 1143), (1354, 1171)),'Nunca': ((1364, 1143), (1480, 1170))},
    12: {'Siempre': ((961, 1186), (1085, 1213)), 'Casi siempre': ((1097, 1184), (1223, 1212)), 'A veces': ((1236, 1183), (1354, 1213)),'Nunca': ((1364, 1182), (1480, 1211))},
    13: {"Siempre": ((958, 1225), (1084, 1253)), "Casi siempre": ((1099, 1225), (1223, 1254)), "Algunas veces": ((1236, 1225), (1353, 1253)),"Nunca": ((1364, 1224), (1480, 1254))},
    14: {"Siempre": ((959, 1266), (1086, 1294)), "Casi siempre": ((1098, 1265), (1225, 1294)), "Algunas veces": ((1235, 1265), (1354, 1294)),"Nunca": ((1365, 1265), (1480, 1291))},
    15: {"Siempre": ((960, 1306), (1088, 1335)), "Casi siempre": ((1097, 1305), (1224, 1334)), "Algunas veces": ((1237, 1305), (1353, 1333)), "Nunca": ((1365, 1303), (1480, 1333))},
    16: {"Siempre": ((960, 1347), (1087, 1394)), "Casi siempre": ((1099, 1345), (1223, 1394)), "Algunas veces": ((1236, 1344), (1354, 1394)),  "Nunca": ((1367, 1344), (1478, 1393))},
    17: {"Siempre": ((961, 1408), (1084, 1436)), "Casi siempre": ((1097, 1407), (1225, 1435)), "Algunas veces": ((1237, 1405), (1354, 1433)),  "Nunca": ((1366, 1404), (1482, 1434))},
    18: {"Siempre": ((960, 1447), (1087, 1476)), "Casi siempre": ((1099, 1446), (1225, 1475)), "Algunas veces": ((1236, 1445), (1354, 1475)),"Nunca": ((1365, 1444), (1484, 1475))},
    19: {"Siempre": ((960, 1488), (1085, 1517)), "Casi siempre": ((1099, 1487), (1224, 1515)), "Algunas veces": ((1238, 1487), (1352, 1514)), "Nunca": ((1365, 1487), (1483, 1515))},
    20: {"Siempre": ((960, 1530), (1085, 1558)), "Casi siempre": ((1099, 1528), (1226, 1557)), "Algunas veces": ((1237, 1527), (1354, 1556)), "Nunca": ((1365, 1528), (1482, 1555))},
    21: {"Siempre": ((960, 1570), (1086, 1597)), "Casi siempre": ((1099, 1568), (1225, 1597)), "Algunas veces": ((1236, 1567), (1352, 1595)), "Nunca": ((1367, 1568), (1483, 1596))},
    22: {"Siempre": ((962, 1609), (1087, 1638)), "Casi siempre": ((1100, 1609), (1224, 1637)), "Algunas veces": ((1237, 1608), (1355, 1635)), "Nunca": ((1368, 1607), (1482, 1634))},
    23: {"Siempre": ((961, 1649), (1086, 1678)), "Casi siempre": ((1101, 1649), (1225, 1677)), "Algunas veces": ((1236, 1648), (1353, 1676)), "Nunca": ((1366, 1649), (1482, 1676))},
    24: {"Siempre": ((962, 1691), (1088, 1739)), "Casi siempre": ((1098, 1689), (1227, 1740)), "Algunas veces": ((1237, 1688), (1356, 1739)), "Nunca": ((1367, 1690), (1484, 1739))},
    25: {"Siempre": ((961, 1753), (1088, 1782)), "Casi siempre": ((1100, 1751), (1227, 1780)), "Algunas veces": ((1238, 1750), (1355, 1779)), "Nunca": ((1366, 1749), (1483, 1779))},
    26: {"Siempre": ((961, 1793), (1087, 1822)), "Casi siempre": ((1101, 1792), (1225, 1821)), "Algunas veces": ((1238, 1792), (1357, 1820)),"Nunca": ((1369, 1790), (1483, 1818))},
    27: {"Siempre": ((962, 1835), (1087, 1861)), "Casi siempre": ((1101, 1833), (1229, 1861)), "Algunas veces": ((1238, 1832), (1354, 1860)),"Nunca": ((1366, 1831), (1484, 1859))},
    28: {"Siempre": ((962, 1874), (1086, 1899)), "Casi siempre": ((1101, 1873), (1226, 1897)), "Algunas veces": ((1239, 1872), (1355, 1898)),"Nunca": ((1367, 1872), (1485, 1899))},
    29: {"Siempre": ((964, 1912), (1088, 1941)), "Casi siempre": ((1101, 1911), (1226, 1939)), "Algunas veces": ((1240, 1911), (1356, 1939)), "Nunca": ((1368, 1910), (1484, 1938))},
    30: {"Siempre": ((963, 1952), (1090, 1983)), "Casi siempre": ((1102, 1953), (1229, 1980)), "Algunas veces": ((1240, 1952), (1357, 1981)),"Nunca": ((1369, 1950), (1484, 1978))},
    31: {"Siempre": ((966, 1995), (1089, 2023)), "Casi siempre": ((1103, 1993), (1227, 2021)), "Algunas veces": ((1239, 1992), (1357, 2020)),"Nunca": ((1369, 1992), (1486, 2017))}
}

coordenadas_paginas = [
    coordenadas_pagina_1,
]

# Lista para almacenar las imágenes con respuestas dibujadas
imagenes_con_respuestas = []
# Lista para almacenar las respuestas de todas las páginas
respuestas_totales = []

# Procesar cada página del PDF

for pagina_idx, imagen in enumerate(paginas):
    imagen_cv = cv2.cvtColor(np.array(imagen), cv2.COLOR_RGB2BGR)
    respuestas_pagina = []  # Lista para almacenar respuestas de esta página

     # Obtener las coordenadas para la página actual
    if pagina_idx < len(coordenadas_paginas):
        coordenadas_actual = coordenadas_paginas[pagina_idx]
    else:
        print(f"Página {pagina_idx + 1}: No hay coordenadas definidas.")
        continue

# Procesar cada página del PDF
for pagina_idx, imagen in enumerate(paginas):
    # Convertir la imagen a formato OpenCV
    imagen_cv = cv2.cvtColor(np.array(imagen), cv2.COLOR_RGB2BGR)
    respuestas_pagina = []  # Lista para almacenar respuestas de esta página    

    # Obtener las coordenadas para la página actual
    if pagina_idx < len(coordenadas_paginas):
        coordenadas_actual = coordenadas_paginas[pagina_idx]
    else:
        print(f"Página {pagina_idx + 1}: No hay coordenadas definidas.")
        continue

    # Procesar cada pregunta y determinar la respuesta
    for pregunta, opciones in coordenadas_actual.items():
        resultados = {}
        casillas_llenas = 0
        casillas_vacias = 0

        for opcion, ((x1, y1), (x2, y2)) in opciones.items():
            pixeles_negros = contar_pixeles_negros(imagen_cv, x1, y1, x2, y2)
            resultados[opcion] = pixeles_negros

            # Consideramos que una casilla está llena si tiene más de cierto umbral de píxeles negros
            if pixeles_negros > 150:  # Umbral ajustado
                casillas_llenas += 1
            # Consideramos que una casilla está vacía si tiene menos de un umbral de píxeles negros
            elif pixeles_negros < 50:
                casillas_vacias += 1

        # Determinar si la respuesta es "ANULADA" por casillas vacías o llenas
        if casillas_vacias == len(opciones):
            respuesta = "ANULADA"
            # Dibuja un rectángulo rojo alrededor de toda la sección de la pregunta con el texto "ANULADA"
            for _, ((x1, y1), (x2, y2)) in opciones.items():
                cv2.rectangle(imagen_cv, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(imagen_cv, "ANULADA", (x1 - 60, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        elif casillas_llenas > 1:
            respuesta = "ANULADA"
            # Dibuja un rectángulo rojo alrededor de toda la sección de la pregunta con el texto "ANULADA"
            for _, ((x1, y1), (x2, y2)) in opciones.items():
                cv2.rectangle(imagen_cv, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(imagen_cv, "ANULADA", (x1 - 60, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        else:
            # Respuesta seleccionada: la opción con más píxeles negros
            respuesta = max(resultados, key=resultados.get)
            # Dibuja un rectángulo verde solo en la casilla seleccionada
            x1, y1, x2, y2 = opciones[respuesta][0][0], opciones[respuesta][0][1], opciones[respuesta][1][0], opciones[respuesta][1][1]
            cv2.rectangle(imagen_cv, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.putText(imagen_cv, respuesta, (x1 + 10, y1 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # **Imprimir el resultado en consola para depuración**
        print(f"Pregunta {pregunta}: {resultados} - Respuesta detectada: {respuesta}")

        # Añadir la respuesta de la pregunta a la lista de respuestas de la página
        respuestas_pagina.append(f"Pregunta {pregunta}: {respuesta}")

    # Añadir las respuestas de esta página a la lista general de respuestas
    respuestas_totales.append(f"Página {pagina_idx + 1}:\n" + "\n".join(respuestas_pagina))

    # Agregar la imagen procesada a la lista
    imagenes_con_respuestas.append(imagen_cv)


# Imprimir todas las respuestas de todas las páginas
print("\n".join(respuestas_totales))

def obtener_respuestas_procesadas4():
    respuestas_procesadas4 = {}
    for pagina_respuestas in respuestas_totales:
        lineas = pagina_respuestas.split("\n")
        for linea in lineas:
            if "Pregunta" in linea:
                partes = linea.split(":")
                pregunta = int(partes[0].replace("Pregunta", "").strip())
                respuesta = partes[1].strip()
                respuestas_procesadas4[pregunta] = respuesta
    return respuestas_procesadas4

# Visualización con desplazamiento y navegación de páginas (sin cambios)
indice_pagina = 0  # Página inicial
desplazamiento_x, desplazamiento_y = 0, 0
alto_ventana, ancho_ventana = 500, 1300  # Tamaño de la ventana de visualización

while True:
    # Obtiene el tamaño de la imagen actual
    alto_imagen, ancho_imagen = imagenes_con_respuestas[indice_pagina].shape[:2]
    
    # Muestra la porción de la imagen según el desplazamiento
    imagen_a_mostrar = imagenes_con_respuestas[indice_pagina][
        desplazamiento_y:desplazamiento_y + alto_ventana,
        desplazamiento_x:desplazamiento_x + ancho_ventana
    ]
    cv2.imshow('Visualizacion de Paginas', imagen_a_mostrar)

    # Espera una tecla
    tecla = cv2.waitKey(0) & 0xFF

    # Navegación entre páginas
    if tecla == ord('b'):  # Siguiente página
        indice_pagina = min(indice_pagina + 1, len(imagenes_con_respuestas) - 1)
        desplazamiento_x, desplazamiento_y = 0, 0  # Restablece desplazamiento al cambiar de página
    elif tecla == ord('v'):  # Página anterior
        indice_pagina = max(indice_pagina - 1, 0)
        desplazamiento_x, desplazamiento_y = 0, 0
    elif tecla == ord('w'):  # Arriba
        desplazamiento_y = max(0, desplazamiento_y - 20)
    elif tecla == ord('s'):  # Abajo
        desplazamiento_y = min(alto_imagen - alto_ventana, desplazamiento_y + 20)
    elif tecla == ord('a'):  # Izquierda
        desplazamiento_x = max(0, desplazamiento_x - 20)
    elif tecla == ord('d'):  # Derecha
        desplazamiento_x = min(ancho_imagen - ancho_ventana, desplazamiento_x + 20)
    elif tecla == 27:  # Tecla 'Esc' para salir
        break

# Cierra la ventana cuando termina
cv2.destroyAllWindows()
    




# Definir los grupos de preguntas y sus valores según las opciones de respuesta
GRUPOS_VALORES = {
    "grupo1": {1, 2, 3, 9, 13, 14, 15, 23, 24},
    "grupo2": {4, 5, 6, 10, 11, 16, 17, 18, 19, 25, 26, 27, 28},
    "grupo3": {7, 8, 12, 20, 21, 22, 29, 30, 31}
}

VALORES_RESPUESTAS = {
    "Siempre": {"grupo1": 9, "grupo2": 6, "grupo3": 3},
    "Casi siempre": {"grupo1": 6, "grupo2": 4, "grupo3": 2},
    "A veces": {"grupo1": 3, "grupo2": 2, "grupo3": 1},
    "Nunca": {"grupo1": 0, "grupo2": 0, "grupo3": 0}
}

# Definir los pesos para los cálculos del puntaje bruto total
PESOS = {
    "bloque1": 4,  # Ítems 1 al 8
    "bloque2": 3,  # Ítems 9 al 12
    "bloque3": 2,  # Ítems 13 al 22
    "bloque4": 1   # Ítems 23 al 31
}

# Escala de transformación y clasificación
ESCALA_TRANSFORMACION = 61.16
CLASIFICACION_JEFES = [
    (0.0, 7.8, "Muy bajo"),
    (7.9, 12.6, "Bajo"),
    (12.7, 17.7, "Medio"),
    (17.8, 25.0, "Alto"),
    (25.1, 100, "Muy alto")
]

CLASIFICACION_OPERARIOS = [
    (0.0, 6.5, "Muy bajo"),
    (6.6, 11.8, "Bajo"),
    (11.9, 17.0, "Medio"),
    (17.1, 23.4, "Alto"),
    (23.5, 100, "Muy alto")
]

# Función para asignar valores según grupo y respuesta
def asignar_valor(pregunta_num, respuesta):
    for grupo, preguntas in GRUPOS_VALORES.items():
        if pregunta_num in preguntas:
            return VALORES_RESPUESTAS.get(respuesta, {}).get(grupo, 0)
    return 0

# Validar que todas las preguntas hayan sido respondidas
def validar_respuestas_completas(respuestas_procesadas):
    return all(respuesta != "ANULADA" for respuesta in respuestas_procesadas.values())

# Calcular el puntaje bruto total
def calcular_puntaje_bruto(respuestas_procesadas):
    if not validar_respuestas_completas(respuestas_procesadas):
        return None  # Puntaje no válido si hay preguntas sin responder

    bloques = {
        "bloque1": range(1, 9),
        "bloque2": range(9, 13),
        "bloque3": range(13, 23),
        "bloque4": range(23, 32)
    }

    puntaje_bruto = 0

    for bloque, preguntas in bloques.items():
        puntajes_bloque = [asignar_valor(p, respuestas_procesadas.get(p, "ANULADA")) for p in preguntas]
        promedio_bloque = sum(puntajes_bloque) / len(preguntas)
        puntaje_bruto += promedio_bloque * PESOS[bloque]

    return round(puntaje_bruto, 2)

# Transformar el puntaje bruto
def transformar_puntaje(puntaje_bruto):
    if puntaje_bruto is None:
        return None
    transformado = (puntaje_bruto / ESCALA_TRANSFORMACION) * 100
    return round(min(max(transformado, 0), 100), 1)

# Clasificar el nivel de estrés
def clasificar_estres(puntaje_transformado, tipo_empleado):
    clasificacion = (CLASIFICACION_JEFES if tipo_empleado == "j"
                     else CLASIFICACION_OPERARIOS)

    for rango_min, rango_max, nivel in clasificacion:
        if rango_min <= puntaje_transformado <= rango_max:
            return nivel
    return "Clasificación no encontrada"

def procesar_cuestionario_estres(tipo_empleado):
    respuestas_procesadas = obtener_respuestas_procesadas4()
    puntaje_bruto = calcular_puntaje_bruto(respuestas_procesadas)

    if puntaje_bruto is None:
        return None, None, "El cuestionario no es válido porque contiene preguntas sin responder."

    puntaje_transformado = transformar_puntaje(puntaje_bruto)
    clasificacion = clasificar_estres(puntaje_transformado, tipo_empleado)

    return puntaje_bruto, puntaje_transformado, clasificacion

# Reporte final si se ejecuta como script principal
if __name__ == "__main__":
    tipo_empleado = input("Ingrese el tipo de empleado (Jefes / Operarios): ")
    resultado = procesar_cuestionario_estres(tipo_empleado)

    if isinstance(resultado, str):  # Validación fallida
        print(resultado)
    else:
        global puntaje_bruto, puntaje_transformado, clasificacion  # Declaramos las variables como globales
        puntaje_bruto, puntaje_transformado, clasificacion = resultado

        print(f"Puntaje Bruto Total: {puntaje_bruto}")
        print(f"Puntaje Transformado: {puntaje_transformado}")
        print(f"Clasificación: {clasificacion}")
