"""Junta todas as telas do app. Cada tela fica no seu próprio arquivo, nesta mesma pasta."""
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from src.views.login_screen import LoginScreen
from src.views.home_screen import HomeScreen
from src.views.calculator_screen import CalculatorScreen
from src.views.summary_screen import SummaryScreen
from src.views.history_screen import HistoryScreen
from src.views.settings_screen import SettingsScreen

# Contraste das cores do tema (de -1 a 1; quanto maior, mais forte a diferença entre texto e fundo).
# No tema claro, um contraste maior deixa o azul dos textos mais escuro, para ler melhor no fundo branco.
CONTRASTE_TEMA_CLARO = 0.8
CONTRASTE_TEMA_ESCURO = 0.0


class MainScreenManager(MDScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(LoginScreen())  
        self.add_widget(HomeScreen())
        self.add_widget(CalculatorScreen())
        self.add_widget(SummaryScreen())
        self.add_widget(HistoryScreen())
        self.add_widget(SettingsScreen())

        # Cada tela pega a cor de fundo uma vez só, quando é criada.
        # Aqui pedimos para o tema avisar sempre que a cor de fundo mudar
        # (claro <-> escuro), e aí trocamos o fundo de todas as telas.
        tema = MDApp.get_running_app().theme_cls
        tema.bind(backgroundColor=self._atualizar_fundo)
        # E quando o tema troca entre claro e escuro, ajustamos o contraste das cores.
        tema.bind(theme_style=self._ajustar_contraste)

    def _atualizar_fundo(self, tema, cor):
        """Chamada pelo tema quando a cor de fundo muda."""
        for screen in self.screens:
            screen.md_bg_color = cor

    def _ajustar_contraste(self, tema, estilo):
        """Chamada pelo tema quando ele troca entre "Light" e "Dark"."""
        if estilo == "Light":
            tema.dynamic_scheme_contrast = CONTRASTE_TEMA_CLARO
        else:
            tema.dynamic_scheme_contrast = CONTRASTE_TEMA_ESCURO

    def atualizar_todas_as_telas(self):
        for screen in self.screens:
            if hasattr(screen, "atualizar_interface") and callable(screen.atualizar_interface):
                screen.atualizar_interface()