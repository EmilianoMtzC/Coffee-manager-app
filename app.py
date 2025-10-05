"""
Creación e implementación de interfaz para el codigo principal
"""
import sys
import datetime

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication

import login as lg
import reservas as rs
import pedidos as pd

class login_window(QtWidgets.QDialog):
    """ Clase que crea una subventana para que el usuario ingrese o registre un nombre de usuario."""

    def __init__(self, parent = None):
        super().__init__(parent)
        """
        Función principal de la subventana
        Continene todo el diseño de la ventana
        """

        self.setWindowTitle("Iniciar Sesion")       # NOMBRE DE LA VENTANA
        self.setModal(True)                         # CREA UNA VENTANA QUE NO PUEDE CERRARSE
        self.setFixedSize(360, 180)                 # TAMANHO DA LA VENTANA

        # =========== CAMPO DE ENTRADA ===========
        self.ingresar_usuario = QtWidgets.QLineEdit(self)               # CAMPO DE ENTRADA
        self.ingresar_usuario.setPlaceholderText("Ingrese usuario")     # MENSAJE DE AYUDA EN EL CAMPO DE ENTRADA

        # ============= BOTONES ==============
        btn_login = QtWidgets.QPushButton("Iniciar sesion")    # BOTON PARA INICIAR SESION
        btn_signup = QtWidgets.QPushButton("Registrarse")      # BOTON PARA REGISTRARSE
        btn_cancelar = QtWidgets.QPushButton("Cancelar")       # BOTON PARA CERRAR LA VENTANA

        # ========= ACCIONES VINCULADAS A LOS BOTONES =========
        btn_login.clicked.connect(self.solicitar_usuario)       # ACCION VINCULADA AL CLICKEAR EL BOTON INICIAR SESION  (FUNCION: solicitar_usuario)
        btn_signup.clicked.connect(self.registrar_usuario)      # ACCION VINCULADA AL CLICKEAR EL BOTON REGISTRARSE  (FUNCION: registrar_usuario)
        btn_cancelar.clicked.connect(self.reject)               # ACCION VINCULADA AL CLICKEAR EL BOTON CANCELAR (CERRAR LA VENTANA)

        # ========= DISEÑO DEL CAMPO DE ENTRADA =========
        forma = QtWidgets.QFormLayout()                         # LAYOUT PARA EL FORMULARIO DE ENTRADA DE DATOS
        forma.addRow("Usuario: ", self.ingresar_usuario)        # TEXTO QUE SE MOSTRA EN EL FORMULARIO DE ENTRADA DE DATOS

        # ======== DISEÑO DE LOS BOTONES ========
        botones = QtWidgets.QHBoxLayout()
        botones.addStretch(1)  # Añade espacio flexible a la izquierda
        botones.addWidget(btn_login)
        botones.addWidget(btn_signup)
        botones.addWidget(btn_cancelar)
        botones.addStretch(1)  # Añade espacio flexible a la derecha

        # ========= DISEÑO DEL LAYOUT PRINCIPAL =========
        layout = QtWidgets.QVBoxLayout(self)  # El layout principal en vertical
        layout.addStretch(1)  # Acomoda el contenido hacia el centro verticalmente
        layout.addLayout(forma)
        layout.addSpacing(10)  # Un pequeño espacio para que se vea más bonito
        layout.addLayout(botones)
        layout.addStretch(1)

        self.setLayout(layout)

    def solicitar_usuario(self):
        """
        Funcion encargada de validar si el usuario que se ingresa es válido
        """
        nombre = self.ingresar_usuario.text().strip()   # OBTIENE EL TEXTO Y LO LIMPIA (REMOVER ESPACIOS EN BLANCO)
        if not nombre:
            """ En caso de que el usuario no ingrese nada se muestra un mensaje de error."""
            QtWidgets.QMessageBox.warning(self, "Aviso", "El nombre no puede estar vacío.")
            return
        if nombre not in lg.USUARIOS:
            """ En caso de que el usuario no exista se muestra un mensaje de error"""
            QtWidgets.QMessageBox.warning(self, "Aviso", "Usuario no registrado.")
            return
        lg.USUARIO_ACTUAL = nombre  # SE UTILIZA EL USUARIO INGRESADO COMO USUARIO ACTUAL
        self.accept()

    def registrar_usuario(self):
        """
        Funcion creada para crear un nuevo usuario
        """
        nombre = self.ingresar_usuario.text().strip()
        if not nombre:
            """ En caso de que el usuario no ingrese nada se muestra un mensaje de error."""
            QtWidgets.QMessageBox.warning(self, "Aviso", "El nombre no puede estar vacío.")

        if nombre in lg.USUARIOS:
            """ En caso de que el usuario ya exista se muestra un mensaje de error"""
            QtWidgets.QMessageBox.warning(self, "Aviso", "Este usuario ya existe.")
            return

        lg.USUARIOS.append(nombre)      # SE AGREGA EL USUARIO NUEVO A LA LISTA DE USUARIOS
        lg.USUARIO_ACTUAL = nombre      # SE UTILIZA EL USUARIO NUEVO COMO USUARIO ACTUAL
        self.accept()                   # SE CERRA LA VENTANA

