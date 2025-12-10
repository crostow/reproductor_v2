import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow
from Interfaz import Ui
from metodos import modulo
from metodos.theme_manager import ThemeManager
from metodos.system_tray import Bandeja_de_sistema

class Reproductor(QMainWindow):
    def __init__(self, parent=None):
        super(Reproductor, self).__init__(parent)

        self.ui = Ui.Interfaz_reproductor()
        self.ui.setupUi(self)

        # Instantiate ThemeManager
        self.theme_manager = ThemeManager(self.ui, self)

        # Se crea la instancia de la lógica y se pasa la interfaz y el theme_manager
        self.logica = modulo.Logica_reproductor(self.ui, self.theme_manager)

        # 4. Inicializar Bandeja de Sistema (Tray)
        # --- AQUÍ ESTABA EL PROBLEMA ---
        # Esta línea es la que hace que al cerrar se vaya al tray.
        # Guardamos la referencia en 'self.bandeja' para que no se borre de memoria.
        self.bandeja = Bandeja_de_sistema(self, self.logica)

        # Connect menu actions to ThemeManager
        self.ui.accion_claro.triggered.connect(lambda: self.theme_manager.aplicar_estilo("claro"))
        self.ui.accion_oscuro.triggered.connect(lambda: self.theme_manager.aplicar_estilo("oscuro"))
        
        # Connect icon actions (if they are separate in the menu)
        self.ui.iconos_claro.triggered.connect(lambda: self.theme_manager.aplicar_iconos("claro"))
        self.ui.iconos_oscuro.triggered.connect(lambda: self.theme_manager.aplicar_iconos("oscuro"))


        # Conectamos ambas señales a la funcion de actualizar el menu
        self.theme_manager.estilo_cambiado.connect(self.update_menu_checks)
        self.theme_manager.iconos_cambiados.connect(self.update_menu_checks)

        # Load initial preference
        self.theme_manager.load_user_preference()

    def update_menu_checks(self):
        # Obtenemos el estado actual del manager
        estilo_actual = self.theme_manager.get_current_style()
        iconos_actuales = self.theme_manager.get_current_icons()

        # Actualizamos los checks de Estilo
        self.ui.accion_claro.setChecked(estilo_actual == "claro")
        self.ui.accion_oscuro.setChecked(estilo_actual == "oscuro")

        # Actualizamos los checks de Iconos
        self.ui.iconos_claro.setChecked(iconos_actuales == "claro")
        self.ui.iconos_oscuro.setChecked(iconos_actuales == "oscuro")


if __name__=="__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("Interfaz/icon_barra.png"))

    repro = Reproductor()
    repro.show()
    sys.exit(app.exec())
