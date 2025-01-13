from pdf2image import convert_from_path
import cv2
import numpy as np
import os
from rutas import ruta_pdf_cuestionario_A

# Ruta completa de poppler
poppler_path = r'C:\Users\practicante.rrhh\Desktop\poppler-24.08.0\Library\bin'

# Rutas principales
directorio_base = r'C:\Users\practicante.rrhh\Desktop\cuestio_extralab'
directorio_plantillas = os.path.join(directorio_base, 'plantillas')
ruta_pdf_referencia = os.path.join(directorio_base, 'ref.pdf')

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
ruta_pdf_cuestionario = ruta_pdf_cuestionario_A
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
   1: {'Siempre': ((884, 737), (990, 798)), 'Casi siempre': ((1009, 738), (1116, 796)), 'Algunas veces': ((1129, 738), (1239, 801)), 'Casi nunca': ((1254, 738), (1357, 799)), 'Nunca': ((1378, 738), (1483, 801))},
2: {'Siempre': ((885, 816), (985, 866)), 'Casi siempre': ((1007, 818), (1111, 866)), 'Algunas veces': ((1133, 819), (1235, 867)), 'Casi nunca': ((1254, 817), (1358, 865)), 'Nunca': ((1381, 817), (1483, 868))},
3: {'Siempre': ((885, 886), (991, 962)), 'Casi siempre': ((1011, 887), (1116, 958)), 'Algunas veces': ((1133, 886), (1238, 959)), 'Casi nunca': ((1256, 887), (1362, 963)), 'Nunca': ((1383, 887), (1484, 959))},
4: {'Siempre': ((884, 981), (992, 1048)), 'Casi siempre': ((1013, 983), (1114, 1047)), 'Algunas veces': ((1134, 979), (1236, 1045)), 'Casi nunca': ((1256, 978), (1359, 1048)), 'Nunca': ((1379, 981), (1485, 1052))},
5: {'Siempre': ((882, 1068), (992, 1114)), 'Casi siempre': ((1013, 1068), (1117, 1117)), 'Algunas veces': ((1132, 1065), (1240, 1116)), 'Casi nunca': ((1257, 1069), (1362, 1114)), 'Nunca': ((1377, 1065), (1487, 1117))},
6: {'Siempre': ((881, 1132), (989, 1180)), 'Casi siempre': ((1006, 1133), (1114, 1179)), 'Algunas veces': ((1130, 1134), (1234, 1180)), 'Casi nunca': ((1259, 1135), (1361, 1181)), 'Nunca': ((1381, 1135), (1481, 1181))},
7: {'Siempre': ((882, 1199), (988, 1294)), 'Casi siempre': ((1010, 1199), (1110, 1294)), 'Algunas veces': ((1137, 1200), (1238, 1298)), 'Casi nunca': ((1260, 1202), (1364, 1297)), 'Nunca': ((1385, 1205), (1484, 1295))},
8: {'Siempre': ((887, 1321), (982, 1387)), 'Casi siempre': ((1012, 1320), (1112, 1385)), 'Algunas veces': ((1135, 1318), (1236, 1385)), 'Casi nunca': ((1260, 1322), (1359, 1385)), 'Nunca': ((1384, 1321), (1480, 1386))},
9: {'Siempre': ((881, 1409), (991, 1478)), 'Casi siempre': ((1011, 1408), (1113, 1478)), 'Algunas veces': ((1130, 1408), (1235, 1475)), 'Casi nunca': ((1258, 1406), (1360, 1471)), 'Nunca': ((1380, 1409), (1481, 1479))},
10: {'Siempre': ((877, 1496), (988, 1604)), 'Casi siempre': ((1009, 1496), (1112, 1601)), 'Algunas veces': ((1133, 1499), (1235, 1597)), 'Casi nunca': ((1255, 1500), (1359, 1598)), 'Nunca': ((1381, 1497), (1486, 1595))},
11: {'Siempre': ((884, 1622), (992, 1668)), 'Casi siempre': ((1010, 1623), (1107, 1672)), 'Algunas veces': ((1134, 1620), (1238, 1665)), 'Casi nunca': ((1254, 1623), (1361, 1672)), 'Nunca': ((1382, 1626), (1485, 1668))},
12: {'Siempre': ((880, 1692), (988, 1756)), 'Casi siempre': ((1009, 1692), (1115, 1756)), 'Algunas veces': ((1128, 1690), (1238, 1757)), 'Casi nunca': ((1260, 1690), (1362, 1756)), 'Nunca': ((1380, 1690), (1486, 1754))}
}