class reservas_window(QtWidgets.QDialog):
    """
    Clase para crear una ventana de registro de reservas.
    """
    def __init__(self, parent = None):
        """
        Aquí se encuentra todo el diseño de la ventana.
        """
        super().__init__(parent)
        # ======== TITULO DE LA VENTANA ========
        self.setWindowTitle("Registrar reserva")    # NOMBRE DE LA VENTANA
        self.setModal(True)                         # CREA UNA VENTANA QUE NO SE PUEDE CERRAR O MODFICAR

        # ======== WIDGETS PRINCIPALES ========
        self.calendario = QtWidgets.QCalendarWidget()                           # CREA UN WIDGET QCALENDAR (CALENDARIO)
        self.editar_hora = QtWidgets.QTimeEdit(QtCore.QTime.currentTime())      # CREA UN WIDGET QTIMEEDIT (HORA) Y SIRVE PARA MODIFICAR LA HORA Y EMPIEZA CON LA HORA ACTUAL
        self.editar_hora.setDisplayFormat("HH:mm")                              # FORMATO DE LA HORA PARA QUE SE MUESTRE EN EL WIDGET

        # ======== BOTONES ========
        btn_registrar = QtWidgets.QPushButton("Registrar reserva")      # BOTÓN PARA REGISTRAR LA RESERVA
        btn_cancelar = QtWidgets.QPushButton("Cancelar")                # BOTÓN PARA CERRAR LA VENTANA

        # ========= ACCIONES VINCULADAS A LOS BOTONES =========
        btn_registrar.clicked.connect(self.registrar_reserva)           # ACCIÓN VINCULADA AL CLICKEAR EL BOTÓN REGISTRAR RESERVA  (FUNCIÓN: registrar_reserva)
        btn_cancelar.clicked.connect(self.reject)                       # ACCIÓN VINCULADA AL CLICKEAR EN EL BOTÓN CANCELAR (CERRAR LA VENTANA)

        # ========= ORGANIZACIÓN DE LA VENTANA PRINCIPAL =========
        forma = QtWidgets.QFormLayout()             # LAYOUT PARA EL FORMULARIO DE ENTRADA DE DATOS
        forma.addRow("Fecha:", self.calendario)     # TEXTO QUE SE MOSTRA EN EL FORMULARIO DE ENTRADA DE DATOS
        forma.addRow("Hora:", self.editar_hora)     # TEXTO QUE SE MOSTRA EN EL FORMULARIO DE ENTRADA DE DATOS

        # ========= AGRUPACIÓN DE LOS BOTONES =========
        botones = QtWidgets.QHBoxLayout()           # LAYOUT PARA EL BOTÓN REGISTRAR Y CANCELAR
        botones.addWidget(btn_registrar)            # SE AÑADE EL BOTON REGISTRAR A LA VENTANA
        botones.addWidget(btn_cancelar)             # SE AÑADE EL BOTON CANCELAR A LA VENTANA

        # ========= CONFIGURACIÓN Y DISEÑO FINAL DE LA VENTANA =========
        layout = QtWidgets.QVBoxLayout(self)        # EL LAYOUT PRINCIPAL EN VERTICAL
        layout.addLayout(forma)                     # EL LAYOUT PARA EL FORMULARIO DE ENTRADA DE DATOS
        layout.addLayout(botones)                   # EL LAYOUT PARA LOS BOTONES REGISTRAR Y CANCELAR
        self.setLayout(layout)                      # VISUALIZA EL LAYOUT PRINCIPAL EN LA VENTANA

    def registrar_reserva(self):
        """
        Funcion encargada de registrar la reserva en el archivo reservas.py
        """
        usuario = lg.USUARIO_ACTUAL     # TOMA AL USUARIO ACTUAL (correcto)
        if not usuario:
            """ En caso de que no exista un usuario activo, se muestra un mensaje de error."""
            QtWidgets.QMessageBox.warning(self, "Error", "No hay usuario activo. Inicia sesión primero.")
            return

        # ======== OBTENCIÓN DE DATOS ==========
        fecha_qdate = self.calendario.selectedDate()    # OBTIENE LA FECHA SELECCIONADA EN EL CALENDARIO QDATE
        hora_qtime = self.editar_hora.time()            # OBTIENE LA HORA SELECCIONADA EN EL WIDGET QTIME

        # ========== UNIÓN DE TODOS LOS DATOS ==========
        fecha = datetime.datetime(
            fecha_qdate.year(),
            fecha_qdate.month(),
            fecha_qdate.day(),
            hora_qtime.hour(),
            hora_qtime.minute()
        )

        # ======== VALIDACIÓN DE HORARIOS ==========
        if not (rs.HORA_APERTURA <= fecha.time() < rs.HORA_CIERRE):
            """ En caso de que la hora no coincida con los horarios, se muestra un mensaje de error."""
            QtWidgets.QMessageBox.warning(self, "Error", "La hora debe estar dentro del horario (07:00 a 16:59).")
            return

        # ========== CONVIERTE LA FECHA A TEXTO ==========
        fecha_str = fecha.strftime("%Y-%m-%d %H:%M")

        # ============= COMPROBACIÓN DE FECHAS DUPLICADAS ==========
        if fecha_str in rs.RESERVAS:
            """ En caso de que se intente registrar una reserva con una fecha duplicada, se muestra un mensaje de error."""
            QtWidgets.QMessageBox.warning(self, "Error", "Esa fecha y hora ya están reservadas.")
            return

        # ========== REGISTRA LA RESERVA EN EL ARCHIVO ==========
        rs.guardar_reserva(fecha_str, usuario)              # SE GUARDA LA RESERVA EN EL ARCHIVO
        QtWidgets.QMessageBox.information(self, "Éxito", f"Reserva registrada para {usuario} el {fecha_str}")     # MENSAJE DE FINALIZACIÓN

