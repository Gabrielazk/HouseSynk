"""Testes da conta da aba Pintura, sem tela (testes unitários).

Cada teste chama a função de conta direto, com os valores dos testes do testes_rodada1.md,
e confere os resultados (assert). Os erros conferem a mensagem certa, sem travar.
Os limites com aviso (janela "Confira os valores") ficam na tela, não na conta: eles são
testados no test_rodada1.py.

Rodar (na pasta C:\\Calc\\Calculadora):
  env311\\Scripts\\python.exe -B -m pytest tests\\abas\\test_pintura.py -v
"""

from src.calculators.pintura import calcular_pintura


def test_pintura_teste_a():
    # Teste A: 100 m² de parede e 40 de teto, 3 demãos, rendimento 10, perda 15, com selador, massa corrida e fundo
    resultado = calcular_pintura(100, 40, demaos=3, rendimento_m2_l=10, perda_percentual=15, selador=True, massa="corrida", fundo=True)
    assert resultado['itens'] == {'parede': {'litros': 34.5, 'latas': 2, 'galoes': 0},
                                  'teto': {'litros': 13.8, 'latas': 0, 'galoes': 4},
                                  'selador': {'litros': 20.1, 'latas': 1, 'galoes': 1},
                                  'fundo': {'litros': 16.1, 'latas': 1, 'galoes': 0}}
    assert resultado['massa_kg'] == 161.0
    assert resultado['baldes_massa'] == 7


def test_pintura_teste_b():
    # Teste B: 100 m² de parede, o resto padrão (2 demãos, rendimento 12, perda 10)
    resultado = calcular_pintura(100, 0)
    assert resultado['demaos'] == 2
    assert resultado['rendimento_m2_l'] == 12.0
    assert resultado['itens'] == {'parede': {'litros': 18.3, 'latas': 1, 'galoes': 1}}
    assert resultado['baldes_massa'] == 0


def test_pintura_so_teto():
    # B2: só 40 m² de teto
    resultado = calcular_pintura(0, 40)
    assert resultado['itens'] == {'teto': {'litros': 7.3, 'latas': 0, 'galoes': 3}}


def test_pintura_parede_e_teto():
    # B3: 100 de parede e 40 de teto
    resultado = calcular_pintura(100, 40)
    assert resultado['itens'] == {'parede': {'litros': 18.3, 'latas': 1, 'galoes': 1},
                                  'teto': {'litros': 7.3, 'latas': 0, 'galoes': 3}}


def test_pintura_com_selador():
    # B4: com selador
    resultado = calcular_pintura(100, 0, selador=True)
    assert resultado['itens'] == {'parede': {'litros': 18.3, 'latas': 1, 'galoes': 1},
                                  'selador': {'litros': 13.8, 'latas': 0, 'galoes': 4}}


def test_pintura_massa_acrilica():
    # B5: massa acrílica (2 demãos)
    resultado = calcular_pintura(100, 0, massa="acrilica")
    assert resultado['massa_kg'] == 110.0
    assert resultado['baldes_massa'] == 5


def test_pintura_com_fundo():
    # B6: com fundo preparador
    resultado = calcular_pintura(100, 0, fundo=True)
    assert resultado['itens'] == {'parede': {'litros': 18.3, 'latas': 1, 'galoes': 1},
                                  'fundo': {'litros': 11.0, 'latas': 0, 'galoes': 4}}


def test_pintura_5_galoes_viram_lata():
    # B7: 180 m² (5 galões viram mais uma lata)
    resultado = calcular_pintura(180, 0)
    assert resultado['itens'] == {'parede': {'litros': 33.0, 'latas': 2, 'galoes': 0}}


def test_pintura_area_pequena():
    # B8: 10 m² (só galão)
    resultado = calcular_pintura(10, 0)
    assert resultado['itens'] == {'parede': {'litros': 1.8, 'latas': 0, 'galoes': 1}}


def test_pintura_6_demaos():
    # 6 demãos: a conta funciona (o aviso de limite é na tela)
    resultado = calcular_pintura(100, 0, demaos=6)
    assert resultado['itens'] == {'parede': {'litros': 55.0, 'latas': 3, 'galoes': 1}}


def test_pintura_perda_2_virgula_5():
    # Perda 2,5
    resultado = calcular_pintura(100, 0, perda_percentual=2.5)
    assert resultado['itens'] == {'parede': {'litros': 17.1, 'latas': 1, 'galoes': 0}}

# ------------------------------------------------------------------
# Erros: a função não pode travar, tem que devolver a mensagem certa
# ------------------------------------------------------------------


def test_pintura_sem_area():
    # Sem parede e sem teto
    resultado = calcular_pintura(0, 0)
    assert resultado == {"erro": "erro_area_parede_ou_teto"}


def test_pintura_area_negativa():
    # Área negativa
    resultado = calcular_pintura(-100, 0)
    assert resultado == {"erro": "erro_areas_negativas"}


def test_pintura_demaos_zero():
    # Demãos zero
    resultado = calcular_pintura(100, 0, demaos=0)
    assert resultado == {"erro": "erro_demaos_rendimento_zero"}


def test_pintura_rendimento_zero():
    # Rendimento zero
    resultado = calcular_pintura(100, 0, rendimento_m2_l=0)
    assert resultado == {"erro": "erro_demaos_rendimento_zero"}


def test_pintura_perda_negativa():
    # Perda negativa
    resultado = calcular_pintura(100, 0, perda_percentual=-5)
    assert resultado == {"erro": "erro_perda_negativa"}


def test_pintura_massa_invalida():
    # Massa que não existe
    resultado = calcular_pintura(100, 0, massa="abc")
    assert resultado == {"erro": "erro_massa_invalida"}