coordenadas_pagina_2 = {
     13: {'Siempre': ((872, 644), (984, 722)), 'Casi siempre': ((1000, 646), (1108, 722)), 'Algunas veces': ((1122, 645), (1232, 721)), 'Casi nunca': ((1245, 645), (1359, 720)), 'Nunca': ((1372, 644), (1484, 721))},
    14: {'Siempre': ((872, 735), (985, 808)), 'Casi siempre': ((998, 734), (1110, 809)), 'Algunas veces': ((1122, 735), (1234, 810)), 'Casi nunca': ((1245, 736), (1356, 806)), 'Nunca': ((1371, 735), (1481, 805))},
    15: {'Siempre': ((872, 824), (988, 897)), 'Casi siempre': ((1001, 825), (1108, 893)), 'Algunas veces': ((1120, 823), (1233, 896)), 'Casi nunca': ((1247, 825), (1357, 896)), 'Nunca': ((1371, 825), (1483, 899))},
    16: {'Siempre': ((872, 1149), (986, 1224)), 'Casi siempre': ((1000, 1153), (1107, 1222)), 'Algunas veces': ((1121, 1149), (1234, 1223)), 'Casi nunca': ((1249, 1152), (1356, 1220)), 'Nunca': ((1370, 1150), (1481, 1222))},
    17: {'Siempre': ((872, 1239), (983, 1310)), 'Casi siempre': ((1001, 1237), (1108, 1309)), 'Algunas veces': ((1121, 1237), (1230, 1309)), 'Casi nunca': ((1247, 1237), (1359, 1311)), 'Nunca': ((1373, 1240), (1480, 1310))},
    18: {'Siempre': ((874, 1326), (986, 1398)), 'Casi siempre': ((999, 1324), (1110, 1400)), 'Algunas veces': ((1122, 1322), (1231, 1400)), 'Casi nunca': ((1245, 1326), (1354, 1395)), 'Nunca': ((1371, 1325), (1477, 1400))},
    19: {'Siempre': ((872, 1412), (983, 1486)), 'Casi siempre': ((999, 1414), (1106, 1487)), 'Algunas veces': ((1125, 1414), (1231, 1488)), 'Casi nunca': ((1245, 1414), (1356, 1490)), 'Nunca': ((1373, 1416), (1482, 1491))},
    20: {'Siempre': ((872, 1503), (983, 1578)), 'Casi siempre': ((1000, 1502), (1110, 1577)), 'Algunas veces': ((1123, 1502), (1233, 1579)), 'Casi nunca': ((1246, 1504), (1358, 1579)), 'Nunca': ((1371, 1504), (1480, 1576))},
    21: {'Siempre': ((872, 1595), (987, 1668)), 'Casi siempre': ((1001, 1593), (1109, 1667)), 'Algunas veces': ((1122, 1591), (1231, 1667)), 'Casi nunca': ((1246, 1595), (1354, 1669)), 'Nunca': ((1370, 1593), (1478, 1667))},
    22: {'Siempre': ((870, 1913), (984, 1990)), 'Casi siempre': ((998, 1913), (1106, 1989)), 'Algunas veces': ((1122, 1914), (1232, 1989)), 'Casi nunca': ((1244, 1911), (1357, 1988)), 'Nunca': ((1371, 1914), (1484, 1990))},
    23: {'Siempre': ((870, 2002), (980, 2077)), 'Casi siempre': ((997, 2004), (1107, 2078)), 'Algunas veces': ((1122, 2004), (1231, 2080)), 'Casi nunca': ((1245, 2003), (1357, 2081)), 'Nunca': ((1372, 2006), (1481, 2081))}
    
}

coordenadas_pagina_3 = {
   24: {'Siempre': ((881, 500), (1000, 577)), 'Casi siempre': ((1009, 500), (1122, 577)), 'Algunas veces': ((1135, 501), (1249, 578)), 'Casi nunca': ((1260, 500), (1376, 579)), 'Nunca': ((1384, 499), (1502, 579))},
   25: {'Siempre': ((881, 587), (999, 665)), 'Casi siempre': ((1010, 589), (1121, 666)), 'Algunas veces': ((1137, 589), (1248, 666)), 'Casi nunca': ((1261, 590), (1368, 667)), 'Nunca': ((1387, 593), (1493, 666))},
   26: {'Siempre': ((881, 678), (999, 754)), 'Casi siempre': ((1012, 681), (1120, 752)), 'Algunas veces': ((1134, 676), (1248, 751)), 'Casi nunca': ((1259, 678), (1372, 756)), 'Nunca': ((1386, 681), (1497, 757))},
    27: {'Siempre': ((882, 766), (997, 829)), 'Casi siempre': ((1009, 766), (1125, 831)), 'Algunas veces': ((1133, 768), (1247, 832)), 'Casi nunca': ((1261, 767), (1372, 831)), 'Nunca': ((1388, 771), (1501, 833))},
    28: {'Siempre': ((881, 841), (998, 919)), 'Casi siempre': ((1008, 844), (1123, 921)), 'Algunas veces': ((1134, 845), (1246, 919)), 'Casi nunca': ((1257, 844), (1373, 920)), 'Nunca': ((1385, 846), (1498, 920))},
    29: {'Siempre': ((882, 933), (998, 1046)), 'Casi siempre': ((1010, 933), (1121, 1047)), 'Algunas veces': ((1136, 933), (1247, 1044)), 'Casi nunca': ((1261, 934), (1371, 1045)), 'Nunca': ((1385, 934), (1497, 1046))},
    30: {'Siempre': ((883, 1058), (998, 1160)), 'Casi siempre': ((1009, 1058), (1124, 1162)), 'Algunas veces': ((1138, 1061), (1247, 1155)), 'Casi nunca': ((1259, 1059), (1372, 1158)), 'Nunca': ((1385, 1059), (1491, 1157))},
    31: {'Siempre': ((857, 1393), (980, 1448)), 'Casi siempre': ((992, 1395), (1110, 1448)), 'Algunas veces': ((1122, 1394), (1242, 1448)), 'Casi nunca': ((1256, 1395), (1365, 1448)), 'Nunca': ((1379, 1395), (1491, 1451))},
    32: {'Siempre': ((854, 1458), (979, 1534)), 'Casi siempre': ((991, 1459), (1113, 1535)), 'Algunas veces': ((1126, 1463), (1241, 1535)), 'Casi nunca': ((1256, 1464), (1363, 1534)), 'Nunca': ((1379, 1459), (1490, 1535))},
    33: {'Siempre': ((855, 1547), (981, 1624)), 'Casi siempre': ((992, 1549), (1109, 1623)), 'Algunas veces': ((1124, 1549), (1243, 1624)), 'Casi nunca': ((1257, 1550), (1360, 1620)), 'Nunca': ((1379, 1550), (1486, 1624))},
    34: {'Siempre': ((855, 1637), (979, 1714)), 'Casi siempre': ((994, 1640), (1109, 1713)), 'Algunas veces': ((1124, 1639), (1244, 1715)), 'Casi nunca': ((1259, 1641), (1360, 1712)), 'Nunca': ((1380, 1641), (1489, 1714))},
    35: {'Siempre': ((854, 1728), (975, 1802)), 'Casi siempre': ((991, 1729), (1106, 1803)), 'Algunas veces': ((1127, 1729), (1243, 1803)), 'Casi nunca': ((1255, 1732), (1364, 1805)), 'Nunca': ((1380, 1730), (1485, 1806))},
    36: {'Siempre': ((860, 1820), (980, 1893)), 'Casi siempre': ((994, 1820), (1111, 1892)), 'Algunas veces': ((1126, 1818), (1241, 1891)), 'Casi nunca': ((1255, 1819), (1364, 1894)), 'Nunca': ((1380, 1819), (1488, 1894))},
    37: {'Siempre': ((856, 1906), (975, 1980)), 'Casi siempre': ((992, 1907), (1109, 1979)), 'Algunas veces': ((1123, 1905), (1241, 1983)), 'Casi nunca': ((1254, 1906), (1367, 1984)), 'Nunca': ((1379, 1909), (1487, 1982))},
    38: {'Siempre': ((854, 1997), (978, 2066)), 'Casi siempre': ((993, 1996), (1110, 2069)), 'Algunas veces': ((1125, 1998), (1239, 2068)), 'Casi nunca': ((1254, 1998), (1362, 2064)), 'Nunca': ((1383, 1998), (1483, 2069))}
}