class pedidos_window(QtWidgets.QDialog):
    """
    Clase para crear una ventana de registro de pedidos.
    """
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Registrar pedido")     # NOMBRE DE LA VENTANA
        self.setModal(True)                         # CREA UNA VENTANA QUE NO SE PUEDE CERRAR O MODFICAR
        self.setFixedSize(560, 540)                 # TAMAÑO DE LA VENTANA

        # ======== CONFIGURACIÓN DE LOS WIDGET/MENÚS =======
        self.tabs = QtWidgets.QTabWidget()              # WIDGET QUE GENERA UN "ÁREA" DONDE ESTARAN LOS MENÚS
        self.txt_des = QtWidgets.QPlainTextEdit()       # MENÚ DE DESAYUNOS
        self.txt_beb = QtWidgets.QPlainTextEdit()       # MENÚ DE BEBIDAS
        self.txt_pos = QtWidgets.QPlainTextEdit()       # MENÚ DE POSTRES

        # ========= CONFIGURACIÓN DE LOS TXT ==========
        for i in (self.txt_des, self.txt_beb, self.txt_pos):
            """ Deja como en solo lectura los textos. """
            i.setReadOnly(True)

        # ======= AÑADIR MENÚS A LA TABS =======
        self.tabs.addTab(self.txt_des, "Desayunos")
        self.tabs.addTab(self.txt_beb, "Bebidas")
        self.tabs.addTab(self.txt_pos, "Postres")

        # ======== BOTONES ========
        btn_registrar = QtWidgets.QPushButton("Registrar pedido")   # SE CREA UN BOTON PARA REGISTRAR EL PEDIDO
        btn_cancelar = QtWidgets.QPushButton("Cancelar")            # SE CREA UN BOTON PARA CERRAR LA VENTANA

        # ========= ACCIONES VINCULADAS A LOS BOTONES =========
        btn_registrar.clicked.connect(self.registrar_pedido)        # ACCIÓN VINCULADA AL CLICKEAR EL BOTÓN REGISTRAR PEDIDO  (FUNCIÓN: registrar_pedido)
        btn_cancelar.clicked.connect(self.reject)                   # ACCIÓN VINCULADA AL CLICKEAR EL BOTÓN CANCELAR (CERRAR LA VENTANA)

        # ========= DISEÑO DE LA VENTANA =========
        layout = QtWidgets.QVBoxLayout()                                # LAYOUT PRINCIPAL EN VERTICAL
        layout.addWidget(QtWidgets.QLabel("Menús (referencia):"))
        layout.addWidget(self.tabs)
        layout.addWidget(QtWidgets.QLabel("Selecciona productos (Ctrl/Cmd para múltiple):"))

        # ========= LISTA PARA SELECCIONAR PRODUCTOS =========
        self.lista = QtWidgets.QListWidget()
        self.lista.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)  # permite selección múltiple

        # Cargar productos
        for producto in sorted(pd.PRODUCTOS):
            self.lista.addItem(producto)

        # Añadir al layout
        layout.addWidget(QtWidgets.QLabel("Selecciona productos (Ctrl/Cmd para múltiple):"))
        layout.addWidget(self.lista)

        botones = QtWidgets.QHBoxLayout()
        botones.addWidget(btn_registrar)
        botones.addWidget(btn_cancelar)

        layout.addLayout(botones)
        self.setLayout(layout)

        self.cargar_textos()

    def cargar_textos(self):
        try:
            with open("menus/desayunos.txt", "r", encoding="utf-8") as f:
                self.txt_des.setPlainText(f.read())
        except FileNotFoundError:
            self.txt_des.setPlainText("Archivo no encontrado.")

        try:
            with open("menus/bebidas.txt", "r", encoding="utf-8") as f:
                self.txt_beb.setPlainText(f.read())
        except FileNotFoundError:
            self.txt_beb.setPlainText("Archivo no encontrado.")

        try:
            with open("menus/postres.txt", "r", encoding="utf-8") as f:
                self.txt_pos.setPlainText(f.read())
        except FileNotFoundError:
            self.txt_pos.setPlainText("Archivo no encontrado.")

    # En app.py, dentro de la clase pedidos_window
    def registrar_pedido(self):
        usuario = lg.USUARIO_ACTUAL  # Obtiene el usuario del módulo 'login' (correcto)
        if not usuario:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Debes iniciar sesión primero.")
            return
        # ...

        # Productos seleccionados
        seleccionados = [item.text() for item in self.lista.selectedItems()]
        if not seleccionados:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Debes seleccionar al menos un producto.")
            return

        # Guardar en memoria
        pd.PEDIDOS.append((usuario, seleccionados))

        # Guardar en archivo
        import os
        os.makedirs("registros", exist_ok=True)
        with open("registros/pedidos.txt", "a", encoding="utf-8") as f:
            f.write(f"Pedido registrado por {usuario}: {', '.join(seleccionados)}\n")

        QtWidgets.QMessageBox.information(self, "Éxito", "Pedido registrado correctamente.")
        self.accept()  # cierra la ventana

