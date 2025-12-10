import os
from PySide6.QtCore import QObject, Signal, QSettings, QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication

class ThemeManager(QObject):
    theme_changed = Signal(str)

    def __init__(self, ui, parent=None):
        super().__init__(parent)
        self.ui = ui
        self.settings = QSettings("MiEmpresa", "MiReproductor")
        self._current_theme = "oscuro"  # Default

    def load_user_preference(self):
        """Loads the saved theme from settings and applies it."""
        theme = self.settings.value("tema", "oscuro")
        self.apply_theme(theme)

    def apply_theme(self, theme_name):
        """Applies the QSS and updates icons for the given theme."""
        self._current_theme = theme_name
        
        # 1. Apply QSS
        self._load_qss(theme_name)
        
        # 2. Update Icons
        self._update_icons(theme_name)
        
        # 3. Save preference
        self.settings.setValue("tema", theme_name)
        
        # 4. Emit signal
        self.theme_changed.emit(theme_name)

    def get_current_theme(self):
        return self._current_theme

    def _load_qss(self, theme_name):
        app = QApplication.instance()
        ruta_qss = os.path.join("Interfaz", "temas", theme_name, f"estilo_{theme_name}.qss")
        try:
            with open(ruta_qss, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Warning: QSS file not found: {ruta_qss}")

    def _update_icons(self, theme_name):
        """Updates all UI icons based on the theme."""
        prefijo = f":/{theme_name}/"

        # Main buttons
        botones = {
            self.ui.btn_play: "boton-de-play.png", # Note: Logic might need to handle play/pause state
            self.ui.btn_stop: "boton-detener.png",
            self.ui.btn_anterior: "atras.png",
            self.ui.btn_siguiente: "siguiente.png",
            self.ui.btn_lp: "anadir-lista.png",
        }

        for btn, archivo in botones.items():
            # Special handling for play button if it's currently showing pause?
            # For now, we reset to play, but the logic might overwrite this.
            # Ideally, we should check the player state, but ThemeManager shouldn't know about player state directly?
            # Or we just update the base icons and let the logic handle the state.
            # Let's just update the base icon for now.
            if btn == self.ui.btn_play:
                 # We'll leave play button handling to the logic or handle it smarter later.
                 # For now, let's just update it to the default 'play' icon of the new theme
                 # UNLESS we can check the icon name.
                 pass
            else:
                btn.setIcon(QIcon(prefijo + archivo))
                btn.setIconSize(QSize(90, 90))

        # Volume Icon (default to medium/low or keep current?)
        # For simplicity, we'll default to volume_1, but logic should update it on volume change.
        ruta_vol = prefijo + "volumen_1.png"
        pix = QPixmap(ruta_vol)
        scaled_pix = pix.scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.lbl_volumen.setPixmap(scaled_pix)

    def get_icon_path(self, icon_name):
        """Helper to get full resource path for current theme."""
        return f":/{self._current_theme}/{icon_name}"