coordenadas_pagina_4 ={
39: {'Siempre': ((845, 618), (969, 696)), 'Casi siempre': ((985, 621), (1098, 696)), 'Algunas veces': ((1112, 624), (1231, 694)), 'Casi nunca': ((1243, 621), (1351, 695)), 'Nunca': ((1366, 619), (1480, 697))},
40: {'Siempre': ((848, 708), (971, 786)), 'Casi siempre': ((981, 708), (1100, 785)), 'Algunas veces': ((1111, 709), (1230, 786)), 'Casi nunca': ((1244, 710), (1355, 787)), 'Nunca': ((1367, 711), (1479, 787))},
41: {'Siempre': ((847, 799), (970, 871)), 'Casi siempre': ((983, 799), (1099, 871)), 'Algunas veces': ((1113, 801), (1231, 873)), 'Casi nunca': ((1245, 801), (1355, 875)), 'Nunca': ((1367, 801), (1481, 873))},
42: {'Siempre': ((845, 885), (970, 962)), 'Casi siempre': ((983, 886), (1100, 963)), 'Algunas veces': ((1114, 885), (1231, 961)), 'Casi nunca': ((1245, 886), (1353, 960)), 'Nunca': ((1368, 885), (1481, 962))},
43: {'Siempre': ((847, 974), (970, 1029)), 'Casi siempre': ((983,974), (1101 ,1029)), 'Algunas veces': ((1112 ,975),(1232 ,1028)), 'Casi nunca' :((1244 ,976),(1355 ,1029)), 'Nunca' :((1367 ,974),(1478 ,1029))},
44: {'Siempre': ((847 ,1043),(972 ,1116)), 'Casi siempre' :((982 ,1044),(1099 ,1114)), 'Algunas veces' :((1112 ,1042),(1230 ,1114)), 'Casi nunca' :((1246 ,1043),(1353 ,1113)), 'Nunca' :((1369 ,1045),(1480 ,1116))},
45: {'Siempre': ((849 ,1129),(972 ,1204)), 'Casi siempre' :((984 ,1128),(1098 ,1203)), 'Algunas veces' :((1113 ,1129),(1231 ,1204)), 'Casi nunca' :((1244 ,1129),(1353 ,1206)), 'Nunca' :((1365, 1122), (1476, 1197))},
46: {'Siempre': ((848 ,1219),(970 ,1294)), 'Casi siempre' :((984 ,1219),(1101 ,1293)), 'Algunas veces' :((1112 ,1217),(1232 ,1293)), 'Casi nunca' :((1243 ,1219),(1353 ,1291)), 'Nunca' :((1369 ,1222),(1478 ,1294))},
47: {'Siempre': ((850 ,1309),(969 ,1381)), 'Casi siempre' :((985 ,1307),(1102 ,1381)), 'Algunas veces' :((1115 ,1305),(1233 ,1381)), 'Casi nunca' :((1247 ,1308),(1356 ,1381)), 'Nunca' :((1367 ,1308),(1478 ,1379))},
48: {'Siempre': ((866 ,1633),(977 ,1709)), 'Casi siempre' :((995 ,1633),(1103 ,1707)), 'Algunas veces' :((1119 ,1635),(1226 ,1709)), 'Casi nunca' :((1242 ,1634),(1353 ,1708)), 'Nunca' :((1368 ,1635),(1476 ,1710))},
49: {'Siempre': ((865 ,1723),(979 ,1795)), 'Casi siempre' :((991 ,1725),(1101 ,1792)), 'Algunas veces' :((1117 ,1724),(1226 ,1794)), 'Casi nunca' :((1243 ,1725),(1351 ,1794)), 'Nunca' :((1366 ,1724),(1476 ,1794))},
50: {'Siempre': ((865 ,1809),(978 ,1882)), 'Casi siempre' :((992 ,1808),(1103 ,1885)), 'Algunas veces' :((1117 ,1811),(1228 ,1885)), 'Casi nunca' :((1241 ,1809),(1355 ,1884)), 'Nunca' :((1369 ,1810),(1478 ,1884))},
51: {'Siempre': ((865,1898), (979,2002)), 'Casi siempre': ((994,1897), (1100,2001)), 'Algunas veces': ((1117,1899), (1228,2000)), 'Casi nunca': ((1245,1901), (1351,2001)), 'Nunca': ((1367,1899), (1476,2001))},
52: {'Siempre': ((861, 2011), (975, 2090)), 'Casi siempre': ((988, 2013), (1099, 2089)), 'Algunas veces': ((1113, 2013), (1223, 2090)), 'Casi nunca': ((1238, 2015), (1349, 2089)), 'Nunca': ((1361, 2014), (1477, 2090))},
}


