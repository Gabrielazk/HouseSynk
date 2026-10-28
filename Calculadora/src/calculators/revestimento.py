import math

# Perda de piso e azulejo (recortes e quebras) pelo tamanho da peça (CONFIRMADO pelo engenheiro em Oct 27, 2026).
# Vale o MAIOR lado da peça: até 70 cm, 10%; de 70 a 90 cm, 15%; acima de 90 cm, 20%.
# Assentamento com desenho (diagonal ou paginado): 25%, qualquer que seja o tamanho.
PERDA_PADRAO_REVESTIMENTO = 10.0          # peças até 70 cm (e o rodapé)
FAIXAS_PERDA = [(70.0, 10.0), (90.0, 15.0)]  # (maior lado até X cm, perda %)
PERDA_PECA_GRANDE = 20.0                  # maior lado acima de 90 cm
PERDA_COM_DESENHO = 25.0

# Argamassa colante (de saco): AC-I, AC-II e AC-III
TIPOS_ARGAMASSA = ["AC-I", "AC-II", "AC-III"]
ARGAMASSA_PADRAO_PISO = "AC-I"
ARGAMASSA_PADRAO_AZULEJO = "AC-II"  # AC-III para áreas molhadas (o cliente escolhe)
SACO_ARGAMASSA_KG = 20.0

# Consumo de argamassa colante: 3,5 kg/m² para qualquer tamanho de peça
# (CONFIRMADO pelo engenheiro em Oct 27, 2026; antes era 5 kg/m², ou 8 kg/m² para peças grandes)
CONSUMO_ARGAMASSA_KG_M2 = 3.5

# Preços PROVISÓRIOS (R$) até a tabela de preços ser refeita
PRECO_PISO_M2 = 50.00
PRECO_AZULEJO_M2 = 40.00
PRECO_RODAPE_M = 15.00
PRECO_ARGAMASSA_SACO = {"AC-I": 22.00, "AC-II": 30.00, "AC-III": 42.00}


def perda_automatica(largura_cm: float, altura_cm: float, desenho: bool = False) -> float:
    """Perda (%) pelo maior lado da peça, ou 25% se o assentamento tiver desenho."""
    if desenho:
        return PERDA_COM_DESENHO
    maior_lado = max(largura_cm, altura_cm)
    for limite_cm, perda in FAIXAS_PERDA:
        if maior_lado <= limite_cm:
            return perda
    return PERDA_PECA_GRANDE


def _calcular_ceramica(
    area_m2: float,
    largura_cm: float,
    altura_cm: float,
    desconto_vaos_m2: float,
    m2_por_caixa: float,
    tipo_argamassa: str,
    perda_percentual,
    desenho: bool,
    rodape_m: float,
    rodape_peca_m: float,
) -> dict:
    if area_m2 <= 0 or largura_cm <= 0 or altura_cm <= 0:
        return {"erro": "Área e tamanho da peça devem ser maiores que zero."}
    if desconto_vaos_m2 < 0 or m2_por_caixa < 0 or rodape_m < 0 or rodape_peca_m < 0:
        return {"erro": "Os valores não podem ser negativos."}
    if perda_percentual is not None and perda_percentual < 0:
        return {"erro": "A perda não pode ser negativa."}
    if desconto_vaos_m2 >= area_m2:
        return {"erro": "O desconto de vãos deve ser menor que a área."}
    if tipo_argamassa not in TIPOS_ARGAMASSA:
        return {"erro": "Tipo de argamassa inválido."}

    # Perda: a que o cliente digitou ou, se ficou vazia (None), a automática pelo tamanho da peça
    perda_auto = perda_percentual is None
    perda = perda_automatica(largura_cm, altura_cm, desenho) if perda_auto else perda_percentual

    area_liquida = area_m2 - desconto_vaos_m2
    fator = 1 + perda / 100.0
    area_com_perda = area_liquida * fator
    area_peca = (largura_cm / 100.0) * (altura_cm / 100.0)
    pecas = math.ceil(area_com_perda / area_peca - 1e-9)
    caixas = math.ceil(area_com_perda / m2_por_caixa - 1e-9) if m2_por_caixa > 0 else 0

    argamassa_kg = area_com_perda * CONSUMO_ARGAMASSA_KG_M2
    sacos = math.ceil(argamassa_kg / SACO_ARGAMASSA_KG - 1e-9)

    # Rodapé: perda de 10% (ou a que o cliente digitou). As peças só são contadas
    # se o cliente informar o tamanho da peça (varia de rodapé para rodapé).
    fator_rodape = 1 + (PERDA_PADRAO_REVESTIMENTO if perda_auto else perda) / 100.0
    rodape_com_perda = rodape_m * fator_rodape
    rodape_pecas = math.ceil(rodape_com_perda / rodape_peca_m - 1e-9) if rodape_m > 0 and rodape_peca_m > 0 else 0

    return {
        "area_bruta_m2": round(area_m2, 2),
        "desconto_vaos_m2": round(desconto_vaos_m2, 2),
        "area_liquida_m2": round(area_liquida, 2),
        "area_com_perda_m2": round(area_com_perda, 2),
        "perda_percentual": perda,
        "perda_automatica": perda_auto,
        "desenho": desenho,
        "largura_cm": largura_cm,
        "altura_cm": altura_cm,
        "pecas": pecas,
        "m2_por_caixa": m2_por_caixa,
        "caixas": caixas,
        "tipo_argamassa": tipo_argamassa,
        "argamassa_kg": round(argamassa_kg, 1),
        "sacos_argamassa": sacos,
        "rodape_m": round(rodape_com_perda, 2),
        "rodape_peca_m": rodape_peca_m,
        "rodape_pecas": rodape_pecas,
    }


def calcular_piso(
    area_m2: float,
    largura_cm: float,
    altura_cm: float,
    m2_por_caixa: float = 0.0,
    tipo_argamassa: str = ARGAMASSA_PADRAO_PISO,
    perda_percentual=None,
    rodape_m: float = 0.0,
    desenho: bool = False,
    rodape_peca_m: float = 0.0,
) -> dict:
    """perda_percentual=None: perda automática pelo tamanho da peça."""
    return _calcular_ceramica(area_m2, largura_cm, altura_cm, 0.0, m2_por_caixa,
                              tipo_argamassa, perda_percentual, desenho, rodape_m, rodape_peca_m)


def calcular_azulejo(
    area_parede_m2: float,
    largura_cm: float,
    altura_cm: float,
    desconto_vaos_m2: float = 0.0,
    m2_por_caixa: float = 0.0,
    tipo_argamassa: str = ARGAMASSA_PADRAO_AZULEJO,
    perda_percentual=None,
    desenho: bool = False,
) -> dict:
    """perda_percentual=None: perda automática pelo tamanho da peça."""
    return _calcular_ceramica(area_parede_m2, largura_cm, altura_cm, desconto_vaos_m2, m2_por_caixa,
                              tipo_argamassa, perda_percentual, desenho, 0.0, 0.0)