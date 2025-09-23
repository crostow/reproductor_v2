from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput


class Logica_reproductor:
    def __init__(self, ui):
        # cargamos la interfaz en la variable self.ui
        self.ui = ui

        # verificamos que todo se inicie correctamente
        self.limpiar_interfaz()

        # creamos el reproductor
        self.creacion_reproductor()


        # abrimos el archivo estatico
        self.Abri_archivo()


        # señal cuando cambia  el reproductor de duracion
        self.reproductor.durationChanged.connect(self.mostrar_info_video)
        # señal para actualizar la posicion del slider
        self.reproductor.positionChanged.connect(self.actualizar_posicion)
        # señal para mover le video cuando el usuario arrastra el slider
        self.ui.sld_avance.sliderMoved.connect(self.cambiar_posicion)

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



    def Abri_archivo(self):
        # damos direccion de archivo local estatico
        archivo=("video_test/sample-30s.mp4")
        # creamos la ubicacion del directorio
        directorio_archivo = QUrl.fromLocalFile(archivo)

        print(directorio_archivo)
        # conectamos el reproductor widget creado en la interfaz
        self.reproductor.setVideoOutput(self.ui.wdg_video)
        # asignamos el archivo
        self.reproductor.setSource(directorio_archivo)
        # reproducimos el archivo asignado
        self.reproductor.play()


        self.ui.wdg_lista.addItem(archivo)


    def limpiar_interfaz(self):
        # limpiamos la lista de reproduccion
        self.ui.wdg_lista.clear()
        # asignamos la barra de volumen al 50%
        self.ui.vol_bar.setValue(50)

        self.ui.btn_play.setEnabled(False)
        self.ui.btn_anterior.setEnabled(False)
        self.ui.btn_stop.setEnabled(False)
        self.ui.btn_siguiente.setEnabled(False)

        self.ui.sld_avance.setRange(0, 0)

