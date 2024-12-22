from pdf2image import convert_from_path
import cv2
import numpy as np
import os


# Ruta completa de poppler
poppler_path = r'C:\Users\practicante.rrhh\Desktop\poppler-24.08.0\Library\bin'

# Rutas principales
directorio_base = r'C:\Users\practicante.rrhh\Desktop\cuestio_extralab'
directorio_plantillas = os.path.join(directorio_base, 'plantillasB')
ruta_pdf_referencia = os.path.join(directorio_base, 'refB.pdf')

# Crear la carpeta de plantillas si no existe
if not os.path.exists(directorio_plantillas):
    os.makedirs(directorio_plantillas)
    

# Generar plantillas desde el PDF de referencia
print("Generando plantillas desde el PDF de referencia...")
paginas_referencia = convert_from_path(ruta_pdf_referencia, poppler_path=poppler_path)

plantillas = []
for i, pagina in enumerate(paginas_referencia):
    # Convertir cada página a imagen OpenCV
    imagen_cv = cv2.cvtColor(np.array(pagina), cv2.COLOR_RGB2BGR)

    # Guardar cada plantilla
    ruta_plantilla = os.path.join(directorio_plantillas, f'plantilla_pagina_{i + 1}.png')
    cv2.imwrite(ruta_plantilla, imagen_cv)
   
    plantillas.append(imagen_cv)

print("Todas las plantillas han sido generadas correctamente.")

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
ruta_pdf_cuestionario = os.path.join(directorio_base, '465496B.pdf')
paginas_cuestionario = convert_from_path(ruta_pdf_cuestionario, poppler_path=poppler_path)
print("Cuestionario convertido a imágenes. Procesando alineación...")

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



# Inicialización de las variables de desplazamiento
desplazamiento_x, desplazamiento_y = 0, 0

# Función para contar píxeles negros en un área cuadrada especificada por las coordenadas
def contar_pixeles_negros(imagen, x1, y1, x2, y2):
    region = imagen[y1:y2, x1:x2]
    gris = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    _, binarizada = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)
    pixeles_negros = np.sum(binarizada == 0)
    return pixeles_negros

