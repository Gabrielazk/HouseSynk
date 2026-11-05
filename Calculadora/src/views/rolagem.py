"""Rolagem com barra visível, que dá para clicar e arrastar com o mouse (pendência 8 da rodada 2).

O MDScrollView normal tem uma barra fininha (2 pixels) que só serve para ver onde você está: não dá
para pegar com o mouse. No Resumo com todas as abas, chegar no fim ficava quase impossível.

Use RolagemComBarra() no lugar de MDScrollView() em toda tela que rola para cima e para baixo.
As faixas que rolam de lado (etapas e abas no topo da calculadora) continuam com MDScrollView sem barra.
"""
from kivy.app import App
from kivy.metrics import dp
from kivymd.uix.scrollview import MDScrollView

LARGURA_BARRA = dp(6)             # largura da barra (antes: 2 pixels). 10dp ficou largo e cobria a borda dos campos;
                                  # com 6dp ela cabe no espaço de 8dp que as abas e o Resumo têm na lateral
COR_BARRA_PADRAO = (0.5, 0.5, 0.5)  # cinza, só se o tema não tiver a cor principal


class RolagemComBarra(MDScrollView):
    """MDScrollView com a barra larga, que dá para arrastar, e da cor do tema.

    scroll_type = ["bars", "content"]: rola arrastando a barra (mouse) E arrastando o conteúdo
    (dedo no celular). A rodinha do mouse continua funcionando como antes.
    Como é um MDScrollView (herança), o isinstance(child, MDScrollView) das outras telas continua valendo.
    """

    def __init__(self, **kwargs):
        # setdefault: só usa o padrão se quem criou a rolagem não mandou outro valor
        kwargs.setdefault("bar_width", LARGURA_BARRA)
        kwargs.setdefault("scroll_type", ["bars", "content"])
        super().__init__(**kwargs)
        # O tema fica no app (App.get_running_app().theme_cls), não dentro da rolagem.
        # Quando o tema muda (claro/escuro), a cor principal muda e a barra é pintada de novo.
        tema = self._tema()
        if tema is not None and hasattr(tema, "primaryColor"):
            tema.bind(primaryColor=self._pintar_barra)
        self._pintar_barra()

    @staticmethod
    def _tema():
        """O tema do app, ou None se o app ainda não estiver rodando (ex.: nos testes)."""
        app = App.get_running_app()
        return getattr(app, "theme_cls", None)

    def _pintar_barra(self, *args):
        """Cor da barra = cor principal do tema. Parada, fica quase transparente (só um risquinho);
        rolando ou arrastando, aparece forte. Dá para pegar com o mouse mesmo quando está discreta."""
        cor = getattr(self._tema(), "primaryColor", None)
        r, g, b = cor[:3] if cor else COR_BARRA_PADRAO
        self.bar_color = (r, g, b, 0.9)           # enquanto rola ou com o mouse em cima
        self.bar_inactive_color = (r, g, b, 0.15)  # parada: discreta (escolha da Gabi, 05/11/2026)