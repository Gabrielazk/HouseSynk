"""Testes da conta da aba Azulejo, sem tela (testes unitários).

Cada teste chama a função de conta direto, com os valores dos testes do testes_rodada1.md,
e confere os resultados (assert). Os erros conferem a mensagem certa, sem travar.
Os limites com aviso (janela "Confira os valores") ficam na tela, não na conta: eles são
testados no test_rodada1.py.

Rodar (na pasta C:\\Calc\\Calculadora):
  env311\\Scripts\\python.exe -B -m pytest tests\\test_azulejo.py -v
"""

from src.calculators.revestimento import calcular_azulejo


def test_azulejo_teste_a():
    # Teste A: 30 m², peça 30x60, vãos 4, 1,8 m² por caixa, AC-III, perda 15, com desenho
    resultado = calcular_azulejo(30, 30, 60, desconto_vaos_m2=4, m2_por_caixa=1.8, tipo_argamassa="AC-III", perda_percentual=15, desenho=True)
    assert resultado['area_liquida_m2'] == 26.0
    assert resultado['perda_percentual'] == 15
    assert resultado['area_com_perda_m2'] == 29.9
    assert resultado['pecas'] == 167
    assert resultado['caixas'] == 17
    assert resultado['argamassa_kg'] == 149.5
    assert resultado['sacos_argamassa'] == 8


def test_azulejo_teste_b():
    # Teste B: 30 m², peça 30x60, o resto padrão (perda automática 10%, AC-II)
    resultado = calcular_azulejo(30, 30, 60)
    assert resultado['tipo_argamassa'] == 'AC-II'
    assert resultado['perda_percentual'] == 10.0
    assert resultado['area_com_perda_m2'] == 33.0
    assert resultado['pecas'] == 184
    assert resultado['caixas'] == 0
    assert resultado['argamassa_kg'] == 165.0
    assert resultado['sacos_argamassa'] == 9


def test_azulejo_com_vaos():
    # B2: com 4 m² de vãos
    resultado = calcular_azulejo(30, 30, 60, desconto_vaos_m2=4)
    assert resultado['area_liquida_m2'] == 26.0
    assert resultado['area_com_perda_m2'] == 28.6
    assert resultado['pecas'] == 159
    assert resultado['sacos_argamassa'] == 8


def test_azulejo_com_caixa():
    # B3: 1,8 m² por caixa
    resultado = calcular_azulejo(30, 30, 60, m2_por_caixa=1.8)
    assert resultado['pecas'] == 184
    assert resultado['caixas'] == 19


def test_azulejo_com_desenho():
    # B4: com desenho (perda 25%)
    resultado = calcular_azulejo(30, 30, 60, desenho=True)
    assert resultado['perda_percentual'] == 25.0
    assert resultado['pecas'] == 209


def test_azulejo_peca_30x90():
    # B6: peça 30x90 (perda 15% e argamassa de peça grande)
    resultado = calcular_azulejo(30, 30, 90)
    assert resultado['perda_percentual'] == 15.0
    assert resultado['consumo_argamassa_kg_m2'] == 8.0
    assert resultado['pecas'] == 128
    assert resultado['sacos_argamassa'] == 14


def test_azulejo_perda_digitada():
    # Perda digitada 2,5
    resultado = calcular_azulejo(30, 30, 60, perda_percentual=2.5)
    assert resultado['perda_percentual'] == 2.5
    assert resultado['area_com_perda_m2'] == 30.75
    assert resultado['pecas'] == 171
    assert resultado['argamassa_kg'] == 153.8

# ------------------------------------------------------------------
# Erros: a função não pode travar, tem que devolver a mensagem certa
# ------------------------------------------------------------------


def test_azulejo_area_zero():
    # Área zero
    resultado = calcular_azulejo(0, 30, 60)
    assert resultado == {"erro": 'Área e tamanho da peça devem ser maiores que zero.'}


def test_azulejo_vaos_igual_area():
    # Vãos iguais à área
    resultado = calcular_azulejo(30, 30, 60, desconto_vaos_m2=30)
    assert resultado == {"erro": 'O desconto de vãos deve ser menor que a área.'}


def test_azulejo_vaos_negativos():
    # Vãos negativos
    resultado = calcular_azulejo(30, 30, 60, desconto_vaos_m2=-4)
    assert resultado == {"erro": 'Os valores não podem ser negativos.'}


def test_azulejo_perda_negativa():
    # Perda negativa
    resultado = calcular_azulejo(30, 30, 60, perda_percentual=-5)
    assert resultado == {"erro": 'A perda não pode ser negativa.'}
