import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from Interfaz import Ui
from metodos import modulo, configuracion


class Reproductor(QMainWindow):
    def __init__(self, parent=None):
        super(Reproductor, self).__init__(parent)

        self.ui = Ui.Interfaz_reproductor()
        self.ui.setupUi(self)


        # Se crea la instancia de la lógica y se pasa la interfaz
        self.logica = modulo.Logica_reproductor(self.ui)

        tema_actual = configuracion.tema_guardado()
        if tema_actual == "claro":
            self.ui.accion_claro.setChecked(True)
        elif tema_actual == "oscuro":
            self.ui.accion_oscuro.setChecked(True)
        else:
            pass

if __name__=="__main__":
    app = QApplication(sys.argv)

    # Aplicar tema guardado antes de cerrar la ventana
    tema = configuracion.tema_guardado()
    configuracion.aplicar_tema(app, tema)

    repro = Reproductor()
    def cambiar_a_claro():
        configuracion.aplicar_tema(app, "claro")
        repro.ui.accion_claro.setChecked(True)
        repro.ui.accion_oscuro.setChecked(False)
    def cambiar_a_oscuro():
        configuracion.aplicar_tema(app, "oscuro")
        repro.ui.accion_oscuro.setChecked(True)
        repro.ui.accion_claro.setChecked(False)

    # Conectar las acciones
    repro.ui.accion_claro.triggered.connect(cambiar_a_claro)
    repro.ui.accion_oscuro.triggered.connect(cambiar_a_oscuro)
    repro.show()
    sys.exit(app.exec())
