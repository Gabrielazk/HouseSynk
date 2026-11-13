"""Lista de compras: soma o mesmo material de todas as abas e separa por tipo de loja.

Usada pela tela de Resumo e pelo PDF (os dois mostram exatamente a mesma lista).
"""
from datetime import datetime

from src.calculators.hidraulica import BARRA_TUBO_M
from src.calculators.baldrame import EMBALAGENS_IMPERM_L
from src.calculators.brocas import rolos_arame_eua
from src.calculators.paredes import TIJOLOS_EUA
from src.calculators.embalagens import grandes_e_pequenas
from src.calculators.unidades import METRICO, IMPERIAL, KG_POR_LB, do_metrico
from src.views.comum import CONFIG_APP, txt, fmt_num, fmt_int, fmt_moeda
from src.calculators.reserva import calcular_reserva
from src.views.calculator_screen import CalculatorScreen, txt_do_pais
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


def _sistema(item):
    """País em que a aba foi calculada. Orçamento antigo (de antes da versão EUA) não tem
    essa informação e foi feito no Brasil: métrico."""
    return item.get("sistema", METRICO)


def _linhas_concreto_ferro_eua(itens, basico):
    """Concreto, ferro e arame das abas já adaptadas aos EUA (Brocas, Baldrame e Laje), com as embalagens
    de lá e os mesmos textos da aba (regra 17). Ficam separados dos do Brasil porque são outras
    embalagens: saco de 94 lb não soma com saco de 50 kg, e barra de 20 ft não soma com barra de 12 m."""
    C = CalculatorScreen
    eua = IMPERIAL
    total = _soma(itens, "cimento_94lb")
    if total > 0:
        basico.append(f"{txt_do_pais('label_cimento', eua)}: {fmt_int(total)} {C._unidade(total, 'un_saco_94', 'un_sacos_94', eua)}")
    total = _soma(itens, "areia_cuyd")
    if total > 0:
        basico.append(f"{txt_do_pais('label_areia', eua)}: {fmt_num(total, 2)} cu yd")
    total = _soma(itens, "pedra_cuyd")
    if total > 0:
        basico.append(f"{txt_do_pais('label_pedra', eua)}: {fmt_num(total, 2)} cu yd")
    total = _soma(itens, "concreto_80lb")
    if total > 0:
        basico.append(C._texto_concreto_pronto(total))
    total = _soma(itens, "concreto_caminhao_cuyd")  # só a Laje dos EUA tem (concreto usinado)
    if total > 0:
        basico.append(C._texto_concreto_caminhao(total))
    total = _soma(itens, "aco_lb")
    if total > 0:
        barras = _soma(itens, "barras_20ft")
        basico.append(f"{txt_do_pais('label_aco', eua)}: {fmt_num(total, 1)} lb "
                      f"({fmt_int(barras)} {C._unidade(barras, 'un_barra20ft', 'un_barras20ft', eua)})")
    total = _soma(itens, "arame_lb")
    if total > 0:
        # Os rolos saem do total somado (2 abas com 1 lb cada = 1 rolo de 3.5 lb, não 2)
        basico.append(f"{txt_do_pais('label_arame', eua)}: {fmt_num(total, 1)} lb = "
                      f"{C._texto_rolos_arame(rolos_arame_eua(total * KG_POR_LB))}")


def _linhas_massa_eua(itens, basico):
    """Massa de assentar das Paredes dos EUA (Nov 9, 2026), com os mesmos textos da aba (regra 17):
    a massa pronta tipo S em sacos de 80 lb e a alternativa do cimento de alvenaria + areia."""
    C = CalculatorScreen
    total = _soma(itens, "massa_80lb")
    if total > 0:
        basico.append(f"{txt_do_pais('label_massa_pronta', IMPERIAL)}: {fmt_int(total)} "
                      f"{C._unidade(total, 'un_saco_80', 'un_sacos_80', IMPERIAL)}")
    total = _soma(itens, "cimento_alv_70lb")
    if total > 0:
        basico.append(C._texto_cimento_alvenaria(total, _soma(itens, "areia_alv_lb")))


