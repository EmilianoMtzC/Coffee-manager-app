USUARIOS = ["admin", "cliente"]
USUARIO_ACTUAL = None

# ============= Sing-in & Log-in =============

def solicitar_usuario():
    """
    Pide al usuario que escriba su nombre para entrar al sistema.
    Devuelve el nombre del usuario activo o None si se cancela.
    """
    print("Por favor ingrese su nombre de usuario:")
    usuario_valido = False
    global usuario_actual

    while not usuario_valido:
        try:
            nombre = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada cancelada. Volviendo al menú inicial.")
            return None
        if not nombre:
            print("El nombre no puede estar vacío. Intenta de nuevo.")
            continue
        if nombre not in USUARIOS:
            print("Usuario no registrado. Por favor, ingrese otro nombre de usuario.")
            usuario_valido = False
        else:
            usuario_actual = nombre
            print(f"Bienvenido, {nombre}!")
            usuario_valido = True

    return usuario_actual

def crear_usuario():
    """
    Crea un nuevo usuario y lo agrega a la lista si no existe.
    Devuelve True si se creó con éxito, False si se cancela.
    """
    print("Ingrese un nombre de usuario con el que se quiere registrar:")
    usuario_valido = False
    global usuario_actual

    while not usuario_valido:
        try:
            nombre = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\nRegistro cancelado. Volviendo al menú.")
            return False
        if not nombre:
            print("El nombre no puede estar vacío. Intenta de nuevo.")
            continue
        if nombre in USUARIOS:
            print("Usuario existente."
              "Por favor, elige otro nombre de usuario.")
            usuario_valido = False
        else:
            USUARIOS.append(nombre)
            print("Usuario creado exitosamente.")
            usuario_valido = True

    return usuario_actual
