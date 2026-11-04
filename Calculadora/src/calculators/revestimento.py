import math
from src.calculators.unidades import METRICO, IMPERIAL, KG_POR_LB, M2_POR_SQFT
from src.calculators.unidades import arredondar  # arredonda certo (1,575 -> 1,58)

# Perda de piso e azulejo (recortes e quebras) pelo tamanho da peça (CONFIRMADO pelo engenheiro em Oct 27, 2026).
# Vale o MAIOR lado da peça: até 70 cm, 10%; de 70 a 90 cm, 15%; acima de 90 cm, 20%.
# Assentamento com desenho (diagonal ou paginado): 25%, qualquer que seja o tamanho.
PERDA_PADRAO_REVESTIMENTO = 10.0          # peças até 70 cm (e o rodapé)
FAIXAS_PERDA = [(70.0, 10.0), (90.0, 15.0)]  # (maior lado até X cm, perda %)
PERDA_PECA_GRANDE = 20.0                  # maior lado acima de 90 cm
PERDA_COM_DESENHO = 25.0

# Limites com aviso (regra 12): passar deles abre a janela "Confira os valores", com Continuar.
# Criados pelo Leo em Nov 3, 2026 (o engenheiro ainda vai conferir; se ele mudar, é só trocar aqui).
# Valem para o Piso e para o Azulejo. Peça: cada lado (existe porcelanato de 120 x 240 cm).
AREA_MAXIMA_REVESTIMENTO_M2 = 2000.0
PECA_MINIMA_CM = 5.0
PECA_MAXIMA_CM = 300.0

# --- BRASIL: argamassa colante (de saco): AC-I, AC-II e AC-III ---
TIPOS_ARGAMASSA = ["AC-I", "AC-II", "AC-III"]
ARGAMASSA_PADRAO_PISO = "AC-I"
ARGAMASSA_PADRAO_AZULEJO = "AC-II"  # AC-III para áreas molhadas (o cliente escolhe)
SACO_ARGAMASSA_KG = 20.0

# Consumo de argamassa colante (números dos fabricantes; o engenheiro aprovou em Oct 29, 2026):
# 5 kg/m² na peça normal e 8 kg/m² na peça grande, que leva dupla colagem (argamassa na peça e no chão).
# Peça grande: maior lado acima de 60 cm (a confirmar com o engenheiro).
CONSUMO_ARGAMASSA_KG_M2 = 5.0
CONSUMO_ARGAMASSA_PECA_GRANDE_KG_M2 = 8.0
LADO_PECA_GRANDE_CM = 60.0

# --- EUA: argamassa colante (thinset) em saco de 50 lb ---
# Tipos pela norma americana (ANSI): A118.1 = não modificada; A118.4 = modificada com polímero.
TIPOS_ARGAMASSA_EUA = ["A118.1", "A118.4"]
ARGAMASSA_PADRAO_PISO_EUA = "A118.1"      # a mais simples, como o AC-I no Brasil
ARGAMASSA_PADRAO_AZULEJO_EUA = "A118.4"   # modificada, como o AC-II no Brasil
SACO_ARGAMASSA_EUA_KG = 50 * KG_POR_LB    # 22,68 kg

# Nos EUA, o consumo vem do rendimento do saco de 50 lb informado pelo fabricante, que depende
# da desempenadeira (e a desempenadeira, do tamanho da peça). O app usa o MENOR rendimento da faixa
# (sobra um pouco, nunca falta):
# - maior lado até 8 in: desempenadeira 1/4 x 1/4 in, 85 sq ft por saco (Custom: 85 a 95)
# - até 16 in: desempenadeira 1/4 x 3/8 in, 60 sq ft por saco (Custom: 60 a 67; Mapei: 60 a 80)
# - acima de 16 in: desempenadeira 1/2 x 1/2 in, 40 sq ft por saco (Mapei: 40 a 50)
#   (PROVISÓRIO para peças de 16 a 24 in: alguns guias indicam a de 3/8 x 3/8 in, sem rendimento
#   publicado; o app usa a de 1/2 x 1/2 in, que gasta mais argamassa)
FAIXAS_DESEMPENADEIRA_EUA = [(8 * 2.54, "1/4 x 1/4", 85.0), (16 * 2.54, "1/4 x 3/8", 60.0)]
DESEMPENADEIRA_GRANDE_EUA = ("1/2 x 1/2", 40.0)

# Preços PROVISÓRIOS até a tabela de preços ser refeita
PRECO_PISO_M2 = 50.00
PRECO_AZULEJO_M2 = 40.00
PRECO_RODAPE_M = 15.00
PRECO_ARGAMASSA_SACO = {"AC-I": 22.00, "AC-II": 30.00, "AC-III": 42.00}  # R$ por saco de 20 kg
# $ por saco de 50 lb. A118.4: VersaBond 50 lb a $17.98 (Home Depot, pesquisa de Oct 28, 2026).
# A118.1: sem preço na pesquisa; usa o número do AC-I do Brasil, em dólar.
PRECO_ARGAMASSA_SACO_EUA = {"A118.1": 22.00, "A118.4": 17.98}


def tipos_argamassa(sistema: str = METRICO):
    """Lista de tipos de argamassa colante do país."""
    return TIPOS_ARGAMASSA_EUA if sistema == IMPERIAL else TIPOS_ARGAMASSA


