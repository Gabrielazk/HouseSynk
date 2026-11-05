"""Testes da conta da aba Laje, sem tela (testes unitários).

Cada teste chama a função de conta direto, com os valores dos testes do testes_rodada1.md,
e confere os resultados (assert). Os erros conferem a mensagem certa, sem travar.
Os limites com aviso (janela "Confira os valores") ficam na tela, não na conta: eles são
testados no test_rodada1.py.

Rodar (na pasta C:\\Calc\\Calculadora):
  env311\\Scripts\\python.exe -B -m pytest tests\\abas\\test_laje.py -v
"""

from src.calculators.laje import calcular_laje


def test_laje_teste_a():
    # Teste A: 50 m², pré-moldada com lajota, capa 5, perda 8, traço 1:3:3, com tela soldada
    resultado = calcular_laje(50, "premoldada", "lajota", capa_cm=5, perda_percentual=8, traco="1:3:3", tela_soldada=True)
    assert resultado['volume_com_perda_m3'] == 3.348
    assert resultado['laje_premoldada_m2'] == 50
    assert resultado['lajotas'] == 648
    assert resultado['sacos_cimento'] == 22
    assert resultado['areia_m3'] == 2.15
    assert resultado['pedra_m3'] == 2.15
    assert resultado['tela_m2'] == 55.0
    assert resultado['tela_paineis'] == 10


def test_laje_macica_teste_a2():
    # A2: 30 m², maciça de 10 cm, perda 7, traço 1,5:5:5
    resultado = calcular_laje(30, "macica", espessura_cm=10, perda_percentual=7, traco="1.5:5:5")
    assert resultado['volume_com_perda_m3'] == 3.21
    assert resultado['laje_premoldada_m2'] == 0.0
    assert resultado['sacos_cimento'] == 19
    assert resultado['areia_m3'] == 2.09
    assert resultado['pedra_m3'] == 2.09


def test_laje_teste_b():
    # Teste B: 50 m², o resto padrão (pré-moldada, isopor, capa 4, perda 5, traço 1:2:3, sem tela)
    resultado = calcular_laje(50)
    assert resultado['tipo'] == 'premoldada'
    assert resultado['enchimento'] == 'eps'
    assert resultado['capa_cm'] == 4.0
    assert resultado['volume_com_perda_m3'] == 2.73
    assert resultado['laje_premoldada_m2'] == 50
    assert resultado['lajotas'] == 0
    assert resultado['sacos_cimento'] == 21
    assert resultado['areia_m3'] == 1.37
    assert resultado['pedra_m3'] == 2.05
    assert resultado['incluiu_tela'] == False


def test_laje_macica_teste_b2():
    # B2: 30 m², maciça de 10 cm
    resultado = calcular_laje(30, "macica", espessura_cm=10)
    assert resultado['volume_com_perda_m3'] == 3.15
    assert resultado['sacos_cimento'] == 24
    assert resultado['areia_m3'] == 1.58
    assert resultado['pedra_m3'] == 2.36


def test_laje_com_tela():
    # B3: igual ao B + tela soldada
    resultado = calcular_laje(50, tela_soldada=True)
    assert resultado['tela_m2'] == 55.0
    assert resultado['tela_paineis'] == 10


def test_laje_com_lajota():
    # B4: igual ao B com lajota
    resultado = calcular_laje(50, enchimento="lajota")
    assert resultado['lajotas'] == 630
    assert resultado['laje_premoldada_m2'] == 50


def test_laje_perda_2_virgula_5():
    # Perda 2,5
    resultado = calcular_laje(50, perda_percentual=2.5)
    assert resultado['volume_com_perda_m3'] == 2.665
    assert resultado['sacos_cimento'] == 20

# ------------------------------------------------------------------
# Erros: a função não pode travar, tem que devolver a mensagem certa
# ------------------------------------------------------------------


def test_laje_area_zero():
    # Área zero
    resultado = calcular_laje(0)
    assert resultado == {"erro": "erro_area_zero"}


def test_laje_capa_zero():
    # Capa zero
    resultado = calcular_laje(50, capa_cm=0)
    assert resultado == {"erro": "erro_capa_zero"}


def test_laje_macica_sem_espessura():
    # Maciça sem espessura
    resultado = calcular_laje(50, "macica")
    assert resultado == {"erro": "erro_espessura_macica"}


def test_laje_perda_negativa():
    # Perda negativa
    resultado = calcular_laje(50, perda_percentual=-5)
    assert resultado == {"erro": "erro_perda_negativa"}


def test_laje_tipo_invalido():
    # Tipo que não existe
    resultado = calcular_laje(50, "abc")
    assert resultado == {"erro": "erro_tipo_laje_invalido"}


def test_laje_enchimento_invalido():
    # Enchimento que não existe
    resultado = calcular_laje(50, enchimento="abc")
    assert resultado == {"erro": "erro_enchimento_invalido"}


def test_laje_traco_invalido():
    # Traço que não existe
    resultado = calcular_laje(50, traco="abc")
    assert resultado == {"erro": "erro_traco_concreto_invalido"}