class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestor de reservas y pedidos") # Nombre de la ventana
        self.setFixedSize(QSize(820, 560)) # Tamaño de la ventana

        self.msj_usuario = QtWidgets.QLabel("Usuario: (Sin iniciar)")
        self.msj_usuario.setStyleSheet("font-weight: bold;")

        btn_login = QtWidgets.QPushButton("Iniciar/Cambiar usuario")
        btn_reserva = QtWidgets.QPushButton("Registrar reserva")
        btn_pedido = QtWidgets.QPushButton("Registrar pedido")
        btn_ver_reservas = QtWidgets.QPushButton("Consultar reservas")
        btn_ver_pedidos = QtWidgets.QPushButton("Consultar pedidos")
        btn_salir = QtWidgets.QPushButton("Salir")

        for i in (btn_login, btn_reserva, btn_pedido, btn_ver_reservas, btn_ver_pedidos, btn_salir):
            i.setMinimumWidth(36)

        btn_login.clicked.connect(self.cambiar_usuario)
        btn_reserva.clicked.connect(self.registrar_reserva)
        btn_pedido.clicked.connect(self.registrar_pedido)
        btn_ver_reservas.clicked.connect(self.consultar_reservas)
        btn_ver_pedidos.clicked.connect(self.consultar_pedidos)
        btn_salir.clicked.connect(QtWidgets.QApplication.instance().quit)

        acciones_group = QtWidgets.QGroupBox("Acciones")
        acciones_layout = QtWidgets.QVBoxLayout()
        acciones_layout.addWidget(btn_reserva)
        acciones_layout.addWidget(btn_pedido)
        acciones_group.setLayout(acciones_layout)

        consultas_group = QtWidgets.QGroupBox("Consultas")
        consultas_layout = QtWidgets.QVBoxLayout()
        consultas_layout.addWidget(btn_ver_reservas)
        consultas_layout.addWidget(btn_ver_pedidos)
        consultas_group.setLayout(consultas_layout)

        izq = QtWidgets.QVBoxLayout()
        izq.addWidget(self.msj_usuario)
        izq.addSpacing(8)
        izq.addWidget(btn_login)
        izq.addWidget(btn_reserva)
        izq.addWidget(btn_pedido)
        izq.addSpacing(8)
        izq.addWidget(btn_ver_reservas)
        izq.addWidget(btn_ver_pedidos)
        izq.addSpacing(1)
        izq.addWidget(btn_salir)

        self.panel_der = QtWidgets.QPlainTextEdit()
        self.panel_der.setReadOnly(True)
        self.panel_der.setPlainText("Lista de reservas y pedidos registrados:")

        central = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(central)
        layout.setContentsMargins(15, 15, 15, 15)  # Añade 15px de margen en todos los lados
        layout.setSpacing(15)  # Espacio entre el panel izquierdo y el derecho
        layout.addLayout(izq, 1)
        layout.addLayout(izq, 1)
        layout.addWidget(self.panel_der, 2)
        self.setCentralWidget(central)

        QtCore.QTimer.singleShot(0, self.cambiar_usuario)

    def actualizar_usuario(self):
        usuario = lg.USUARIO_ACTUAL or "Sin iniciar"
        self.msj_usuario.setText(f"Usuario: {usuario}")

    def cambiar_usuario(self):
        dialogo = login_window(self)
        dialogo.exec_()
        self.actualizar_usuario()

    def registrar_reserva(self):
        if not lg.USUARIO_ACTUAL:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Debe iniciar sesion primero.")
            self.cambiar_usuario()
            if not lg.USUARIO_ACTUAL:
                return
        dialogo = reservas_window(self)
        dialogo.exec_()

    def registrar_pedido(self):
        if not lg.USUARIO_ACTUAL:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Debe iniciar sesion primero.")
            self.cambiar_usuario()
            if not lg.USUARIO_ACTUAL:
                return
        dialogo = pedidos_window(self)
        dialogo.exec_()

    def consultar_reservas(self):
        rs.cargar_reservas()  # <- usar el módulo reservas
        self.panel_der.clear()

        if lg.USUARIO_ACTUAL != "admin":
            QtWidgets.QMessageBox.warning(self, "Aviso", "Debes ser administrador para consultar las reservas.")
            return

        if not rs.RESERVAS:
            self.panel_der.setPlainText("No hay reservas registradas.")
            return
        texto = "=== Reservas registradas ===\n"
        for i, (fecha, usuario) in enumerate(rs.RESERVAS.items(), start=1):
            texto += f"{i}. {fecha} | {usuario}\n"
        self.panel_der.setPlainText(texto)

    # En app.py, dentro de la clase main_window
    def consultar_pedidos(self):
        self.panel_der.clear()  # Limpia el panel de texto

        if lg.USUARIO_ACTUAL != "admin":
            QtWidgets.QMessageBox.warning(self, "Aviso", "Debes ser administrador para consultar los pedidos.")
            return

        try:
            # Abre y lee el archivo de registros directamente
            with open("registros/pedidos.txt", "r", encoding="utf-8") as archivo:
                lineas = [line.strip() for line in archivo if line.strip()]

            if not lineas:
                self.panel_der.setPlainText("No hay pedidos registrados.")
                return

            # Construye el texto para mostrarlo en la GUI
            texto = "=== Pedidos registrados ===\n"
            for i, linea in enumerate(lineas, start=1):
                texto += f"{i}. {linea}\n"

            # Asigna el texto al panel derecho
            self.panel_der.setPlainText(texto)

        except FileNotFoundError:
            # Si el archivo no existe, muéstralo en el panel
            self.panel_der.setPlainText("No hay pedidos registrados.")

def main ():
    app = QApplication(sys.argv)

    font = QFont("Roboto")  # Puedes usar fuentes como Roboto, Lato, Open Sans
    app.setFont(font)

    app.setStyleSheet("""
            QWidget {
                background-color: #2E3440; /* Fondo general oscuro */
                color: #ECEFF4;             /* Color de texto claro */
                font-family: Arial;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4C566A;
                border: 1px solid #5E81AC;
                padding: 8px;
                border-radius: 4px; /* Bordes redondeados */
            }
            QPushButton:hover {
                background-color: #5E81AC; /* Color al pasar el mouse */
            }
            QPushButton:pressed {
                background-color: #81A1C1; /* Color al presionar */
            }
            QLineEdit, QPlainTextEdit {
                background-color: #3B4252;
                border: 1px solid #4C566A;
                padding: 5px;
                border-radius: 4px;
            }
            QLabel {
                font-weight: bold;
            }
        """)

    window = main_window()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
