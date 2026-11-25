"""
Modulo: Pruebas Estadisticas para Numeros Pseudoaleatorios
Tarea 3.1: Evaluacion integral de 100 numeros pseudoaleatorios (Uniformidad e Independencia)
Descripcion: Ejecuta las pruebas de Promedios, Frecuencias (Chi-cuadrada), 
Kolmogorov-Smirnov (K-S) y Poker (5 digitos) con un nivel de confianza del 95% (alpha = 0.05).
"""

import numpy as np
from scipy import stats
from collections import Counter


def prueba_promedios(R: list, alpha: float = 0.05) -> dict:
    """
    1. Realiza la prueba de los promedios (test Z) para verificar uniformidad.

    Parametros:
    -----------
    R: list -> Lista de numeros pseudoaleatorios r_i en el intervalo (0, 1)
    alpha: float -> Nivel de significancia (por defecto 0.05 para 95% de confianza)

    Retorna:
    --------
    dict -> Resultados cuantitativos y veredicto de la hipotesis.
    """
    n = len(R)
    r_bar = np.mean(R)

    # 1. Calculamos el estadistico de prueba Z0
    error_estandar = 1 / np.sqrt(12 * n)
    Z0 = (r_bar - 0.5) / error_estandar

    # 2. Valor critico de la distribucion normal estandar Z_(alpha/2)
    z_critico = stats.norm.ppf(1 - alpha / 2)

    # 3. Regla de decision: Si |Z0| < Z_critico, no se rechaza H0
    pasa_prueba = abs(Z0) < z_critico

    return {
        'n': n,
        'Media_muestral': r_bar,
        'Estadistico_Z0': Z0,
        'Valor_critico_Z': z_critico,
        'Pasa_prueba': pasa_prueba
    }


def prueba_frecuencias_chi2(R: list, k: int = 10, alpha: float = 0.05) -> dict:
    """
    2. Realiza la prueba de frecuencias (Chi-cuadrada) dividiendo [0, 1] en k subintervalos.

    Parametros:
    -----------
    R: list -> Muestra de numeros r_i
    k: int -> Numero de subintervalos de igual amplitud (por defecto 10)
    alpha: float -> Nivel de significancia (por defecto 0.05)

    Retorna:
    --------
    dict -> Frecuencias observadas, esperadas, estadistico Chi^2 y dictamen.
    """
    n = len(R)
    limites = np.linspace(0, 1, k + 1)

    # 1. Frecuencias observadas (O_i) y esperadas (E_i)
    O, _ = np.histogram(R, bins=limites)
    E = np.full(k, n / k)

    # 2. Estadistico Chi-cuadrado: Suma((O_i - E_i)^2 / E_i)
    chi0_cuadrado = np.sum(((O - E) ** 2) / E)

    # 3. Valor critico de tablas Chi^2 con grados de libertad k - 1
    grados_libertad = k - 1
    chi_critico = stats.chi2.ppf(1 - alpha, df=grados_libertad)

    # Regla de decision
    pasa_prueba = chi0_cuadrado < chi_critico

    return {
        'Intervalos': limites,
        'Observados': O,
        'Esperados': E,
        'Chi0_Cuadrado': chi0_cuadrado,
        'Chi_Critico': chi_critico,
        'Pasa_prueba': pasa_prueba
    }


def prueba_kolmogorov_smirnov(R: list, alpha: float = 0.05) -> dict:
    """
    3. Realiza la prueba de Kolmogorov-Smirnov (K-S) comparando la acumulada empirica Fn(x).

    Parametros:
    -----------
    R: list -> Muestra de numeros r_i
    alpha: float -> Nivel de significancia (por defecto 0.05)

    Retorna:
    --------
    dict -> Estadisticos D+, D-, D global, valor critico y dictamen.
    """
    n = len(R)
    R_ordenados = np.sort(R)
    i = np.arange(1, n + 1)

    # 1. Calculo de desviaciones maximas D+ y D-
    D_mas = np.max((i / n) - R_ordenados)
    D_menos = np.max(R_ordenados - ((i - 1) / n))
    D_estadistico = max(D_mas, D_menos)

    # 2. Valor critico D_(alpha, n) para alpha = 0.05 y n > 35
    D_critico = 1.36 / np.sqrt(n) if alpha == 0.05 else stats.ksone.ppf(1 - alpha / 2, n)

    # Regla de decision
    pasa_prueba = D_estadistico < D_critico

    return {
        'D_mas': D_mas,
        'D_menos': D_menos,
        'D_estadistico': D_estadistico,
        'D_critico': D_critico,
        'Pasa_prueba': pasa_prueba
    }


