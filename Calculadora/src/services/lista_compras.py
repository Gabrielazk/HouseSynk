"""Lista de compras: soma o mesmo material de todas as abas e separa por tipo de loja.

Usada pela tela de Resumo e pelo PDF (os dois mostram exatamente a mesma lista).
"""
import math
from datetime import datetime

from src.calculators.baldrame import LITROS_POR_LATA
from src.calculators.hidraulica import BARRA_TUBO_M
from src.views.comum import CONFIG_APP, txt, fmt_num
from src.views.calculator_screen import CalculatorScreen
from src.views import comum

# Ordem dos grupos (lojas) na lista
GRUPOS = ["basico", "acabamento", "eletrica", "hidraulica", "esquadrias"]


def cabecalho():
    """Linhas do topo do Resumo e do PDF: responsável (se estiver logado), data e região."""
    linhas = []
    usuario = comum.USUARIO_LOGADO
    if usuario and usuario.get("nome"):
        linhas.append(f"{txt('resumo_responsavel')}: {usuario['nome']} ({usuario.get('email', '')})")
    formato = "%d/%m/%Y" if CONFIG_APP.get("idioma", "pt") == "pt" else "%m/%d/%Y"
    linhas.append(f"{txt('resumo_data')}: {datetime.now().strftime(formato)}")
    linhas.append(f"{txt('resumo_regiao')}: {CONFIG_APP['pais']} ({CONFIG_APP['estado']})")
    return linhas


def _soma(itens, chave):
    return sum(item.get(chave, 0) for item in itens)


def _do_tipo(itens, tipo):
    return [item for item in itens if item.get("tipo") == tipo]


