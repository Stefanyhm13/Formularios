import numpy as np
import cv2
import os
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from pdf2image import convert_from_path
import pytesseract

# Función para cargar imágenes desde un directorio
def cargar_imagenes(directorio, etiqueta, tamano=(20, 20)):
    imagenes = []
    etiquetas = []
    
    for archivo in os.listdir(directorio):
        if archivo.endswith(".png"):
            # Cargar la imagen
            imagen = cv2.imread(os.path.join(directorio, archivo), cv2.IMREAD_GRAYSCALE)
            # Redimensionar la imagen
            imagen = cv2.resize(imagen, tamano)
            # Normalizar
            imagen = imagen.flatten() / 255.0
            imagenes.append(imagen)
            etiquetas.append(etiqueta)
    
    return imagenes, etiquetas

# Función para convertir PDF en imágenes y extraer texto
def ocr_pdf(pdf_path):
    # Convertir el PDF a imágenes (una imagen por página)
    paginas_imagenes = convert_from_path(pdf_path)
    
    texto_completo = ""
    imagenes_pdf = []
    for pagina_imagen in paginas_imagenes:
        # Convertir la imagen de la página a un formato adecuado para el modelo
        imagen_cv = np.array(pagina_imagen)
        imagen_cv = cv2.cvtColor(imagen_cv, cv2.COLOR_RGB2GRAY)
        imagen_cv = cv2.resize(imagen_cv, (20, 20))  # Redimensionar
        imagen_cv = imagen_cv.flatten() / 255.0  # Normalizar
        
        # Añadir la imagen procesada
        imagenes_pdf.append(imagen_cv)
        
        # Usar Tesseract para extraer texto de la imagen
        texto_completo += pytesseract.image_to_string(pagina_imagen)
    
    return texto_completo, np.array(imagenes_pdf)

# Cargar datos (suponiendo que tienes un directorio con imágenes)
imagenes_x, etiquetas_x = cargar_imagenes("imagenes_x", 1)  # 1 para 'x'
imagenes_no_x, etiquetas_no_x = cargar_imagenes("imagenes_no_x", 0)  # 0 para no 'x'

# Unir datos de 'x' y no 'x'
imagenes = np.array(imagenes_x + imagenes_no_x)
etiquetas = np.array(etiquetas_x + etiquetas_no_x)

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(imagenes, etiquetas, test_size=0.2, random_state=42)

# Entrenamiento del modelo SVM
clf = svm.SVC(kernel='linear')
clf.fit(X_train, y_train)

# Predicciones
y_pred = clf.predict(X_test)

# Evaluación
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo con datos de imágenes: {accuracy * 100:.2f}%")

# Ahora, cargamos un PDF y procesamos las imágenes
pdf_path = "./prueba.pdf"  # Reemplaza con la ruta del archivo PDF
texto_extraido, imagenes_pdf = ocr_pdf(pdf_path)

# Usar el clasificador para predecir si las imágenes del PDF contienen la letra 'x'
predicciones_pdf = clf.predict(imagenes_pdf)

# Mostrar el resultado de las predicciones (0 para no 'x', 1 para 'x')
print(f"Texto extraído del PDF:\n{texto_extraido}")
print(f"Predicciones de las páginas del PDF: {predicciones_pdf}")
