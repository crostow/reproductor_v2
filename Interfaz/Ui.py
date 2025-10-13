from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QPixmap, QAction
from PySide6.QtMultimedia import QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QSlider, QPushButton, QSizePolicy, \
    QMenuBar
import iconos_rc
class Interfaz_reproductor(object):
    def setupUi(self,MainWindow):

        # se le asigna un nombre al mainwindow
        MainWindow.setObjectName("MainWindow")

        # se le da un tamaño(ancho - alto )
        MainWindow.resize(550, 300)

        # widget central
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # layout principla
        self.layout_horizontal = QVBoxLayout(self.centralwidget)
        self.layout_horizontal.setContentsMargins(4,0,4,4)


######## menu  y barar inferior
        # creamos la barra de menu
        self.menu_bar = QMenuBar(MainWindow)
        # la enviamos al main window
        MainWindow.setMenuBar(self.menu_bar)

        # creamos el menu archivo
        self.menu_archivo = self.menu_bar.addMenu("Archivo")  # ✅ guardamos en otra variable

        # Crear acción "Abrir"
        self.accion_abrir = QAction("Abrir", MainWindow)

        # Agregar acción al menú
        self.menu_archivo.addAction(self.accion_abrir)
# ================================================================================

######## widget superior (reproductor y lista de reproduccion)
        self.wdg_superior = QWidget()
        self.wdg_superior.setStyleSheet("border:1px solid #000000")
        # le damos css temporal para ver que se vayan creando bien
        # self.wdg_superior.setStyleSheet("background-color: rgb(150, 150, 150);")  # Color claro

        # asignamos el tipo de layout que tendra
        self.layout_wdg_superior = QHBoxLayout(self.wdg_superior)
        self.layout_wdg_superior.setContentsMargins(0,0,0,0)
        self.layout_wdg_superior.setSpacing(0)

        # crearemos 2 widget mas uno para la lista de reproduccion y otro para el video 
        self.wdg_lista = ListaVideos()
        # self.wdg_lista = QListWidget()
        self.wdg_lista.setMinimumHeight(300)
        self.wdg_lista.setMaximumWidth(300)
        # le damos css temporal para ver que se vayan creando bien
        self.wdg_lista.setStyleSheet("background-color: rgba(0, 0, 0, 50);")


        # creamos el widget de video
        self.wdg_video = QVideoWidget()
        self.audio_output = QAudioOutput()

        # agregamos los widgets creados al layout del widget superior
        self.layout_wdg_superior.addWidget(self.wdg_lista)
        self.layout_wdg_superior.addWidget(self.wdg_video)
#================================================================================


