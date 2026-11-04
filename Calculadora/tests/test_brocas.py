"""Testes da conta da aba Brocas, sem tela (testes unitários).

Cada teste chama a função de conta direto, com os valores dos testes do testes_rodada1.md,
e confere os resultados (assert). Os erros conferem a mensagem certa, sem travar.
Os limites com aviso (janela "Confira os valores") ficam na tela, não na conta: eles são
testados no test_rodada1.py.

Rodar (na pasta C:\\Calc\\Calculadora):
  env311\\Scripts\\python.exe -B -m pytest tests\\test_brocas.py -v
"""

from src.calculators.brocas import calcular_brocas


def test_brocas_teste_a():
    # Teste A: 12 brocas de 25 cm com 3,5 m, perda 12, traço 1:3:3, 4 barras de 10 mm, estribo a cada 15 cm e mão de obra R$ 30/m
    resultado = calcular_brocas(12, 3.5, 25, perda_percentual=12, incluir_ferragem=True, num_barras_longitudinais=4, bitola_mm=10.0, preco_mao_obra_metro=30.0, traco="1:3:3", espacamento_estribo_cm=15)
    assert resultado['volume_com_perda_m3'] == 2.309
    assert resultado['sacos_cimento'] == 15
    assert resultado['areia_m3'] == 1.48
    assert resultado['pedra_m3'] == 1.48
    assert resultado['altura_gaiola_m'] == 1.75
    assert resultado['kg_longitudinal'] == 57.01
    assert resultado['barras_12m_longitudinal'] == 8
    assert resultado['kg_estribos'] == 14.8
    assert resultado['barras_12m_estribos'] == 9
    assert resultado['quilos_aco'] == 71.81
    assert resultado['arame_kg'] == 1.44
    assert resultado['custo_mao_obra'] == 1260.0


def test_brocas_teste_b():
    # Teste B: 10 brocas de 20 cm com 3 m, só os obrigatórios (perda 10, traço 1:2:3, sem ferro)
    resultado = calcular_brocas(10, 3, 20)
    assert resultado['volume_nominal_m3'] == 0.942
    assert resultado['volume_com_perda_m3'] == 1.037
    assert resultado['sacos_cimento'] == 8
    assert resultado['areia_m3'] == 0.52
    assert resultado['pedra_m3'] == 0.78
    assert resultado['incluiu_ferragem'] == False


def test_brocas_com_4_barras():
    # B2: igual ao B + 4 barras de 8 mm (estribo padrão a cada 20 cm)
    resultado = calcular_brocas(10, 3, 20, incluir_ferragem=True, num_barras_longitudinais=4)
    assert resultado['altura_gaiola_m'] == 1.5
    assert resultado['kg_longitudinal'] == 26.07
    assert resultado['barras_12m_longitudinal'] == 6
    assert resultado['kg_estribos'] == 6.31
    assert resultado['barras_12m_estribos'] == 4
    assert resultado['quilos_aco'] == 32.38
    assert resultado['arame_kg'] == 0.65


def test_brocas_sem_estribo():
    # 4 barras com espaçamento 0: sem estribos
    resultado = calcular_brocas(10, 3, 20, incluir_ferragem=True, num_barras_longitudinais=4, espacamento_estribo_cm=0)
    assert resultado['incluiu_estribos'] == False
    assert resultado['kg_estribos'] == 0.0
    assert resultado['quilos_aco'] == 26.07


def test_brocas_perda_2_virgula_5():
    # Perda 2,5
    resultado = calcular_brocas(10, 3, 20, perda_percentual=2.5)
    assert resultado['volume_com_perda_m3'] == 0.966
    assert resultado['sacos_cimento'] == 8


def test_brocas_profundidade_30m():
    # 30 m: ainda calcula (o aviso de limite é na tela, não na conta)
    resultado = calcular_brocas(10, 30, 20)
    assert resultado['volume_com_perda_m3'] == 10.367
    assert resultado['sacos_cimento'] == 78

# ------------------------------------------------------------------
# Erros: a função não pode travar, tem que devolver a mensagem certa
# ------------------------------------------------------------------


def test_brocas_quantidade_zero():
    # Quantidade zero
    resultado = calcular_brocas(0, 3, 20)
    assert resultado == {"erro": 'Quantidade, profundidade e diâmetro devem ser maiores que zero.'}


def test_brocas_profundidade_negativa():
    # Profundidade negativa
    resultado = calcular_brocas(10, -3, 20)
    assert resultado == {"erro": 'Quantidade, profundidade e diâmetro devem ser maiores que zero.'}


def test_brocas_perda_negativa():
    # Perda negativa
    resultado = calcular_brocas(10, 3, 20, perda_percentual=-5)
    assert resultado == {"erro": 'A perda não pode ser negativa.'}


def test_brocas_diametro_pequeno_com_ferro():
    # Diâmetro 4 cm com ferro: não cabe o estribo
    resultado = calcular_brocas(10, 3, 4, incluir_ferragem=True, num_barras_longitudinais=4)
    assert resultado == {"erro": 'Diâmetro muito pequeno para colocar estribos.'}


def test_brocas_barras_negativas():
    # Barras negativas
    resultado = calcular_brocas(10, 3, 20, incluir_ferragem=True, num_barras_longitudinais=-4)
    assert resultado == {"erro": 'Barras e espaçamento dos estribos não podem ser negativos.'}


def test_brocas_traco_invalido():
    # Traço que não existe
    resultado = calcular_brocas(10, 3, 20, traco="abc")
    assert resultado == {"erro": 'Traço de concreto inválido.'}


def test_brocas_bitola_invalida():
    # Bitola que não existe
    resultado = calcular_brocas(10, 3, 20, incluir_ferragem=True, num_barras_longitudinais=4, bitola_mm=7.0)
    assert resultado == {"erro": 'Bitola do ferro inválida.'}
