import math
from src.calculators.tracos import consumo_concreto_por_m3, TRACO_CONCRETO_PADRAO
from src.calculators.unidades import METRICO, IMPERIAL, KG_POR_LB, UNIDADES

# As mensagens de erro são CHAVES de texto (ex.: "erro_perda_negativa"): a tela mostra a frase
# no idioma escolhido com o txt() (os textos ficam no comum.py). Assim aqui só ficam as contas.

# Peso (kg por metro) das bitolas comerciais de aço (mm -> kg/m).
# ATENÇÃO (conferir na revisão dos cálculos): valores de tabela de trabalho.
PESO_POR_METRO = {
    5.0: 0.154,
    6.3: 0.245,
    8.0: 0.395,
    10.0: 0.617,
    12.5: 0.963,
    16.0: 1.578,
    20.0: 2.466,
}

# Bitolas oferecidas na tela para o ferro longitudinal (a de 5 mm fica só para estribo)
BITOLAS_LONGITUDINAL = [6.3, 8.0, 10.0, 12.5, 16.0]
BITOLA_PADRAO = 8.0

# Estribos (CONFIRMADO pelo engenheiro em Oct 27, 2026)
BITOLA_ESTRIBO_MM = 5.0
ESPACAMENTO_ESTRIBO_PADRAO_CM = 20.0
# Cobrimento: concreto que cobre o estribo. Broca e baldrame ficam enterrados, então o engenheiro
# indicou de 3 a 5 cm (Oct 29, 2026). A Gabi escolheu 3 cm: a gaiola fica maior, então sobra ferro e nunca falta.
COBRIMENTO_CM = 3.0
GANCHO_ESTRIBO_CM = 5.0    # sobra para fechar o estribo (nas Brocas, uma em cada ponta da espiral)

# Perda do ferro: cortes e sobras (CONFIRMADO pelo engenheiro em Oct 27, 2026)
PERDA_ACO_PERCENTUAL = 10.0

# Nas Brocas a gaiola de ferro vai só até a METADE da profundidade (CONFIRMADO pelo engenheiro em Oct 27, 2026).
# O concreto continua sendo a broca inteira; só o ferro em pé e o estribo usam essa altura.
FRACAO_GAIOLA_BROCA = 0.5

# Profundidade máxima aceita (CONFIRMADO pelo engenheiro em Oct 28, 2026: 30 m).
# Acima disso, a tela avisa para conferir o número (ex.: digitou 300 no lugar de 3,00).
PROFUNDIDADE_MAXIMA_M = 30.0

BARRA_COMERCIAL_M = 12.0

# Arame recozido para amarrar os estribos nos ferros: 2% do peso do aço (CONFIRMADO pelo engenheiro em Oct 27, 2026)
ARAME_POR_KG_ACO = 0.02
PRECO_ARAME_KG = 15.00  # preço PROVISÓRIO (R$) até a tabela de preços ser refeita

# ==========================================
# EUA (Parte A da versão EUA, Nov 9, 2026; pesquisa em claude/pesquisa_embalagens_eua.md)
# A conta continua em métrico por dentro: aqui só mudam as medidas do ferro e as embalagens.
# ==========================================
PE_M = UNIDADES["comprimento"][2]          # 1 ft = 0,3048 m
LB_POR_FT_EM_KG_POR_M = KG_POR_LB / PE_M   # 1 lb/ft = 1,488 kg/m
PE_CUBICO_M3 = PE_M ** 3                   # 1 cu ft = 0,0283 m³
JARDA_CUBICA_M3 = UNIDADES["volume"][2]    # 1 cu yd = 0,7646 m³

# Bitolas americanas: o número é o diâmetro em oitavos de polegada (#4 = 4/8 = 1/2 in).
# A chave é o diâmetro em mm (#3 = 9,525 mm), para a conta continuar igual à do Brasil.
# Peso por ft da tabela americana (Home Depot / Inch Calculator), convertido para kg/m.
BITOLAS_EUA = {9.525: "#3", 12.7: "#4", 15.875: "#5"}
PESO_POR_METRO[9.525] = 0.376 * LB_POR_FT_EM_KG_POR_M     # #3: 0,376 lb/ft
PESO_POR_METRO[12.7] = 0.668 * LB_POR_FT_EM_KG_POR_M      # #4: 0,668 lb/ft
PESO_POR_METRO[15.875] = 1.043 * LB_POR_FT_EM_KG_POR_M    # #5: 1,043 lb/ft
BITOLAS_LONGITUDINAL_EUA = [9.525, 12.7, 15.875]
BITOLA_PADRAO_EUA = 12.7       # #4, a mais usada em fundação de casa
# O estribo de 5 mm não existe nos EUA: o menor ferro comum é o #3 (PROVISÓRIO, pesquisa ⚠️)
BITOLA_ESTRIBO_EUA_MM = 9.525
# Cobrimento: o código residencial (IRC R403.1.3) pede 3 in quando o concreto encosta na terra
COBRIMENTO_EUA_CM = 3 * 2.54   # 7,62 cm
BARRA_COMERCIAL_EUA_M = 20 * PE_M   # barra de 20 ft = 6,096 m

