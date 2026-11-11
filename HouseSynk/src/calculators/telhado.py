import math
from src.calculators.unidades import IMPERIAL, M2_POR_SQFT

# As mensagens de erro são CHAVES de texto (ex.: "erro_perda_negativa"): a tela mostra a frase
# no idioma escolhido com o txt() (os textos ficam no comum.py). Assim aqui só ficam as contas.

# Tipos de telha
TIPOS_TELHA = ["ceramica", "concreto", "fibrocimento"]
TIPO_TELHA_PADRAO = "ceramica"

# Perda padrão (quebras e recortes)
PERDA_PADRAO_TELHADO = 5.0

# Inclinação padrão (%) de cada tipo de telha (PROVISÓRIO, confirmar com o engenheiro)
INCLINACAO_PADRAO = {"ceramica": 30.0, "concreto": 30.0, "fibrocimento": 15.0}

# Limites com aviso (regra 12): passar deles abre a janela "Confira os valores", com Continuar.
# Criados pelo Leo em Nov 3, 2026 (o engenheiro ainda vai conferir; se ele mudar, é só trocar aqui).
AREA_MAXIMA_TELHADO_M2 = 2000.0
INCLINACAO_MAXIMA_PERCENTUAL = 100.0  # telhado bem inclinado já fica perto de 45%

# Telhas por m² de telhado (PROVISÓRIO, confirmar com o engenheiro)
# Cerâmica: tipo romana. Fibrocimento: telha de 2,44 x 1,10 m (cerca de 2,4 m² úteis cada)
TELHAS_POR_M2 = {"ceramica": 16.0, "concreto": 10.5, "fibrocimento": 1 / 2.4}

# Peças de cumeeira por metro (PROVISÓRIO, confirmar com o engenheiro)
CUMEEIRAS_POR_M = {"ceramica": 3.0, "concreto": 3.0, "fibrocimento": 1.0}

# Madeiramento: metros de madeira por m² de telhado (PROVISÓRIO, confirmar com o engenheiro)
# Telha fibrocimento vai direto nas terças (sem ripas e caibros)
MADEIRA_POR_M2 = {
    "ceramica": {"ripas": 3.0, "caibros": 2.0, "tercas": 0.6},
    "concreto": {"ripas": 3.0, "caibros": 2.0, "tercas": 0.6},
    "fibrocimento": {"ripas": 0.0, "caibros": 0.0, "tercas": 0.8},
}

# Preços PROVISÓRIOS (R$) até a tabela de preços ser refeita
PRECO_TELHA = {"ceramica": 2.50, "concreto": 4.50, "fibrocimento": 75.00}      # por telha
PRECO_CUMEEIRA = {"ceramica": 4.00, "concreto": 8.00, "fibrocimento": 45.00}   # por peça
PRECO_MADEIRA_M = {"ripas": 3.00, "caibros": 9.00, "tercas": 25.00}            # por metro


def calcular_telhado(
    area_m2: float,
    tipo_telha: str = TIPO_TELHA_PADRAO,
    inclinacao_percentual: float = None,
    cumeeira_m: float = 0.0,
    incluir_madeiramento: bool = False,
    perda_percentual: float = PERDA_PADRAO_TELHADO,
) -> dict:
    if tipo_telha not in TIPOS_TELHA:
        return {"erro": "erro_telha_invalida"}
    if inclinacao_percentual is None:
        inclinacao_percentual = INCLINACAO_PADRAO[tipo_telha]
    if area_m2 <= 0:
        return {"erro": "erro_area_zero"}
    if inclinacao_percentual < 0 or cumeeira_m < 0 or perda_percentual < 0:
        return {"erro": "erro_valores_negativos"}

    # A área informada é a da planta (vista de cima); a inclinação aumenta a área real do telhado
    area_real = area_m2 * math.sqrt(1 + (inclinacao_percentual / 100.0) ** 2)
    fator = 1 + perda_percentual / 100.0

    telhas = math.ceil(area_real * TELHAS_POR_M2[tipo_telha] * fator - 1e-9)
    cumeeiras = math.ceil(cumeeira_m * CUMEEIRAS_POR_M[tipo_telha] * fator - 1e-9) if cumeeira_m > 0 else 0

    madeira = {"ripas": 0.0, "caibros": 0.0, "tercas": 0.0}
    if incluir_madeiramento:
        for peca, metros_m2 in MADEIRA_POR_M2[tipo_telha].items():
            madeira[peca] = round(area_real * metros_m2 * fator, 1)

    return {
        "area_planta_m2": round(area_m2, 2),
        "inclinacao_percentual": inclinacao_percentual,
        "area_real_m2": round(area_real, 2),
        "tipo_telha": tipo_telha,
        "perda_percentual": perda_percentual,
        "telhas": telhas,
        "cumeeira_m": round(cumeeira_m, 2),
        "cumeeiras": cumeeiras,
        "incluiu_madeiramento": incluir_madeiramento,
        "ripas_m": madeira["ripas"],
        "caibros_m": madeira["caibros"],
        "tercas_m": madeira["tercas"],
    }

