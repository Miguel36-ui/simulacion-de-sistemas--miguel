"""
Modulo: Generacion de Numeros Pseudoaleatorios
Tarea 2 - Punto 2: Algoritmo Congruencial Multiplicativo
Formula: Xn+1 = (a * Xn) mod m
         Ui = Xi+1 / m
Descripcion: Genera numeros pseudoaleatorios uniformemente distribuidos en (0, 1)
             eliminando la constante aditiva (c = 0) y evalua si alcanza el periodo maximo (m/4).
"""

import pandas as pd  # Importamos pandas para construir y formatear la tabla de resultados

def generador_congruencial_multiplicativo(X0: int, a: int, m: int) -> pd.DataFrame:
    """
    Genera una secuencia de numeros pseudoaleatorios usando el metodo congruencial multiplicativo.
    
    Parametros:
    -----------
    X0: int -> Semilla inicial (debe ser un entero impar y primo relativo con m)
    a: int  -> Constante multiplicativa
    m: int  -> Modulo de la operacion (generalmente potencia de 2, como 128)

    Retorna:
    --------
    pd.DataFrame -> Tabla con las iteraciones hasta completar un ciclo completo
    """
    Xi = X0         # Inicializamos Xi con el valor de la semilla original (X0)
    historial = []  # Lista vacia para almacenar cada fila de la tabla
    iteracion = 1   # Contador de pasos iniciando en 1

    # Usamos un ciclo 'while True' para que avance hasta que el ciclo se repita por si solo
    while True:
        # 1. Aplicamos la formula multiplicativa: multiplicamos y sacamos el residuo (%) sin sumar 'c'
        Xi_siguiente = (a * Xi) % m

        # 2. Normalizamos el entero obtenido dividiendolo entre 'm' para llevarlo al intervalo (0, 1)
        Ui = Xi_siguiente / m

        # 3. Guardamos los datos de esta iteracion en nuestra lista
        historial.append({
            'Iteracion': iteracion,
            'X_i (Anterior)': Xi,
            'X_i+1 (Nuevo)': Xi_siguiente,
            'U_i (0,1)': Ui
        })

        # 4. Condicion de paro: si volvemos a obtener la semilla inicial, el ciclo ha terminado
        if Xi_siguiente == X0:
            break

        # 5. Actualizamos Xi y aumentamos el contador para la siguiente vuelta
        Xi = Xi_siguiente
        iteracion += 1

    # Convertimos los registros en una tabla (DataFrame) de pandas y la retornamos
    return pd.DataFrame(historial)

# --- Bloque principal de ejecucion ---
if __name__ == "__main__":
    # Parametros asignados en la Tarea 2 para el Generador Multiplicativo
    semilla = 13
    multiplicador = 19
    modulo = 128

    print(f"Generando secuencia Multiplicativa con X0 = {semilla}, a = {multiplicador}, m = {modulo}\n")

    # Llamamos a la funcion y guardamos la tabla resultante
    df_multiplicativo = generador_congruencial_multiplicativo(semilla, multiplicador, modulo)

    # Imprimimos la tabla completa en consola
    print(df_multiplicativo.to_string(index=False))

    # --- Evaluacion del periodo maximo esperado (m / 4) ---
    periodo_alcanzado = len(df_multiplicativo)
    periodo_esperado = modulo // 4  # Division entera para obtener el valor exacto (128 / 4 = 32)

    print(f"\nPeriodo alcanzado: {periodo_alcanzado} iteraciones.")
    print(f"Periodo maximo esperado (m/4): {periodo_esperado} iteraciones.")

    if periodo_alcanzado == periodo_esperado:
        print("Resultado: La secuencia SI alcanza el periodo maximo esperado.")
    else:
        print("Resultado: La secuencia NO alcanza el periodo maximo esperado.")