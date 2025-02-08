from backend.rutas import obtener_cuestionarios
from backend.calculosA import procesar_cuestionario
from backend.IntraA import funcion_procesar 
from backend.formB import funcion_procesarb
from backend.calculosB import procesar_cuestionario_B
from backend.Extra import funcion_procesare
from backend.calculosE import procesar_cuestionario_extralaboral
from backend.estres import procesar_cuestionario_estres, funcion_procesares
from backend.calculototal import calcular_puntaje_total, guardar_en_db, generar_excel  

def formulario(datos: dict):
    """
    Recibe los datos del formulario (cedula, nombre, tipo de empleado y área),
    obtiene las rutas de los cuestionarios y procesa cada uno.
    El parámetro 'tipo_empleado' (A o B) se utiliza para procesar la clasificación del cuestionario de estrés.
    """
    cedula = datos.get("cedula")
    nombre_empleado = datos.get("nombre_empleado")
    tipo_empleado = datos.get("tipo_empleado")  # "A" para jefes, "B" para operarios
    area = datos.get("area")

    print(f"Datos ingresados:\nCédula: {cedula}\nNombre: {nombre_empleado}\nTipo: {tipo_empleado}\nÁrea: {area}")

    # Obtener rutas de los cuestionarios
    cuestionarios = obtener_cuestionarios(cedula)

    # Procesar Cuestionario Intralaboral A
    respuestas_a = None
    if cuestionarios[0] is not None:
        print("Cuestionario Intralaboral A encontrado. Procesando...")
        proc_respuestas_a = funcion_procesar(cuestionarios)
        if proc_respuestas_a is not None:
            respuestas_a = procesar_cuestionario(proc_respuestas_a)
            print(f"Resultados Intralaboral A: {respuestas_a}")
        else:
            print("La función de procesamiento de A devolvió None.")
    else:
        print("No se encontró Cuestionario Intralaboral A.")

    # Procesar Cuestionario Intralaboral B
    respuestas_b = None
    if cuestionarios[1] is not None:
        print("Cuestionario Intralaboral B encontrado. Procesando...")
        proc_respuestas_b = funcion_procesarb(cuestionarios)
        if proc_respuestas_b is not None:
            respuestas_b = procesar_cuestionario_B(proc_respuestas_b)
            print(f"Resultados Intralaboral B: {respuestas_b}")
        else:
            print("La función de procesamiento de B devolvió None.")
    else:
        print("No se encontró Cuestionario Intralaboral B.")

    # Procesar Cuestionario Extralaboral
    if len(cuestionarios) > 2 and cuestionarios[2] is not None:
        print("Cuestionario Extralaboral encontrado. Procesando...")
        # Llamar a la función de extracción y asignar su resultado
        proc_extralaboral = funcion_procesare(cuestionarios)
        respuestas_extralaboral = procesar_cuestionario_extralaboral(proc_extralaboral)
        print(f"Resultados Extralaboral: {respuestas_extralaboral}")
    else:
        print("No se encontró Cuestionario Extralaboral.")

    # Procesar Cuestionario de Estrés
    # Se asume que el cuestionario de estrés está siempre presente (índice 3)
    print("Cuestionario de Estrés encontrado. Procesando...")
    proc_respuestas_estres = funcion_procesares(cuestionarios)
    respuestas_estres = procesar_cuestionario_estres(tipo_empleado, proc_respuestas_estres)
    print(f"Resultados de Estrés: {respuestas_estres}")
    
    # Calcular puntaje total
    if(tipo_empleado.upper()=="A"):
        respuestas_totales=calcular_puntaje_total(respuestas_a[4],respuestas_extralaboral[4],tipo_empleado)

    elif(tipo_empleado.upper()=="B"):
        respuestas_totales=calcular_puntaje_total(respuestas_b[4],respuestas_extralaboral[4],tipo_empleado)


    
    mns_db=guardar_en_db(tipo_empleado, nombre_empleado, cedula, area, respuestas_a, respuestas_b, respuestas_extralaboral, respuestas_estres)
    
    mns_excel=generar_excel(respuestas_estres[0],respuestas_estres[1],respuestas_estres[2],cedula,tipo_empleado, cuestionarios,respuestas_totales,respuestas_a,respuestas_b,respuestas_extralaboral)

    print(f'Mensaje: {mns_excel}')

    return list((mns_db, mns_excel))   