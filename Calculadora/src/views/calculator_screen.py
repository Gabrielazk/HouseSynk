"""Tela de cálculo com as abas (Brocas, Baldrame, Paredes...)."""
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.uix.button import (
    MDButton,
    MDButtonText,
    MDButtonIcon,
    MDIconButton,
)
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.scrollview import MDScrollView
from src.views.rolagem import RolagemComBarra  # rolagem com barra larga, que dá para arrastar
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)
from src.calculators.brocas import (
    PRECO_ARAME_KG,
    calcular_brocas,
    BITOLAS_LONGITUDINAL,
    BITOLA_PADRAO,
    ESPACAMENTO_ESTRIBO_PADRAO_CM,
    PROFUNDIDADE_MAXIMA_M,
)
from src.calculators.baldrame import (
    calcular_baldrame,
    PERDA_PADRAO_BALDRAME,
    PRECO_IMPERM_LITRO,
    PRECO_IMPERM_LITRO_EUA,
    EMBALAGENS_IMPERM_L,
    LARGURA_MINIMA_CM,
    ALTURA_MINIMA_CM,
)
from src.calculators.reboco import (
    calcular_reboco,
    ESPESSURA_PADRAO_CM as ESPESSURA_REBOCO_PADRAO_CM,
    PERDA_PADRAO_REBOCO,
    CHAPISCO_TRACO_RODAPE,
    CHAPISCO_ESPESSURA_CM,
    AREA_MAXIMA_REBOCO_M2,
    ESPESSURA_MINIMA_CM as ESPESSURA_MINIMA_REBOCO_CM,
    ESPESSURA_MAXIMA_CM as ESPESSURA_MAXIMA_REBOCO_CM,
)
from src.calculators.contrapiso import (
    calcular_contrapiso,
    PERDA_PADRAO_CONTRAPISO,
    TRACO_PADRAO_CONTRAPISO,
    AREA_MAXIMA_CONTRAPISO_M2,
    ESPESSURA_MINIMA_CM as ESPESSURA_MINIMA_CONTRAPISO_CM,
    ESPESSURA_MAXIMA_CM as ESPESSURA_MAXIMA_CONTRAPISO_CM,
)
from src.calculators.revestimento import (
    calcular_piso,
    calcular_azulejo,
    TIPOS_ARGAMASSA,
    ARGAMASSA_PADRAO_PISO,
    ARGAMASSA_PADRAO_AZULEJO,
    PRECO_PISO_M2,
    PRECO_AZULEJO_M2,
    PRECO_RODAPE_M,
    PRECO_ARGAMASSA_SACO,
    PRECO_ARGAMASSA_SACO_EUA,
    tipos_argamassa,
    argamassa_padrao,
    AREA_MAXIMA_REVESTIMENTO_M2,
    PECA_MINIMA_CM,
    PECA_MAXIMA_CM,
)
from src.calculators.laje import (
    calcular_laje,
    TIPOS_LAJE,
    TIPO_LAJE_PADRAO,
    ENCHIMENTOS,
    ENCHIMENTO_PADRAO,
    PERDA_PADRAO_LAJE,
    CAPA_PADRAO_CM,
    PRECO_LAJE_PREMOLDADA_M2,
    PRECO_PAINEL_TELA,
    AREA_MAXIMA_LAJE_M2,
    CAPA_MINIMA_CM,
    CAPA_MAXIMA_CM,
    ESPESSURA_MACICA_MINIMA_CM,
    ESPESSURA_MACICA_MAXIMA_CM,
)
from src.calculators.telhado import (
    calcular_telhado,
    TIPOS_TELHA,
    TIPO_TELHA_PADRAO,
    PERDA_PADRAO_TELHADO,
    INCLINACAO_PADRAO,
    PRECO_TELHA,
    PRECO_CUMEEIRA,
    PRECO_MADEIRA_M,
    AREA_MAXIMA_TELHADO_M2,
    INCLINACAO_MAXIMA_PERCENTUAL,
)
from src.calculators.eletrica import (
    calcular_eletrica,
    BITOLAS_FIO,
    PERDA_PADRAO_ELETRICA,
    PRECO_ROLO_CONDUITE,
    PRECO_ROLO_FIO,
    PRECO_CAIXA_4X2,
    PRECO_CAIXA_OCTOGONAL,
    PRECO_TOMADA,
    PRECO_INTERRUPTOR,
    TOMADAS_MAXIMO,
    INTERRUPTORES_MAXIMO,
    LUZES_MAXIMO,
    CHUVEIROS_MAXIMO,
)
from src.calculators.hidraulica import (
    calcular_hidraulica,
    TUBOS,
    BARRA_TUBO_M,
    PERDA_PADRAO_HIDRAULICA,
    PRECO_BARRA_TUBO,
    PRECO_CONEXAO,
    PRECO_REGISTRO,
    PONTOS_MAXIMO,
)
from src.calculators.pintura import (
    calcular_pintura,
    DEMAOS_PADRAO,
    DEMAOS_MAXIMO,
    DEMAOS_MASSA,
    PERDA_PADRAO_PINTURA,
    RENDIMENTO_PADRAO_M2_L,
    TIPOS_MASSA,
    PRECO_TINTA,
    PRECO_TINTA_EUA,
    PRECO_BALDE_MASSA,
    RENDIMENTO_PADRAO_EUA_SQFT_GAL,
    rendimento_padrao_m2_l,
    limites_rendimento_m2_l,
    AREA_MAXIMA_PINTURA_M2,
)
from src.calculators.esquadrias import (
    calcular_esquadrias,
    TIPOS_ESQUADRIA,
    TIPO_ESQUADRIA_PADRAO,
    MATERIAIS,
    MATERIAL_PADRAO,
    PRECO_TUBO_ESPUMA,
    PRECO_PARAFUSO,
    PRECO_SACO_ARGAMASSA_FIXACAO,
    QUANTIDADE_MAXIMA as QUANTIDADE_MAXIMA_ESQUADRIA,
    LARGURA_MAXIMA_CM as LARGURA_MAXIMA_ESQUADRIA_CM,
    ALTURA_MAXIMA_CM as ALTURA_MAXIMA_ESQUADRIA_CM,
)
from src.calculators.rejunte import (
    calcular_rejunte,
    PERDA_PADRAO_REJUNTE,
    ESPESSURA_PADRAO_MM,
    PRECO_LATA_1KG,
    PRECO_LATA_2KG,
    PRECO_REJUNTE_EUA,
    AREA_MAXIMA_REJUNTE_M2,
    JUNTA_MINIMA_MM,
    JUNTA_MAXIMA_MM,
)
from src.calculators.paredes import (
    calcular_paredes,
    TIJOLOS,
    TIJOLO_PADRAO,
    ASSENTAMENTOS,
    ASSENTAMENTO_PADRAO,
    JUNTA_PADRAO_CM,
    QUEBRA_PADRAO_PERCENTUAL,
    AREA_MAXIMA_M2,
    JUNTA_MINIMA_CM,
    JUNTA_MAXIMA_CM,
    QUEBRA_MAXIMA_PERCENTUAL,
)
from src.calculators.tracos import (
    TRACOS_CONCRETO,
    TRACO_CONCRETO_PADRAO,
    TRACOS_MASSA,
    TRACO_MASSA_PADRAO,
)
from kivymd.uix.widget import MDWidget
from src.views.comum import CONFIG_APP, TABELA_PRECOS_GLOBAL, ORCAMENTO_FINAL, TEXTOS, txt, fmt_moeda, fmt_num, fmt_int, sistema_unidades, sem_quebra
from src.views.textos_eua import TEXTOS_EUA
from src.calculators.unidades import METRICO, IMPERIAL, arredondar, ler_numero, para_metrico, do_metrico, texto_polegadas, nome_unidade


def txt_do_pais(chave, sistema=None):
    """Igual ao txt(), mas no país em que a conta foi feita (sistema = METRICO ou IMPERIAL).
    Serve para a lista de compras de um orçamento feito no outro país continuar certa
    (ex.: um orçamento do Brasil mostra "lata de 18 L" mesmo com o país trocado para EUA).
    sistema=None: usa o país escolhido agora (é o mesmo que txt)."""
    if sistema is None or sistema == sistema_unidades():
        return txt(chave)
    lang = CONFIG_APP.get("idioma", "pt").lower()
    if sistema == IMPERIAL:
        texto_eua = TEXTOS_EUA.get(lang, {}).get(chave)
        if texto_eua is not None:
            return texto_eua
    return TEXTOS.get(lang, TEXTOS.get("pt", {})).get(chave, chave)


class MenuAlinhado(MDDropdownMenu):
    """Menu (dropdown) que abre embaixo do botão, começando na borda esquerda dele, e nunca sai da janela.

    O MDDropdownMenu do KivyMD mede o espaço a partir do MEIO do botão: um menu largo (nomes compridos,
    como "Tijolo baiano 9 furos (9x14x19)") ficava estreito e cortava o texto, ou crescia para a
    esquerda e saía da tela. Aqui a gente troca só duas funções dele (o resto continua igual)."""

    def adjust_width(self):
        # A largura pedida, mas nunca maior que a janela (com a margem dos dois lados)
        largura_pedida = getattr(self, "_initial_width", self.width)  # getattr: funciona em versões do KivyMD sem esse nome
        self.width = min(largura_pedida, Window.width - 2 * self.border_margin)

    def set_menu_pos(self, *args):
        super().set_menu_pos(*args)  # o KivyMD calcula a altura (embaixo do botão)
        x_botao = self.caller.to_window(self.caller.x, self.caller.y)[0]
        # Começa na borda esquerda do botão; se não couber, encosta na margem da direita
        self.x = max(self.border_margin, min(x_botao, Window.width - self.width - self.border_margin))


# --- TELA DE CÁLCULO COM ABAS (Navegação Interna) ---
# Ordem das abas no fluxo (botão Próximo). Aba nova entra aqui.
# Etapas do fluxo, na ordem da obra, com as abas de cada uma. Aba nova entra na etapa dela.
ETAPAS = [
    ("estrutura", ["brocas", "baldrame", "paredes", "laje", "telhado"]),
    ("instalacoes", ["eletrica", "hidraulica"]),
    ("acabamento", ["contrapiso", "reboco", "piso", "azulejo", "rejunte", "pintura", "esquadrias"]),
]
# Todas as abas em sequência (é a ordem dos botões Anterior / Próximo)
ABAS_ORDEM = [aba for _, abas in ETAPAS for aba in abas]


def etapa_da_aba(aba):
    """Posição (0, 1, 2) e nome da etapa de uma aba."""
    for indice, (etapa, abas) in enumerate(ETAPAS):
        if aba in abas:
            return indice, etapa
    return 0, ETAPAS[0][0]

# Campos de texto que cada aba guarda (chave usada no estado e no Histórico)
CAMPOS_ABA = {
    "brocas": ["qtd", "prof", "diam", "perda", "barras", "esp_estribo", "mo"],
    "baldrame": ["comp", "larg", "alt", "perda", "mo", "barras", "esp_estribo"],
    "paredes": ["area", "vaos", "junta", "quebra"],
    "contrapiso": ["area", "esp", "perda"],
    "reboco": ["area", "vaos", "esp", "perda"],
    "piso": ["area", "larg", "alt", "caixa", "perda", "rodape", "rodape_peca"],
    "azulejo": ["area", "larg", "alt", "vaos", "caixa", "perda"],
    "rejunte": ["area", "larg", "alt", "junta", "esp", "perda"],
    "laje": ["area", "capa", "esp", "perda"],
    "telhado": ["area", "incl", "cumeeira", "perda"],
    "eletrica": ["tomadas", "interruptores", "luzes", "chuveiros", "chuveiros4", "conduite", "fio1.5", "fio2.5", "fio4", "fio6", "perda"],
    "hidraulica": ["fria", "quente", "esgoto", "tubo_fria", "tubo_quente", "tubo_esg40", "tubo_esg100", "perda"],
    "pintura": ["parede", "teto", "demaos", "rend", "perda"],
    "esquadrias": ["qtd", "larg", "alt"],  # campos do formulário "Nova porta ou janela"; a lista fica em self.esquadrias_itens
}
# Se algum destes tiver texto, a aba conta como preenchida (aba em branco é ignorada)
CAMPOS_INICIAIS = {
    "brocas": ["qtd", "prof", "diam", "barras", "mo"],
    "baldrame": ["comp", "larg", "alt", "barras", "mo"],
    "paredes": ["area", "vaos"],
    "contrapiso": ["area", "esp"],
    "reboco": ["area", "vaos"],
    "piso": ["area", "larg", "alt"],
    "azulejo": ["area", "larg", "alt"],
    "rejunte": ["area", "larg", "alt", "junta"],
    "laje": ["area", "esp"],
    "telhado": ["area", "cumeeira"],
    "eletrica": ["tomadas", "interruptores", "luzes", "chuveiros", "chuveiros4", "conduite", "fio1.5", "fio2.5", "fio4", "fio6"],
    "hidraulica": ["fria", "quente", "esgoto", "tubo_fria", "tubo_quente", "tubo_esg40", "tubo_esg100"],
    "pintura": ["parede", "teto"],
    "esquadrias": ["qtd", "larg", "alt"],
}
# Versão EUA: a unidade de cada campo com medida (os tipos estão em src/calculators/unidades.py).
# Nos EUA, o que a pessoa digita nesses campos é convertido para métrico antes da conta.
# Campo que não está aqui não muda (quantidades, perdas, barras, inclinação, demãos, pontos).
# Esquadrias não está aqui: as medidas dela são convertidas ao tocar em "Adicionar à lista".
UNIDADE_CAMPO = {
    "brocas": {"prof": "comprimento", "diam": "centimetro", "esp_estribo": "centimetro", "mo": "preco_comprimento"},
    "baldrame": {"comp": "comprimento", "larg": "centimetro", "alt": "centimetro",
                 "esp_estribo": "centimetro", "mo": "preco_comprimento"},
    "paredes": {"area": "area", "vaos": "area", "junta": "centimetro"},
    "contrapiso": {"area": "area", "esp": "centimetro"},
    "reboco": {"area": "area", "vaos": "area", "esp": "centimetro"},
    "piso": {"area": "area", "larg": "centimetro", "alt": "centimetro", "caixa": "area", "rodape": "comprimento",
             "rodape_peca": "comprimento"},
    "azulejo": {"area": "area", "larg": "centimetro", "alt": "centimetro", "vaos": "area", "caixa": "area"},
    "rejunte": {"area": "area", "larg": "centimetro", "alt": "centimetro", "junta": "milimetro", "esp": "milimetro"},
    "laje": {"area": "area", "capa": "centimetro", "esp": "centimetro"},
    "telhado": {"area": "area", "cumeeira": "comprimento"},
    "eletrica": {chave: "comprimento" for chave in CAMPOS_ABA["eletrica"] if chave == "conduite" or chave.startswith("fio")},
    "hidraulica": {chave: "comprimento" for chave in CAMPOS_ABA["hidraulica"] if chave.startswith("tubo_")},
    "pintura": {"parede": "area", "teto": "area", "rend": "rendimento"},
}


class CalculatorScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "calculator"
        self.md_bg_color = self.theme_cls.backgroundColor
        self.reiniciar(montar=False)

        self.layout_principal = MDBoxLayout(orientation="vertical", padding="16dp", spacing="12dp")
        self.add_widget(self.layout_principal)
        self.montar_tela()

    def reiniciar(self, montar=True):
        """Nova obra: apaga os dados de todas as abas e volta aos valores padrão."""
        self.aba_atual = ABAS_ORDEM[0]
        self.origem = "home"
        self.modo_somente_leitura = False
        self.estado_abas = {}        # texto digitado em cada aba
        self.textos_resultado = {}   # último resultado mostrado em cada aba
        self._sistema_estado = sistema_unidades()  # em que unidades o texto do estado_abas está
        self.traco = {"brocas": TRACO_CONCRETO_PADRAO, "baldrame": TRACO_CONCRETO_PADRAO, "paredes": TRACO_MASSA_PADRAO, "contrapiso": TRACO_PADRAO_CONTRAPISO, "reboco": TRACO_MASSA_PADRAO, "laje": TRACO_CONCRETO_PADRAO}
        self.tijolo = {"paredes": TIJOLO_PADRAO}
        self.assent = {"paredes": ASSENTAMENTO_PADRAO}
        self.bitola = {"brocas": BITOLA_PADRAO, "baldrame": BITOLA_PADRAO}
        self.imperm = {"baldrame": False}
        self.dois_lados = {"reboco": False}
        self.chapisco = {"reboco": False}
        # Argamassa colante: AC-I / AC-II no Brasil; A118.1 / A118.4 (thinset) nos EUA
        sistema = self._sistema_estado
        self.argamassa = {"piso": argamassa_padrao(True, sistema), "azulejo": argamassa_padrao(False, sistema)}
        self.desenho = {"piso": False, "azulejo": False}  # assentamento com desenho: perda de 25%
        self.laje_tipo = TIPO_LAJE_PADRAO
        self.laje_enchimento = ENCHIMENTO_PADRAO
        self.telha_tipo = TIPO_TELHA_PADRAO
        self.madeiramento = {"telhado": False}
        self.tela = {"laje": False}  # tela soldada na capa da laje pré-moldada
        self.selador = {"pintura": False}
        self.fundo = {"pintura": False}
        self.massa_tipo = "nenhuma"
        self.esquadrias_itens = []   # lista de portas e janelas da aba Esquadrias (medidas sempre em cm)
        self.esq_tipo = TIPO_ESQUADRIA_PADRAO
        self.esq_material = MATERIAL_PADRAO
        self.esq_fixacao = {"espuma": False, "parafusos": False, "argamassa": False}
        self._campos = {}            # campos da aba aberta no momento
        self._botoes_traco = {}
        self._botoes_bitola = {}
        self._botoes_imperm = {}
        self._botoes_sn = {}
        self._botoes_arg = {}
        self._botoes_tijolo = {}
        self._botoes_assent = {}
        self._lbl_resultado = None
        self.menu_ativo = None
        self.dialog_ajuda = None
        self.dialog_limpar = None
        self.dialog_aviso = None
        # Avisos de limite que a pessoa já aceitou ("Continuar"), por aba. O texto do aviso tem o valor
        # digitado, então se a pessoa mudar o número, o aviso aparece de novo.
        self._avisos_aceitos = {}
        if montar:
            self.montar_tela()

    def _sincronizar_unidades(self):
        """O país mudou nas Configurações: converte o que já foi digitado para as unidades novas."""
        sistema = sistema_unidades()
        if sistema == self._sistema_estado:
            return
        self._capturar_estado()  # guarda o texto da aba aberta antes de converter
        self._converter_estado_abas(self._sistema_estado, sistema)
        self._trocar_argamassa_de_pais(sistema)
        self._sistema_estado = sistema
        self._campos = {}  # não deixa os campos antigos sobrescreverem o que foi convertido

    def _trocar_argamassa_de_pais(self, sistema):
        """Cada país tem os seus tipos de argamassa colante. Ao trocar de país, troca pelo
        equivalente: AC-I <-> A118.1 (não modificada); AC-II e AC-III <-> A118.4 (modificada)."""
        equivalente = {"AC-I": "A118.1", "AC-II": "A118.4", "AC-III": "A118.4",
                       "A118.1": "AC-I", "A118.4": "AC-II"}
        for aba in self.argamassa:
            atual = self.argamassa[aba]
            if atual not in tipos_argamassa(sistema):
                novo = equivalente.get(atual)
                self.argamassa[aba] = novo if novo in tipos_argamassa(sistema) else argamassa_padrao(aba == "piso", sistema)

    def montar_tela(self):
        self._sincronizar_unidades()
        self.layout_principal.clear_widgets()

        # --- TOPO (Botão Voltar + Título) ---
        topo = MDBoxLayout(size_hint_y=None, height="40dp", spacing="10dp")
        self.btn_voltar = MDButton(MDButtonText(text=txt("btn_voltar")), on_release=self.voltar_home)
        self.titulo_topo = MDLabel(
            text=f"{txt('titulo_calculadora')} ({CONFIG_APP['estado']})",
            font_style="Title",
            role="medium",
            bold=True,
            theme_text_color="Primary"
        )
        topo.add_widget(self.btn_voltar)
        topo.add_widget(self.titulo_topo)
        self.layout_principal.add_widget(topo)

        # --- ETAPAS (Estrutura, Instalações, Acabamento): a etapa atual fica destacada ---
        self.rolagem_etapas = MDScrollView(do_scroll_x=True, do_scroll_y=False, bar_width=0, size_hint_y=None, height="48dp")
        self.faixa_etapas = MDBoxLayout(size_hint_x=None, spacing="8dp")
        self.faixa_etapas.bind(minimum_width=self.faixa_etapas.setter("width"))
        self.rolagem_etapas.add_widget(self.faixa_etapas)
        self.layout_principal.add_widget(self.rolagem_etapas)

        # --- ABAS DA ETAPA ATUAL + AJUDA "?": a aba aberta fica destacada ---
        box_tabs = MDBoxLayout(size_hint_y=None, height="48dp", spacing="8dp")

        # As abas ficam numa faixa que rola para o lado (cabem muitas abas em telas pequenas)
        self.faixa_abas = MDBoxLayout(size_hint_x=None, spacing="8dp")
        self.faixa_abas.bind(minimum_width=self.faixa_abas.setter("width"))
        self.rolagem_abas = MDScrollView(do_scroll_x=True, do_scroll_y=False, bar_width=0)
        self.rolagem_abas.add_widget(self.faixa_abas)
        box_tabs.add_widget(self.rolagem_abas)
        self.btn_ajuda = MDIconButton(
            icon="help-circle-outline",
            pos_hint={"center_y": 0.5},
            on_release=self.abrir_ajuda
        )
        box_tabs.add_widget(self.btn_ajuda)
        self.layout_principal.add_widget(box_tabs)

        # --- ÁREA DINÂMICA (Conteúdo das Abas) ---
        self.container_conteudo = MDBoxLayout(orientation="vertical")
        self.layout_principal.add_widget(self.container_conteudo)

        # Reabre a aba que estava ativa (brocas por padrão)
        self.trocar_aba(self.aba_atual)

    def atualizar_interface(self):
        self.montar_tela()

    # ==========================================
    # BARRAS DE ETAPAS E ABAS (destaque: botão preenchido = onde a pessoa está)
    # ==========================================
    def _atualizar_barras(self):
        indice_etapa, _ = etapa_da_aba(self.aba_atual)

        self.faixa_etapas.clear_widgets()
        for indice, (etapa, abas) in enumerate(ETAPAS):
            self.faixa_etapas.add_widget(MDButton(
                MDButtonText(text=f"{indice + 1}. {txt('etapa_' + etapa)}"),
                style="filled" if indice == indice_etapa else "outlined",
                on_release=lambda x, a=abas[0]: self.trocar_aba(a)  # pula para a 1ª aba da etapa
            ))

        self.faixa_abas.clear_widgets()
        botao_atual = None
        for aba in ETAPAS[indice_etapa][1]:
            botao = MDButton(
                MDButtonText(text=txt(f"aba_{aba}")),
                style="filled" if aba == self.aba_atual else "outlined",
                on_release=lambda x, a=aba: self.trocar_aba(a)
            )
            if aba == self.aba_atual:
                botao_atual = botao
            self.faixa_abas.add_widget(botao)

        # Rola a faixa até a aba aberta (para ela não ficar escondida no canto)
        if botao_atual is not None:
            Clock.schedule_once(lambda dt: self.rolagem_abas.scroll_to(botao_atual, padding=dp(8), animate=False), 0)

    # ==========================================
    # ESTADO DE CADA ABA (não perde o que foi digitado ao trocar de aba)
    # ==========================================
    def _capturar_estado(self):
        if not self._campos:
            return
        self.estado_abas[self.aba_atual] = {chave: campo.text for chave, campo in self._campos.items()}

    def _restaurar_estado(self):
        estado = self.estado_abas.get(self.aba_atual, {})
        for chave, campo in self._campos.items():
            if chave in estado:
                campo.text = estado[chave]
        texto = self.textos_resultado.get(self.aba_atual)
        if texto and self._lbl_resultado is not None:
            self._lbl_resultado.text = sem_quebra(texto)  # número e unidade sempre na mesma linha

    def trocar_aba(self, aba_nome):
        self._capturar_estado()
        self.aba_atual = aba_nome
        self._campos = {}
        self.container_conteudo.clear_widgets()
        self._atualizar_barras()

        if aba_nome == "brocas":
            self.container_conteudo.add_widget(self.montar_conteudo_brocas())
        elif aba_nome == "baldrame":
            self.container_conteudo.add_widget(self.montar_conteudo_baldrame())
        elif aba_nome == "paredes":
            self.container_conteudo.add_widget(self.montar_conteudo_paredes())
        elif aba_nome == "contrapiso":
            self.container_conteudo.add_widget(self.montar_conteudo_contrapiso())
        elif aba_nome == "reboco":
            self.container_conteudo.add_widget(self.montar_conteudo_reboco())
        elif aba_nome in ("piso", "azulejo"):
            self.container_conteudo.add_widget(self.montar_conteudo_ceramica(aba_nome))
        elif aba_nome == "rejunte":
            self.container_conteudo.add_widget(self.montar_conteudo_rejunte())
        elif aba_nome == "laje":
            self.container_conteudo.add_widget(self.montar_conteudo_laje())
        elif aba_nome == "telhado":
            self.container_conteudo.add_widget(self.montar_conteudo_telhado())
        elif aba_nome == "eletrica":
            self.container_conteudo.add_widget(self.montar_conteudo_eletrica())
        elif aba_nome == "hidraulica":
            self.container_conteudo.add_widget(self.montar_conteudo_hidraulica())
        elif aba_nome == "pintura":
            self.container_conteudo.add_widget(self.montar_conteudo_pintura())
        elif aba_nome == "esquadrias":
            self.container_conteudo.add_widget(self.montar_conteudo_esquadrias())

        self._restaurar_estado()

    # ==========================================
    # CONTEÚDO DA ABA 1: BROCAS
    # ==========================================
    def montar_conteudo_brocas(self):
        scroll = RolagemComBarra()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        # --- Obrigatórios ---
        self.lbl_obrigatorio = MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        self.in_qtd = MDTextField(MDTextFieldHintText(text=txt("hint_qtd")), mode="outlined", write_tab=False, readonly=ro)
        self.in_prof = MDTextField(MDTextFieldHintText(text=txt("hint_prof")), mode="outlined", write_tab=False, readonly=ro)
        self.in_diam = MDTextField(MDTextFieldHintText(text=txt("hint_diam")), mode="outlined", write_tab=False, readonly=ro)
        box_form.add_widget(self.lbl_obrigatorio)
        box_form.add_widget(self.in_qtd)
        box_form.add_widget(self.in_diam)
        box_form.add_widget(self.in_prof)

        # --- Opcionais (já vêm preenchidos com valores padrão; os rótulos dizem "opcional") ---
        self._montar_seletor_traco(box_form, "brocas")

        self.in_perda = MDTextField(MDTextFieldHintText(text=txt("hint_perda")), text="10", mode="outlined", write_tab=False, readonly=ro)
        self.in_mo = MDTextField(MDTextFieldHintText(text=txt("hint_mo")), mode="outlined", write_tab=False, readonly=ro)
        box_form.add_widget(self.in_perda)
        box_form.add_widget(self.in_mo)

        # --- Armadura ---
        self.lbl_armadura = MDLabel(text=txt("secao_armadura"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        self.in_barras = MDTextField(MDTextFieldHintText(text=txt("hint_barras")), mode="outlined", write_tab=False, readonly=ro)
        self.in_esp_estribo = MDTextField(
            MDTextFieldHintText(text=txt("hint_esp_estribo")),
            text=self._texto_padrao(ESPACAMENTO_ESTRIBO_PADRAO_CM, "centimetro"),
            mode="outlined", write_tab=False, readonly=ro
        )
        box_form.add_widget(self.lbl_armadura)
        box_form.add_widget(self.in_barras)
        self._montar_seletor_bitola(box_form, "brocas")
        box_form.add_widget(self.in_esp_estribo)

        self._campos = {
            "qtd": self.in_qtd, "prof": self.in_prof, "diam": self.in_diam,
            "perda": self.in_perda, "mo": self.in_mo,
            "barras": self.in_barras, "esp_estribo": self.in_esp_estribo,
        }

        if not ro:
            self.btn_calcular = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calcular)

        box_resultado = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_resultado.bind(minimum_height=box_resultado.setter('height'))

        self.lbl_resultado = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_resultado.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_resultado
        box_resultado.add_widget(self.lbl_resultado)

        self._montar_botoes_fluxo(box_resultado)

        box_form.add_widget(box_resultado)
        scroll.add_widget(box_form)
        return scroll

    # ==========================================
    # CONTEÚDO DA ABA 2: BALDRAME
    # ==========================================
    def montar_conteudo_baldrame(self):
        scroll = RolagemComBarra()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        # --- Obrigatórios ---
        self.lbl_obrigatorio_bal = MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        self.in_bal_comp = MDTextField(MDTextFieldHintText(text=txt("hint_comprimento")), mode="outlined", write_tab=False, readonly=ro)
        self.in_bal_larg = MDTextField(MDTextFieldHintText(text=txt("hint_largura")), mode="outlined", write_tab=False, readonly=ro)
        self.in_bal_alt = MDTextField(MDTextFieldHintText(text=txt("hint_altura")), mode="outlined", write_tab=False, readonly=ro)
        box_form.add_widget(self.lbl_obrigatorio_bal)
        box_form.add_widget(self.in_bal_comp)
        box_form.add_widget(self.in_bal_larg)
        box_form.add_widget(self.in_bal_alt)

        # --- Opcionais (já vêm preenchidos com valores padrão; os rótulos dizem "opcional") ---
        self._montar_seletor_traco(box_form, "baldrame")

        self.in_bal_perda = MDTextField(
            MDTextFieldHintText(text=txt("hint_perda_bal")),
            text=self._texto_campo(PERDA_PADRAO_BALDRAME),
            mode="outlined", write_tab=False, readonly=ro
        )
        self.in_bal_mo = MDTextField(MDTextFieldHintText(text=txt("hint_mo")), mode="outlined", write_tab=False, readonly=ro)
        box_form.add_widget(self.in_bal_perda)
        box_form.add_widget(self.in_bal_mo)

        # --- Armadura ---
        self.lbl_armadura_bal = MDLabel(text=txt("secao_armadura"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        self.in_bal_barras = MDTextField(MDTextFieldHintText(text=txt("hint_barras_bal")), mode="outlined", write_tab=False, readonly=ro)
        self.in_bal_esp_estribo = MDTextField(
            MDTextFieldHintText(text=txt("hint_esp_estribo")),
            text=self._texto_padrao(ESPACAMENTO_ESTRIBO_PADRAO_CM, "centimetro"),
            mode="outlined", write_tab=False, readonly=ro
        )
        box_form.add_widget(self.lbl_armadura_bal)
        box_form.add_widget(self.in_bal_barras)
        self._montar_seletor_bitola(box_form, "baldrame")
        box_form.add_widget(self.in_bal_esp_estribo)

        # --- Impermeabilização (Sim / Não) ---
        self._montar_seletor_imperm(box_form, "baldrame")

        self._campos = {
            "comp": self.in_bal_comp, "larg": self.in_bal_larg, "alt": self.in_bal_alt,
            "perda": self.in_bal_perda, "mo": self.in_bal_mo,
            "barras": self.in_bal_barras, "esp_estribo": self.in_bal_esp_estribo,
        }

        if not ro:
            self.btn_calc_bal = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_bal)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_baldrame = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_baldrame.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_baldrame
        box_res.add_widget(self.lbl_res_baldrame)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    # ==========================================
    # CONTEÚDO DA ABA 3: PAREDES
    # ==========================================
    def montar_conteudo_paredes(self):
        scroll = RolagemComBarra()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        # --- Obrigatórios ---
        self.lbl_obrigatorio_par = MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        self.in_par_area = MDTextField(MDTextFieldHintText(text=txt("hint_area_parede")), mode="outlined", write_tab=False, readonly=ro)
        box_form.add_widget(self.lbl_obrigatorio_par)
        box_form.add_widget(self.in_par_area)
        self._montar_seletor_tijolo(box_form, "paredes")
        self._montar_seletor_assent(box_form, "paredes")

        # --- Opcionais (já vêm preenchidos com valores padrão; os rótulos dizem "opcional") ---
        self.in_par_vaos = MDTextField(MDTextFieldHintText(text=txt("hint_vaos")), mode="outlined", write_tab=False, readonly=ro)
        self.in_par_junta = MDTextField(
            MDTextFieldHintText(text=txt("hint_junta")),
            text=self._texto_padrao(JUNTA_PADRAO_CM, "centimetro"), mode="outlined", write_tab=False, readonly=ro
        )
        self.in_par_quebra = MDTextField(
            MDTextFieldHintText(text=txt("hint_quebra")),
            text=self._texto_campo(QUEBRA_PADRAO_PERCENTUAL), mode="outlined", write_tab=False, readonly=ro
        )
        box_form.add_widget(self.in_par_vaos)
        box_form.add_widget(self.in_par_junta)
        box_form.add_widget(self.in_par_quebra)
        self._montar_seletor_traco(box_form, "paredes")

        self._campos = {
            "area": self.in_par_area, "vaos": self.in_par_vaos,
            "junta": self.in_par_junta, "quebra": self.in_par_quebra,
        }

        if not ro:
            self.btn_calc_par = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_par)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_paredes = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_paredes.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_paredes
        box_res.add_widget(self.lbl_res_paredes)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    # ==========================================
    # CONTEÚDO DA ABA 4: CONTRAPISO
    # ==========================================
    def montar_conteudo_contrapiso(self):
        scroll = RolagemComBarra()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        # --- Obrigatórios ---
        self.lbl_obrigatorio_con = MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        self.in_con_area = MDTextField(MDTextFieldHintText(text=txt("hint_area_contrapiso")), mode="outlined", write_tab=False, readonly=ro)
        self.in_con_esp = MDTextField(MDTextFieldHintText(text=txt("hint_esp_contrapiso")), mode="outlined", write_tab=False, readonly=ro)
        box_form.add_widget(self.lbl_obrigatorio_con)
        box_form.add_widget(self.in_con_area)
        box_form.add_widget(self.in_con_esp)

        # --- Opcionais (já vêm preenchidos com valores padrão; os rótulos dizem "opcional") ---
        self._montar_seletor_traco(box_form, "contrapiso")
        self.in_con_perda = MDTextField(
            MDTextFieldHintText(text=txt("hint_perda_bal")),
            text=self._texto_campo(PERDA_PADRAO_CONTRAPISO), mode="outlined", write_tab=False, readonly=ro
        )
        box_form.add_widget(self.in_con_perda)

        self._campos = {"area": self.in_con_area, "esp": self.in_con_esp, "perda": self.in_con_perda}

        if not ro:
            self.btn_calc_con = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_con)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_contrapiso = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_contrapiso.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_contrapiso
        box_res.add_widget(self.lbl_res_contrapiso)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    # ==========================================
    # CONTEÚDO DA ABA 5: REBOCO
    # ==========================================
    def montar_conteudo_reboco(self):
        scroll = RolagemComBarra()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        # --- Obrigatórios (a espessura e o traço já vêm com valor padrão) ---
        self.lbl_obrigatorio_reb = MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary")
        self.in_reb_area = MDTextField(MDTextFieldHintText(text=txt("hint_area_reboco")), mode="outlined", write_tab=False, readonly=ro)
        self.in_reb_esp = MDTextField(
            MDTextFieldHintText(text=txt("hint_esp_reboco")),
            text=self._texto_padrao(ESPESSURA_REBOCO_PADRAO_CM, "centimetro"), mode="outlined", write_tab=False, readonly=ro
        )
        box_form.add_widget(self.lbl_obrigatorio_reb)
        box_form.add_widget(self.in_reb_area)
        box_form.add_widget(self.in_reb_esp)
        self._montar_seletor_traco(box_form, "reboco")

        # --- Opcionais ---
        self.in_reb_vaos = MDTextField(MDTextFieldHintText(text=txt("hint_vaos")), mode="outlined", write_tab=False, readonly=ro)
        self.in_reb_perda = MDTextField(
            MDTextFieldHintText(text=txt("hint_perda")),
            text=self._texto_campo(PERDA_PADRAO_REBOCO), mode="outlined", write_tab=False, readonly=ro
        )
        box_form.add_widget(self.in_reb_vaos)
        box_form.add_widget(self.in_reb_perda)
        self._montar_sim_nao(box_form, txt("label_dois_lados"), self.dois_lados, "reboco", "dois_lados")
        self._montar_sim_nao(box_form, txt("label_chapisco"), self.chapisco, "reboco", "chapisco")

        self._campos = {
            "area": self.in_reb_area, "vaos": self.in_reb_vaos,
            "esp": self.in_reb_esp, "perda": self.in_reb_perda,
        }

        if not ro:
            self.btn_calc_reb = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_reb)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_reboco = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_reboco.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_reboco
        box_res.add_widget(self.lbl_res_reboco)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    # ==========================================
    # CONTEÚDO DAS ABAS PISO E AZULEJO (mesma tela, campos um pouco diferentes)
    # ==========================================
    def montar_conteudo_ceramica(self, aba):
        scroll = RolagemComBarra()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura
        piso = (aba == "piso")

        def campo(hint, texto=""):
            return MDTextField(MDTextFieldHintText(text=hint), text=texto, mode="outlined", write_tab=False, readonly=ro)

        # --- Obrigatórios ---
        box_form.add_widget(MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        self.in_cer_area = campo(txt("hint_area_piso" if piso else "hint_area_azulejo"))
        box_form.add_widget(self.in_cer_area)
        if piso and not ro:
            self._montar_dica_contrapiso(box_form)
        self.in_cer_larg = campo(txt("hint_larg_peca"))
        self.in_cer_alt = campo(txt("hint_alt_peca"))
        box_form.add_widget(self.in_cer_larg)
        box_form.add_widget(self.in_cer_alt)

        # --- Opcionais ---
        # A perda começa vazia: vazia = automática pelo tamanho da peça (10%, 15%, 20% ou 25% com desenho)
        self.in_cer_vaos = campo(txt("hint_vaos"))
        self.in_cer_caixa = campo(txt("hint_m2_caixa"))
        self.in_cer_perda = campo(txt("hint_perda_auto"))
        if not piso:
            box_form.add_widget(self.in_cer_vaos)
        box_form.add_widget(self.in_cer_caixa)
        self._montar_sim_nao(box_form, txt("label_desenho"), self.desenho, aba, "desenho")
        box_form.add_widget(self.in_cer_perda)
        self._botoes_arg[aba] = self._montar_dropdown(
            box_form, txt("label_argamassa"), tipos_argamassa(sistema_unidades()), self.argamassa[aba],
            lambda v: self._escolher_argamassa(aba, v), rotulo=self._rotulo_argamassa,
            largura=None if sistema_unidades() == IMPERIAL else 200  # nos EUA o nome é mais comprido
        )
        self.in_cer_rodape = campo(txt("hint_rodape"))
        self.in_cer_rodape_peca = campo(txt("hint_rodape_peca"))
        if piso:
            box_form.add_widget(self.in_cer_rodape)
            box_form.add_widget(self.in_cer_rodape_peca)

        self._campos = {
            "area": self.in_cer_area, "larg": self.in_cer_larg, "alt": self.in_cer_alt,
            "caixa": self.in_cer_caixa, "perda": self.in_cer_perda,
        }
        if piso:
            self._campos["rodape"] = self.in_cer_rodape
            self._campos["rodape_peca"] = self.in_cer_rodape_peca
        else:
            self._campos["vaos"] = self.in_cer_vaos

        if not ro:
            self.btn_calc_cer = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_cer)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_ceramica = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_ceramica.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_ceramica
        box_res.add_widget(self.lbl_res_ceramica)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    def _area_contrapiso_digitada(self):
        """Área já digitada na aba Contrapiso (texto), ou None."""
        texto = ((self.estado_abas.get("contrapiso") or {}).get("area") or "").strip()
        try:
            return texto if texto and self._numero(texto) > 0 else None
        except ValueError:
            return None

    def _montar_dica_contrapiso(self, box_form):
        """Dica do .md: a área do Contrapiso pode ser reaproveitada no Piso (toque para usar)."""
        area = self._area_contrapiso_digitada()
        if not area:
            return
        self.btn_dica_contrapiso = MDButton(
            MDButtonText(text=txt("dica_area_contrapiso").format(area=area)),
            style="text", on_release=lambda x: setattr(self.in_cer_area, "text", area)
        )
        box_form.add_widget(self.btn_dica_contrapiso)

    # ==========================================
    # CONTEÚDO DA ABA LAJE (pré-moldada treliçada ou maciça)
    # ==========================================
    def montar_conteudo_laje(self):
        scroll = RolagemComBarra()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura
        premoldada = (self.laje_tipo == "premoldada")

        def campo(hint, texto=""):
            return MDTextField(MDTextFieldHintText(text=hint), text=texto, mode="outlined", write_tab=False, readonly=ro)

        # Os dois campos de espessura sempre existem (o que foi digitado não se perde ao trocar o tipo),
        # mas só aparece o do tipo escolhido
        self.in_laje_area = campo(txt("hint_area_laje"))
        self.in_laje_capa = campo(txt("hint_capa_laje"), self._texto_padrao(CAPA_PADRAO_CM, "centimetro"))
        self.in_laje_esp = campo(txt("hint_esp_laje"))
        self.in_laje_perda = campo(txt("hint_perda_bal"), self._texto_campo(PERDA_PADRAO_LAJE))

        # --- Obrigatórios ---
        box_form.add_widget(MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        box_form.add_widget(self.in_laje_area)
        self._botao_laje_tipo = self._montar_dropdown(
            box_form, txt("label_tipo_laje"), TIPOS_LAJE, self.laje_tipo,
            self._escolher_laje_tipo, rotulo=self._rotulo_laje, largura=None
        )
        if not premoldada:
            box_form.add_widget(self.in_laje_esp)

        # --- Opcionais (já vêm com valor padrão) ---
        if premoldada:
            self._botao_laje_ench = self._montar_dropdown(
                box_form, txt("label_enchimento"), ENCHIMENTOS, self.laje_enchimento,
                self._escolher_laje_enchimento, rotulo=self._rotulo_laje, largura=None
            )
            box_form.add_widget(self.in_laje_capa)
            self._montar_sim_nao(box_form, txt("label_tela"), self.tela, "laje", "tela")
        self._montar_seletor_traco(box_form, "laje")
        box_form.add_widget(self.in_laje_perda)

        self._campos = {
            "area": self.in_laje_area, "capa": self.in_laje_capa,
            "esp": self.in_laje_esp, "perda": self.in_laje_perda,
        }

        if not ro:
            self.btn_calc_laje = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_laje)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_laje = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_laje.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_laje
        box_res.add_widget(self.lbl_res_laje)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    @staticmethod
    def _rotulo_laje(chave):
        """Texto na tela para o tipo de laje e o enchimento."""
        return txt(f"opcao_{chave}")

    def _escolher_laje_tipo(self, valor):
        if valor == self.laje_tipo:
            return
        self.laje_tipo = valor
        self.textos_resultado.pop("laje", None)  # o resultado antigo era do outro tipo
        self.trocar_aba("laje")  # remonta a aba mostrando os campos do tipo escolhido

    def _escolher_laje_enchimento(self, valor):
        self.laje_enchimento = valor
        self._botao_laje_ench.text = self._rotulo_laje(valor)

    # ==========================================
    # CONTEÚDO DA ABA TELHADO (telhas, cumeeira e madeiramento)
    # ==========================================
    def montar_conteudo_telhado(self):
        scroll = RolagemComBarra()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        def campo(hint, texto=""):
            return MDTextField(MDTextFieldHintText(text=hint), text=texto, mode="outlined", write_tab=False, readonly=ro)

        # --- Obrigatórios ---
        box_form.add_widget(MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        self.in_tel_area = campo(txt("hint_area_telhado"))
        box_form.add_widget(self.in_tel_area)
        self._botao_telha_tipo = self._montar_dropdown(
            box_form, txt("label_tipo_telha"), TIPOS_TELHA, self.telha_tipo,
            self._escolher_telha_tipo, rotulo=self._rotulo_telha, largura=None
        )

        # --- Opcionais (já vêm com valor padrão) ---
        self.in_tel_incl = campo(txt("hint_inclinacao"), self._texto_campo(INCLINACAO_PADRAO[self.telha_tipo]))
        self.in_tel_cumeeira = campo(txt("hint_cumeeira"))
        self.in_tel_perda = campo(txt("hint_perda_bal"), self._texto_campo(PERDA_PADRAO_TELHADO))
        box_form.add_widget(self.in_tel_incl)
        box_form.add_widget(self.in_tel_cumeeira)
        self._montar_sim_nao(box_form, txt("label_madeiramento"), self.madeiramento, "telhado", "madeiramento")
        box_form.add_widget(self.in_tel_perda)

        self._campos = {
            "area": self.in_tel_area, "incl": self.in_tel_incl,
            "cumeeira": self.in_tel_cumeeira, "perda": self.in_tel_perda,
        }

        if not ro:
            self.btn_calc_tel = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_tel)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_telhado = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_telhado.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_telhado
        box_res.add_widget(self.lbl_res_telhado)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    @staticmethod
    def _rotulo_telha(chave):
        return txt(f"opcao_{chave}")

    def _escolher_telha_tipo(self, valor):
        antigo = self.telha_tipo
        self.telha_tipo = valor
        self._botao_telha_tipo.text = self._rotulo_telha(valor)
        # Se a inclinação ainda é a padrão do tipo antigo (ou está vazia), troca pela padrão do tipo novo
        incl_atual = self.in_tel_incl.text.strip()
        if not incl_atual or incl_atual == self._texto_campo(INCLINACAO_PADRAO[antigo]):
            self.in_tel_incl.text = self._texto_campo(INCLINACAO_PADRAO[valor])

    # ==========================================
    # CONTEÚDO DA ABA ELÉTRICA (estimativa por ponto, ou metragens do projeto)
    # ==========================================
    @staticmethod
    def _chave_fio(bitola):
        """1.5 -> 'fio1.5', 4.0 -> 'fio4' (chave do campo no estado e no Histórico)."""
        return f"fio{fmt_num(bitola, 0 if float(bitola).is_integer() else 1).replace(',', '.')}"

    @staticmethod
    def _rotulo_bitola_fio(bitola):
        return fmt_num(bitola, 0 if float(bitola).is_integer() else 1)

    def montar_conteudo_eletrica(self):
        scroll = RolagemComBarra()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        def campo(hint, texto=""):
            return MDTextField(MDTextFieldHintText(text=hint), text=texto, mode="outlined", write_tab=False, readonly=ro)

        # --- Obrigatórios ---
        box_form.add_widget(MDLabel(text=txt("secao_quantidades"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        self.in_ele_tomadas = campo(txt("hint_tomadas"))
        self.in_ele_interruptores = campo(txt("hint_interruptores"))
        self.in_ele_luzes = campo(txt("hint_luzes"))
        self.in_ele_chuveiros = campo(txt("hint_chuveiros"))      # acima de 5.500 W: fio 6 mm²
        self.in_ele_chuveiros4 = campo(txt("hint_chuveiros4"))    # até 5.500 W: fio 4 mm²
        box_form.add_widget(self.in_ele_tomadas)
        box_form.add_widget(self.in_ele_interruptores)
        box_form.add_widget(self.in_ele_luzes)
        box_form.add_widget(self.in_ele_chuveiros)
        box_form.add_widget(self.in_ele_chuveiros4)

        # --- Opcionais: metragens de quem já tem o projeto (vazio = o app estima) ---
        box_form.add_widget(MDLabel(text=txt("secao_projeto"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        self.in_ele_conduite = campo(txt("hint_conduite"))
        box_form.add_widget(self.in_ele_conduite)
        self._campos = {
            "tomadas": self.in_ele_tomadas, "interruptores": self.in_ele_interruptores,
            "luzes": self.in_ele_luzes, "chuveiros": self.in_ele_chuveiros,
            "chuveiros4": self.in_ele_chuveiros4, "conduite": self.in_ele_conduite,
        }
        for bitola in BITOLAS_FIO:
            campo_fio = campo(txt("hint_fio").format(b=self._rotulo_bitola_fio(bitola)))
            box_form.add_widget(campo_fio)
            self._campos[self._chave_fio(bitola)] = campo_fio
        self.in_ele_perda = campo(txt("hint_perda"), self._texto_campo(PERDA_PADRAO_ELETRICA))
        box_form.add_widget(self.in_ele_perda)
        self._campos["perda"] = self.in_ele_perda

        if not ro:
            self.btn_calc_ele = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_ele)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_eletrica = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_eletrica.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_eletrica
        box_res.add_widget(self.lbl_res_eletrica)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    # ==========================================
    # CONTEÚDO DA ABA HIDRÁULICA (estimativa por ponto, ou metragens do projeto)
    # ==========================================
    def montar_conteudo_hidraulica(self):
        scroll = RolagemComBarra()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        def campo(hint, texto=""):
            return MDTextField(MDTextFieldHintText(text=hint), text=texto, mode="outlined", write_tab=False, readonly=ro)

        self._campos = {}

        # --- Obrigatórios ---
        box_form.add_widget(MDLabel(text=txt("secao_quantidades"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        for chave in ("fria", "quente", "esgoto"):
            self._campos[chave] = campo(txt(f"hint_pontos_{chave}"))
            box_form.add_widget(self._campos[chave])

        # --- Opcionais: metragens de quem já tem o projeto (vazio = o app estima) ---
        box_form.add_widget(MDLabel(text=txt("secao_projeto"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        for tubo in TUBOS:
            self._campos[f"tubo_{tubo}"] = campo(txt(f"hint_tubo_{tubo}"))
            box_form.add_widget(self._campos[f"tubo_{tubo}"])
        self._campos["perda"] = campo(txt("hint_perda"), self._texto_campo(PERDA_PADRAO_HIDRAULICA))
        box_form.add_widget(self._campos["perda"])

        if not ro:
            self.btn_calc_hid = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_hid)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_hidraulica = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_hidraulica.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_hidraulica
        box_res.add_widget(self.lbl_res_hidraulica)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    @staticmethod
    def _texto_barras(qtd, metros_barra):
        """Ex.: '5 barras de 6 m'."""
        m = fmt_num(metros_barra, 0 if float(metros_barra).is_integer() else 1)
        return f"{fmt_int(qtd)} {(txt('un_barra_m') if qtd == 1 else txt('un_barras_m')).format(m=m)}"

    # ==========================================
    # CONTEÚDO DA ABA PINTURA (tinta de parede e de teto + complementos)
    # ==========================================
    def montar_conteudo_pintura(self):
        scroll = RolagemComBarra()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        def campo(hint, texto=""):
            return MDTextField(MDTextFieldHintText(text=hint), text=texto, mode="outlined", write_tab=False, readonly=ro)

        # --- Obrigatórios (basta uma das duas áreas) ---
        box_form.add_widget(MDLabel(text=txt("secao_areas"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        self.in_pint_parede = campo(txt("hint_area_parede_pint"))
        self.in_pint_teto = campo(txt("hint_area_teto_pint"))
        self.in_pint_demaos = campo(txt("hint_demaos"), self._texto_campo(DEMAOS_PADRAO))
        box_form.add_widget(self.in_pint_parede)
        box_form.add_widget(self.in_pint_teto)
        box_form.add_widget(self.in_pint_demaos)

        # --- Opcionais (já vêm com valor padrão) ---
        # Rendimento padrão: 12 m²/L no Brasil; 400 sq ft/gal nos EUA (o que os fabricantes de lá informam)
        eua = (sistema_unidades() == IMPERIAL)
        self.in_pint_rend = campo(txt("hint_rendimento"), self._rend_padrao_texto(sistema_unidades()))
        self.in_pint_perda = campo(txt("hint_perda"), self._texto_campo(PERDA_PADRAO_PINTURA))
        box_form.add_widget(self.in_pint_rend)
        # Nos EUA não aparecem selador nem massa: lá a parede é de drywall e só se usa o primer
        if not eua:
            self._montar_sim_nao(box_form, txt("label_selador"), self.selador, "pintura", "selador")
            self._botao_massa = self._montar_dropdown(
                box_form, txt("label_massa"), TIPOS_MASSA, self.massa_tipo,
                self._escolher_massa, rotulo=self._rotulo_massa, largura=None
            )
        self._montar_sim_nao(box_form, txt("label_fundo"), self.fundo, "pintura", "fundo")
        box_form.add_widget(self.in_pint_perda)

        self._campos = {
            "parede": self.in_pint_parede, "teto": self.in_pint_teto, "demaos": self.in_pint_demaos,
            "rend": self.in_pint_rend, "perda": self.in_pint_perda,
        }

        if not ro:
            self.btn_calc_pint = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_pint)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_pintura = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_pintura.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_pintura
        box_res.add_widget(self.lbl_res_pintura)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    @staticmethod
    def _rotulo_massa(chave):
        return txt(f"opcao_massa_{chave}")

    def _escolher_massa(self, valor):
        self.massa_tipo = valor
        self._botao_massa.text = self._rotulo_massa(valor)

    @staticmethod
    def _texto_latas_galoes(latas, galoes, sistema=None):
        """Ex.: '2 latas de 18 L e 1 galão de 3,6 L' (Brasil) ou '2 baldes de 5 gal e 1 galão de 1 gal' (EUA).
        sistema: o país em que a conta foi feita (None = o país escolhido agora)."""
        t = lambda chave: txt_do_pais(chave, sistema)
        partes = []
        if latas:
            partes.append(f"{fmt_int(latas)} {t('un_lata_18') if latas == 1 else t('un_latas_18')}")
        if galoes:
            partes.append(f"{fmt_int(galoes)} {t('un_galao_36') if galoes == 1 else t('un_galoes_36')}")
        return f" {t('un_e')} ".join(partes)

    @staticmethod
    def _med(valor_metrico, tipo, casas=2):
        """Medida do resultado (a conta é em métrico) com a unidade do país escolhido.
        Ex.: área 10 -> "10,00 m²" no Brasil ou "107.64 sq ft" nos EUA;
        peça 30 cm -> "30 cm" ou "11.811 in" (12 in digitado volta como "12 in");
        junta 0,79375 mm -> "1/32 in" (mm vai até 1/32 in; cm, até 1/16 in)."""
        sistema = sistema_unidades()
        if sistema == IMPERIAL:
            valor = do_metrico(valor_metrico, tipo, sistema)
            if tipo in ("centimetro", "milimetro"):
                return f"{texto_polegadas(valor, divisao=CalculatorScreen._divisao_polegada(tipo))} in"
            unidade = {"area": "sq ft", "comprimento": "ft", "peso": "lb", "litro": "gal",
                       "consumo": "lb/sq ft", "rendimento": "sq ft/gal"}[tipo]
            return f"{fmt_num(valor, casas)} {unidade}"
        if tipo in ("centimetro", "milimetro"):
            unidade = "cm" if tipo == "centimetro" else "mm"
            return f"{fmt_num(valor_metrico, 0 if float(valor_metrico).is_integer() else 1)} {unidade}"
        unidade = {"area": "m²", "comprimento": "m", "peso": "kg", "litro": "L",
                   "consumo": "kg/m²", "rendimento": "m²/L"}[tipo]
        return f"{fmt_num(valor_metrico, casas)} {unidade}"

    @staticmethod
    def _divisao_polegada(tipo):
        """Menor pedaço da fração nos EUA: as medidas pequenas em mm (junta e espessura do rejunte)
        vão até 1/32 in (0,79 mm -> "1/32"); as em cm (peça, estribo...) vão até 1/16 in."""
        return 32 if tipo == "milimetro" else 16

    @staticmethod
    def _texto_peca(larg, alt, sistema):
        """Tamanho da peça no resultado. Brasil: "60x60 cm" (igual a antes).
        EUA: com espaço, "12 x 12 in" e "11 3/4 x 12 in" (com fração, "11 3/4x12" ficava confuso)."""
        if sistema == IMPERIAL:
            lados = [texto_polegadas(do_metrico(v, "centimetro", sistema)) for v in (larg, alt)]
            return f"{lados[0]} x {lados[1]} in"
        n = lambda v: fmt_num(v, 0 if float(v).is_integer() else 1)
        return f"{n(larg)}x{n(alt)} cm"

    # ==========================================
    # CONTEÚDO DA ABA ESQUADRIAS (lista de portas e janelas + insumos de fixação)
    # ==========================================
    def montar_conteudo_esquadrias(self):
        scroll = RolagemComBarra()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        def campo(hint, texto=""):
            return MDTextField(MDTextFieldHintText(text=hint), text=texto, mode="outlined", write_tab=False, readonly=ro)

        # --- Formulário para adicionar uma porta ou janela (some no modo leitura) ---
        self.in_esq_qtd = campo(txt("hint_qtd_esquadria"))
        self.in_esq_larg = campo(txt("hint_larg_esquadria"))
        self.in_esq_alt = campo(txt("hint_alt_esquadria"))
        if not ro:
            box_form.add_widget(MDLabel(text=txt("secao_nova_esquadria"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
            self._botao_esq_tipo = self._montar_dropdown(
                box_form, txt("label_tipo_esquadria"), TIPOS_ESQUADRIA, self.esq_tipo,
                self._escolher_esq_tipo, rotulo=self._rotulo_esq_tipo, largura=None
            )
            self._botao_esq_material = self._montar_dropdown(
                box_form, txt("label_material"), MATERIAIS, self.esq_material,
                self._escolher_esq_material, rotulo=self._rotulo_material, largura=None
            )
            box_form.add_widget(self.in_esq_qtd)
            box_form.add_widget(self.in_esq_larg)
            box_form.add_widget(self.in_esq_alt)
            box_form.add_widget(MDButton(
                MDButtonIcon(icon="plus"), MDButtonText(text=txt("btn_adicionar_lista")),
                style="tonal", pos_hint={"center_x": 0.5}, on_release=self._adicionar_esquadria
            ))
        self._campos = {"qtd": self.in_esq_qtd, "larg": self.in_esq_larg, "alt": self.in_esq_alt}

        # --- Lista para cotação (cada item tem um X para remover) ---
        box_form.add_widget(MDLabel(text=txt("secao_lista_esquadrias"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        if not self.esquadrias_itens:
            box_form.add_widget(MDLabel(text=txt("msg_lista_vazia"), theme_text_color="Secondary", adaptive_height=True))
        for indice, item in enumerate(self.esquadrias_itens):
            linha = MDBoxLayout(size_hint_y=None, height="48dp", spacing="8dp")
            linha.add_widget(MDLabel(text=self._texto_item_esquadria(item), theme_text_color="Primary"))
            if not ro:
                linha.add_widget(MDIconButton(
                    icon="close", pos_hint={"center_y": 0.5},
                    on_release=lambda x, i=indice: self._remover_esquadria(i)
                ))
            box_form.add_widget(linha)

        # --- Opcionais: insumos de fixação ---
        box_form.add_widget(MDLabel(text=txt("secao_fixacao"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        self._montar_sim_nao(box_form, txt("label_espuma"), self.esq_fixacao, "espuma", "fixacao")
        self._montar_sim_nao(box_form, txt("label_parafusos"), self.esq_fixacao, "parafusos", "fixacao")
        self._montar_sim_nao(box_form, txt("label_argamassa_fix"), self.esq_fixacao, "argamassa", "fixacao")

        if not ro:
            self.btn_calc_esq = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_esq)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_esquadrias = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_esquadrias.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_esquadrias
        box_res.add_widget(self.lbl_res_esquadrias)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    @staticmethod
    def _rotulo_esq_tipo(chave):
        return txt(f"opcao_{chave}")

    @staticmethod
    def _rotulo_material(chave):
        return txt(f"opcao_mat_{chave}")

    def _escolher_esq_tipo(self, valor):
        self.esq_tipo = valor
        self._botao_esq_tipo.text = self._rotulo_esq_tipo(valor)

    def _escolher_esq_material(self, valor):
        self.esq_material = valor
        self._botao_esq_material.text = self._rotulo_material(valor)

    @staticmethod
    def _texto_item_esquadria(item):
        """Ex.: '3x Porta 80 x 210 cm (Madeira)' no Brasil, '3x Door 36 x 80 in' nos EUA.
        As medidas ficam guardadas em cm; nos EUA só são mostradas em polegadas."""
        if sistema_unidades() == IMPERIAL:
            larg = texto_polegadas(do_metrico(item["larg"], "centimetro", IMPERIAL))
            alt = texto_polegadas(do_metrico(item["alt"], "centimetro", IMPERIAL))
            unidade = "in"
        else:
            def n(v):
                return fmt_num(v, 0 if float(v).is_integer() else 1)
            larg, alt, unidade = n(item["larg"]), n(item["alt"]), "cm"
        texto = f"{fmt_int(item['qtd'])}x {CalculatorScreen._rotulo_esq_tipo(item['tipo'])} {larg} x {alt} {unidade}"
        if item["material"] != MATERIAL_PADRAO:
            texto += f" ({CalculatorScreen._rotulo_material(item['material'])})"
        return texto

    def _texto_total_esquadrias(self, portas, janelas):
        """Ex.: "4 portas e 5 janelas", "1 porta" (o que for zero não aparece)."""
        partes = []
        if portas > 0:
            partes.append(f"{fmt_int(portas)} {self._unidade(portas, 'un_porta', 'un_portas')}")
        if janelas > 0:
            partes.append(f"{fmt_int(janelas)} {self._unidade(janelas, 'un_janela', 'un_janelas')}")
        return f" {txt('un_e')} ".join(partes)

    def _adicionar_esquadria(self, instance=None):
        try:
            qtd = int(self.in_esq_qtd.text.strip())
            larg = self._numero(self.in_esq_larg.text)
            alt = self._numero(self.in_esq_alt.text)
        except ValueError:
            self._lbl_resultado.text = txt("msg_erro_num")
            return
        if qtd <= 0 or larg <= 0 or alt <= 0:
            self._lbl_resultado.text = txt("msg_erro_num")
            return
        # Nos EUA a pessoa digita em polegadas; a lista guarda sempre em cm
        sistema = sistema_unidades()
        larg = round(para_metrico(larg, "centimetro", sistema), 4)
        alt = round(para_metrico(alt, "centimetro", sistema), 4)

        # Limites com aviso (esquadrias.py): a janela abre antes de o item entrar na lista.
        # Continuar chama o Adicionar de novo (os campos continuam preenchidos) e o item entra.
        avisos = []
        self._aviso_maximo(avisos, "aviso_esq_qtd_max", qtd, QUANTIDADE_MAXIMA_ESQUADRIA)
        self._aviso_maximo(avisos, "aviso_esq_larg_max", larg, LARGURA_MAXIMA_ESQUADRIA_CM, "centimetro")
        self._aviso_maximo(avisos, "aviso_esq_alt_max", alt, ALTURA_MAXIMA_ESQUADRIA_CM, "centimetro")
        pendentes = self._avisos_pendentes("esquadrias", avisos)
        if pendentes:
            self._pedir_confirmacao("esquadrias", pendentes["aviso"], self._adicionar_esquadria)
            return

        # Mesmo tipo, material e tamanho: soma na quantidade em vez de repetir a linha
        for item in self.esquadrias_itens:
            if (item["tipo"], item["material"], item["larg"], item["alt"]) == (self.esq_tipo, self.esq_material, larg, alt):
                item["qtd"] += qtd
                break
        else:
            self.esquadrias_itens.append({"tipo": self.esq_tipo, "material": self.esq_material, "qtd": qtd, "larg": larg, "alt": alt})

        for campo in self._campos.values():  # limpa o formulário para a próxima
            campo.text = ""
        self.textos_resultado.pop("esquadrias", None)
        self.trocar_aba("esquadrias")

    def _remover_esquadria(self, indice):
        if 0 <= indice < len(self.esquadrias_itens):
            self.esquadrias_itens.pop(indice)
        self.textos_resultado.pop("esquadrias", None)
        self.trocar_aba("esquadrias")

    # ==========================================
    # CONTEÚDO DA ABA REJUNTE (pode reaproveitar os dados do Piso ou do Azulejo)
    # ==========================================
    def montar_conteudo_rejunte(self):
        scroll = RolagemComBarra()
        box_form = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        box_form.bind(minimum_height=box_form.setter('height'))
        ro = self.modo_somente_leitura

        def campo(hint, texto=""):
            return MDTextField(MDTextFieldHintText(text=hint), text=texto, mode="outlined", write_tab=False, readonly=ro)

        # --- Obrigatórios ---
        box_form.add_widget(MDLabel(text=txt("secao_dimensoes"), font_style="Title", role="small", bold=True, theme_text_color="Primary"))
        self.in_rej_area = campo(txt("hint_area_rejunte"))
        self.in_rej_larg = campo(txt("hint_larg_peca"))
        self.in_rej_alt = campo(txt("hint_alt_peca"))
        self.in_rej_junta = campo(txt("hint_junta_mm"))
        if not ro:
            self._montar_dicas_rejunte(box_form)
        box_form.add_widget(self.in_rej_area)
        box_form.add_widget(self.in_rej_larg)
        box_form.add_widget(self.in_rej_alt)
        box_form.add_widget(self.in_rej_junta)

        # --- Opcionais (já vêm com valor padrão) ---
        self.in_rej_esp = campo(txt("hint_esp_peca"), self._texto_padrao(ESPESSURA_PADRAO_MM, "milimetro"))
        self.in_rej_perda = campo(txt("hint_perda"), self._texto_campo(PERDA_PADRAO_REJUNTE))
        box_form.add_widget(self.in_rej_esp)
        box_form.add_widget(self.in_rej_perda)

        self._campos = {
            "area": self.in_rej_area, "larg": self.in_rej_larg, "alt": self.in_rej_alt,
            "junta": self.in_rej_junta, "esp": self.in_rej_esp, "perda": self.in_rej_perda,
        }

        if not ro:
            self.btn_calc_rej = MDButton(MDButtonText(text=txt("btn_calcular")), pos_hint={"center_x": 0.5}, on_release=self.executar_calculo)
            box_form.add_widget(self.btn_calc_rej)

        box_res = MDBoxLayout(orientation="vertical", spacing="12dp", padding=("0dp", "16dp", "0dp", "0dp"), size_hint_y=None)
        box_res.bind(minimum_height=box_res.setter('height'))

        self.lbl_res_rejunte = MDLabel(text=txt("msg_inicial"), theme_text_color="Secondary", size_hint_y=None)
        self.lbl_res_rejunte.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self._lbl_resultado = self.lbl_res_rejunte
        box_res.add_widget(self.lbl_res_rejunte)

        self._montar_botoes_fluxo(box_res)

        box_form.add_widget(box_res)
        scroll.add_widget(box_form)
        return scroll

    def _dados_ceramica_digitados(self, aba):
        """Área (já sem os vãos, no Azulejo), largura e altura digitadas no Piso/Azulejo, ou None."""
        e = self.estado_abas.get(aba) or {}
        try:
            area = self._numero(e.get("area"))
            larg = self._numero(e.get("larg"))
            alt = self._numero(e.get("alt"))
            vaos = self._numero(e.get("vaos"), 0.0) if aba == "azulejo" else 0.0
        except ValueError:
            return None
        area -= vaos
        if area <= 0 or larg <= 0 or alt <= 0:
            return None
        if sistema_unidades() == IMPERIAL:
            # Peça em polegadas com fração, igual se digita lá: 11.75 -> "11 3/4"
            return self._texto_campo(round(area, 2)), texto_polegadas(larg), texto_polegadas(alt)
        return self._texto_campo(round(area, 2)), self._texto_campo(larg), self._texto_campo(alt)

    def _montar_dicas_rejunte(self, box_form):
        """Dica em botão: "Usar dados do Piso (...)" / "Usar dados do Azulejo (...)".
        Ao tocar, preenche a área e o tamanho da peça com o que foi digitado naquela aba
        (igual à dica do Contrapiso na aba Piso)."""
        for aba in ("piso", "azulejo"):
            dados = self._dados_ceramica_digitados(aba)
            if not dados:
                continue
            area, larg, alt = dados
            # Peça: "60x60" no Brasil; "11 3/4 x 12" nos EUA (com espaço, igual ao resultado)
            peca = f"{larg} x {alt}" if sistema_unidades() == IMPERIAL else f"{larg}x{alt}"
            box_form.add_widget(MDButton(
                MDButtonText(text=sem_quebra(txt(f"dica_rejunte_{aba}").format(area=area, peca=peca))),
                style="text",
                on_release=lambda x, d=dados: self._usar_dados_ceramica(*d)
            ))

    def _usar_dados_ceramica(self, area, larg, alt):
        """Preenche a área e o tamanho da peça do Rejunte (a junta a pessoa ainda digita)."""
        self.in_rej_area.text = area
        self.in_rej_larg.text = larg
        self.in_rej_alt.text = alt

    @staticmethod
    def _rotulo_argamassa(tipo, sistema=None):
        """Brasil: o próprio nome (AC-I, AC-II...). EUA: "Modificada (ANSI A118.4)"..."""
        sistema = sistema or sistema_unidades()
        if sistema == IMPERIAL:
            return txt_do_pais(f"arg_{tipo}", sistema)
        return tipo

    def _escolher_argamassa(self, aba, valor):
        self.argamassa[aba] = valor
        if aba in self._botoes_arg:
            self._botoes_arg[aba].text = self._rotulo_argamassa(valor)

    # ==========================================
    # BOTÕES DO FLUXO: Limpar, Anterior (menos na 1ª aba), Próximo (menos na última) e Finalizar
    # (somem no modo leitura)
    # ==========================================
    def _montar_botoes_fluxo(self, box):
        """Limpar e Anterior (menos na 1ª aba); Próximo dentro da etapa; na última aba de cada etapa,
        "Avançar para a próxima etapa" no lugar do Próximo; Finalizar em todas."""
        if self.modo_somente_leitura:
            return
        posicao = ABAS_ORDEM.index(self.aba_atual)
        indice_etapa, _ = etapa_da_aba(self.aba_atual)
        abas_etapa = ETAPAS[indice_etapa][1]
        ultima_da_etapa = (self.aba_atual == abas_etapa[-1])
        ultima_etapa = (indice_etapa == len(ETAPAS) - 1)

        linha = MDBoxLayout(size_hint_y=None, height="48dp", spacing="8dp")
        linha.add_widget(MDWidget())
        self.btn_limpar = MDButton(MDButtonText(text=txt("btn_limpar")), style="outlined", on_release=self.pedir_limpar)
        linha.add_widget(self.btn_limpar)
        if posicao > 0:
            anterior = ABAS_ORDEM[posicao - 1]
            self.btn_anterior = MDButton(MDButtonText(text=txt("btn_anterior")), style="outlined", on_release=lambda x: self.trocar_aba(anterior))
            linha.add_widget(self.btn_anterior)
        if not ultima_da_etapa:
            proxima = ABAS_ORDEM[posicao + 1]
            self.btn_proximo = MDButton(MDButtonText(text=txt("btn_proximo")), style="outlined", on_release=lambda x: self.trocar_aba(proxima))
            linha.add_widget(self.btn_proximo)
        linha.add_widget(MDWidget())
        box.add_widget(linha)

        # Fim da etapa: o botão é maior, então fica numa linha só dele (não cabe ao lado dos outros no celular)
        if ultima_da_etapa and not ultima_etapa:
            primeira_da_proxima = ETAPAS[indice_etapa + 1][1][0]
            self.btn_avancar_etapa = MDButton(
                MDButtonIcon(icon="arrow-right"), MDButtonText(text=txt("btn_avancar_etapa")),
                style="tonal", pos_hint={"center_x": 0.5},
                on_release=lambda x: self.trocar_aba(primeira_da_proxima)
            )
            box.add_widget(self.btn_avancar_etapa)

        self.btn_finalizar = MDButton(MDButtonText(text=txt("btn_finalizar")), style="filled", pos_hint={"center_x": 0.5}, on_release=self.finalizar_e_ir_resumo)
        box.add_widget(self.btn_finalizar)

    def pedir_limpar(self, instance=None):
        if self.dialog_limpar:
            self.dialog_limpar.dismiss()
        self.dialog_limpar = MDDialog(
            MDDialogHeadlineText(text=txt("btn_limpar")),
            MDDialogSupportingText(text=txt("dialog_limpar")),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text=txt("btn_cancelar")), on_release=lambda x: self.dialog_limpar.dismiss()),
                MDButton(MDButtonText(text=txt("btn_confirmar")), on_release=self.limpar_aba_atual)
            )
        )
        self.dialog_limpar.open()

    def limpar_aba_atual(self, instance=None):
        """Apaga só a aba aberta (as outras não são afetadas)."""
        aba = self.aba_atual
        self.estado_abas.pop(aba, None)
        self.textos_resultado.pop(aba, None)
        self._avisos_aceitos.pop(aba, None)
        self.traco[aba] = self._tabela_traco(aba)[1]
        if aba in self.tijolo:
            self.tijolo[aba] = TIJOLO_PADRAO
        if aba in self.assent:
            self.assent[aba] = ASSENTAMENTO_PADRAO
        if aba in self.bitola:
            self.bitola[aba] = BITOLA_PADRAO
        if aba in self.imperm:
            self.imperm[aba] = False
        if aba in self.dois_lados:
            self.dois_lados[aba] = False
        if aba in self.chapisco:
            self.chapisco[aba] = False
        if aba in self.argamassa:
            self.argamassa[aba] = argamassa_padrao(aba == "piso", sistema_unidades())
        if aba in self.desenho:
            self.desenho[aba] = False
        if aba == "laje":
            self.laje_tipo = TIPO_LAJE_PADRAO
            self.laje_enchimento = ENCHIMENTO_PADRAO
            self.tela["laje"] = False
        if aba == "telhado":
            self.telha_tipo = TIPO_TELHA_PADRAO
            self.madeiramento[aba] = False
        if aba == "pintura":
            self.selador[aba] = False
            self.fundo[aba] = False
            self.massa_tipo = "nenhuma"
        if aba == "esquadrias":
            self.esquadrias_itens = []
            self.esq_tipo = TIPO_ESQUADRIA_PADRAO
            self.esq_material = MATERIAL_PADRAO
            self.esq_fixacao = {"espuma": False, "parafusos": False, "argamassa": False}
        self._campos = {}
        self.trocar_aba(aba)
        if self.dialog_limpar:
            self.dialog_limpar.dismiss()

    # ==========================================
    # DROPDOWNS (traço do concreto e bitola do ferro)
    # ==========================================
    @staticmethod
    def _rotulo_bitola(bitola):
        if float(bitola).is_integer():
            return f"{int(bitola)} mm"
        return f"{fmt_num(bitola, 1)} mm"

    def _montar_dropdown(self, box_form, titulo, opcoes, atual, ao_escolher, rotulo=str, largura=200):
        """Título + botão que abre a lista de opções. Retorna o texto do botão (mostra a opção atual)."""
        # O título fica 14dp mais baixo que o próprio texto: o texto "sobra" 7dp para cima e 7dp para baixo,
        # dentro do espaço de 16dp entre os campos. Assim ele fica perto do campo de cima e do botão,
        # igual aos títulos de seção (ex.: "Armadura / Ferragem"). A altura segue o texto, então um
        # título que quebra em 2 linhas continua sem invadir o campo de cima.
        lbl_titulo = MDLabel(
            text=titulo, font_style="Title", role="small", bold=True, theme_text_color="Primary",
            size_hint_y=None
        )
        lbl_titulo.bind(texture_size=lambda instance, value: setattr(instance, "height", max(dp(1), value[1] - dp(14))))
        box_form.add_widget(lbl_titulo)
        texto = MDButtonText(text=rotulo(atual))
        botao = MDButton(
            MDButtonIcon(icon="menu-down"),
            texto,
            style="outlined",
            size_hint_x=1,
            disabled=self.modo_somente_leitura,
            on_release=lambda x: self._abrir_menu(x, opcoes, ao_escolher, rotulo, largura)
        )
        box_form.add_widget(botao)
        return texto

    def _abrir_menu(self, caller, opcoes, ao_escolher, rotulo, largura=200):
        if self.menu_ativo:
            self.menu_ativo.dismiss()
        # largura=None: o menu vai da borda esquerda do botão até perto da borda da janela,
        # para nomes compridos não serem cortados (ex.: "Tijolo baiano 9 furos (9x14x19)").
        # O MenuAlinhado garante que ele não sai da janela.
        if largura:
            largura_menu = dp(largura)
        else:
            x_botao = caller.to_window(caller.x, caller.y)[0]  # onde o botão começa, na janela
            largura_menu = max(caller.width, Window.width - x_botao - dp(16))
        itens = [
            {"text": rotulo(opcao), "on_release": lambda *args, o=opcao: self._escolher_no_menu(ao_escolher, o)}
            for opcao in opcoes
        ]
        self.menu_ativo = MenuAlinhado(caller=caller, items=itens, width=largura_menu, position="bottom")
        self.menu_ativo.open()

    def _escolher_no_menu(self, ao_escolher, opcao):
        ao_escolher(opcao)
        if self.menu_ativo:
            self.menu_ativo.dismiss()

    # --- Traço do concreto ou da massa ---
    @staticmethod
    def _tabela_traco(aba):
        """Concreto (Brocas, Baldrame, Laje, Contrapiso) ou massa (Paredes, Reboco):
        tabela de traços, traço padrão e título do campo."""
        if aba == "paredes":
            return TRACOS_MASSA, TRACO_MASSA_PADRAO, "label_traco_massa"
        if aba == "reboco":
            return TRACOS_MASSA, TRACO_MASSA_PADRAO, "label_traco_massa_obrig"
        if aba == "contrapiso":
            return TRACOS_CONCRETO, TRACO_PADRAO_CONTRAPISO, "label_traco"  # contrapiso usa 1:3:3
        return TRACOS_CONCRETO, TRACO_CONCRETO_PADRAO, "label_traco"

    @staticmethod
    def _rotulo_traco(nome):
        """Traço na tela com o separador decimal do país: "1:0,5:6" no Brasil, "1:0.5:6" nos EUA.
        Por dentro, a chave continua "1:0.5:6" (é assim que fica no tracos.py e no Histórico)."""
        return nome.replace(".", CONFIG_APP["separador_decimal"])

    def _montar_seletor_traco(self, box_form, aba):
        tabela, _, titulo = self._tabela_traco(aba)
        self._botoes_traco[aba] = self._montar_dropdown(
            box_form, txt(titulo), list(tabela.keys()), self.traco[aba],
            lambda nome: self._escolher_traco(aba, nome), rotulo=self._rotulo_traco
        )

    def _escolher_traco(self, aba, nome):
        self.traco[aba] = nome
        if aba in self._botoes_traco:
            self._botoes_traco[aba].text = self._rotulo_traco(nome)

    # --- Bitola do ferro ---
    def _montar_seletor_bitola(self, box_form, aba):
        self._botoes_bitola[aba] = self._montar_dropdown(
            box_form, txt("label_bitola"), BITOLAS_LONGITUDINAL, self.bitola[aba],
            lambda b: self._escolher_bitola(aba, b), rotulo=self._rotulo_bitola
        )

    def _escolher_bitola(self, aba, bitola):
        self.bitola[aba] = bitola
        if aba in self._botoes_bitola:
            self._botoes_bitola[aba].text = self._rotulo_bitola(bitola)

    # --- Tijolo / bloco e assentamento (Paredes) ---
    @staticmethod
    def _rotulo_tijolo(chave):
        return txt(f"tj_{chave}")

    def _montar_seletor_tijolo(self, box_form, aba):
        self._botoes_tijolo[aba] = self._montar_dropdown(
            box_form, txt("label_tijolo"), list(TIJOLOS.keys()), self.tijolo[aba],
            lambda t: self._escolher_tijolo(aba, t), rotulo=self._rotulo_tijolo, largura=None
        )

    def _escolher_tijolo(self, aba, chave):
        self.tijolo[aba] = chave
        if aba in self._botoes_tijolo:
            self._botoes_tijolo[aba].text = self._rotulo_tijolo(chave)

    @staticmethod
    def _rotulo_assent(chave):
        return txt(f"opcao_{chave}")

    def _montar_seletor_assent(self, box_form, aba):
        self._botoes_assent[aba] = self._montar_dropdown(
            box_form, txt("label_assent"), ASSENTAMENTOS, self.assent[aba],
            lambda a: self._escolher_assent(aba, a), rotulo=self._rotulo_assent
        )

    def _escolher_assent(self, aba, chave):
        self.assent[aba] = chave
        if aba in self._botoes_assent:
            self._botoes_assent[aba].text = self._rotulo_assent(chave)

    # --- Sim / Não genérico (Reboco: dois lados e chapisco) ---
    def _montar_sim_nao(self, box_form, titulo, estado, aba, nome):
        self._botoes_sn[(nome, aba)] = self._montar_dropdown(
            box_form, titulo, [False, True], estado[aba],
            lambda v: self._escolher_sim_nao(estado, aba, nome, v), rotulo=self._rotulo_sim_nao
        )

    def _escolher_sim_nao(self, estado, aba, nome, valor):
        estado[aba] = valor
        if (nome, aba) in self._botoes_sn:
            self._botoes_sn[(nome, aba)].text = self._rotulo_sim_nao(valor)

    # --- Impermeabilização (Sim / Não) ---
    @staticmethod
    def _rotulo_sim_nao(valor):
        return txt("opcao_sim") if valor else txt("opcao_nao")

    def _montar_seletor_imperm(self, box_form, aba):
        self._botoes_imperm[aba] = self._montar_dropdown(
            box_form, txt("label_imperm"), [False, True], self.imperm[aba],
            lambda v: self._escolher_imperm(aba, v), rotulo=self._rotulo_sim_nao
        )

    def _escolher_imperm(self, aba, valor):
        self.imperm[aba] = valor
        if aba in self._botoes_imperm:
            self._botoes_imperm[aba].text = self._rotulo_sim_nao(valor)

    # --- Ajuda "?" da aba (inclui a nota sobre os valores padrão) ---
    def abrir_ajuda(self, instance=None):
        if self.dialog_ajuda:
            self.dialog_ajuda.dismiss()
        texto = f"{txt(f'ajuda_{self.aba_atual}')}\n\n{txt('nota_opcionais')}"
        # EUA + português: explica as siglas (ft, in, sq ft...) no fim da ajuda
        if sistema_unidades() == IMPERIAL and CONFIG_APP.get("idioma", "pt").lower() == "pt":
            texto += f"\n\n{txt('legenda_unidades')}"
        self.dialog_ajuda = MDDialog(
            MDDialogHeadlineText(text=txt("titulo_ajuda")),
            MDDialogSupportingText(text=texto),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text=txt("btn_fechar")), on_release=lambda x: self.dialog_ajuda.dismiss())
            )
        )
        self.dialog_ajuda.open()

    # ==========================================
    # UNIDADES DA VERSÃO EUA (as contas são sempre em métrico; aqui só se traduz o texto)
    # ==========================================
    @staticmethod
    def _formatar_medida(valor_metrico, tipo, sistema):
        """Texto de uma medida (guardada em métrico) nas unidades do sistema.
        Polegadas saem em fração (3/8, 1 1/2) quando o número permite."""
        if sistema != IMPERIAL:
            return CalculatorScreen._texto_campo(round(valor_metrico, 2))
        convertido = do_metrico(valor_metrico, tipo, sistema)
        if tipo in ("centimetro", "milimetro"):
            return texto_polegadas(convertido, divisao=CalculatorScreen._divisao_polegada(tipo))
        return CalculatorScreen._texto_campo(round(convertido, 3))

    @staticmethod
    def _texto_padrao(valor_metrico, tipo):
        """Valor que já vem preenchido no campo. Nos EUA, arredonda para um número "redondo" de lá:
        1 cm -> 3/8 in, 15 cm -> 6 in, 8 mm -> 5/16 in, 10 m²/L -> 400 sq ft/gal."""
        sistema = sistema_unidades()
        if sistema != IMPERIAL:
            return CalculatorScreen._texto_campo(valor_metrico)
        convertido = do_metrico(valor_metrico, tipo, sistema)
        if tipo in ("centimetro", "milimetro"):
            if convertido >= 4:
                return str(round(convertido))  # medida grande: polegada inteira
            return texto_polegadas(convertido, aproximar=True, divisao=16 if tipo == "milimetro" else 8)
        if tipo == "rendimento":
            return str(int(round(convertido / 25.0) * 25))  # de 25 em 25 sq ft/gal
        return CalculatorScreen._texto_campo(round(convertido, 2))

    @staticmethod
    def _texto_medida(aba, chave, valor):
        """Valor salvo no Histórico (sempre em métrico) -> texto do campo nas unidades atuais."""
        tipo = UNIDADE_CAMPO.get(aba, {}).get(chave)
        sistema = sistema_unidades()
        numero = isinstance(valor, (int, float)) and not isinstance(valor, bool)
        if tipo is None or sistema != IMPERIAL or not numero:
            return CalculatorScreen._texto_campo(valor)
        return CalculatorScreen._formatar_medida(valor, tipo, sistema)

    def _estado_metrico(self, aba, e):
        """Cópia do texto digitado com as medidas já em métrico (é isso que vai para a conta).
        No Brasil, devolve o mesmo texto. Número inválido dá ValueError (o _calcular_aba trata)."""
        sistema = sistema_unidades()
        if sistema != IMPERIAL:
            return e
        convertido = dict(e)
        for chave, tipo in UNIDADE_CAMPO.get(aba, {}).items():
            texto = (e.get(chave) or "").strip()
            if texto:
                convertido[chave] = repr(para_metrico(self._numero(texto), tipo, sistema))
        return convertido

    def _converter_estado_abas(self, antigo, novo):
        """O país mudou com abas preenchidas: reescreve as medidas digitadas nas unidades novas
        (ex.: 3 m vira 9.84 ft). Os resultados antigos são apagados (estavam na unidade velha)."""
        separador = "," if antigo == METRICO else "."
        rend_antes = ((self.estado_abas.get("pintura") or {}).get("rend") or "").strip()
        for aba, estado in self.estado_abas.items():
            for chave, tipo in UNIDADE_CAMPO.get(aba, {}).items():
                texto = (estado.get(chave) or "").strip()
                if not texto:
                    continue
                try:
                    valor = ler_numero(texto, separador)
                except ValueError:
                    continue  # texto inválido fica como está (o Calcular avisa)
                estado[chave] = self._formatar_medida(para_metrico(valor, tipo, antigo), tipo, novo)
        # Rendimento da tinta que ainda era o padrão do país antigo: vira o padrão do país novo
        # (12 m²/L <-> 400 sq ft/gal), em vez de um número quebrado como 491 sq ft/gal
        pintura = self.estado_abas.get("pintura")
        if pintura is not None and rend_antes == self._rend_padrao_texto(antigo):
            pintura["rend"] = self._rend_padrao_texto(novo)
        self.textos_resultado.clear()

    @staticmethod
    def _rend_padrao_texto(sistema):
        """Texto do rendimento padrão da tinta: "12" (m²/L) no Brasil, "400" (sq ft/gal) nos EUA."""
        if sistema == IMPERIAL:
            return str(RENDIMENTO_PADRAO_EUA_SQFT_GAL)
        return CalculatorScreen._texto_campo(RENDIMENTO_PADRAO_M2_L)

    # ==========================================
    # CÁLCULOS (a partir do texto digitado, sem depender dos campos na tela)
    # ==========================================
    @staticmethod
    def _numero(texto, padrao=0.0):
        """Lê o número digitado. Aceita decimal (2,5 ou 2.5) e fração (1/8, 2 1/2)."""
        return ler_numero(texto, CONFIG_APP["separador_decimal"], padrao)

    @staticmethod
    def _num_curto(valor, casas=2):
        """Número sem zeros sobrando: 10 -> "10", 2,5 -> "2,5", 29,75 -> "29,75", 2000 -> "2.000".
        (Antes a perda 2,5% aparecia como "2%" e o espaçamento 12,5 cm como "12 cm".)
        Os zeros só são tirados depois da vírgula: antes, 2000 virava "2" (o limite da Paredes)."""
        texto = fmt_num(valor, casas)
        sep = CONFIG_APP["separador_decimal"]
        if sep in texto:
            texto = texto.rstrip("0").rstrip(sep)
        return texto

    @staticmethod
    def _unidade(qtd, singular, plural, sistema=None):
        """Escolhe o singular ou o plural da unidade: "1 saco", "2 sacos".
        Com número quebrado, o singular vai até menos de 2, como se fala em português:
        "0,79 milheiro", "1,58 milheiro", "2,5 milheiros". Zero fica no plural ("0 sacos").
        singular e plural são as chaves dos textos (ex.: "un_saco" e "un_sacos")."""
        return txt_do_pais(singular if 0 < abs(qtd) < 2 else plural, sistema)

    @staticmethod
    def _txt_milheiros(milheiros, sistema=None):
        """O milheiro dos tijolos entre parênteses: " (0,79 milheiro)", " (2,50 milheiros)".
        "Milheiro" é um jeito brasileiro de comprar tijolo e não tem igual em inglês: lá o texto
        un_milheiro fica vazio e este parêntese não aparece (só "788 pcs"). Usado na aba Paredes
        e na lista de compras (regra 17: o Resumo igual à aba). Pendência 4 da rodada 2."""
        if not txt_do_pais('un_milheiro', sistema):
            return ""
        unidade = CalculatorScreen._unidade(milheiros, 'un_milheiro', 'un_milheiros', sistema)  # 0,79 e 1,58 milheiro; 2,5 milheiros
        return f" ({fmt_num(milheiros, 2)} {unidade})"

    def _linhas_concreto(self, res, custo_cimento, custo_areia, custo_pedra):
        """Linhas do cimento, da areia e da brita (Brocas, Baldrame, Laje e Contrapiso).
        O material que dá zero não aparece (regra 14): ex.: viga minúscula com 0,00 m³ de areia."""
        linhas = ""
        if res['sacos_cimento'] > 0:
            qtd = res['sacos_cimento']
            linhas += f"• {txt('label_cimento')}: {fmt_int(qtd)} {self._unidade(qtd, 'un_saco', 'un_sacos')} ({fmt_moeda(custo_cimento)})\n"
        if arredondar(res['areia_m3'], 2) > 0:
            linhas += f"• {txt('label_areia')}: {fmt_num(res['areia_m3'], 2)} m³ ({fmt_moeda(custo_areia)})\n"
        if arredondar(res['pedra_m3'], 2) > 0:
            linhas += f"• {txt('label_pedra')}: {fmt_num(res['pedra_m3'], 2)} m³ ({fmt_moeda(custo_pedra)})\n"
        return linhas

    def _linhas_massa(self, res, custo_cimento, custo_cal, custo_areia):
        """Linhas do cimento, da cal e da areia da massa (Paredes e Reboco).
        O que dá zero não aparece (regra 14): ex.: o traço 1:0:3 não tem cal."""
        linhas = ""
        if res['sacos_cimento'] > 0:
            qtd = res['sacos_cimento']
            linhas += f"• {txt('label_cimento')}: {fmt_int(qtd)} {self._unidade(qtd, 'un_saco', 'un_sacos')} ({fmt_moeda(custo_cimento)})\n"
        if res['sacos_cal'] > 0:
            qtd = res['sacos_cal']
            linhas += f"• {txt('label_cal')}: {fmt_int(qtd)} {self._unidade(qtd, 'un_saco_cal', 'un_sacos_cal')} ({fmt_moeda(custo_cal)})\n"
        if arredondar(res['areia_m3'], 2) > 0:
            linhas += f"• {txt('label_areia')}: {fmt_num(res['areia_m3'], 2)} m³ ({fmt_moeda(custo_areia)})\n"
        return linhas

    @staticmethod
    def _txt_perda(perda):
        """Texto da perda, igual em todas as abas: "com 2,5% de perda" (inglês: "with 2.5% waste")."""
        return txt("label_com_perda").format(p=CalculatorScreen._num_curto(perda))

    def _med_curto(self, valor_metrico, tipo, casas=2):
        """Medida curta para os avisos, na unidade do país: "300 m", "0,2 cm", "98,43 ft", "12 in"."""
        sistema = sistema_unidades()
        valor = do_metrico(valor_metrico, tipo, sistema)
        if sistema == IMPERIAL and tipo in ("centimetro", "milimetro"):
            return f"{texto_polegadas(valor, divisao=self._divisao_polegada(tipo))} in"
        return f"{self._num_curto(valor, casas)} {nome_unidade(tipo, sistema)}"

    def _limite_cm(self, valor_cm):
        """Limite em cm para os avisos: "20 cm" no Brasil, "8 in" (arredondado) nos EUA."""
        unidade = "in" if sistema_unidades() == IMPERIAL else "cm"
        return f"{self._texto_padrao(valor_cm, 'centimetro')} {unidade}"

    # ==========================================
    # AVISOS DE LIMITE ("passou do limite, deseja continuar?")
    # Passar do limite não impede a conta: pode existir obra de qualquer tamanho.
    # A pessoa vê o aviso e escolhe Cancelar (corrige o número) ou Continuar (calcula assim mesmo).
    # ==========================================
    def _avisos_pendentes(self, aba, avisos):
        """Só os avisos que a pessoa ainda não aceitou nesta aba. Retorna {"aviso": [...]} ou None."""
        aceitos = self._avisos_aceitos.get(aba, set())
        pendentes = [aviso for aviso in avisos if aviso not in aceitos]
        return {"aviso": pendentes} if pendentes else None

    def _pedir_confirmacao(self, aba, avisos, depois):
        """Mostra os avisos com Cancelar / Continuar. Continuar guarda o aceite e faz de novo
        o que a pessoa tinha pedido (depois = Calcular ou Finalizar)."""
        if self.dialog_aviso:
            self.dialog_aviso.dismiss()

        def continuar(*args):
            self._avisos_aceitos.setdefault(aba, set()).update(avisos)
            self.dialog_aviso.dismiss()
            depois()

        texto = "\n\n".join(avisos) + f"\n\n{txt('aviso_continuar')}"
        self.dialog_aviso = MDDialog(
            MDDialogHeadlineText(text=txt("aviso_titulo")),
            MDDialogSupportingText(text=texto),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text=txt("btn_cancelar")), on_release=lambda x: self.dialog_aviso.dismiss()),
                MDButton(MDButtonText(text=txt("btn_continuar")), on_release=continuar)
            )
        )
        self.dialog_aviso.open()

    def _med_limite(self, valor_metrico, tipo):
        """Limite para os avisos, na unidade do país: "2.000 m²", "0,5 cm", "15 mm".
        Nos EUA, cm e mm viram polegadas "redondas" (ex.: 8 cm -> 3 1/8 in), igual ao _limite_cm."""
        if sistema_unidades() == IMPERIAL and tipo in ("centimetro", "milimetro"):
            return f"{self._texto_padrao(valor_metrico, tipo)} in"
        return self._med_curto(valor_metrico, tipo, 0 if tipo == "area" else 2)

    def _limite_no_pais(self, valor_metrico, tipo):
        """O limite do jeito que aparece no aviso, de volta em métrico. No Brasil não muda nada.
        Nos EUA o limite aparece arredondado (3 cm -> 1 1/8 in; 2.000 m² -> 21,528 sq ft), então a conta
        compara com esse número, senão quem digitasse 1 1/8 in veria "1 1/8 in: o normal é de 1 1/8 in..."."""
        sistema = sistema_unidades()
        if sistema != IMPERIAL or not tipo:
            return valor_metrico
        if tipo in ("centimetro", "milimetro"):
            mostrado = ler_numero(self._texto_padrao(valor_metrico, tipo), ".")
        else:
            mostrado = round(do_metrico(valor_metrico, tipo, sistema), 0 if tipo == "area" else 2)
        return para_metrico(mostrado, tipo, sistema)

    def _fora_da_faixa(self, valor, minimo, maximo, tipo):
        """Fora da faixa normal? Zero e número negativo não contam (continuam dando a mensagem de erro)."""
        return 0 < valor < self._limite_no_pais(minimo, tipo) or valor > self._limite_no_pais(maximo, tipo)

    def _aviso_maximo(self, avisos, chave, valor, maximo, tipo=None):
        """Passou do máximo: acrescenta o aviso. tipo = "area", "centimetro"... (medida, na unidade
        do país) ou None (quantidade ou porcentagem, sem unidade: tomadas, demãos, inclinação)."""
        if valor > self._limite_no_pais(maximo, tipo):
            if tipo:
                avisos.append(txt(chave).format(valor=self._med_curto(valor, tipo), max=self._med_limite(maximo, tipo)))
            else:
                avisos.append(txt(chave).format(valor=self._num_curto(valor), max=self._num_curto(maximo)))

    def _aviso_faixa(self, avisos, chave, valor, minimo, maximo, tipo):
        """Fora da faixa normal (ex.: capa de 3 a 8 cm): acrescenta o aviso.
        Zero e número negativo não entram aqui: continuam dando a mensagem de erro de antes."""
        if self._fora_da_faixa(valor, minimo, maximo, tipo):
            avisos.append(txt(chave).format(
                valor=self._med_curto(valor, tipo),
                min=self._med_limite(minimo, tipo), max=self._med_limite(maximo, tipo)))

    def _aba_iniciada(self, aba, estado):
        if aba == "esquadrias" and self.esquadrias_itens:
            return True  # a lista já tem itens (mesmo com o formulário vazio)
        return any((estado.get(chave) or "").strip() for chave in CAMPOS_INICIAIS[aba])

    @staticmethod
    def _txt_erro(chave):
        """Mensagem de erro de uma conta (src/calculators), no idioma escolhido.
        As contas devolvem uma chave (ex.: 'erro_perda_negativa'); aqui ela vira a frase:
        'Erro: A perda não pode ser negativa.' / 'Error: Waste cannot be negative.'"""
        return f"{txt('label_erro')}: {txt(chave)}"

    def _calcular_aba(self, aba, e):
        """Retorna {"erro": mensagem} ou {"texto": resultado na tela, "resultado": dados da etapa}."""
        try:
            e = self._estado_metrico(aba, e)  # nos EUA: ft, in, sq ft... viram m, cm, m²...
            if aba == "baldrame":
                return self._calcular_baldrame(e)
            if aba == "paredes":
                return self._calcular_paredes(e)
            if aba == "contrapiso":
                return self._calcular_contrapiso(e)
            if aba == "reboco":
                return self._calcular_reboco(e)
            if aba in ("piso", "azulejo"):
                return self._calcular_ceramica(aba, e)
            if aba == "rejunte":
                return self._calcular_rejunte(e)
            if aba == "laje":
                return self._calcular_laje(e)
            if aba == "telhado":
                return self._calcular_telhado(e)
            if aba == "eletrica":
                return self._calcular_eletrica(e)
            if aba == "hidraulica":
                return self._calcular_hidraulica(e)
            if aba == "pintura":
                return self._calcular_pintura(e)
            if aba == "esquadrias":
                return self._calcular_esquadrias(e)
            return self._calcular_brocas(e)
        except ValueError:
            return {"erro": txt("msg_erro_num")}

    def _calcular_brocas(self, e):
        if not (e.get("qtd") or "").strip() or not (e.get("prof") or "").strip() or not (e.get("diam") or "").strip():
            return {"erro": txt("msg_erro_num")}

        qtd = int(e["qtd"].strip())
        prof = self._numero(e["prof"])
        diam = self._numero(e["diam"])
        perda = self._numero(e.get("perda"), 10.0)
        t_barras = (e.get("barras") or "").strip()
        num_barras = int(t_barras) if t_barras else 0
        esp_estribo = self._numero(e.get("esp_estribo"), 0.0)
        preco_mo = self._numero(e.get("mo"), 0.0)
        bitola = self.bitola["brocas"]

        # Profundidade acima do limite do engenheiro (ex.: 300 no lugar de 3,00): pergunta se quer continuar.
        # O limite é em metros; nos EUA o aviso mostra em ft.
        avisos = []
        if prof > PROFUNDIDADE_MAXIMA_M:
            avisos.append(txt("aviso_prof_max").format(
                valor=self._med_curto(prof, "comprimento"), max=self._med_curto(PROFUNDIDADE_MAXIMA_M, "comprimento")))
        pendentes = self._avisos_pendentes("brocas", avisos)
        if pendentes:
            return pendentes

        res = calcular_brocas(
            quantidade=qtd, profundidade_m=prof, diametro_cm=diam,
            perda_percentual=perda, incluir_ferragem=(num_barras > 0),
            num_barras_longitudinais=num_barras, bitola_mm=bitola,
            preco_mao_obra_metro=preco_mo, traco=self.traco["brocas"],
            espacamento_estribo_cm=esp_estribo
        )
        if "erro" in res:
            return {"erro": self._txt_erro(res['erro'])}

        custo_cimento = res['sacos_cimento'] * TABELA_PRECOS_GLOBAL.cimento_50kg
        custo_areia = res['areia_m3'] * TABELA_PRECOS_GLOBAL.areia_m3
        custo_pedra = res['pedra_m3'] * TABELA_PRECOS_GLOBAL.pedra_m3
        custo_aco = res['quilos_aco'] * TABELA_PRECOS_GLOBAL.aco_kg if res['incluiu_ferragem'] else 0.0
        custo_arame = res['arame_kg'] * PRECO_ARAME_KG if res['incluiu_ferragem'] else 0.0
        custo_aco += custo_arame  # o arame entra no custo da ferragem
        custo_mo = res['custo_mao_obra']
        custo_mat = custo_cimento + custo_areia + custo_pedra + custo_aco
        custo_total = custo_mat + custo_mo

        texto_res = (
            f"{txt('label_traco_curto')}: {self._rotulo_traco(res['traco'])}\n"
            f"{txt('label_volume')} ({self._txt_perda(res['perda_percentual'])}): {fmt_num(res['volume_com_perda_m3'], 3)} m³\n"
            f"{self._linhas_concreto(res, custo_cimento, custo_areia, custo_pedra)}"
        )
        if res['incluiu_ferragem']:
            texto_res += f"{txt('label_gaiola').format(m=fmt_num(res['altura_gaiola_m'], 2))}\n"
            texto_res += (
                f"• {txt('label_ferro')} {self._rotulo_bitola(res['bitola_mm'])}: "
                f"{fmt_num(res['kg_longitudinal'], 1)} kg ({fmt_int(res['barras_12m_longitudinal'])} {self._unidade(res['barras_12m_longitudinal'], 'un_barra12', 'un_barras12')})\n"
            )
            if res['incluiu_estribos']:
                texto_res += (
                    f"• {txt('label_estribos')} {self._rotulo_bitola(res['bitola_estribo_mm'])} "
                    f"{txt('label_estribo_cada')} {self._num_curto(res['espacamento_estribo_cm'])} cm: "
                    f"{fmt_num(res['kg_estribos'], 1)} kg ({fmt_int(res['barras_12m_estribos'])} {self._unidade(res['barras_12m_estribos'], 'un_barra12', 'un_barras12')})\n"
                )
            texto_res += f"• {txt('label_aco')}: {fmt_num(res['quilos_aco'], 1)} kg ({fmt_moeda(custo_aco - custo_arame)})\n"
            texto_res += f"• {txt('label_arame')}: {fmt_num(res['arame_kg'], 1)} kg ({fmt_moeda(custo_arame)})\n"
        if custo_mo > 0:
            texto_res += f"• {txt('label_mo')}: {fmt_num(res['total_metros_escavados'], 1)} m ({fmt_moeda(custo_mo)})\n"
        texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_total)}"

        resultado = {
            "etapa": txt("secao_brocas"),
            "tipo": "brocas",
            "inputs": {
                "qtd": qtd, "prof": prof, "diam": diam, "perda": perda, "barras": num_barras,
                "mo": preco_mo, "traco": res["traco"], "bitola": bitola, "esp_estribo": esp_estribo
            },
            "cimento": res['sacos_cimento'], "areia": res['areia_m3'], "pedra": res['pedra_m3'],
            "aco_kg": res['quilos_aco'], "barras_12m": res['barras_12m'],
            "arame_kg": res['arame_kg'] if res['incluiu_ferragem'] else 0.0,
            "custo_mat": custo_mat, "custo_mo": custo_mo, "custo_total": custo_total,
            "resumo_texto": texto_res
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_baldrame(self, e):
        if not (e.get("comp") or "").strip() or not (e.get("larg") or "").strip() or not (e.get("alt") or "").strip():
            return {"erro": txt("msg_erro_num")}

        comp = self._numero(e["comp"])
        larg = self._numero(e["larg"])
        alt = self._numero(e["alt"])
        perda = self._numero(e.get("perda"), PERDA_PADRAO_BALDRAME)
        t_barras = (e.get("barras") or "").strip()
        num_barras = int(t_barras) if t_barras else 0
        esp_estribo = self._numero(e.get("esp_estribo"), 0.0)
        preco_mo = self._numero(e.get("mo"), 0.0)
        bitola = self.bitola["baldrame"]
        imperm = self.imperm["baldrame"]

        # Viga menor que o mínimo do engenheiro (ex.: 0,2 digitado pensando em metros, mas o campo é em cm):
        # pergunta se quer continuar. Zero e negativo continuam com o erro do baldrame.py ("maiores que zero").
        # Os mínimos são em cm; nos EUA o aviso mostra em polegadas inteiras (8 in e 12 in), e a conta
        # compara com esse número (_limite_no_pais), senão 7 7/8 x 11 7/8 in passava sem aviso (rodada 3, P4).
        avisos = []
        larg_min = self._limite_no_pais(LARGURA_MINIMA_CM, "centimetro")
        alt_min = self._limite_no_pais(ALTURA_MINIMA_CM, "centimetro")
        if (0 < larg < larg_min) or (0 < alt < alt_min):
            avisos.append(txt("aviso_viga_min").format(
                larg=self._med_curto(larg, "centimetro"), alt=self._med_curto(alt, "centimetro"),
                larg_min=self._limite_cm(LARGURA_MINIMA_CM), alt_min=self._limite_cm(ALTURA_MINIMA_CM),
            ))
        pendentes = self._avisos_pendentes("baldrame", avisos)
        if pendentes:
            return pendentes

        res = calcular_baldrame(
            comprimento_m=comp, largura_cm=larg, altura_cm=alt,
            perda_percentual=perda, traco=self.traco["baldrame"],
            num_barras_longitudinais=num_barras, bitola_mm=bitola,
            espacamento_estribo_cm=esp_estribo, incluir_impermeabilizacao=imperm,
            sistema=sistema_unidades()
        )
        if "erro" in res:
            return {"erro": self._txt_erro(res['erro'])}

        custo_cimento = res['sacos_cimento'] * TABELA_PRECOS_GLOBAL.cimento_50kg
        custo_areia = res['areia_m3'] * TABELA_PRECOS_GLOBAL.areia_m3
        custo_pedra = res['pedra_m3'] * TABELA_PRECOS_GLOBAL.pedra_m3
        custo_aco = res['quilos_aco'] * TABELA_PRECOS_GLOBAL.aco_kg if res['incluiu_ferragem'] else 0.0
        custo_arame = res['arame_kg'] * PRECO_ARAME_KG if res['incluiu_ferragem'] else 0.0
        custo_aco += custo_arame  # o arame entra no custo da ferragem
        custo_mo = comp * preco_mo
        # Impermeabilizante: preço por litro, sobre os litros das embalagens compradas
        # (Brasil: 18 L e 3,6 L; EUA: balde de 5 gal com 4,75 gal e galão de 1 gal).
        # Litros exatos das embalagens: o 'litros_compra_imperm' vem arredondado (11,4 L em vez de
        # 11,356 L nos EUA, e 3 galões davam $ 25.33 em vez de $ 25.23; rodada 3, P5).
        sistema = sistema_unidades()
        preco_imperm = PRECO_IMPERM_LITRO_EUA if sistema == IMPERIAL else PRECO_IMPERM_LITRO
        balde_l, galao_l = EMBALAGENS_IMPERM_L[sistema]
        litros_compra = res['latas_imperm'] * balde_l + res['galoes_imperm'] * galao_l
        custo_imperm = litros_compra * preco_imperm if res['incluiu_impermeabilizacao'] else 0.0
        custo_mat = custo_cimento + custo_areia + custo_pedra + custo_aco + custo_imperm
        custo_total = custo_mat + custo_mo

        texto_res = (
            f"{txt('label_traco_curto')}: {self._rotulo_traco(res['traco'])}\n"
            f"{txt('label_volume')} ({self._txt_perda(perda)}): {fmt_num(res['volume_com_perda_m3'], 3)} m³\n"
            f"{self._linhas_concreto(res, custo_cimento, custo_areia, custo_pedra)}"
        )
        if res['incluiu_ferragem']:
            linha_ferro = (
                f"• {txt('label_ferro')} {self._rotulo_bitola(res['bitola_mm'])}: "
                f"{fmt_num(res['kg_longitudinal'], 1)} kg ({fmt_int(res['barras_12m_longitudinal'])} {self._unidade(res['barras_12m_longitudinal'], 'un_barra12', 'un_barras12')})"
            )
            if res['traspasse_m'] > 0:  # viga maior que 12 m: as barras têm emendas
                linha_ferro += f" ({txt('label_traspasse').format(m=fmt_num(res['traspasse_m'], 2))})"
            texto_res += linha_ferro + "\n"
            if res['incluiu_estribos']:
                texto_res += (
                    f"• {txt('label_estribos')} {self._rotulo_bitola(res['bitola_estribo_mm'])} "
                    # Espaçamento na unidade do país: "20 cm" no Brasil; "8 in" nos EUA (rodada 3, P6)
                    f"{txt('label_estribo_cada')} {self._med_curto(res['espacamento_estribo_cm'], 'centimetro')}: "
                    f"{fmt_num(res['kg_estribos'], 1)} kg ({fmt_int(res['barras_12m_estribos'])} {self._unidade(res['barras_12m_estribos'], 'un_barra12', 'un_barras12')})\n"
                )
            texto_res += f"• {txt('label_aco')}: {fmt_num(res['quilos_aco'], 1)} kg ({fmt_moeda(custo_aco - custo_arame)})\n"
            texto_res += f"• {txt('label_arame')}: {fmt_num(res['arame_kg'], 1)} kg ({fmt_moeda(custo_arame)})\n"
        if res['incluiu_impermeabilizacao']:
            texto_res += (
                f"• {txt('label_imperm_item')}: {self._med(res['area_imperm_m2'], 'area', 1)} · "
                f"{self._med(res['litros_imperm'], 'litro', 1)} = "
                f"{self._texto_latas_galoes(res['latas_imperm'], res['galoes_imperm'])} ({fmt_moeda(custo_imperm)})\n"
            )
        if custo_mo > 0:
            # Metros no Brasil, pés nos EUA: "12,2 m" / "40.0 ft" (rodada 3, P6)
            texto_res += f"• {txt('label_mo')}: {self._med(comp, 'comprimento', 1)} ({fmt_moeda(custo_mo)})\n"
        texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_total)}"

        resultado = {
            "etapa": txt("secao_baldrame"),
            "tipo": "baldrame",
            "cimento": res['sacos_cimento'], "areia": res['areia_m3'], "pedra": res['pedra_m3'],
            "aco_kg": res['quilos_aco'], "barras_12m": res['barras_12m'],
            "arame_kg": res['arame_kg'] if res['incluiu_ferragem'] else 0.0,
            "imperm_litros": res['litros_imperm'],
            "sistema": sistema_unidades(),  # país da conta (a lista de compras usa as embalagens dele)
            "custo_mat": custo_mat, "custo_mo": custo_mo, "custo_total": custo_total,
            "resumo_texto": texto_res,
            "inputs": {
                "comp": comp, "larg": larg, "alt": alt, "perda": perda, "mo": preco_mo,
                "traco": res["traco"], "barras": num_barras, "bitola": bitola,
                "esp_estribo": esp_estribo, "imperm": imperm
            }
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_reboco(self, e):
        if not (e.get("area") or "").strip() or not (e.get("esp") or "").strip():
            return {"erro": txt("msg_erro_num")}

        area = self._numero(e["area"])
        esp = self._numero(e["esp"])
        vaos = self._numero(e.get("vaos"), 0.0)
        perda = self._numero(e.get("perda"), PERDA_PADRAO_REBOCO)
        dois_lados = self.dois_lados["reboco"]
        chapisco = self.chapisco["reboco"]

        # Limites com aviso (reboco.py): passar deles pergunta se quer continuar
        avisos = []
        self._aviso_maximo(avisos, "aviso_area_max", area, AREA_MAXIMA_REBOCO_M2, "area")
        self._aviso_faixa(avisos, "aviso_espessura", esp, ESPESSURA_MINIMA_REBOCO_CM, ESPESSURA_MAXIMA_REBOCO_CM, "centimetro")
        pendentes = self._avisos_pendentes("reboco", avisos)
        if pendentes:
            return pendentes

        res = calcular_reboco(
            area_bruta_m2=area, espessura_cm=esp, desconto_vaos_m2=vaos,
            dois_lados=dois_lados, chapisco=chapisco, perda_percentual=perda,
            traco=self.traco["reboco"]
        )
        if "erro" in res:
            return {"erro": self._txt_erro(res['erro'])}

        custo_cimento = res['sacos_cimento'] * TABELA_PRECOS_GLOBAL.cimento_50kg
        custo_cal = res['sacos_cal'] * TABELA_PRECOS_GLOBAL.cal_20kg
        custo_areia = res['areia_m3'] * TABELA_PRECOS_GLOBAL.areia_m3
        custo_mat = custo_cimento + custo_cal + custo_areia

        texto_res = f"{txt('label_area_bruta')}: {fmt_num(res['area_bruta_m2'], 2)} m²\n"
        if res['desconto_vaos_m2'] > 0:
            texto_res += f"{txt('label_vaos')}: {fmt_num(res['desconto_vaos_m2'], 2)} m²\n"
            texto_res += f"{txt('label_area_liquida')}: {fmt_num(res['area_liquida_m2'], 2)} m²\n"
        if dois_lados:
            texto_res += f"{txt('label_area_rebocar')} ({txt('txt_dois_lados')}): {fmt_num(res['area_rebocada_m2'], 2)} m²\n"
        texto_res += (
            f"{txt('label_espessura_reboco')}: {self._med_curto(esp, 'centimetro')}\n"
            f"{txt('label_traco_curto')}: {self._rotulo_traco(res['traco'])}\n"
            f"{txt('label_volume_reboco')} ({self._txt_perda(perda)}): {fmt_num(res['volume_reboco_m3'], 3)} m³\n"
        )
        if chapisco:
            texto_res += f"{txt('label_chapisco_res')}: {txt('txt_chapisco_incluido')} ({CHAPISCO_TRACO_RODAPE}, {fmt_num(CHAPISCO_ESPESSURA_CM, 1)} cm)\n"
        texto_res += (
            f"{self._linhas_massa(res, custo_cimento, custo_cal, custo_areia)}"
            f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"
        )

        resultado = {
            "etapa": txt("secao_reboco"),
            "tipo": "reboco",
            "cimento": res['sacos_cimento'], "cal": res['sacos_cal'], "areia": res['areia_m3'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {
                "area": area, "vaos": vaos, "esp": esp, "perda": perda,
                "traco": res["traco"], "dois_lados": dois_lados, "chapisco": chapisco
            }
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_ceramica(self, aba, e):
        piso = (aba == "piso")
        if not all((e.get(k) or "").strip() for k in ("area", "larg", "alt")):
            return {"erro": txt("msg_erro_num")}

        area = self._numero(e["area"])
        larg = self._numero(e["larg"])
        alt = self._numero(e["alt"])
        caixa = self._numero(e.get("caixa"), 0.0)
        perda_txt = (e.get("perda") or "").strip()
        perda_digitada = self._numero(perda_txt) if perda_txt else None  # vazio = automática
        desenho = self.desenho[aba]
        tipo_arg = self.argamassa[aba]
        vaos = 0.0 if piso else self._numero(e.get("vaos"), 0.0)
        rodape = self._numero(e.get("rodape"), 0.0) if piso else 0.0
        rodape_peca = self._numero(e.get("rodape_peca"), 0.0) if piso else 0.0

        # Limites com aviso (revestimento.py), iguais no Piso e no Azulejo
        avisos = []
        self._aviso_maximo(avisos, "aviso_area_max", area, AREA_MAXIMA_REVESTIMENTO_M2, "area")
        if any(self._fora_da_faixa(lado, PECA_MINIMA_CM, PECA_MAXIMA_CM, "centimetro") for lado in (larg, alt)):
            avisos.append(txt("aviso_peca").format(
                larg=self._med_curto(larg, "centimetro"), alt=self._med_curto(alt, "centimetro"),
                min=self._med_limite(PECA_MINIMA_CM, "centimetro"), max=self._med_limite(PECA_MAXIMA_CM, "centimetro")))
        pendentes = self._avisos_pendentes(aba, avisos)
        if pendentes:
            return pendentes

        sistema = sistema_unidades()
        eua = (sistema == IMPERIAL)
        if piso:
            res = calcular_piso(area, larg, alt, caixa, tipo_arg, perda_digitada, rodape, desenho, rodape_peca, sistema)
        else:
            res = calcular_azulejo(area, larg, alt, vaos, caixa, tipo_arg, perda_digitada, desenho, sistema)
        if "erro" in res:
            return {"erro": self._txt_erro(res['erro'])}
        perda = res['perda_percentual']

        # Áreas e rodapé mostrados: no Brasil, os do cálculo (já arredondados, igual a antes);
        # nos EUA, sem o arredondamento em m² (senão 430 sq ft aparece como 430.02 sq ft)
        if eua:
            fator_rodape = 1 + ((10.0 if res['perda_automatica'] else perda) / 100.0)
            mostra = {"bruta": area, "vaos": vaos, "liquida": area - vaos,
                      "com_perda": (area - vaos) * (1 + perda / 100.0), "rodape": rodape * fator_rodape}
        else:
            mostra = {"bruta": res['area_bruta_m2'], "vaos": res['desconto_vaos_m2'], "liquida": res['area_liquida_m2'],
                      "com_perda": res['area_com_perda_m2'], "rodape": res['rodape_m']}

        # Custo das peças e do rodapé: pela área com perda e pelo rodapé MOSTRADOS (no Brasil, os mesmos
        # de antes; nos EUA, sem o arredondamento em m², senão 473 sq ft dava $ 2,197.00 em vez de $ 2,197.16)
        preco_m2 = PRECO_PISO_M2 if piso else PRECO_AZULEJO_M2
        custo_pecas = mostra['com_perda'] * preco_m2
        preco_saco = PRECO_ARGAMASSA_SACO_EUA if eua else PRECO_ARGAMASSA_SACO
        custo_arg = res['sacos_argamassa'] * preco_saco[tipo_arg]
        custo_rodape = mostra['rodape'] * PRECO_RODAPE_M
        custo_mat = custo_pecas + custo_arg + custo_rodape
        texto_res = f"{txt('label_area')}: {self._med(mostra['bruta'], 'area')}\n"
        if res['desconto_vaos_m2'] > 0:
            texto_res += f"{txt('label_vaos')}: {self._med(mostra['vaos'], 'area')}\n"
            texto_res += f"{txt('label_area_liquida')}: {self._med(mostra['liquida'], 'area')}\n"
        origem_perda = f", {txt('label_perda_auto')}" if res['perda_automatica'] else ""
        texto_peca = self._texto_peca(larg, alt, sistema)  # "60x60 cm" ou "12 x 12 in"
        texto_res += (
            f"{txt('label_area_perda')} ({self._num_curto(perda)}%{origem_perda}): {self._med(mostra['com_perda'], 'area')}\n"
            f"{txt('label_peca')}: {texto_peca}\n"
        )
        if desenho:  # só aparece quando é com desenho (o normal não precisa dizer)
            texto_res += f"{txt('label_assent')}: {txt('txt_com_desenho')}\n"
        custo_txt = f" ({fmt_moeda(custo_pecas)})"
        if res['caixas'] > 0:
            # Por caixa: m² no Brasil, sq ft nos EUA (o número que a pessoa digitou)
            por_caixa = fmt_num(do_metrico(caixa, "area", sistema), 2)
            texto_res += f"• {txt('label_pecas')}: {fmt_int(res['pecas'])}\n"
            # "Caixas: 21 (2,16 m² por caixa)": sem repetir "caixas" depois do número (pendência 12 da rodada 2)
            texto_res += f"• {txt('label_caixas')}: {fmt_int(res['caixas'])} ({por_caixa} {txt('un_caixa_m2')}){custo_txt}\n"
        else:
            texto_res += f"• {txt('label_pecas')}: {fmt_int(res['pecas'])}{custo_txt}\n"
        if eua:
            # Ex.: "Argamassa colante (thinset) Modificada (ANSI A118.4): 3 sacos de 50 lb (150 lb)"
            qtd = res['sacos_argamassa']
            texto_res += (
                f"• {txt('label_argamassa_res')} {self._rotulo_argamassa(tipo_arg)}: "
                f"{fmt_int(qtd)} {txt('un_saco_argamassa') if qtd == 1 else txt('un_sacos_argamassa')} "
                f"({self._med(res['argamassa_kg'], 'peso', 1)}) ({fmt_moeda(custo_arg)})\n"
                f"  {txt('label_desempenadeira')}: {res['desempenadeira']} in · "
                f"{txt('label_consumo')}: {self._med(res['consumo_argamassa_kg_m2'], 'consumo', 3)}\n"
            )
        else:
            texto_res += (
                f"• {txt('label_argamassa_res')} {tipo_arg}: {fmt_int(res['sacos_argamassa'])} {self._unidade(res['sacos_argamassa'], 'un_saco_cal', 'un_sacos_cal')} "
                f"({fmt_num(res['argamassa_kg'], 1)} kg) ({fmt_moeda(custo_arg)})\n"
            )
        if res['rodape_m'] > 0:
            linha_rodape = f"• {txt('label_rodape')}: {self._med(mostra['rodape'], 'comprimento')}"
            if res['rodape_pecas'] > 0:  # só quando o cliente informa o tamanho da peça
                linha_rodape += f" ({fmt_int(res['rodape_pecas'])} {self._unidade(res['rodape_pecas'], 'un_peca', 'un_pecas')} {txt('un_de')} {self._med(res['rodape_peca_m'], 'comprimento')})"
            texto_res += f"{linha_rodape} ({fmt_moeda(custo_rodape)})\n"
        texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"

        resultado = {
            "etapa": txt("secao_" + aba),
            "tipo": aba,
            "sistema": sistema,  # país da conta (a lista de compras usa as embalagens dele)
            "argamassa_sacos": res['sacos_argamassa'],
            "pecas": res['pecas'], "caixas": res['caixas'], "rodape_m": res['rodape_m'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {
                "area": area, "larg": larg, "alt": alt, "caixa": caixa,
                "perda": perda_digitada if perda_digitada is not None else "",  # vazio = automática
                "argamassa": tipo_arg, "vaos": vaos, "rodape": rodape,
                "rodape_peca": rodape_peca if rodape_peca > 0 else "", "desenho": desenho
            }
        }
        return {"texto": texto_res, "resultado": resultado}

    @staticmethod
    def _texto_latas(latas_1kg, latas_2kg, sistema=None):
        """Ex.: '2 latas de 2 kg e 1 lata de 1 kg' (latinhas de rejunte do Brasil)."""
        t = lambda chave: txt_do_pais(chave, sistema)
        partes = []
        if latas_2kg:
            partes.append(f"{fmt_int(latas_2kg)} {t('un_lata_2kg') if latas_2kg == 1 else t('un_latas_2kg')}")
        if latas_1kg:
            partes.append(f"{fmt_int(latas_1kg)} {t('un_lata_1kg') if latas_1kg == 1 else t('un_latas_1kg')}")
        return f" {t('un_e')} ".join(partes)

    @staticmethod
    def _texto_rejunte(tipo, grandes, pequenas, sistema=None):
        """Embalagens de rejunte por tipo. Brasil ("lata"): '2 latas de 2 kg e 1 lata de 1 kg'.
        EUA: '2 sacos de 25 lb e 1 caixa de 7 lb' (com areia) ou '3 caixas de 10 lb' (sem areia)."""
        if tipo == "lata":
            return CalculatorScreen._texto_latas(pequenas, grandes, sistema)
        t = lambda chave: txt_do_pais(chave, sistema)
        partes = []
        if grandes:
            partes.append(f"{fmt_int(grandes)} {t('un_grande_' + tipo) if grandes == 1 else t('un_grandes_' + tipo)}")
        if pequenas:
            partes.append(f"{fmt_int(pequenas)} {t('un_pequena_' + tipo) if pequenas == 1 else t('un_pequenas_' + tipo)}")
        return f" {t('un_e')} ".join(partes)

    def _calcular_rejunte(self, e):
        if not all((e.get(k) or "").strip() for k in ("area", "larg", "alt", "junta")):
            return {"erro": txt("msg_erro_num")}

        area = self._numero(e["area"])
        larg = self._numero(e["larg"])
        alt = self._numero(e["alt"])
        junta = self._numero(e["junta"])
        # Espessura apagada: usa o mesmo número que o campo mostra (8 mm no Brasil; 5/16 in nos EUA,
        # e não 8 mm = 0.315 in). O _limite_no_pais faz essa volta: número mostrado -> métrico.
        esp = self._numero(e.get("esp"), self._limite_no_pais(ESPESSURA_PADRAO_MM, "milimetro"))
        perda = self._numero(e.get("perda"), PERDA_PADRAO_REJUNTE)

        # Limites com aviso (rejunte.py). Junta de 30 mm é quase certeza de quem digitou em cm errado.
        avisos = []
        self._aviso_maximo(avisos, "aviso_area_max", area, AREA_MAXIMA_REJUNTE_M2, "area")
        self._aviso_faixa(avisos, "aviso_junta", junta, JUNTA_MINIMA_MM, JUNTA_MAXIMA_MM, "milimetro")
        pendentes = self._avisos_pendentes("rejunte", avisos)
        if pendentes:
            return pendentes

        sistema = sistema_unidades()
        res = calcular_rejunte(area, larg, alt, junta, esp, perda, sistema)
        if "erro" in res:
            return {"erro": self._txt_erro(res['erro'])}

        tipo_rej = res['tipo_rejunte']  # "lata" (Brasil), "com_areia" ou "sem_areia" (EUA)
        if tipo_rej == "lata":
            custo_mat = res['latas_1kg'] * PRECO_LATA_1KG + res['latas_2kg'] * PRECO_LATA_2KG
        else:
            preco_grande, preco_pequena = PRECO_REJUNTE_EUA[tipo_rej]
            custo_mat = res['embalagens_grandes'] * preco_grande + res['embalagens_pequenas'] * preco_pequena

        def n(v):
            return fmt_num(v, 0 if float(v).is_integer() else 1)

        if tipo_rej == "lata":  # Brasil: igual a antes
            texto_dados = (
                f"{txt('label_area')}: {fmt_num(res['area_m2'], 2)} m²\n"
                f"{txt('label_peca')}: {n(larg)}x{n(alt)} cm\n"
                f"{txt('label_junta')}: {n(junta)} mm\n"
                f"{txt('label_espessura')}: {n(esp)} mm\n"
                f"{txt('label_consumo')}: {fmt_num(res['consumo_kg_m2'], 3)} kg/m²\n"
            )
            linha_kg = f"• {txt('label_rejunte_res')} ({self._txt_perda(perda)}): {fmt_num(res['kg_total'], 1)} kg"
        else:   # EUA: sq ft, in, lb
            texto_dados = (
                f"{txt('label_area')}: {self._med(area, 'area')}\n"
                f"{txt('label_peca')}: {self._texto_peca(larg, alt, sistema)}\n"
                f"{txt('label_junta')}: {self._med(junta, 'milimetro')}\n"
                f"{txt('label_espessura')}: {self._med(esp, 'milimetro')}\n"
                f"{txt('label_consumo')}: {self._med(res['consumo_kg_m2'], 'consumo', 3)}\n"
            )
            linha_kg = f"• {txt('label_rejunte_' + tipo_rej)} ({self._txt_perda(perda)}): {self._med(res['kg_total'], 'peso', 1)}"
        # Uma linha só, igual à Pintura: "• Rejunte (com 10% de perda): 5,6 kg = 3 latas de 2 kg (R$ 54,00)"
        texto_res = (
            texto_dados
            + f"{linha_kg} = {self._texto_rejunte(tipo_rej, res['embalagens_grandes'], res['embalagens_pequenas'])} ({fmt_moeda(custo_mat)})\n"
            + f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"
        )

        resultado = {
            "etapa": txt("secao_rejunte"),
            "tipo": "rejunte",
            "sistema": sistema,  # país da conta (a lista de compras usa as embalagens dele)
            "rejunte_kg": res['kg_total'],
            "rejunte_latas_1kg": res['latas_1kg'],
            "rejunte_latas_2kg": res['latas_2kg'],
            "rejunte_tipo": tipo_rej,
            "rejunte_grandes": res['embalagens_grandes'],
            "rejunte_pequenas": res['embalagens_pequenas'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {"area": area, "larg": larg, "alt": alt, "junta": junta, "esp": esp, "perda": perda}
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_laje(self, e):
        premoldada = (self.laje_tipo == "premoldada")
        obrigatorios = ("area",) if premoldada else ("area", "esp")
        if not all((e.get(k) or "").strip() for k in obrigatorios):
            return {"erro": txt("msg_erro_num")}

        area = self._numero(e["area"])
        capa = self._numero(e.get("capa"), CAPA_PADRAO_CM)
        esp = self._numero(e.get("esp"), 0.0)
        perda = self._numero(e.get("perda"), PERDA_PADRAO_LAJE)

        # Limites com aviso (laje.py): a capa só vale na pré-moldada; a espessura, só na maciça
        avisos = []
        self._aviso_maximo(avisos, "aviso_area_max", area, AREA_MAXIMA_LAJE_M2, "area")
        if premoldada:
            self._aviso_faixa(avisos, "aviso_capa", capa, CAPA_MINIMA_CM, CAPA_MAXIMA_CM, "centimetro")
        else:
            self._aviso_faixa(avisos, "aviso_espessura", esp, ESPESSURA_MACICA_MINIMA_CM, ESPESSURA_MACICA_MAXIMA_CM, "centimetro")
        pendentes = self._avisos_pendentes("laje", avisos)
        if pendentes:
            return pendentes

        res = calcular_laje(area, self.laje_tipo, self.laje_enchimento, capa, esp, perda, self.traco["laje"],
                            tela_soldada=self.tela["laje"])
        if "erro" in res:
            return {"erro": self._txt_erro(res['erro'])}

        custo_cimento = res['sacos_cimento'] * TABELA_PRECOS_GLOBAL.cimento_50kg
        custo_areia = res['areia_m3'] * TABELA_PRECOS_GLOBAL.areia_m3
        custo_pedra = res['pedra_m3'] * TABELA_PRECOS_GLOBAL.pedra_m3
        custo_laje_pm = res['laje_premoldada_m2'] * PRECO_LAJE_PREMOLDADA_M2.get(res['enchimento'], 0.0)
        custo_tela = res['tela_paineis'] * PRECO_PAINEL_TELA
        custo_mat = custo_cimento + custo_areia + custo_pedra + custo_laje_pm + custo_tela

        def n(v):
            return fmt_num(v, 0 if float(v).is_integer() else 1)

        texto_res = (
            f"{txt('label_area')}: {fmt_num(res['area_m2'], 2)} m²\n"
            f"{txt('label_tipo_laje')}: {self._rotulo_laje(res['tipo'])}\n"
        )
        if premoldada:
            texto_res += (
                f"{txt('label_enchimento').replace(' (Opcional)', '').replace(' (Optional)', '')}: {self._rotulo_laje(res['enchimento'])}\n"
                f"{txt('label_capa')}: {n(res['capa_cm'])} cm\n"
            )
        else:
            texto_res += f"{txt('label_espessura_laje')}: {n(res['espessura_cm'])} cm\n"
        texto_res += (
            f"{txt('label_traco_curto')}: {self._rotulo_traco(res['traco'])}\n"
            f"{txt('label_volume')} ({self._txt_perda(perda)}): {fmt_num(res['volume_com_perda_m3'], 3)} m³\n"
        )
        if premoldada:
            texto_res += f"• {txt('label_laje_pm')}: {fmt_num(res['laje_premoldada_m2'], 2)} m² ({fmt_moeda(custo_laje_pm)})\n"
            if res['lajotas'] > 0:
                texto_res += f"  ({txt('label_lajotas')}: {fmt_int(res['lajotas'])} {self._unidade(res['lajotas'], 'un_unidade', 'un_unidades')})\n"
            if res['incluiu_tela']:
                qtd = res['tela_paineis']
                texto_res += (
                    f"• {txt('label_tela_res')}: {fmt_num(res['tela_m2'], 2)} m² = "
                    f"{fmt_int(qtd)} {txt('un_painel_tela') if qtd == 1 else txt('un_paineis_tela')} ({fmt_moeda(custo_tela)})\n"
                )
        texto_res += (
            f"{self._linhas_concreto(res, custo_cimento, custo_areia, custo_pedra)}"
            f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"
        )

        resultado = {
            "etapa": txt("secao_laje"),
            "tipo": "laje",
            "cimento": res['sacos_cimento'], "areia": res['areia_m3'], "pedra": res['pedra_m3'],
            "laje_premoldada_m2": res['laje_premoldada_m2'], "lajotas": res['lajotas'],
            "tela_paineis": res['tela_paineis'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {
                "area": area, "capa": capa, "esp": esp if esp > 0 else "", "perda": perda, "traco": res["traco"],
                "tipo_laje": res["tipo"], "enchimento": self.laje_enchimento, "tela": self.tela["laje"]
            }
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_telhado(self, e):
        if not (e.get("area") or "").strip():
            return {"erro": txt("msg_erro_num")}

        tipo = self.telha_tipo
        area = self._numero(e["area"])
        incl = self._numero(e.get("incl"), INCLINACAO_PADRAO[tipo])
        cumeeira = self._numero(e.get("cumeeira"), 0.0)
        perda = self._numero(e.get("perda"), PERDA_PADRAO_TELHADO)
        madeira = self.madeiramento["telhado"]

        # Limites com aviso (telhado.py)
        avisos = []
        self._aviso_maximo(avisos, "aviso_area_max", area, AREA_MAXIMA_TELHADO_M2, "area")
        self._aviso_maximo(avisos, "aviso_inclinacao_max", incl, INCLINACAO_MAXIMA_PERCENTUAL)
        pendentes = self._avisos_pendentes("telhado", avisos)
        if pendentes:
            return pendentes

        res = calcular_telhado(area, tipo, incl, cumeeira, madeira, perda)
        if "erro" in res:
            return {"erro": self._txt_erro(res['erro'])}

        custo_telhas = res['telhas'] * PRECO_TELHA[tipo]
        custo_cumeeira = res['cumeeiras'] * PRECO_CUMEEIRA[tipo]
        custo_ripas = res['ripas_m'] * PRECO_MADEIRA_M["ripas"]
        custo_caibros = res['caibros_m'] * PRECO_MADEIRA_M["caibros"]
        custo_tercas = res['tercas_m'] * PRECO_MADEIRA_M["tercas"]
        custo_madeira = custo_ripas + custo_caibros + custo_tercas
        custo_mat = custo_telhas + custo_cumeeira + custo_madeira

        def n(v):
            return fmt_num(v, 0 if float(v).is_integer() else 1)

        texto_res = (
            f"{txt('label_area_planta')}: {fmt_num(res['area_planta_m2'], 2)} m²\n"
            f"{txt('label_inclinacao')}: {n(res['inclinacao_percentual'])}%\n"
            f"{txt('label_area_real')}: {fmt_num(res['area_real_m2'], 2)} m²\n"
            f"{txt('label_tipo_telha')}: {self._rotulo_telha(tipo)}\n"
            f"• {txt('label_telhas')} ({self._txt_perda(perda)}): "
            f"{fmt_int(res['telhas'])} {self._unidade(res['telhas'], 'un_unidade', 'un_unidades')} ({fmt_moeda(custo_telhas)})\n"
        )
        if res['cumeeiras'] > 0:
            texto_res += (
                f"• {txt('label_cumeeira')}: {fmt_num(res['cumeeira_m'], 2)} m = "
                f"{fmt_int(res['cumeeiras'])} {self._unidade(res['cumeeiras'], 'un_peca', 'un_pecas')} ({fmt_moeda(custo_cumeeira)})\n"
            )
        if res['incluiu_madeiramento']:
            texto_res += f"• {txt('label_madeiramento_res')}:\n"
            for chave, custo in (("ripas", custo_ripas), ("caibros", custo_caibros), ("tercas", custo_tercas)):
                if res[f"{chave}_m"] > 0:
                    texto_res += f"   - {txt('label_' + chave)}: {fmt_num(res[chave + '_m'], 1)} m ({fmt_moeda(custo)})\n"
        texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"

        resultado = {
            "etapa": txt("secao_telhado"),
            "tipo": "telhado",
            "telhas": res['telhas'], "tipo_telha": tipo, "cumeeiras": res['cumeeiras'],
            "ripas_m": res['ripas_m'], "caibros_m": res['caibros_m'], "tercas_m": res['tercas_m'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {
                "area": area, "incl": incl, "cumeeira": cumeeira if cumeeira > 0 else "", "perda": perda,
                "tipo_telha": tipo, "madeiramento": madeira
            }
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_esquadrias(self, e):
        # Digitou no formulário mas não adicionou: avisa (se começou, tem que terminar)
        if any((e.get(chave) or "").strip() for chave in CAMPOS_ABA["esquadrias"]):
            return {"erro": txt("msg_esquadria_pendente")}
        if not self.esquadrias_itens:
            return {"erro": txt("msg_lista_vazia")}

        fix = self.esq_fixacao
        res = calcular_esquadrias(self.esquadrias_itens, fix["espuma"], fix["parafusos"], fix["argamassa"])
        if "erro" in res:
            return {"erro": self._txt_erro(res['erro'])}

        custo_espuma = res['tubos_espuma'] * PRECO_TUBO_ESPUMA
        custo_parafusos = res['parafusos'] * PRECO_PARAFUSO
        custo_argamassa = res['sacos_argamassa'] * PRECO_SACO_ARGAMASSA_FIXACAO
        custo_mat = custo_espuma + custo_parafusos + custo_argamassa

        texto_res = ""
        for tipo, rotulo in (("porta", "label_portas"), ("janela", "label_janelas")):
            itens_tipo = [i for i in self.esquadrias_itens if i["tipo"] == tipo]
            if not itens_tipo:
                continue
            texto_res += f"{txt(rotulo)}:\n"
            for item in itens_tipo:
                area = (item["larg"] / 100.0) * (item["alt"] / 100.0)
                texto_res += f"• {self._texto_item_esquadria(item)}: {fmt_num(area, 2)} m² {txt('label_cada')}\n"
            texto_res += "\n"
        texto_res += (
            f"{txt('label_total')}: {self._texto_total_esquadrias(res['portas'], res['janelas'])}\n"
            f"{txt('label_area_vaos')}: {fmt_num(res['area_vaos_m2'], 2)} m²\n"
        )
        if res['tubos_espuma'] or res['parafusos'] or res['sacos_argamassa']:
            texto_res += f"\n{txt('secao_fixacao')}:\n"
        if res['tubos_espuma'] > 0:
            qtd = res['tubos_espuma']
            texto_res += f"• {txt('label_res_espuma')}: {fmt_int(qtd)} {txt('un_tubo_500') if qtd == 1 else txt('un_tubos_500')} ({fmt_moeda(custo_espuma)})\n"
        if res['parafusos'] > 0:
            texto_res += f"• {txt('label_res_parafusos')}: {fmt_int(res['parafusos'])} {self._unidade(res['parafusos'], 'un_unidade', 'un_unidades')} ({fmt_moeda(custo_parafusos)})\n"
        if res['sacos_argamassa'] > 0:
            qtd = res['sacos_argamassa']
            texto_res += (
                f"• {txt('label_res_argamassa_fix')}: {fmt_num(res['argamassa_kg'], 1)} kg = "
                f"{fmt_int(qtd)} {txt('un_saco_20') if qtd == 1 else txt('un_sacos_20')} ({fmt_moeda(custo_argamassa)})\n"
            )
        # O app não tem preço de porta e janela (varia muito): o custo é só o dos insumos de fixação.
        # Sem insumo, em vez de "R$ 0,00" (parece que as portas são de graça), só a frase.
        # Com custo, uma linha em branco separa o custo da frase (pendência 17 da rodada 2)
        if custo_mat > 0:
            texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}\n"
        texto_res += f"\n{txt('txt_esquadrias_orcamento')}"

        resultado = {
            "etapa": txt("secao_esquadrias"),
            "tipo": "esquadrias",
            "esquadrias": [dict(i) for i in self.esquadrias_itens],
            "tubos_espuma": res['tubos_espuma'], "parafusos": res['parafusos'],
            "sacos_argamassa_fix": res['sacos_argamassa'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {"itens": [dict(i) for i in self.esquadrias_itens], **fix},
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_pintura(self, e):
        parede_txt = (e.get("parede") or "").strip()
        teto_txt = (e.get("teto") or "").strip()
        demaos_txt = (e.get("demaos") or "").strip()
        if not (parede_txt or teto_txt) or not demaos_txt:
            return {"erro": txt("msg_erro_num")}

        parede = self._numero(parede_txt, 0.0)
        teto = self._numero(teto_txt, 0.0)
        demaos = int(demaos_txt)
        sistema = sistema_unidades()
        eua = (sistema == IMPERIAL)
        # Rendimento vazio: o padrão do país (12 m²/L no Brasil; 400 sq ft/gal nos EUA)
        rend = self._numero(e.get("rend"), rendimento_padrao_m2_l(sistema))
        # Limites com aviso (pintura.py). Demãos acima de 5 (ex.: "22" no lugar de "2") eram erro;
        # agora abrem a janela com Continuar, igual às outras abas (regra 12).
        # Rendimento: 4 a 20 m²/L no Brasil; 150 a 800 sq ft/gal nos EUA (rodada 3, P8)
        rend_min, rend_max = limites_rendimento_m2_l(sistema)
        avisos = []
        self._aviso_maximo(avisos, "aviso_area_parede_max", parede, AREA_MAXIMA_PINTURA_M2, "area")
        self._aviso_maximo(avisos, "aviso_area_teto_max", teto, AREA_MAXIMA_PINTURA_M2, "area")
        self._aviso_maximo(avisos, "aviso_demaos_max", demaos, DEMAOS_MAXIMO)
        self._aviso_faixa(avisos, "aviso_rendimento", rend, rend_min, rend_max, "rendimento")
        pendentes = self._avisos_pendentes("pintura", avisos)
        if pendentes:
            return pendentes
        perda = self._numero(e.get("perda"), PERDA_PADRAO_PINTURA)
        # Nos EUA não existem selador nem massa (a tela nem mostra; aqui garante que não entram)
        selador = False if eua else self.selador["pintura"]
        fundo = self.fundo["pintura"]
        massa = "nenhuma" if eua else self.massa_tipo

        res = calcular_pintura(parede, teto, demaos, rend, perda, selador, massa, fundo, sistema)
        if "erro" in res:
            return {"erro": self._txt_erro(res['erro'])}

        tabela_precos = PRECO_TINTA_EUA if eua else PRECO_TINTA
        custos = {
            item: d['latas'] * tabela_precos[item]["lata"] + d['galoes'] * tabela_precos[item]["galao"]
            for item, d in res['itens'].items()
        }
        custo_massa = res['baldes_massa'] * PRECO_BALDE_MASSA.get(massa, 0.0)
        custo_mat = sum(custos.values()) + custo_massa

        def n(v):
            return fmt_num(v, 0 if float(v).is_integer() else 1)

        texto_res = ""
        # Nos EUA mostra a área digitada, sem o arredondamento em m² (1000 sq ft, e não 999.97)
        if res['area_parede_m2'] > 0:
            texto_res += f"{txt('label_area_parede_pint')}: {self._med(parede if eua else res['area_parede_m2'], 'area')}\n"
        if res['area_teto_m2'] > 0:
            texto_res += f"{txt('label_area_teto_pint')}: {self._med(teto if eua else res['area_teto_m2'], 'area')}\n"
        if eua:  # ex.: 400 sq ft/gal (o número que a pessoa digitou)
            texto_rend = f"{n(round(do_metrico(rend, 'rendimento', sistema), 1))} sq ft/gal"
        else:
            texto_rend = f"{n(rend)} m²/L"
        texto_res += (
            f"{txt('label_demaos')}: {demaos}\n"
            f"{txt('label_rendimento')}: {texto_rend}\n"
        )
        perda_txt = self._txt_perda(perda)
        for item, d in res['itens'].items():
            texto_res += (
                f"• {txt('label_pint_' + item)} ({perda_txt}): {self._med(d['litros'], 'litro', 1)} = "
                f"{self._texto_latas_galoes(d['latas'], d['galoes'])} ({fmt_moeda(custos[item])})\n"
            )
        if res['baldes_massa'] > 0:
            qtd = res['baldes_massa']
            texto_res += (
                f"• {self._rotulo_massa(massa)} ({perda_txt}): {fmt_num(res['massa_kg'], 1)} kg = "
                f"{fmt_int(qtd)} {txt('un_balde_25') if qtd == 1 else txt('un_baldes_25')} ({fmt_moeda(custo_massa)})\n"
            )
        # "Demãos" e "Rendimento" do topo valem só para as tintas: os complementos têm demãos próprias,
        # sobre a área total (parede + teto). Só aparece se tiver algum complemento.
        complementos = []
        for item in ("selador", "fundo"):
            if item in res['itens']:
                complementos.append(f"{txt('label_pint_' + item)} {txt('txt_1_demao')}")
        if res['baldes_massa'] > 0:
            complementos.append(f"{self._rotulo_massa(massa)} {txt('txt_n_demaos').format(n=DEMAOS_MASSA)}")
        if complementos:
            texto_res += f"{txt('label_nota_complementos')}: {', '.join(complementos)}\n"
        texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"

        resultado = {
            "etapa": txt("secao_pintura"),
            "tipo": "pintura",
            "sistema": sistema,  # país da conta (a lista de compras usa as embalagens dele)
            "pintura": {item: [d['latas'], d['galoes']] for item, d in res['itens'].items()},
            "massa_tipo": massa, "baldes_massa": res['baldes_massa'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {
                "parede": parede if parede > 0 else "", "teto": teto if teto > 0 else "",
                "demaos": demaos, "rend": rend, "perda": perda,
                "selador": selador, "fundo": fundo, "massa": massa,
            }
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_hidraulica(self, e):
        def inteiro(chave):
            texto = (e.get(chave) or "").strip()
            return int(texto) if texto else 0

        pontos = {chave: inteiro(chave) for chave in ("fria", "quente", "esgoto")}
        tubos_projeto = {}
        for tubo in TUBOS:
            texto = (e.get(f"tubo_{tubo}") or "").strip()
            if texto:  # vazio = o app estima
                tubos_projeto[tubo] = self._numero(texto)
        perda = self._numero(e.get("perda"), PERDA_PADRAO_HIDRAULICA)

        # Limites com aviso (hidraulica.py): o mesmo para cada tipo de ponto
        avisos = []
        for chave in ("fria", "quente", "esgoto"):
            self._aviso_maximo(avisos, f"aviso_{chave}_max", pontos[chave], PONTOS_MAXIMO)
        pendentes = self._avisos_pendentes("hidraulica", avisos)
        if pendentes:
            return pendentes

        res = calcular_hidraulica(pontos["fria"], pontos["quente"], pontos["esgoto"], tubos_projeto, perda)
        if "erro" in res:
            return {"erro": self._txt_erro(res['erro'])}

        custo_tubos = {t: d['barras'] * PRECO_BARRA_TUBO[t] for t, d in res['tubos'].items()}
        custo_conexoes = {t: q * PRECO_CONEXAO[t] for t, q in res['conexoes'].items()}
        custo_registros = res['registros'] * PRECO_REGISTRO
        custo_mat = sum(custo_tubos.values()) + sum(custo_conexoes.values()) + custo_registros

        texto_res = ""
        for chave in ("fria", "quente", "esgoto"):
            if pontos[chave] > 0:  # ponto com zero não aparece
                texto_res += f"{txt('label_pontos_' + chave)}: {fmt_int(pontos[chave])}\n"
        for tubo, dados in res['tubos'].items():
            origem = txt("label_do_projeto") if dados['do_projeto'] else txt("label_estimado")
            texto_res += (
                f"• {txt('label_tubo_' + tubo)} ({origem}, {self._txt_perda(perda)}): {fmt_num(dados['metros'], 1)} m = "
                f"{self._texto_barras(dados['barras'], BARRA_TUBO_M[tubo])} ({fmt_moeda(custo_tubos[tubo])})\n"
            )
        for tipo, qtd in res['conexoes'].items():
            texto_res += f"• {txt('label_conexoes_' + tipo)}: {fmt_int(qtd)} {self._unidade(qtd, 'un_unidade', 'un_unidades')} ({fmt_moeda(custo_conexoes[tipo])})\n"
        if res['registros'] > 0:
            texto_res += f"• {txt('label_registros')}: {fmt_int(res['registros'])} {self._unidade(res['registros'], 'un_unidade', 'un_unidades')} ({fmt_moeda(custo_registros)})\n"
        texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"

        inputs = {chave: (qtd if qtd else "") for chave, qtd in pontos.items()}
        for tubo in TUBOS:
            inputs[f"tubo_{tubo}"] = tubos_projeto.get(tubo, "")
        inputs["perda"] = perda

        resultado = {
            "etapa": txt("secao_hidraulica"),
            "tipo": "hidraulica",
            "tubos": {t: d['barras'] for t, d in res['tubos'].items()},
            "conexoes": res['conexoes'],
            "registros": res['registros'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": inputs,
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_eletrica(self, e):
        def inteiro(chave):
            texto = (e.get(chave) or "").strip()
            return int(texto) if texto else 0

        def metros(chave):
            texto = (e.get(chave) or "").strip()
            return self._numero(texto) if texto else None  # vazio = o app estima

        tomadas = inteiro("tomadas")
        interruptores = inteiro("interruptores")
        luzes = inteiro("luzes")
        chuveiros = inteiro("chuveiros")      # acima de 5.500 W (fio 6 mm²)
        chuveiros4 = inteiro("chuveiros4")    # até 5.500 W (fio 4 mm²)
        conduite = metros("conduite")
        fios_projeto = {}
        for bitola in BITOLAS_FIO:
            valor = metros(self._chave_fio(bitola))
            if valor is not None:
                fios_projeto[bitola] = valor
        perda = self._numero(e.get("perda"), PERDA_PADRAO_ELETRICA)

        # Limites com aviso (eletrica.py). Os chuveiros contam somando os dois campos.
        avisos = []
        self._aviso_maximo(avisos, "aviso_tomadas_max", tomadas, TOMADAS_MAXIMO)
        self._aviso_maximo(avisos, "aviso_interruptores_max", interruptores, INTERRUPTORES_MAXIMO)
        self._aviso_maximo(avisos, "aviso_luzes_max", luzes, LUZES_MAXIMO)
        self._aviso_maximo(avisos, "aviso_chuveiros_max", chuveiros + chuveiros4, CHUVEIROS_MAXIMO)
        pendentes = self._avisos_pendentes("eletrica", avisos)
        if pendentes:
            return pendentes

        res = calcular_eletrica(tomadas, interruptores, luzes, conduite, fios_projeto, perda, chuveiros, chuveiros4)
        if "erro" in res:
            return {"erro": self._txt_erro(res['erro'])}

        custo_conduite = res['rolos_conduite'] * PRECO_ROLO_CONDUITE
        custo_fios = {b: f['rolos'] * PRECO_ROLO_FIO[b] for b, f in res['fios'].items()}
        custo_caixas_4x2 = res['caixas_4x2'] * PRECO_CAIXA_4X2
        custo_caixas_oct = res['caixas_octogonais'] * PRECO_CAIXA_OCTOGONAL
        custo_caixas = custo_caixas_4x2 + custo_caixas_oct
        custo_tomadas = tomadas * PRECO_TOMADA
        custo_interruptores = interruptores * PRECO_INTERRUPTOR
        custo_mat = custo_conduite + sum(custo_fios.values()) + custo_caixas + custo_tomadas + custo_interruptores

        def origem(do_projeto):
            return txt("label_do_projeto") if do_projeto else txt("label_estimado")

        def rolos(qtd, un1, un2):
            return f"{fmt_int(qtd)} {txt(un1) if qtd == 1 else txt(un2)}"

        # Quantidades do topo: o que for zero não aparece
        texto_res = ""
        for qtd, rotulo in ((tomadas, "label_tomadas"), (interruptores, "label_interruptores"), (luzes, "label_luzes"),
                            (chuveiros, "label_chuveiros"), (chuveiros4, "label_chuveiros4")):
            if qtd > 0:
                texto_res += f"{txt(rotulo)}: {fmt_int(qtd)}\n"
        if res['rolos_conduite'] > 0:
            texto_res += (
                f"• {txt('label_conduite')} ({origem(not res['conduite_estimado'])}, {self._txt_perda(perda)}): "
                f"{fmt_num(res['conduite_m'], 1)} m = {rolos(res['rolos_conduite'], 'un_rolo_conduite', 'un_rolos_conduite')} ({fmt_moeda(custo_conduite)})\n"
            )
        for bitola, fio in res['fios'].items():
            texto_res += (
                f"• {txt('label_fio').format(b=self._rotulo_bitola_fio(bitola))} ({origem(fio['do_projeto'])}, {self._txt_perda(perda)}): "
                f"{fmt_num(fio['metros'], 1)} m = {rolos(fio['rolos'], 'un_rolo_fio', 'un_rolos_fio')} ({fmt_moeda(custo_fios[bitola])})\n"
            )
        if res['caixas_4x2'] > 0:
            texto_res += f"• {txt('label_caixa_4x2')}: {fmt_int(res['caixas_4x2'])} {self._unidade(res['caixas_4x2'], 'un_unidade', 'un_unidades')} ({fmt_moeda(custo_caixas_4x2)})\n"
        if res['caixas_octogonais'] > 0:
            texto_res += f"• {txt('label_caixa_oct')}: {fmt_int(res['caixas_octogonais'])} {self._unidade(res['caixas_octogonais'], 'un_unidade', 'un_unidades')} ({fmt_moeda(custo_caixas_oct)})\n"
        if tomadas > 0:
            texto_res += f"• {txt('label_tomadas')}: {fmt_int(tomadas)} {self._unidade(tomadas, 'un_unidade', 'un_unidades')} ({fmt_moeda(custo_tomadas)})\n"
        if interruptores > 0:
            texto_res += f"• {txt('label_interruptores')}: {fmt_int(interruptores)} {self._unidade(interruptores, 'un_unidade', 'un_unidades')} ({fmt_moeda(custo_interruptores)})\n"
        texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"

        inputs = {
            "tomadas": tomadas if tomadas else "", "interruptores": interruptores if interruptores else "",
            "luzes": luzes if luzes else "", "chuveiros": chuveiros if chuveiros else "",
            "chuveiros4": chuveiros4 if chuveiros4 else "", "conduite": conduite if conduite is not None else "", "perda": perda,
        }
        for bitola in BITOLAS_FIO:
            inputs[self._chave_fio(bitola)] = fios_projeto.get(bitola, "")

        resultado = {
            "etapa": txt("secao_eletrica"),
            "tipo": "eletrica",
            "rolos_conduite": res['rolos_conduite'],
            "fios": {str(b): f['rolos'] for b, f in res['fios'].items()},
            "caixas_4x2": res['caixas_4x2'], "caixas_octogonais": res['caixas_octogonais'],
            "tomadas": tomadas, "interruptores": interruptores, "chuveiros": chuveiros, "chuveiros4": chuveiros4,
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": inputs,
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_contrapiso(self, e):
        if not (e.get("area") or "").strip() or not (e.get("esp") or "").strip():
            return {"erro": txt("msg_erro_num")}

        area = self._numero(e["area"])
        esp = self._numero(e["esp"])
        perda = self._numero(e.get("perda"), PERDA_PADRAO_CONTRAPISO)

        # Limites com aviso (contrapiso.py). O normal é de 5 a 7 cm (engenheiro).
        avisos = []
        self._aviso_maximo(avisos, "aviso_area_max", area, AREA_MAXIMA_CONTRAPISO_M2, "area")
        self._aviso_faixa(avisos, "aviso_espessura", esp, ESPESSURA_MINIMA_CONTRAPISO_CM, ESPESSURA_MAXIMA_CONTRAPISO_CM, "centimetro")
        pendentes = self._avisos_pendentes("contrapiso", avisos)
        if pendentes:
            return pendentes

        res = calcular_contrapiso(area_m2=area, espessura_cm=esp, perda_percentual=perda, traco=self.traco["contrapiso"])
        if "erro" in res:
            return {"erro": self._txt_erro(res['erro'])}

        custo_cimento = res['sacos_cimento'] * TABELA_PRECOS_GLOBAL.cimento_50kg
        custo_areia = res['areia_m3'] * TABELA_PRECOS_GLOBAL.areia_m3
        custo_pedra = res['pedra_m3'] * TABELA_PRECOS_GLOBAL.pedra_m3
        custo_mat = custo_cimento + custo_areia + custo_pedra

        texto_res = (
            f"{txt('label_area_contrapiso')}: {fmt_num(res['area_m2'], 2)} m²\n"
            f"{txt('label_espessura_media')}: {self._med_curto(esp, 'centimetro')}\n"
            f"{txt('label_traco_curto')}: {self._rotulo_traco(res['traco'])}\n"
            f"{txt('label_volume')} ({self._txt_perda(perda)}): {fmt_num(res['volume_com_perda_m3'], 3)} m³\n"
            f"{self._linhas_concreto(res, custo_cimento, custo_areia, custo_pedra)}"
            f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"
        )

        resultado = {
            "etapa": txt("secao_contrapiso"),
            "tipo": "contrapiso",
            "cimento": res['sacos_cimento'], "areia": res['areia_m3'], "pedra": res['pedra_m3'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {"area": area, "esp": esp, "perda": perda, "traco": res["traco"]}
        }
        return {"texto": texto_res, "resultado": resultado}

    def _calcular_paredes(self, e):
        if not (e.get("area") or "").strip():
            return {"erro": txt("msg_erro_num")}

        area = self._numero(e["area"])
        vaos = self._numero(e.get("vaos"), 0.0)
        junta = self._numero(e.get("junta"), JUNTA_PADRAO_CM)
        quebra = self._numero(e.get("quebra"), QUEBRA_PADRAO_PERCENTUAL)
        tijolo = self.tijolo["paredes"]
        assent = self.assent["paredes"]

        # Limites de conferência (paredes.py): passar deles pergunta se quer continuar.
        # Número negativo não entra aqui: continua com o erro do paredes.py.
        avisos = []
        if area > AREA_MAXIMA_M2:
            avisos.append(txt("aviso_area_max").format(
                valor=self._med_curto(area, "area"), max=self._med_curto(AREA_MAXIMA_M2, "area", 0)))
        if 0 <= junta < JUNTA_MINIMA_CM or junta > JUNTA_MAXIMA_CM:
            avisos.append(txt("aviso_junta").format(
                valor=self._med_curto(junta, "centimetro"),
                min=self._med_curto(JUNTA_MINIMA_CM, "centimetro") if sistema_unidades() != IMPERIAL else "3/16 in",
                max=self._med_curto(JUNTA_MAXIMA_CM, "centimetro") if sistema_unidades() != IMPERIAL else "1 1/4 in",
            ))
        if quebra > QUEBRA_MAXIMA_PERCENTUAL:
            avisos.append(txt("aviso_quebra_max").format(
                valor=self._num_curto(quebra), max=self._num_curto(QUEBRA_MAXIMA_PERCENTUAL)))
        pendentes = self._avisos_pendentes("paredes", avisos)
        if pendentes:
            return pendentes

        res = calcular_paredes(
            area_bruta_m2=area, tijolo=tijolo, assentamento=assent,
            desconto_vaos_m2=vaos, junta_cm=junta, quebra_percentual=quebra,
            traco=self.traco["paredes"]
        )
        if "erro" in res:
            return {"erro": self._txt_erro(res['erro'])}

        custo_tijolo = res['unidades'] * res['preco_unitario']
        custo_cimento = res['sacos_cimento'] * TABELA_PRECOS_GLOBAL.cimento_50kg
        custo_cal = res['sacos_cal'] * TABELA_PRECOS_GLOBAL.cal_20kg
        custo_areia = res['areia_m3'] * TABELA_PRECOS_GLOBAL.areia_m3
        custo_mat = custo_tijolo + custo_cimento + custo_cal + custo_areia

        texto_res = f"{txt('label_area_bruta')}: {fmt_num(res['area_bruta_m2'], 2)} m²\n"
        if res['desconto_vaos_m2'] > 0:  # sem vãos, a área líquida é igual à bruta (igual ao Reboco e ao Azulejo)
            texto_res += f"{txt('label_vaos')}: {fmt_num(res['desconto_vaos_m2'], 2)} m²\n"
            texto_res += f"{txt('label_area_liquida')}: {fmt_num(res['area_liquida_m2'], 2)} m²\n"
        texto_res += (
            f"{txt('label_traco_curto')}: {self._rotulo_traco(res['traco'])}\n"
            f"• {self._rotulo_tijolo(tijolo)}: {fmt_int(res['unidades'])} {self._unidade(res['unidades'], 'un_unidade', 'un_unidades')}"
            f"{self._txt_milheiros(res['milheiros'])} ({fmt_moeda(custo_tijolo)})\n"
        )
        # Material que deu zero não aparece (ex.: traço 1:0:3 não tem cal)
        texto_res += self._linhas_massa(res, custo_cimento, custo_cal, custo_areia)
        texto_res += f"\n{txt('label_custo')}: {fmt_moeda(custo_mat)}"

        resultado = {
            "etapa": txt("secao_paredes"),
            "tipo": "paredes",
            "cimento": res['sacos_cimento'], "cal": res['sacos_cal'], "areia": res['areia_m3'],
            "tijolos": res['unidades'],
            "custo_mat": custo_mat, "custo_mo": 0.0, "custo_total": custo_mat,
            "resumo_texto": texto_res,
            "inputs": {
                "area": area, "vaos": vaos, "junta": junta, "quebra": quebra,
                "tijolo": tijolo, "assent": assent, "traco": res["traco"]
            }
        }
        return {"texto": texto_res, "resultado": resultado}

    def executar_calculo(self, instance=None):
        """Botão Calcular: calcula a aba aberta e mostra o resultado."""
        self._capturar_estado()
        aba = self.aba_atual
        r = self._calcular_aba(aba, self.estado_abas.get(aba, {}))
        if "aviso" in r:  # passou de um limite: pergunta se quer continuar
            self._pedir_confirmacao(aba, r["aviso"], self.executar_calculo)
            return
        if "erro" in r:
            self.textos_resultado.pop(aba, None)
            self._lbl_resultado.text = r["erro"]
            return
        self.textos_resultado[aba] = r["texto"]
        self._lbl_resultado.text = sem_quebra(r["texto"])  # número e unidade sempre na mesma linha

    # --- USADO PELO HISTÓRICO (visualizar / editar) ---
    @staticmethod
    def _texto_campo(valor) -> str:
        if isinstance(valor, float) and valor.is_integer():
            valor = int(valor)
        return str(valor).replace('.', CONFIG_APP["separador_decimal"])

    def preencher_campos(self, inputs_dict: dict, modo_leitura: bool = False, tipo: str = "brocas"):
        """Carrega os valores salvos de UMA aba (o Histórico chama uma vez por aba).
        As medidas estão salvas em métrico; nos EUA, aparecem convertidas para ft, in, sq ft..."""
        self._sincronizar_unidades()  # as outras abas já carregadas ficam nas unidades atuais
        aba = tipo if tipo in ABAS_ORDEM else ABAS_ORDEM[0]
        self.modo_somente_leitura = modo_leitura
        self.aba_atual = aba

        tabela_tracos, traco_padrao, _ = self._tabela_traco(aba)
        traco = inputs_dict.get("traco")
        self.traco[aba] = traco if traco in tabela_tracos else traco_padrao
        if aba in self.tijolo:
            self.tijolo[aba] = inputs_dict.get("tijolo") if inputs_dict.get("tijolo") in TIJOLOS else TIJOLO_PADRAO
        if aba in self.assent:
            self.assent[aba] = inputs_dict.get("assent") if inputs_dict.get("assent") in ASSENTAMENTOS else ASSENTAMENTO_PADRAO
        if aba in self.bitola:
            bitola = inputs_dict.get("bitola")
            self.bitola[aba] = bitola if bitola in BITOLAS_LONGITUDINAL else BITOLA_PADRAO
        if aba in self.imperm:
            self.imperm[aba] = bool(inputs_dict.get("imperm"))
        if aba in self.dois_lados:
            self.dois_lados[aba] = bool(inputs_dict.get("dois_lados"))
        if aba in self.chapisco:
            self.chapisco[aba] = bool(inputs_dict.get("chapisco"))
        if aba in self.argamassa:
            # Tipo salvo no orçamento; se for do outro país, troca pelo equivalente deste país
            self.argamassa[aba] = inputs_dict.get("argamassa") or argamassa_padrao(aba == "piso", sistema_unidades())
            self._trocar_argamassa_de_pais(sistema_unidades())
        if aba in self.desenho:
            self.desenho[aba] = bool(inputs_dict.get("desenho"))
        if aba == "laje":
            tipo = inputs_dict.get("tipo_laje")
            self.laje_tipo = tipo if tipo in TIPOS_LAJE else TIPO_LAJE_PADRAO
            ench = inputs_dict.get("enchimento")
            self.laje_enchimento = ench if ench in ENCHIMENTOS else ENCHIMENTO_PADRAO
            self.tela["laje"] = bool(inputs_dict.get("tela"))
        if aba == "telhado":
            telha = inputs_dict.get("tipo_telha")
            self.telha_tipo = telha if telha in TIPOS_TELHA else TIPO_TELHA_PADRAO
            self.madeiramento[aba] = bool(inputs_dict.get("madeiramento"))
        if aba == "pintura":
            self.selador[aba] = bool(inputs_dict.get("selador"))
            self.fundo[aba] = bool(inputs_dict.get("fundo"))
            massa = inputs_dict.get("massa")
            self.massa_tipo = massa if massa in TIPOS_MASSA else "nenhuma"
        if aba == "esquadrias":
            self.esquadrias_itens = [dict(item) for item in inputs_dict.get("itens", [])]
            for chave in self.esq_fixacao:
                self.esq_fixacao[chave] = bool(inputs_dict.get(chave))

        estado = {}
        for chave in CAMPOS_ABA[aba]:
            if chave in inputs_dict:
                valor = inputs_dict[chave]
                estado[chave] = "" if (chave == "esp_estribo" and not valor) else self._texto_medida(aba, chave, valor)
            elif chave == "esp_estribo":
                estado[chave] = ""  # orçamento antigo: não tinha estribos
        self.estado_abas[aba] = estado
        self._campos = {}  # não deixa os campos antigos sobrescreverem o que foi carregado
        self.montar_tela()

    def voltar_home(self, instance):
        destino = "history" if self.origem == "history" else "home"
        self.origem = "home"
        self.manager.current = destino

    def finalizar_e_ir_resumo(self, instance=None):
        """Soma todas as abas preenchidas (aba em branco é ignorada) e abre o Resumo."""
        self._capturar_estado()
        itens = []
        for aba in ABAS_ORDEM:
            estado = self.estado_abas.get(aba) or {}
            if not self._aba_iniciada(aba, estado):
                continue
            r = self._calcular_aba(aba, estado)
            if "aviso" in r:  # passou de um limite: abre a aba e pergunta (Continuar volta a finalizar)
                if aba != self.aba_atual:
                    self.trocar_aba(aba)
                self._pedir_confirmacao(aba, r["aviso"], self.finalizar_e_ir_resumo)
                return
            if "erro" in r:
                if aba != self.aba_atual:
                    self.trocar_aba(aba)
                self._lbl_resultado.text = r["erro"]
                return
            self.textos_resultado[aba] = r["texto"]
            itens.append(r["resultado"])

        if not itens:
            self._lbl_resultado.text = txt("msg_inicial")
            return

        ORCAMENTO_FINAL.clear()
        ORCAMENTO_FINAL.extend(itens)
        summary_screen = self.manager.get_screen("summary")
        summary_screen.origem = "calculator"  # o Voltar do Resumo volta para as abas
        summary_screen.atualizar_resumo()
        self.manager.current = "summary"