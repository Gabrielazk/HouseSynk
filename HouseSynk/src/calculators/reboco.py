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

# ==========================================
# EUA (Parte A da versão EUA, Nov 13, 2026): o reboco vira o STUCCO, só na parede de fora
# (por dentro, a casa americana usa drywall: Parte B). Pesquisa em claude/pesquisa_embalagens_eua.md, item 9.
# Decisões da Gabi (Nov 13, 2026): menu "Parede de" madeira ou bloco/concreto, e o stucco pronto em
# sacos de 80 lb (base coat + finish coat), igual à massa pronta das Paredes dos EUA. Sem traço,
# sem chapisco e sem "dois lados": a espessura vem do sistema de demãos.
# Código IRC (R703.7 e Tabela R702.1): sobre madeira, 3 demãos sobre tela metálica (3/8 + 3/8 + 1/8 in
# = 7/8 in) e papel em 2 camadas (Grade D) por baixo; sobre bloco ou concreto, 2 demãos
# (3/8 + 1/8 in = 1/2 in), sem tela e sem papel. A conta continua em métrico por dentro.
# ==========================================
PE2_M2 = 0.09290304          # 1 sq ft em m²
POL2_M2 = 0.00064516         # 1 in² em m²

PAREDES_STUCCO = ["madeira", "bloco"]
PAREDE_STUCCO_PADRAO = "madeira"             # a casa mais comum de stucco nos EUA (estrutura de madeira com OSB)
DEMAOS_BASE_STUCCO = {"madeira": 2, "bloco": 1}  # demãos de base coat de 3/8 in (scratch e brown; no bloco, só uma)

# Embalagens e rendimentos (pesquisa ✅)
COBERTURA_BASE_M2 = 20 * PE2_M2          # base coat 80 lb: 20 a 24 sq ft por saco a 3/8 in (Quikrete); o menor, para não faltar
COBERTURA_ACABAMENTO_M2 = 70 * PE2_M2    # finish coat 80 lb: 70 sq ft por saco a 1/8 in (Quikrete)
# Tela metálica 2.5 lb em folhas de 27 x 96 in, com 1/2 in de sobreposição do lado e 1 in na ponta (IRC)
FOLHA_TELA_UTIL_M2 = (27 - 0.5) * (96 - 1) * POL2_M2
# Papel de 2 camadas (60 minutos, Grade D) em rolos de 162 sq ft (40 in de largura); emenda de 2 in
# na horizontal, então cada rolo cobre 38 de cada 40 in
ROLO_PAPEL_UTIL_M2 = 162 * PE2_M2 * 38 / 40

# Preços PROVISÓRIOS ($) até a tabela de preços ser refeita
PRECO_SACO_BASE_STUCCO = 15.00
PRECO_SACO_ACABAMENTO_STUCCO = 25.00
PRECO_FOLHA_TELA_STUCCO = 20.00
PRECO_ROLO_PAPEL_STUCCO = 25.00


def calcular_reboco_eua(
    area_bruta_m2: float,
    desconto_vaos_m2: float = 0.0,
    parede: str = PAREDE_STUCCO_PADRAO,
    perda_percentual: float = PERDA_PADRAO_REBOCO,
) -> dict:
    """Stucco dos EUA. parede: "madeira" (3 demãos, tela e papel) ou "bloco" (2 demãos).
    Recebe e devolve em métrico (a tela converte)."""
    if area_bruta_m2 <= 0:
        return {"erro": "erro_area_zero_stucco"}
    if desconto_vaos_m2 < 0 or perda_percentual < 0:
        return {"erro": "erro_desconto_perda_negativos"}
    if parede not in PAREDES_STUCCO:
        parede = PAREDE_STUCCO_PADRAO

    area_liquida_m2 = area_bruta_m2 - desconto_vaos_m2
    if area_liquida_m2 <= 0:
        return {"erro": "erro_desconto_vaos"}

    area_com_perda = area_liquida_m2 * (1 + perda_percentual / 100.0)
    demaos_base = DEMAOS_BASE_STUCCO[parede]
    madeira = (parede == "madeira")
    return {
        "area_bruta_m2": area_bruta_m2,
        "desconto_vaos_m2": desconto_vaos_m2,
        "area_liquida_m2": area_liquida_m2,
        "parede": parede,
        "demaos_base": demaos_base,
        "perda_percentual": perda_percentual,
        "sacos_base": math.ceil(area_com_perda * demaos_base / COBERTURA_BASE_M2 - 1e-9),
        "sacos_acabamento": math.ceil(area_com_perda / COBERTURA_ACABAMENTO_M2 - 1e-9),
        "folhas_tela": math.ceil(area_com_perda / FOLHA_TELA_UTIL_M2 - 1e-9) if madeira else 0,
        "rolos_papel": math.ceil(area_com_perda / ROLO_PAPEL_UTIL_M2 - 1e-9) if madeira else 0,
    }