coordenadas_pagina_5 ={
    53: {'Siempre': ((857, 655), (983, 733)), 'Casi siempre': ((995, 656), (1112, 734)), 'Algunas veces': ((1127, 655), (1246, 736)), 'Casi nunca': ((1261, 659), (1372, 734)), 'Nunca': ((1381, 657), (1494, 734))},
54: {'Siempre': ((859, 744), (982, 823)), 'Casi siempre': ((998, 746), (1115, 825)), 'Algunas veces': ((1127, 746), (1249, 823)), 'Casi nunca': ((1260, 750), (1372, 825)), 'Nunca': ((1386, 749), (1495, 825))},
55: {'Siempre': ((859, 834), (980, 906)), 'Casi siempre': ((997, 836), (1111, 911)), 'Algunas veces': ((1126, 836), (1248, 912)), 'Casi nunca': ((1258, 837), (1373, 911)), 'Nunca': ((1384, 838), (1493, 910))},
56: {'Siempre': ((859, 924), (979, 995)), 'Casi siempre': ((995, 924), (1111, 998)), 'Algunas veces': ((1127, 924), (1249, 1001)), 'Casi nunca': ((1260, 924), (1371, 1000)), 'Nunca': ((1383, 926), (1495, 998))},
57: {'Siempre': ((858, 1012), (982, 1085)), 'Casi siempre': ((997, 1011), (1113, 1086)), 'Algunas veces': ((1127, 1012), (1244, 1088)), 'Casi nunca': ((1258, 1011), (1366, 1087)), 'Nunca': ((1383, 1014), (1492, 1086))},
58: {'Siempre': ((859, 1098), (984, 1172)), 'Casi siempre': ((994, 1100), (1109, 1175)), 'Algunas veces': ((1125, 1100), (1244, 1176)), 'Casi nunca': ((1257, 1100), (1368, 1173)), 'Nunca': ((1382, 1101), (1494, 1176))},
59: {'Siempre': ((857, 1187), (983, 1262)), 'Casi siempre': ((994, 1188), (1112,1266)), 'Algunas veces': ((1126 ,1189),(1244 ,1264)), 'Casi nunca' :((1260 ,1191),(1367 ,1265)), 'Nunca' :((1382 ,1188),(1496 ,1266))},
60: {'Siempre': ((876 ,1591),(989 ,1689)), 'Casi siempre' :((1002 ,1592),(1114 ,1690)), 'Algunas veces' :((1127 ,1593),(1237 ,1692)), 'Casi nunca' :((1253 ,1594),(1366 ,1690)), 'Nunca' :((1379 ,1593),(1491 ,1693))},
61: {'Siempre': ((876 ,1703),(990 ,1782)), 'Casi siempre' :((1003 ,1703),(1115 ,1782)), 'Algunas veces' :((1127 ,1705),(1236 ,1784)), 'Casi nunca' :((1252 ,1706),(1366 ,1784)), 'Nunca' :((1378 ,1704),(1486 ,1784))},
62: {'Siempre': ((874 ,1795),(991 ,1871)), 'Casi siempre' :((1002 ,1796),(1113 ,1871)), 'Algunas veces' :((1127 ,1797),(1238 ,1873)), 'Casi nunca' :((1252 ,1799),(1364 ,1874)), 'Nunca' :((1378 ,1799),(1484 ,1872))},
}


