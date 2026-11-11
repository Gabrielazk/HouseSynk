import math
from src.calculators.unidades import arredondar  # arredonda certo (1,575 -> 1,58)

# As mensagens de erro são CHAVES de texto (ex.: "erro_perda_negativa"): a tela mostra a frase
# no idioma escolhido com o txt() (os textos ficam no comum.py). Assim aqui só ficam as contas.

# Perda padrão (sobras de fio e conduíte)
PERDA_PADRAO_ELETRICA = 10.0

# Limites com aviso (regra 12): passar deles abre a janela "Confira os valores", com Continuar.
# Criados pelo Leo em Nov 3, 2026 (o engenheiro ainda vai conferir; se ele mudar, é só trocar aqui).
TOMADAS_MAXIMO = 300
INTERRUPTORES_MAXIMO = 300
LUZES_MAXIMO = 300
CHUVEIROS_MAXIMO = 10  # somando os dois campos de chuveiro

# Bitolas de fio (mm²)
BITOLAS_FIO = [1.5, 2.5, 4.0, 6.0]

# Embalagens fixas
ROLO_CONDUITE_M = 50.0   # conduíte corrugado 3/4"
ROLO_FIO_M = 100.0

# Estimativa por ponto, para quem não tem o projeto (CONFIRMADO pelo engenheiro em Oct 27, 2026)
CONDUITE_POR_PONTO_M = 5.0          # metros de conduíte por tomada, interruptor ou ponto de luz
FIO_POR_TOMADA_M = {2.5: 15.0}       # fase, neutro e terra (3 fios x 5 m)
FIO_POR_INTERRUPTOR_M = {1.5: 10.0}  # fase e retorno (2 fios x 5 m)
FIO_POR_LUZ_M = {1.5: 10.0}          # neutro e retorno (2 fios x 5 m)

# Chuveiro elétrico: circuito só dele, saindo do quadro de luz (o engenheiro aprovou o campo em Oct 27, 2026).
# PROVISÓRIO (confirmar com o engenheiro): 3 fios de 6 mm² (2 fases ou fase e neutro, mais o terra)
# com uns 10 m cada, e 10 m de conduíte.
CONDUITE_POR_CHUVEIRO_M = 10.0
FIO_POR_CHUVEIRO_M = {6.0: 30.0}
# Chuveiro mais fraco (até 5.500 W): usa fio de 4 mm² (o engenheiro aprovou a opção em Oct 29, 2026).
# Mesmo circuito: 3 fios de uns 10 m e 10 m de conduíte.
FIO_POR_CHUVEIRO_ATE_5500W_M = {4.0: 30.0}

# Preços PROVISÓRIOS (R$) até a tabela de preços ser refeita
PRECO_ROLO_CONDUITE = 75.00
PRECO_ROLO_FIO = {1.5: 150.00, 2.5: 230.00, 4.0: 360.00, 6.0: 530.00}
PRECO_CAIXA_4X2 = 2.50        # caixinha de tomada e interruptor
PRECO_CAIXA_OCTOGONAL = 5.00  # caixa do ponto de luz no teto
PRECO_TOMADA = 15.00
PRECO_INTERRUPTOR = 12.00


def calcular_eletrica(
    tomadas: int,
    interruptores: int,
    pontos_luz: int,
    conduite_m: float = None,
    fios_m: dict = None,
    perda_percentual: float = PERDA_PADRAO_ELETRICA,
    chuveiros: int = 0,
    chuveiros_ate_5500w: int = 0,
) -> dict:
    """chuveiros: acima de 5.500 W (fio 6 mm²); chuveiros_ate_5500w: até 5.500 W (fio 4 mm²).
    conduite_m e fios_m são opcionais (quem tem o projeto).
    Em fios_m, só as bitolas informadas substituem a estimativa; as outras continuam estimadas."""
    if tomadas < 0 or interruptores < 0 or pontos_luz < 0 or chuveiros < 0 or chuveiros_ate_5500w < 0:
        return {"erro": "erro_quantidades_negativas"}
    if tomadas + interruptores + pontos_luz + chuveiros + chuveiros_ate_5500w <= 0:
        return {"erro": "erro_pontos_eletrica"}
    if perda_percentual < 0 or (conduite_m is not None and conduite_m < 0):
        return {"erro": "erro_valores_negativos"}
    fios_m = fios_m or {}
    if any(v < 0 for v in fios_m.values()):
        return {"erro": "erro_valores_negativos"}

    fator = 1 + perda_percentual / 100.0
    pontos = tomadas + interruptores + pontos_luz
    todos_chuveiros = chuveiros + chuveiros_ate_5500w

    # Conduíte: do projeto ou estimado por ponto (e por chuveiro)
    conduite_estimado = conduite_m is None
    conduite_base = (pontos * CONDUITE_POR_PONTO_M + todos_chuveiros * CONDUITE_POR_CHUVEIRO_M) if conduite_estimado else conduite_m
    conduite_total = conduite_base * fator
    rolos_conduite = math.ceil(conduite_total / ROLO_CONDUITE_M - 1e-9) if conduite_total > 0 else 0

    # Fios: cada bitola do projeto, ou estimada por ponto (e por chuveiro)
    fios = {}
    for bitola in BITOLAS_FIO:
        if bitola in fios_m:
            base = fios_m[bitola]
        else:
            base = (tomadas * FIO_POR_TOMADA_M.get(bitola, 0.0)
                    + interruptores * FIO_POR_INTERRUPTOR_M.get(bitola, 0.0)
                    + pontos_luz * FIO_POR_LUZ_M.get(bitola, 0.0)
                    + chuveiros * FIO_POR_CHUVEIRO_M.get(bitola, 0.0)
                    + chuveiros_ate_5500w * FIO_POR_CHUVEIRO_ATE_5500W_M.get(bitola, 0.0))
        total = base * fator
        if total > 0:
            fios[bitola] = {
                "metros": arredondar(total, 1),
                "rolos": math.ceil(total / ROLO_FIO_M - 1e-9),
                "do_projeto": bitola in fios_m,
            }

    return {
        "tomadas": tomadas,
        "interruptores": interruptores,
        "pontos_luz": pontos_luz,
        "chuveiros": chuveiros,
        "chuveiros_ate_5500w": chuveiros_ate_5500w,
        "perda_percentual": perda_percentual,
        "conduite_estimado": conduite_estimado,
        "conduite_m": arredondar(conduite_total, 1),
        "rolos_conduite": rolos_conduite,
        "fios": fios,
        "caixas_4x2": tomadas + interruptores,
        "caixas_octogonais": pontos_luz,
    }

