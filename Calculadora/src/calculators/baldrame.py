import math
from src.calculators.tracos import consumo_concreto_por_m3, TRACO_CONCRETO_PADRAO
from src.calculators.brocas import (
    PESO_POR_METRO,
    BITOLA_PADRAO,
    BITOLA_ESTRIBO_MM,
    ESPACAMENTO_ESTRIBO_PADRAO_CM,
    COBRIMENTO_CM,
    GANCHO_ESTRIBO_CM,
    PERDA_ACO_PERCENTUAL,
    BARRA_COMERCIAL_M,
    ARAME_POR_KG_ACO,
)
from src.calculators.unidades import METRICO, IMPERIAL, L_POR_GAL
from src.calculators.embalagens import grandes_e_pequenas

# Perda padrão do concreto do baldrame (CONFIRMADO pelo engenheiro em Oct 27, 2026; a da broca é 10%)
PERDA_PADRAO_BALDRAME = 5.0

# Traspasse (emenda) do ferro quando a viga passa do tamanho da barra de 12 m:
# as duas barras ficam sobrepostas por 40 vezes a bitola (ex.: ferro de 8 mm -> 32 cm).
# O engenheiro deixou a escolha com a gente (Oct 27, 2026); 40 vezes é a regra mais usada na prática.
TRASPASSE_DIAMETROS = 40

# Impermeabilização: tinta asfáltica (ex.: Neutrol), aplicada no topo e nas duas laterais da viga.
# O fabricante indica de 0,4 a 0,5 L por m²; o app usa 0,4 L/m² por demão, em 2 demãos.
# (Nos EUA isso dá 2 gal por 100 sq ft; a Henry indica de 1,5 a 2 gal por 100 sq ft: bate.)
DEMAOS_IMPERMEABILIZANTE = 2
LITROS_POR_M2_POR_DEMAO = 0.4

# Embalagens do impermeabilizante: (balde, galão), em litros
# Brasil: balde de 18 L e galão de 3,6 L (as mesmas da tinta).
# EUA (Henry, damp-proofing de fundação): balde de 5 gal com 4,75 gal de produto dentro, e galão de 1 gal.
EMBALAGENS_IMPERM_L = {
    METRICO: (18.0, 3.6),
    IMPERIAL: (4.75 * L_POR_GAL, 1 * L_POR_GAL),
}

# Preço PROVISÓRIO por litro até a tabela de preços ser refeita.
# O engenheiro pediu o preço por litro, porque o produto vem em balde e galão.
PRECO_IMPERM_LITRO = 15.50   # Brasil (R$)
# EUA ($): balde de 5 gal (4,75 gal) a $39.95 (pesquisa de Oct 28, 2026) = cerca de $2.22 por litro
PRECO_IMPERM_LITRO_EUA = 39.95 / (4.75 * L_POR_GAL)


