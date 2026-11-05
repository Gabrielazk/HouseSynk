"""Testes da conta da aba Piso, sem tela (testes unitários).

Cada teste chama a função de conta direto, com os valores dos testes do testes_rodada1.md,
e confere os resultados (assert). Os erros conferem a mensagem certa, sem travar.
Os limites com aviso (janela "Confira os valores") ficam na tela, não na conta: eles são
testados no test_rodada1.py.

Rodar (na pasta C:\\Calc\\Calculadora):
  env311\\Scripts\\python.exe -B -m pytest tests\\abas\\test_piso.py -v
"""

from src.calculators.revestimento import calcular_piso


def test_piso_teste_a():
    # Teste A: 40 m², peça 60x60, 2,16 m² por caixa, AC-II, perda 12, rodapé 30 m em peças de 0,6 m, com desenho
    resultado = calcular_piso(40, 60, 60, m2_por_caixa=2.16, tipo_argamassa="AC-II", perda_percentual=12, rodape_m=30, desenho=True, rodape_peca_m=0.6)
    assert resultado['perda_percentual'] == 12
    assert resultado['area_com_perda_m2'] == 44.8
    assert resultado['pecas'] == 125
    assert resultado['caixas'] == 21
    assert resultado['argamassa_kg'] == 224.0
    assert resultado['sacos_argamassa'] == 12
    assert resultado['rodape_m'] == 33.6
    assert resultado['rodape_pecas'] == 56


def test_piso_teste_b():
    # Teste B: 40 m², peça 60x60, o resto padrão (perda automática 10%, AC-I)
    resultado = calcular_piso(40, 60, 60)
    assert resultado['perda_percentual'] == 10.0
    assert resultado['perda_automatica'] == True
    assert resultado['area_com_perda_m2'] == 44.0
    assert resultado['pecas'] == 123
    assert resultado['caixas'] == 0
    assert resultado['consumo_argamassa_kg_m2'] == 5.0
    assert resultado['argamassa_kg'] == 220.0
    assert resultado['sacos_argamassa'] == 11


def test_piso_peca_80():
    # B2: peça 80x80 (perda 15% e 8 kg/m² de argamassa)
    resultado = calcular_piso(40, 80, 80)
    assert resultado['perda_percentual'] == 15.0
    assert resultado['area_com_perda_m2'] == 46.0
    assert resultado['pecas'] == 72
    assert resultado['consumo_argamassa_kg_m2'] == 8.0
    assert resultado['sacos_argamassa'] == 19


def test_piso_peca_120x60():
    # B3: peça 120x60 (perda 20%)
    resultado = calcular_piso(40, 120, 60)
    assert resultado['perda_percentual'] == 20.0
    assert resultado['pecas'] == 67
    assert resultado['sacos_argamassa'] == 20


def test_piso_com_desenho():
    # B4: com desenho (perda 25%)
    resultado = calcular_piso(40, 60, 60, desenho=True)
    assert resultado['perda_percentual'] == 25.0
    assert resultado['area_com_perda_m2'] == 50.0
    assert resultado['pecas'] == 139


def test_piso_com_caixa():
    # B5: 2,16 m² por caixa
    resultado = calcular_piso(40, 60, 60, m2_por_caixa=2.16)
    assert resultado['pecas'] == 123
    assert resultado['caixas'] == 21


def test_piso_rodape_sem_peca():
    # B6: rodapé de 30 m sem o tamanho da peça
    resultado = calcular_piso(40, 60, 60, rodape_m=30)
    assert resultado['rodape_m'] == 33.0
    assert resultado['rodape_pecas'] == 0


def test_piso_rodape_com_peca():
    # B7: rodapé de 30 m em peças de 0,6 m
    resultado = calcular_piso(40, 60, 60, rodape_m=30, rodape_peca_m=0.6)
    assert resultado['rodape_m'] == 33.0
    assert resultado['rodape_pecas'] == 55


def test_piso_perda_digitada():
    # Perda digitada 2,5 (vale o que a pessoa digitou)
    resultado = calcular_piso(40, 60, 60, perda_percentual=2.5)
    assert resultado['perda_percentual'] == 2.5
    assert resultado['perda_automatica'] == False
    assert resultado['area_com_perda_m2'] == 41.0
    assert resultado['pecas'] == 114


def test_piso_peca_70():
    # Peça 70x70: ainda 10%
    resultado = calcular_piso(40, 70, 70)
    assert resultado['perda_percentual'] == 10.0
    assert resultado['pecas'] == 90


def test_piso_peca_90():
    # Peça 90x90: 15%
    resultado = calcular_piso(40, 90, 90)
    assert resultado['perda_percentual'] == 15.0
    assert resultado['pecas'] == 57

# ------------------------------------------------------------------
# Erros: a função não pode travar, tem que devolver a mensagem certa
# ------------------------------------------------------------------


def test_piso_area_zero():
    # Área zero
    resultado = calcular_piso(0, 60, 60)
    assert resultado == {"erro": "erro_area_peca_zero"}


def test_piso_peca_zero():
    # Peça com lado zero
    resultado = calcular_piso(40, 0, 60)
    assert resultado == {"erro": "erro_area_peca_zero"}


def test_piso_perda_negativa():
    # Perda negativa
    resultado = calcular_piso(40, 60, 60, perda_percentual=-5)
    assert resultado == {"erro": "erro_perda_negativa"}


def test_piso_caixa_negativa():
    # m² por caixa negativo
    resultado = calcular_piso(40, 60, 60, m2_por_caixa=-2)
    assert resultado == {"erro": "erro_valores_negativos"}


def test_piso_argamassa_invalida():
    # Argamassa que não existe
    resultado = calcular_piso(40, 60, 60, tipo_argamassa="abc")
    assert resultado == {"erro": "erro_argamassa_invalida"}
