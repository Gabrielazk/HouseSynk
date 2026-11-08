"""Testes da conta da aba Reboco, sem tela (testes unitários).

Cada teste chama a função de conta direto, com os valores dos testes do testes_rodada1.md,
e confere os resultados (assert). Os erros conferem a mensagem certa, sem travar.
Os limites com aviso (janela "Confira os valores") ficam na tela, não na conta: eles são
testados no test_rodada1.py.

Rodar (no terminal, na pasta do app, a que tem o main.py):
  env311\\Scripts\\python.exe -B -m pytest tests\\abas\\test_reboco.py -v
"""

from src.calculators.reboco import calcular_reboco


def test_reboco_teste_a():
    # Teste A: 30 m², espessura 2,5, vãos 5, dois lados, chapisco, perda 12, traço 1:0,5:6
    resultado = calcular_reboco(30, espessura_cm=2.5, desconto_vaos_m2=5, dois_lados=True, chapisco=True, perda_percentual=12, traco="1:0.5:6")
    assert resultado['area_liquida_m2'] == 25
    assert resultado['area_rebocada_m2'] == 50
    assert resultado['volume_reboco_m3'] == 1.4
    assert resultado['volume_chapisco_m3'] == 0.28
    assert resultado['sacos_cimento'] == 8
    assert resultado['sacos_cal'] == 6
    assert resultado['areia_m3'] == 1.66


def test_reboco_teste_b():
    # Teste B: 30 m², o resto padrão (espessura 2, perda 10, traço 1:2:8)
    resultado = calcular_reboco(30)
    assert resultado['area_rebocada_m2'] == 30.0
    assert resultado['espessura_cm'] == 2.0
    assert resultado['volume_reboco_m3'] == 0.66
    assert resultado['sacos_cimento'] == 2
    assert resultado['sacos_cal'] == 7
    assert resultado['areia_m3'] == 0.6


def test_reboco_com_vaos():
    # B2: com 5 m² de vãos
    resultado = calcular_reboco(30, desconto_vaos_m2=5)
    assert resultado['area_liquida_m2'] == 25
    assert resultado['volume_reboco_m3'] == 0.55
    assert resultado['sacos_cimento'] == 2
    assert resultado['sacos_cal'] == 6
    assert resultado['areia_m3'] == 0.5


def test_reboco_dois_lados():
    # B3: os dois lados (dobra a área)
    resultado = calcular_reboco(30, dois_lados=True)
    assert resultado['area_rebocada_m2'] == 60.0
    assert resultado['volume_reboco_m3'] == 1.32
    assert resultado['sacos_cimento'] == 4


def test_reboco_com_chapisco():
    # B4: com chapisco
    resultado = calcular_reboco(30, chapisco=True)
    assert resultado['volume_chapisco_m3'] == 0.165
    assert resultado['sacos_cimento'] == 4
    assert resultado['areia_m3'] == 0.75


def test_reboco_traco_sem_cal():
    # B5: traço 1:0:3 (sem cal)
    resultado = calcular_reboco(30, traco="1:0:3")
    assert resultado['sacos_cimento'] == 5
    assert resultado['sacos_cal'] == 0
    assert resultado['areia_m3'] == 0.62


def test_reboco_perda_2_virgula_5():
    # Perda 2,5
    resultado = calcular_reboco(30, perda_percentual=2.5)
    assert resultado['volume_reboco_m3'] == 0.615
    assert resultado['areia_m3'] == 0.56

# ------------------------------------------------------------------
# Erros: a função não pode travar, tem que devolver a mensagem certa
# ------------------------------------------------------------------


def test_reboco_area_zero():
    # Área zero
    resultado = calcular_reboco(0)
    assert resultado == {"erro": "erro_area_espessura_zero"}


def test_reboco_espessura_zero():
    # Espessura zero
    resultado = calcular_reboco(30, espessura_cm=0)
    assert resultado == {"erro": "erro_area_espessura_zero"}


def test_reboco_vaos_igual_area():
    # Vãos iguais à área
    resultado = calcular_reboco(30, desconto_vaos_m2=30)
    assert resultado == {"erro": "erro_desconto_vaos"}


def test_reboco_vaos_negativos():
    # Vãos negativos
    resultado = calcular_reboco(30, desconto_vaos_m2=-5)
    assert resultado == {"erro": "erro_desconto_perda_negativos"}


def test_reboco_perda_negativa():
    # Perda negativa
    resultado = calcular_reboco(30, perda_percentual=-5)
    assert resultado == {"erro": "erro_desconto_perda_negativos"}


def test_reboco_traco_invalido():
    # Traço que não existe
    resultado = calcular_reboco(30, traco="abc")
    assert resultado == {"erro": "erro_traco_massa_invalido"}