def argamassa_padrao(piso: bool, sistema: str = METRICO) -> str:
    """Tipo de argamassa que já vem escolhido no Piso e no Azulejo."""
    if sistema == IMPERIAL:
        return ARGAMASSA_PADRAO_PISO_EUA if piso else ARGAMASSA_PADRAO_AZULEJO_EUA
    return ARGAMASSA_PADRAO_PISO if piso else ARGAMASSA_PADRAO_AZULEJO


def desempenadeira_eua(largura_cm: float, altura_cm: float):
    """EUA: (desempenadeira, sq ft por saco de 50 lb) pelo maior lado da peça."""
    maior_lado = max(largura_cm, altura_cm)
    for limite_cm, desempenadeira, rendimento in FAIXAS_DESEMPENADEIRA_EUA:
        if maior_lado <= limite_cm + 1e-6:
            return desempenadeira, rendimento
    return DESEMPENADEIRA_GRANDE_EUA


def consumo_argamassa_kg_m2(largura_cm: float, altura_cm: float) -> float:
    """Brasil: kg de argamassa colante por m². Peça com o maior lado acima de 60 cm leva dupla colagem."""
    if max(largura_cm, altura_cm) > LADO_PECA_GRANDE_CM:
        return CONSUMO_ARGAMASSA_PECA_GRANDE_KG_M2
    return CONSUMO_ARGAMASSA_KG_M2


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
    sistema: str = METRICO,
) -> dict:
    if area_m2 <= 0 or largura_cm <= 0 or altura_cm <= 0:
        return {"erro": "Área e tamanho da peça devem ser maiores que zero."}
    if desconto_vaos_m2 < 0 or m2_por_caixa < 0 or rodape_m < 0 or rodape_peca_m < 0:
        return {"erro": "Os valores não podem ser negativos."}
    if perda_percentual is not None and perda_percentual < 0:
        return {"erro": "A perda não pode ser negativa."}
    if desconto_vaos_m2 >= area_m2:
        return {"erro": "O desconto de vãos deve ser menor que a área."}
    if tipo_argamassa not in tipos_argamassa(sistema):
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

    # Argamassa colante: Brasil 3,5 kg/m² em sacos de 20 kg; EUA pelo rendimento do saco de 50 lb
    desempenadeira = ""
    if sistema == IMPERIAL:
        desempenadeira, sqft_por_saco = desempenadeira_eua(largura_cm, altura_cm)
        saco_kg = SACO_ARGAMASSA_EUA_KG
        consumo_kg_m2 = saco_kg / (sqft_por_saco * M2_POR_SQFT)
    else:
        saco_kg = SACO_ARGAMASSA_KG
        consumo_kg_m2 = consumo_argamassa_kg_m2(largura_cm, altura_cm)
    argamassa_kg = area_com_perda * consumo_kg_m2
    sacos = math.ceil(argamassa_kg / saco_kg - 1e-9)

    # Rodapé: perda de 10% (ou a que o cliente digitou). As peças só são contadas
    # se o cliente informar o tamanho da peça (varia de rodapé para rodapé).
    fator_rodape = 1 + (PERDA_PADRAO_REVESTIMENTO if perda_auto else perda) / 100.0
    rodape_com_perda = rodape_m * fator_rodape
    rodape_pecas = math.ceil(rodape_com_perda / rodape_peca_m - 1e-9) if rodape_m > 0 and rodape_peca_m > 0 else 0

    return {
        "area_bruta_m2": arredondar(area_m2, 2),
        "desconto_vaos_m2": arredondar(desconto_vaos_m2, 2),
        "area_liquida_m2": arredondar(area_liquida, 2),
        "area_com_perda_m2": arredondar(area_com_perda, 2),
        "perda_percentual": perda,
        "perda_automatica": perda_auto,
        "desenho": desenho,
        "largura_cm": largura_cm,
        "altura_cm": altura_cm,
        "pecas": pecas,
        "m2_por_caixa": m2_por_caixa,
        "caixas": caixas,
        "tipo_argamassa": tipo_argamassa,
        "argamassa_kg": arredondar(argamassa_kg, 1),
        "sacos_argamassa": sacos,
        "consumo_argamassa_kg_m2": arredondar(consumo_kg_m2, 3),
        "desempenadeira": desempenadeira,   # só nos EUA (ex.: "1/4 x 3/8"); vazio no Brasil
        "rodape_m": arredondar(rodape_com_perda, 2),
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
    sistema: str = METRICO,
) -> dict:
    """perda_percentual=None: perda automática pelo tamanho da peça."""
    return _calcular_ceramica(area_m2, largura_cm, altura_cm, 0.0, m2_por_caixa,
                              tipo_argamassa, perda_percentual, desenho, rodape_m, rodape_peca_m, sistema)


def calcular_azulejo(
    area_parede_m2: float,
    largura_cm: float,
    altura_cm: float,
    desconto_vaos_m2: float = 0.0,
    m2_por_caixa: float = 0.0,
    tipo_argamassa: str = ARGAMASSA_PADRAO_AZULEJO,
    perda_percentual=None,
    desenho: bool = False,
    sistema: str = METRICO,
) -> dict:
    """perda_percentual=None: perda automática pelo tamanho da peça."""
    return _calcular_ceramica(area_parede_m2, largura_cm, altura_cm, desconto_vaos_m2, m2_por_caixa,
                              tipo_argamassa, perda_percentual, desenho, 0.0, 0.0, sistema)