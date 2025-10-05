"""Aplicación de cafetería para gestionar reservas y pedidos desde consola.
Incluye inicio de sesión/registro, carga de reservas desde archivo, registro
de pedidos y consultas básicas. Esta cabecera ayuda a herramientas como pylint
a entender el propósito del módulo.
"""

import time
from login import crear_usuario, solicitar_usuario
from reservas import cargar_reservas, registrar_reserva, consultar_reservas
from pedidos import cargar_menu, consultar_pedidos
from utils import cuenta_regresiva, barra_carga

# CAFETERÍA
# INICIO

print("Horario: 7:00 am - 5:00 pm")

MENU_TEXTO = (
    "\n================================\n"
    "            CAFETERÍA   \n"
    "==================================\n"
    " 1) Registrar reserva\n"
    " 2) Registrar pedido\n"
    " 3) Consultar reservas\n"
    " 4) Consultar pedidos\n"
    " 5) Cambiar de usuario\n"
    " 6) Salir\n"
    "--------------------------------"
)

MENU_TIMEOUT_SEGUNDOS = 600  # Tiempo máximo de espera en el menú
PROGRESO_TOTAL = 100         # Pasos de la barra de progreso
RETRASO_PROGRESO = 0.02        # Retardo entre pasos de progreso
# ========= FUNCIONES ===========

def login_signup():
    """
    Pantalla inicial: permite iniciar sesión o registrarse.
    Repite hasta que el usuario complete una opción o cancele.
    """
    print("Antes de comenzar seleccione cual de las siguientes opciones: (Ingrese 1 o 2)"
          "\n1) Iniciar sesion"
          "\n2) Registrarse")
    ready = False
    while not ready:
        try:
            opcion = input("Elige una opción (1-2): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nOperación cancelada. Saliendo al menú principal.")
            return
        if opcion == "1":
            if solicitar_usuario() is not None:
                ready = True
        elif opcion == "2":
            if crear_usuario():
                ready = True
        else:
            print("Opcion no valida. Escribe 1 o 2.")

def interaccion_pedidos():
    """ Permite al usuario elegir un menú y registrar un pedido. """
    print("======= ORDENAR =======")
    cargar_menu()

def interaccion_final():
    """
    Controla la interacción del usuario con el menú principal.
    Espera hasta MENU_TIMEOUT_SEGUNDOS por una respuesta.
    """
    while True:
        print(MENU_TEXTO)
        try:
            entrada = cuenta_regresiva("Elige una opción (1 - 6): ", MENU_TIMEOUT_SEGUNDOS)
            if entrada is None:
                # No hubo respuesta en el tiempo establecido
                while True:
                    try:
                        seguir = input("Han pasado 10 minutos sin elegir. ¿Deseas continuar en el menú? (si/no): ").strip().lower()
                    except (EOFError, KeyboardInterrupt):
                        print("\nOperación cancelada. Volviendo a la pantalla inicial.")
                        login_signup()
                        break
                    if seguir in ("si", "no"):
                        break
                    print('Respuesta inválida. Escribe "si" o "no".')
                if seguir == "no":
                    print("Regresando a la pantalla inicial...")
                    login_signup()
                    continue
                # El usuario desea continuar: volvemos al principio del bucle sin convertir entrada
                continue

            # Validación defensiva por si llega vacío
            if not str(entrada).strip():
                continue

            try:
                accion = int(entrada)
            except ValueError:
                print("Ingresa un número válido (1 - 6).")
                continue
        except KeyboardInterrupt:
            print("\nInteracción cancelada por el usuario.")
            break

        match accion:
            case 1:
                registrar_reserva()
            case 2:
                interaccion_pedidos()
            case 3:
                consultar_reservas()
            case 4:
                consultar_pedidos()
            case 5:
                login_signup()
            case 6:
                print("Saliendo del programa.")
                break
            case _:
                print("Opcion no valida.")

def main():
    """
    Punto de entrada del programa: maneja inicio de sesión, carga reservas,
    muestra barra de progreso y abre el menú de interacción.
    """
    try:
        login_signup()

        # Cargar reservas existentes desde archivo antes de continuar
        cargar_reservas()

        # Configuración de la barra de progreso (solo visual)
        for i in range(PROGRESO_TOTAL + 1):
            print("\r" + barra_carga(i, PROGRESO_TOTAL), end="", flush=True)
            time.sleep(RETRASO_PROGRESO)

        interaccion_final()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario. ¡Hasta luego!")

if __name__ == "__main__":
    main()