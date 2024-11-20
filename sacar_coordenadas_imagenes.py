import cv2
from pdf2image import convert_from_path
import numpy as np

# Función para crear el diccionario de preguntas y opciones dinámicamente
def crear_diccionario_preguntas(desde, hasta):
    diccionario = {}
    for i in range(desde, hasta + 1):
        diccionario[i] = {
            'Siempre': None,
            'Casi siempre': None,
            'Algunas veces': None,
            'Casi nunca': None,
            'Nunca': None
        }
    return diccionario

# Crear el diccionario para preguntas de tal a la tal
coordenadas_dict = crear_diccionario_preguntas(13, 23)

# Variables de desplazamiento y otros ajustes
desplazamiento_x = 0
desplazamiento_y = 0
scroll_step = 20  # Cuántos píxeles desplazarse con cada tecla

# Variables para la pregunta y opción actual
pregunta_actual = 13
opcion_actual = 'Siempre'  # Inicia en la primera opción

# Variables para capturar el cuadro
punto_inicial = None  # Primer clic
punto_final = None    # Segundo clic

# Función para registrar el cuadro (dos puntos) en la imagen
def marcar_cuadro(event, x, y, flags, param):
    global punto_inicial, punto_final, pregunta_actual, opcion_actual
    if event == cv2.EVENT_LBUTTONDOWN:
        if punto_inicial is None:
            punto_inicial = (x + desplazamiento_x, y + desplazamiento_y)
            print(f"Punto inicial registrado para {opcion_actual} de la pregunta {pregunta_actual}: {punto_inicial}")
        else:
            punto_final = (x + desplazamiento_x, y + desplazamiento_y)
            print(f"Punto final registrado para {opcion_actual} de la pregunta {pregunta_actual}: {punto_final}")
            # Dibujar el cuadro en la imagen
            cv2.rectangle(imagen_cv, punto_inicial, punto_final, (0, 255, 0), 2)
            # Guardar las coordenadas del cuadro en el diccionario
            coordenadas_dict[pregunta_actual][opcion_actual] = (punto_inicial, punto_final)
            print(f"Cuadro registrado para {opcion_actual} de la pregunta {pregunta_actual}: {punto_inicial}, {punto_final}")
            # Resetear los puntos para el próximo cuadro
            punto_inicial, punto_final = None, None

# Función para cambiar a la siguiente opción
def siguiente_opcion():
    global pregunta_actual, opcion_actual
    opciones = ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca']
    index = opciones.index(opcion_actual) + 1
    if index < len(opciones):
        opcion_actual = opciones[index]
    else:
        opcion_actual = opciones[0]
        pregunta_actual += 1
        if pregunta_actual > 23:
            pregunta_actual = 13  # Regresar a la primera pregunta si se pasa de la última
    print(f"Ahora seleccionando para la opción: {opcion_actual} de la pregunta {pregunta_actual}")

# Función para desplazar la imagen usando las letras
def desplazar_imagen(tecla):
    global desplazamiento_x, desplazamiento_y
    if tecla == ord('w'):  # Tecla 'w' para mover hacia arriba
        desplazamiento_y -= scroll_step
    elif tecla == ord('s'):  # Tecla 's' para mover hacia abajo
        desplazamiento_y += scroll_step
    elif tecla == ord('a'):  # Tecla 'a' para mover hacia la izquierda
        desplazamiento_x -= scroll_step
    elif tecla == ord('d'):  # Tecla 'd' para mover hacia la derecha
        desplazamiento_x += scroll_step

# Ruta de la imagen convertida desde el PDF
ruta_imagen = 'C:\\Users\\practicante.rrhh\\Desktop\\cuestio_extralab\\1193522709.pdf'

# Convertir la segunda página del PDF a imagen
poppler_path = r'C:\Users\practicante.rrhh\Desktop\poppler-24.08.0\Library\bin'
paginas = convert_from_path(ruta_imagen, first_page=9, last_page=9, poppler_path=poppler_path)



# Seleccionar la segunda página convertida
imagen = paginas[0]

# Convertir la imagen de PIL a formato OpenCV
imagen_cv = cv2.cvtColor(np.array(imagen), cv2.COLOR_RGB2BGR)

# Mostrar la imagen con dimensiones reales
cv2.imshow("Imagen seleccionada", imagen_cv)

# Configurar la función para capturar los clics en la imagen
cv2.setMouseCallback("Imagen seleccionada", marcar_cuadro)

# Instrucciones iniciales
print("Haz clic en dos puntos para definir el cuadro para cada opción de la pregunta. Presiona 'n' para cambiar de opción.")
print("Usa las teclas 'w', 'a', 's', 'd' para desplazarte por la imagen.")

# Mantener la ventana abierta hasta que el usuario presione 'n' para cambiar de opción o 'Esc' para salir
while True:
    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord('n'):
        siguiente_opcion()
    elif tecla == 27:  # Presionar 'Esc' para salir
        break
    else:
        desplazar_imagen(tecla)

    # Actualizar la imagen desplazada
    imagen_desplazada = imagen_cv[desplazamiento_y:desplazamiento_y + 600, desplazamiento_x:desplazamiento_x + 800]
    if imagen_desplazada.shape[0] < 600 or imagen_desplazada.shape[1] < 800:
        imagen_desplazada = imagen_cv[desplazamiento_y:, desplazamiento_x:]

    cv2.imshow("Imagen seleccionada", imagen_desplazada)

cv2.destroyAllWindows()

# Mostrar las coordenadas almacenadas en el diccionario
print("Coordenadas almacenadas en el diccionario:")
for pregunta, opciones in coordenadas_dict.items():
    print(f"Pregunta {pregunta}:")
    for opcion, coordenada in opciones.items():
        print(f"  {opcion}: {coordenada}")