def prueba_poker_5_digitos(R_floats: list, alpha: float = 0.05) -> dict:
    """
    4. Ejecuta la prueba del poker analizando los primeros 5 decimales de cada numero.

    Parametros:
    -----------
    R_floats: list -> Muestra de numeros r_i
    alpha: float -> Nivel de significancia (por defecto 0.05)

    Retorna:
    --------
    dict -> Frecuencias observadas, esperadas, estadistico Chi^2 y dictamen.
    """
    n = len(R_floats)
    # Contadores: TD=Todos Diferentes, P1=Un Par, P2=Dos Pares, T=Tercia, F=Full, P=Poker, Q=Quintilla
    td, p1, p2, t, f, p, q = 0, 0, 0, 0, 0, 0, 0

    # 1. Clasificacion digito por digito (5 decimales)
    for r in R_floats:
        d_str = f"{r:.5f}".split('.')[1][:5]
        conteo = sorted(Counter(d_str).values(), reverse=True)

        if conteo == [1, 1, 1, 1, 1]:
            td += 1
        elif conteo == [2, 1, 1, 1]:
            p1 += 1
        elif conteo == [2, 2, 1]:
            p2 += 1
        elif conteo == [3, 1, 1]:
            t += 1
        elif conteo == [3, 2]:
            f += 1
        elif conteo == [4, 1]:
            p += 1
        else:
            q += 1

    # Array de Frecuencias observadas (O_i)
    O = np.array([td, p1, p2, t, f, p, q])

    # Probabilidades teoricas conocidas para 5 digitos:
    probabilidades = np.array([0.3024, 0.5040, 0.1080, 0.0720, 0.0090, 0.0045, 0.0001])

    # Frecuencias esperadas (E_i = n * p_i)
    E = n * probabilidades

    # 2. Calculo del estadistico Chi-cuadrado: Suma((O_i - E_i)^2 / E_i)
    chi0_cuadrado = np.sum(((O - E) ** 2) / E)

    # 3. Valor critico Chi^2 con grados de libertad k - 1 = 7 - 1 = 6
    grados_libertad = len(probabilidades) - 1
    chi_critico = stats.chi2.ppf(1 - alpha, df=grados_libertad)

    # Regla de decision
    pasa_prueba = chi0_cuadrado < chi_critico

    return {
        'Observados_TD_1P_2P_T_F_P_Q': O,
        'Esperados_TD_1P_2P_T_F_P_Q': E,
        'Chi0_Cuadrado': chi0_cuadrado,
        'Chi_Critico': chi_critico,
        'Pasa_prueba': pasa_prueba
    }


