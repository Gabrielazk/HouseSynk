import math
from src.calculators.unidades import METRICO, IMPERIAL, L_POR_GAL, para_metrico
from src.calculators.embalagens import grandes_e_pequenas

# Valores padrão
DEMAOS_PADRAO = 2
# Mais que isso é quase sempre erro de digitação (ex.: "22" no lugar de "2"); a tela avisa
DEMAOS_MAXIMO = 5
PERDA_PADRAO_PINTURA = 10.0

# Rendimento da tinta: m² pintados com 1 litro, em UMA demão (CONFIRMADO pelo engenheiro em Oct 27, 2026)
RENDIMENTO_PADRAO_M2_L = 12.0

# --- Embalagens de tinta, selador, fundo e primer: (embalagem grande, embalagem pequena), em litros ---
# Brasil: lata de 18 L e galão de 3,6 L. EUA: balde de 5 gal e galão de 1 gal (Behr).
LATA_L = 18.0
GALAO_L = 3.6
EMBALAGENS_TINTA_L = {
    METRICO: (LATA_L, GALAO_L),
    IMPERIAL: (5 * L_POR_GAL, 1 * L_POR_GAL),
}
GALOES_POR_LATA = 5  # 5 galões = 1 lata; a partir daí compensa comprar a lata (vale nos dois países)

# Complementos (uma demão cada), sobre a área total (parede + teto). CONFIRMADO pelo engenheiro em Oct 27, 2026
RENDIMENTO_SELADOR_M2_L = 8.0
RENDIMENTO_FUNDO_M2_L = 10.0
TIPOS_MASSA = ["nenhuma", "corrida", "acrilica"]   # corrida: área interna seca; acrílica: externa ou úmida
CONSUMO_MASSA_KG_M2 = 0.5                         # 2 demãos finas
BALDE_MASSA_KG = 25.0

# --- EUA ---
# Rendimento da tinta: 400 sq ft por galão em uma demão (Behr: "até 400"; Sherwin-Williams: 350 a 400).
RENDIMENTO_PADRAO_EUA_SQFT_GAL = 400
# Nos EUA, selador e fundo preparador viram um produto só, o primer: 400 sq ft por galão
# (Sherwin-Williams: 400 a 450; o app usa o menor). Massa corrida não é comum (parede de drywall).
# O primer usa a mesma escolha "fundo" da tela, com o nome Primer.
RENDIMENTO_PRIMER_EUA_SQFT_GAL = 400

# Preços PROVISÓRIOS até a tabela de preços ser refeita
# Brasil (R$)
PRECO_TINTA = {
    "parede": {"lata": 300.00, "galao": 90.00},
    "teto": {"lata": 250.00, "galao": 75.00},
    "selador": {"lata": 150.00, "galao": 45.00},
    "fundo": {"lata": 170.00, "galao": 50.00},
}
PRECO_BALDE_MASSA = {"corrida": 80.00, "acrilica": 130.00}
# EUA ($): "lata" = balde de 5 gal; "galao" = galão de 1 gal.
# Tinta: Behr 5 gal a $181.00 (HD Supply) e galão a partir de $34.98 (Behr), pesquisa de Oct 28, 2026.
# Primer ("fundo"): sem preço na pesquisa; usa os números do fundo preparador do Brasil, em dólar.
PRECO_TINTA_EUA = {
    "parede": {"lata": 181.00, "galao": 34.98},
    "teto": {"lata": 181.00, "galao": 34.98},
    "fundo": {"lata": 170.00, "galao": 50.00},
}


def rendimento_padrao_m2_l(sistema: str = METRICO) -> float:
    """Rendimento padrão da tinta em m²/L (a conta é sempre em métrico).
    Nos EUA, são os 400 sq ft/gal dos fabricantes, convertidos."""
    if sistema == IMPERIAL:
        return para_metrico(RENDIMENTO_PADRAO_EUA_SQFT_GAL, "rendimento", IMPERIAL)
    return RENDIMENTO_PADRAO_M2_L


def latas_e_galoes(litros: float, sistema: str = METRICO):
    """Quantas embalagens grandes e pequenas comprar para os litros pedidos.
    Brasil: latas de 18 L e galões de 3,6 L. EUA: baldes de 5 gal e galões de 1 gal."""
    grande, pequena = EMBALAGENS_TINTA_L[sistema]
    return grandes_e_pequenas(litros, grande, pequena)


def calcular_pintura(
    area_parede_m2: float,
    area_teto_m2: float,
    demaos: int = DEMAOS_PADRAO,
    rendimento_m2_l: float = RENDIMENTO_PADRAO_M2_L,
    perda_percentual: float = PERDA_PADRAO_PINTURA,
    selador: bool = False,
    massa: str = "nenhuma",
    fundo: bool = False,
    sistema: str = METRICO,
) -> dict:
    if area_parede_m2 < 0 or area_teto_m2 < 0:
        return {"erro": "As áreas não podem ser negativas."}
    if area_parede_m2 + area_teto_m2 <= 0:
        return {"erro": "Informe a área de parede ou a área de teto."}
    if demaos <= 0 or rendimento_m2_l <= 0:
        return {"erro": "Demãos e rendimento devem ser maiores que zero."}
    if perda_percentual < 0:
        return {"erro": "A perda não pode ser negativa."}
    if massa not in TIPOS_MASSA:
        return {"erro": "Tipo de massa inválido."}

    eua = (sistema == IMPERIAL)
    if eua:  # nos EUA só existe o primer (escolha "fundo"); selador e massa não entram
        selador = False
        massa = "nenhuma"
        rendimento_fundo = para_metrico(RENDIMENTO_PRIMER_EUA_SQFT_GAL, "rendimento", IMPERIAL)
    else:
        rendimento_fundo = RENDIMENTO_FUNDO_M2_L

    fator = 1 + perda_percentual / 100.0
    area_total = area_parede_m2 + area_teto_m2

    def produto(litros):
        latas, galoes = latas_e_galoes(litros, sistema)
        return {"litros": round(litros, 1), "latas": latas, "galoes": galoes}

    itens = {}
    if area_parede_m2 > 0:
        itens["parede"] = produto(area_parede_m2 * demaos / rendimento_m2_l * fator)
    if area_teto_m2 > 0:
        itens["teto"] = produto(area_teto_m2 * demaos / rendimento_m2_l * fator)
    if selador:
        itens["selador"] = produto(area_total / RENDIMENTO_SELADOR_M2_L * fator)
    if fundo:
        itens["fundo"] = produto(area_total / rendimento_fundo * fator)

    massa_kg = area_total * CONSUMO_MASSA_KG_M2 * fator if massa != "nenhuma" else 0.0
    baldes_massa = math.ceil(massa_kg / BALDE_MASSA_KG - 1e-9) if massa_kg > 0 else 0

    return {
        "area_parede_m2": round(area_parede_m2, 2),
        "area_teto_m2": round(area_teto_m2, 2),
        "demaos": demaos,
        "rendimento_m2_l": rendimento_m2_l,
        "perda_percentual": perda_percentual,
        "itens": itens,
        "massa": massa,
        "massa_kg": round(massa_kg, 1),
        "baldes_massa": baldes_massa,
    }