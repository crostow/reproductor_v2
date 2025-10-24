import os
from PySide6.QtCore import QSettings, QSize
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtWidgets import QApplication


def aplicar_tema(app, nombre_tema):
    print(nombre_tema)
    """
    Aplica el QSS de un tema y guarda la elección en QSettings.
    """
    print("entra a cambiar el tema")
    # Construir ruta al QSS
    ruta_qss = os.path.join("Interfaz", "temas", nombre_tema, f"estilo_{nombre_tema}.qss")
    print(ruta_qss)
    # Aplicar QSS
    try:
        with open(ruta_qss, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
            print(f"Tema '{nombre_tema}' aplicado correctamente")
    except FileNotFoundError:
        print(f"No se encontró el archivo de estilo: {ruta_qss}")

    # Guardar elección en QSettings
    settings = QSettings("MiEmpresa", "MiReproductor")
    settings.setValue("tema", nombre_tema)

def tema_guardado():
    """
    Devuelve el tema guardado en QSettings, por defecto 'oscuro'.
    """
    print("si llama a este metodo")
    settings = QSettings("MiEmpresa", "MiReproductor")
    return settings.value("tema", "oscuro")

def conectar_cambio_tema(ui):
    """
    Conecta las acciones del menú (claro / oscuro) y actualiza su estado.
    """
    ui.accion_claro.triggered.connect(lambda: cambiar_tema(ui, "claro"))
    ui.accion_oscuro.triggered.connect(lambda: cambiar_tema(ui, "oscuro"))

    # Cargar estado inicial
    tema = tema_guardado()
    if tema == "claro":
        ui.accion_claro.setChecked(True)
        ui.accion_oscuro.setChecked(False)
    else:
        ui.accion_oscuro.setChecked(True)
        ui.accion_claro.setChecked(False)

def cambiar_tema(ui, nombre_tema):
    """
    Cambia el tema en tiempo real, aplica el QSS y guarda la preferencia.
    """
    app = QApplication.instance()
    aplicar_tema(app, nombre_tema)

    # Actualizar checks en el menú
    if nombre_tema == "claro":
        ui.accion_claro.setChecked(True)
        ui.accion_oscuro.setChecked(False)
    else:
        ui.accion_oscuro.setChecked(True)
        ui.accion_claro.setChecked(False)


def aplicar_iconos(ui, tema):
    """
    Cambia los iconos de los botones según el tema (claro/oscuro) usando los recursos compilados (iconos_rc.py).
    """

    guardar_iconos(tema)
    # Prefijo según el tema
    prefijo = f":/{tema}/"  # Ej: ":/claro/" o ":/oscuro/"

    # Botones principales
    botones = {
        ui.btn_play: "boton-de-play.png",
        ui.btn_stop: "boton-detener.png",
        ui.btn_anterior: "atras.png",
        ui.btn_siguiente: "siguiente.png",
        ui.btn_lp: "anadir-lista.png",
    }

    for btn, archivo in botones.items():
        btn.setIcon(QIcon(prefijo + archivo))
        btn.setIconSize(QSize(90, 90))

    # Icono de volumen
    ruta_vol = prefijo + "volumen_1.png"
    pix = QPixmap(ruta_vol)
    scaled_pix = pix.scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    ui.lbl_volumen.setPixmap(scaled_pix)

def conectar_cambio_iconos(ui):
    """
    Conecta las acciones del menú (claro / oscuro) y actualiza su estado.
    """
    ui.iconos_claro.triggered.connect(lambda: aplicar_iconos(ui, "claro"))
    ui.iconos_oscuro.triggered.connect(lambda: aplicar_iconos(ui, "oscuro"))

    # Cargar estado inicial
    # tema = tema_guardado()
    tema = iconos_guardados()
    aplicar_iconos(ui, tema)
    if tema == "claro":
        ui.iconos_claro.setChecked(True)
        ui.iconos_oscuro.setChecked(False)
    elif tema == "oscuro":
        ui.iconos_oscuro.setChecked(True)
        ui.iconos_claro.setChecked(False)
    else:
        pass

def guardar_iconos(tema):
    settings = QSettings("MiEmpresa", "MiReproductor")
    settings.setValue("iconos", tema)

def iconos_guardados():
    settings = QSettings("MiEmpresa", "MiReproductor")
    return settings.value("iconos", "oscuro")  # Por defecto oscuro
