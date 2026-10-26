"""Tela de Resumo: orçamento consolidado da obra e lista de compras (separados por botões no topo)."""
import os
import subprocess
import sys
import webbrowser
from urllib.parse import quote
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from src.models.database import salvar_orcamento, quantidade_orcamentos_salvos
from src.views.comum import CONFIG_APP, ORCAMENTO_FINAL, txt, fmt_moeda
from src.views import comum
from src.services.lista_compras import montar_lista_compras, cabecalho, texto_whatsapp, texto_whatsapp_orcamento
from src.calculators.reserva import PERFIS_RESERVA, PERCENTUAL_RESERVA, calcular_reserva


# --- TELA DE RESUMO CONSOLIDADO ---
class SummaryScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "summary"
        self.md_bg_color = self.theme_cls.backgroundColor
        self.dialog_salvar = None
        self.modo = "orcamento"  # "orcamento" ou "lista" (botões no topo)
        self.origem = "calculator"  # tela para onde o Voltar leva ("calculator" ou "history")
        
        layout_main = MDBoxLayout(orientation="vertical", padding="16dp", spacing="12dp")
        
        topo = MDBoxLayout(size_hint_y=None, height="40dp", spacing="10dp")
        self.titulo_topo = MDLabel(text=txt("titulo_resumo"), font_style="Title", role="medium", bold=True, theme_text_color="Primary")
        self.txt_voltar = MDButtonText(text=txt("btn_voltar"))
        self.btn_voltar = MDButton(self.txt_voltar, on_release=self.voltar)
        topo.add_widget(self.btn_voltar)
        topo.add_widget(self.titulo_topo)

        # Botões Orçamento | Lista de compras (o que está aberto fica destacado)
        self.box_modos = MDBoxLayout(size_hint_y=None, height="48dp", spacing="8dp")
        
        self.scroll = MDScrollView()
        scroll = self.scroll
        self.box_conteudo = MDBoxLayout(orientation="vertical", spacing="16dp", padding="8dp", size_hint_y=None)
        self.box_conteudo.bind(minimum_height=self.box_conteudo.setter('height'))
        
        self.lbl_detalhes = MDLabel(text=txt("lbl_resumo_vazio"), theme_text_color="Primary", size_hint_y=None)
        self.lbl_detalhes.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        
        box_botoes = MDBoxLayout(orientation="vertical", spacing="8dp", size_hint_y=None)
        box_botoes.bind(minimum_height=box_botoes.setter('height'))
        
        self.btn_salvar_hist = MDButton(MDButtonText(text=txt("btn_salvar_hist")), pos_hint={"center_x": 0.5}, on_release=self.abrir_dialog_salvar)
        self.btn_pdf = MDButton(MDButtonText(text=txt("btn_pdf")), pos_hint={"center_x": 0.5}, on_release=self.abrir_dialog_pdf)
        self.btn_editar = MDButton(MDButtonText(text=txt("btn_editar")), pos_hint={"center_x": 0.5}, on_release=self.editar_calculos)
        
        box_botoes.add_widget(self.btn_salvar_hist)
        box_botoes.add_widget(self.btn_pdf)
        box_botoes.add_widget(self.btn_editar)
        
        # Seletor da reserva para imprevistos (aparece só na aba Orçamento)
        self.box_reserva = MDBoxLayout(orientation="vertical", spacing="8dp", adaptive_height=True)
        self.menu_reserva = None
        self.box_conteudo.add_widget(self.box_reserva)
        self.box_conteudo.add_widget(self.lbl_detalhes)
        # Botão do WhatsApp (nas duas abas: manda a lista ou o resumo do orçamento), logo acima dos outros botões
        self.box_whatsapp = MDBoxLayout(orientation="vertical", adaptive_height=True)
        self.box_conteudo.add_widget(self.box_whatsapp)
        self.box_conteudo.add_widget(box_botoes)
        
        scroll.add_widget(self.box_conteudo)
        layout_main.add_widget(topo)
        layout_main.add_widget(self.box_modos)
        layout_main.add_widget(scroll)
        self.add_widget(layout_main)

    def voltar(self, instance=None):
        """Volta para a tela de onde a pessoa veio: as abas (Finalizar) ou o Histórico (botão Resumo)."""
        self.manager.current = "history" if self.origem == "history" else "calculator"

    def editar_calculos(self, instance):
        calc_screen = self.manager.get_screen("calculator")
        for child in calc_screen.layout_principal.children:
            if isinstance(child, MDScrollView):
                child.scroll_y = 1.0
        self.manager.current = "calculator"

    def abrir_dialog_salvar(self, instance):
        if not ORCAMENTO_FINAL:
            return
            
        user_id = comum.USUARIO_LOGADO.get("id") if comum.USUARIO_LOGADO else None
        LIMITE_HISTORICO_GRATIS = 5
        if quantidade_orcamentos_salvos(user_id) >= LIMITE_HISTORICO_GRATIS:
            self.dialog_limite = MDDialog(
                MDDialogHeadlineText(text="Limite Alcançado"),
                MDDialogSupportingText(text="Você atingiu o limite de 5 orçamentos. Exclua um item antigo no Histórico!"),
                MDDialogButtonContainer(
                    MDButton(MDButtonText(text=txt("btn_fechar")), on_release=lambda x: self.dialog_limite.dismiss())
                )
            )
            self.dialog_limite.open()
            return

        self.input_nome_obra = MDTextField(
            MDTextFieldHintText(text=txt("hint_nome_obra")),
            mode="outlined"
        )
        
        self.dialog_salvar = MDDialog(
            MDDialogHeadlineText(text=txt("dialog_salvar_titulo")),
            MDDialogSupportingText(text=txt("dialog_salvar_sub")),
            MDDialogContentContainer(self.input_nome_obra, orientation="vertical", padding="12dp"),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text=txt("btn_cancelar")), on_release=lambda x: self.dialog_salvar.dismiss()),
                MDButton(MDButtonText(text=txt("btn_salvar")), on_release=self.confirmar_salvar)
            )
        )
        self.dialog_salvar.open()

    def confirmar_salvar(self, instance):
        nome = self.input_nome_obra.text.strip()
        if not nome:
            nome = "Orçamento Sem Nome"
            
        subtotal_mat = sum(item.get("custo_mat", 0) for item in ORCAMENTO_FINAL)
        subtotal_mo = sum(item.get("custo_mo", 0) for item in ORCAMENTO_FINAL)
        valor_total = subtotal_mat + subtotal_mo
        
        user_id = comum.USUARIO_LOGADO.get("id") if comum.USUARIO_LOGADO else None
        salvar_orcamento(
            usuario_id=user_id,
            nome=nome,
            estado=CONFIG_APP["estado"],
            dados=[dict(item, reserva_perfil=comum.RESERVA["perfil"]) for item in ORCAMENTO_FINAL],
            valor_total=valor_total
        )
        self.dialog_salvar.dismiss()
        self.manager.get_screen("history").carregar_historico()
        self.manager.current = "history"

    # ==========================================
    # PDF: escolher o que vai no arquivo, gerar e abrir
    # ==========================================
    def abrir_dialog_pdf(self, instance=None):
        if not ORCAMENTO_FINAL:
            return
        opcoes = MDDialogContentContainer(orientation="vertical", spacing="8dp", padding="12dp")
        for tipo, chave in (("orcamento", "pdf_op_orcamento"), ("lista", "pdf_op_lista"), ("ambos", "pdf_op_ambos")):
            opcoes.add_widget(MDButton(
                MDButtonText(text=txt(chave)), style="tonal", pos_hint={"center_x": 0.5},
                on_release=lambda x, t=tipo: self.gerar_pdf(t)
            ))
        self.dialog_pdf = MDDialog(
            MDDialogHeadlineText(text=txt("pdf_titulo")),
            MDDialogSupportingText(text=txt("pdf_sub")),
            opcoes,
            MDDialogButtonContainer(
                MDButton(MDButtonText(text=txt("btn_cancelar")), on_release=lambda x: self.dialog_pdf.dismiss())
            )
        )
        self.dialog_pdf.open()

    def gerar_pdf(self, tipo):
        self.dialog_pdf.dismiss()
        try:
            from src.services.pdf_generator import gerar_pdf  # importa aqui: se faltar o reportlab, o resto do app abre normal
            caminho = gerar_pdf(ORCAMENTO_FINAL, tipo)
        except Exception as erro:
            self._aviso_pdf(txt("pdf_erro").format(erro=erro))
            return
        # Abre o PDF direto; só mostra a mensagem com o caminho se não conseguir abrir
        if not self._abrir_arquivo(caminho):
            self._aviso_pdf(txt("pdf_salvo").format(caminho=caminho))

    def _aviso_pdf(self, mensagem):
        self.dialog_aviso_pdf = MDDialog(
            MDDialogHeadlineText(text=txt("pdf_titulo")),
            MDDialogSupportingText(text=mensagem),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text=txt("btn_fechar")), on_release=lambda x: self.dialog_aviso_pdf.dismiss())
            )
        )
        self.dialog_aviso_pdf.open()

    def _abrir_arquivo(self, caminho):
        """Abre o PDF no programa padrão do computador e devolve True se deu certo.
        (No iPhone isso vai virar o botão de compartilhar.)"""
        try:
            if sys.platform.startswith("win"):
                os.startfile(caminho)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", caminho])
            else:
                subprocess.Popen(["xdg-open", caminho])
            return True
        except Exception:
            return False

    def atualizar_resumo(self):
        self.titulo_topo.text = txt("titulo_resumo")
        self.txt_voltar.text = txt("btn_voltar")
        self.btn_salvar_hist.children[0].text = txt("btn_salvar_hist")
        self.btn_pdf.children[0].text = txt("btn_pdf")
        self.btn_editar.children[0].text = txt("btn_editar")
        self._montar_botoes_modo()
        self._montar_seletor_reserva()
        self._montar_botao_whatsapp()

        if not ORCAMENTO_FINAL:
            self.lbl_detalhes.text = txt("lbl_resumo_vazio")
        elif self.modo == "lista":
            self.lbl_detalhes.text = self.texto_lista_compras()
        else:
            self.lbl_detalhes.text = self.texto_orcamento()
        self.ir_para_o_topo()

    def ir_para_o_topo(self):
        """Barra de rolagem lá em cima. Espera o texto novo ser desenhado (o tamanho dele muda) e sobe de novo."""
        for atraso in (0, 0.1):
            Clock.schedule_once(lambda dt: setattr(self.scroll, "scroll_y", 1), atraso)

    def _montar_botoes_modo(self):
        self.box_modos.clear_widgets()
        for modo, chave in (("orcamento", "resumo_aba_orcamento"), ("lista", "resumo_aba_lista")):
            self.box_modos.add_widget(MDButton(
                MDButtonText(text=txt(chave)),
                style="filled" if modo == self.modo else "outlined",
                on_release=lambda x, m=modo: self.trocar_modo(m)
            ))

    def _montar_botao_whatsapp(self):
        self.box_whatsapp.clear_widgets()
        if not ORCAMENTO_FINAL:
            return
        self.box_whatsapp.add_widget(MDButton(
            MDButtonIcon(icon="whatsapp"), MDButtonText(text=txt("btn_whatsapp")),
            style="filled", pos_hint={"center_x": 0.5}, on_release=self.enviar_whatsapp
        ))

    def enviar_whatsapp(self, instance=None):
        """Abre o WhatsApp com o texto já escrito (a lista ou o resumo do orçamento, conforme a aba aberta);
        a pessoa só escolhe o contato e envia.
        No computador abre o WhatsApp Web/Desktop; no celular, o app. (No iPhone vai virar o botão de compartilhar.)"""
        texto = texto_whatsapp(ORCAMENTO_FINAL) if self.modo == "lista" else texto_whatsapp_orcamento(ORCAMENTO_FINAL)
        link = "https://wa.me/?text=" + quote(texto)
        try:
            webbrowser.open(link)
        except Exception as erro:
            self._aviso_pdf(txt("whatsapp_erro").format(erro=erro))

    def _montar_seletor_reserva(self):
        self.box_reserva.clear_widgets()
        if self.modo != "orcamento" or not ORCAMENTO_FINAL:
            return
        self.box_reserva.add_widget(MDLabel(text=txt("label_reserva"), font_style="Title", role="small",
                                            bold=True, theme_text_color="Primary", adaptive_height=True))
        self.btn_reserva = MDButton(
            MDButtonIcon(icon="menu-down"), MDButtonText(text=txt("reserva_" + comum.RESERVA["perfil"])),
            style="outlined", size_hint_x=1, on_release=self._abrir_menu_reserva
        )
        self.box_reserva.add_widget(self.btn_reserva)

    def _abrir_menu_reserva(self, caller):
        if self.menu_reserva:
            self.menu_reserva.dismiss()
        itens = [{"text": txt("reserva_" + perfil), "on_release": lambda *args, p=perfil: self._escolher_reserva(p)}
                 for perfil in PERFIS_RESERVA]
        # mesma largura do botão: assim o menu não passa da borda da tela
        self.menu_reserva = MDDropdownMenu(caller=caller, items=itens, position="bottom", width=caller.width)
        self.menu_reserva.open()

    def _escolher_reserva(self, perfil):
        comum.RESERVA["perfil"] = perfil
        if self.menu_reserva:
            self.menu_reserva.dismiss()
        self.atualizar_resumo()

    def trocar_modo(self, modo):
        self.modo = modo
        self.atualizar_resumo()

    @staticmethod
    def _topo(titulo):
        texto = "========================================\n"
        texto += f"{titulo}\n"
        texto += "\n".join(cabecalho()) + "\n"
        texto += "========================================\n\n"
        return texto

    def texto_orcamento(self):
        """Etapas preenchidas com o custo de cada uma, o total da obra e o aviso (sem a lista de compras)."""
        subtotal_materiais = sum(item.get("custo_mat", 0) for item in ORCAMENTO_FINAL)
        subtotal_mo = sum(item.get("custo_mo", 0) for item in ORCAMENTO_FINAL)
        total_geral = subtotal_materiais + subtotal_mo

        texto = self._topo(txt("resumo_titulo"))
        texto += f"{txt('resumo_etapas')}:\n"
        for idx, item in enumerate(ORCAMENTO_FINAL, 1):
            texto += f"\n[{idx}] {item['etapa']}\n{item['resumo_texto']}\n"

        texto += "\n----------------------------------------\n"
        texto += f"{txt('resumo_financeiro')}:\n"
        texto += "----------------------------------------\n"
        texto += f"• {txt('resumo_sub_mat')}: {fmt_moeda(subtotal_materiais)}\n"
        if subtotal_mo > 0:
            texto += f"• {txt('resumo_sub_mo')}: {fmt_moeda(subtotal_mo)}\n"
        texto += f"\n{txt('resumo_total')}: {fmt_moeda(total_geral)}\n"
        perfil = comum.RESERVA["perfil"]
        reserva = calcular_reserva(total_geral, perfil)
        if reserva > 0:  # linha separada, nunca misturada nos materiais
            texto += f"• {txt('label_reserva')} – {txt('reserva_' + perfil)}: {fmt_moeda(reserva)}\n"
            texto += f"{txt('resumo_total_reserva')}: {fmt_moeda(total_geral + reserva)}\n"
        texto += "========================================\n\n"
        texto += txt("aviso_estimativa")
        return texto

    def texto_lista_compras(self):
        """Materiais de todas as abas somados e separados por loja."""
        texto = self._topo(txt("lista_titulo"))
        for grupo, linhas in montar_lista_compras(ORCAMENTO_FINAL):
            texto += f"{txt('loja_' + grupo)}\n"
            texto += "".join(f"• {linha}\n" for linha in linhas)
            texto += "\n"
        texto += "========================================\n\n"
        texto += txt("aviso_estimativa")
        return texto