# Función para verificar si la respuesta de la pregunta filtro es "SI" o "NO"
def verificar_si(imagen_cv, coordenadas_filtro, pagina_idx):
    
    # Contar píxeles negros para cada casilla (SI y NO)
    pixeles_si = contar_pixeles_negros(imagen_cv, *coordenadas_filtro["SI"][0], *coordenadas_filtro["SI"][1])
    pixeles_no = contar_pixeles_negros(imagen_cv, *coordenadas_filtro["NO"][0], *coordenadas_filtro["NO"][1])

    print(f"Filtro - Página {pagina_idx + 1}: SI: {pixeles_si} píxeles, NO: {pixeles_no} píxeles")

    # Determinar la respuesta según el conteo de píxeles
    respuesta_filtro = "SI" if pixeles_si > pixeles_no else "NO"

    # Configurar el color según la respuesta
    if respuesta_filtro == "SI":
        color = (0, 255, 0)  # Verde para "SI"
        x1, y1, x2, y2 = coordenadas_filtro["SI"][0][0], coordenadas_filtro["SI"][0][1], coordenadas_filtro["SI"][1][0], coordenadas_filtro["SI"][1][1]
    else:
        color = (0, 0, 255)  # Rojo para "NO"
        x1, y1, x2, y2 = coordenadas_filtro["NO"][0][0], coordenadas_filtro["NO"][0][1], coordenadas_filtro["NO"][1][0], coordenadas_filtro["NO"][1][1]

        # Si la respuesta es "NO", imprimir un mensaje específico y no procesar más preguntas
        print(f"Página {pagina_idx + 1} - Respuesta filtro: NO")
        return False

    # Dibuja el rectángulo alrededor de la respuesta seleccionada
    cv2.rectangle(imagen_cv, (x1, y1), (x2, y2), color, 3)
    cv2.putText(imagen_cv, respuesta_filtro, (x1 + 5, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Retorna True si la respuesta es "SI", False si es "NO"
    return True


# Coordenadas para las preguntas y respuestas desde la 1 hasta la 10
coordenadas_pagina_1 = {
    1: {'Siempre': ((885, 673), (1000, 744)), 'Casi siempre': ((1011, 676), (1124, 745)), 'Algunas veces': ((1134, 676), (1245, 746)), 'Casi nunca': ((1255, 677), (1368, 747)), 'Nunca': ((1378, 678), (1489, 746))},
    2: {'Siempre': ((883, 754), (1001, 810)), 'Casi siempre': ((1011, 754), (1122, 811)), 'Algunas veces': ((1133, 754), (1244, 811)), 'Casi nunca': ((1256, 755), (1368, 813)), 'Nunca': ((1377, 757), (1490, 814))},
    3: {'Siempre': ((883, 822), (1001, 904)), 'Casi siempre': ((1009, 822), (1120, 905)), 'Algunas veces': ((1131, 822), (1244, 905)), 'Casi nunca': ((1255, 824), (1366, 904)), 'Nunca': ((1377, 824), (1491, 905))},
    4: {'Siempre': ((883, 913), (997, 992)), 'Casi siempre': ((1007, 915), (1119, 992)), 'Algunas veces': ((1132, 916), (1243, 993)), 'Casi nunca': ((1253, 916), (1366, 991)), 'Nunca': ((1376, 916), (1486, 991))},
    5: {'Siempre': ((882, 1002), (998, 1059)), 'Casi siempre': ((1007, 1001), (1122, 1058)), 'Algunas veces': ((1131, 1004), (1243, 1057)), 'Casi nunca': ((1252, 1002), (1366, 1059)), 'Nunca': ((1375, 1004), (1489, 1061))},
    6: {'Siempre': ((881, 1067), (997, 1124)), 'Casi siempre': ((1008, 1068), (1119, 1125)), 'Algunas veces': ((1129, 1069), (1243, 1125)), 'Casi nunca': ((1252, 1070), (1365, 1126)), 'Nunca': ((1376, 1070), (1486, 1128))},
    7: {'Siempre': ((881, 1136), (997, 1242)), 'Casi siempre': ((1006, 1134), (1119, 1242)), 'Algunas veces': ((1130, 1135), (1242, 1244)), 'Casi nunca': ((1253, 1137), (1364, 1246)), 'Nunca': ((1375, 1138), (1486, 1245))},
    8: {'Siempre': ((882, 1252), (998, 1332)), 'Casi siempre': ((1007, 1253), (1120, 1333)), 'Algunas veces': ((1129, 1253), (1241, 1331)), 'Casi nunca': ((1251, 1256), (1362, 1333)), 'Nunca': ((1376, 1255), (1486, 1334))},
    9: {'Siempre': ((881, 1341), (997, 1420)), 'Casi siempre': ((1006, 1345), (1118, 1421)), 'Algunas veces': ((1130, 1343), (1241, 1420)), 'Casi nunca': ((1250, 1344), (1363, 1422)), 'Nunca': ((1374, 1344), (1484, 1423))},
    10: {'Siempre': ((880, 1430), (994, 1544)), 'Casi siempre': ((1007, 1432), (1116, 1545)), 'Algunas veces': ((1129, 1431), (1240, 1546)), 'Casi nunca': ((1252, 1431), (1364, 1547)), 'Nunca': ((1374, 1432), (1485, 1548))},
    11: {'Siempre': ((880, 1554), (993, 1611)), 'Casi siempre': ((1004, 1555), (1117, 1611)), 'Algunas veces': ((1127, 1556), (1241, 1614)), 'Casi nunca': ((1250, 1558), (1363, 1615)), 'Nunca': ((1374, 1559), (1486, 1615))},
    12: {'Siempre': ((879, 1620), (994, 1702)), 'Casi siempre': ((1003, 1620), (1117, 1702)), 'Algunas veces': ((1128, 1623), (1242, 1704)), 'Casi nunca': ((1250, 1625), (1363, 1706)), 'Nunca': ((1372, 1624), (1488, 1703))}
}

coordenadas_pagina_2 = {
    13: {'Siempre': ((859, 667), (977, 747)), 'Casi siempre': ((986, 670), (1098, 748)), 'Algunas veces': ((1107, 667), (1222, 749)), 'Casi nunca': ((1231, 668), (1346, 747)), 'Nunca': ((1355, 670), (1469, 748))},
    14: {'Siempre': ((858, 758), (977, 835)), 'Casi siempre': ((985, 758), (1100, 837)), 'Algunas veces': ((1107, 758), (1222, 838)), 'Casi nunca': ((1230, 756), (1346, 836)), 'Nunca': ((1356, 757), (1471, 836))},
    15: {'Siempre': ((859, 847), (976, 926)), 'Casi siempre': ((986, 845), (1099, 924)), 'Algunas veces': ((1108, 848), (1223, 924)), 'Casi nunca': ((1232, 846), (1346, 924)), 'Nunca': ((1355, 846), (1472, 926))},
    16: {'Siempre': ((861, 1167), (979, 1247)), 'Casi siempre': ((987, 1168), (1103, 1247)), 'Algunas veces': ((1112, 1168), (1221, 1246)), 'Casi nunca': ((1233, 1168), (1349, 1246)), 'Nunca': ((1358, 1169), (1470, 1245))},
    17: {'Siempre': ((861, 1257), (977, 1327)), 'Casi siempre': ((988, 1258), (1100, 1328)), 'Algunas veces': ((1109, 1256), (1224, 1328)), 'Casi nunca': ((1233, 1258), (1347, 1327)), 'Nunca': ((1356, 1256), (1470, 1328))},
    18: {'Siempre': ((861, 1339), (979, 1416)), 'Casi siempre': ((988, 1339), (1100, 1418)), 'Algunas veces': ((1110, 1339), (1223, 1417)), 'Casi nunca': ((1233, 1340), (1347, 1417)), 'Nunca': ((1356, 1338), (1471, 1417))},
    19: {'Siempre': ((861, 1427), (979, 1508)), 'Casi siempre': ((988, 1428), (1102, 1508)), 'Algunas veces': ((1111, 1430), (1225, 1507)), 'Casi nunca': ((1232, 1427), (1348, 1506)), 'Nunca': ((1357, 1428), (1470, 1505))},
    20: {'Siempre': ((862, 1518), (976, 1595)), 'Casi siempre': ((987, 1519), (1100, 1593)), 'Algunas veces': ((1111, 1517), (1223, 1595)), 'Casi nunca': ((1233, 1518), (1347, 1595)), 'Nunca': ((1358, 1517), (1473, 1597))},
    21: {'Siempre': ((841, 1842), (965, 1900)), 'Casi siempre': ((976, 1840), (1093, 1900)), 'Algunas veces': ((1103, 1840), (1224, 1898)), 'Casi nunca': ((1234, 1842), (1350, 1898)), 'Nunca': ((1358, 1842), (1474, 1898))},
    22: {'Siempre': ((839, 1908), (966, 1988)), 'Casi siempre': ((977, 1908), (1096, 1987)), 'Algunas veces': ((1105, 1909), (1225, 1988)), 'Casi nunca': ((1237, 1908), (1349, 1987)), 'Nunca': ((1359, 1910), (1471, 1987))}
}

coordenadas_pagina_3 = {
    23: {'Siempre': ((862, 567), (987, 647)), 'Casi siempre': ((996, 570), (1115, 648)), 'Algunas veces': ((1126, 571), (1245, 648)), 'Casi nunca': ((1255, 571), (1368, 648)), 'Nunca': ((1377, 571), (1490, 649))},
    24: {'Siempre': ((860, 656), (989, 735)), 'Casi siempre': ((997, 659), (1115, 735)), 'Algunas veces': ((1125, 658), (1246, 735)), 'Casi nunca': ((1256, 658), (1368, 736)), 'Nunca': ((1376, 659), (1490, 737))},
    25: {'Siempre': ((860, 744), (986, 824)), 'Casi siempre': ((995, 745), (1116, 821)), 'Algunas veces': ((1125, 747), (1245, 826)), 'Casi nunca': ((1257, 747), (1368, 827)), 'Nunca': ((1377, 747), (1488, 824))},
    26: {'Siempre': ((860, 833), (985, 913)), 'Casi siempre': ((996, 836), (1118, 915)), 'Algunas veces': ((1126, 836), (1245, 915)), 'Casi nunca': ((1255, 836), (1368, 915)), 'Nunca': ((1378, 836), (1488, 915))},
    27: {'Siempre': ((859, 922), (985, 999)), 'Casi siempre': ((995, 923), (1115, 999)), 'Algunas veces': ((1125, 925), (1244, 1001)), 'Casi nunca': ((1254, 924), (1366, 1003)), 'Nunca': ((1375, 926), (1489, 1003))},
    28: {'Siempre': ((858, 1010), (983, 1088)), 'Casi siempre': ((994, 1011), (1114, 1087)), 'Algunas veces': ((1123, 1012), (1243, 1088)), 'Casi nunca': ((1255, 1012), (1367, 1090)), 'Nunca': ((1374, 1013), (1490, 1090))},
    29: {'Siempre': ((859, 1330), (983, 1387)), 'Casi siempre': ((995, 1331), (1114, 1388)), 'Algunas veces': ((1123, 1330), (1244, 1390)), 'Casi nunca': ((1254, 1333), (1364, 1388)), 'Nunca': ((1375, 1332), (1486, 1390))},
    30: {'Siempre': ((856, 1396), (986, 1479)), 'Casi siempre': ((994, 1396), (1115, 1476)), 'Algunas veces': ((1122, 1399), (1243, 1476)), 'Casi nunca': ((1252, 1397), (1364, 1479)), 'Nunca': ((1372, 1400), (1486, 1478))},
    31: {'Siempre': ((859, 1486), (985, 1564)), 'Casi siempre': ((993, 1485), (1114, 1566)), 'Algunas veces': ((1122, 1489), (1242, 1565)), 'Casi nunca': ((1251, 1489), (1363, 1567)), 'Nunca': ((1373, 1488), (1485, 1568))},
    32: {'Siempre': ((858, 1574), (984, 1666)), 'Casi siempre': ((993, 1576), (1112, 1670)), 'Algunas veces': ((1121, 1577), (1243, 1669)), 'Casi nunca': ((1250, 1574), (1364, 1673)), 'Nunca': ((1374, 1576), (1486, 1671))},
    33: {'Siempre': ((857, 1676), (984, 1736)), 'Casi siempre': ((991, 1677), (1110, 1737)), 'Algunas veces': ((1121, 1679), (1243, 1738)), 'Casi nunca': ((1254, 1680), (1364, 1738)), 'Nunca': ((1373, 1680), (1483, 1738))},
    34: {'Siempre': ((856, 1746), (981, 1837)), 'Casi siempre': ((992, 1745), (1111, 1839)), 'Algunas veces': ((1120, 1746), (1242, 1841)), 'Casi nunca': ((1251, 1748), (1365, 1840)), 'Nunca': ((1373, 1747), (1483, 1837))},
    35: {'Siempre': ((856, 1847), (983, 1929)), 'Casi siempre': ((993, 1848), (1113, 1930)), 'Algunas veces': ((1121, 1848), (1241, 1930)), 'Casi nunca': ((1249, 1849), (1363, 1930)), 'Nunca': ((1371, 1850), (1485, 1932))}
}

coordenadas_pagina_4 = {
36: {'Siempre': ((837, 608), (963, 687)), 'Casi siempre': ((973, 610), (1091, 686)), 'Algunas veces': ((1100, 610), (1221, 686)), 'Casi nunca': ((1233, 610), (1344, 687)), 'Nunca': ((1352, 609), (1468, 686))},
37: {'Siempre': ((837, 697), (964, 776)), 'Casi siempre': ((974, 698), (1092, 776)), 'Algunas veces': ((1099, 698), (1222, 777)), 'Casi nunca': ((1231, 697), (1345, 776)), 'Nunca': ((1353, 697), (1469, 777))},
38: {'Siempre': ((860, 1019), (978, 1100)), 'Casi siempre': ((986, 1020), (1099, 1100)), 'Algunas veces': ((1109, 1024), (1221, 1098)), 'Casi nunca': ((1232, 1020), (1345, 1099)), 'Nunca': ((1355, 1021), (1469, 1099))},
39: {'Siempre': ((862, 1108), (975, 1186)), 'Casi siempre': ((987, 1111), (1096, 1183)), 'Algunas veces': ((1107, 1109), (1219, 1189)), 'Casi nunca': ((1230, 1112), (1344, 1189)), 'Nunca': ((1353, 1109), (1468, 1187))},
40: {'Siempre': ((860, 1198), (978, 1324)), 'Casi siempre': ((986, 1197), (1098, 1324)), 'Algunas veces': ((1108, 1197), (1219, 1323)), 'Casi nunca': ((1231, 1199), (1344, 1325)), 'Nunca': ((1354, 1199), (1468, 1324))},
41: {'Siempre': ((838, 1600), (967, 1681)), 'Casi siempre': ((977, 1601), (1095, 1681)), 'Algunas veces': ((1102, 1602), (1225, 1680)), 'Casi nunca': ((1236, 1601), (1345, 1680)), 'Nunca': ((1355, 1602), (1465, 1680))},
42: {'Siempre': ((840, 1690), (966, 1770)), 'Casi siempre': ((975, 1693), (1094, 1770)), 'Algunas veces': ((1104, 1691), (1224, 1769)), 'Casi nunca': ((1234, 1690), (1344, 1768)), 'Nunca': ((1354, 1692), (1468, 1771))},
43: {'Siempre': ((839, 1780), (965, 1860)), 'Casi siempre': ((976, 1780), (1093, 1860)), 'Algunas veces': ((1103, 1782), (1223, 1859)), 'Casi nunca': ((1234, 1781), (1344, 1858)), 'Nunca': ((1354, 1780), (1469, 1860))},
44: {'Siempre': ((839, 1869), (963, 1948)), 'Casi siempre': ((976, 1869), (1093, 1949)), 'Algunas veces': ((1103, 1870), (1221, 1949)), 'Casi nunca': ((1235, 1871), (1346, 1948)), 'Nunca': ((1354, 1871), (1467, 1949))}
}

coordenadas_pagina_5 = {
45: {'Siempre': ((867, 576), (991, 653)), 'Casi siempre': ((1002, 578), (1121, 655)), 'Algunas veces': ((1131, 579), (1253, 655)), 'Casi nunca': ((1262, 579), (1375, 657)), 'Nunca': ((1386, 579), (1499, 657))},
46: {'Siempre': ((884, 929), (999, 1044)), 'Casi siempre': ((1015, 930), (1125, 1042)), 'Algunas veces': ((1138, 933), (1248, 1045)), 'Casi nunca': ((1258, 933), (1372, 1047)), 'Nunca': ((1384, 933), (1494, 1049))},
47: {'Siempre': ((883, 1053), (1001, 1110)), 'Casi siempre': ((1011, 1054), (1125, 1113)), 'Algunas veces': ((1135, 1054), (1248, 1115)), 'Casi nunca': ((1255, 1055), (1371, 1114)), 'Nunca': ((1380, 1057), (1494, 1118))},
48: {'Siempre': ((883, 1119), (998, 1198)), 'Casi siempre': ((1009, 1121), (1124, 1199)), 'Algunas veces': ((1134, 1124), (1246, 1198)), 'Casi nunca': ((1257, 1124), (1370, 1201)), 'Nunca': ((1381, 1126), (1492, 1203))},
49: {'Siempre': ((859, 1441), (989, 1498)), 'Casi siempre': ((996, 1441), (1115, 1499)), 'Algunas veces': ((1125, 1443), (1248, 1499)), 'Casi nunca': ((1256, 1444), (1370, 1502)), 'Nunca': ((1380, 1445), (1493, 1502))},
50: {'Siempre': ((859, 1508), (988, 1586)), 'Casi siempre': ((998, 1508), (1115, 1587)), 'Algunas veces': ((1126, 1510), (1246, 1588)), 'Casi nunca': ((1257, 1509), (1370, 1588)), 'Nunca': ((1381, 1512), (1491, 1590))},
51: {'Siempre': ((857, 1595), (985, 1684)), 'Casi siempre': ((995, 1596), (1116, 1684)), 'Algunas veces': ((1124, 1598), (1245, 1685)), 'Casi nunca': ((1255, 1597), (1369, 1686)), 'Nunca': ((1379, 1601), (1491, 1686))},
52: {'Siempre': ((858, 1692), (986, 1773)), 'Casi siempre': ((994, 1693), (1115, 1775)), 'Algunas veces': ((1125, 1695), (1244, 1775)), 'Casi nunca': ((1256, 1696), (1366, 1776)), 'Nunca': ((1377, 1696), (1491, 1778))},
53: {'Siempre': ((857, 1782), (986, 1862)), 'Casi siempre': ((994, 1782), (1116, 1863)), 'Algunas veces': ((1125, 1785), (1245, 1864)), 'Casi nunca': ((1254, 1786), (1364, 1865)), 'Nunca': ((1377, 1787), (1490, 1868))},
54: {'Siempre': ((857, 1870), (985, 1951)), 'Casi siempre': ((994, 1874), (1114, 1950)), 'Algunas veces': ((1124, 1875), (1244, 1952)), 'Casi nunca': ((1254, 1877), (1367, 1953)), 'Nunca': ((1378, 1877), (1486, 1955))}
}

coordenadas_pagina_6 = {
55: {'Siempre': ((829, 601), (956, 657)), 'Casi siempre': ((965, 601), (1086, 655)), 'Algunas veces': ((1095, 599), (1214, 655)), 'Casi nunca': ((1226, 600), (1339, 655)), 'Nunca': ((1348, 599), (1465, 656))},
56: {'Siempre': ((829, 667), (961, 738)), 'Casi siempre': ((968, 667), (1086, 737)), 'Algunas veces': ((1095, 666), (1217, 738)), 'Casi nunca': ((1226, 667), (1337, 739)), 'Nunca': ((1348, 666), (1463, 739))},
57: {'Siempre': ((828, 749), (956, 826)), 'Casi siempre': ((965, 748), (1088, 825)), 'Algunas veces': ((1095, 749), (1216, 827)), 'Casi nunca': ((1225, 749), (1339, 824)), 'Nunca': ((1350, 749), (1463, 826))},
58: {'Siempre': ((830, 838), (956, 893)), 'Casi siempre': ((964, 837), (1086, 895)), 'Algunas veces': ((1096, 837), (1216, 893)), 'Casi nunca': ((1226, 836), (1337, 893)), 'Nunca': ((1347, 837), (1461, 893))},
59: {'Siempre': ((830, 902), (958, 960)), 'Casi siempre': ((968, 904), (1084, 960)), 'Algunas veces': ((1094, 904), (1217, 959)), 'Casi nunca': ((1226, 904), (1340, 959)), 'Nunca': ((1350, 903), (1464, 959))},
60: {'Siempre': ((830, 971), (957, 1049)), 'Casi siempre': ((966, 971), (1086, 1049)), 'Algunas veces': ((1097, 970), (1219, 1051)), 'Casi nunca': ((1228, 971), (1338, 1048)), 'Nunca': ((1350, 973), (1463, 1047))},
61: {'Siempre': ((830, 1058), (959, 1132)), 'Casi siempre': ((967, 1060), (1086, 1131)), 'Algunas veces': ((1095, 1059), (1216, 1130)), 'Casi nunca': ((1226, 1061), (1342, 1130)), 'Nunca': ((1350, 1058), (1464, 1133))},
62: {'Siempre': ((836, 1408), (960, 1490)), 'Casi siempre': ((972, 1410), (1089, 1490)), 'Algunas veces': ((1102, 1408), (1217, 1491)), 'Casi nunca': ((1232, 1410), (1342, 1491)), 'Nunca': ((1353, 1410), (1464, 1491))},
63: {'Siempre': ((835, 1504), (963, 1581)), 'Casi siempre': ((972, 1502), (1090, 1580)), 'Algunas veces': ((1102, 1502), (1220, 1580)), 'Casi nunca': ((1231, 1503), (1342, 1582)), 'Nunca': ((1352, 1502), (1463, 1580))},
64: {'Siempre': ((835, 1592), (960, 1671)), 'Casi siempre': ((971, 1591), (1089, 1671)), 'Algunas veces': ((1100, 1593), (1221, 1669)), 'Casi nunca': ((1231, 1594), (1342, 1670)), 'Nunca': ((1352, 1593), (1464, 1669))},
65: {'Siempre': ((836, 1682), (962, 1762)), 'Casi siempre': ((972, 1682), (1091, 1759)), 'Algunas veces': ((1100, 1683), (1220, 1760)), 'Casi nunca': ((1231, 1681), (1341, 1761)), 'Nunca': ((1353, 1681), (1464, 1761))},
66: {'Siempre': ((835, 1772), (961, 1849)), 'Casi siempre': ((971, 1772), (1087, 1849)), 'Algunas veces': ((1103, 1774), (1222, 1850)), 'Casi nunca': ((1231, 1771), (1344, 1849)), 'Nunca': ((1352, 1772), (1465, 1849))},
67: {'Siempre': ((835, 1862), (963, 1941)), 'Casi siempre': ((972, 1859), (1092, 1940)), 'Algunas veces': ((1101, 1861), (1220, 1937)), 'Casi nunca': ((1231, 1862), (1342, 1939)), 'Nunca': ((1351, 1860), (1460, 1940))},
68: {'Siempre': ((834, 1949), (960, 2006)), 'Casi siempre': ((971, 1950), (1091, 2007)), 'Algunas veces': ((1101, 1951), (1221, 2007)), 'Casi nunca': ((1230, 1952), (1339, 2006)), 'Nunca': ((1351, 1951), (1466, 2007))}
}

coordenadas_pagina_7 = {
69: {'Siempre': ((847, 577), (982, 657)), 'Casi siempre': ((992, 577), (1129, 658)), 'Algunas veces': ((1139, 578), (1277, 656)), 'Casi nunca': ((1286, 579), (1386, 657)), 'Nunca': ((1397, 578), (1495, 658))},
70: {'Siempre': ((847, 669), (983, 745)), 'Casi siempre': ((993, 668), (1132, 746)), 'Algunas veces': ((1141, 669), (1276, 746)), 'Casi nunca': ((1285, 669), (1387, 746)), 'Nunca': ((1397, 669), (1497, 745))},
71: {'Siempre': ((848, 756), (986, 835)), 'Casi siempre': ((994, 758), (1133, 835)), 'Algunas veces': ((1141, 756), (1276, 834)), 'Casi nunca': ((1287, 756), (1387, 835)), 'Nunca': ((1396, 757), (1495, 833))},
72: {'Siempre': ((848, 844), (980, 922)), 'Casi siempre': ((994, 844), (1132, 922)), 'Algunas veces': ((1141, 844), (1274, 922)), 'Casi nunca': ((1285, 844), (1388, 920)), 'Nunca': ((1398, 843), (1496, 922))},
73: {'Siempre': ((848, 931), (983, 1009)), 'Casi siempre': ((995, 932), (1130, 1009)), 'Algunas veces': ((1140, 933), (1278, 1010)), 'Casi nunca': ((1287, 933), (1388, 1011)), 'Nunca': ((1397, 932), (1498, 1012))},
74: {'Siempre': ((848, 1296), (983, 1375)), 'Casi siempre': ((994, 1296), (1130, 1375)), 'Algunas veces': ((1141, 1297), (1278, 1375)), 'Casi nunca': ((1288, 1299), (1388, 1375)), 'Nunca': ((1397, 1297), (1496, 1377))},
75: {'Siempre': ((848, 1385), (984, 1465)), 'Casi siempre': ((994, 1385), (1129, 1464)), 'Algunas veces': ((1141, 1385), (1276, 1465)), 'Casi nunca': ((1285, 1385), (1389, 1465)), 'Nunca': ((1400, 1386), (1494, 1467))},
76: {'Siempre': ((849, 1476), (984, 1551)), 'Casi siempre': ((995, 1476), (1129, 1553)), 'Algunas veces': ((1141, 1476), (1278, 1555)), 'Casi nunca': ((1286, 1475), (1390, 1554)), 'Nunca': ((1399, 1477), (1498, 1555))},
77: {'Siempre': ((848, 1562), (985, 1643)), 'Casi siempre': ((993, 1562), (1130, 1641)), 'Algunas veces': ((1139, 1564), (1275, 1642)), 'Casi nunca': ((1287, 1563), (1390, 1644)), 'Nunca': ((1398, 1564), (1498, 1642))},
78: {'Siempre': ((848, 1652), (985, 1732)), 'Casi siempre': ((994, 1652), (1132, 1733)), 'Algunas veces': ((1140, 1652), (1275, 1732)), 'Casi nunca': ((1285, 1654), (1386, 1731)), 'Nunca': ((1398, 1652), (1498, 1734))}
}


coordenadas_pagina_8 = {
79: {'Siempre': ((836, 760), (964, 825)), 'Casi siempre': ((970, 760), (1091, 824)), 'Algunas veces': ((1102, 760), (1225, 824)), 'Casi nunca': ((1233, 760), (1346, 825)), 'Nunca': ((1357, 761), (1470, 822))},
80: {'Siempre': ((837, 834), (964, 912)), 'Casi siempre': ((973, 835), (1093, 912)), 'Algunas veces': ((1102, 834), (1223, 912)), 'Casi nunca': ((1231, 835), (1344, 914)), 'Nunca': ((1353, 834), (1467, 913))},
81: {'Siempre': ((837, 922), (964, 1002)), 'Casi siempre': ((973, 923), (1092, 1002)), 'Algunas veces': ((1100, 923), (1222, 1002)), 'Casi nunca': ((1232, 923), (1344, 1002)), 'Nunca': ((1355, 923), (1469, 1002))},
82: {'Siempre': ((837, 1011), (962, 1082)), 'Casi siempre': ((973, 1012), (1092, 1083)), 'Algunas veces': ((1102, 1012), (1222, 1083)), 'Casi nunca': ((1234, 1010), (1349, 1082)), 'Nunca': ((1355, 1013), (1467, 1083))},
83: {'Siempre': ((837, 1092), (962, 1171)), 'Casi siempre': ((972, 1091), (1089, 1172)), 'Algunas veces': ((1102, 1093), (1222, 1171)), 'Casi nunca': ((1234, 1093), (1345, 1170)), 'Nunca': ((1356, 1092), (1469, 1173))},
84: {'Siempre': ((837, 1181), (966, 1259)), 'Casi siempre': ((972, 1181), (1092, 1259)), 'Algunas veces': ((1101, 1181), (1224, 1260)), 'Casi nunca': ((1232, 1181), (1346, 1257)), 'Nunca': ((1355, 1181), (1466, 1260))},
85: {'Siempre': ((837, 1269), (958, 1325)), 'Casi siempre': ((973, 1270), (1093, 1325)), 'Algunas veces': ((1101, 1269), (1223, 1326)), 'Casi nunca': ((1233, 1269), (1348, 1325)), 'Nunca': ((1357, 1270), (1468, 1325))},
86: {'Siempre': ((837, 1334), (963, 1393)), 'Casi siempre': ((975, 1337), (1089, 1391)), 'Algunas veces': ((1099, 1335), (1223, 1392)), 'Casi nunca': ((1232, 1335), (1344, 1391)), 'Nunca': ((1355, 1337), (1472, 1391))},
87: {'Siempre': ((836, 1400), (966, 1469)), 'Casi siempre': ((973, 1402), (1088, 1467)), 'Algunas veces': ((1102, 1402), (1222, 1471)), 'Casi nunca': ((1234, 1402), (1345, 1469)), 'Nunca': ((1355, 1400), (1467, 1469))},
88: {'Siempre': ((836, 1478), (963, 1561)), 'Casi siempre': ((972, 1480), (1094, 1563)), 'Algunas veces': ((1102, 1480), (1222, 1560)), 'Casi nunca': ((1234, 1480), (1346, 1562)), 'Nunca': ((1355, 1480), (1468, 1559))}
}

coordenadas_pagina_9 = {
89: {'Siempre': ((881, 975), (1000, 1030)), 'Casi siempre': ((1010, 976), (1126, 1034)), 'Algunas veces': ((1134, 978), (1249, 1034)), 'Casi nunca': ((1260, 977), (1376, 1032)), 'Nunca': ((1384, 978), (1500, 1033))},
90: {'Siempre': ((881, 1039), (999, 1121)), 'Casi siempre': ((1009, 1042), (1124, 1120)), 'Algunas veces': ((1134, 1042), (1248, 1121)), 'Casi nunca': ((1259, 1043), (1375, 1121)), 'Nunca': ((1384, 1043), (1499, 1121))},
91: {'Siempre': ((879, 1129), (999, 1185)), 'Casi siempre': ((1008, 1129), (1124, 1186)), 'Algunas veces': ((1132, 1130), (1248, 1185)), 'Casi nunca': ((1258, 1130), (1373, 1186)), 'Nunca': ((1383, 1132), (1500, 1188))},
92: {'Siempre': ((881, 1194), (1000, 1272)), 'Casi siempre': ((1009, 1196), (1121, 1275)), 'Algunas veces': ((1134, 1195), (1248, 1275)), 'Casi nunca': ((1259, 1196), (1373, 1273)), 'Nunca': ((1382, 1197), (1498, 1275))},
93: {'Siempre': ((880, 1281), (1000, 1363)), 'Casi siempre': ((1009, 1283), (1122, 1363)), 'Algunas veces': ((1134, 1283), (1245, 1363)), 'Casi nunca': ((1259, 1284), (1372, 1365)), 'Nunca': ((1382, 1285), (1501, 1363))},
94: {'Siempre': ((879, 1371), (994, 1448)), 'Casi siempre': ((1008, 1370), (1122, 1449)), 'Algunas veces': ((1133, 1374), (1248, 1450)), 'Casi nunca': ((1258, 1373), (1372, 1450)), 'Nunca': ((1384, 1374), (1497, 1452))},
95: {'Siempre': ((878, 1457), (1000, 1537)), 'Casi siempre': ((1008, 1460), (1121, 1538)), 'Algunas veces': ((1132, 1459), (1247, 1539)), 'Casi nunca': ((1259, 1461), (1371, 1537)), 'Nunca': ((1383, 1461), (1496, 1541))},
96: {'Siempre': ((880, 1547), (997, 1627)), 'Casi siempre': ((1007, 1547), (1120, 1628)), 'Algunas veces': ((1131, 1547), (1245, 1627)), 'Casi nunca': ((1258, 1549), (1370, 1627)), 'Nunca': ((1380, 1549), (1495, 1627))},
97: {'Siempre': ((878, 1635), (992, 1715)), 'Casi siempre': ((1007, 1636), (1121, 1717)), 'Algunas veces': ((1132, 1638), (1247, 1718)), 'Casi nunca': ((1258, 1637), (1373, 1718)), 'Nunca': ((1383, 1639), (1497, 1717))}
}


# Coordenadas de la pregunta filtro en la parte superior de las páginas 9 
coordenadas_filtro_pagina_9 = {'SI':  ((1088, 664), (1177, 695)), 'NO': ((1087, 704), (1176, 734))}


# Lista de todas las coordenadas de páginas

coordenadas_paginas = [
    coordenadas_pagina_1,
    coordenadas_pagina_2,
    coordenadas_pagina_3,
    coordenadas_pagina_4,
    coordenadas_pagina_5,
    coordenadas_pagina_6,
    coordenadas_pagina_7,
    coordenadas_pagina_8,
    coordenadas_pagina_9,
 

]

# Lista para almacenar las imágenes con respuestas dibujadas
imagenes_con_respuestas = []
# Lista para almacenar las respuestas de todas las páginas
respuestas_totales = []

# Procesar cada página del PDF
for pagina_idx, imagen in enumerate(paginas):
    imagen_cv = cv2.cvtColor(np.array(imagen), cv2.COLOR_RGB2BGR)
    respuestas_pagina = []  # Lista para almacenar respuestas de esta página

    # Validar si es una página con filtro (páginas 9 )
    if pagina_idx == 8:  # Página 9
        es_si = verificar_si(imagen_cv, coordenadas_filtro_pagina_9, pagina_idx)
        if not es_si:
            print(f"Página {pagina_idx + 1} omitida: Respuesta filtro 'NO'")
            continue  # Saltar esta página si el filtro es "NO"
        print(f"Página {pagina_idx + 1} procesada: Respuesta filtro 'SI'")
   
    # Obtener las coordenadas para la página actual
    if pagina_idx < len(coordenadas_paginas):
        coordenadas_actual = coordenadas_paginas[pagina_idx]
    else:
        print(f"Página {pagina_idx + 1}: No hay coordenadas definidas.")
        continue
# Procesar cada página del PDF
for pagina_idx, imagen in enumerate(paginas):
    imagen_cv = cv2.cvtColor(np.array(imagen), cv2.COLOR_RGB2BGR)
    respuestas_pagina = []  # Lista para almacenar respuestas de esta página

    # Validar si es una página con filtro (solo página 9)
    if pagina_idx == 8:  # Página 9
        es_si = verificar_si(imagen_cv, coordenadas_filtro_pagina_9, pagina_idx)
        if not es_si:
            print(f"Página {pagina_idx + 1} omitida: Respuesta filtro 'NO'")
            continue  # Saltar esta página si el filtro es "NO"
        print(f"Página {pagina_idx + 1} procesada: Respuesta filtro 'SI'")

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

def obtener_respuestas_procesadas1():
    respuestas_procesadas1 = {}
    for pagina_respuestas in respuestas_totales:
        lineas = pagina_respuestas.split("\n")
        for linea in lineas:
            if "Pregunta" in linea:
                partes = linea.split(":")
                pregunta = int(partes[0].replace("Pregunta", "").strip())
                respuesta = partes[1].strip()
                respuestas_procesadas1[pregunta] = respuesta
    return respuestas_procesadas1

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
