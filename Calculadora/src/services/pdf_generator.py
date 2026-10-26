"""Gera o PDF do orçamento e/ou da lista de compras (ReportLab).

Uso: gerar_pdf(ORCAMENTO_FINAL, "orcamento" | "lista" | "ambos", pasta) -> caminho do arquivo criado.
A lista de compras vem do mesmo lugar que a tela de Resumo (src/services/lista_compras.py).
"""
import os
import re
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak,
)

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from src.views.comum import CONFIG_APP, LOGO_APP, NOME_APP, PASTA_APP, txt, fmt_moeda
from src.services.lista_compras import montar_lista_compras, cabecalho
from src.calculators.reserva import calcular_reserva
from src.views import comum

# Fonte própria (vai junto com o app em assets/fonts): a Helvetica padrão do PDF não tem "²" e "³".
# Liberation Sans, licença SIL OFL (o arquivo da licença está na mesma pasta).
PASTA_FONTES = os.path.join(PASTA_APP, "assets", "fonts")
try:
    pdfmetrics.registerFont(TTFont("HouseSynk", os.path.join(PASTA_FONTES, "LiberationSans-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("HouseSynk-Bold", os.path.join(PASTA_FONTES, "LiberationSans-Bold.ttf")))
    FONTE, FONTE_NEGRITO = "HouseSynk", "HouseSynk-Bold"
except Exception:  # sem os arquivos da fonte, usa a padrão (aí ² e ³ não aparecem)
    FONTE, FONTE_NEGRITO = "Helvetica", "Helvetica-Bold"

# Cores da marca (as mesmas do ícone)
AZUL = colors.HexColor("#2E5E7E")
AZUL_CLARO = colors.HexColor("#E8F0F5")
CINZA = colors.HexColor("#5F6B73")
LINHA = colors.HexColor("#D5DEE4")

ESTILO_TITULO = ParagraphStyle("titulo", fontName=FONTE_NEGRITO, fontSize=20, textColor=AZUL, leading=24)
ESTILO_SUBTITULO = ParagraphStyle("subtitulo", fontName=FONTE, fontSize=10, textColor=CINZA, leading=13)
ESTILO_INFO = ParagraphStyle("info", fontName=FONTE, fontSize=9, textColor=CINZA, leading=12, alignment=TA_RIGHT)
ESTILO_SECAO = ParagraphStyle("secao", fontName=FONTE_NEGRITO, fontSize=13, textColor=AZUL, leading=16, spaceBefore=6, spaceAfter=6)
ESTILO_ETAPA = ParagraphStyle("etapa", fontName=FONTE_NEGRITO, fontSize=11, textColor=colors.white, leading=14)
ESTILO_TEXTO = ParagraphStyle("texto", fontName=FONTE, fontSize=9, leading=12)
ESTILO_DETALHE = ParagraphStyle("detalhe", fontName=FONTE, fontSize=8.5, textColor=CINZA, leading=11)
ESTILO_VALOR = ParagraphStyle("valor", fontName=FONTE, fontSize=9, leading=12, alignment=TA_RIGHT)
ESTILO_NEGRITO = ParagraphStyle("negrito", fontName=FONTE_NEGRITO, fontSize=10, leading=13)
ESTILO_NEGRITO_DIR = ParagraphStyle("negrito_dir", parent=ESTILO_NEGRITO, alignment=TA_RIGHT)

LARGURA = A4[0] - 30 * mm  # largura útil (margens de 15 mm)


def _esc(texto):
    """Escapa &, < e > (o Paragraph do ReportLab entende o texto como HTML simples)."""
    return texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _separar_custo(linha):
    """'Cimento: 13 sacos (R$ 468,00)' -> ('Cimento: 13 sacos', 'R$ 468,00'). Sem custo no fim -> (linha, '')."""
    moeda = re.escape(CONFIG_APP.get("moeda", "R$"))
    m = re.match(rf"^(.*?)\s*\(({moeda} [^()]*)\)\s*$", linha)
    return (m.group(1), m.group(2)) if m else (linha, "")


def _cabecalho(titulo_doc):
    logo = Image(LOGO_APP, width=18 * mm, height=18 * mm) if os.path.exists(LOGO_APP) else Spacer(18 * mm, 18 * mm)
    nome = [Paragraph(NOME_APP, ESTILO_TITULO), Paragraph(_esc(titulo_doc), ESTILO_SUBTITULO)]
    info = [Paragraph(_esc(linha), ESTILO_INFO) for linha in cabecalho()]
    tabela = Table([[logo, nome, info]], colWidths=[22 * mm, 70 * mm, LARGURA - 92 * mm])
    tabela.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, AZUL),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return [tabela, Spacer(1, 8 * mm)]


def _bloco_etapa(numero, item):
    """Uma etapa (aba) do orçamento: faixa azul com o nome, linhas de informação e tabela de materiais com custo."""
    linhas = [l for l in item["resumo_texto"].split("\n") if l.strip()]
    rotulo_custo = txt("label_custo")
    custo_etapa = ""
    infos, materiais = [], []
    for linha in linhas:
        if linha.startswith(rotulo_custo):
            custo_etapa = linha.split(":", 1)[1].strip()
        elif linha.lstrip().startswith(("•", "-")):
            materiais.append(_separar_custo(linha.lstrip().lstrip("•-").strip()))
        elif not linha.strip().endswith(":"):  # linhas que são só título ("Portas:") ficam de fora
            infos.append(linha.strip())

    dados = [[Paragraph(_esc(f"{numero}. {item['etapa']}"), ESTILO_ETAPA), ""]]
    estilo = [
        ("SPAN", (0, 0), (-1, 0)),
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if infos:
        dados.append([Paragraph(_esc("  ·  ".join(infos)), ESTILO_DETALHE), ""])
        estilo.append(("SPAN", (0, len(dados) - 1), (-1, len(dados) - 1)))
    for descricao, valor in materiais:
        dados.append([Paragraph(_esc(descricao), ESTILO_TEXTO), Paragraph(_esc(valor), ESTILO_VALOR)])
        estilo.append(("LINEBELOW", (0, len(dados) - 1), (-1, len(dados) - 1), 0.4, LINHA))
    if custo_etapa:
        dados.append([Paragraph(_esc(rotulo_custo), ESTILO_NEGRITO), Paragraph(_esc(custo_etapa), ESTILO_NEGRITO_DIR)])
        estilo.append(("BACKGROUND", (0, len(dados) - 1), (-1, len(dados) - 1), AZUL_CLARO))

    tabela = Table(dados, colWidths=[LARGURA - 38 * mm, 38 * mm])
    tabela.setStyle(TableStyle(estilo))
    return KeepTogether([tabela, Spacer(1, 5 * mm)])


def _parte_orcamento(itens):
    partes = _cabecalho(txt("resumo_titulo").capitalize())
    partes.append(Paragraph(_esc(txt("resumo_etapas").capitalize()), ESTILO_SECAO))
    for numero, item in enumerate(itens, 1):
        partes.append(_bloco_etapa(numero, item))

    subtotal_mat = sum(i.get("custo_mat", 0) for i in itens)
    subtotal_mo = sum(i.get("custo_mo", 0) for i in itens)
    dados = [[Paragraph(_esc(txt("resumo_sub_mat")), ESTILO_TEXTO), Paragraph(fmt_moeda(subtotal_mat), ESTILO_VALOR)]]
    if subtotal_mo > 0:
        dados.append([Paragraph(_esc(txt("resumo_sub_mo")), ESTILO_TEXTO), Paragraph(fmt_moeda(subtotal_mo), ESTILO_VALOR)])
    total = ParagraphStyle("total", parent=ESTILO_NEGRITO, textColor=colors.white, fontSize=12, leading=15)
    total_dir = ParagraphStyle("total_dir", parent=total, alignment=TA_RIGHT)
    total_obra = subtotal_mat + subtotal_mo
    perfil = comum.RESERVA["perfil"]
    reserva = calcular_reserva(total_obra, perfil)
    if reserva > 0:
        # total da obra, reserva em linha separada e o total com reserva em destaque
        dados.append([Paragraph(_esc(txt("resumo_total").capitalize()), ESTILO_NEGRITO), Paragraph(fmt_moeda(total_obra), ESTILO_NEGRITO_DIR)])
        dados.append([Paragraph(_esc(f"{txt('label_reserva')} – {txt('reserva_' + perfil)}"), ESTILO_TEXTO), Paragraph(fmt_moeda(reserva), ESTILO_VALOR)])
        dados.append([Paragraph(_esc(txt("resumo_total_reserva").capitalize()), total), Paragraph(fmt_moeda(total_obra + reserva), total_dir)])
    else:
        dados.append([Paragraph(_esc(txt("resumo_total").capitalize()), total), Paragraph(fmt_moeda(total_obra), total_dir)])
    tabela = Table(dados, colWidths=[LARGURA - 50 * mm, 50 * mm])
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, -1), (-1, -1), AZUL),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, LINHA),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    partes += [Paragraph(_esc(txt("resumo_financeiro").capitalize()), ESTILO_SECAO), KeepTogether(tabela)]
    return partes


