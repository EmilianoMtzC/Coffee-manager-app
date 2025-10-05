import datetime
import os

HORA_APERTURA = datetime.time(7, 0)          # 07:00
HORA_CIERRE = datetime.time(17, 0) # 17:00
RESERVAS = {}
USUARIO_ACTUAL = None

# RESERVAS
def cargar_reservas():
    """
    Metodo creado para evitar reservas duplicadas.
    Carga las reservas desde 'reservas.txt' al diccionario 'reservas' en memoria.
    Formato esperado por línea: 'YYYY-MM-DD HH:MM|usuario'.
    Ignora líneas que no cumplan el formato. Si el archivo no existe, no hace nada.
    """
    global RESERVAS
    try:
        with open("registros/reservas.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()     # Elimina espacios en blanco de cada linea
                if not line:            # Si no hay contenido, omitir
                    continue
                if "|" in line:                                           # Si hay un separador | en la linea, hará lo siguiente:
                    fecha, usuario = line.split("|", 1)     # fecha va a ser la primera parte de la linea, y usuario la segunda.
                    fecha = fecha.strip()                                 # Se eliminan espacios en blanco en fecha
                    usuario = usuario.strip()                             # Se eliminan espacios en blanco en usuario
                    try:
                        datetime.datetime.strptime(fecha, "%Y-%m-%d %H:%M")     # fecha se convierte a datetime.datetime para validar
                        RESERVAS[fecha] = usuario                                       # Se agrega al diccionario reservas
                    except ValueError:
                        # Línea con formato incorrecto; la omitimos
                        pass
                # Líneas en otros formatos se omiten.
    except FileNotFoundError:
        # No hay archivo aún, no pasa nada
        pass
    except UnicodeDecodeError:
        print("Error al leer reservas.txt (codificación inválida). Revise el archivo.")

def guardar_reserva(fecha: str, usuario: str):
    """Guarda una reserva en memoria y en archivo"""
    global RESERVAS
    RESERVAS[fecha] = usuario

    # Crear carpeta si no existe
    os.makedirs("registros", exist_ok=True)

    with open("registros/reservas.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha}|{usuario}\n")

def consultar_reservas():
    """
    Muestra todas las reservas desde 'reservas.txt', numeradas.
    Si no hay archivo o está vacío, informa al usuario.
    """
    try:
        with open("registros/reservas.txt", "r", encoding="utf-8") as archivo:
            lineas = [line.strip() for line in archivo if line.strip()]

    except FileNotFoundError:
        print("No hay reservas registradas.")
        return
    except UnicodeDecodeError:
        print("Error al leer reservas.txt (codificación inválida).")
        return

    if not lineas:
        print("No hay reservas registradas.")
        return

    print("\n=== Reservas registradas ===")
    for i, linea in enumerate(lineas, start=1):    # Se imprime cada fecha en lista
        print(f" {i}. {linea}")