# ☕ Coffee Manager App

**Coffee Manager App** es una aplicación de escritorio desarrollada en **Python** con **PyQt5** que permite gestionar **reservas y pedidos** en una cafetería. Fue creada como proyecto escolar con el objetivo de aplicar conceptos de **programación orientada a objetos**, manejo de archivos y diseño de interfaz gráfica.

---

## Tabla de contenidos

- [Características](#-características)
- [Tecnologías utilizadas](#-tecnologías-utilizadas)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Módulos](#-módulos)
- [Requisitos previos](#-requisitos-previos)
- [Instalación y ejecución](#-instalación-y-ejecución)
- [Uso de la aplicación](#-uso-de-la-aplicación)
- [Roles de usuario](#-roles-de-usuario)
- [Almacenamiento de datos](#-almacenamiento-de-datos)

---

## Características

- Inicio de sesión y registro de nuevos usuarios
- Registro de reservas con selección de fecha y hora mediante calendario interactivo
- Validación de horarios: solo se aceptan reservas entre **07:00 y 16:59**
- Prevención de reservas duplicadas en el mismo horario
- Registro de pedidos con selección múltiple de productos desde el menú
- Visualización de menús por categoría: Desayunos, Bebidas y Postres
- Consulta de reservas y pedidos registrados (solo administradores)
- Almacenamiento persistente de datos en archivos `.txt`
- Interfaz gráfica con tema oscuro

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.10+ | Lenguaje principal |
| PyQt5 | Interfaz gráfica de usuario |
| `datetime` | Manejo y validación de fechas y horas |
| `os` | Manejo de directorios y archivos |
| Archivos `.txt` | Persistencia de datos |

---

## Estructura del proyecto

```
coffee-manager-app/
│
├── app.py              # Punto de entrada; contiene toda la interfaz gráfica (GUI)
├── login.py            # Lógica de autenticación y registro de usuarios
├── pedidos.py          # Lógica de registro y consulta de pedidos
├── reservas.py         # Lógica de registro y consulta de reservas
│
├── menus/
│   ├── desayunos.txt   # Menú de desayunos (lectura)
│   ├── bebidas.txt     # Menú de bebidas (lectura)
│   └── postres.txt     # Menú de postres (lectura)
│
└── registros/
    ├── pedidos.txt     # Pedidos guardados (generado automáticamente)
    └── reservas.txt    # Reservas guardadas (generado automáticamente)
```

> La carpeta `registros/` se crea automáticamente al guardar el primer pedido o reserva. Los archivos de menú dentro de `menus/` deben existir antes de ejecutar la aplicación.

---

## Módulos

### `app.py` — Interfaz gráfica

Contiene las cuatro clases de ventana de la aplicación:

**`main_window`** — Ventana principal
- Panel izquierdo con botones de navegación
- Panel derecho para mostrar reservas y pedidos consultados
- Al iniciar, solicita automáticamente que el usuario inicie sesión

**`login_window`** — Subventana de sesión
- Campo de texto para ingresar el nombre de usuario
- Botón **Iniciar sesión**: valida que el usuario exista en el sistema
- Botón **Registrarse**: crea un nuevo usuario si el nombre no está en uso
- Botón **Cancelar**: cierra la ventana sin cambios

**`reservas_window`** — Subventana de reservas
- Widget de calendario para seleccionar la fecha
- Widget de hora con formato `HH:mm`
- Valida que la hora esté en el horario de operación (07:00–16:59)
- Verifica que no exista ya una reserva en esa fecha y hora
- Guarda la reserva en `registros/reservas.txt`

**`pedidos_window`** — Subventana de pedidos
- Pestañas con los menús de Desayunos, Bebidas y Postres como referencia (solo lectura)
- Lista de productos con selección múltiple
- Guarda el pedido en `registros/pedidos.txt`

---

### `login.py` — Autenticación

| Elemento | Descripción |
|---|---|
| `USUARIOS` | Lista de usuarios registrados. Incluye `"admin"` y `"cliente"` por defecto |
| `USUARIO_ACTUAL` | Variable global con el usuario activo en la sesión |
| `solicitar_usuario()` | Solicita y valida un usuario existente por consola |
| `crear_usuario()` | Crea y registra un nuevo usuario si el nombre no existe |

---

### `pedidos.py` — Gestión de pedidos

| Elemento | Descripción |
|---|---|
| `PRODUCTOS` | Conjunto con los productos disponibles del menú |
| `PEDIDOS` | Lista en memoria con los pedidos de la sesión |
| `INTENTOS_PRODUCTO` | Número de intentos permitidos por producto (3) |
| `registrar_pedido()` | Registra un pedido validando cada producto ingresado |
| `cargar_menu()` | Muestra el menú elegido y llama a `registrar_pedido()` |
| `consultar_pedidos()` | Lee y muestra los pedidos desde `registros/pedidos.txt` |

**Productos disponibles:**
`Brownie`, `Cafe`, `Capuccino`, `Chilaquiles`, `Chocolate`, `Galleta`, `Molletes`, `Omelette`, `Pay`

---

### `reservas.py` — Gestión de reservas

| Elemento | Descripción |
|---|---|
| `HORA_APERTURA` | `07:00` — hora mínima para reservar |
| `HORA_CIERRE` | `17:00` — hora máxima para reservar |
| `RESERVAS` | Diccionario en memoria: `{fecha_str: usuario}` |
| `cargar_reservas()` | Carga reservas desde archivo al diccionario para evitar duplicados |
| `guardar_reserva(fecha, usuario)` | Guarda una reserva en memoria y en `registros/reservas.txt` |
| `consultar_reservas()` | Lee y muestra las reservas desde el archivo |

---

## Requisitos previos

- Python **3.10 o superior** (se utiliza `match/case`)
- PyQt5

---

## Instalación y ejecución

1. Clona el repositorio:
   ```bash
   git clone https://github.com/EmilianoMtzC/coffee-manager-app.git
   cd coffee-manager-app
   ```

2. Instala las dependencias:
   ```bash
   pip install PyQt5
   ```

3. Crea la carpeta de menús y añade los archivos de texto correspondientes:
   ```
   menus/desayunos.txt
   menus/bebidas.txt
   menus/postres.txt
   ```

4. Ejecuta la aplicación:
   ```bash
   python app.py
   ```

---

## Uso de la aplicación

1. **Iniciar sesión** — Al abrir la app se solicita un usuario. Ingresa un nombre existente o regístrate con uno nuevo.
2. **Registrar una reserva** — Selecciona una fecha en el calendario y una hora entre 07:00 y 16:59. El sistema evita horarios duplicados.
3. **Registrar un pedido** — Consulta los menús en las pestañas y selecciona uno o más productos de la lista. Usa `Ctrl` (o `Cmd` en Mac) para selección múltiple.
4. **Consultar registros** — Los botones "Consultar reservas" y "Consultar pedidos" muestran los registros en el panel derecho. Esta función está restringida al usuario **admin**.

---

## Roles de usuario

| Usuario | Permisos |
|---|---|
| `admin` | Registrar pedidos y reservas + consultar todos los registros |
| `cliente` | Registrar pedidos y reservas únicamente |
| Cualquier nombre nuevo | Se registra como usuario regular (mismos permisos que `cliente`) |

---

## Almacenamiento de datos

Todos los datos se persisten en archivos de texto plano dentro de la carpeta `registros/`:

**`registros/reservas.txt`** — Una reserva por línea con el formato:
```
YYYY-MM-DD HH:MM|nombre_usuario
```
Ejemplo:
```
2025-06-15 09:30|admin
2025-06-16 14:00|cliente
```

**`registros/pedidos.txt`** — Un pedido por línea con el formato:
```
Pedido registrado por nombre_usuario: Producto1, Producto2
```
Ejemplo:
```
Pedido registrado por cliente: Cafe, Brownie
Pedido registrado por admin: Omelette, Chocolate, Galleta
```