def _linhas_laje_eua(itens, basico):
    """Base de brita, lona e tela da Laje dos EUA (Nov 9, 2026), com os mesmos textos da aba (regra 17).
    A tela fica separada da tela do Brasil: painel de 5 x 10 ft não soma com painel de 2 x 3 m."""
    C = CalculatorScreen
    eua = IMPERIAL
    total = _soma(itens, "base_brita_cuyd")
    if total > 0:
        basico.append(f"{txt_do_pais('label_base_brita_res', eua)}: {fmt_num(total, 2)} cu yd")
    total = _soma(itens, "lona_rolos")
    if total > 0:
        basico.append(f"{txt_do_pais('label_lona_res', eua)}: {fmt_int(total)} {C._unidade(total, 'un_rolo_lona', 'un_rolos_lona', eua)}")
    total = _soma(itens, "tela_paineis_eua")
    if total > 0:
        basico.append(f"{txt_do_pais('label_tela_res', eua)}: {fmt_int(total)} "
                      f"{C._unidade(total, 'un_painel_tela_eua', 'un_paineis_tela_eua', eua)}")


def _linhas_telhado_eua(item, basico):
    """Telhado dos EUA (Nov 11, 2026), com os mesmos nomes e embalagens da aba (regra 17):
    shingle em fardos (ou telhas de concreto), cumeeira, manta, OSB, pingadeira, starter e pregos."""
    C = CalculatorScreen
    eua = IMPERIAL
    tipo = item.get("tipo_telha")
    shingle = (tipo == "shingle")

    def linha(rotulo, qtd, singular, plural):
        if qtd > 0:
            basico.append(f"{rotulo}: {fmt_int(qtd)} {C._unidade(qtd, singular, plural, eua)}")

    linha(C._rotulo_telha(tipo, eua), item.get("telhas_eua", 0),
          *(("un_fardo", "un_fardos") if shingle else ("un_unidade", "un_unidades")))
    linha(txt_do_pais("label_cumeeira", eua), item.get("cumeeiras_eua", 0),
          *(("un_fardo_cumeeira", "un_fardos_cumeeira") if shingle else ("un_peca", "un_pecas")))
    linha(txt_do_pais("label_manta_res", eua), item.get("manta_rolos", 0), "un_rolo_manta", "un_rolos_manta")
    linha(txt_do_pais("label_osb_res", eua), item.get("osb_chapas", 0), "un_chapa_osb", "un_chapas_osb")
    linha(txt_do_pais("label_pingadeira", eua), item.get("pingadeira_pecas", 0), "un_peca_10ft", "un_pecas_10ft")
    linha(txt_do_pais("label_starter", eua), item.get("starter_fardos", 0), "un_fardo_starter", "un_fardos_starter")
    linha(txt_do_pais("label_pregos_telhado", eua), item.get("pregos_caixas", 0), "un_caixa_pregos", "un_caixas_pregos")


def _linhas_eletrica_eua(item, ele):
    """Elétrica dos EUA (Nov 11, 2026), com os mesmos nomes da aba (regra 17): cabos Romex em
    rolos de 250 ft, caixas, tomadas comuns, tomadas GFCI de 20 A e interruptores."""
    C = CalculatorScreen
    eua = IMPERIAL
    for cabo, qtd in item.get("cabos_eua", {}).items():
        ele.append(f"{txt_do_pais('label_cabo', eua).format(c=cabo)}: {fmt_int(qtd)} "
                   f"{C._unidade(qtd, 'un_rolo_cabo', 'un_rolos_cabo', eua)}")
    for chave, rotulo in (("caixas_1gang", "label_caixa_4x2"), ("caixas_redondas", "label_caixa_oct"),
                          ("tomadas_eua", "label_tomadas"), ("tomadas_gfci", "label_tomadas_gfci"),
                          ("interruptores_eua", "label_interruptores")):
        qtd = item.get(chave, 0)
        if qtd > 0:
            ele.append(f"{txt_do_pais(rotulo, eua)}: {fmt_int(qtd)} {C._unidade(qtd, 'un_unidade', 'un_unidades', eua)}")


