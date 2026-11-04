"""Testes da conta da aba Telhado, sem tela (testes unitários).

Cada teste chama a função de conta direto, com os valores dos testes do testes_rodada1.md,
e confere os resultados (assert). Os erros conferem a mensagem certa, sem travar.
Os limites com aviso (janela "Confira os valores") ficam na tela, não na conta: eles são
testados no test_rodada1.py.

Rodar (na pasta C:\\Calc\\Calculadora):
  env311\\Scripts\\python.exe -B -m pytest tests\\test_telhado.py -v
"""

from src.calculators.telhado import calcular_telhado


def test_telhado_teste_a():
    # Teste A: 80 m², telha de concreto, inclinação 35, cumeeira 10 m, com madeiramento, perda 8
    resultado = calcular_telhado(80, "concreto", inclinacao_percentual=35, cumeeira_m=10, incluir_madeiramento=True, perda_percentual=8)
    assert resultado['area_real_m2'] == 84.76
    assert resultado['telhas'] == 962
    assert resultado['cumeeiras'] == 33
    assert resultado['ripas_m'] == 274.6
    assert resultado['caibros_m'] == 183.1
    assert resultado['tercas_m'] == 54.9


def test_telhado_fibrocimento_teste_a2():
    # A2: 60 m², fibrocimento (inclinação padrão 15), cumeeira 8 m, com madeiramento
    resultado = calcular_telhado(60, "fibrocimento", cumeeira_m=8, incluir_madeiramento=True)
    assert resultado['inclinacao_percentual'] == 15.0
    assert resultado['area_real_m2'] == 60.67
    assert resultado['telhas'] == 27
    assert resultado['cumeeiras'] == 9
    assert resultado['ripas_m'] == 0.0
    assert resultado['caibros_m'] == 0.0
    assert resultado['tercas_m'] == 51.0


def test_telhado_teste_b():
    # Teste B: 80 m², o resto padrão (cerâmica, inclinação 30, perda 5)
    resultado = calcular_telhado(80)
    assert resultado['tipo_telha'] == 'ceramica'
    assert resultado['inclinacao_percentual'] == 30.0
    assert resultado['area_real_m2'] == 83.52
    assert resultado['telhas'] == 1404
    assert resultado['cumeeiras'] == 0
    assert resultado['incluiu_madeiramento'] == False


def test_telhado_com_cumeeira():
    # B2: igual ao B + 10 m de cumeeira
    resultado = calcular_telhado(80, cumeeira_m=10)
    assert resultado['cumeeiras'] == 32


def test_telhado_com_madeiramento():
    # B3: igual ao B + madeiramento
    resultado = calcular_telhado(80, incluir_madeiramento=True)
    assert resultado['ripas_m'] == 263.1
    assert resultado['caibros_m'] == 175.4
    assert resultado['tercas_m'] == 52.6


def test_telhado_fibrocimento():
    # B4: fibrocimento
    resultado = calcular_telhado(80, "fibrocimento")
    assert resultado['inclinacao_percentual'] == 15.0
    assert resultado['telhas'] == 36


def test_telhado_concreto():
    # B5: telha de concreto
    resultado = calcular_telhado(80, "concreto")
    assert resultado['inclinacao_percentual'] == 30.0
    assert resultado['telhas'] == 921


def test_telhado_inclinacao_zero():
    # Inclinação 0: área real igual à de planta
    resultado = calcular_telhado(80, inclinacao_percentual=0)
    assert resultado['area_real_m2'] == 80.0
    assert resultado['telhas'] == 1344


def test_telhado_perda_2_virgula_5():
    # Perda 2,5
    resultado = calcular_telhado(80, perda_percentual=2.5)
    assert resultado['telhas'] == 1370


def test_telhado_cumeeira_pequena():
    # Cumeeira de 0,3 m: 1 peça
    resultado = calcular_telhado(80, cumeeira_m=0.3)
    assert resultado['cumeeiras'] == 1

# ------------------------------------------------------------------
# Erros: a função não pode travar, tem que devolver a mensagem certa
# ------------------------------------------------------------------


def test_telhado_area_zero():
    # Área zero
    resultado = calcular_telhado(0)
    assert resultado == {"erro": "erro_area_zero"}


def test_telhado_inclinacao_negativa():
    # Inclinação negativa
    resultado = calcular_telhado(80, inclinacao_percentual=-30)
    assert resultado == {"erro": "erro_valores_negativos"}


def test_telhado_cumeeira_negativa():
    # Cumeeira negativa
    resultado = calcular_telhado(80, cumeeira_m=-10)
    assert resultado == {"erro": "erro_valores_negativos"}


def test_telhado_telha_invalida():
    # Telha que não existe
    resultado = calcular_telhado(80, "abc")
    assert resultado == {"erro": "erro_telha_invalida"}
