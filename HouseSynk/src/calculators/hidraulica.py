import math

# As mensagens de erro são CHAVES de texto (ex.: "erro_perda_negativa"): a tela mostra a frase
# no idioma escolhido com o txt() (os textos ficam no comum.py). Assim aqui só ficam as contas.

# Perda padrão (sobras e cortes de tubo)
PERDA_PADRAO_HIDRAULICA = 10.0

# Limites com aviso (regra 12): passar deles abre a janela "Confira os valores", com Continuar.
# Criados pelo Leo em Nov 3, 2026 (o engenheiro ainda vai conferir; se ele mudar, é só trocar aqui).
PONTOS_MAXIMO = 200  # de cada tipo: água fria, água quente e esgoto

# Tubos (ordem em que aparecem na tela e no resultado)
#   fria:   PVC soldável marrom 25 mm (água fria)
#   quente: CPVC 22 mm (água quente)
#   esg40:  PVC branco 40 mm (esgoto de pia, chuveiro, ralo)
#   esg100: PVC branco 100 mm (esgoto do vaso e ramal principal)
TUBOS = ["fria", "quente", "esg40", "esg100"]

# Comprimento da barra vendida, em metros (embalagens fixas)
BARRA_TUBO_M = {"fria": 6.0, "quente": 3.0, "esg40": 6.0, "esg100": 6.0}

# Estimativa por ponto, para quem não tem o projeto (PROVISÓRIO, confirmar com o engenheiro)
TUBO_POR_PONTO_M = {
    "fria": {"fria": 4.0},                    # cada ponto de água fria: 4 m de tubo 25 mm
    "quente": {"quente": 5.0},                # cada ponto de água quente: 5 m de tubo 22 mm
    "esgoto": {"esg40": 3.0, "esg100": 2.0},  # cada ponto de esgoto: 3 m de 40 mm + 2 m de 100 mm
}
CONEXOES_POR_PONTO = {"fria": 4, "quente": 4, "esgoto": 3}  # joelhos, tês, luvas...
PONTOS_POR_REGISTRO = 4  # um registro de gaveta a cada 4 pontos de água (mais ou menos um por ambiente)

# Preços PROVISÓRIOS (R$) até a tabela de preços ser refeita
PRECO_BARRA_TUBO = {"fria": 30.00, "quente": 45.00, "esg40": 35.00, "esg100": 90.00}
PRECO_CONEXAO = {"fria": 3.00, "quente": 9.00, "esgoto": 6.00}
PRECO_REGISTRO = 45.00


def calcular_hidraulica(
    pontos_fria: int,
    pontos_quente: int,
    pontos_esgoto: int,
    tubos_m: dict = None,
    perda_percentual: float = PERDA_PADRAO_HIDRAULICA,
) -> dict:
    """tubos_m é opcional (quem tem o projeto): só os tubos informados substituem a estimativa."""
    if pontos_fria < 0 or pontos_quente < 0 or pontos_esgoto < 0:
        return {"erro": "erro_quantidades_negativas"}
    if pontos_fria + pontos_quente + pontos_esgoto <= 0:
        return {"erro": "erro_pontos_hidraulica"}
    tubos_m = tubos_m or {}
    if perda_percentual < 0 or any(v < 0 for v in tubos_m.values()):
        return {"erro": "erro_valores_negativos"}

    fator = 1 + perda_percentual / 100.0
    pontos = {"fria": pontos_fria, "quente": pontos_quente, "esgoto": pontos_esgoto}

    tubos = {}
    for tubo in TUBOS:
        if tubo in tubos_m:
            base = tubos_m[tubo]
        else:
            base = sum(qtd * TUBO_POR_PONTO_M[tipo].get(tubo, 0.0) for tipo, qtd in pontos.items())
        total = base * fator
        if total > 0:
            tubos[tubo] = {
                "metros": round(total, 1),
                "barras": math.ceil(total / BARRA_TUBO_M[tubo] - 1e-9),
                "do_projeto": tubo in tubos_m,
            }

    conexoes = {tipo: qtd * CONEXOES_POR_PONTO[tipo] for tipo, qtd in pontos.items() if qtd > 0}
    pontos_agua = pontos_fria + pontos_quente
    registros = math.ceil(pontos_agua / PONTOS_POR_REGISTRO) if pontos_agua > 0 else 0

    return {
        "pontos_fria": pontos_fria,
        "pontos_quente": pontos_quente,
        "pontos_esgoto": pontos_esgoto,
        "perda_percentual": perda_percentual,
        "tubos": tubos,
        "conexoes": conexoes,
        "registros": registros,
    }

# ==========================================
# EUA (Parte A da versão EUA, Nov 11, 2026; pesquisa em claude/pesquisa_embalagens_eua.md, item 7)
# Na casa americana a água fria e a quente usam o tubo PEX (azul na fria, vermelho na quente),
# vendido em rolos; o CPVC do Brasil não entra. O esgoto usa o PVC DWV (Schedule 40) em barras de 10 ft.
# Decisões da Gabi (Nov 11, 2026): esgoto em 2 in (pia, chuveiro, ralo e máquina; o código IRC
# pede 2 in no chuveiro e na máquina) + 3 in (vaso), igual aos dois tubos do Brasil; e um registro
# (stop valve) por ponto de água, que é o costume de lá (um embaixo de cada pia, vaso e máquina).
# A conta continua em métrico por dentro.
# ==========================================
PE_M = 0.3048