coordenadas_pagina_6 ={
63: {'Siempre': ((842, 690), (966, 744)), 'Casi siempre': ((980, 689), (1094, 742)), 'Algunas veces': ((1106, 688), (1225, 743)), 'Casi nunca': ((1239, 692), (1352, 746)), 'Nunca': ((1360, 692), (1472, 743))},
64: {'Siempre': ((842, 757), (967, 812)), 'Casi siempre': ((980, 757), (1095, 810)), 'Algunas veces': ((1110, 758), (1226, 811)), 'Casi nunca': ((1239, 758), (1351, 813)), 'Nunca': ((1363, 758), (1475, 812))},
65: {'Siempre': ((842, 823), (968, 902)), 'Casi siempre': ((977, 824), (1093, 901)), 'Algunas veces': ((1109, 825), (1225, 900)), 'Casi nunca': ((1237, 824), (1353, 899)), 'Nunca': ((1368, 829), (1474, 900))},
66: {'Siempre': ((842, 915), (965, 982)), 'Casi siempre': ((977, 913), (1098, 984)), 'Algunas veces': ((1109, 912), (1225, 984)), 'Casi nunca': ((1239, 914), (1352, 983)), 'Nunca': ((1364, 914), (1477, 982))},
67: {'Siempre': ((842, 995), (967, 1065)), 'Casi siempre': ((979, 994), (1097, 1063)), 'Algunas veces': ((1110, 995), (1227, 1064)), 'Casi nunca': ((1240, 995), (1352, 1063)), 'Nunca': ((1362, 995), (1476, 1063))},
68: {'Siempre': ((841, 1076), (967, 1144)), 'Casi siempre': ((979, 1076), (1096, 1144)), 'Algunas veces': ((1108, 1078), (1225, 1142)), 'Casi nunca': ((1240, 1078), (1351, 1144)), 'Nunca': ((1362, 1077), (1477, 1146))},
69: {'Siempre': ((843,1157),(967 ,1234)), 'Casi siempre' :((980 ,1157),(1096 ,1234)), 'Algunas veces' :((1109 ,1157),(1227 ,1235)), 'Casi nunca' :((1242 ,1157),(1352 ,1235)), 'Nunca' :((1365 ,1158),(1473 ,1231))},
70: {'Siempre': ((841 ,1245),(967 ,1301)), 'Casi siempre' :((977 ,1246),(1098 ,1301)), 'Algunas veces' :((1111 ,1248),(1227 ,1302)), 'Casi nunca' :((1241 ,1247),(1349 ,1300)), 'Nunca' :((1365 ,1248),(1476 ,1299))},
71: {'Siempre': ((843 ,1313),(968 ,1378)), 'Casi siempre' :((980 ,1315),(1095 ,1377)), 'Algunas veces' :((1111 ,1315),(1229 ,1376)), 'Casi nunca' :((1242 ,1314),(1348 ,1378)), 'Nunca' :((1366 ,1316),(1469 ,1376))},
72: {'Siempre': ((843 ,1391),(965 ,1468)), 'Casi siempre' :((979 ,1392),(1096 ,1465)), 'Algunas veces' :((1112 ,1393),(1229 ,1469)), 'Casi nunca' :((1243 ,1392),(1349 ,1466)), 'Nunca' :((1365 ,1393),(1475 ,1468))},
73: {'Siempre': ((844 ,1481),(966 ,1534)), 'Casi siempre' :((979 ,1480),(1092 ,1533)), 'Algunas veces' :((1110 ,1483),(1227 ,1536)), 'Casi nunca' :((1241 ,1481),(1350 ,1535)), 'Nunca' :((1364 ,1481),(1475 ,1537))},
74: {'Siempre': ((845, 1548), (963, 1619)), 'Casi siempre' :((982, 1548), (1095, 1621)), 'Algunas veces' : ((1112, 1547), (1224, 1622)), 'Casi nunca' :((1245, 1549), (1350, 1622)), 'Nunca' :((1370, 1546), (1475, 1623))},
75: {'Siempre': ((840, 1642), (962, 1714)), 'Casi siempre' :((976, 1643), (1093, 1715)), 'Algunas veces' :((1107, 1644), (1224, 1715)), 'Casi nunca' :((1237, 1645), (1345, 1715)), 'Nunca' : ((1361, 1643), (1471, 1715))},
}


