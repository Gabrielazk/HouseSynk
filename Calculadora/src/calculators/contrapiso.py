import math
from src.calculators.tracos import consumo_concreto_por_m3

# Perda padrão do contrapiso
PERDA_PADRAO_CONTRAPISO = 5.0

# Traço mais usado no contrapiso: 1 de cimento, 3 de areia e 3 de brita, com 5 a 7 cm de espessura
# (CONFIRMADO pelo engenheiro em Oct 27, 2026). As outras abas de concreto continuam com 1:2:3.
TRACO_PADRAO_CONTRAPISO = "1:3:3"


def calcular_contrapiso(
    area_m2: float,
    espessura_cm: float,
    perda_percentual: float = PERDA_PADRAO_CONTRAPISO,
    traco: str = TRACO_PADRAO_CONTRAPISO,
) -> dict:
    if area_m2 <= 0 or espessura_cm <= 0:
        return {"erro": "Área e espessura devem ser maiores que zero."}
    if perda_percentual < 0:
        return {"erro": "A perda não pode ser negativa."}

    consumo = consumo_concreto_por_m3(traco)
    if consumo is None:
        return {"erro": "Traço de concreto inválido."}

    volume = area_m2 * (espessura_cm / 100.0)
    volume_com_perda = volume * (1 + perda_percentual / 100.0)

    return {
        "area_m2": round(area_m2, 2),
        "espessura_cm": espessura_cm,
        "volume_m3": round(volume, 3),
        "volume_com_perda_m3": round(volume_com_perda, 3),
        "perda_percentual": perda_percentual,
        "traco": traco,
        "sacos_cimento": math.ceil(volume_com_perda * consumo["sacos_cimento"]),
        "areia_m3": round(volume_com_perda * consumo["areia_m3"], 2),
        "pedra_m3": round(volume_com_perda * consumo["pedra_m3"], 2),
    }