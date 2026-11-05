"""Testes da conta da aba Rejunte, sem tela (testes unitários).

Cada teste chama a função de conta direto, com os valores dos testes do testes_rodada1.md,
e confere os resultados (assert). Os erros conferem a mensagem certa, sem travar.
Os limites com aviso (janela "Confira os valores") ficam na tela, não na conta: eles são
testados no test_rodada1.py.

Rodar (na pasta C:\\Calc\\Calculadora):
  env311\\Scripts\\python.exe -B -m pytest tests\\abas\\test_rejunte.py -v
"""

from src.calculators.rejunte import calcular_rejunte


def test_rejunte_teste_a():
    # Teste A: 40 m², peça 60x60, junta 3 mm, espessura 10 mm, perda 15
    resultado = calcular_rejunte(40, 60, 60, 3, espessura_mm=10, perda_percentual=15)
    assert resultado['consumo_kg_m2'] == 0.158
    assert resultado['kg_total'] == 7.27
    assert resultado['latas_2kg'] == 4
    assert resultado['latas_1kg'] == 0


def test_rejunte_teste_b():
    # Teste B: 40 m², peça 60x60, junta 3 mm, o resto padrão (espessura 8, perda 10)
    resultado = calcular_rejunte(40, 60, 60, 3)
    assert resultado['espessura_mm'] == 8.0
    assert resultado['consumo_kg_m2'] == 0.126
    assert resultado['kg_total'] == 5.56
    assert resultado['latas_2kg'] == 3
    assert resultado['latas_1kg'] == 0
    assert resultado['tipo_rejunte'] == 'lata'


def test_rejunte_peca_30_junta_5():
    # B2: peça 30x30 com junta 5 mm (completa com lata de 1 kg)
    resultado = calcular_rejunte(40, 30, 30, 5)
    assert resultado['consumo_kg_m2'] == 0.421
    assert resultado['kg_total'] == 18.54
    assert resultado['latas_2kg'] == 9
    assert resultado['latas_1kg'] == 1


def test_rejunte_dados_do_azulejo():
    # B4: os dados do Azulejo (26 m², peça 30x60) com junta 2 mm
    resultado = calcular_rejunte(26, 30, 60, 2)
    assert resultado['kg_total'] == 3.62
    assert resultado['latas_2kg'] == 2
    assert resultado['latas_1kg'] == 0


def test_rejunte_junta_1_virgula_5():
    # Junta 1,5 mm
    resultado = calcular_rejunte(40, 60, 60, 1.5)
    assert resultado['consumo_kg_m2'] == 0.063
    assert resultado['kg_total'] == 2.78
    assert resultado['latas_2kg'] == 1
    assert resultado['latas_1kg'] == 1


def test_rejunte_perda_2_virgula_5():
    # Perda 2,5
    resultado = calcular_rejunte(40, 60, 60, 3, perda_percentual=2.5)
    assert resultado['kg_total'] == 5.18
    assert resultado['latas_2kg'] == 3


def test_rejunte_area_1m2():
    # Área 1 m²: 1 lata de 1 kg
    resultado = calcular_rejunte(1, 60, 60, 3)
    assert resultado['kg_total'] == 0.14
    assert resultado['latas_2kg'] == 0
    assert resultado['latas_1kg'] == 1

# ------------------------------------------------------------------
# Erros: a função não pode travar, tem que devolver a mensagem certa
# ------------------------------------------------------------------


def test_rejunte_area_zero():
    # Área zero
    resultado = calcular_rejunte(0, 60, 60, 3)
    assert resultado == {"erro": "erro_area_peca_junta_zero"}


def test_rejunte_junta_zero():
    # Junta zero
    resultado = calcular_rejunte(40, 60, 60, 0)
    assert resultado == {"erro": "erro_area_peca_junta_zero"}


def test_rejunte_espessura_zero():
    # Espessura da peça zero
    resultado = calcular_rejunte(40, 60, 60, 3, espessura_mm=0)
    assert resultado == {"erro": "erro_espessura_peca_zero"}


def test_rejunte_perda_negativa():
    # Perda negativa
    resultado = calcular_rejunte(40, 60, 60, 3, perda_percentual=-5)
    assert resultado == {"erro": "erro_perda_negativa"}
