from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QEvent, QTimer

class Bandeja_de_sistema():
    """
    controlador del icono en la bandeja del sistema para el reproductor
    se encarga de ocultar, mostrar, pausar y cerrar la aplicacion desde el tray
    """
    def __init__(self, ventana, logica):
        self.ventana = ventana
        self.logica = logica

        # creamos el icono del tray
        self.tray_icon = QSystemTrayIcon(self.ventana)
        self.tray_icon.setIcon(QIcon("Interfaz/icon_barra"))
        self.tray_icon.setToolTip("Reproductor de video")

        # menu contextual
        menu = QMenu()

        accion_mostrar = QAction("Mostrar", self.ventana)
        accion_mostrar.triggered.connect(self.mostrar_ventana)
        menu.addAction(accion_mostrar)

        accion_pausar = QAction("Pausar")
        accion_pausar.triggered.connect(self.pausar_video)
        menu.addAction(accion_pausar)

        accion_salir = QAction("Salir", self.ventana)
        accion_salir.triggered.connect(self.salir_app)
        menu.addAction(accion_salir)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self.icono_activado)

        self.tray_icon.show()
        self._conectar_eventos()


    def _conectar_eventos(self):
        # inyecta eventos personalizados para la ventana principal
        ventana_original_change = self.ventana.changeEvent
        ventana_original_close = self.ventana.changeEvent

        def nuevo_change_event(event):
            if event.type() == QEvent.WindowStateChange and self.ventana.isMinimized():
                QTimer.singleShot(0, self.ventana.hide)
                self.tray_icon.showMessage(
                    "Reproductor de Video",
                    "El reproductor sigue activo en la bandeja del sistema.",
                    QSystemTrayIcon.Information,
                    3000
                )
            ventana_original_change(event)

        def nuevo_close_event(event):
            event.ignore()
            self.ventana.hide()
            self.tray_icon.showMessage(
                "Reproductor de Video",
                "El reproductor sigue ejecutándose en segundo plano.",
                QSystemTrayIcon.Information,
                3000
            )

        self.ventana.changeEvent = nuevo_change_event
        self.ventana.closeEvent = nuevo_close_event

    def mostrar_ventana(self):
        self.ventana.showNormal()
        self.ventana.activateWindow()

    def pausar_video(self):
        if hasattr(self.logica, "reproductor"):
            self.logica.reproductor.pause()

    def salir_app(self):
        self.tray_icon.hide()
        QApplication.quit()

    def icono_activado(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.mostrar_ventana()