coordenadas_pagina_7 = {
76: {'Siempre': ((857, 626), (978, 694)), 'Casi siempre': ((993, 628), (1111, 698)), 'Algunas veces': ((1122, 627), (1240, 698)), 'Casi nunca': ((1254, 628), (1364, 696)), 'Nunca': ((1375, 628), (1486, 697))},
77: {'Siempre': ((854, 707), (983, 786)), 'Casi siempre': ((994, 707), (1109, 782)), 'Algunas veces': ((1122, 708), (1243, 786)), 'Casi nunca': ((1255, 709), (1364, 787)), 'Nunca': ((1378, 710), (1486, 788))},
78: {'Siempre': ((853, 797), (981, 874)), 'Casi siempre': ((992, 797), (1110, 872)), 'Algunas veces': ((1123, 797), (1237, 873)), 'Casi nunca': ((1256, 796), (1363, 871)), 'Nunca': ((1375, 797), (1487, 875))},
79: {'Siempre': ((854, 884), (977, 962)), 'Casi siempre': ((991, 886), (1107, 963)), 'Algunas veces': ((1121, 885), (1241, 962)), 'Casi nunca': ((1254, 887), (1364, 963)), 'Nunca': ((1375, 887), (1485, 965))},
80: {'Siempre': ((854, 973), (979, 1051)), 'Casi siempre': ((994, 973), (1109, 1050)), 'Algunas veces': ((1120, 974), (1238, 1051)), 'Casi nunca': ((1252, 975), (1361, 1051)), 'Nunca': ((1376, 976), (1485, 1052))},
81: {'Siempre': ((855, 1063), (979, 1138)), 'Casi siempre': ((991, 1062), (1109, 1137)), 'Algunas veces': ((1121, 1063), (1242, 1139)), 'Casi nunca': ((1253, 1065), (1359, 1139)), 'Nunca': ((1377, 1064), (1483, 1135))},
82: {'Siempre': ((855, 1149), (976,1226)), 'Casi siempre':((991 ,1151),(1107 ,1226)), 'Algunas veces' :((1120 ,1148),(1240 ,1226)), 'Casi nunca' :((1253 ,1150),(1365 ,1226)), 'Nunca' :((1376 ,1152),(1486 ,1228))},
83: {'Siempre': ((855 ,1238),(977 ,1315)), 'Casi siempre' :((991 ,1238),(1109 ,1316)), 'Algunas veces' :((1121 ,1238),(1240 ,1316)), 'Casi nunca' :((1254 ,1241),(1361 ,1315)), 'Nunca' :((1375 ,1239),(1485 ,1317))},
84: {'Siempre': ((853 ,1327),(980 ,1402)), 'Casi siempre' :((992 ,1328),(1105 ,1405)), 'Algunas veces' :((1121 ,1327),(1237 ,1403)), 'Casi nunca' :((1253 ,1329),(1360 ,1405)), 'Nunca' :((1373 ,1329),(1481 ,1405))},
85: {'Siempre': ((854 ,1416),(980 ,1488)), 'Casi siempre' :((992 ,1417),(1110 ,1493)), 'Algunas veces' :((1121 ,1418),(1238 ,1494)), 'Casi nunca' :((1252 ,1418),(1361 ,1494)), 'Nunca' :((1375 ,1418),(1482 ,1494))},
86: {'Siempre': ((853 ,1507),(979 ,1581)), 'Casi siempre' :((992 ,1506),(1108 ,1581)), 'Algunas veces' :((1124 ,1506),(1239 ,1583)), 'Casi nunca' :((1255 ,1507),(1362 ,1582)), 'Nunca' :((1374 ,1508),(1481 ,1585))},
87: {'Siempre': ((854 ,1593),(977 ,1671)), 'Casi siempre' :((990 ,1593),(1108 ,1669)), 'Algunas veces' :((1120 ,1595),(1236 ,1670)), 'Casi nunca' :((1253 ,1594),(1363 ,1670)), 'Nunca' :((1376 ,1598),(1482 ,1672))},
88: {'Siempre': ((853 ,1683),(975 ,1758)), 'Casi siempre' :((991 ,1683),(1106 ,1760)), 'Algunas veces' :((1121 ,1685),(1240 ,1758)), 'Casi nunca' :((1254 ,1687),(1360 ,1759)), 'Nunca' :((1374 ,1685),(1483 ,1757))},
89: {'Siempre': ((853 ,1772),(979 ,1848)), 'Casi siempre' :((991 ,1774),(1107 ,1850)), 'Algunas veces' :((1120 ,1774),(1236 ,1850)), 'Casi nunca' :((1251 ,1773),(1362 ,1851)), 'Nunca' :((1374 ,1776),(1485 ,1850))},
}


coordenadas_pagina_8 = {
90: {'Siempre': ((846, 597), (972, 677)), 'Casi siempre': ((983, 597), (1100, 675)), 'Algunas veces': ((1114, 600), (1233, 677)), 'Casi nunca': ((1245, 598), (1359, 677)), 'Nunca': ((1370, 598), (1481, 677))},
91: {'Siempre': ((847, 688), (972, 767)), 'Casi siempre': ((982, 689), (1101, 768)), 'Algunas veces': ((1114, 689), (1233, 766)), 'Casi nunca': ((1246, 690), (1357, 767)), 'Nunca': ((1371, 689), (1481, 766))},
92: {'Siempre': ((846, 779), (968, 855)), 'Casi siempre': ((983, 778), (1101, 853)), 'Algunas veces': ((1114, 779), (1231, 855)), 'Casi nunca': ((1245, 780), (1357, 854)), 'Nunca': ((1370, 779), (1482, 856))},
93: {'Siempre': ((847, 868), (972, 945)), 'Casi siempre': ((984, 869), (1101, 945)), 'Algunas veces': ((1115, 867), (1234, 945)), 'Casi nunca': ((1247, 869), (1359, 945)), 'Nunca': ((1368, 870), (1481, 946))},
94: {'Siempre': ((846, 959), (970, 1032)), 'Casi siempre': ((984, 960), (1101, 1032)), 'Algunas veces': ((1115, 959), (1233, 1032)), 'Casi nunca': ((1246, 956), (1356, 1032)), 'Nunca': ((1371, 959), (1481, 1033))},
95: {'Siempre': ((870 ,1239),(985 ,1295)), 'Casi siempre' :((996 ,1240),(1108 ,1296)), 'Algunas veces' :((1122 ,1240),(1232 ,1296)), 'Casi nunca' :((1244 ,1241),(1357 ,1297)), 'Nunca' :((1370 ,1241),(1484 ,1294))},
96: {'Siempre': ((869 ,1308),(985 ,1382)), 'Casi siempre' :((997 ,1308),(1110 ,1382)), 'Algunas veces' :((1121 ,1308),(1233 ,1383)), 'Casi nunca' :((1243 ,1307),(1358 ,1383)), 'Nunca' :((1369 ,1308),(1483 ,1382))},
97: {'Siempre': ((869 ,1393),(987 ,1474)), 'Casi siempre' :((999 ,1395),(1108 ,1470)), 'Algunas veces' :((1121 ,1394),(1231 ,1472)), 'Casi nunca' :((1243 ,1396),(1356 ,1472)), 'Nunca' :((1369 ,1397),(1485 ,1470))},
98: {'Siempre': ((872 ,1485),(983 ,1561)), 'Casi siempre' :((999 ,1485),(1106 ,1558)), 'Algunas veces' :((1121 ,1485),(1232 ,1559)), 'Casi nunca' :((1242 ,1484),(1356 ,1560)), 'Nunca' :((1370 ,1486),(1480 ,1558))},
99: {'Siempre': ((873 ,1573),(986 ,1643)), 'Casi siempre' :((997 ,1575),(1110 ,1641)), 'Algunas veces' :((1121 ,1573),(1234 ,1642)), 'Casi nunca' :((1246 ,1575),(1356 ,1642)), 'Nunca' :((1370 ,1575),(1482 ,1641))},
100: {'Siempre': ((870 ,1655),(986 ,1732)), 'Casi siempre' :((998 ,1656),(1111 ,1730)), 'Algunas veces' :((1122 ,1656),(1233 ,1730)), 'Casi nunca' :((1245 ,1656),(1359 ,1732)), 'Nunca' :((1370 ,1656),(1478 ,1730))},
101: {'Siempre': ((870 ,1745),(984 ,1820)), 'Casi siempre' :((997 ,1743),(1108 ,1819)), 'Algunas veces' :((1122 ,1745),(1232 ,1820)), 'Casi nunca' :((1246 ,1747),(1357 ,1820)), 'Nunca' :((1368 ,1745),(1483 ,1821))},
102: {'Siempre': ((869,1832), (987,1888)), 'Casi siempre': ((997,1834), (1110,1886)), 'Algunas veces': ((1121,1834), (1232,1885)), 'Casi nunca': ((1243,1834), (1356,1888)), 'Nunca': ((1369,1835), (1479,1887))},
103: {'Siempre': ((870,1900), (985,1955)), 'Casi siempre': ((997,1902), (1108,1955)), 'Algunas veces': ((1121,1901), (1229,1954)), 'Casi nunca': ((1247,1902), (1355,1954)), 'Nunca': ((1372,1901), (1482,1956))},
104: {'Siempre': ((869,1969), (982,2052)), 'Casi siempre': ((999,1970), (1109,2051)), 'Algunas veces': ((1122,1970), (1229,2047)), 'Casi nunca': ((1246,1970), (1355,2050)), 'Nunca': ((1370,1969), (1481,2051))},
105: {'Siempre': ((870,2065),(986,2137)),'Casi siempre':((999,2065),(1108,2136)),'Algunas veces':((1123,2065),(1234,2134)),'Casi nunca':((1245,2065),(1359,2136)),'Nunca':((1370,2066),(1483,2134))},
}

