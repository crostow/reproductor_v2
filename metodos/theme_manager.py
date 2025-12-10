import os
from PySide6.QtCore import QObject, Signal, QSettings, QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication


class ThemeManager(QObject):
    # Emitimos señales separadas o una general cuando algo cambia
    estilo_cambiado = Signal(str)
    iconos_cambiados = Signal(str)

    def __init__(self, ui, parent=None):
        super().__init__(parent)
        self.ui = ui
        self.settings = QSettings("MiEmpresa", "MiReproductor")

        # Variables de estado separadas
        self._estilo_actual = "oscuro"
        self._iconos_actuales = "oscuro"

    def load_user_preference(self):
        """Carga las preferencias guardadas independientemente."""
        # Cargamos estilo
        estilo = self.settings.value("tema_estilo", "oscuro")
        self.aplicar_estilo(estilo)

        # Cargamos iconos
        iconos = self.settings.value("tema_iconos", "oscuro")
        self.aplicar_iconos(iconos)

    def aplicar_estilo(self, nombre_estilo):
        """Solo cambia el QSS (Colores)."""
        if self._estilo_actual == nombre_estilo and self.ui.centralwidget.styleSheet() != "":
            # Pequeña optimización: si ya es el estilo actual, no recargamos a menos que sea el inicio
            pass

        self._estilo_actual = nombre_estilo
        self._load_qss(nombre_estilo)

        self.settings.setValue("tema_estilo", nombre_estilo)
        self.estilo_cambiado.emit(nombre_estilo)

    def aplicar_iconos(self, nombre_set_iconos):
        """Solo cambia las imágenes de los iconos."""
        self._iconos_actuales = nombre_set_iconos

        self._update_icons_static()

        self.settings.setValue("tema_iconos", nombre_set_iconos)
        # Emitimos señal para que modulo.py actualice los dinámicos (Play/Volumen)
        self.iconos_cambiados.emit(nombre_set_iconos)

    def get_icon_path(self, icon_name):
        """Devuelve la ruta basada en el SET DE ICONOS seleccionado (no el estilo)."""
        return f":/{self._iconos_actuales}/{icon_name}"

    def get_current_style(self):
        return self._estilo_actual

    def get_current_icons(self):
        return self._iconos_actuales

    def _load_qss(self, theme_name):
        app = QApplication.instance()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_qss = os.path.join(base_dir, "Interfaz", "temas", theme_name, f"estilo_{theme_name}.qss")

        try:
            with open(ruta_qss, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Warning: QSS file not found: {ruta_qss}")

    def _update_icons_static(self):
        """Actualiza los botones estáticos con el set de iconos actual."""
        prefijo = f":/{self._iconos_actuales}/"

        botones = {
            self.ui.btn_stop: "boton-detener.png",
            self.ui.btn_anterior: "atras.png",
            self.ui.btn_siguiente: "siguiente.png",
            self.ui.btn_lp: "anadir-lista.png",
        }

        for btn, archivo in botones.items():
            btn.setIcon(QIcon(prefijo + archivo))
            btn.setIconSize(QSize(90, 90))  # Mantenemos el tamaño fijo que definimos antes