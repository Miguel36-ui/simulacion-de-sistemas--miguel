"""
Modulo Generacion de Numeros Pseudoaleatorios
Ejercicio 2: Algoritmo Congruencial Mixto (Lineal)4
Formula: Xn+1 = (a * Xn + c) mod m
    rn = Xn / m
Descripcion: Genera numero pseudoaletorios uniformemente distribuidos en (0, 1) mediante relaciones de 
recurrencia modular.
"""


import pandas as pd

def generador_congruencia_mixto(XO: int, a: int, c: int, m: int) -> pd.DataFrame:

    """
    Genera una secuencia de numeros pseudoaleatorios usando el metodo congruencial mixto
    Parametros:
    -----------


    XO: int -> Semilla inicial (deber ser > 0)
    a: int -> Multiplicador (deber ser > 0)
    c: int -> Constante adictivo o incremento (deber ser > 0)
    m: int -> Modulo de la operacion (m > XO, a, c))

    Retrona:
    pd.DataFrame -> Tabla con los valores de Xn y los pseudoaleatorios rn
    """
    Xi = XO #Asignamos el valor actual de la semilla
    historial  = [] #Lista para guardar los registros de cada paso

    #El periodo maximo posible de este generador es 'm'
    for i in range(50):
        #1. Aplicamos la formula del generador congruencial: xn+1 = (a * Xn + c) mod m
        Xi_siguiente = (a * Xi + c) % m

        #2. Normalizamos el entero obtenido para llevarlo al intervalo (0, 1)
        ri = Xi_siguiente / m

        #3. Guardamos los resultados de la iteracion actual
        historial.append({
            'Iteracion': i + 1,
            'X_i': Xi_siguiente,
            'U_i (0,1)': ri
        })

        #4. Actualizamos el valor de Xi para la siguiente iteracion
        Xi = Xi_siguiente

        #Si volvemos a obtener el numero de la semilla inicial, el ciclo se repite 

    return pd.DataFrame(historial)

#---Bloque principal de ejecucion---
if __name__ == "__main__":
    #Paramtros probados en clase XO =, a = 5, c = 7, m = 8
    semilla = 27
    multiplicador = 17
    constante_c = 43
    modulo = 100

    print(f"Generador secuencia con XO = {semilla}, a = {multiplicador}, c = {constante_c}, m = {modulo}\n")
    df_numeros = generador_congruencia_mixto(semilla, multiplicador, constante_c, modulo)

    #Imprimimos la tabla formateada
    print(df_numeros.to_string(index=False))
    print(f"\nPeriodo alcanzado: {len(df_numeros)} numeros generados antes de repetirse") 