def calcular_baldrame(
    comprimento_m: float,
    largura_cm: float,
    altura_cm: float,
    perda_percentual: float = PERDA_PADRAO_BALDRAME,
    traco: str = TRACO_CONCRETO_PADRAO,
    num_barras_longitudinais: int = 0,
    bitola_mm: float = BITOLA_PADRAO,
    espacamento_estribo_cm: float = ESPACAMENTO_ESTRIBO_PADRAO_CM,
    incluir_impermeabilizacao: bool = False,
    sistema: str = METRICO,
) -> dict:
    if comprimento_m <= 0 or largura_cm <= 0 or altura_cm <= 0:
        return {"erro": "Valores devem ser maiores que zero."}
    if perda_percentual < 0:
        return {"erro": "A perda não pode ser negativa."}
    if num_barras_longitudinais < 0 or espacamento_estribo_cm < 0:
        return {"erro": "Barras e espaçamento dos estribos não podem ser negativos."}
    if bitola_mm not in PESO_POR_METRO:
        return {"erro": "Bitola do ferro inválida."}

    largura_m = largura_cm / 100.0
    altura_m = altura_cm / 100.0

    volume = comprimento_m * largura_m * altura_m
    volume_com_perda = volume * (1 + perda_percentual / 100.0)

    consumo = consumo_concreto_por_m3(traco)
    if consumo is None:
        return {"erro": "Traço de concreto inválido."}

    sacos_cimento = math.ceil(volume_com_perda * consumo["sacos_cimento"])
    areia_m3 = round(volume_com_perda * consumo["areia_m3"], 2)
    pedra_m3 = round(volume_com_perda * consumo["pedra_m3"], 2)

    # Ferragem opcional: ferro longitudinal + estribos retangulares
    incluiu_ferragem = num_barras_longitudinais > 0
    total_metros_barras = 0.0
    traspasse_m = 0.0
    kg_longitudinal = 0.0
    barras_longitudinal = 0
    total_estribos = 0
    total_metros_estribos = 0.0
    kg_estribos = 0.0
    barras_estribos = 0

    if incluiu_ferragem:
        fator_aco = 1 + PERDA_ACO_PERCENTUAL / 100.0  # perda do ferro (cortes e sobras)
        # Emendas: uma a cada 12 m de viga, em cada barra (ex.: 30 m de viga = 2 emendas por barra)
        emendas_por_barra = max(0, math.ceil(comprimento_m / BARRA_COMERCIAL_M - 1e-9) - 1)
        traspasse_m = emendas_por_barra * num_barras_longitudinais * TRASPASSE_DIAMETROS * bitola_mm / 1000.0
        total_metros_barras = (comprimento_m * num_barras_longitudinais + traspasse_m) * fator_aco
        kg_longitudinal = round(total_metros_barras * PESO_POR_METRO[bitola_mm], 2)
        barras_longitudinal = math.ceil(total_metros_barras / BARRA_COMERCIAL_M)

        if espacamento_estribo_cm > 0:
            largura_interna_cm = largura_cm - 2 * COBRIMENTO_CM
            altura_interna_cm = altura_cm - 2 * COBRIMENTO_CM
            if largura_interna_cm <= 0 or altura_interna_cm <= 0:
                return {"erro": "Viga muito pequena para colocar estribos."}
            comprimento_estribo_m = (2 * (largura_interna_cm + altura_interna_cm) + GANCHO_ESTRIBO_CM) / 100.0
            total_estribos = int(comprimento_m * 100.0 // espacamento_estribo_cm) + 1
            total_metros_estribos = total_estribos * comprimento_estribo_m * fator_aco
            kg_estribos = round(total_metros_estribos * PESO_POR_METRO[BITOLA_ESTRIBO_MM], 2)
            barras_estribos = math.ceil(total_metros_estribos / BARRA_COMERCIAL_M)

    quilos_aco = round(kg_longitudinal + kg_estribos, 2)
    barras_12m = barras_longitudinal + barras_estribos

    # Impermeabilização opcional: topo + 2 laterais da viga
    balde_l, galao_l = EMBALAGENS_IMPERM_L[sistema]
    area_imperm_m2 = 0.0
    litros_imperm = 0.0
    latas_imperm = 0
    galoes_imperm = 0
    if incluir_impermeabilizacao:
        area_imperm_m2 = comprimento_m * (largura_m + 2 * altura_m)
        litros_imperm = area_imperm_m2 * LITROS_POR_M2_POR_DEMAO * DEMAOS_IMPERMEABILIZANTE
        latas_imperm, galoes_imperm = grandes_e_pequenas(litros_imperm, balde_l, galao_l)
    litros_compra_imperm = latas_imperm * balde_l + galoes_imperm * galao_l

    return {
        "volume_m3": round(volume, 3),
        "volume_com_perda_m3": round(volume_com_perda, 3),
        "perda_percentual": perda_percentual,
        "traco": traco,
        "sacos_cimento": sacos_cimento,
        "areia_m3": areia_m3,
        "pedra_m3": pedra_m3,
        "incluiu_ferragem": incluiu_ferragem,
        "bitola_mm": bitola_mm,
        "traspasse_m": round(traspasse_m, 2),
        "total_metros_barras": round(total_metros_barras, 2),
        "kg_longitudinal": kg_longitudinal,
        "barras_12m_longitudinal": barras_longitudinal,
        "incluiu_estribos": total_estribos > 0,
        "bitola_estribo_mm": BITOLA_ESTRIBO_MM,
        "espacamento_estribo_cm": espacamento_estribo_cm,
        "total_estribos": total_estribos,
        "total_metros_estribos": round(total_metros_estribos, 2),
        "kg_estribos": kg_estribos,
        "barras_12m_estribos": barras_estribos,
        "quilos_aco": quilos_aco,
        "arame_kg": round(quilos_aco * ARAME_POR_KG_ACO, 2),
        "barras_12m": barras_12m,
        "incluiu_impermeabilizacao": incluir_impermeabilizacao,
        "area_imperm_m2": round(area_imperm_m2, 2),
        "litros_imperm": round(litros_imperm, 1),
        "latas_imperm": latas_imperm,       # baldes (18 L no Brasil; 5 gal nos EUA)
        "galoes_imperm": galoes_imperm,     # galões (3,6 L no Brasil; 1 gal nos EUA)
        "litros_compra_imperm": round(litros_compra_imperm, 1),
    }