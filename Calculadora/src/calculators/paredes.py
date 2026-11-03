import math
from src.calculators.tracos import (
    TRACOS_MASSA,
    TRACO_MASSA_PADRAO,
    SACO_CIMENTO_KG,
    SACO_CAL_KG,
    materiais_da_massa,
)
from src.calculators.unidades import arredondar  # arredonda certo (1,575 -> 1,58)

# Tijolos e blocos: medidas em cm, na ordem do nome (largura x altura x comprimento).
# ATENÇÃO (conferir com engenheiro): medidas e preços são premissas de trabalho.
# O preço aqui é PROVISÓRIO: vai para a tabela de preços (por país e estado) na etapa de preços.
TIJOLOS = {
    "baiano":      {"largura": 9.0,  "altura": 19.0, "comprimento": 19.0, "preco": 1.20},
    "baiano_9f":   {"largura": 9.0,  "altura": 14.0, "comprimento": 19.0, "preco": 1.00},
    "bloco_9":     {"largura": 9.0,  "altura": 19.0, "comprimento": 39.0, "preco": 3.00},
    "bloco_14":    {"largura": 14.0, "altura": 19.0, "comprimento": 39.0, "preco": 4.50},
    "bloco_19":    {"largura": 19.0, "altura": 19.0, "comprimento": 39.0, "preco": 6.00},
}
TIJOLO_PADRAO = "baiano"

# Assentamento: qual lado do tijolo fica como espessura da parede.
#   em pé:   aparece o comprimento x a altura; a espessura da parede é a largura
#   deitado: aparece o comprimento x a largura; a espessura da parede é a altura
ASSENTAMENTOS = ["em_pe", "deitado"]
ASSENTAMENTO_PADRAO = "em_pe"

JUNTA_PADRAO_CM = 1.0
QUEBRA_PADRAO_PERCENTUAL = 5.0

# Perda da massa de assentar (decidido pela Gabriela em Oct 29, 2026: 10%, igual ao reboco).
# Não é um campo da tela: entra sempre, igual à perda do ferro nas Brocas.
PERDA_MASSA_PERCENTUAL = 10.0

# Limites de conferência (criados pelo Leo em Oct 29, 2026; o engenheiro não tinha um número).
# Passar deles NÃO impede a conta: a tela mostra um aviso e pergunta se a pessoa quer continuar.
AREA_MAXIMA_M2 = 2000.0           # uma casa grande fica bem abaixo disso
JUNTA_MINIMA_CM = 0.5             # junta normal: de 0,5 a 3 cm
JUNTA_MAXIMA_CM = 3.0
QUEBRA_MAXIMA_PERCENTUAL = 20.0


def calcular_paredes(
    area_bruta_m2: float,
    tijolo: str = TIJOLO_PADRAO,
    assentamento: str = ASSENTAMENTO_PADRAO,
    desconto_vaos_m2: float = 0.0,
    junta_cm: float = JUNTA_PADRAO_CM,
    quebra_percentual: float = QUEBRA_PADRAO_PERCENTUAL,
    traco: str = TRACO_MASSA_PADRAO,
) -> dict:
    if area_bruta_m2 <= 0:
        return {"erro": "A área da parede deve ser maior que zero."}
    if desconto_vaos_m2 < 0 or junta_cm < 0 or quebra_percentual < 0:
        return {"erro": "Desconto, junta e quebra não podem ser negativos."}
    if tijolo not in TIJOLOS:
        return {"erro": "Tipo de tijolo ou bloco inválido."}
    if assentamento not in ASSENTAMENTOS:
        return {"erro": "Assentamento inválido."}
    if traco not in TRACOS_MASSA:
        return {"erro": "Traço da massa inválido."}

    area_liquida_m2 = area_bruta_m2 - desconto_vaos_m2
    if area_liquida_m2 <= 0:
        return {"erro": "O desconto de portas e janelas não pode ser maior que a área da parede."}

    dados = TIJOLOS[tijolo]
    if assentamento == "em_pe":
        face_comprimento_cm = dados["comprimento"]
        face_altura_cm = dados["altura"]
        espessura_cm = dados["largura"]
    else:
        face_comprimento_cm = dados["comprimento"]
        face_altura_cm = dados["largura"]
        espessura_cm = dados["altura"]

    # Quantas peças cabem em 1 m2 (a junta entra na medida de cada peça)
    peca_com_junta_m2 = ((face_comprimento_cm + junta_cm) / 100.0) * ((face_altura_cm + junta_cm) / 100.0)
    pecas_por_m2 = 1.0 / peca_com_junta_m2
    unidades = math.ceil(area_liquida_m2 * pecas_por_m2 * (1 + quebra_percentual / 100.0))
    milheiros = unidades / 1000.0

    # Volume de massa = o que sobra na parede depois de tirar o volume dos tijolos, mais a perda da massa
    area_face_peca_m2 = (face_comprimento_cm / 100.0) * (face_altura_cm / 100.0)
    massa_por_m2_m3 = (espessura_cm / 100.0) * (1.0 - pecas_por_m2 * area_face_peca_m2)
    volume_massa_m3 = massa_por_m2_m3 * area_liquida_m2 * (1 + PERDA_MASSA_PERCENTUAL / 100.0)

    # Mesma conta da massa do Reboco (fica no tracos.py, com o inchamento da areia)
    materiais = materiais_da_massa(volume_massa_m3, traco)
    sacos_cimento = math.ceil(materiais["cimento_kg"] / SACO_CIMENTO_KG - 1e-9)
    sacos_cal = math.ceil(materiais["cal_kg"] / SACO_CAL_KG - 1e-9)
    areia_m3 = arredondar(materiais["areia_m3"], 2)

    return {
        "area_bruta_m2": arredondar(area_bruta_m2, 2),
        "desconto_vaos_m2": arredondar(desconto_vaos_m2, 2),
        "area_liquida_m2": arredondar(area_liquida_m2, 2),
        "tijolo": tijolo,
        "assentamento": assentamento,
        "junta_cm": junta_cm,
        "quebra_percentual": quebra_percentual,
        "pecas_por_m2": arredondar(pecas_por_m2, 2),
        "unidades": unidades,
        "milheiros": arredondar(milheiros, 2),
        "preco_unitario": dados["preco"],
        "traco": traco,
        "perda_massa_percentual": PERDA_MASSA_PERCENTUAL,
        "volume_massa_m3": arredondar(volume_massa_m3, 3),
        "sacos_cimento": sacos_cimento,
        "sacos_cal": sacos_cal,
        "areia_m3": areia_m3,
    }