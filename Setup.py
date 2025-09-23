import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from Interfaz import Ui
from metodos import modulo


class Reproductor(QMainWindow):
    def __init__(self, parent=None):
        super(Reproductor, self).__init__(parent)

        self.ui = Ui.Interfaz_reproductor()
        self.ui.setupUi(self)

        # Se crea la instancia de la lógica y se pasa la interfaz
        self.logica = modulo.Logica_reproductor(self.ui)

if __name__=="__main__":
    app = QApplication(sys.argv)
    repro = Reproductor()
    repro.show()
    sys.exit(app.exec())