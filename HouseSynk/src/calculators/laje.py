import math
from src.calculators.tracos import consumo_concreto_por_m3, TRACO_CONCRETO_PADRAO

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