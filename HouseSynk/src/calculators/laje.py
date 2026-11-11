import math
from src.calculators.tracos import consumo_concreto_por_m3, TRACO_CONCRETO_PADRAO
from src.calculators.unidades import IMPERIAL, M2_POR_SQFT
from src.calculators.brocas import embalagens_eua, JARDA_CUBICA_M3

# As mensagens de erro são CHAVES de texto (ex.: "erro_perda_negativa"): a tela mostra a frase
# no idioma escolhido com o txt() (os textos ficam no comum.py). Assim aqui só ficam as contas.

# Tipos de laje
TIPOS_LAJE = ["premoldada", "macica"]
TIPO_LAJE_PADRAO = "premoldada"

# Enchimento da laje pré-moldada treliçada
ENCHIMENTOS = ["eps", "lajota"]
ENCHIMENTO_PADRAO = "eps"

# Valores padrão
PERDA_PADRAO_LAJE = 5.0
CAPA_PADRAO_CM = 4.0

# Limites com aviso (regra 12): passar deles abre a janela "Confira os valores", com Continuar.
# Criados pelo Leo em Nov 3, 2026 (o engenheiro ainda vai conferir; se ele mudar, é só trocar aqui).
AREA_MAXIMA_LAJE_M2 = 2000.0
CAPA_MINIMA_CM = 3.0
CAPA_MAXIMA_CM = 8.0
ESPESSURA_MACICA_MINIMA_CM = 8.0
ESPESSURA_MACICA_MAXIMA_CM = 20.0

# Pré-moldada: concreto que entra entre as vigotas, além da capa (m³ por m² de laje)
# (CONFIRMADO pelo engenheiro em Oct 27, 2026; laje H12 = enchimento 8 cm + capa 4 cm)
CONCRETO_NERVURAS_M3_M2 = 0.012

# Lajotas cerâmicas por m² de laje (CONFIRMADO pelo engenheiro em Oct 27, 2026)
LAJOTAS_POR_M2 = 12

# Tela soldada na capa da laje pré-moldada (opcional). A família do engenheiro usa mais a tela;
# outros usam ferro. Vendida em painéis de 2 x 3 m (ex.: Malha POP Gerdau, tipos Leve ou Médio).
TELA_PAINEL_LARGURA_M = 2.0
TELA_PAINEL_COMPRIMENTO_M = 3.0
TELA_SOBREPOSICAO_PERCENTUAL = 10.0  # PROVISÓRIO: sobra para sobrepor os painéis (confirmar com o engenheiro)

# Preços PROVISÓRIOS (R$) até a tabela de preços ser refeita
# Laje pré-moldada vendida por m² (vigotas + enchimento)
PRECO_LAJE_PREMOLDADA_M2 = {"eps": 75.00, "lajota": 65.00}
PRECO_PAINEL_TELA = 95.00  # painel de tela soldada de 2 x 3 m