####### widget inferior (controles y sliders)
        # variables para los controles
        margen_bot = 0
        tam_btn = 35
        tam_icon = tam_btn - 10
        margen_btn = 0
        h_sld_tiempo = 30
        margen_sld_tiempo = 0
        spacec = 0

        # variables para los controles
        self.wdg_inferior = QWidget()
        # self.wdg_inferior.setMinimumHeight(tam_btn + (margen_btn*2) + h_sld_tiempo + (margen_sld_tiempo*2))
        print("tam bot", (tam_btn + (margen_btn*2) + h_sld_tiempo + (margen_sld_tiempo*2)))
        self.wdg_inferior.setMaximumHeight(tam_btn + (margen_btn*2) + h_sld_tiempo + (margen_sld_tiempo*2)+spacec)
        # le damos css temporal para ver que se vayan creando bien
        self.wdg_inferior.setStyleSheet("background-color: rgb(200, 200, 200);")  # Color claro
        self.layout_wdg_inferior = QVBoxLayout(self.wdg_inferior)
        self.layout_wdg_inferior.setContentsMargins(margen_bot, margen_bot, margen_bot, margen_bot)
        self.layout_wdg_inferior.setSpacing(spacec)

        # creamos los widget para el controles del reproductor e informacion del video

        # widget que contendra tiempo transcurrido, slider de avance y tiempo de duracion
        self.wdg_info = QWidget()
        # le damos css temporal para ver que se vayan creando bien
        self.wdg_info.setStyleSheet("background-color: rgb(136, 75, 200);")
        self.wdg_info.setMaximumHeight(h_sld_tiempo + (margen_sld_tiempo*2))
        self.layout_info = QHBoxLayout(self.wdg_info)

        # creamos los elementos mencionados informacion del video
        self.lbl_tiempo = QLabel()
        self.lbl_tiempo.setText("00:00:00")
        self.lbl_tiempo.setStyleSheet("font-size:12pt;")

        self.sld_avance = QSlider(Qt.Horizontal)


        self.lbl_tiempo_total = QLabel()
        self.lbl_tiempo_total.setText("00:00:00")
        self.lbl_tiempo_total.setStyleSheet("font-size:12pt;")

        self.layout_info.addWidget(self.lbl_tiempo)
        self.layout_info.addWidget(self.sld_avance)
        self.layout_info.addWidget(self.lbl_tiempo_total)
        self.layout_info.setContentsMargins(0,0,0,0)


        # creamos el widget que contrenda los botones de control del reproductor
        self.wdg_controles = QWidget()
        # le damos css temporal para ver que se vayan creando bien

        self.wdg_controles.setStyleSheet("background-color: rgb(200, 189, 10);")
        self.wdg_controles.setMaximumHeight(tam_btn + (margen_btn*2))
        self.layout_controles = QHBoxLayout(self.wdg_controles)
        self.layout_controles.setContentsMargins(margen_btn, margen_btn, margen_btn, margen_btn)

        # creamos los botones de control
        self.btn_lp = QPushButton()
        self.btn_lp.setFixedSize(tam_btn, tam_btn)
        self.btn_lp.setIcon(QIcon(":/anadir-lista.png"))
        self.btn_lp.setIconSize(QSize(tam_icon, tam_icon))


        self.btn_play = QPushButton()
        self.btn_play.setFixedSize(tam_btn, tam_btn)
        self.btn_play.setIcon(QIcon(":/boton-de-play.png"))
        self.btn_play.setIconSize(QSize(tam_icon, tam_icon))


        self.btn_anterior = QPushButton()
        self.btn_anterior.setFixedSize(tam_btn, tam_btn)
        self.btn_anterior.setIcon(QIcon(":/atras.png"))
        self.btn_anterior.setIconSize(QSize(tam_icon, tam_icon))

        self.btn_stop = QPushButton()
        self.btn_stop.setFixedSize(tam_btn, tam_btn)
        self.btn_stop.setIcon(QIcon(":/boton-detener.png"))
        self.btn_stop.setIconSize(QSize(tam_icon, tam_icon))

        self.btn_siguiente = QPushButton()
        self.btn_siguiente.setFixedSize(tam_btn, tam_btn)
        self.btn_siguiente.setIcon(QIcon(":/siguiente.png"))
        self.btn_siguiente.setIconSize(QSize(tam_icon, tam_icon))

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.lbl_volumen = QLabel()
        self.lbl_volumen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_volumen.setFixedSize(tam_btn, tam_btn)
        # self.lbl_volumen.setStyleSheet("background-color: #ff0000;")
        pix =QPixmap(":/volumen_1.png")
        max_icon = tam_icon
        scaled_pix = pix.scaled(
            max_icon, max_icon,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.lbl_volumen.setPixmap(scaled_pix)

        # barra de sonido
        self.vol_bar = QSlider(Qt.Horizontal)
        self.vol_bar.setRange(0, 100) # volumen de o a 100
        self.vol_bar.setValue(50) # valor inicial
        self.vol_bar.setTickInterval(10)  # marcas cada 10 unidades
        self.vol_bar.setTickPosition(QSlider.TicksBelow)  # marcas abajo
        self.vol_bar.setFixedSize(150, tam_btn)

        # agregamos los botones al layout
        self.layout_controles.addWidget(self.btn_lp)
        self.layout_controles.addWidget(self.btn_play)
        self.layout_controles.addWidget(self.btn_anterior)
        self.layout_controles.addWidget(self.btn_stop)
        self.layout_controles.addWidget(self.btn_siguiente)
        self.layout_controles.addWidget(spacer)
        self.layout_controles.addWidget(self.lbl_volumen)
        self.layout_controles.addWidget(self.vol_bar)

        # agregamos los widget contenedores
        self.layout_wdg_inferior.addWidget(self.wdg_info)
        self.layout_wdg_inferior.addWidget(self.wdg_controles)

#==============================================================================

        # agregamos los widget a layout principal
        self.layout_horizontal.addWidget(self.wdg_superior)
        self.layout_horizontal.addWidget(self.wdg_inferior)
        
        # mandamos el widget central
        MainWindow.setCentralWidget(self.centralwidget)

        # self.btn_lp.setFlat(True)
        # self.btn_play.setFlat(True)
        # self.btn_anterior.setFlat(True)
        # self.btn_siguiente.setFlat(True)
        # self.btn_stop.setFlat(True)

        # MainWindow.setStyleSheet("background-color: red")
        self.wdg_lista.setStyleSheet("""
    /* 1. ESTILO BASE DE LA BARRA (TRACK) */
    QScrollBar:horizontal {
        border: 1px solid #101010;       /* Borde sutil */
        background: #2D2D2D;             /* Fondo de la barra */
        height: 12px;                    /* Altura de la barra */
        /* ELIMINA LOS MÁRGENES: Esto asegura que el track ocupe todo el ancho */
        margin: 0px 0px 0px 0px; 
        border-radius: 6px;
    }

    /* 2. OCULTAR EL BOTÓN IZQUIERDO (SUB-LINE) */
    QScrollBar::sub-line:horizontal {
        border: none;
        width: 0px;
        height: 0px;
        background: none;
    }

    /* 3. OCULTAR EL BOTÓN DERECHO (ADD-LINE) */
    QScrollBar::add-line:horizontal {
        border: none;
        width: 0px;
        height: 0px;
        background: none;
    }

    /* ----------------------------------------------- */
    /* 4. ESTILO DEL CONTROL DESLIZANTE (HANDLE) */
    /* ----------------------------------------------- */
    QScrollBar::handle:horizontal {
        background: #101010;             /* Gris plomo para el control */
        min-width: 20px;
        border-radius: 5px;
        border: 1px solid #303030;
    }

    /* Estilo del Handle al pasar el ratón (HOVER) */
    QScrollBar::handle:horizontal:hover {
        background: #000000;             /* Gris plomo más claro */
    }
""")
        

    def setBackgroundColor(self, bg:str):
        """asignar color de fondo al player(bg)"""
        self.centralwidget.setStyleSheet(f"background-color: {bg}")
        self.wdg_info.setStyleSheet(f"background-color: {bg}")
        self.wdg_controles.setStyleSheet(f"background-color: {bg}")
        self.menu_bar.setStyleSheet(f"background-color: {bg}")


class ListaVideos(QListWidget):
    archivos_dropeados = Signal(list)  # señal que emitirá lista de rutas
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        # self.setStyleBar()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            archivos = []
            for url in event.mimeData().urls():
                archivo = url.toLocalFile()
                if archivo:
                    archivos.append(archivo)
            if archivos:
                self.archivos_dropeados.emit(archivos)  # emitimos la señal con la lista
            event.acceptProposedAction()
        else:
            event.ignore()

    def setStyleBar(self):
        self.setStyleSheet("""
    /* 1. ESTILO BASE DEL WIDGET (el área de la barra) */
    QListWidget {
        background-color: #2D2D2D; /* Gris muy oscuro, fondo de la barra */
        border: 1px solid #444444; /* Borde gris oscuro */
        outline: 0; /* Importante para eliminar el foco por defecto */
    }

    /* 2. ESTILO DE LOS ÍTEMS NORMALES */
    QListWidget::item {
        background-color: transparent; /* Usa el fondo del widget */
        color: #CCCCCC; /* Texto gris claro */
        padding: 5px; /* Espacio interno para que se vean mejor */
        margin: 2px 0; /* Pequeña separación entre ítems */
    }

    /* 3. ESTILO DE LOS ÍTEMS AL PASAR EL RATÓN */
    QListWidget::item:hover {
        background-color: #3A3A3A; /* Un gris ligeramente más claro que el fondo base */
        color: #FFFFFF; /* Texto blanco */
    }

    /* 4. ESTILO DE LOS ÍTEMS SELECCIONADOS */
    QListWidget::item:selected {
        background-color: #606060; /* Gris plomo destacado para la selección */
        color: #FFFFFF; /* Texto blanco para buen contraste */
        border: 1px solid #777777; /* Borde sutil para resaltar aún más */
        border-radius: 3px;
    }

    /* 5. ESTILO ADICIONAL: Barra de desplazamiento (Scrollbar) si es visible */
    QScrollBar:vertical {
        border: 1px solid #2D2D2D;
        background: #ff0000; /* Fondo de la barra de desplazamiento */
        width: 10px;
        margin: 0px 0px 0px 0px;
    }
""")
