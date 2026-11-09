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
    # EUA (Parte A, Nov 9, 2026): o mesmo padrão americano das Brocas
    COBRIMENTO_EUA_CM,
    BARRA_COMERCIAL_EUA_M,
    BITOLA_ESTRIBO_EUA_MM,
    PE_M,
    barras_comerciais,
    embalagens_eua,
)
from src.calculators.unidades import METRICO, IMPERIAL, L_POR_GAL
from src.calculators.embalagens import grandes_e_pequenas

# As mensagens de erro são CHAVES de texto (ex.: "erro_perda_negativa"): a tela mostra a frase
# no idioma escolhido com o txt() (os textos ficam no comum.py). Assim aqui só ficam as contas.

# Perda padrão do concreto do baldrame (CONFIRMADO pelo engenheiro em Oct 27, 2026; a da broca é 10%)
PERDA_PADRAO_BALDRAME = 5.0

# Medidas mínimas da viga (CONFIRMADO pelo engenheiro em Oct 28, 2026: largura 20 cm, altura 30 cm).
# Abaixo disso, a tela avisa para conferir (ex.: digitou 0,2 pensando em metros, mas o campo é em cm).
# O comprimento não tem máximo: depende da obra (resposta do engenheiro).
LARGURA_MINIMA_CM = 20.0
ALTURA_MINIMA_CM = 30.0

# Traspasse (emenda) do ferro quando a viga passa do tamanho da barra (12 m no Brasil, 20 ft nos EUA):
# as duas barras ficam sobrepostas por 40 vezes a bitola (ex.: ferro de 8 mm -> 32 cm; #4 -> 20 in).
# O engenheiro deixou a escolha com a gente (Oct 27, 2026); 40 vezes é a regra mais usada na prática.
# Nos EUA o IRC manda para uma tabela; a regra prática de 40 diâmetros é a mesma (PROVISÓRIO, pesquisa ⚠️).
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
    """Concreto, ferro e impermeabilização do baldrame. sistema=IMPERIAL (EUA): cobrimento de 3 in,
    barras de 20 ft (as emendas também a cada 20 ft), estribo #3 e, no fim, as embalagens americanas
    (as mesmas chaves extras das Brocas). No Brasil (METRICO) o resultado é o mesmo de sempre."""
    eua = (sistema == IMPERIAL)
    cobrimento_cm = COBRIMENTO_EUA_CM if eua else COBRIMENTO_CM
    barra_m = BARRA_COMERCIAL_EUA_M if eua else BARRA_COMERCIAL_M
    bitola_estribo_mm = BITOLA_ESTRIBO_EUA_MM if eua else BITOLA_ESTRIBO_MM

    if comprimento_m <= 0 or largura_cm <= 0 or altura_cm <= 0:
        return {"erro": "erro_valores_zero"}
    if perda_percentual < 0:
        return {"erro": "erro_perda_negativa"}
    if num_barras_longitudinais < 0 or espacamento_estribo_cm < 0:
        return {"erro": "erro_barras_estribos_negativos"}
    if bitola_mm not in PESO_POR_METRO:
        return {"erro": "erro_bitola_invalida"}

    largura_m = largura_cm / 100.0
    altura_m = altura_cm / 100.0

    volume = comprimento_m * largura_m * altura_m
    volume_com_perda = volume * (1 + perda_percentual / 100.0)

    consumo = consumo_concreto_por_m3(traco)
    if consumo is None:
        return {"erro": "erro_traco_concreto_invalido"}

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
        # Emendas: uma a cada barra de viga (12 m no Brasil, 20 ft nos EUA), em cada barra de ferro
        # (ex.: 30 m de viga = 2 emendas por barra; 50 ft = 2 emendas)
        emendas_por_barra = max(0, math.ceil(comprimento_m / barra_m - 1e-9) - 1)
        traspasse_m = emendas_por_barra * num_barras_longitudinais * TRASPASSE_DIAMETROS * bitola_mm / 1000.0
        total_metros_barras = (comprimento_m * num_barras_longitudinais + traspasse_m) * fator_aco
        kg_longitudinal = round(total_metros_barras * PESO_POR_METRO[bitola_mm], 2)
        barras_longitudinal = barras_comerciais(total_metros_barras, barra_m)

        if espacamento_estribo_cm > 0:
            largura_interna_cm = largura_cm - 2 * cobrimento_cm
            altura_interna_cm = altura_cm - 2 * cobrimento_cm
            if largura_interna_cm <= 0 or altura_interna_cm <= 0:
                return {"erro": "erro_viga_pequena_estribos"}
            comprimento_estribo_m = (2 * (largura_interna_cm + altura_interna_cm) + GANCHO_ESTRIBO_CM) / 100.0
            # Um estribo a cada espaçamento, mais o da ponta. O "+ 1e-9" é a mesma folguinha das barras:
            # 100 ft de viga com estribo a cada 6 in davam 199,99999 espaços (200 estribos, e não 201).
            total_estribos = int(comprimento_m * 100.0 / espacamento_estribo_cm + 1e-9) + 1
            total_metros_estribos = total_estribos * comprimento_estribo_m * fator_aco
            kg_estribos = round(total_metros_estribos * PESO_POR_METRO[bitola_estribo_mm], 2)
            barras_estribos = barras_comerciais(total_metros_estribos, barra_m)

    quilos_aco = round(kg_longitudinal + kg_estribos, 2)
    barras_12m = barras_longitudinal + barras_estribos  # nos EUA, são barras de 20 ft

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

    resultado = {
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
        "barras_12m_longitudinal": barras_longitudinal,   # nos EUA, barras de 20 ft (vale para as 3 chaves "barras_12m")
        "incluiu_estribos": total_estribos > 0,
        "bitola_estribo_mm": bitola_estribo_mm,
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

    if eua:
        # Embalagens americanas (as mesmas das Brocas): cimento em sacos de 94 lb, areia e brita em
        # cu yd, concreto pronto em sacos de 80 lb, ferro e arame em lb, arame em rolos de 3,5 lb.
        resultado.update(embalagens_eua(volume_com_perda, consumo, kg_longitudinal, kg_estribos,
                                        quilos_aco, resultado["arame_kg"]))
        # Emendas em ft, direto dos metros (sem arredondar em m antes)
        resultado["traspasse_ft"] = round(traspasse_m / PE_M, 2)
    return resultado