coordenadas_pagina_9 = {
106: {'Siempre': ((866, 933), (987, 992)), 'Casi siempre': ((995, 935), (1111, 992)), 'Algunas veces': ((1121, 935), (1236, 993)), 'Casi nunca': ((1247, 935), (1362, 993)), 'Nunca': ((1372, 936), (1487, 992))},
107: {'Siempre': ((867, 1001), (986, 1088)), 'Casi siempre': ((996, 1001), (1111, 1090)), 'Algunas veces': ((1120, 1002), (1234, 1088)), 'Casi nunca': ((1246, 1003), (1361, 1090)), 'Nunca': ((1370, 1003), (1486, 1089))},
108: {'Siempre': ((867, 1099), (986, 1156)), 'Casi siempre': ((996, 1098), (1110, 1155)), 'Algunas veces': ((1120, 1098), (1236, 1156)), 'Casi nunca': ((1245, 1100), (1360, 1156)), 'Nunca': ((1369, 1100), (1483, 1156))},
109: {'Siempre': ((870, 1167), (985, 1243)), 'Casi siempre': ((996, 1165), (1111, 1243)), 'Algunas veces': ((1121, 1165), (1235, 1243)), 'Casi nunca': ((1245, 1165), (1359, 1243)), 'Nunca': ((1371, 1166), (1484, 1244))},
110: {'Siempre': ((868, 1253), (986, 1333)), 'Casi siempre': ((995, 1252), (1112, 1333)), 'Algunas veces': ((1121, 1253), (1235, 1331)), 'Casi nunca': ((1246, 1255), (1360, 1333)), 'Nunca': ((1370, 1253), (1485, 1335))},
111: {'Siempre': ((869, 1342), (985, 1398)), 'Casi siempre': ((995, 1342), (1110, 1397)), 'Algunas veces': ((1120, 1343), (1233, 1400)), 'Casi nunca': ((1246, 1343), (1361, 1400)), 'Nunca': ((1369, 1344), (1483, 1399))},
112: {'Siempre': ((867, 1407), (984, 1487)), 'Casi siempre': ((995, 1409), (1112, 1487)), 'Algunas veces': ((1120, 1408), (1235, 1487)), 'Casi nunca': ((1243, 1409), (1360, 1488)), 'Nunca': ((1370, 1410), (1485, 1489))},
113: {'Siempre': ((868, 1497), (985, 1577)), 'Casi siempre': ((995, 1497), (1111, 1575)), 'Algunas veces': ((1122, 1497), (1233, 1575)), 'Casi nunca': ((1245, 1497), (1360, 1575)), 'Nunca': ((1369, 1498), (1481, 1575))},
114: {'Siempre': ((868, 1587), (985, 1665)), 'Casi siempre': ((995, 1585), (1110, 1665)), 'Algunas veces': ((1120, 1586), (1235, 1665)), 'Casi nunca': ((1245, 1586), (1361, 1665)), 'Nunca': ((1369, 1588), (1485, 1667))}
}

