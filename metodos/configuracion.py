import os
from PySide6.QtCore import QSettings

def aplicar_tema(app, nombre_tema):
    """
    Aplica el QSS de un tema y guarda la elección en QSettings.
    """
    print("entra a cambiar el tema")
    # Construir ruta al QSS
    ruta_qss = os.path.join("Interfaz", "temas", nombre_tema, f"estilo_{nombre_tema}.qss")
    print(ruta_qss)
    # Aplicar QSS
    try:
        with open(ruta_qss, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
            print(f"Tema '{nombre_tema}' aplicado correctamente")
    except FileNotFoundError:
        print(f"No se encontró el archivo de estilo: {ruta_qss}")

    # Guardar elección en QSettings
    settings = QSettings("MiEmpresa", "MiReproductor")
    settings.setValue("tema", nombre_tema)

def tema_guardado():
    """
    Devuelve el tema guardado en QSettings, por defecto 'oscuro'.
    """
    print("si llama a este metodo")
    settings = QSettings("MiEmpresa", "MiReproductor")
    return settings.value("tema", "oscuro")
