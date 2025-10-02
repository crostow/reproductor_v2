from PySide6.QtCore import Qt, QSize
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
        MainWindow.resize(800, 300)

        # widget central
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # layout principla
        self.layout_horizontal = QVBoxLayout(self.centralwidget)



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
        # le damos css temporal para ver que se vayan creando bien
        self.wdg_superior.setStyleSheet("background-color: rgb(150, 150, 150);")  # Color claro

        # asignamos el tipo de layout que tendra
        self.layout_wdg_superior = QHBoxLayout(self.wdg_superior)

        # crearemos 2 widget mas uno para la lista de reproduccion y otro para el video 
        self.wdg_lista = QListWidget()
        self.wdg_lista.setMinimumHeight(300)
        self.wdg_lista.setMaximumWidth(300)
        # le damos css temporal para ver que se vayan creando bien
        self.wdg_lista.setStyleSheet("background-color: rgb(130, 130, 130);")


        # creamos el widget de video
        self.wdg_video = QVideoWidget()
        self.audio_output = QAudioOutput()

        # agregamos los widgets creados al layout del widget superior
        self.layout_wdg_superior.addWidget(self.wdg_lista)
        self.layout_wdg_superior.addWidget(self.wdg_video)
#================================================================================


####### widget inferior (controles y sliders)
        self.wdg_inferior = QWidget()
        self.wdg_inferior.setMinimumHeight(300)
        self.wdg_inferior.setMaximumHeight(300)
        # le damos css temporal para ver que se vayan creando bien
        self.wdg_inferior.setStyleSheet("background-color: rgb(200, 200, 200);")  # Color claro
        self.layout_wdg_inferior = QVBoxLayout(self.wdg_inferior)

        # creamos los widget para el controles del reproductor e informacion del video

        # widget que contendra tiempo transcurrido, slider de avance y tiempo de duracion
        self.wdg_info = QWidget()
        # le damos css temporal para ver que se vayan creando bien
        self.wdg_info.setStyleSheet("background-color: rgb(136, 75, 200);")
        self.wdg_info.setMaximumHeight(150)
        self.layout_info = QHBoxLayout(self.wdg_info)

        # creamos los elementos mencionados informacion del video
        self.lbl_tiempo = QLabel()
        self.lbl_tiempo.setText("00:00:00")

        self.sld_avance = QSlider(Qt.Horizontal)


        self.lbl_tiempo_total = QLabel()
        self.lbl_tiempo_total.setText("00:00:00")

        self.layout_info.addWidget(self.lbl_tiempo)
        self.layout_info.addWidget(self.sld_avance)
        self.layout_info.addWidget(self.lbl_tiempo_total)


        # creamos el widget que contrenda los botones de control del reproductor
        self.wdg_controles = QWidget()
        # le damos css temporal para ver que se vayan creando bien

        self.wdg_controles.setStyleSheet("background-color: rgb(200, 189, 10);")
        self.wdg_controles.setMinimumHeight(150)
        self.layout_controles = QHBoxLayout(self.wdg_controles)

        # creamos los botones de control
        self.btn_lp = QPushButton()
        self.btn_lp.setFixedSize(100, 100)
        self.btn_lp.setIcon(QIcon(":/anadir-lista.png"))
        self.btn_lp.setIconSize(QSize(90, 90))


        self.btn_play = QPushButton()
        self.btn_play.setFixedSize(100, 100)
        self.btn_play.setIcon(QIcon(":/boton-de-play.png"))
        self.btn_play.setIconSize(QSize(90, 90))


        self.btn_anterior = QPushButton()
        self.btn_anterior.setFixedSize(100, 100)
        self.btn_anterior.setIcon(QIcon(":/atras.png"))
        self.btn_anterior.setIconSize(QSize(90, 90))

        self.btn_stop = QPushButton()
        self.btn_stop.setFixedSize(100, 100)
        self.btn_stop.setIcon(QIcon(":/boton-detener.png"))
        self.btn_stop.setIconSize(QSize(90, 90))

        self.btn_siguiente = QPushButton()
        self.btn_siguiente.setFixedSize(100, 100)
        self.btn_siguiente.setIcon(QIcon(":/siguiente.png"))
        self.btn_siguiente.setIconSize(QSize(90, 90))

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.lbl_volumen = QLabel()
        self.lbl_volumen.setFixedSize(100, 100)
        pix =QPixmap(":/volumen_1.png")
        max_icon = 90
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
        self.vol_bar.setFixedSize(150, 30)

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

