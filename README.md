# 🎬 Reproductor Multimedia V2 con PySide6

Un reproductor de video moderno, modular y personalizable desarrollado en Python utilizando el framework **Qt (PySide6)**. 

Este proyecto implementa una arquitectura limpia separando la lógica de negocio, la interfaz de usuario y la gestión de recursos.


<img width="847" height="692" alt="imagen" src="https://github.com/user-attachments/assets/94f0d2ee-c4e7-41b0-8a71-bb6807fbd8d6" />


## 🚀 Características Principales

* **📺 Reproducción de Video:** Soporte para formatos comunes (MP4, AVI, MKV, MOV) usando `QMediaPlayer`.
* **🎨 Personalización Avanzada:** * Sistema de **Temas Dinámicos** (Claro / Oscuro).
    * **Gestión Independiente:** Posibilidad de mezclar Estilos (colores de la ventana) con Sets de Iconos (imágenes de los botones) por separado.
    * Persistencia de configuración (recuerda tus gustos al cerrar la app).
* **📂 Lista de Reproducción Inteligente:**
    * Soporte para **Drag & Drop** (arrastrar y soltar archivos).
    * Generación automática de **Miniaturas** de video usando OpenCV.
* **system_tray Bandeja del Sistema:** * La aplicación se minimiza a la bandeja del sistema en lugar de cerrarse.
    * Control de reproducción (Pausa/Reanudar) desde el menú contextual del icono.
* **🛠️ Interfaz Robusta:** Diseño fluido que mantiene la consistencia visual y geométrica al cambiar de temas (sin "saltos" en los widgets).

## 📋 Estructura del Proyecto

El proyecto sigue una arquitectura modular organizada:

```text
reproductor_v2/
├── Interfaz/               # Lógica visual y recursos compilados
│   ├── temas/              # Archivos .qss (Hojas de estilo)
│   ├── Ui.py               # Estructura de la ventana principal
│   └── iconos_rc.py        # Recursos binarios (iconos)
├── metodos/                # Lógica de negocio
│   ├── modulo.py           # Control del QMediaPlayer y lógica de reproducción
│   ├── theme_manager.py    # Gestor de temas, iconos y persistencia
│   └── system_tray.py      # Lógica de segundo plano y bandeja del sistema
├── Setup.py                # Punto de entrada (Main) de la aplicación



## lista de requirimientos para ejecutar el reproductor

PySide6
opencv-python
numpy