def _linhas_hidraulica_eua(item, hid):
    """Hidráulica dos EUA (Nov 11, 2026), com os mesmos nomes da aba (regra 17): tubos PEX em rolos
    de 100 ft, tubos de esgoto PVC DWV em barras de 10 ft, conexões e stop valves."""
    C = CalculatorScreen
    eua = IMPERIAL
    for tubo, qtd in item.get("tubos_eua", {}).items():
        hid.append(f"{txt_do_pais('label_tubo_eua_' + tubo, eua)}: {C._texto_tubo_eua(tubo, qtd)}")
    for tipo, qtd in item.get("conexoes_eua", {}).items():
        hid.append(f"{txt_do_pais('label_conexoes_eua_' + tipo, eua)}: {fmt_int(qtd)} "
                   f"{C._unidade(qtd, 'un_unidade', 'un_unidades', eua)}")
    qtd = item.get("registros_eua", 0)
    if qtd > 0:
        hid.append(f"{txt_do_pais('label_registros_eua', eua)}: {fmt_int(qtd)} {C._unidade(qtd, 'un_unidade', 'un_unidades', eua)}")


def montar_lista_compras(itens):
    """Recebe o orçamento (lista de resultados das abas) e devolve [(grupo, [linhas]), ...],
    só com os grupos que têm algum material. Cada material aparece só se for maior que zero."""
    grupos = {g: [] for g in GRUPOS}
    C = CalculatorScreen  # funções que escrevem latas, barras, esquadrias... do mesmo jeito das abas

    # ---------------- MATERIAL BÁSICO ----------------
    basico = grupos["basico"]
    # Tijolos: uma linha por tipo, com o mesmo nome da aba ("Tijolo baiano (9x19x19): 788 un (0,79 milheiro)").
    # Orçamento antigo sem o tipo guardado: "Tijolos/Blocos".
    por_tijolo = {}
    for item in itens:
        if item.get("tijolos", 0) > 0:
            tipo = (item.get("inputs") or {}).get("tijolo")
            por_tijolo[tipo] = por_tijolo.get(tipo, 0) + item["tijolos"]
    for tipo, total in por_tijolo.items():
        rotulo = C._rotulo_tijolo(tipo) if tipo else txt('label_tijolos_resumo')
        milheiros = total / 1000.0
        # O bloco CMU dos EUA não é vendido por milheiro: só as peças (igual à aba)
        txt_milheiro = "" if tipo in TIJOLOS_EUA else C._txt_milheiros(milheiros)
        basico.append(f"{rotulo}: {fmt_int(total)} {C._unidade(total, 'un_unidade', 'un_unidades')}{txt_milheiro}")
    total = _soma(itens, "cimento")
    if total > 0:
        basico.append(f"{txt('label_cimento')}: {fmt_int(total)} {C._unidade(total, 'un_saco', 'un_sacos')}")
    total = _soma(itens, "cal")
    if total > 0:
        basico.append(f"{txt('label_cal')}: {fmt_int(total)} {C._unidade(total, 'un_saco_cal', 'un_sacos_cal')}")
    total = _soma(itens, "areia")
    if total > 0:
        basico.append(f"{txt('label_areia')}: {fmt_num(total, 2)} m³")
    total = _soma(itens, "pedra")
    if total > 0:
        basico.append(f"{txt('label_pedra')}: {fmt_num(total, 2)} m³")
    total = _soma(itens, "aco_kg")
    if total > 0:
        basico.append(f"{txt('label_aco')}: {fmt_num(total, 1)} kg ({fmt_int(_soma(itens, 'barras_12m'))} {C._unidade(_soma(itens, 'barras_12m'), 'un_barra12', 'un_barras12')})")
    total = _soma(itens, "arame_kg")
    if total > 0:
        basico.append(f"{txt('label_arame')}: {fmt_num(total, 1)} kg")
    _linhas_concreto_ferro_eua(itens, basico)
    _linhas_massa_eua(itens, basico)
    _linhas_laje_eua(itens, basico)
    for item in _do_tipo(itens, "baldrame"):
        litros = item.get("imperm_litros", 0)
        if litros > 0:
            # Brasil: baldes de 18 L e galões de 3,6 L. EUA: baldes de 5 gal (4,75 gal) e galões de 1 gal.
            # (Vale também para orçamentos antigos, que só têm os litros.)
            sistema = _sistema(item)
            balde, galao = EMBALAGENS_IMPERM_L[sistema]
            latas, galoes = grandes_e_pequenas(litros, balde, galao)
            if sistema == IMPERIAL:
                quantidade = f"{fmt_num(do_metrico(litros, 'litro', IMPERIAL), 1)} gal"
            else:
                quantidade = f"{fmt_num(litros, 1)} L"
            basico.append(f"{txt_do_pais('label_imperm_item', sistema)}: {quantidade} "
                          f"({C._texto_latas_galoes(latas, galoes, sistema)})")
    total = _soma(itens, "laje_premoldada_m2")
    if total > 0:
        linha = f"{txt('label_laje_pm_resumo')}: {fmt_num(total, 2)} m²"
        lajotas = _soma(itens, "lajotas")
        if lajotas > 0:
            linha += f" ({txt('label_lajotas')}: {fmt_int(lajotas)} {C._unidade(lajotas, 'un_unidade', 'un_unidades')})"
        basico.append(linha)
    total = _soma(itens, "tela_paineis")
    if total > 0:
        basico.append(f"{txt('label_tela_res')}: {fmt_int(total)} {txt('un_painel_tela') if total == 1 else txt('un_paineis_tela')}")
    for item in _do_tipo(itens, "telhado"):
        if _sistema(item) == IMPERIAL:
            _linhas_telhado_eua(item, basico)
            continue
        linha = f"{txt('label_telhas_resumo')} ({C._rotulo_telha(item['tipo_telha'])}): {fmt_int(item['telhas'])} {C._unidade(item['telhas'], 'un_unidade', 'un_unidades')}"
        if item.get("cumeeiras", 0) > 0:
            linha += f" + {fmt_int(item['cumeeiras'])} {C._unidade(item['cumeeiras'], 'un_peca', 'un_pecas')} {txt('un_de')} {txt('label_cumeeira').lower()}"
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
            basico.append(f"{txt('label_res_espuma')}: {fmt_int(qtd)} {txt('un_tubo_500') if qtd == 1 else txt('un_tubos_500')}")
        if item.get("parafusos", 0) > 0:
            basico.append(f"{txt('label_res_parafusos')}: {fmt_int(item['parafusos'])} {C._unidade(item['parafusos'], 'un_unidade', 'un_unidades')}")
        if item.get("sacos_argamassa_fix", 0) > 0:
            qtd = item["sacos_argamassa_fix"]
            basico.append(f"{txt('label_res_argamassa_fix')}: {fmt_int(qtd)} {txt('un_saco_20') if qtd == 1 else txt('un_sacos_20')}")

    # ---------------- ACABAMENTO ----------------
    acab = grupos["acabamento"]
    for rotulo, tipo in (("label_piso_resumo", "piso"), ("label_azulejo_resumo", "azulejo")):
        itens_c = _do_tipo(itens, tipo)
        if itens_c:
            caixas = _soma(itens_c, "caixas")
            pecas = _soma(itens_c, "pecas")
            if caixas > 0:
                acab.append(f"{txt(rotulo)}: {fmt_int(caixas)} {C._unidade(caixas, 'un_caixa', 'un_caixas')} ({fmt_int(pecas)} {C._unidade(pecas, 'un_peca', 'un_pecas')})")
            else:
                acab.append(f"{txt(rotulo)}: {fmt_int(pecas)} {C._unidade(pecas, 'un_peca', 'un_pecas')}")
    # Argamassa colante: uma linha por tipo (o tipo muda o preço na loja), com o mesmo nome da aba:
    # "Argamassa colante AC-I: 13 sacos de 20 kg". Sacos de 20 kg (Brasil) ou de 50 lb (EUA).
    por_argamassa = {}
    for item in itens:
        if item.get("argamassa_sacos", 0) > 0:
            chave = (_sistema(item), (item.get("inputs") or {}).get("argamassa"))
            por_argamassa[chave] = por_argamassa.get(chave, 0) + item["argamassa_sacos"]
    for (sistema, tipo), total in por_argamassa.items():
        rotulo = txt_do_pais('label_argamassa_res', sistema)
        if tipo:  # orçamento antigo sem o tipo guardado: só "Argamassa colante"
            rotulo += f" {C._rotulo_argamassa(tipo, sistema)}"
        if sistema == IMPERIAL:
            unidade = txt_do_pais("un_saco_argamassa" if total == 1 else "un_sacos_argamassa", sistema)
        else:
            unidade = C._unidade(total, 'un_saco_cal', 'un_sacos_cal', sistema)
        acab.append(f"{rotulo}: {fmt_int(total)} {unidade}")
    # Rodapé: metros no Brasil, ft nos EUA
    for sistema in (METRICO, IMPERIAL):
        total = _soma([i for i in itens if _sistema(i) == sistema], "rodape_m")
        if total > 0:
            if sistema == IMPERIAL:
                acab.append(f"{txt('label_rodape')}: {fmt_num(do_metrico(total, 'comprimento', IMPERIAL), 1)} ft")
            else:
                acab.append(f"{txt('label_rodape')}: {fmt_num(total, 2)} m")
    for item in _do_tipo(itens, "rejunte"):
        kg = item.get("rejunte_kg", 0)
        if kg <= 0:
            continue
        sistema = _sistema(item)
        tipo_rej = item.get("rejunte_tipo", "lata")
        if tipo_rej == "lata":
            # Orçamento antigo não tem "rejunte_grandes": usa as latas de 2 kg e de 1 kg
            grandes = item.get("rejunte_grandes", item.get("rejunte_latas_2kg", 0))
            pequenas = item.get("rejunte_pequenas", item.get("rejunte_latas_1kg", 0))
            quantidade = f"{fmt_num(kg, 1)} kg"  # 1 casa, igual ao resultado da aba
            rotulo = txt_do_pais("label_rejunte_resumo", sistema)
        else:
            grandes = item.get("rejunte_grandes", 0)
            pequenas = item.get("rejunte_pequenas", 0)
            quantidade = f"{fmt_num(do_metrico(kg, 'peso', IMPERIAL), 1)} lb"  # 1 casa, igual ao resultado da aba
            rotulo = txt_do_pais("label_rejunte_" + tipo_rej, sistema)
        acab.append(f"{rotulo}: {quantidade} ({C._texto_rejunte(tipo_rej, grandes, pequenas, sistema)})")
    for item in _do_tipo(itens, "pintura"):
        sistema = _sistema(item)
        for produto, (latas, galoes) in item.get("pintura", {}).items():
            acab.append(f"{txt_do_pais('label_pint_' + produto, sistema)}: {C._texto_latas_galoes(latas, galoes, sistema)}")
        if item.get("baldes_massa", 0) > 0:
            qtd = item["baldes_massa"]
            acab.append(f"{C._rotulo_massa(item['massa_tipo'])}: {fmt_int(qtd)} {txt('un_balde_25') if qtd == 1 else txt('un_baldes_25')}")

    # ---------------- ELÉTRICA ----------------
    ele = grupos["eletrica"]
    for item in _do_tipo(itens, "eletrica"):
        if _sistema(item) == IMPERIAL:
            _linhas_eletrica_eua(item, ele)
            continue
        if item.get("rolos_conduite", 0) > 0:
            qtd = item["rolos_conduite"]
            ele.append(f"{txt('label_conduite')}: {fmt_int(qtd)} {txt('un_rolo_conduite') if qtd == 1 else txt('un_rolos_conduite')}")
        for bitola, qtd in item.get("fios", {}).items():
            ele.append(f"{txt('label_fio').format(b=C._rotulo_bitola_fio(float(bitola)))}: {fmt_int(qtd)} {txt('un_rolo_fio') if qtd == 1 else txt('un_rolos_fio')}")
        for chave, rotulo in (("caixas_4x2", "label_caixa_4x2"), ("caixas_octogonais", "label_caixa_oct"),
                              ("tomadas", "label_tomadas"), ("interruptores", "label_interruptores")):
            if item.get(chave, 0) > 0:
                ele.append(f"{txt(rotulo)}: {fmt_int(item[chave])} {C._unidade(item[chave], 'un_unidade', 'un_unidades')}")

    # ---------------- HIDRÁULICA ----------------
    hid = grupos["hidraulica"]
    for item in _do_tipo(itens, "hidraulica"):
        if _sistema(item) == IMPERIAL:
            _linhas_hidraulica_eua(item, hid)
            continue
        for tubo, barras in item.get("tubos", {}).items():
            hid.append(f"{txt('label_tubo_' + tubo)}: {C._texto_barras(barras, BARRA_TUBO_M[tubo])}")
        for tipo, qtd in item.get("conexoes", {}).items():
            hid.append(f"{txt('label_conexoes_' + tipo)}: {fmt_int(qtd)} {C._unidade(qtd, 'un_unidade', 'un_unidades')}")
        if item.get("registros", 0) > 0:
            hid.append(f"{txt('label_registros')}: {fmt_int(item['registros'])} {C._unidade(item['registros'], 'un_unidade', 'un_unidades')}")

    # ---------------- ESQUADRIAS (para cotação) ----------------
    for item in _do_tipo(itens, "esquadrias"):
        for esq in item.get("esquadrias", []):
            grupos["esquadrias"].append(C._texto_item_esquadria(esq))

    return [(g, grupos[g]) for g in GRUPOS if grupos[g]]


