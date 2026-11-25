"""
Modulo: Generacion de Numeros Pseudoaleatorios
Tarea 2 - Punto 1: Algoritmo Congruencial Mixto (Lineal)
Formula: Xn+1 = (a * Xn + c) mod m
         Ui = Xi+1 / m
Descripcion: Genera 50 numeros pseudoaleatorios uniformemente distribuidos en (0, 1)
             e identifica el periodo real de la secuencia.
"""

import pandas as pd  # Importamos la libreria pandas para crear y dar formato de tabla a los datos

def generador_congruencia_mixto(X0: int, a: int, c: int, m: int, cantidad: int = 50) -> pd.DataFrame:
    """
    Genera una secuencia de numeros pseudoaleatorios usando el metodo congruencial mixto.
    
    Parametros:
    -----------
    X0: int       -> Semilla inicial (debe ser >= 0)
    a: int        -> Constante multiplicativa (debe ser > 0)
    c: int        -> Constante aditiva o incremento (debe ser > 0)
    m: int        -> Modulo de la operacion (m > X0, a, c)
    cantidad: int -> Cantidad total de numeros a generar (por defecto 50)

    Retorna:
    --------
    pd.DataFrame -> Tabla estructurada con la iteracion, los enteros X_i y los decimales U_i
    """
    Xi = X0         # Inicializamos Xi con el valor de la semilla original (X0)
    historial = []  # Lista vacia donde iremos guardando cada fila de resultados

    # El ciclo 'for' se repetira exactamente 'cantidad' veces (50 iteraciones)
    for i in range(cantidad):
        # 1. Aplicamos la formula congruencial: multiplicamos, sumamos y sacamos el residuo (%)
        Xi_siguiente = (a * Xi + c) % m

        # 2. Normalizamos el entero obtenido dividiendolo entre 'm' para obtener un decimal entre 0 y 1
        Ui = Xi_siguiente / m

        # 3. Guardamos los datos de esta vuelta como un diccionario dentro de nuestra lista
        historial.append({
            'Iteracion': i + 1,        # i empieza en 0, por eso sumamos 1 para mostrar del 1 al 50
            'X_i (Anterior)': Xi,      # Guardamos con que numero empezo esta operacion
            'X_i+1 (Nuevo)': Xi_siguiente, # Guardamos el resultado entero obtenido
            'U_i (0,1)': Ui            # Guardamos el numero pseudoaleatorio ya normalizado
        })

        # 4. Actualizamos Xi: el resultado de hoy sera el ingrediente de mañana
        Xi = Xi_siguiente

    # Convertimos la lista de diccionarios en una tabla (DataFrame) de pandas y la devolvemos
    return pd.DataFrame(historial)

# --- Bloque principal de ejecucion ---
if __name__ == "__main__":
    # Parametros asignados en la Tarea 2 para el Generador Mixto
    semilla = 27
    multiplicador = 17
    constante_c = 43
    modulo = 100
    total_numeros = 50

    print(f"Generando secuencia Mixta con X0 = {semilla}, a = {multiplicador}, c = {constante_c}, m = {modulo}\n")
    
    # Llamamos a la funcion y guardamos la tabla resultante en la variable 'df_numeros'
    df_numeros = generador_congruencia_mixto(semilla, multiplicador, constante_c, modulo, total_numeros)

    # Imprimimos toda la tabla en consola ocultando el indice automatico de pandas (index=False)
    print(df_numeros.to_string(index=False))

    # --- Calculo automatico del periodo real ---
    # Buscamos en la tabla en que iteracion vuelve a aparecer nuestra semilla original (27)
    repeticiones = df_numeros[df_numeros['X_i+1 (Nuevo)'] == semilla]
    
    # Si la semilla volvio a aparecer, tomamos el numero de esa primera iteracion (.iloc[0])
    if not repeticiones.empty:
        periodo_real = repeticiones['Iteracion'].iloc[0]
        print(f"\nPeriodo detectado: {periodo_real} iteraciones antes de que el ciclo comience a repetirse.")
    else:
        print(f"\nEl ciclo no se repitio dentro de las primeras {total_numeros} iteraciones.")