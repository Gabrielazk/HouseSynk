"""Testes da conta da aba Esquadrias, sem tela (testes unitários).

Cada teste chama a função de conta direto, com os valores dos testes do testes_rodada1.md,
e confere os resultados (assert). Os erros conferem a mensagem certa, sem travar.
Os limites com aviso (janela "Confira os valores") ficam na tela, não na conta: eles são
testados no test_rodada1.py.

Rodar (na pasta C:\\Calc\\Calculadora):
  env311\\Scripts\\python.exe -B -m pytest tests\\test_esquadrias.py -v
"""

from src.calculators.esquadrias import calcular_esquadrias


def test_esquadrias_teste_a():
    # Teste A: 3 portas de madeira, 1 de alumínio, 4 janelas de alumínio e 1 de vidro, com os 3 insumos
    resultado = calcular_esquadrias([{"tipo": "porta", "material": "madeira", "qtd": 3, "larg": 80, "alt": 210}, {"tipo": "porta", "material": "aluminio", "qtd": 1, "larg": 90, "alt": 210}, {"tipo": "janela", "material": "aluminio", "qtd": 4, "larg": 120, "alt": 100}, {"tipo": "janela", "material": "vidro", "qtd": 1, "larg": 60, "alt": 60}], espuma=True, parafusos=True, argamassa=True)
    assert resultado['portas'] == 4
    assert resultado['janelas'] == 5
    assert resultado['area_vaos_m2'] == 12.09
    assert resultado['perimetro_m'] == 40.1
    assert resultado['tubos_espuma'] == 7
    assert resultado['parafusos'] == 101
    assert resultado['argamassa_kg'] == 60.2
    assert resultado['sacos_argamassa'] == 4


def test_esquadrias_teste_b():
    # Teste B: 3 portas 80x210 e 2 janelas 120x100, sem insumos
    resultado = calcular_esquadrias([{"tipo": "porta", "material": "nao_informado", "qtd": 3, "larg": 80, "alt": 210}, {"tipo": "janela", "material": "nao_informado", "qtd": 2, "larg": 120, "alt": 100}])
    assert resultado['portas'] == 3
    assert resultado['janelas'] == 2
    assert resultado['area_vaos_m2'] == 7.44
    assert resultado['tubos_espuma'] == 0
    assert resultado['parafusos'] == 0
    assert resultado['sacos_argamassa'] == 0


def test_esquadrias_so_espuma():
    # B2: com espuma
    resultado = calcular_esquadrias([{"tipo": "porta", "material": "nao_informado", "qtd": 3, "larg": 80, "alt": 210}, {"tipo": "janela", "material": "nao_informado", "qtd": 2, "larg": 120, "alt": 100}], espuma=True)
    assert resultado['tubos_espuma'] == 4


def test_esquadrias_so_parafusos():
    # B3: com parafusos
    resultado = calcular_esquadrias([{"tipo": "porta", "material": "nao_informado", "qtd": 3, "larg": 80, "alt": 210}, {"tipo": "janela", "material": "nao_informado", "qtd": 2, "larg": 120, "alt": 100}], parafusos=True)
    assert resultado['parafusos'] == 60


def test_esquadrias_so_argamassa():
    # B4: com argamassa
    resultado = calcular_esquadrias([{"tipo": "porta", "material": "nao_informado", "qtd": 3, "larg": 80, "alt": 210}, {"tipo": "janela", "material": "nao_informado", "qtd": 2, "larg": 120, "alt": 100}], argamassa=True)
    assert resultado['argamassa_kg'] == 35.7
    assert resultado['sacos_argamassa'] == 2


def test_esquadrias_uma_porta():
    # C11: 1 porta com os 3 insumos
    resultado = calcular_esquadrias([{"tipo": "porta", "material": "nao_informado", "qtd": 1, "larg": 80, "alt": 210}], espuma=True, parafusos=True, argamassa=True)
    assert resultado['perimetro_m'] == 5.0
    assert resultado['tubos_espuma'] == 1
    assert resultado['parafusos'] == 13
    assert resultado['argamassa_kg'] == 7.5
    assert resultado['sacos_argamassa'] == 1

# ------------------------------------------------------------------
# Erros: a função não pode travar, tem que devolver a mensagem certa
# ------------------------------------------------------------------


def test_esquadrias_lista_vazia():
    # Lista vazia
    resultado = calcular_esquadrias([])
    assert resultado == {"erro": "erro_lista_esquadrias_vazia"}


def test_esquadrias_tipo_invalido():
    # Tipo que não existe
    resultado = calcular_esquadrias([{"tipo": "abc", "material": "nao_informado", "qtd": 1, "larg": 80, "alt": 210}])
    assert resultado == {"erro": "erro_tipo_material_invalido"}


def test_esquadrias_quantidade_zero():
    # Quantidade zero
    resultado = calcular_esquadrias([{"tipo": "porta", "material": "nao_informado", "qtd": 0, "larg": 80, "alt": 210}])
    assert resultado == {"erro": "erro_qtd_larg_alt_zero"}


def test_esquadrias_largura_zero():
    # Largura zero
    resultado = calcular_esquadrias([{"tipo": "porta", "material": "nao_informado", "qtd": 1, "larg": 0, "alt": 210}])
    assert resultado == {"erro": "erro_qtd_larg_alt_zero"}
