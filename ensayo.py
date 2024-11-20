import fitz  # PyMuPDF
import cv2
import numpy as np

print("Ejecutando el script ensayo.py")
ruta_pdf = r'C:\Users\practicante.rrhh\Desktop\cuestio_extralab\1193522709.pdf'
print(f"Ruta del archivo PDF: {ruta_pdf}")
template_path = 'casilla.png'  # Asegúrate de tener esta imagen en la misma carpeta

def extraer_paginas_pdf(ruta_pdf):
    """
    Extrae todas las páginas de un PDF y las convierte en imágenes.
    Devuelve una lista de imágenes.
    """
    documento = fitz.open(ruta_pdf)
    print(f"PDF cargado correctamente. Páginas totales: {len(documento)}")
    imagenes = []
    
    for num_pagina in range(len(documento)):
        print(f"Extrayendo página {num_pagina + 1}...")
        pagina = documento.load_page(num_pagina)
        pix = pagina.get_pixmap(dpi=200)
        imagen = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
        imagen = cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)
        imagenes.append(imagen)
    
    documento.close()
    return imagenes

def cargar_template(template_path):
    """
    Cargar la imagen de la plantilla y verificar su validez.
    """
    template = cv2.imread(template_path)
    if template is None:
        print(f"Error: No se pudo cargar la plantilla desde {template_path}.")
        return None
    print(f"Tamaño de la plantilla: {template.shape}")
    cv2.imshow("Plantilla", template)
    cv2.waitKey(0)
    return template

def detectar_casillas(imagen, template):
    """
    Detecta casillas usando Template Matching con diferentes escalas.
    """
    print("Detectando casillas en la imagen usando Template Matching...")
    
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    template_gris = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    # Ajustar el tamaño de la plantilla si es necesario
    escalas = [1.0, 0.9, 0.8, 0.7]
    casillas = []
    for escala in escalas:
        print(f"Probando con escala: {escala}")
        template_redimensionado = cv2.resize(template_gris, (0, 0), fx=escala, fy=escala)
        h, w = template_redimensionado.shape
        
        # Aplicar Template Matching
        resultado = cv2.matchTemplate(gris, template_redimensionado, cv2.TM_CCOEFF_NORMED)
        umbral = 0.4  # Hacer el umbral más bajo para ser más permisivo
        localizaciones = np.where(resultado >= umbral)
        
        for pt in zip(*localizaciones[::-1]):
            cv2.rectangle(imagen, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
            casillas.append((pt[0], pt[1], w, h))
        
        # Mostrar el resultado del mapa de coincidencia
        cv2.imshow(f"Resultado de coincidencia (escala {escala})", resultado)
        cv2.waitKey(0)
    
    # Mostrar las casillas detectadas
    cv2.imshow("Casillas detectadas", imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print(f"Casillas detectadas: {len(casillas)}")
    return casillas

def procesar_pdf(ruta_pdf, template_path):
    """
    Procesa un PDF, detecta casillas en cada página y extrae las respuestas.
    """
    template = cargar_template(template_path)
    if template is None:
        return
    
    paginas_imagenes = extraer_paginas_pdf(ruta_pdf)
    if not paginas_imagenes:
        print("No se encontraron imágenes en el PDF.")
        return
    
    for num_pagina, imagen in enumerate(paginas_imagenes):
        print(f"\nProcesando página {num_pagina + 1}")
        casillas = detectar_casillas(imagen, template)
        
        if not casillas:
            print("No se detectaron casillas en esta página.")
        else:
            print(f"Se detectaron {len(casillas)} casillas en la página {num_pagina + 1}")

# Ejecutar el script
procesar_pdf(ruta_pdf, template_path)
