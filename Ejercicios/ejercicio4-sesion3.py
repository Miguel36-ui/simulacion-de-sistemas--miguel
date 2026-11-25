"""
Modulo: Pruebas Estadisticas para numeros pseudoaleatorios 
Ejercicio 2: Prueba del poker para 3 decimales (prueba de independencia)
Descripcion: Clasifica las frecuencias de combinacion de digitos (Todos diferentes, un par, tercia)
t valida la independencia usando Chi-cuadrada (Chi^2)
"""

import numpy as np
from scipy import stats

def prueba_poker_3_digitos(R_floats: list, alpha: float = 0.05) -> dict:
    """
    Ejecuta la prueba del poker analizando los primeros 3 decimales de cada numero.

    Parametros: 
    -----------
    R_floats: list -> Muestra de numeros r_i
    alpha float -> Nivel de significancia (por defecto 0.05)

    Retorna: 
    --------
    dict -> Frecuencias observadas, esperadas, estadisticas Chi^2 y dictamen
    """

    n = len(R_floats) 
    td, p1, t = 0, 0, 0 #Contadores TD= Todos Diferentes, P1= Un Par, T= Tercia

    #1. Clasificacion digito por digito
    for r in R_floats:
        #Extraemos los primeros 3 decimales como cadena de  caracteres 
        d_str = f"{r:.3f}".split('.')[1][:3]

        #Convertimos la cadena a un conjunto (set) para contar digitos unicos 
        digitos_unicos = len(set(d_str))

        if digitos_unicos == 3:
            td += 1 #Ej: 0.375 -> (3,7,5) -> 3 digitos distintos
        elif digitos_unicos == 2:
            p1 += 1 #Ej: 0.775 -> (7,7,5) -> par (dos 7s)
        else:
            t += 1 #Ej: 0.888 -> (8,8,8) -> 1 tercia (tres 8s) 

    #Array de Frecuencias observadas (o_i)
    O = np.array([td, p1, t])

    #Probabilidades teoricas conocidas para 3 digitos:
    #P (TD) = 0.720 | P(1P) = 0.270 | P(Tercia) = 0.010
    probabilidades = np.array([0.720, 0.270, 0.010])

    #Frecuencias esperadas (e_i= n *p_i)
    E = n * probabilidades

    #2. Calculo del estaditico Chi-cuadrado: Suma ((o_i - e_i)^2/e_i)
    chi0_cuadrado = np.sum((O-E)**2/E)

    #3. Obtecon del valor critico chi^2 con grados de libertad k-1 = 3-1 =2
    grados_libertad = len(probabilidades) - 1
    chi_critico = stats.chi2.ppf(1-alpha, df=grados_libertad)

    #Regla de decision = si chi0^2 < chi critico, la muestra pasa la prueba
    pasa_prueba = chi0_cuadrado < chi_critico 

    return{
        'Observados_TD_1P_T' : O,
        'Esperado_TD_1P_T' : E,
        'Chi0_Cuadrado': chi0_cuadrado,
        'Chi_Critico': chi_critico,
        'Pasa_Prueba': pasa_prueba
    }

#--bloque principal de ejecucion---
if __name__ == "__main__":
    #muestra de prueba utilizada en el ejercicio de clase 
    datos_poker =[0.375, 0.775, 0.625, 0.888, 0.125]

    res = prueba_poker_3_digitos(datos_poker, alpha=0.05)

    print("===PRUEBA DEL POKER (3 DIGITOS)===")
    print(f"Frecuencas Observadas (TD, 1P, T): {res['Observados_TD_1P_T']}")
    print(f"Frecuencias Esperadas (TD, 1P, T): {np.round(res['Esperado_TD_1P_T'], 2)}")
    print(f"Estadistico Chi-cuadrado (Chi0^2): {res['Chi0_Cuadrado']:.4f}")
    print(f"Valor Critico Tabla Chi^2 (alpha = 0.05): {res['Chi_Critico']:.4f}")
    print("----------------------------------------------------")
    if res['Pasa_Prueba']:
        print("DICTAMEN: APROBADO -> La muestra pasa la prueba de independencia del Poker.")
    else:
        print("DICTAMENT: RECHAZADO -> Se observa una desviacion atipica de digitos repetidos")