# Embalagens americanas
SACO_CIMENTO_EUA_KG = 94 * KG_POR_LB               # cimento Portland em saco de 94 lb (42,64 kg)
SACO_CONCRETO_PRONTO_M3 = 0.60 * PE_CUBICO_M3      # concreto pronto de 80 lb rende 0,60 cu ft (Quikrete)
ROLO_ARAME_EUA_KG = 3.5 * KG_POR_LB                # arame (tie wire) em rolo de 3,5 lb


def _barras(metros, barra_m):
    """Quantas barras comprar. O "- 1e-9" é uma folguinha para o erro do computador com número
    quebrado: 220 ft de ferro em barras de 20 ft dava 11,0000000001 e virava 12 barras."""
    return math.ceil(metros / barra_m - 1e-9)


def bitolas_do_pais(sistema=METRICO):
    """(lista de bitolas do ferro em pé, bitola padrão) do país: em mm no Brasil, #3 a #5 nos EUA."""
    if sistema == IMPERIAL:
        return BITOLAS_LONGITUDINAL_EUA, BITOLA_PADRAO_EUA
    return BITOLAS_LONGITUDINAL, BITOLA_PADRAO


def rolos_arame_eua(arame_kg):
    """Rolos de 3,5 lb de arame para os kg pedidos (nos EUA o arame é vendido em rolo)."""
    if arame_kg <= 1e-9:
        return 0
    return math.ceil(arame_kg / ROLO_ARAME_EUA_KG - 1e-9)


