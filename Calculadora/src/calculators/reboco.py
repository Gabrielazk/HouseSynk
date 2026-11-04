import math
from src.calculators.tracos import (
    TRACOS_MASSA,
    TRACO_MASSA_PADRAO,
    SACO_CIMENTO_KG,
    SACO_CAL_KG,
    materiais_da_massa,
)

# As mensagens de erro são CHAVES de texto (ex.: "erro_perda_negativa"): a tela mostra a frase
# no idioma escolhido com o txt() (os textos ficam no comum.py). Assim aqui só ficam as contas.

ESPESSURA_PADRAO_CM = 2.0
PERDA_PADRAO_REBOCO = 10.0

# Limites com aviso (regra 12): passar deles abre a janela "Confira os valores", com Continuar.
# Criados pelo Leo em Nov 3, 2026 (o engenheiro ainda vai conferir; se ele mudar, é só trocar aqui).
AREA_MAXIMA_REBOCO_M2 = 2000.0
ESPESSURA_MINIMA_CM = 0.5   # o normal é 2 cm
ESPESSURA_MAXIMA_CM = 4.0

# Chapisco (premissas de trabalho, a conferir): camada fina de cimento e areia 1:3
CHAPISCO_TRACO = "1:0:3"          # cimento : cal : areia  (1:3 de cimento e areia, sem cal)
CHAPISCO_ESPESSURA_CM = 0.5
CHAPISCO_TRACO_RODAPE = "1:3"     # como aparece para o cliente


def calcular_reboco(
    area_bruta_m2: float,
    espessura_cm: float = ESPESSURA_PADRAO_CM,
    desconto_vaos_m2: float = 0.0,
    dois_lados: bool = False,
    chapisco: bool = False,
    perda_percentual: float = PERDA_PADRAO_REBOCO,
    traco: str = TRACO_MASSA_PADRAO,
) -> dict:
    if area_bruta_m2 <= 0 or espessura_cm <= 0:
        return {"erro": "erro_area_espessura_zero"}
    if desconto_vaos_m2 < 0 or perda_percentual < 0:
        return {"erro": "erro_desconto_perda_negativos"}
    if traco not in TRACOS_MASSA:
        return {"erro": "erro_traco_massa_invalido"}

    area_liquida_m2 = area_bruta_m2 - desconto_vaos_m2
    if area_liquida_m2 <= 0:
        return {"erro": "erro_desconto_vaos"}

    area_rebocada_m2 = area_liquida_m2 * (2 if dois_lados else 1)
    fator_perda = 1 + perda_percentual / 100.0

    volume_reboco_m3 = area_rebocada_m2 * (espessura_cm / 100.0) * fator_perda
    materiais = materiais_da_massa(volume_reboco_m3, traco)
    cimento_kg = materiais["cimento_kg"]
    cal_kg = materiais["cal_kg"]
    areia_m3 = materiais["areia_m3"]

    volume_chapisco_m3 = 0.0
    if chapisco:
        volume_chapisco_m3 = area_rebocada_m2 * (CHAPISCO_ESPESSURA_CM / 100.0) * fator_perda
        mat_chap = materiais_da_massa(volume_chapisco_m3, CHAPISCO_TRACO)
        cimento_kg += mat_chap["cimento_kg"]
        cal_kg += mat_chap["cal_kg"]
        areia_m3 += mat_chap["areia_m3"]

    return {
        "area_bruta_m2": round(area_bruta_m2, 2),
        "desconto_vaos_m2": round(desconto_vaos_m2, 2),
        "area_liquida_m2": round(area_liquida_m2, 2),
        "dois_lados": dois_lados,
        "area_rebocada_m2": round(area_rebocada_m2, 2),
        "espessura_cm": espessura_cm,
        "perda_percentual": perda_percentual,
        "traco": traco,
        "volume_reboco_m3": round(volume_reboco_m3, 3),
        "chapisco": chapisco,
        "volume_chapisco_m3": round(volume_chapisco_m3, 3),
        "sacos_cimento": math.ceil(cimento_kg / SACO_CIMENTO_KG),
        "sacos_cal": math.ceil(cal_kg / SACO_CAL_KG),
        "areia_m3": round(areia_m3, 2),
    }