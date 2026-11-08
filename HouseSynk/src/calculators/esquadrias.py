import math

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


def perimetro_m(tipo: str, largura_cm: float, altura_cm: float) -> float:
    larg, alt = largura_cm / 100.0, altura_cm / 100.0
    return 2 * alt + larg if tipo == "porta" else 2 * (larg + alt)


def calcular_esquadrias(
    itens: list,
    espuma: bool = False,
    parafusos: bool = False,
    argamassa: bool = False,
) -> dict:
    """itens: lista de {"tipo", "material", "qtd", "larg", "alt"} (larguras e alturas em cm)."""
    if not itens:
        return {"erro": "erro_lista_esquadrias_vazia"}
    for item in itens:
        if item.get("tipo") not in TIPOS_ESQUADRIA or item.get("material") not in MATERIAIS:
            return {"erro": "erro_tipo_material_invalido"}
        if item.get("qtd", 0) <= 0 or item.get("larg", 0) <= 0 or item.get("alt", 0) <= 0:
            return {"erro": "erro_qtd_larg_alt_zero"}

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