def calcular_brocas(
    quantidade: int,
    profundidade_m: float,
    diametro_cm: float,
    perda_percentual: float = 10.0,
    incluir_ferragem: bool = False,
    num_barras_longitudinais: int = 0,
    bitola_mm: float = BITOLA_PADRAO,
    preco_mao_obra_metro: float = 0.0,
    traco: str = TRACO_CONCRETO_PADRAO,
    espacamento_estribo_cm: float = ESPACAMENTO_ESTRIBO_PADRAO_CM,
    sistema: str = METRICO
) -> dict:
    """Concreto e ferro das brocas. sistema=IMPERIAL (EUA): cobrimento de 3 in, barras de 20 ft,
    estribo #3 e, no fim, as embalagens americanas (chaves extras, ver o fim da função).
    No Brasil (METRICO) o resultado é o mesmo de sempre."""
    eua = (sistema == IMPERIAL)
    cobrimento_cm = COBRIMENTO_EUA_CM if eua else COBRIMENTO_CM
    barra_m = BARRA_COMERCIAL_EUA_M if eua else BARRA_COMERCIAL_M
    bitola_estribo_mm = BITOLA_ESTRIBO_EUA_MM if eua else BITOLA_ESTRIBO_MM

    if quantidade <= 0 or profundidade_m <= 0 or diametro_cm <= 0:
        return {"erro": "erro_qtd_prof_diam"}
    if perda_percentual < 0:
        return {"erro": "erro_perda_negativa"}
    if num_barras_longitudinais < 0 or espacamento_estribo_cm < 0:
        return {"erro": "erro_barras_estribos_negativos"}
    if bitola_mm not in PESO_POR_METRO:
        return {"erro": "erro_bitola_invalida"}

    raio_m = (diametro_cm / 100.0) / 2.0
    area_base_m2 = math.pi * (raio_m ** 2)
    volume_nominal_m3 = area_base_m2 * profundidade_m * quantidade

    # Perda ajustável
    fator_perda = 1.0 + (perda_percentual / 100.0)
    volume_total_m3 = volume_nominal_m3 * fator_perda

    consumo = consumo_concreto_por_m3(traco)
    if consumo is None:
        return {"erro": "erro_traco_concreto_invalido"}

    sacos_cimento = math.ceil(volume_total_m3 * consumo["sacos_cimento"])
    areia_m3 = round(volume_total_m3 * consumo["areia_m3"], 2)
    pedra_m3 = round(volume_total_m3 * consumo["pedra_m3"], 2)

    # Ferragem opcional: ferro longitudinal + estribos
    altura_gaiola_m = profundidade_m * FRACAO_GAIOLA_BROCA
    total_metros_barras = 0.0
    kg_longitudinal = 0.0
    barras_longitudinal = 0
    estribos_por_broca = 0
    total_estribos = 0
    total_metros_estribos = 0.0
    kg_estribos = 0.0
    barras_estribos = 0

    fator_aco = 1 + PERDA_ACO_PERCENTUAL / 100.0
    if incluir_ferragem and num_barras_longitudinais > 0:
        total_metros_barras = quantidade * altura_gaiola_m * num_barras_longitudinais * fator_aco
        kg_longitudinal = round(total_metros_barras * PESO_POR_METRO[bitola_mm], 2)
        barras_longitudinal = _barras(total_metros_barras, barra_m)

        if espacamento_estribo_cm > 0:
            diametro_interno_cm = diametro_cm - 2 * cobrimento_cm
            if diametro_interno_cm <= 0:
                return {"erro": "erro_diametro_pequeno_estribos"}
            # Estribo em ESPIRAL (resposta do engenheiro): um fio contínuo que dá voltas pela gaiola.
            # Cada volta sobe o espaçamento (passo); o comprimento de uma volta é a hipotenusa
            # entre a circunferência e o passo. Mais um gancho em cada ponta.
            circunferencia_m = math.pi * diametro_interno_cm / 100.0
            passo_m = espacamento_estribo_cm / 100.0
            voltas = altura_gaiola_m / passo_m
            espiral_por_broca_m = voltas * math.hypot(circunferencia_m, passo_m) + 2 * GANCHO_ESTRIBO_CM / 100.0
            estribos_por_broca = math.ceil(voltas)  # número de voltas
            total_estribos = estribos_por_broca * quantidade
            total_metros_estribos = espiral_por_broca_m * quantidade * fator_aco
            kg_estribos = round(total_metros_estribos * PESO_POR_METRO[bitola_estribo_mm], 2)
            barras_estribos = _barras(total_metros_estribos, barra_m)

    quilos_aco = round(kg_longitudinal + kg_estribos, 2)
    barras_12m = barras_longitudinal + barras_estribos  # nos EUA, são barras de 20 ft

    # Mão de obra opcional
    total_metros_escavados = quantidade * profundidade_m
    custo_mao_obra = round(total_metros_escavados * preco_mao_obra_metro, 2)

    resultado = {
        "volume_nominal_m3": round(volume_nominal_m3, 3),
        "volume_com_perda_m3": round(volume_total_m3, 3),
        "perda_percentual": perda_percentual,
        "traco": traco,
        "sacos_cimento": sacos_cimento,
        "areia_m3": areia_m3,
        "pedra_m3": pedra_m3,
        "incluiu_ferragem": incluir_ferragem and num_barras_longitudinais > 0,
        "bitola_mm": bitola_mm,
        "altura_gaiola_m": round(altura_gaiola_m, 2),
        "total_metros_barras": round(total_metros_barras, 2),
        "kg_longitudinal": kg_longitudinal,
        "barras_12m_longitudinal": barras_longitudinal,   # nos EUA, barras de 20 ft (vale para as 3 chaves "barras_12m")
        "incluiu_estribos": total_estribos > 0,
        "bitola_estribo_mm": bitola_estribo_mm,
        "espacamento_estribo_cm": espacamento_estribo_cm,
        "total_estribos": total_estribos,
        "total_metros_estribos": round(total_metros_estribos, 2),
        "perda_aco_percentual": PERDA_ACO_PERCENTUAL,
        "kg_estribos": kg_estribos,
        "barras_12m_estribos": barras_estribos,
        "quilos_aco": quilos_aco,
        "arame_kg": round(quilos_aco * ARAME_POR_KG_ACO, 2),
        "barras_12m": barras_12m,
        "total_metros_escavados": round(total_metros_escavados, 2),
        "custo_mao_obra": custo_mao_obra
    }

    if eua:
        # Embalagens americanas (só nos EUA; o Brasil continua com as chaves de cima).
        # Cimento: os kg do traço (sacos de 50 kg x 50) em sacos de 94 lb.
        kg_cimento = volume_total_m3 * consumo["sacos_cimento"] * 50.0
        arame_kg = resultado["arame_kg"]
        resultado.update({
            "sistema": IMPERIAL,
            "sacos_cimento": math.ceil(kg_cimento / SACO_CIMENTO_EUA_KG),     # sacos de 94 lb
            "areia_cuyd": round(volume_total_m3 * consumo["areia_m3"] / JARDA_CUBICA_M3, 2),
            "pedra_cuyd": round(volume_total_m3 * consumo["pedra_m3"] / JARDA_CUBICA_M3, 2),
            "volume_com_perda_cuyd": round(volume_total_m3 / JARDA_CUBICA_M3, 2),
            "altura_gaiola_ft": round(altura_gaiola_m / PE_M, 2),   # direto, sem arredondar em m antes (10 ft = 5.00 ft, não 4.99)
            # Ou concreto pronto em saco (cimento + areia + brita juntos): mais comum em obra pequena
            "sacos_concreto_pronto": math.ceil(volume_total_m3 / SACO_CONCRETO_PRONTO_M3),   # sacos de 80 lb
            "lb_longitudinal": round(kg_longitudinal / KG_POR_LB, 1),
            "lb_estribos": round(kg_estribos / KG_POR_LB, 1),
            "lb_aco": round(quilos_aco / KG_POR_LB, 1),
            "arame_lb": round(arame_kg / KG_POR_LB, 1),
            "rolos_arame": rolos_arame_eua(arame_kg),
        })
    return resultado