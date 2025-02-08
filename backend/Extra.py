from pdf2image import convert_from_path
import cv2
import numpy as np
import os
from pathlib import Path
from backend.rutas import poppler_path

# ===================== 1. Rutas principales y configuración inicial =====================
directorio_base = os.path.dirname(os.path.abspath(__file__))
directorio_plantillas = os.path.join(directorio_base, 'plantillasC')
ruta_pdf_referencia = os.path.join(directorio_base, 'refE.pdf')

def obtener_respuestas_procesadas3(respuestas_totales):
    respuestas_procesadas3 = {}
    for pagina_respuestas in respuestas_totales:
        lineas = pagina_respuestas.split("\n")
        for linea in lineas:
            if "Pregunta" in linea:
                partes = linea.split(":")
                pregunta = int(partes[0].replace("Pregunta", "").strip())
                respuesta = partes[1].strip()
                respuestas_procesadas3[pregunta] = respuesta
    return respuestas_procesadas3

def funcion_procesare(cuestionarios):
  
    if len(cuestionarios) <= 1 or cuestionarios[2] is None:
        raise FileNotFoundError("El cuestionario Intralaboral no fue encontrado.")

    ruta_cuestionario = cuestionarios[2]

    if not Path(ruta_cuestionario).exists():
        raise FileNotFoundError(f"El archivo {ruta_cuestionario} no existe.")
    
    # Crear la carpeta de plantillas si no existe
    if not os.path.exists(directorio_plantillas):
        os.makedirs(directorio_plantillas)
        
    # Generar plantillas desde el PDF de referencia
    paginas_referencia = convert_from_path(ruta_pdf_referencia, poppler_path=poppler_path)

    plantillas = []
    for i, pagina in enumerate(paginas_referencia):
        # Convertir cada página a imagen OpenCV
        imagen_cv = cv2.cvtColor(np.array(pagina), cv2.COLOR_RGB2BGR)

        # Guardar cada plantilla
        ruta_plantilla = os.path.join(directorio_plantillas, f'plantilla_pagina_{i + 1}.png')
        cv2.imwrite(ruta_plantilla, imagen_cv)
        plantillas.append(imagen_cv)

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

    paginas_cuestionario = convert_from_path(ruta_cuestionario, poppler_path=poppler_path)

    imagenes_alineadas = []
    for i, pagina in enumerate(paginas_cuestionario):
        imagen_cv = cv2.cvtColor(np.array(pagina), cv2.COLOR_RGB2BGR)
        
        try:
            # Alinear con la plantilla correspondiente
            imagen_alineada = alinear_con_plantilla(imagen_cv, plantillas[i])
            imagenes_alineadas.append(imagen_alineada)

        except ValueError as e:
            print(f"Error al alinear la página {i + 1}: {e}")

    # Integrar imágenes alineadas en el resto del procesamiento
    paginas = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in imagenes_alineadas]

    '''# Inicialización de las variables de desplazamiento
    desplazamiento_x, desplazamiento_y = 0, 0'''

    # Función para contar píxeles negros en un área cuadrada especificada por las coordenadas
    def contar_pixeles_negros(imagen, x1, y1, x2, y2):
        region = imagen[y1:y2, x1:x2]
        gris = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        _, binarizada = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)
        pixeles_negros = np.sum(binarizada == 0)
        return pixeles_negros


    # Coordenadas para las preguntas y respuestas desde la 1 hasta la 10
    coordenadas_pagina_1 = {
        1: {'Siempre': ((868, 744), (986, 809)), 'Casi siempre': ((995, 745), (1108, 807)), 'Algunas veces': ((1118, 745), (1228, 807)), 'Casi nunca': ((1241, 744), (1357, 807)), 'Nunca': ((1366, 742), (1478, 806))},
        2: {'Siempre': ((868, 819), (985, 921)), 'Casi siempre': ((994, 818), (1110, 921)), 'Algunas veces': ((1120, 817), (1233, 920)), 'Casi nunca': ((1242, 818), (1356, 919)), 'Nunca': ((1365, 817), (1479, 917))},
        3: {'Siempre': ((870, 931), (985, 1008)), 'Casi siempre': ((997, 931), (1109, 1009)), 'Algunas veces': ((1118, 930), (1232, 1005)), 'Casi nunca': ((1241, 929), (1355, 1005)), 'Nunca': ((1365, 929), (1481, 1007))},
        4: {'Siempre': ((870, 1018), (986, 1101)), 'Casi siempre': ((995, 1018), (1111, 1101)), 'Algunas veces': ((1119, 1018), (1233, 1100)), 'Casi nunca': ((1242, 1017), (1356, 1100)), 'Nunca': ((1367, 1017), (1480, 1097))},
        5: {'Siempre': ((871, 1112), (988, 1171)), 'Casi siempre': ((997, 1111), (1108, 1169)), 'Algunas veces': ((1119, 1111), (1234, 1171)), 'Casi nunca': ((1244, 1110), (1358, 1171)), 'Nunca': ((1367, 1110), (1482, 1168))},
        6: {'Siempre': ((870, 1182), (986, 1261)), 'Casi siempre': ((997, 1182), (1111, 1261)), 'Algunas veces': ((1120, 1180), (1234, 1261)), 'Casi nunca': ((1244, 1181), (1357, 1259)), 'Nunca': ((1368, 1180), (1479, 1259))},
        7: {'Siempre': ((871, 1272), (987, 1353)), 'Casi siempre': ((999, 1274), (1111, 1352)), 'Algunas veces': ((1121, 1274), (1233, 1352)), 'Casi nunca': ((1242, 1271), (1359, 1352)), 'Nunca': ((1368, 1273), (1482, 1351))},
        8: {'Siempre': ((871, 1363), (985, 1443)), 'Casi siempre': ((998, 1364), (1111, 1444)), 'Algunas veces': ((1121, 1364), (1233, 1443)), 'Casi nunca': ((1244, 1362), (1359, 1442)), 'Nunca': ((1369, 1364), (1483, 1440))},
        9: {'Siempre': ((873, 1456), (988, 1535)), 'Casi siempre': ((998, 1456), (1110, 1535)), 'Algunas veces': ((1122, 1456), (1234, 1534)), 'Casi nunca': ((1246, 1456), (1355, 1533)), 'Nunca': ((1370, 1454), (1483, 1533))},
        10: {'Siempre': ((873, 1548), (988, 1606)), 'Casi siempre': ((999, 1547), (1112, 1607)), 'Algunas veces': ((1124, 1546), (1236, 1604)), 'Casi nunca': ((1245, 1546), (1360, 1605)), 'Nunca': ((1368, 1545), (1484, 1604))},
        11: {'Siempre': ((873, 1618), (989, 1679)), 'Casi siempre': ((1000, 1618), (1114, 1677)), 'Algunas veces': ((1124, 1616), (1235, 1676)), 'Casi nunca': ((1247, 1616), (1360, 1675)), 'Nunca': ((1369, 1615), (1483, 1676))},
        12: {'Siempre': ((875, 1689), (989, 1770)), 'Casi siempre': ((1002, 1689), (1113, 1770)), 'Algunas veces': ((1125, 1687), (1236, 1770)), 'Casi nunca': ((1247, 1688), (1359, 1768)), 'Nunca': ((1370, 1686), (1483, 1767))},
        13: {'Siempre': ((874, 1781), (990, 1863)), 'Casi siempre': ((1002, 1781), (1114, 1861)), 'Algunas veces': ((1124, 1781), (1237, 1859)), 'Casi nunca': ((1247, 1780), (1359, 1860)), 'Nunca': ((1371, 1780), (1485, 1858))}
    }


    coordenadas_pagina_2 = {
        14: {'Siempre': ((842, 756), (965, 835)), 'Casi siempre': ((978, 756), (1095, 835)), 'Algunas veces': ((1104, 757), (1227, 836)), 'Casi nunca': ((1237, 759), (1348, 835)), 'Nunca': ((1359, 759), (1473, 836))},
        15: {'Siempre': ((841, 848), (963, 928)), 'Casi siempre': ((978, 848), (1092, 928)), 'Algunas veces': ((1105, 846), (1222, 928)), 'Casi nunca': ((1238, 849), (1347, 927)), 'Nunca': ((1359, 848), (1471, 929))},
        16: {'Siempre': ((840, 939), (964, 1019)), 'Casi siempre': ((977, 937), (1093, 1019)), 'Algunas veces': ((1107, 940), (1224, 1020)), 'Casi nunca': ((1237, 942), (1347, 1020)), 'Nunca': ((1359, 940), (1470, 1021))},
        17: {'Siempre': ((841, 1033), (964, 1111)), 'Casi siempre': ((978, 1033), (1093, 1111)), 'Algunas veces': ((1107, 1034), (1225, 1112)), 'Casi nunca': ((1238, 1034), (1346, 1110)), 'Nunca': ((1360, 1034), (1472, 1113))},
        18: {'Siempre': ((841, 1123), (965, 1203)), 'Casi siempre': ((976, 1125), (1093, 1203)), 'Algunas veces': ((1106, 1124), (1225, 1203)), 'Casi nunca': ((1235, 1123), (1347, 1203)), 'Nunca': ((1360, 1124), (1470, 1202))},
        19: {'Siempre': ((841, 1215), (965, 1273)), 'Casi siempre': ((977, 1214), (1094, 1273)), 'Algunas veces': ((1106, 1215), (1223, 1273)), 'Casi nunca': ((1236, 1216), (1345, 1274)), 'Nunca': ((1359, 1216), (1470, 1274))},
        20: {'Siempre': ((843, 1286), (964, 1360)), 'Casi siempre': ((977, 1286), (1093, 1359)), 'Algunas veces': ((1104, 1285), (1225, 1359)), 'Casi nunca': ((1237, 1288), (1349, 1361)), 'Nunca': ((1360, 1286), (1470, 1359))},
        21: {'Siempre': ((841, 1370), (964, 1451)), 'Casi siempre': ((976, 1372), (1093, 1450)), 'Algunas veces': ((1105, 1371), (1225, 1452)), 'Casi nunca': ((1236, 1372), (1348, 1452)), 'Nunca': ((1359, 1371), (1470, 1451))},
        22: {'Siempre': ((841, 1464), (964, 1544)), 'Casi siempre': ((975, 1464), (1093, 1544)), 'Algunas veces': ((1106, 1465), (1223, 1545)), 'Casi nunca': ((1236, 1465), (1345, 1544)), 'Nunca': ((1360, 1465), (1469, 1545))},
        23: {'Siempre': ((841, 1557), (965, 1637)), 'Casi siempre': ((977, 1557), (1094, 1636)), 'Algunas veces': ((1106, 1558), (1223, 1638)), 'Casi nunca': ((1236, 1556), (1345, 1636)), 'Nunca': ((1360, 1557), (1470, 1638))},
        24: {'Siempre': ((840, 1648), (964, 1726)), 'Casi siempre': ((977, 1649), (1095, 1726)), 'Algunas veces': ((1108, 1649), (1226, 1728)), 'Casi nunca': ((1238, 1649), (1347, 1727)), 'Nunca': ((1358, 1649), (1468, 1729))},
        25: {'Siempre': ((841, 1739), (962, 1800)), 'Casi siempre': ((978, 1740), (1093, 1800)), 'Algunas veces': ((1104, 1739), (1222, 1798)), 'Casi nunca': ((1235, 1739), (1347, 1800)), 'Nunca': ((1359, 1741), (1470, 1799))},
        26: {'Siempre': ((841, 1811), (964, 1921)), 'Casi siempre': ((976, 1811), (1092, 1920)), 'Algunas veces': ((1108, 1811), (1224, 1921)), 'Casi nunca': ((1236, 1812), (1350, 1923)), 'Nunca': ((1358, 1811), (1470, 1919))},
        27: {'Siempre': ((840, 1933), (964, 2014)), 'Casi siempre': ((975, 1932), (1093, 2013)), 'Algunas veces': ((1106, 1932), (1225, 2014)), 'Casi nunca': ((1236, 1933), (1348, 2014)), 'Nunca': ((1358, 1935), (1473, 2015))}
    }

    coordenadas_pagina_3 = {
        28: {'Siempre': ((848, 626), (973, 708)), 'Casi siempre': ((983, 626), (1101, 707)), 'Algunas veces': ((1113, 627), (1232, 705)), 'Casi nunca': ((1244, 627), (1354, 707)), 'Nunca': ((1366, 626), (1477, 707))},
        29: {'Siempre': ((848, 720), (971, 799)), 'Casi siempre': ((984, 719), (1102, 801)), 'Algunas veces': ((1113, 719), (1232, 798)), 'Casi nunca': ((1245, 719), (1356, 799)), 'Nunca': ((1364, 719), (1478, 799))},
        30: {'Siempre': ((848, 811), (972, 919)), 'Casi siempre': ((984, 811), (1101, 916)), 'Algunas veces': ((1112, 813), (1230, 917)), 'Casi nunca': ((1242, 813), (1355, 918)), 'Nunca': ((1366, 812), (1478, 915))},
        31: {'Siempre': ((848, 928), (972, 1009)), 'Casi siempre': ((983, 932), (1101, 1010)), 'Algunas veces': ((1114, 931), (1236, 1009)), 'Casi nunca': ((1247, 929), (1357, 1009)), 'Nunca': ((1368, 930), (1479, 1010))}
    }


    # Lista de todas las coordenadas de páginas
    coordenadas_paginas = [
        coordenadas_pagina_1,
        coordenadas_pagina_2,
        coordenadas_pagina_3,
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
            continue

        # Procesar cada pregunta y determinar la respuesta
        for pregunta, opciones in coordenadas_actual.items():
            resultados = {}
            casillas_llenas = 0
            casillas_vacias = 0

            # Procesar cada opción dentro de la pregunta
            for opcion, ((x1, y1), (x2, y2)) in opciones.items():
                pixeles_negros = contar_pixeles_negros(imagen_cv, x1, y1, x2, y2)
                resultados[opcion] = pixeles_negros

                # Considerar una casilla llena si tiene más de cierto umbral de píxeles negros
                if pixeles_negros > 150:  # Umbral ajustado
                    casillas_llenas += 1
                # Considerar una casilla vacía si tiene menos de cierto umbral
                elif pixeles_negros < 50:
                    casillas_vacias += 1

            # Determinar si la respuesta es "ANULADA" por casillas vacías o llenas
            if casillas_vacias == len(opciones):
                respuesta = "ANULADA"
                '''# Dibujar un rectángulo rojo alrededor de toda la sección de la pregunta
                for _, ((x1, y1), (x2, y2)) in opciones.items():
                    cv2.rectangle(imagen_cv, (x1, y1), (x2, y2), (0, 0, 255), 3)
                cv2.putText(imagen_cv, "ANULADA", (x1 - 60, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)'''

            elif casillas_llenas > 1:
                respuesta = "ANULADA"
                '''# Dibujar un rectángulo rojo alrededor de toda la sección de la pregunta
                for _, ((x1, y1), (x2, y2)) in opciones.items():
                    cv2.rectangle(imagen_cv, (x1, y1), (x2, y2), (0, 0, 255), 3)
                cv2.putText(imagen_cv, "ANULADA", (x1 - 60, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)'''

            else:
                # Respuesta seleccionada: la opción con más píxeles negros
                respuesta = max(resultados, key=resultados.get)
                '''# Dibujar un rectángulo verde alrededor de la casilla seleccionada
                x1, y1, x2, y2 = opciones[respuesta][0][0], opciones[respuesta][0][1], opciones[respuesta][1][0], opciones[respuesta][1][1]
                cv2.rectangle(imagen_cv, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.putText(imagen_cv, respuesta, (x1 + 10, y1 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)'''

            

            # Añadir la respuesta de la pregunta a la lista de respuestas de la página
            respuestas_pagina.append(f"Pregunta {pregunta}: {respuesta}")

        # Añadir las respuestas de esta página a la lista general de respuestas
        respuestas_totales.append(f"Página {pagina_idx + 1}:\n" + "\n".join(respuestas_pagina))

        # Agregar la imagen procesada a la lista
        imagenes_con_respuestas.append(imagen_cv)

    '''# Visualización con desplazamiento y navegación de páginas (sin cambios)
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
    cv2.destroyAllWindows()'''

    return respuestas_totales 