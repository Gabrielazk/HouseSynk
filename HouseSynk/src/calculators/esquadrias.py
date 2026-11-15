import math

from src.calculators.unidades import IMPERIAL

# As mensagens de erro são CHAVES de texto (ex.: "erro_perda_negativa"): a tela mostra a frase
# no idioma escolhido com o txt() (os textos ficam no comum.py). Assim aqui só ficam as contas.

# Tipos e materiais (o material é só informação para a cotação, não muda a conta)
TIPOS_ESQUADRIA = ["porta", "janela"]
TIPO_ESQUADRIA_PADRAO = "porta"
MATERIAIS = ["nao_informado", "aluminio", "madeira", "vidro"]
MATERIAL_PADRAO = "nao_informado"

# Limites com aviso (regra 12): passar deles abre a janela "Confira os valores", com Continuar.
# Criados pelo Leo em Nov 3, 2026 (o engenheiro ainda vai conferir; se ele mudar, é só trocar aqui).
# O aviso aparece no "Adicionar à lista" (antes de o item entrar na lista).
QUANTIDADE_MAXIMA = 100
LARGURA_MAXIMA_CM = 500.0
ALTURA_MAXIMA_CM = 400.0  # 8000 é quase certeza de quem digitou em mm

# Insumos de fixação, calculados pelo perímetro das esquadrias (PROVISÓRIO, confirmar com o engenheiro)
# Porta: os dois lados + a parte de cima (embaixo é o piso). Janela: os quatro lados.
METROS_POR_TUBO_ESPUMA = 6.0       # 1 tubo de espuma expansiva (500 ml) a cada 6 m de perímetro
METROS_POR_PARAFUSO = 0.4          # 1 parafuso com bucha a cada 40 cm de perímetro
ARGAMASSA_FIXACAO_KG_M = 1.5       # kg de argamassa por metro de perímetro
SACO_ARGAMASSA_FIXACAO_KG = 20.0

# Preços PROVISÓRIOS (R$) até a tabela de preços ser refeita
PRECO_TUBO_ESPUMA = 35.00
PRECO_PARAFUSO = 0.80
PRECO_SACO_ARGAMASSA_FIXACAO = 25.00


# --- EUA (Parte A, Nov 13, 2026; decisões da Gabi) ---
# Na casa de madeira dos EUA a janela é pregada pela aba (nailing flange) e a argamassa não se usa.
# Material: a lista americana (lá a janela mais comum é de vinil; aço é comum na porta de entrada).
MATERIAIS_EUA = ["nao_informado", "vinil", "madeira", "aluminio", "fibra", "aco"]
# Todos os materiais (um item feito num país continua válido no outro; o material é só informação)
TODOS_MATERIAIS = MATERIAIS + [m for m in MATERIAIS_EUA if m not in MATERIAIS]

# Insumos de fixação dos EUA, também pelo contorno dos vãos (o mesmo do Brasil):
# - Espuma de baixa expansão (window & door) em latas de 12 oz: 1 lata enche de 4 a 6 janelas de
#   36 x 60 in (Great Stuff ✅); o app usa 4 (o menor, para não faltar) = 4 x 16 ft = 64 ft de contorno.
PES_POR_LATA_ESPUMA_EUA = 64.0
METROS_POR_LATA_ESPUMA_EUA = PES_POR_LATA_ESPUMA_EUA * 0.3048
# - Pregos galvanizados de 2 in pela aba, a cada 8 in (instrução de instalação da Home Depot: 8 in ou
#   um furo sim e outro não ✅; outros fabricantes pedem a cada 12 in, então sobra em vez de faltar).
#   Caixa de 1 lb com cerca de 138 pregos (Grip-Rite 2 in ✅). PROVISÓRIO na porta (ela varia mais).
METROS_POR_PREGO_EUA = 8 * 0.0254
PREGOS_POR_CAIXA_EUA = 138
# - Fita de flashing de 4 in em rolos de 75 ft (3M, DuPont, Andersen ✅), no contorno do vão,
#   com 4 in a mais em cada canto para a sobreposição (janela: 4 cantos; porta: os 2 de cima).
#   PROVISÓRIO ⚠️ (a sobreposição é regra prática).
FITA_SOBRA_POR_CANTO_M = 4 * 0.0254
ROLO_FITA_EUA_M = 75 * 0.3048
CANTOS_POR_TIPO = {"porta": 2, "janela": 4}

# Preços PROVISÓRIOS ($) até a tabela de preços (números de loja, Home Depot e Ace, nov/2026)
PRECO_LATA_ESPUMA_EUA = 6.00
PRECO_CAIXA_PREGOS_EUA = 6.00
PRECO_ROLO_FITA_EUA = 40.00


