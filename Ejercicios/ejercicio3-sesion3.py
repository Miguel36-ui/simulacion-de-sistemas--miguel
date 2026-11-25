"""
Modul: Pruebas Estadisticas para Numeros Pseudoaleatorios
Ejercicio 3: Prueba de los promedios (prueba de uniformidad)
Descripcion: Evalua si la media de una muestra de numeros pseudoaleatorios es 
estadisticamente igual a 0.5 con un nivel de confianza del 95%
"""


import numpy as np
from scipy import stats

def prueba_promedios(R: list, alpha: float = 0.05) -> dict:
    
    """
    Realiza a prueba de los promedios (test z) para verificar uniformidad 

    Parametros:
    -----------
    R: list -> Lista de numeros pseudoaleatorios r_i en el intervalo (0, 1)
    alpha: float -> Nivel de significancia (por defecto 0.05 para 95% de confianza)

    Retorna:
    --------
    dict -> Resultados cuantitativos y veredicto de la hipotesis. 
    """
    n = len(R)  # Tamaño de la muestra de numeros
    r_bar = np . mean(R)  # Media aritmetica observada en la muestra 

    #1. Calculamos el estadistico de prueba Z0: (r_bar - 0.5 / (1/ np.sqrt(12*n))) 
    error_estandar = 1 / np.sqrt(12 * n)
    Z0 = (r_bar - 0.5) / error_estandar

    #2 Obtendremos el valor critico de la distribucion normal estandar z_(alpha/2) 
    z_critico = stats.norm.ppf(1 - alpha / 2)

    #3 Regla de decision: Si |Z0| < Z_critico, no se rechaza H0 
    pasa_prueba = abs(Z0) < z_critico

    #Armams el diccionario de retorno
    resultados = {
        'n': n,
        'Media muestral': r_bar,
        'Estadistico Z0': Z0,
        'Valor critico Z': z_critico,
        'Pasa_prueba': pasa_prueba
    }
    return resultados

#---Bloques principal de ejercicio ---
if __name__ == "__main__":
    #Serie de numeros r_i a probar
    datos_r = [0.375, 0.750, 0.625, 0.000, 0.875, 0.250, 0.125, 0.500, 0.450, 0.550]

    res = prueba_promedios(datos_r, alpha=0.05)
    print("=== PRUEBA DE PROMEDIOS UNIFORMIDAD ===")
    print(f"Cantidad de datos (n): {res['n']}")
    print(f"Media observada (r_bar): {res['Media muestral']: .4f}")
    print("-------------------------------------------------------")
    if res['Pasa_prueba']:
        print("DICTAMEN: APROBADO -> La muestra tiene una media estaditicamente aceptable de 0.5")
    else:
        print("DICTAMEN: RECHAZADO -> La muestra n cumple con la media de 0.5 esperada")
        