# ==========================================
# EUA (Parte A da versão EUA, Nov 11, 2026; pesquisa em claude/pesquisa_embalagens_eua.md)
# Na casa americana a fiação é o cabo Romex (NM-B): os fios e o terra vêm juntos num cabo só,
# passado por furos na madeira, sem conduíte. Chuveiro elétrico quase não existe (aquecimento central).
# Decisões da Gabi (Nov 11, 2026): dois campos de tomada (comuns no 14/2; cozinha, banheiro,
# lavanderia e garagem no 12/2, como pede o código NEC 210.11(C)) e as tomadas de 20 A contadas
# como GFCI (o NEC 210.8 exige a proteção nessas áreas). A conta continua em métrico por dentro.
# ==========================================
PE_M = 0.3048
CABO_POR_PONTO_EUA_M = 15 * PE_M     # 15 ft de cabo por tomada, interruptor ou ponto de luz (PROVISÓRIO ⚠️, Mike Holt)
ROLO_CABO_EUA_M = 250 * PE_M         # rolo de 250 ft (Southwire 14/2 e 12/2; pesquisa ✅)
CABOS_EUA = ["14/2", "12/2"]         # 14/2: circuito de 15 A (tomadas comuns e luz); 12/2: 20 A

# Preços PROVISÓRIOS ($) até a tabela de preços ser refeita
PRECO_ROLO_CABO_EUA = {"14/2": 95.00, "12/2": 140.00}   # rolo de 250 ft
PRECO_CAIXA_1GANG_EUA = 2.50       # caixa de tomada e interruptor (o mesmo número da caixinha 4x2 do Brasil)
PRECO_CAIXA_REDONDA_EUA = 5.00     # caixa redonda de 4 in da luz (o mesmo número da octogonal do Brasil)
PRECO_TOMADA_EUA = 15.00           # tomada comum (o mesmo número do Brasil)
PRECO_TOMADA_GFCI_EUA = 25.00      # tomada GFCI de 20 A
PRECO_INTERRUPTOR_EUA = 12.00      # (o mesmo número do Brasil)


def calcular_eletrica_eua(
    tomadas: int,
    tomadas_20a: int,
    interruptores: int,
    pontos_luz: int,
    cabos_m: dict = None,
    perda_percentual: float = PERDA_PADRAO_ELETRICA,
) -> dict:
    """Elétrica dos EUA. tomadas: comuns (cabo 14/2); tomadas_20a: cozinha, banheiro, lavanderia
    e garagem (cabo 12/2, tomadas GFCI). cabos_m: metragens do projeto ({"14/2": m, "12/2": m});
    o cabo que não vier do projeto é estimado por ponto. Recebe e devolve em métrico."""
    if min(tomadas, tomadas_20a, interruptores, pontos_luz) < 0:
        return {"erro": "erro_quantidades_negativas"}
    if tomadas + tomadas_20a + interruptores + pontos_luz <= 0:
        return {"erro": "erro_pontos_eletrica"}
    cabos_m = cabos_m or {}
    if perda_percentual < 0 or any(v < 0 for v in cabos_m.values()):
        return {"erro": "erro_valores_negativos"}

    fator = 1 + perda_percentual / 100.0
    estimado = {
        "14/2": (tomadas + interruptores + pontos_luz) * CABO_POR_PONTO_EUA_M,
        "12/2": tomadas_20a * CABO_POR_PONTO_EUA_M,
    }
    cabos = {}
    for cabo in CABOS_EUA:
        base = cabos_m[cabo] if cabo in cabos_m else estimado[cabo]
        total = base * fator
        if total > 0:
            cabos[cabo] = {
                "metros": total,
                "rolos": math.ceil(total / ROLO_CABO_EUA_M - 1e-9),
                "do_projeto": cabo in cabos_m,
            }

    return {
        "tomadas": tomadas,
        "tomadas_20a": tomadas_20a,
        "interruptores": interruptores,
        "pontos_luz": pontos_luz,
        "perda_percentual": perda_percentual,
        "cabos": cabos,
        "caixas_1gang": tomadas + tomadas_20a + interruptores,
        "caixas_redondas": pontos_luz,
    }