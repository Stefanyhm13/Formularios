import os
from pathlib import Path

# Ruta completa de poppler
poppler_path = r'C:\Users\practicante.rrhh\Desktop\poppler-24.08.0\Library\bin'

def obtener_cuestionarios(cedula):
    """
    Busca los cuestionarios en la carpeta del empleado identificada por su cédula y los organiza en una lista.
    Índices:
        - 0: Cuestionario Intralaboral
        - 1: Cuestionario Extralaboral
        - 2: Cuestionario de Estrés
    :param cedula: Número de cédula del empleado.
    :return: Lista con rutas a los cuestionarios [intralaboral, extralaboral, estres].
    """
    # Definir la ruta base
    ruta_base = Path(f'C:/Users/practicante.rrhh/Desktop/Cuestionarios/{cedula}')
    print(f"Ruta base para la cédula {cedula}: {ruta_base}")  # Depuración para verificar la ruta
    # Verificar si la carpeta existe
    if not ruta_base.exists() or not ruta_base.is_dir():
        raise FileNotFoundError(f"No se encontró la carpeta para el empleado con cédula {cedula}")
    
    # Inicializar la lista con None
    cuestionarios = [None, None, None,None]
    
    # Buscar los archivos en la carpeta del empleado
    for archivo in ruta_base.iterdir():
        nombre_archivo = archivo.name.lower()
        if "intra_a" in nombre_archivo:
            cuestionarios[0] = archivo
        elif "intra_b" in nombre_archivo:
            cuestionarios[1] = archivo
        elif "extra" in nombre_archivo:
            cuestionarios[2] = archivo    
        elif "es" in nombre_archivo:
            cuestionarios[3] = archivo
    

        
    return cuestionarios

