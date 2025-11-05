from PySide6.QtCore import QUrl, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon, Qt, QPixmap, QImage
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
import os
import cv2
# import configuracion
from PySide6.QtWidgets import QListWidgetItem, QFileDialog, QMessageBox

from metodos import configuracion
from metodos.configuracion import aplicar_tema


class Logica_reproductor:
    def __init__(self, ui):
        # cargamos la interfaz en la variable self.ui
        self.ui = ui


        # designamos la lista para que acepte arrastar y pegar
        self.ui.wdg_lista.setAcceptDrops(True)
        # self.lista_videos.setAcceptDrops(True)

        # verificamos que todo se inicie correctamente
        self.limpiar_interfaz()

        # lista de rutas completas
        self.lista_reproduccion = []
        self.indice_actual = -1

        # creamos el reproductor
        self.creacion_reproductor()


        # ejecutamos una señal para cuando se arrasten los archivos se ejecute un metodo
        self.ui.wdg_lista.archivos_dropeados.connect(self.agregar_archivos)
        # señal cuando cambia el reproductor de duracion
        self.reproductor.durationChanged.connect(self.mostrar_info_video)
        # señal para actualizar la posicion del slider
        self.reproductor.positionChanged.connect(self.actualizar_posicion)
        # señal para mover el video cuando el usuario arrastra el slider
        self.ui.sld_avance.sliderMoved.connect(self.cambiar_posicion)
        # señal para hacer doble click en la lr y reproducir archivo
        self.ui.wdg_lista.itemDoubleClicked.connect(self.reproducir_item)
        # Conectar la acción a tu metodo
        self.ui.accion_abrir.triggered.connect(self.abrir_archivo)
        # conectamos el boton de play para buscar archivos tambien
        # self.ui.btn_play.clicked.connect(self.abrir_archivo)
        # conectar slider de volumen
        self.ui.vol_bar.valueChanged.connect(self.mod_volumen)
        # conectar btn_lp a metodo para ocultar la lp
        self.ui.btn_lp.clicked.connect(self.lp_cambio)
        # detectar si el reproductor termina
        self.reproductor.mediaStatusChanged.connect(self.revisar_final)
        # señal para pausar video
        self.ui.btn_play.clicked.connect(self.play_pausa)
        # señal para detener el video
        self.ui.btn_stop.clicked.connect(self.stop)
        # señal para video siguiente
        self.ui.btn_siguiente.clicked.connect(self.siguiente_video)
        # señal para video anterior
        self.ui.btn_anterior.clicked.connect(self.anterior_video)
        # señal para detectar algun error al reproducir el video y mandar mensaje de error
        self.reproductor.errorOccurred.connect(self.manejar_error)
        # señal para detectar estado de errorerror al reproducir el video y mandar mensaje de error
        self.reproductor.mediaStatusChanged.connect(self.verificar_estado)

    def verificar_estado(self, status):
        if status == QMediaPlayer.InvalidMedia:
            QMessageBox.critical(
                None,
                "Archivo no válido",
                "El archivo seleccionado no es un video válido o está dañado."
            )
        elif status == QMediaPlayer.NoMedia:
            QMessageBox.information(
                None,
                "Sin medios",
                "No hay ningún video cargado para reproducir."
            )

    def manejar_error(self, error, errorString):
        if error != self.reproductor.NoError:
            QMessageBox.warning(
                None,
                "Error de reproducción",
                f"No se pudo reproducir el video.\n\nDetalles: {errorString}"
            )
            # saltar al siguiente video
            self.indice_actual += 1
            if self.indice_actual < len(self.lista_reproduccion):
                self.reproducir_video()
            else:
                self.indice_actual = -1

    def siguiente_video(self):
        #"Reproduce el siguiente video en la lista si existe
        if self.indice_actual + 1 < len(self.lista_reproduccion):
            self.indice_actual += 1
            self.reproducir_video()
        else:
            print("Fin de la lista de reproducción")

    def anterior_video(self):
        #Reproduce el video anterior si existe
        if self.indice_actual > 0:
            self.indice_actual -= 1
            self.reproducir_video()
        else:
            print("Inicio de la lista de reproducción")

    def actualizar_botones(self):
        # actualiza los botones cuando detecta cambios posicion en la lista de reproduccion
        self.ui.btn_anterior.setEnabled(self.indice_actual > 0)
        self.ui.btn_siguiente.setEnabled(self.indice_actual < len(self.lista_reproduccion) - 1)

    def stop(self):
        # desactiva los botones cuando se detenie el video
        self.reproductor.stop()
        self.ui.btn_play.setIcon(QIcon(":/boton-de-play.png"))
        self.ui.btn_play.setEnabled(False)
        self.ui.btn_stop.setEnabled(False)
        self.ui.btn_siguiente.setEnabled(False)
        self.ui.btn_anterior.setEnabled(False)

    def play_pausa(self):
        tema = configuracion.iconos_guardados()
        prefijo = f":/{tema}/"  # Ej: ":/claro/" o ":/oscuro/"
        print(prefijo)
        # funcion para el cambio de estado del boton pausa
        estado_repro = self.reproductor.playbackState()
        print(estado_repro)
        if estado_repro == QMediaPlayer.PlayingState:
            self.ui.btn_play.setIcon(QIcon(prefijo +"boton-de-play.png"))
            self.reproductor.pause()
        elif estado_repro == QMediaPlayer.PausedState:
            self.ui.btn_play.setIcon(QIcon(prefijo + "pausa.png"))
            # self.ui.btn_play.setIcon(QIcon(":/pause.png"))
            self.reproductor.play()

    def revisar_final(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.indice_actual+= 1
            if self.indice_actual < len(self.lista_reproduccion):
                self.reproducir_video()

    def lp_cambio(self):
        # tomamos el valor del ancho actual de la lp
        ancho_actual = self.ui.wdg_lista.width()

        # creamos animacion sobre maximunwidth
        self.animacion = QPropertyAnimation(self.ui.wdg_lista, b"maximumWidth")
        # duracion de la animacion
        self.animacion.setDuration(300)
        self.animacion.setEasingCurve(QEasingCurve.InOutQuad)

        # definimos si se va a cerrar o a mostrarse
        if ancho_actual > 0:
            self.animacion.setStartValue(ancho_actual)
            self.animacion.setEndValue(0)
        else:
            self.animacion.setStartValue(0)
            self.animacion.setEndValue(300)
        self.animacion.start()

    def mod_volumen(self, valor):
        tema = configuracion.iconos_guardados()
        prefijo = f":/{tema}/"  # Ej: ":/claro/" o ":/oscuro/"
        print(prefijo)

        # cabio de valor de audio dependiendo el valor del slider
        self.salida_audio.setVolume(valor/100)
        if valor <= 100 and valor >= 80:
            print("alto")
            pix = QPixmap(prefijo + "volumen_2.png")
            max_icon = 90
            scaled_pix = pix.scaled(
                max_icon, max_icon,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.ui.lbl_volumen.setPixmap(scaled_pix)
        elif valor <= 80 and valor >0:
            print("medio")
            pix = QPixmap(prefijo + "volumen_1.png")
            max_icon = 90
            scaled_pix = pix.scaled(
                max_icon, max_icon,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.ui.lbl_volumen.setPixmap(scaled_pix)
        elif valor == 0:
            print("bajo")
            pix = QPixmap(prefijo + "silencio.png")
            max_icon = 90
            scaled_pix = pix.scaled(
                max_icon, max_icon,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.ui.lbl_volumen.setPixmap(scaled_pix)


    def reproducir_item(self, item):
        # metodo que se encarga cuando da doble click en la lp haga elk cambio
        self.reproductor.stop()
        # detenemos el reproductor
        ruta = item.data(Qt.UserRole)
        # tomamos la ruta del item
        if ruta:
            self.indice_actual = self.lista_reproduccion.index(ruta)
            self.reproducir_video()




    def abrir_archivo(self, archivo=None):
        archivos, _ = QFileDialog.getOpenFileNames(
            None, "Selecciona el video",
            os.path.expanduser("~"),
            "Videos (*.mp4 *.avi *.mkv *.mov)"
        )

        if archivos:
            self.agregar_archivos(archivos)

    def generar_miniatura(self, ruta):
        # generamos una miniatura el el video para mostralo en la lista de reproduccion
        captura = cv2.VideoCapture(ruta)
        exito, frame = captura.read()
        captura.release()

        if not exito:
            return None

        # convertir de  bgr(opencv) a rgb(Qt)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        alto, ancho, canal = frame_rgb.shape
        bytes = canal * ancho
        imagen = QImage(frame_rgb.data, ancho, alto, bytes, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(imagen).scaled(100, 60)
        print("entra a la miniaturaA")
        return QIcon(pixmap)

    def agregar_archivos(self, archivos):
        formatos_permitidos = (".mp4", ".avi", ".mkv", ".mov")

        # print("dialog",directorio_archivo)
        for  directorio_archivo in archivos:
            # Convertimos a minúsculas y verificamos la extensión
            if not directorio_archivo.lower().endswith(formatos_permitidos):
                continue  # salta archivos no permitidos

            if directorio_archivo in self.lista_reproduccion:
                continue  # evita duplicados

            if directorio_archivo in archivos:
                self.lista_reproduccion.append(directorio_archivo)
                icono = self.generar_miniatura(directorio_archivo)
                nombre_archivo = os.path.basename(directorio_archivo)
                # agregamos el nombre del archivo a la lista de reproduccion
                item = QListWidgetItem(icono, nombre_archivo)
                item.setData(Qt.UserRole, directorio_archivo)

                self.ui.wdg_lista.addItem(item)

                if self.reproductor.mediaStatus() != QMediaPlayer.LoadedMedia and self.indice_actual == -1:
                    self.indice_actual = len(self.lista_reproduccion) - 1
                    self.reproducir_video()
            self.actualizar_botones()

    def reproducir_video(self):
        if 0 <= self.indice_actual < len(self.lista_reproduccion):
            ruta = self.lista_reproduccion[self.indice_actual]
            # conectamos el reproductor widget creado en la interfaz
            self.reproductor.setVideoOutput(self.ui.wdg_video)
            # asignamos el reproductor
            self.reproductor.setSource(QUrl.fromLocalFile(ruta))
            self.reproductor.play()
            self.activar_btns()
            self.actualizar_botones()
            self.ui.wdg_lista.setCurrentRow(self.indice_actual)

    def activar_btns(self):
        tema = configuracion.iconos_guardados()
        prefijo = f":/{tema}/"  # Ej: ":/claro/" o ":/oscuro/"
        print(prefijo)
        self.ui.btn_play.setEnabled(True)
        self.ui.btn_play.setIcon(QIcon(prefijo +"pausa.png"))
        self.ui.btn_anterior.setEnabled(True)
        self.ui.btn_stop.setEnabled(True)
        self.ui.btn_siguiente.setEnabled(True)

    def cambiar_posicion(self, posicion):
        self.reproductor.setPosition(posicion)

    def actualizar_posicion(self, posicion):
        self.ui.sld_avance.setValue(posicion)
        # Qt entrega la duración en milisegundos → lo pasamos a segundos
        duracion_segundos = posicion // 1000

        # Convertimos a horas, minutos y segundos
        horas = duracion_segundos // 3600
        minutos = int(duracion_segundos // 60)
        segundos = int(duracion_segundos % 60)
        self.ui.lbl_tiempo.setText(f"{horas:02d}:{minutos:02d}:{segundos:02d}")

    def mostrar_info_video(self, duracion):
        # damos el rango al slider de 0 a la duracion total del video
        self.ui.sld_avance.setRange(0, duracion)

        # Qt entrega la duración en milisegundos → lo pasamos a segundos
        duracion_segundos = duracion // 1000

        # Convertimos a horas, minutos y segundos
        horas = duracion_segundos // 3600
        minutos = int(duracion_segundos // 60)
        segundos = int(duracion_segundos % 60)

        # Formateamos como mm:ss y lo mostramos en el QLabel
        self.ui.lbl_tiempo_total.setText(f"{horas:02d}:{minutos:02d}:{segundos:02d}")

    def creacion_reproductor(self):
        # creamos el reproductor
        self.reproductor = QMediaPlayer()
        # creamos la salida de audio
        self.salida_audio = QAudioOutput()
        # asignamos audio del video a la salida de audio
        self.reproductor.setAudioOutput(self.salida_audio)

    def limpiar_interfaz(self):
        # limpiamos la lista de reproduccion
        self.ui.wdg_lista.clear()
        # asignamos la barra de volumen al 50%
        self.ui.vol_bar.setValue(50)

        # desactivamos los botones al inicia
        self.ui.btn_play.setEnabled(False)
        self.ui.btn_anterior.setEnabled(False)
        self.ui.btn_stop.setEnabled(False)
        self.ui.btn_siguiente.setEnabled(False)

        # slider de reproduccion lo definimos en 0
        self.ui.sld_avance.setRange(0, 0)