def materiais_do_pais(sistema=None):
    """(materiais, padrão) do país: a lista do Brasil ou a americana (sistema = IMPERIAL)."""
    return (MATERIAIS_EUA if sistema == IMPERIAL else MATERIAIS), MATERIAL_PADRAO


def perimetro_m(tipo: str, largura_cm: float, altura_cm: float) -> float:
    larg, alt = largura_cm / 100.0, altura_cm / 100.0
    return 2 * alt + larg if tipo == "porta" else 2 * (larg + alt)


def _conferir_itens(itens):
    """Mesmas conferências nos dois países. Retorna a chave do erro ou None."""
    if not itens:
        return "erro_lista_esquadrias_vazia"
    for item in itens:
        if item.get("tipo") not in TIPOS_ESQUADRIA or item.get("material") not in TODOS_MATERIAIS:
            return "erro_tipo_material_invalido"
        if item.get("qtd", 0) <= 0 or item.get("larg", 0) <= 0 or item.get("alt", 0) <= 0:
            return "erro_qtd_larg_alt_zero"
    return None


def calcular_esquadrias_eua(
    itens: list,
    espuma: bool = False,
    pregos: bool = False,
    fita: bool = False,
) -> dict:
    """Esquadrias nos EUA. itens: a mesma lista do Brasil (medidas sempre em cm).
    Insumos: espuma em latas de 12 oz, pregos de 2 in em caixas de 1 lb e fita de flashing
    de 4 in em rolos de 75 ft (sem argamassa)."""
    erro = _conferir_itens(itens)
    if erro:
        return {"erro": erro}

    totais = {"porta": 0, "janela": 0}
    area_total = 0.0
    perimetro_total = 0.0
    fita_total = 0.0
    for item in itens:
        totais[item["tipo"]] += item["qtd"]
        area_total += item["qtd"] * (item["larg"] / 100.0) * (item["alt"] / 100.0)
        perimetro = perimetro_m(item["tipo"], item["larg"], item["alt"])
        perimetro_total += item["qtd"] * perimetro
        fita_total += item["qtd"] * (perimetro + CANTOS_POR_TIPO[item["tipo"]] * FITA_SOBRA_POR_CANTO_M)

    latas = math.ceil(perimetro_total / METROS_POR_LATA_ESPUMA_EUA - 1e-9) if espuma else 0
    qtd_pregos = math.ceil(perimetro_total / METROS_POR_PREGO_EUA - 1e-9) if pregos else 0
    caixas = math.ceil(qtd_pregos / PREGOS_POR_CAIXA_EUA - 1e-9) if qtd_pregos else 0
    fita_m = fita_total if fita else 0.0
    rolos = math.ceil(fita_m / ROLO_FITA_EUA_M - 1e-9) if fita_m > 0 else 0

    return {
        "portas": totais["porta"],
        "janelas": totais["janela"],
        "area_vaos_m2": area_total,          # sem arredondar: a tela mostra em sq ft
        "perimetro_m": perimetro_total,
        "latas_espuma": latas,
        "pregos": qtd_pregos,
        "caixas_pregos": caixas,
        "fita_m": fita_m,
        "rolos_fita": rolos,
    }


def calcular_esquadrias(
    itens: list,
    espuma: bool = False,
    parafusos: bool = False,
    argamassa: bool = False,
) -> dict:
    """itens: lista de {"tipo", "material", "qtd", "larg", "alt"} (larguras e alturas em cm)."""
    erro = _conferir_itens(itens)
    if erro:
        return {"erro": erro}

    totais = {"porta": 0, "janela": 0}
    area_total = 0.0
    perimetro_total = 0.0
    for item in itens:
        totais[item["tipo"]] += item["qtd"]
        area_total += item["qtd"] * (item["larg"] / 100.0) * (item["alt"] / 100.0)
        perimetro_total += item["qtd"] * perimetro_m(item["tipo"], item["larg"], item["alt"])

    tubos_espuma = math.ceil(perimetro_total / METROS_POR_TUBO_ESPUMA - 1e-9) if espuma else 0
    qtd_parafusos = math.ceil(perimetro_total / METROS_POR_PARAFUSO - 1e-9) if parafusos else 0
    argamassa_kg = perimetro_total * ARGAMASSA_FIXACAO_KG_M if argamassa else 0.0
    sacos_argamassa = math.ceil(argamassa_kg / SACO_ARGAMASSA_FIXACAO_KG - 1e-9) if argamassa_kg > 0 else 0

    return {
        "portas": totais["porta"],
        "janelas": totais["janela"],
        "area_vaos_m2": round(area_total, 2),
        "perimetro_m": round(perimetro_total, 2),
        "tubos_espuma": tubos_espuma,
        "parafusos": qtd_parafusos,
        "argamassa_kg": round(argamassa_kg, 1),
        "sacos_argamassa": sacos_argamassa,
    }