def calcular_laje(
    area_m2: float,
    tipo: str = TIPO_LAJE_PADRAO,
    enchimento: str = ENCHIMENTO_PADRAO,
    capa_cm: float = CAPA_PADRAO_CM,
    espessura_cm: float = 0.0,
    perda_percentual: float = PERDA_PADRAO_LAJE,
    traco: str = TRACO_CONCRETO_PADRAO,
    tela_soldada: bool = False,
) -> dict:
    if area_m2 <= 0:
        return {"erro": "erro_area_zero"}
    if tipo not in TIPOS_LAJE:
        return {"erro": "erro_tipo_laje_invalido"}
    if perda_percentual < 0:
        return {"erro": "erro_perda_negativa"}

    if tipo == "premoldada":
        if enchimento not in ENCHIMENTOS:
            return {"erro": "erro_enchimento_invalido"}
        if capa_cm <= 0:
            return {"erro": "erro_capa_zero"}
        volume = area_m2 * (capa_cm / 100.0 + CONCRETO_NERVURAS_M3_M2)
    else:
        if espessura_cm <= 0:
            return {"erro": "erro_espessura_macica"}
        volume = area_m2 * (espessura_cm / 100.0)

    consumo = consumo_concreto_por_m3(traco)
    if consumo is None:
        return {"erro": "erro_traco_concreto_invalido"}

    fator = 1 + perda_percentual / 100.0
    volume_com_perda = volume * fator

    premoldada = (tipo == "premoldada")
    lajotas = math.ceil(area_m2 * LAJOTAS_POR_M2 * fator - 1e-9) if premoldada and enchimento == "lajota" else 0

    # Tela soldada: só na capa da laje pré-moldada (a maciça leva armadura, que é projeto de engenheiro)
    incluiu_tela = premoldada and tela_soldada
    tela_m2 = area_m2 * (1 + TELA_SOBREPOSICAO_PERCENTUAL / 100.0) if incluiu_tela else 0.0
    area_painel_m2 = TELA_PAINEL_LARGURA_M * TELA_PAINEL_COMPRIMENTO_M
    tela_paineis = math.ceil(tela_m2 / area_painel_m2 - 1e-9) if incluiu_tela else 0

    return {
        "area_m2": round(area_m2, 2),
        "tipo": tipo,
        "enchimento": enchimento if premoldada else "",
        "capa_cm": capa_cm if premoldada else 0.0,
        "espessura_cm": espessura_cm if not premoldada else 0.0,
        "perda_percentual": perda_percentual,
        "traco": traco,
        "volume_m3": round(volume, 3),
        "volume_com_perda_m3": round(volume_com_perda, 3),
        "laje_premoldada_m2": round(area_m2, 2) if premoldada else 0.0,
        "lajotas": lajotas,
        "sacos_cimento": math.ceil(volume_com_perda * consumo["sacos_cimento"] - 1e-9),
        "areia_m3": round(volume_com_perda * consumo["areia_m3"], 2),
        "pedra_m3": round(volume_com_perda * consumo["pedra_m3"], 2),
        "incluiu_tela": incluiu_tela,
        "tela_m2": round(tela_m2, 2),
        "tela_paineis": tela_paineis,
    }


# ==========================================
# EUA (Parte A da versão EUA, Nov 9, 2026; pesquisa em claude/pesquisa_embalagens_eua.md)
# A laje pré-moldada com isopor/lajota não é usada na casa americana. Lá a "laje" é o piso de
# concreto feito direto no chão (slab-on-grade, código IRC R506): concreto, tela soldada,
# lona plástica por baixo e base de brita. A conta continua em métrico por dentro.
# ==========================================
TIPO_SLAB_EUA = "slab"

ESPESSURA_SLAB_PADRAO_CM = 4 * 2.54     # 4 in (o mais comum em casa; PROVISÓRIO, pesquisa ⚠️)
# Limites com aviso (regra 12), decididos pela Gabi em Nov 9, 2026:
ESPESSURA_SLAB_MINIMA_CM = 3.5 * 2.54   # 3 1/2 in: o mínimo do código IRC R506 (pesquisa ✅)
ESPESSURA_SLAB_MAXIMA_CM = 8 * 2.54     # 8 in: quase o máximo da laje maciça do Brasil (20 cm)

# Tela soldada (wire mesh 6x6 W1.4/W1.4): painel de 5 x 10 ft (50 sq ft), pesquisa ✅.
# Os mesmos 10% a mais para a sobreposição do Brasil (as calculadoras de lá também usam 10%; ⚠️).
TELA_PAINEL_EUA_M2 = 5 * 10 * M2_POR_SQFT

# Lona plástica por baixo (vapor retarder): o IRC exige, com emendas de 6 in (pesquisa ✅).
# Rolo de 10 x 100 ft (1.000 sq ft), o mais vendido na Home Depot em 6 mil e 10 mil.
LONA_ROLO_M2 = 10 * 100 * M2_POR_SQFT
LONA_SOBREPOSICAO_PERCENTUAL = 10.0     # emendas e as bordas que sobem na forma (PROVISÓRIO ⚠️)

# Base de brita embaixo da lona: 4 in (IRC R506, pesquisa ✅), com a mesma perda do concreto
BASE_BRITA_CM = 4 * 2.54

# Concreto usinado (o caminhão betoneira, "ready-mix"): pedido de 1/4 em 1/4 de cu yd (PROVISÓRIO ⚠️)
PASSO_CAMINHAO_CUYD = 0.25