# ==========================================
# EUA (Parte A da versão EUA, Nov 11, 2026; pesquisa em claude/pesquisa_embalagens_eua.md)
# Na casa americana o telhado mais comum é o de shingle asfáltico, sem ripa e caibro: a estrutura
# recebe chapas de OSB, depois a manta (underlayment) e depois o shingle. A telha de concreto
# também existe (mais no sul). Decisões da Gabi (Nov 11, 2026): shingle e concreto no menu
# (o fibrocimento sai), inclinação em pitch (x/12, padrão 6/12) e perda de 10%.
# A conta continua em métrico por dentro; aqui só entram as embalagens de lá.
# ==========================================
TIPOS_TELHA_EUA = ["shingle", "concreto"]
TIPO_TELHA_PADRAO_EUA = "shingle"

PERDA_PADRAO_TELHADO_EUA = 10.0   # as calculadoras de lá usam 10% no telhado de duas águas (15% no de quatro)

# Pitch: quanto o telhado sobe a cada 12 de largura (6/12 = 50%). A conta usa a porcentagem.
PERCENTUAL_POR_PITCH = 100.0 / 12.0
INCLINACAO_PADRAO_EUA = 6 * PERCENTUAL_POR_PITCH          # 6/12 = 50% (PROVISÓRIO ⚠️, o mais comum)
# Mínimo do código IRC (só aviso, regra 12): shingle 2/12 (R905.2.2) e telha de concreto 2 1/2/12 (R905.3.2)
INCLINACAO_MINIMA_EUA = {"shingle": 2 * PERCENTUAL_POR_PITCH, "concreto": 2.5 * PERCENTUAL_POR_PITCH}
# Abaixo de 4/12 o IRC pede a manta em 2 camadas (Tabela R905.1.1)
INCLINACAO_MANTA_DUPLA = 4 * PERCENTUAL_POR_PITCH

SQFT_POR_SQUARE = 100.0            # 1 square = 100 sq ft (o jeito de lá de medir telhado)
FARDOS_SHINGLE_POR_SQUARE = 3      # 3 fardos de 33,3 sq ft = 1 square (pesquisa ✅)
TELHAS_CONCRETO_POR_SQUARE = 87    # Boral: 85 a 87 peças por square (pesquisa ✅; o maior, para não faltar)
CUMEEIRA_SHINGLE_FT_POR_FARDO = 33.3   # fardo de cumeeira (hip & ridge) de 33,3 ft (Tamko, GAF; pesquisa ✅)
CUMEEIRA_CONCRETO_PECAS_POR_FT = 1.0   # 1 peça de cumeeira por ft (PROVISÓRIO ⚠️; o Brasil usa 3 por metro)
MANTA_SQFT_POR_ROLO = 937.5        # rolo de 10 squares cobre 937,5 sq ft úteis, pela sobreposição (TAMKO ✅)
OSB_SQFT_POR_CHAPA = 4 * 8         # chapa de OSB de 4 x 8 ft (pesquisa ✅)
STARTER_FT_POR_FARDO = 120.0       # starter (primeira fiada), beirais e oitões: 120 ft por fardo (GAF Pro-Start ✅)
PINGADEIRA_PECA_FT = 10.0          # pingadeira (drip edge) em peças de 10 ft (Home Depot ✅)
PINGADEIRA_EMENDA_FT = 2 / 12.0    # 2 in de emenda entre as peças (IRC R905.2.8.5 ✅)
PREGOS_POR_SQUARE = 320            # 4 pregos por shingle, cerca de 320 por square (código ✅)
PREGOS_POR_CAIXA = 978             # caixa de 5 lb de pregos de 1 1/4 in: cerca de 978 (Grip-Rite ✅; a menor contagem)

# Preços PROVISÓRIOS ($) até a tabela de preços ser refeita
PRECO_TELHA_EUA = {"shingle": 40.00, "concreto": 4.50}     # shingle por fardo; concreto por telha (o número do Brasil)
PRECO_CUMEEIRA_EUA = {"shingle": 60.00, "concreto": 8.00}  # shingle por fardo; concreto por peça (o número do Brasil)
PRECO_ROLO_MANTA = 120.00
PRECO_CHAPA_OSB = 20.00
PRECO_FARDO_STARTER = 55.00
PRECO_PECA_PINGADEIRA = 10.00
PRECO_CAIXA_PREGOS = 18.00