def _caixinha():
    desenho = Drawing(10, 10)
    desenho.add(Rect(0.5, 0.5, 9, 9, rx=1.5, ry=1.5, strokeColor=AZUL, strokeWidth=0.8, fillColor=None))
    return desenho


def _parte_lista(itens):
    partes = _cabecalho(txt("lista_titulo").capitalize())
    for grupo, linhas in montar_lista_compras(itens):
        # quadradinho na frente de cada material, para marcar o que já foi comprado
        dados = [[_caixinha(), Paragraph(_esc(linha), ESTILO_TEXTO)] for linha in linhas]
        tabela = Table(dados, colWidths=[9 * mm, LARGURA - 9 * mm])
        estilo = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
        for i in range(len(dados)):
            estilo.append(("LINEBELOW", (0, i), (-1, i), 0.4, LINHA))
        tabela.setStyle(TableStyle(estilo))
        partes.append(KeepTogether([Paragraph(_esc(txt("loja_" + grupo)), ESTILO_SECAO), tabela, Spacer(1, 4 * mm)]))
    return partes


class _Rodape:
    """Rodapé de todas as páginas: aviso de estimativa, nome do app e número da página."""

    def __init__(self, total_paginas=None):
        self.total = total_paginas

    def __call__(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(LINHA)
        canvas.line(15 * mm, 18 * mm, A4[0] - 15 * mm, 18 * mm)
        canvas.setFont(FONTE, 7.5)
        canvas.setFillColor(CINZA)
        canvas.drawString(15 * mm, 13 * mm, txt("aviso_estimativa"))
        pagina = f"{NOME_APP}  ·  {doc.page}" + (f" / {self.total}" if self.total else "")
        canvas.drawRightString(A4[0] - 15 * mm, 8 * mm, pagina)
        canvas.restoreState()


def gerar_pdf(itens, tipo="ambos", pasta=None):
    """Cria o PDF e devolve o caminho do arquivo. tipo: 'orcamento', 'lista' ou 'ambos'."""
    if not itens:
        raise ValueError("Nada para exportar: o orçamento está vazio.")
    pasta = pasta or pasta_padrao()
    os.makedirs(pasta, exist_ok=True)
    nome = f"{NOME_APP}_{tipo}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.pdf"
    caminho = os.path.join(pasta, nome)

    def montar():
        historia = []
        if tipo in ("orcamento", "ambos"):
            historia += _parte_orcamento(itens)
        if tipo == "ambos":
            historia.append(PageBreak())
        if tipo in ("lista", "ambos"):
            historia += _parte_lista(itens)
        return historia

    def documento():
        return SimpleDocTemplate(
            caminho, pagesize=A4, title=f"{NOME_APP} - {txt('resumo_titulo').capitalize()}",
            author=NOME_APP, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=15 * mm, bottomMargin=24 * mm,
        )

    # 1ª passada só para saber o total de páginas ("1 / 3"); a 2ª gera o arquivo final
    doc = documento()
    doc.build(montar(), onFirstPage=_Rodape(), onLaterPages=_Rodape())
    total = doc.page
    doc = documento()
    doc.build(montar(), onFirstPage=_Rodape(total), onLaterPages=_Rodape(total))
    return caminho


def pasta_padrao():
    """Onde salvar: a pasta Downloads do computador; se não existir (ex.: celular), a pasta de dados do app."""
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    if os.path.isdir(downloads):
        return downloads
    try:
        from kivy.app import App
        app = App.get_running_app()
        if app:
            return os.path.join(app.user_data_dir, "pdfs")
    except Exception:
        pass
    return os.path.join(os.path.expanduser("~"), NOME_APP)