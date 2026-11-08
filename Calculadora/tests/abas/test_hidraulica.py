"""Testes da conta da aba Hidráulica, sem tela (testes unitários).

Cada teste chama a função de conta direto, com os valores dos testes do testes_rodada1.md,
e confere os resultados (assert). Os erros conferem a mensagem certa, sem travar.
Os limites com aviso (janela "Confira os valores") ficam na tela, não na conta: eles são
testados no test_rodada1.py.

Rodar (no terminal, na pasta do app, a que tem o main.py):
  env311\\Scripts\\python.exe -B -m pytest tests\\abas\\test_hidraulica.py -v
"""

from src.calculators.hidraulica import calcular_hidraulica


def test_hidraulica_teste_a():
    # Teste A: 10 de água fria, 3 de quente, 8 de esgoto, todas as metragens do projeto, perda 5
    resultado = calcular_hidraulica(10, 3, 8, tubos_m={"fria": 50, "quente": 20, "esg40": 30, "esg100": 18}, perda_percentual=5)
    assert resultado['tubos'] == {'fria': {'metros': 52.5, 'barras': 9, 'do_projeto': True},
                                  'quente': {'metros': 21.0, 'barras': 7, 'do_projeto': True},
                                  'esg40': {'metros': 31.5, 'barras': 6, 'do_projeto': True},
                                  'esg100': {'metros': 18.9, 'barras': 4, 'do_projeto': True}}
    assert resultado['conexoes'] == {'fria': 40, 'quente': 12, 'esgoto': 24}
    assert resultado['registros'] == 4


def test_hidraulica_teste_b():
    # Teste B: 10 de água fria, 3 de quente, 8 de esgoto, tudo estimado (perda 10)
    resultado = calcular_hidraulica(10, 3, 8)
    assert resultado['tubos'] == {'fria': {'metros': 44.0, 'barras': 8, 'do_projeto': False},
                                  'quente': {'metros': 16.5, 'barras': 6, 'do_projeto': False},
                                  'esg40': {'metros': 26.4, 'barras': 5, 'do_projeto': False},
                                  'esg100': {'metros': 17.6, 'barras': 3, 'do_projeto': False}}
    assert resultado['conexoes'] == {'fria': 40, 'quente': 12, 'esgoto': 24}
    assert resultado['registros'] == 4


def test_hidraulica_so_um_ponto():
    # B2: só 1 ponto de água fria
    resultado = calcular_hidraulica(1, 0, 0)
    assert resultado['tubos'] == {'fria': {'metros': 4.4, 'barras': 1, 'do_projeto': False}}
    assert resultado['conexoes'] == {'fria': 4}
    assert resultado['registros'] == 1


def test_hidraulica_fria_do_projeto():
    # B3: tubo de água fria do projeto (50 m)
    resultado = calcular_hidraulica(10, 3, 8, tubos_m={"fria": 50})
    assert resultado['tubos'] == {'fria': {'metros': 55.0, 'barras': 10, 'do_projeto': True},
                                  'quente': {'metros': 16.5, 'barras': 6, 'do_projeto': False},
                                  'esg40': {'metros': 26.4, 'barras': 5, 'do_projeto': False},
                                  'esg100': {'metros': 17.6, 'barras': 3, 'do_projeto': False}}


def test_hidraulica_so_esgoto():
    # B4: só 8 pontos de esgoto
    resultado = calcular_hidraulica(0, 0, 8)
    assert resultado['tubos'] == {'esg40': {'metros': 26.4, 'barras': 5, 'do_projeto': False},
                                  'esg100': {'metros': 17.6, 'barras': 3, 'do_projeto': False}}
    assert resultado['conexoes'] == {'esgoto': 24}
    assert resultado['registros'] == 0


def test_hidraulica_perda_2_virgula_5():
    # Perda 2,5
    resultado = calcular_hidraulica(10, 3, 8, perda_percentual=2.5)
    assert resultado['tubos'] == {'fria': {'metros': 41.0, 'barras': 7, 'do_projeto': False},
                                  'quente': {'metros': 15.4, 'barras': 6, 'do_projeto': False},
                                  'esg40': {'metros': 24.6, 'barras': 5, 'do_projeto': False},
                                  'esg100': {'metros': 16.4, 'barras': 3, 'do_projeto': False}}

# ------------------------------------------------------------------
# Erros: a função não pode travar, tem que devolver a mensagem certa
# ------------------------------------------------------------------


def test_hidraulica_tudo_zero():
    # Tudo zero
    resultado = calcular_hidraulica(0, 0, 0)
    assert resultado == {"erro": "erro_pontos_hidraulica"}


def test_hidraulica_pontos_negativos():
    # Pontos negativos
    resultado = calcular_hidraulica(-10, 3, 8)
    assert resultado == {"erro": "erro_quantidades_negativas"}


def test_hidraulica_perda_negativa():
    # Perda negativa
    resultado = calcular_hidraulica(10, 3, 8, perda_percentual=-5)
    assert resultado == {"erro": "erro_valores_negativos"}


def test_hidraulica_tubo_negativo():
    # Tubo negativo
    resultado = calcular_hidraulica(10, 3, 8, tubos_m={"fria": -10})
    assert resultado == {"erro": "erro_valores_negativos"}