# Preços PROVISÓRIOS ($) até a tabela de preços ser refeita
PRECO_PAINEL_TELA_EUA = 95.00   # o mesmo número do painel de 2 x 3 m do Brasil
PRECO_ROLO_LONA_EUA = 90.00     # rolo de 10 x 100 ft


def calcular_laje_eua(
    area_m2: float,
    espessura_cm: float = ESPESSURA_SLAB_PADRAO_CM,
    perda_percentual: float = PERDA_PADRAO_LAJE,
    traco: str = TRACO_CONCRETO_PADRAO,
    tela_soldada: bool = False,
    lona: bool = True,
    base_brita: bool = True,
) -> dict:
    """Piso de concreto no chão dos EUA (slab-on-grade). Recebe e devolve em métrico, mais as
    embalagens americanas: cimento em sacos de 94 lb, areia e brita em cu yd, concreto pronto
    em sacos de 80 lb, concreto usinado em cu yd, tela em painéis de 5 x 10 ft e lona em rolos."""
    if area_m2 <= 0:
        return {"erro": "erro_area_zero"}
    if espessura_cm <= 0:
        return {"erro": "erro_espessura_slab"}
    if perda_percentual < 0:
        return {"erro": "erro_perda_negativa"}

    consumo = consumo_concreto_por_m3(traco)
    if consumo is None:
        return {"erro": "erro_traco_concreto_invalido"}

    fator = 1 + perda_percentual / 100.0
    volume = area_m2 * (espessura_cm / 100.0)
    volume_com_perda = volume * fator

    # Embalagens do concreto: as mesmas das Brocas e do Baldrame (sem ferro, então o aço vai zero)
    emb = embalagens_eua(volume_com_perda, consumo, 0.0, 0.0, 0.0, 0.0)
    # Caminhão: o volume em cu yd, arredondado para cima de 1/4 em 1/4
    caminhao_cuyd = math.ceil(volume_com_perda / JARDA_CUBICA_M3 / PASSO_CAMINHAO_CUYD - 1e-9) * PASSO_CAMINHAO_CUYD

    tela_m2 = area_m2 * (1 + TELA_SOBREPOSICAO_PERCENTUAL / 100.0) if tela_soldada else 0.0
    tela_paineis = math.ceil(tela_m2 / TELA_PAINEL_EUA_M2 - 1e-9) if tela_soldada else 0

    lona_m2 = area_m2 * (1 + LONA_SOBREPOSICAO_PERCENTUAL / 100.0) if lona else 0.0
    lona_rolos = math.ceil(lona_m2 / LONA_ROLO_M2 - 1e-9) if lona else 0

    base_m3 = area_m2 * (BASE_BRITA_CM / 100.0) * fator if base_brita else 0.0

    return {
        "tipo": TIPO_SLAB_EUA,
        "sistema": IMPERIAL,
        "area_m2": area_m2,
        "espessura_cm": espessura_cm,
        "perda_percentual": perda_percentual,
        "traco": traco,
        "volume_m3": round(volume, 3),
        "volume_com_perda_m3": round(volume_com_perda, 3),
        "volume_com_perda_cuyd": emb["volume_com_perda_cuyd"],
        "sacos_cimento": emb["sacos_cimento"],                  # sacos de 94 lb
        "areia_m3": round(volume_com_perda * consumo["areia_m3"], 2),   # para o custo (preço por m³)
        "pedra_m3": round(volume_com_perda * consumo["pedra_m3"], 2),
        "areia_cuyd": emb["areia_cuyd"],
        "pedra_cuyd": emb["pedra_cuyd"],
        "sacos_concreto_pronto": emb["sacos_concreto_pronto"],  # alternativa: sacos de 80 lb
        "caminhao_cuyd": caminhao_cuyd,                         # alternativa: concreto usinado
        "incluiu_tela": tela_soldada,
        "tela_m2": tela_m2,
        "tela_paineis": tela_paineis,                           # painéis de 5 x 10 ft
        "incluiu_lona": lona,
        "lona_m2": lona_m2,
        "lona_rolos": lona_rolos,                               # rolos de 10 x 100 ft
        "incluiu_base": base_brita,
        "base_m3": round(base_m3, 3),
        "base_cuyd": round(base_m3 / JARDA_CUBICA_M3, 2),
    }