coordenadas_pagina_10 = {
    115: {'Siempre': ((844, 1001), (964, 1077)), 'Casi siempre': ((972, 1000), (1087, 1077)), 'Algunas veces': ((1097, 999), (1211, 1077)), 'Casi nunca': ((1219, 998), (1362, 1074)), 'Nunca': ((1372, 1000), (1483, 1076))},
    116: {'Siempre': ((846, 1086), (962, 1167)), 'Casi siempre': ((971, 1086), (1088, 1164)), 'Algunas veces': ((1098, 1088), (1210, 1165)), 'Casi nunca': ((1221, 1086), (1360, 1165)), 'Nunca': ((1371, 1086), (1485, 1164))},
    117: {'Siempre': ((845, 1177), (965, 1254)), 'Casi siempre': ((973, 1178), (1088, 1253)), 'Algunas veces': ((1097, 1176), (1213, 1254)), 'Casi nunca': ((1224, 1176), (1360, 1252)), 'Nunca': ((1369, 1174), (1485, 1252))},
    118: {'Siempre': ((846, 1266), (963, 1344)), 'Casi siempre': ((973, 1264), (1088, 1343)), 'Algunas veces': ((1097, 1265), (1211, 1343)), 'Casi nunca': ((1221, 1263), (1359, 1341)), 'Nunca': ((1371, 1264), (1486, 1341))},
    119: {'Siempre': ((846, 1354), (964, 1432)), 'Casi siempre': ((975, 1355), (1089, 1429)), 'Algunas veces': ((1100, 1354), (1213, 1431)), 'Casi nunca': ((1224, 1352), (1361, 1430)), 'Nunca': ((1370, 1353), (1486, 1428))},
    120: {'Siempre': ((847, 1442), (964, 1521)), 'Casi siempre': ((974, 1441), (1089, 1521)), 'Algunas veces': ((1098, 1440), (1211, 1520)), 'Casi nunca': ((1224, 1440), (1361, 1521)), 'Nunca': ((1371, 1441), (1486, 1519))},
    121: {'Siempre': ((848, 1531), (964, 1611)), 'Casi siempre': ((975, 1532), (1088, 1612)), 'Algunas veces': ((1099, 1530), (1215, 1610)), 'Casi nunca': ((1223, 1531), (1362, 1610)), 'Nunca': ((1372, 1530), (1485, 1609))},
    122: {'Siempre': ((850, 1621), (965, 1700)), 'Casi siempre': ((976, 1622), (1089, 1699)), 'Algunas veces': ((1100, 1623), (1214, 1699)), 'Casi nunca': ((1224, 1620), (1362, 1699)), 'Nunca': ((1373, 1622), (1487, 1700))},
    123: {'Siempre': ((849, 1711), (965, 1787)), 'Casi siempre': ((975, 1709), (1089, 1787)), 'Algunas veces': ((1099, 1708), (1214, 1789)), 'Casi nunca': ((1225, 1709), (1363, 1787)), 'Nunca': ((1374, 1710), (1484, 1786))}
}

# Coordenadas de la pregunta filtro en la parte superior de las páginas 9 y 10
coordenadas_filtro_pagina_9 = {'SI': ((1072, 614), (1160, 644)), 'NO': ((1071, 653), (1159, 685))}
coordenadas_filtro_pagina_10 = {'SI': ((812, 536), (881, 568)), 'NO': ((811, 576), (881, 607))}


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
    coordenadas_pagina_10,

]

# Lista para almacenar las imágenes con respuestas dibujadas
imagenes_con_respuestas = []
# Lista para almacenar las respuestas de todas las páginas
respuestas_totales = []

# Procesar cada página del PDF

for pagina_idx, imagen in enumerate(paginas):
    imagen_cv = cv2.cvtColor(np.array(imagen), cv2.COLOR_RGB2BGR)
    respuestas_pagina = []  # Lista para almacenar respuestas de esta página

    # Validar si es una página con filtro (páginas 9 y 10)
    if pagina_idx == 8:  # Página 9
        es_si = verificar_si(imagen_cv, coordenadas_filtro_pagina_9, pagina_idx)
        if not es_si:
            print(f"Página {pagina_idx + 1} omitida: Respuesta filtro 'NO'")
            continue  # Saltar esta página si el filtro es "NO"
        print(f"Página {pagina_idx + 1} procesada: Respuesta filtro 'SI'")
    elif pagina_idx == 9:  # Página 10
        es_si = verificar_si(imagen_cv, coordenadas_filtro_pagina_10, pagina_idx)
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
    # Convertir la imagen a formato OpenCV
    imagen_cv = cv2.cvtColor(np.array(imagen), cv2.COLOR_RGB2BGR)
    respuestas_pagina = []  # Lista para almacenar respuestas de esta página

    # Validar si es una página con filtro (páginas 9 y 10)
    if pagina_idx == 8:  # Página 9
        es_si = verificar_si(imagen_cv, coordenadas_filtro_pagina_9, pagina_idx)
        if not es_si:
            print(f"Página {pagina_idx + 1} omitida: Respuesta filtro 'NO'")
            continue  # Saltar esta página si el filtro es "NO"
        print(f"Página {pagina_idx + 1} procesada: Respuesta filtro 'SI'")
    elif pagina_idx == 9:  # Página 10
        es_si = verificar_si(imagen_cv, coordenadas_filtro_pagina_10, pagina_idx)
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

def obtener_respuestas_procesadas():
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
