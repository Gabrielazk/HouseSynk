"""Testes da conta da aba Paredes, sem tela (testes unitários).

Cada teste chama a função de conta direto, com os valores dos testes do testes_rodada1.md,
e confere os resultados (assert). Os erros conferem a mensagem certa, sem travar.
Os limites com aviso (janela "Confira os valores") ficam na tela, não na conta: eles são
testados no test_rodada1.py.

Rodar (na pasta C:\\Calc\\Calculadora):
  env311\\Scripts\\python.exe -B -m pytest tests\\test_paredes.py -v
"""

from src.calculators.paredes import calcular_paredes


def test_paredes_teste_a():
    # Teste A: 80 m², bloco 14x19x39 deitado, vãos 12,5, junta 1,5, quebra 8, traço 1:0,5:6
    resultado = calcular_paredes(80, tijolo="bloco_14", assentamento="deitado", desconto_vaos_m2=12.5, junta_cm=1.5, quebra_percentual=8, traco="1:0.5:6")
    assert resultado['area_liquida_m2'] == 67.5
    assert resultado['unidades'] == 1162
    assert resultado['milheiros'] == 1.16
    assert resultado['sacos_cimento'] == 8
    assert resultado['sacos_cal'] == 7
    assert resultado['areia_m3'] == 1.84


def test_paredes_teste_b():
    # Teste B: 30 m², o resto padrão (tijolo baiano, em pé, junta 1, quebra 5, traço 1:2:8)
    resultado = calcular_paredes(30)
    assert resultado['area_liquida_m2'] == 30.0
    assert resultado['tijolo'] == 'baiano'
    assert resultado['assentamento'] == 'em_pe'
    assert resultado['unidades'] == 788
    assert resultado['milheiros'] == 0.79
    assert resultado['sacos_cimento'] == 1
    assert resultado['sacos_cal'] == 3
    assert resultado['areia_m3'] == 0.26


def test_paredes_bloco_19():
    # B2: bloco de concreto 19x19x39
    resultado = calcular_paredes(30, tijolo="bloco_19")
    assert resultado['unidades'] == 394
    assert resultado['sacos_cimento'] == 2
    assert resultado['sacos_cal'] == 5
    assert resultado['areia_m3'] == 0.42


def test_paredes_baiano_9_furos_deitado():
    # B3: tijolo baiano 9 furos deitado
    resultado = calcular_paredes(30, tijolo="baiano_9f", assentamento="deitado")
    assert resultado['unidades'] == 1575
    assert resultado['milheiros'] == 1.58
    assert resultado['sacos_cimento'] == 2
    assert resultado['sacos_cal'] == 7
    assert resultado['areia_m3'] == 0.61


def test_paredes_traco_sem_cal():
    # B4: traço 1:0:3 (sem cal)
    resultado = calcular_paredes(30, traco="1:0:3")
    assert resultado['sacos_cimento'] == 3
    assert resultado['sacos_cal'] == 0
    assert resultado['areia_m3'] == 0.27


def test_paredes_com_vaos():
    # Com 5 m² de vãos
    resultado = calcular_paredes(30, desconto_vaos_m2=5)
    assert resultado['area_liquida_m2'] == 25.0
    assert resultado['unidades'] == 657


def test_paredes_quebra_2_virgula_5():
    # Quebra 2,5
    resultado = calcular_paredes(30, quebra_percentual=2.5)
    assert resultado['unidades'] == 769


def test_paredes_junta_zero():
    # Junta 0: só os tijolos, sem massa
    resultado = calcular_paredes(30, junta_cm=0)
    assert resultado['unidades'] == 873
    assert resultado['sacos_cimento'] == 0
    assert resultado['sacos_cal'] == 0
    assert resultado['areia_m3'] == 0.0

# ------------------------------------------------------------------
# Erros: a função não pode travar, tem que devolver a mensagem certa
# ------------------------------------------------------------------


def test_paredes_area_zero():
    # Área zero
    resultado = calcular_paredes(0)
    assert resultado == {"erro": 'A área da parede deve ser maior que zero.'}


def test_paredes_vaos_igual_area():
    # Vãos iguais à área
    resultado = calcular_paredes(30, desconto_vaos_m2=30)
    assert resultado == {"erro": 'O desconto de vãos deve ser menor que a área.'}


def test_paredes_vaos_negativos():
    # Vãos negativos
    resultado = calcular_paredes(30, desconto_vaos_m2=-5)
    assert resultado == {"erro": 'Desconto, junta e quebra não podem ser negativos.'}


def test_paredes_quebra_negativa():
    # Quebra negativa
    resultado = calcular_paredes(30, quebra_percentual=-5)
    assert resultado == {"erro": 'Desconto, junta e quebra não podem ser negativos.'}


def test_paredes_tijolo_invalido():
    # Tijolo que não existe
    resultado = calcular_paredes(30, tijolo="abc")
    assert resultado == {"erro": 'Tipo de tijolo ou bloco inválido.'}


def test_paredes_assentamento_invalido():
    # Assentamento que não existe
    resultado = calcular_paredes(30, assentamento="abc")
    assert resultado == {"erro": 'Assentamento inválido.'}


def test_paredes_traco_invalido():
    # Traço que não existe
    resultado = calcular_paredes(30, traco="abc")
    assert resultado == {"erro": 'Traço da massa inválido.'}
