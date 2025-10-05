import queue
import threading
import time

def barra_carga(part, total, tamanio = 30):
    """
    Genera una barra de progreso en texto.
    part: progreso actual, total: valor total, tamanio: ancho visual.
    """
    frac = part / total
    completed = int(frac * tamanio)
    missing = tamanio - completed
    bar = f"[{'=' * completed}{'-' * missing}]{frac: .2%}"
    return bar

def cuenta_regresiva(prompt: str, timeout_segundos: int):
    """
    Lee la entrada del usuario con un tiempo máximo de espera.
    Devuelve la cadena ingresada o None si vence el tiempo.
    """

    q = queue.Queue()

    # Hilo que lee la entrada del usuario
    def lector():
        try:
            q.put(input(prompt))
        except (EOFError, KeyboardInterrupt):
            q.put(None)

    hilo = threading.Thread(target=lector, daemon=True)
    hilo.start()

    # Ciclo for que mide el tiempo
    for _ in range(timeout_segundos):
        if not q.empty():
            return q.get()  # Usuario escribió algo
        time.sleep(1)  # Espera 1 segundo y vuelve a checar

    # Tiempo agotado
    return None