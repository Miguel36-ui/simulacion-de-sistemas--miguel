"""

Modulo: Simulacion de sistemas de eventos discretos

Ejercicio1: Simulacion 


"""

import pandas as pd


def simular_caja(llegadas: list, servicios: list) -> pd.DataFrame:
    """
    Simular la atencion de clientes en un servidor unico
    Parametros:
    -----------
    llegadas: list
        Lista con minutos en los que llega cada cliente
    servicios: list
        Lista con la duracion (en minutos) del servicio de cada cliente

    Retorna:
    --------
    pd.DataFrame
        Tabla detallada con los tiempos de inicio, espera, salida y permanencia de cada cliente
    """

    # Inicializar listas vacias para almacenar los resultados de cada cliente
    t_inicio = []  # Minuto exacto en que la caja empieza atender al cliente
    t_espera = []  # Tiempo que el cliente espera en la fila (en minutos)
    t_salida = []  # Minuto exacto en que el cliente termina su atencion y se va
    t_sistema = []  # Tiempo total que el cliente pasa en la tienda (Espera + Servicio)

    # Variable para rastrear cuando queda desocupada la caja registradora
    t_caja_libre = 0

    # Recorrer cada cliente según su orden de llegada
    for i in range(len(llegadas)):
        arr = llegadas[i]  # Tiempo de llegada del cliente i
        dur = servicios[i]  # Tiempo de servicio requerido por el cliente i

        # El cliente entra a caja en su hora de llegada o cuando la caja se desocupe
        inicio = max(arr, t_caja_libre)

        # El tiempo de espera es la diferencia entre cuando empeiza la atencion y cuando llego
        espera = inicio - arr

        # El minuto de salida es cuando inicia la atencion mas la duracion del servicio
        salida = inicio + dur

        # El tiempo total en el sistema es desde que llega hasta que se va
        sistema = salida - arr

        # Guardamos los resultados calculados en nuestras listas
        t_inicio.append(inicio)
        t_espera.append(espera)
        t_salida.append(salida)
        t_sistema.append(sistema)

        # Actualizamos la disponibilidad de la caja para el siguiente cliente
        t_caja_libre = salida

    # Construimos un DataFrame de Pandas para organizar la informacion en formato de tabla
    df = pd.DataFrame({
        'Cliente': range(1, len(llegadas) + 1),  # ID del cliente (1, 2, 3, ...)
        'T_llegada': llegadas,  # Hora de llegada del cliente
        'T_servicio': servicios,  # Tiempo requerido de atencion
        'T_inicio': t_inicio,  # Hora que inicio la atencion
        'T_espera_Fila': t_espera,  # Minutos perdidos en la fila
        'T_salida': t_salida,  # Hora que salio
        'T_sistema': t_sistema  # Estancia total en el negocio
    })

    return df


# --- Bloque principal de ejecucion ---
if __name__ == "__main__":
    # Datos de entrada del problema (minutos de llegada y duracion de atencion)
    tiempos_llegada = [0, 2, 4, 5, 7]
    tiempos_servicio = [3, 2, 1, 4, 2]

    # Ejecutamos la simulacion
    df_resultados = simular_caja(tiempos_llegada, tiempos_servicio)

    # Mostramos la tabla completa en consola
    print("===Resultados de la simulacion de colas===")
    print(df_resultados.to_string(index=False))

    # Calculamos e imprimimos los indicadores de desempeño principales (KPIs)
    promedio_espera = df_resultados['T_espera_Fila'].mean()
    promedio_sistema = df_resultados['T_sistema'].mean()

    print(f"\n=== Resumen de indicadores de desempeño ===")
    print(f"Tiempo promedio de espera en la fila: {promedio_espera:.2f} minutos")
    print(f"Tiempo promedio en el sistema (espera + servicio): {promedio_sistema:.2f} minutos")
