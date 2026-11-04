"""Testes da conta da aba Elétrica, sem tela (testes unitários).

Cada teste chama a função de conta direto, com os valores dos testes do testes_rodada1.md,
e confere os resultados (assert). Os erros conferem a mensagem certa, sem travar.
Os limites com aviso (janela "Confira os valores") ficam na tela, não na conta: eles são
testados no test_rodada1.py.

Rodar (na pasta C:\\Calc\\Calculadora):
  env311\\Scripts\\python.exe -B -m pytest tests\\test_eletrica.py -v
"""

from src.calculators.eletrica import calcular_eletrica


def test_eletrica_teste_a():
    # Teste A: 20 tomadas, 10 interruptores, 12 pontos de luz, 2 chuveiros grandes e 1 pequeno, todas as metragens do projeto, perda 5
    resultado = calcular_eletrica(20, 10, 12, conduite_m=150, fios_m={1.5: 200, 2.5: 250, 4.0: 40, 6.0: 60}, perda_percentual=5, chuveiros=2, chuveiros_ate_5500w=1)
    assert resultado['conduite_estimado'] == False
    assert resultado['conduite_m'] == 157.5
    assert resultado['rolos_conduite'] == 4
    assert resultado['fios'] == {1.5: {'metros': 210.0, 'rolos': 3, 'do_projeto': True},
                                 2.5: {'metros': 262.5, 'rolos': 3, 'do_projeto': True},
                                 4.0: {'metros': 42.0, 'rolos': 1, 'do_projeto': True},
                                 6.0: {'metros': 63.0, 'rolos': 1, 'do_projeto': True}}
    assert resultado['caixas_4x2'] == 30
    assert resultado['caixas_octogonais'] == 12


def test_eletrica_teste_b():
    # Teste B: 20 tomadas, 10 interruptores, 12 pontos de luz, tudo estimado (perda 10)
    resultado = calcular_eletrica(20, 10, 12)
    assert resultado['conduite_estimado'] == True
    assert resultado['conduite_m'] == 231.0
    assert resultado['rolos_conduite'] == 5
    assert resultado['fios'] == {1.5: {'metros': 242.0, 'rolos': 3, 'do_projeto': False},
                                 2.5: {'metros': 330.0, 'rolos': 4, 'do_projeto': False}}
    assert resultado['caixas_4x2'] == 30
    assert resultado['caixas_octogonais'] == 12


def test_eletrica_chuveiros_grandes():
    # B2: + 2 chuveiros acima de 5.500 W (fio 6 mm²)
    resultado = calcular_eletrica(20, 10, 12, chuveiros=2)
    assert resultado['conduite_m'] == 253.0
    assert resultado['fios'] == {1.5: {'metros': 242.0, 'rolos': 3, 'do_projeto': False},
                                 2.5: {'metros': 330.0, 'rolos': 4, 'do_projeto': False},
                                 6.0: {'metros': 66.0, 'rolos': 1, 'do_projeto': False}}


def test_eletrica_chuveiros_pequenos():
    # B3: + 2 chuveiros até 5.500 W (fio 4 mm²)
    resultado = calcular_eletrica(20, 10, 12, chuveiros_ate_5500w=2)
    assert resultado['conduite_m'] == 253.0
    assert resultado['fios'] == {1.5: {'metros': 242.0, 'rolos': 3, 'do_projeto': False},
                                 2.5: {'metros': 330.0, 'rolos': 4, 'do_projeto': False},
                                 4.0: {'metros': 66.0, 'rolos': 1, 'do_projeto': False}}


def test_eletrica_conduite_do_projeto():
    # B5: conduíte do projeto (150 m)
    resultado = calcular_eletrica(20, 10, 12, conduite_m=150)
    assert resultado['conduite_estimado'] == False
    assert resultado['conduite_m'] == 165.0
    assert resultado['rolos_conduite'] == 4


def test_eletrica_so_um_chuveiro():
    # B7: só 1 chuveiro
    resultado = calcular_eletrica(0, 0, 0, chuveiros=1)
    assert resultado['conduite_m'] == 11.0
    assert resultado['fios'] == {6.0: {'metros': 33.0, 'rolos': 1, 'do_projeto': False}}
    assert resultado['caixas_4x2'] == 0
    assert resultado['caixas_octogonais'] == 0


def test_eletrica_perda_2_virgula_5():
    # Perda 2,5
    resultado = calcular_eletrica(20, 10, 12, perda_percentual=2.5)
    assert resultado['conduite_m'] == 215.3
    assert resultado['rolos_conduite'] == 5

# ------------------------------------------------------------------
# Erros: a função não pode travar, tem que devolver a mensagem certa
# ------------------------------------------------------------------


def test_eletrica_tudo_zero():
    # Tudo zero
    resultado = calcular_eletrica(0, 0, 0)
    assert resultado == {"erro": "erro_pontos_eletrica"}


def test_eletrica_tomadas_negativas():
    # Tomadas negativas
    resultado = calcular_eletrica(-5, 10, 12)
    assert resultado == {"erro": "erro_quantidades_negativas"}


def test_eletrica_perda_negativa():
    # Perda negativa
    resultado = calcular_eletrica(20, 10, 12, perda_percentual=-5)
    assert resultado == {"erro": "erro_valores_negativos"}


def test_eletrica_conduite_negativo():
    # Conduíte negativo
    resultado = calcular_eletrica(20, 10, 12, conduite_m=-10)
    assert resultado == {"erro": "erro_valores_negativos"}