# --- Bloque principal de ejecucion ---
if __name__ == "__main__":
    # Serie de 100 numeros pseudoaleatorios U_i a evaluar
    datos_U = [
        0.84215, 0.12567, 0.49302, 0.95184, 0.36729, 0.60418, 0.08943, 0.72150, 0.24891, 0.58364,
        0.91702, 0.45039, 0.17685, 0.69241, 0.30578, 0.87420, 0.51296, 0.03847, 0.74613, 0.28159,
        0.31948, 0.78412, 0.61095, 0.20438, 0.55821, 0.89134, 0.43670, 0.16289, 0.94503, 0.37146,
        0.70852, 0.04197, 0.62918, 0.85340, 0.26475, 0.54019, 0.98263, 0.18904, 0.47528, 0.73186,
        0.67204, 0.05839, 0.92471, 0.38156, 0.74902, 0.19385, 0.51649, 0.83017, 0.29473, 0.65820,
        0.11496, 0.48231, 0.79564, 0.35712, 0.93805, 0.07248, 0.61893, 0.25170, 0.80429, 0.44615,
        0.14892, 0.53107, 0.88743, 0.40219, 0.69581, 0.02764, 0.76410, 0.34925, 0.97188, 0.21536,
        0.58904, 0.82371, 0.15649, 0.46802, 0.71258, 0.39417, 0.84930, 0.06385, 0.63514, 0.28976,
        0.90341, 0.41628, 0.27590, 0.73814, 0.18463, 0.50927, 0.86152, 0.64209, 0.09574, 0.47831,
        0.81365, 0.33048, 0.68492, 0.22917, 0.96043, 0.52186, 0.13759, 0.75402, 0.42861, 0.89634
    ]

    # 1. Ejecutar Prueba de Promedios
    res_prom = prueba_promedios(datos_U, alpha=0.05)
    print("=== 1. PRUEBA DE PROMEDIOS (UNIFORMIDAD) ===")
    print(f"Cantidad de datos (n): {res_prom['n']}")
    print(f"Media observada (r_bar): {res_prom['Media_muestral']:.5f}")
    print(f"Estadistico Z0: {res_prom['Estadistico_Z0']:.5f} | Valor Critico Z: {res_prom['Valor_critico_Z']:.5f}")
    print("-------------------------------------------------------")
    if res_prom['Pasa_prueba']:
        print("DICTAMEN: APROBADO -> La muestra tiene una media estadisticamente aceptable de 0.5\n")
    else:
        print("DICTAMEN: RECHAZADO -> La muestra no cumple con la media de 0.5 esperada\n")

    # 2. Ejecutar Prueba de Frecuencias (Chi-cuadrada)
    res_chi = prueba_frecuencias_chi2(datos_U, k=10, alpha=0.05)
    print("=== 2. PRUEBA DE FRECUENCIAS CHI-CUADRADA (UNIFORMIDAD) ===")
    print(f"Frecuencias Observadas (O_i): {res_chi['Observados']}")
    print(f"Frecuencias Esperadas (E_i):  {res_chi['Esperados']}")
    print(f"Estadistico Chi0^2: {res_chi['Chi0_Cuadrado']:.4f} | Valor Critico Chi^2: {res_chi['Chi_Critico']:.4f}")
    print("-------------------------------------------------------")
    if res_chi['Pasa_prueba']:
        print("DICTAMEN: APROBADO -> Los numeros se distribuyen uniformemente en los 10 intervalos.\n")
    else:
        print("DICTAMEN: RECHAZADO -> Los numeros no siguen una distribucion uniforme.\n")

    # 3. Ejecutar Prueba de Kolmogorov-Smirnov (K-S)
    res_ks = prueba_kolmogorov_smirnov(datos_U, alpha=0.05)
    print("=== 3. PRUEBA DE KOLMOGOROV-SMIRNOV (UNIFORMIDAD) ===")
    print(f"Estadistico D+: {res_ks['D_mas']:.5f} | Estadistico D-: {res_ks['D_menos']:.5f}")
    print(f"Estadistico D global: {res_ks['D_estadistico']:.5f} | Valor Critico D: {res_ks['D_critico']:.5f}")
    print("-------------------------------------------------------")
    if res_ks['Pasa_prueba']:
        print("DICTAMEN: APROBADO -> La distribucion acumulada empirica es uniforme.\n")
    else:
        print("DICTAMEN: RECHAZADO -> La distribucion acumulada difiere de la uniforme.\n")

    # 4. Ejecutar Prueba del Poker (5 digitos)
    res_poker = prueba_poker_5_digitos(datos_U, alpha=0.05)
    print("=== 4. PRUEBA DEL POKER 5 DIGITOS (INDEPENDENCIA) ===")
    print(f"Frecuencias Observadas (TD, 1P, 2P, T, F, P, Q): {res_poker['Observados_TD_1P_2P_T_F_P_Q']}")
    print(f"Frecuencias Esperadas  (TD, 1P, 2P, T, F, P, Q): {np.round(res_poker['Esperados_TD_1P_2P_T_F_P_Q'], 2)}")
    print(f"Estadistico Chi0^2: {res_poker['Chi0_Cuadrado']:.4f} | Valor Critico Chi^2: {res_poker['Chi_Critico']:.4f}")
    print("-------------------------------------------------------")
    if res_poker['Pasa_prueba']:
        print("DICTAMEN: APROBADO -> La muestra pasa la prueba de independencia del Poker.\n")
    else:
        print("DICTAMEN: RECHAZADO -> Se observa una desviacion atipica de digitos repetidos.\n")