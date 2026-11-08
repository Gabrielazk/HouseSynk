from kivy.config import Config

# Size fixo para mobile (400x700)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')
Config.set('graphics', 'resizable', False)

from kivy.core.window import Window
from kivymd.app import MDApp
from src.views.main_screen import MainScreenManager
from src.models.database import init_db
from src.views.comum import LOGO_APP, NOME_APP

Window.size = (400, 700)

class HouseSynkApp(MDApp):
    def build(self):
        self.title = NOME_APP   # nome na barra da janela
        self.icon = LOGO_APP    # ícone da janela
        init_db()  # Inicializa o SQLite
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"  # Palette em tons de Azul
        return MainScreenManager()

if __name__ == "__main__":
    HouseSynkApp().run()