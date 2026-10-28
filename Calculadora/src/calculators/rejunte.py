import math
from src.calculators.unidades import METRICO, IMPERIAL, KG_POR_LB
from src.calculators.embalagens import grandes_e_pequenas

# Perda padrão do rejunte (sobras e limpeza da junta)
PERDA_PADRAO_REJUNTE = 10.0

# Espessura padrão da peça (mm), usada quando o cliente não informa (opcional)
ESPESSURA_PADRAO_MM = 8.0

# Densidade do rejunte cimentício em kg/dm³ (CONFIRMADA pelo engenheiro em Oct 27, 2026)
DENSIDADE_REJUNTE = 1.58

# --- Embalagens ---
# Brasil: latinhas de 2 kg e 1 kg
LATA_PEQUENA_KG = 1
LATA_GRANDE_KG = 2

# EUA (Custom Building Products, Polyblend):
# - com areia (sanded), para juntas de 1/8 a 1/2 in: saco de 25 lb e caixa de 7 lb
# - sem areia (non-sanded), para juntas de 1/16 a 1/8 in: caixa de 10 lb
# A junta decide o tipo: até 1/8 in, sem areia; acima de 1/8 in, com areia.
JUNTA_MAX_SEM_AREIA_MM = 25.4 / 8   # 1/8 in = 3,175 mm
EMBALAGENS_REJUNTE_KG = {
    "lata": (LATA_GRANDE_KG, LATA_PEQUENA_KG),           # Brasil
    "com_areia": (25 * KG_POR_LB, 7 * KG_POR_LB),        # EUA: 25 lb e 7 lb
    "sem_areia": (10 * KG_POR_LB, None),                 # EUA: só caixa de 10 lb
}

# Preços PROVISÓRIOS até a tabela de preços ser refeita
# Brasil (R$): latinhas de 1 kg e 2 kg
PRECO_LATA_1KG = 10.00
PRECO_LATA_2KG = 18.00
# EUA ($): (embalagem grande, embalagem pequena). Preços vistos no Walmart na pesquisa de Oct 28, 2026
# (Polyblend Plus 25 lb $36.61, 7 lb $30.22; Polyblend sem areia 10 lb $33.83)
PRECO_REJUNTE_EUA = {
    "com_areia": (36.61, 30.22),
    "sem_areia": (33.83, 0.0),
}


def tipo_rejunte(junta_mm: float, sistema: str = METRICO) -> str:
    """Brasil: sempre 'lata'. EUA: 'sem_areia' até 1/8 in de junta, 'com_areia' acima disso."""
    if sistema != IMPERIAL:
        return "lata"
    return "sem_areia" if junta_mm <= JUNTA_MAX_SEM_AREIA_MM + 0.01 else "com_areia"


def calcular_rejunte(
    area_m2: float,
    largura_cm: float,
    altura_cm: float,
    junta_mm: float,
    espessura_mm: float = ESPESSURA_PADRAO_MM,
    perda_percentual: float = PERDA_PADRAO_REJUNTE,
    sistema: str = METRICO,
) -> dict:
    if area_m2 <= 0 or largura_cm <= 0 or altura_cm <= 0 or junta_mm <= 0:
        return {"erro": "Área, tamanho da peça e junta devem ser maiores que zero."}
    if espessura_mm <= 0:
        return {"erro": "A espessura da peça deve ser maior que zero."}
    if perda_percentual < 0:
        return {"erro": "A perda não pode ser negativa."}

    # Fórmula usada pelos fabricantes de rejunte:
    # kg/m² = ((C + L) / (C x L)) x junta x espessura x densidade   (C e L da peça em mm)
    c_mm = largura_cm * 10.0
    l_mm = altura_cm * 10.0
    consumo_kg_m2 = ((c_mm + l_mm) / (c_mm * l_mm)) * junta_mm * espessura_mm * DENSIDADE_REJUNTE

    fator = 1 + perda_percentual / 100.0
    kg_total = area_m2 * consumo_kg_m2 * fator

    # Embalagens: o máximo possível das grandes e, se sobrar, as pequenas (do jeito que sobra menos)
    tipo = tipo_rejunte(junta_mm, sistema)
    kg_grande, kg_pequena = EMBALAGENS_REJUNTE_KG[tipo]
    grandes, pequenas = grandes_e_pequenas(kg_total, kg_grande, kg_pequena)

    # Brasil: mesmos nomes de antes (latas de 2 kg e de 1 kg)
    kg_compra = max(1, math.ceil(kg_total - 1e-9))
    latas_2kg = grandes if tipo == "lata" else 0
    latas_1kg = pequenas if tipo == "lata" else 0

    return {
        "area_m2": round(area_m2, 2),
        "largura_cm": largura_cm,
        "altura_cm": altura_cm,
        "junta_mm": junta_mm,
        "espessura_mm": espessura_mm,
        "perda_percentual": perda_percentual,
        "consumo_kg_m2": round(consumo_kg_m2, 3),
        "kg_total": round(kg_total, 2),
        "kg_compra": kg_compra,
        "latas_1kg": latas_1kg,
        "latas_2kg": latas_2kg,
        "tipo_rejunte": tipo,       # "lata" (Brasil), "com_areia" ou "sem_areia" (EUA)
        "embalagens_grandes": grandes,
        "embalagens_pequenas": pequenas,
    }