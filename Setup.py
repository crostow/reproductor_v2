import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow
from Interfaz import Ui
from metodos import modulo, configuracion
from metodos.system_tray import Bandeja_de_sistema

class Reproductor(QMainWindow):
    def __init__(self, parent=None):
        super(Reproductor, self).__init__(parent)

        self.ui = Ui.Interfaz_reproductor()
        self.ui.setupUi(self)

        # Se crea la instancia de la lógica y se pasa la interfaz
        self.logica = modulo.Logica_reproductor(self.ui)

        configuracion.conectar_cambio_tema(self.ui, self.logica)

        configuracion.conectar_cambio_iconos(self.ui)

        self.Bandeja = Bandeja_de_sistema(self, self.logica)


if __name__=="__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("Interfaz/icon_barra.png"))


    repro = Reproductor()
    # Aplicar tema guardado antes de cerrar la ventana
    tema = configuracion.tema_guardado()
    configuracion.aplicar_tema(app, tema)

    tema_iconos = configuracion.iconos_guardados()
    configuracion.conectar_cambio_iconos(repro.ui)

    repro.show()
    sys.exit(app.exec())