# Tubos dos EUA (ordem em que aparecem no resultado). Os campos da tela são os mesmos do Brasil
# (tubo_fria, tubo_quente, tubo_esg40, tubo_esg100), cada um com o tubo parecido de lá:
#   fria:   PEX 1/2 in azul (água fria)            <- campo tubo_fria
#   quente: PEX 1/2 in vermelho (água quente)      <- campo tubo_quente
#   esg2:   PVC DWV 2 in (pia, chuveiro, ralo, máquina) <- campo tubo_esg40
#   esg3:   PVC DWV 3 in (vaso e ramal principal)  <- campo tubo_esg100
TUBOS_EUA = ["fria", "quente", "esg2", "esg3"]
CAMPO_TUBO_EUA = {"fria": "fria", "quente": "quente", "esg2": "esg40", "esg3": "esg100"}

# Embalagens (pesquisa ✅ Home Depot): PEX em rolo de 100 ft; PVC DWV em barra de 10 ft
EMBALAGEM_TUBO_EUA_M = {"fria": 100 * PE_M, "quente": 100 * PE_M, "esg2": 10 * PE_M, "esg3": 10 * PE_M}
TUBO_EM_ROLO_EUA = {"fria": True, "quente": True, "esg2": False, "esg3": False}

# Estimativa por ponto (PROVISÓRIO ⚠️): os metros do Brasil (confirmados pelo engenheiro),
# arredondados em ft: água fria 13 ft (4 m), água quente 16 ft (5 m), esgoto 10 ft de 2 in (3 m)
# + 7 ft de 3 in (2 m).
TUBO_POR_PONTO_EUA_M = {
    "fria": {"fria": 13 * PE_M},
    "quente": {"quente": 16 * PE_M},
    "esgoto": {"esg2": 10 * PE_M, "esg3": 7 * PE_M},
}
# Conexões (PROVISÓRIO ⚠️, a mesma regra do Brasil): 4 por ponto de água, 3 por ponto de esgoto
CONEXOES_POR_PONTO_EUA = CONEXOES_POR_PONTO
# Registros: 1 stop valve por ponto de água (fria ou quente). O chuveiro normalmente não tem,
# então pode sobrar algum (sobra em vez de faltar).

# Preços PROVISÓRIOS ($) até a tabela de preços ser refeita
PRECO_TUBO_EUA = {"fria": 40.00, "quente": 40.00, "esg2": 15.00, "esg3": 30.00}  # rolo de 100 ft / barra de 10 ft
PRECO_CONEXAO_EUA = {"fria": 3.00, "quente": 3.00, "esgoto": 6.00}
PRECO_REGISTRO_EUA = 10.00  # stop valve


def calcular_hidraulica_eua(
    pontos_fria: int,
    pontos_quente: int,
    pontos_esgoto: int,
    tubos_m: dict = None,
    perda_percentual: float = PERDA_PADRAO_HIDRAULICA,
) -> dict:
    """Hidráulica dos EUA. tubos_m: metragens do projeto, com as chaves dos EUA
    ({"fria": m, "quente": m, "esg2": m, "esg3": m}); o tubo que não vier do projeto é estimado
    por ponto. Recebe e devolve em métrico."""
    if pontos_fria < 0 or pontos_quente < 0 or pontos_esgoto < 0:
        return {"erro": "erro_quantidades_negativas"}
    if pontos_fria + pontos_quente + pontos_esgoto <= 0:
        return {"erro": "erro_pontos_hidraulica"}
    tubos_m = tubos_m or {}
    if perda_percentual < 0 or any(v < 0 for v in tubos_m.values()):
        return {"erro": "erro_valores_negativos"}

    fator = 1 + perda_percentual / 100.0
    pontos = {"fria": pontos_fria, "quente": pontos_quente, "esgoto": pontos_esgoto}

    tubos = {}
    for tubo in TUBOS_EUA:
        if tubo in tubos_m:
            base = tubos_m[tubo]
        else:
            base = sum(qtd * TUBO_POR_PONTO_EUA_M[tipo].get(tubo, 0.0) for tipo, qtd in pontos.items())
        total = base * fator
        if total > 0:
            tubos[tubo] = {
                "metros": total,
                "embalagens": math.ceil(total / EMBALAGEM_TUBO_EUA_M[tubo] - 1e-9),  # rolos ou barras
                "do_projeto": tubo in tubos_m,
            }

    conexoes = {tipo: qtd * CONEXOES_POR_PONTO_EUA[tipo] for tipo, qtd in pontos.items() if qtd > 0}

    return {
        "pontos_fria": pontos_fria,
        "pontos_quente": pontos_quente,
        "pontos_esgoto": pontos_esgoto,
        "perda_percentual": perda_percentual,
        "tubos": tubos,
        "conexoes": conexoes,
        "registros": pontos_fria + pontos_quente,  # 1 stop valve por ponto de água
    }