"""Testes da conta da aba Baldrame, sem tela (testes unitários).

Cada teste chama a função de conta direto, com os valores dos testes do testes_rodada1.md,
e confere os resultados (assert). Os erros conferem a mensagem certa, sem travar.
Os limites com aviso (janela "Confira os valores") ficam na tela, não na conta: eles são
testados no test_rodada1.py.

Rodar (no terminal, na pasta do app, a que tem o main.py):
  env311\\Scripts\\python.exe -B -m pytest tests\\abas\\test_baldrame.py -v
"""

from src.calculators.baldrame import calcular_baldrame


def test_baldrame_teste_a():
    # Teste A: 30 m, 20 x 40 cm, perda 8, traço 1:4:3, 6 barras de 12,5 mm, estribo a cada 15 cm, com impermeabilização
    resultado = calcular_baldrame(30, 20, 40, perda_percentual=8, traco="1:4:3", num_barras_longitudinais=6, bitola_mm=12.5, espacamento_estribo_cm=15, incluir_impermeabilizacao=True)
    assert resultado['volume_com_perda_m3'] == 2.592
    assert resultado['sacos_cimento'] == 15
    assert resultado['areia_m3'] == 1.94
    assert resultado['pedra_m3'] == 1.46
    assert resultado['traspasse_m'] == 6.0
    assert resultado['kg_longitudinal'] == 197.03
    assert resultado['barras_12m_longitudinal'] == 18
    assert resultado['kg_estribos'] == 34.39
    assert resultado['barras_12m_estribos'] == 19
    assert resultado['quilos_aco'] == 231.42
    assert resultado['arame_kg'] == 4.63
    assert resultado['area_imperm_m2'] == 30.0
    assert resultado['litros_imperm'] == 24.0
    assert resultado['latas_imperm'] == 1
    assert resultado['galoes_imperm'] == 2


def test_baldrame_teste_b():
    # Teste B: 12,5 m, 20 x 30 cm, só os obrigatórios (perda 5, traço 1:2:3)
    resultado = calcular_baldrame(12.5, 20, 30)
    assert resultado['volume_m3'] == 0.75
    assert resultado['volume_com_perda_m3'] == 0.788
    assert resultado['sacos_cimento'] == 6
    assert resultado['areia_m3'] == 0.39
    assert resultado['pedra_m3'] == 0.59
    assert resultado['incluiu_ferragem'] == False
    assert resultado['incluiu_impermeabilizacao'] == False


def test_baldrame_com_4_barras():
    # B2: igual ao B + 4 barras de 8 mm (passa de 12 m: tem emenda)
    resultado = calcular_baldrame(12.5, 20, 30, num_barras_longitudinais=4)
    assert resultado['traspasse_m'] == 1.28
    assert resultado['kg_longitudinal'] == 22.28
    assert resultado['barras_12m_longitudinal'] == 5
    assert resultado['kg_estribos'] == 8.64
    assert resultado['barras_12m_estribos'] == 5
    assert resultado['quilos_aco'] == 30.92
    assert resultado['arame_kg'] == 0.62


def test_baldrame_impermeabilizacao():
    # B3: igual ao B + impermeabilização
    resultado = calcular_baldrame(12.5, 20, 30, incluir_impermeabilizacao=True)
    assert resultado['area_imperm_m2'] == 10.0
    assert resultado['litros_imperm'] == 8.0
    assert resultado['latas_imperm'] == 0
    assert resultado['galoes_imperm'] == 3
    assert resultado['litros_compra_imperm'] == 10.8


def test_baldrame_12m_sem_emenda():
    # 12 m com 4 barras: ainda não tem emenda
    resultado = calcular_baldrame(12, 20, 30, num_barras_longitudinais=4)
    assert resultado['traspasse_m'] == 0.0
    assert resultado['barras_12m_longitudinal'] == 5


def test_baldrame_24m_uma_emenda():
    # 24 m com 4 barras: uma emenda por barra
    resultado = calcular_baldrame(24, 20, 30, num_barras_longitudinais=4)
    assert resultado['traspasse_m'] == 1.28
    assert resultado['barras_12m_longitudinal'] == 9


def test_baldrame_perda_2_virgula_5():
    # Perda 2,5
    resultado = calcular_baldrame(12.5, 20, 30, perda_percentual=2.5)
    assert resultado['volume_com_perda_m3'] == 0.769
    assert resultado['sacos_cimento'] == 6
    assert resultado['areia_m3'] == 0.38
    assert resultado['pedra_m3'] == 0.58

# ------------------------------------------------------------------
# Erros: a função não pode travar, tem que devolver a mensagem certa
# ------------------------------------------------------------------


def test_baldrame_altura_zero():
    # Altura zero
    resultado = calcular_baldrame(12.5, 20, 0)
    assert resultado == {"erro": "erro_valores_zero"}


def test_baldrame_comprimento_negativo():
    # Comprimento negativo
    resultado = calcular_baldrame(-5, 20, 30)
    assert resultado == {"erro": "erro_valores_zero"}


def test_baldrame_perda_negativa():
    # Perda negativa
    resultado = calcular_baldrame(12.5, 20, 30, perda_percentual=-2)
    assert resultado == {"erro": "erro_perda_negativa"}


def test_baldrame_viga_pequena_com_ferro():
    # Largura 4 cm com ferro: não cabe o estribo
    resultado = calcular_baldrame(12.5, 4, 30, num_barras_longitudinais=4)
    assert resultado == {"erro": "erro_viga_pequena_estribos"}


def test_baldrame_barras_negativas():
    # Barras negativas
    resultado = calcular_baldrame(12.5, 20, 30, num_barras_longitudinais=-4)
    assert resultado == {"erro": "erro_barras_estribos_negativos"}


def test_baldrame_traco_invalido():
    # Traço que não existe
    resultado = calcular_baldrame(12.5, 20, 30, traco="abc")
    assert resultado == {"erro": "erro_traco_concreto_invalido"}