def tipos_telha_do_pais(sistema):
    """As telhas do menu e a padrão de cada país: (lista, padrão)."""
    if sistema == IMPERIAL:
        return TIPOS_TELHA_EUA, TIPO_TELHA_PADRAO_EUA
    return TIPOS_TELHA, TIPO_TELHA_PADRAO


def _pecas(quantidade, por_peca):
    """Quantas peças inteiras para cobrir a quantidade (com a mesma folguinha das barras)."""
    return math.ceil(quantidade / por_peca - 1e-9) if quantidade > 0 else 0


def calcular_telhado_eua(
    area_m2: float,
    tipo_telha: str = TIPO_TELHA_PADRAO_EUA,
    inclinacao_percentual: float = INCLINACAO_PADRAO_EUA,
    cumeeira_m: float = 0.0,
    perimetro_m: float = 0.0,
    incluir_manta: bool = True,
    incluir_osb: bool = False,
    perda_percentual: float = PERDA_PADRAO_TELHADO_EUA,
) -> dict:
    """Telhado dos EUA. Recebe em métrico (a tela converte o que foi digitado) e devolve as
    quantidades nas embalagens de lá: shingle em fardos (3 por square) ou telhas de concreto,
    cumeeira, manta em rolos de 10 squares, chapas de OSB 4 x 8 ft, starter, pingadeira e pregos.
    O perímetro (beirais + oitões) é opcional: sem ele, o starter e a pingadeira não entram."""
    if tipo_telha not in TIPOS_TELHA_EUA:
        return {"erro": "erro_telha_invalida"}
    if area_m2 <= 0:
        return {"erro": "erro_area_zero"}
    if inclinacao_percentual < 0 or cumeeira_m < 0 or perimetro_m < 0 or perda_percentual < 0:
        return {"erro": "erro_valores_negativos"}

    shingle = (tipo_telha == "shingle")
    area_real = area_m2 * math.sqrt(1 + (inclinacao_percentual / 100.0) ** 2)
    fator = 1 + perda_percentual / 100.0

    # Tudo o que cobre o telhado usa a área real com a perda (igual ao Brasil)
    area_compra_sqft = area_real / M2_POR_SQFT * fator
    squares = area_compra_sqft / SQFT_POR_SQUARE
    if shingle:
        telhas = _pecas(squares * FARDOS_SHINGLE_POR_SQUARE, 1)          # fardos de shingle
    else:
        telhas = _pecas(squares * TELHAS_CONCRETO_POR_SQUARE, 1)         # telhas de concreto

    cumeeira_ft = cumeeira_m / 0.3048
    if shingle:
        cumeeiras = _pecas(cumeeira_ft * fator, CUMEEIRA_SHINGLE_FT_POR_FARDO)    # fardos de 33,3 ft
    else:
        cumeeiras = _pecas(cumeeira_ft * CUMEEIRA_CONCRETO_PECAS_POR_FT * fator, 1)  # peças

    camadas_manta = 0
    if incluir_manta:
        camadas_manta = 2 if inclinacao_percentual < INCLINACAO_MANTA_DUPLA - 1e-9 else 1
    manta_rolos = _pecas(area_compra_sqft * camadas_manta, MANTA_SQFT_POR_ROLO)

    osb_chapas = _pecas(area_compra_sqft, OSB_SQFT_POR_CHAPA) if incluir_osb else 0

    perimetro_ft = perimetro_m / 0.3048
    starter_fardos = _pecas(perimetro_ft * fator, STARTER_FT_POR_FARDO) if shingle else 0
    pingadeira_pecas = _pecas(perimetro_ft * fator, PINGADEIRA_PECA_FT - PINGADEIRA_EMENDA_FT)

    pregos = math.ceil(squares * PREGOS_POR_SQUARE - 1e-9) if shingle else 0
    pregos_caixas = _pecas(pregos, PREGOS_POR_CAIXA)

    return {
        "sistema": IMPERIAL,
        "area_planta_m2": area_m2,
        "inclinacao_percentual": inclinacao_percentual,
        "area_real_m2": area_real,
        "tipo_telha": tipo_telha,
        "perda_percentual": perda_percentual,
        "squares": round(squares, 2),
        "telhas": telhas,                       # shingle: fardos; concreto: telhas
        "cumeeira_m": cumeeira_m,
        "cumeeiras": cumeeiras,                 # shingle: fardos de 33,3 ft; concreto: peças
        "incluiu_manta": incluir_manta,
        "camadas_manta": camadas_manta,
        "manta_rolos": manta_rolos,
        "incluiu_osb": incluir_osb,
        "osb_chapas": osb_chapas,
        "perimetro_m": perimetro_m,
        "starter_fardos": starter_fardos,
        "pingadeira_pecas": pingadeira_pecas,
        "pregos": pregos,
        "pregos_caixas": pregos_caixas,
    }