from PySide6.QtCore import QUrl, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon, Qt
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
import os

from PySide6.QtWidgets import QListWidgetItem, QFileDialog, QListWidget


class Logica_reproductor:
    def __init__(self, ui):
        # cargamos la interfaz en la variable self.ui
        self.ui = ui

        self.ui.wdg_lista.setAcceptDrops(True)
        # self.lista_videos.setAcceptDrops(True)

        # verificamos que todo se inicie correctamente
        self.limpiar_interfaz()

        # lista de rutas completas

        self.lista_reproduccion = []
        self.indice_actual = -1

        # creamos el reproductor
        self.creacion_reproductor()

        # abrimos el archivo estatico
        # self.Abri_archivo()
        # self.ui.wdg_lista.callback_agregar = self.abrir_archivo


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

    def revisar_final(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.indice_actual+= 1
            if self.indice_actual < len(self.lista_reproduccion):
                self.reproducir_video()

    def lp_cambio(self):
        print(".zfkdjgva<sfjnagia<")
        ancho_actual = self.ui.wdg_lista.width()

        # creamos animacion sobre maximunwidth
        self.animacion = QPropertyAnimation(self.ui.wdg_lista, b"maximumWidth")
        self.animacion.setDuration(300)
        self.animacion.setEasingCurve(QEasingCurve.InOutQuad)

        if ancho_actual > 0:
            self.animacion.setStartValue(ancho_actual)
            self.animacion.setEndValue(0)
        else:
            self.animacion.setStartValue(0)
            self.animacion.setEndValue(300)
        self.animacion.start()

    def mod_volumen(self, valor):
        self.salida_audio.setVolume(valor/100)

    def reproducir_item(self, item):
        self.reproductor.stop()
        ruta = item.data(Qt.UserRole)
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
        # if not archivos:
        #     return

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
                # creamos QUrl para el reproductor
                # nombre_archivo = QUrl.fromLocalFile(directorio_archivo)

                # obtenemos el nombre del archivo
                nombre_archivo = os.path.basename(directorio_archivo)
                # agregamos el nombre del archivo a la lista de reproduccion
                item = QListWidgetItem(nombre_archivo)

                item.setData(Qt.UserRole, directorio_archivo)

                self.ui.wdg_lista.addItem(item)

                if self.reproductor.mediaStatus() != QMediaPlayer.LoadedMedia and self.indice_actual == -1:
                    self.indice_actual = len(self.lista_reproduccion) - 1
                    self.reproducir_video()


                    # # conectamos el reproductor widget creado en la interfaz
                    # self.reproductor.setVideoOutput(self.ui.wdg_video)
                    # # asignamos el archivo
                    # self.reproductor.setSource(directorio_archivo)
                    # # reproducimos el archivo asignado
                    # self.reproductor.play()
                    # self.guardar_info_video(directorio_archivo)



    def reproducir_video(self):
        if 0 <= self.indice_actual < len(self.lista_reproduccion):
            ruta = self.lista_reproduccion[self.indice_actual]
            # conectamos el reproductor widget creado en la interfaz
            self.reproductor.setVideoOutput(self.ui.wdg_video)
            # asignamos el reproductor
            self.reproductor.setSource(QUrl.fromLocalFile(ruta))
            self.reproductor.play()


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