def montar_lista_compras(itens):
    """Recebe o orçamento (lista de resultados das abas) e devolve [(grupo, [linhas]), ...],
    só com os grupos que têm algum material. Cada material aparece só se for maior que zero."""
    grupos = {g: [] for g in GRUPOS}
    C = CalculatorScreen  # funções que escrevem latas, barras, esquadrias... do mesmo jeito das abas

    # ---------------- MATERIAL BÁSICO ----------------
    basico = grupos["basico"]
    total = _soma(itens, "tijolos")
    if total > 0:
        basico.append(f"{txt('label_tijolos_resumo')}: {total} {txt('un_unidades')}")
    total = _soma(itens, "cimento")
    if total > 0:
        basico.append(f"{txt('label_cimento')}: {total} {txt('un_sacos')}")
    total = _soma(itens, "cal")
    if total > 0:
        basico.append(f"{txt('label_cal')}: {total} {txt('un_sacos_cal')}")
    total = _soma(itens, "areia")
    if total > 0:
        basico.append(f"{txt('label_areia')}: {fmt_num(total, 2)} m³")
    total = _soma(itens, "pedra")
    if total > 0:
        basico.append(f"{txt('label_pedra')}: {fmt_num(total, 2)} m³")
    total = _soma(itens, "aco_kg")
    if total > 0:
        basico.append(f"{txt('label_aco')}: {fmt_num(total, 1)} kg ({_soma(itens, 'barras_12m')} {txt('un_barras12')})")
    total = _soma(itens, "arame_kg")
    if total > 0:
        basico.append(f"{txt('label_arame')}: {fmt_num(total, 1)} kg")
    total = _soma(itens, "imperm_litros")
    if total > 0:
        latas = math.ceil(total / LITROS_POR_LATA)
        basico.append(f"{txt('label_imperm_item')}: {fmt_num(total, 1)} L ({latas} {txt('un_lata') if latas == 1 else txt('un_latas')})")
    total = _soma(itens, "laje_premoldada_m2")
    if total > 0:
        linha = f"{txt('label_laje_pm_resumo')}: {fmt_num(total, 2)} m²"
        lajotas = _soma(itens, "lajotas")
        if lajotas > 0:
            linha += f" ({txt('label_lajotas')}: {lajotas} {txt('un_unidades')})"
        basico.append(linha)
    for item in _do_tipo(itens, "telhado"):
        linha = f"{txt('label_telhas_resumo')} ({C._rotulo_telha(item['tipo_telha'])}): {item['telhas']} {txt('un_unidades')}"
        if item.get("cumeeiras", 0) > 0:
            linha += f" + {item['cumeeiras']} {txt('un_pecas')} {txt('un_de')} {txt('label_cumeeira').lower()}"
        basico.append(linha)
        madeira = [
            f"{txt('label_' + chave).lower()} {fmt_num(item.get(chave + '_m', 0), 1)} m"
            for chave in ("ripas", "caibros", "tercas") if item.get(chave + "_m", 0) > 0
        ]
        if madeira:
            basico.append(f"{txt('label_madeira_resumo')}: {', '.join(madeira)}")
    for item in _do_tipo(itens, "esquadrias"):  # insumos de fixação das portas e janelas
        if item.get("tubos_espuma", 0) > 0:
            qtd = item["tubos_espuma"]
            basico.append(f"{txt('label_res_espuma')}: {qtd} {txt('un_tubo_500') if qtd == 1 else txt('un_tubos_500')}")
        if item.get("parafusos", 0) > 0:
            basico.append(f"{txt('label_res_parafusos')}: {item['parafusos']} {txt('un_unidades')}")
        if item.get("sacos_argamassa_fix", 0) > 0:
            qtd = item["sacos_argamassa_fix"]
            basico.append(f"{txt('label_res_argamassa_fix')}: {qtd} {txt('un_saco_20') if qtd == 1 else txt('un_sacos_20')}")

    # ---------------- ACABAMENTO ----------------
    acab = grupos["acabamento"]
    for rotulo, tipo in (("label_piso_resumo", "piso"), ("label_azulejo_resumo", "azulejo")):
        itens_c = _do_tipo(itens, tipo)
        if itens_c:
            caixas = _soma(itens_c, "caixas")
            pecas = _soma(itens_c, "pecas")
            if caixas > 0:
                acab.append(f"{txt(rotulo)}: {caixas} {txt('un_caixas')} ({pecas} {txt('un_pecas')})")
            else:
                acab.append(f"{txt(rotulo)}: {pecas} {txt('un_pecas')}")
    total = _soma(itens, "argamassa_sacos")
    if total > 0:
        acab.append(f"{txt('label_argamassa_resumo')}: {total} {txt('un_sacos_cal').replace(' de 20 kg', '').replace(' of 20 kg', '')}")
    total = _soma(itens, "rodape_m")
    if total > 0:
        acab.append(f"{txt('label_rodape')}: {fmt_num(total, 2)} m")
    total = _soma(itens, "rejunte_kg")
    if total > 0:
        latas_1 = _soma(itens, "rejunte_latas_1kg")
        latas_2 = _soma(itens, "rejunte_latas_2kg")
        acab.append(f"{txt('label_rejunte_resumo')}: {fmt_num(total, 2)} kg ({C._texto_latas(latas_1, latas_2)})")
    for item in _do_tipo(itens, "pintura"):
        for produto, (latas, galoes) in item.get("pintura", {}).items():
            acab.append(f"{txt('label_pint_' + produto)}: {C._texto_latas_galoes(latas, galoes)}")
        if item.get("baldes_massa", 0) > 0:
            qtd = item["baldes_massa"]
            acab.append(f"{C._rotulo_massa(item['massa_tipo'])}: {qtd} {txt('un_balde_25') if qtd == 1 else txt('un_baldes_25')}")

    # ---------------- ELÉTRICA ----------------
    ele = grupos["eletrica"]
    for item in _do_tipo(itens, "eletrica"):
        if item.get("rolos_conduite", 0) > 0:
            qtd = item["rolos_conduite"]
            ele.append(f"{txt('label_conduite')}: {qtd} {txt('un_rolo_conduite') if qtd == 1 else txt('un_rolos_conduite')}")
        for bitola, qtd in item.get("fios", {}).items():
            ele.append(f"{txt('label_fio').format(b=C._rotulo_bitola_fio(float(bitola)))}: {qtd} {txt('un_rolo_fio') if qtd == 1 else txt('un_rolos_fio')}")
        for chave, rotulo in (("caixas_4x2", "label_caixa_4x2"), ("caixas_octogonais", "label_caixa_oct"),
                              ("tomadas", "label_tomadas"), ("interruptores", "label_interruptores")):
            if item.get(chave, 0) > 0:
                ele.append(f"{txt(rotulo)}: {item[chave]} {txt('un_unidades')}")

    # ---------------- HIDRÁULICA ----------------
    hid = grupos["hidraulica"]
    for item in _do_tipo(itens, "hidraulica"):
        for tubo, barras in item.get("tubos", {}).items():
            hid.append(f"{txt('label_tubo_' + tubo)}: {C._texto_barras(barras, BARRA_TUBO_M[tubo])}")
        for tipo, qtd in item.get("conexoes", {}).items():
            hid.append(f"{txt('label_conexoes_' + tipo)}: {qtd} {txt('un_unidades')}")
        if item.get("registros", 0) > 0:
            hid.append(f"{txt('label_registros')}: {item['registros']} {txt('un_unidades')}")

    # ---------------- ESQUADRIAS (para cotação) ----------------
    for item in _do_tipo(itens, "esquadrias"):
        for esq in item.get("esquadrias", []):
            grupos["esquadrias"].append(C._texto_item_esquadria(esq))

    return [(g, grupos[g]) for g in GRUPOS if grupos[g]]
