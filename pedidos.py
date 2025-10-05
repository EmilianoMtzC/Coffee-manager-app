from login import solicitar_usuario

INTENTOS_PRODUCTO = 3                        # Intentos por producto en pedidos
PRODUCTOS = { "Cafe", "Capuccino", "Chocolate", "Chilaquiles", "Molletes", "Omelette", "Galleta", "Brownie", "Pay" }
PEDIDOS = []
USUARIO_ACTUAL = None

def registrar_pedido():
    """
    Registra un pedido validando productos y guardándolo en 'pedidos.txt'.
    Pide cuántos productos, intenta hasta 3 veces por producto si hay error.
    """
    global USUARIO_ACTUAL
    if not USUARIO_ACTUAL:
        print("No hay usuario activo. Inicia sesion primero.")
        if not solicitar_usuario():
            return

    try:
        num_productos = int(input("Cuantos productos serán? "))
        if num_productos <= 0:
            print("El número de productos debe ser mayor que 0.")
            return
    except (ValueError, EOFError, KeyboardInterrupt):
        print("Ingresa un número válido de productos.")
        return

    pedido_actual = []
    for _ in range(num_productos):
        try:
            producto_input = input("Ingresar pedido: ").strip().capitalize()
        except (EOFError, KeyboardInterrupt):
            print("\nRegistro de pedido cancelado.")
            return
        oportunidades = INTENTOS_PRODUCTO
        while oportunidades > 0:
            if producto_input not in PRODUCTOS:
                print("Producto no válido. Disponibles:", ", ".join(sorted(PRODUCTOS)))
                oportunidades -= 1
                if oportunidades == 0:
                    print("Se agotaron los intentos para este producto.")
                    break
                try:
                    producto_input = input("Intenta de nuevo (producto): ").strip().capitalize()
                except (EOFError, KeyboardInterrupt):
                    print("\nRegistro de pedido cancelado.")
                    return
            else:
                pedido_actual.append(producto_input)
                print("Pedido guardado:", producto_input)
                break  # producto válido, salir del while

    if not pedido_actual:
        print("No se registraron productos válidos en este pedido.")
        return

    # Agrega los productos válidos de este pedido a la lista global
    PEDIDOS.extend(pedido_actual)

    try:
        with open("menus/pedidos.txt", "a", encoding="utf-8") as f:
            f.write(f"Pedido registrado por {USUARIO_ACTUAL} con los siguientes productos: {', '.join(pedido_actual)}\n")
    except OSError:
        print(f"Error al guardar el pedido")

def cargar_menu():
    """ Muestra un menú para que el usuario elija entre desayunos, bebidas o postres. Después de mostrarlo, permite registrar un pedido. """
    print("====== ELEGIR MENÚ =======")
    try: menu = int(input("Elige un menú:\n" 
                          "1) Desayunos\n"
                          "2) Bebidas\n"
                          "3) Postres\n"
                          "4) Regresar\n"
                          "Elige una opcion entre (1-4): "))
    except (ValueError, EOFError, KeyboardInterrupt):
        print("Entrada inválida.")
        return

    match menu:
        case 1:
            with open("menus/desayunos.txt", "r", encoding="utf-8") as archivo:
                print(archivo.read())
        case 2:
            with open("menus/bebidas.txt", "r", encoding="utf-8") as archivo:
                print(archivo.read())
        case 3:
            with open("menus/postres.txt", "r", encoding="utf-8") as archivo:
                print(archivo.read())
        case 4:
            return
        case _:
            print("Opción no válida.")

    registrar_pedido()

def consultar_pedidos():
    """
    Muestra todos los pedidos desde 'pedidos.txt', numerados.
    Si no hay archivo o está vacío, informa al usuario.
    """
    try:
        with open("registros/pedidos.txt", "r", encoding="utf-8") as archivo:
            lineas = [line.strip() for line in archivo if line.strip()]
    except FileNotFoundError:
        print("No hay pedidos registrados.")
        return
    except UnicodeDecodeError:
        print("Error al leer pedidos.txt (codificación inválida).")
        return

    if not lineas:
        print("No hay pedidos registrados.")
        return

    print("\n=== Pedidos registrados ===")
    for i, linea in enumerate(lineas, start=1):     # Se imprime cada pedido en lista
        print(f" {i}. {linea}")