def texto_whatsapp(itens):
    """A lista de compras pronta para mandar no WhatsApp (*texto* = negrito, _texto_ = itálico)."""
    formato = "%d/%m/%Y" if CONFIG_APP.get("idioma", "pt") == "pt" else "%m/%d/%Y"
    texto = f"*{txt('lista_titulo').capitalize()} - {comum.NOME_APP}*\n{datetime.now().strftime(formato)}\n"
    for grupo, linhas in montar_lista_compras(itens):
        texto += f"\n*{txt('loja_' + grupo)}*\n"
        texto += "".join(f"• {linha}\n" for linha in linhas)
    texto += f"\n_{txt('aviso_estimativa')}_"
    return texto


def texto_whatsapp_orcamento(itens):
    """Resumo curto do orçamento para o WhatsApp: custo de cada etapa, subtotais, total e reserva.
    (O detalhe de cada material fica no PDF, senão a mensagem fica enorme.)"""
    formato = "%d/%m/%Y" if CONFIG_APP.get("idioma", "pt") == "pt" else "%m/%d/%Y"
    texto = f"*{txt('resumo_titulo').capitalize()} - {comum.NOME_APP}*\n{datetime.now().strftime(formato)}\n\n"
    for item in itens:
        if item.get("tipo") == "esquadrias" and item.get("custo_total", 0) <= 0:
            # Sem insumos: igual à aba, a frase no lugar de "R$ 0,00"
            texto += f"• {item['etapa']}: {txt('txt_esquadrias_curto')}\n"
            continue
        texto += f"• {item['etapa']}: {fmt_moeda(item.get('custo_total', 0))}\n"

    subtotal_mat = sum(i.get("custo_mat", 0) for i in itens)
    subtotal_mo = sum(i.get("custo_mo", 0) for i in itens)
    total = subtotal_mat + subtotal_mo
    texto += f"\n{txt('resumo_sub_mat')}: {fmt_moeda(subtotal_mat)}\n"
    if subtotal_mo > 0:
        texto += f"{txt('resumo_sub_mo')}: {fmt_moeda(subtotal_mo)}\n"
    texto += f"*{txt('resumo_total').capitalize()}: {fmt_moeda(total)}*\n"

    perfil = comum.RESERVA["perfil"]
    reserva = calcular_reserva(total, perfil)
    if reserva > 0:
        texto += f"{txt('label_reserva')} – {txt('reserva_' + perfil)}: {fmt_moeda(reserva)}\n"
        texto += f"*{txt('resumo_total_reserva').capitalize()}: {fmt_moeda(total + reserva)}*\n"
    texto += f"\n_{txt('aviso_estimativa')}_"
    return texto