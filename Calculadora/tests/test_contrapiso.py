"""Testes da conta do Contrapiso (src/calculators/contrapiso.py), sem tela.

Os dois primeiros testes foram escritos pela Gabi (04/11/2026), o primeiro teste dela no pytest.
Os outros completam: todos os resultados (volume, cimento, areia e brita), os 4 traços, números
quebrados e as mensagens de erro. Os resultados batem com o testes_rodada1.md (Contrapiso).

Rodar (na pasta C:\\Calc\\Calculadora):
  env311\\Scripts\\python.exe -B -m pytest tests\\test_contrapiso.py -v
"""
import pytest

from src.calculators.contrapiso import calcular_contrapiso


# ------------------------------------------------------------------
# Os dois primeiros testes da Gabi
# ------------------------------------------------------------------
def test_contrapiso_padrao():
    resultado = calcular_contrapiso(40, 6)
    assert resultado["sacos_cimento"] == 17
    assert resultado["volume_com_perda_m3"] == 2.52
    assert resultado["areia_m3"] == 1.62
    assert resultado["pedra_m3"] == 1.62


def test_contrapiso_todos_os_campos():
    # Teste A do roteiro: área 40, espessura 6, perda 8, traço 1:2:3
    resultado = calcular_contrapiso(40, 6, 8, "1:2:3")
    assert resultado["sacos_cimento"] == 20
    assert resultado["volume_com_perda_m3"] == 2.592
    assert resultado["areia_m3"] == 1.3
    assert resultado["pedra_m3"] == 1.94


# ------------------------------------------------------------------
# Teste B do roteiro: só os obrigatórios (perda 5 e traço 1:3:3 são o padrão)
# ------------------------------------------------------------------
def test_contrapiso_teste_b():
    resultado = calcular_contrapiso(40, 5)
    assert resultado["area_m2"] == 40
    assert resultado["volume_m3"] == 2.0              # 40 m² x 0,05 m, sem perda
    assert resultado["volume_com_perda_m3"] == 2.1    # + 5% de perda
    assert resultado["sacos_cimento"] == 14
    assert resultado["areia_m3"] == 1.35
    assert resultado["pedra_m3"] == 1.35


def test_contrapiso_valores_padrao():
    # Sem informar perda e traço, a função tem que usar 5% e 1:3:3 (confirmado pelo engenheiro)
    resultado = calcular_contrapiso(40, 5)
    assert resultado["perda_percentual"] == 5
    assert resultado["traco"] == "1:3:3"


# ------------------------------------------------------------------
# Os traços do menu
# ------------------------------------------------------------------
def test_contrapiso_traco_1_5_5_5():
    # B2 do roteiro: traço 1,5:5:5 (por dentro ele é guardado com ponto: "1.5:5:5")
    resultado = calcular_contrapiso(40, 5, 5, "1.5:5:5")
    assert resultado["sacos_cimento"] == 13
    assert resultado["areia_m3"] == 1.37
    assert resultado["pedra_m3"] == 1.37


@pytest.mark.parametrize("traco", ["1:2:3", "1:3:3", "1:4:3", "1.5:5:5"])
def test_contrapiso_todos_os_tracos_calculam(traco):
    # Todo traço do menu tem que dar uma conta (e não um erro)
    resultado = calcular_contrapiso(40, 5, 5, traco)
    assert "erro" not in resultado
    assert resultado["sacos_cimento"] > 0


# ------------------------------------------------------------------
# Números quebrados e outras perdas (C8, C11, C13 do roteiro)
# ------------------------------------------------------------------
def test_contrapiso_area_quebrada():
    resultado = calcular_contrapiso(40.5, 5)
    assert resultado["volume_com_perda_m3"] == 2.126
    assert resultado["sacos_cimento"] == 14
    assert resultado["areia_m3"] == 1.37


def test_contrapiso_espessura_quebrada():
    resultado = calcular_contrapiso(40, 5.5)
    assert resultado["volume_com_perda_m3"] == 2.31
    assert resultado["sacos_cimento"] == 15
    assert resultado["areia_m3"] == 1.49


def test_contrapiso_perda_2_virgula_5():
    resultado = calcular_contrapiso(40, 5, 2.5)
    assert resultado["volume_com_perda_m3"] == 2.05
    assert resultado["sacos_cimento"] == 14
    assert resultado["areia_m3"] == 1.32


def test_contrapiso_sem_perda():
    resultado = calcular_contrapiso(40, 5, 0)
    assert resultado["volume_com_perda_m3"] == 2.0
    assert resultado["sacos_cimento"] == 13


# ------------------------------------------------------------------
# Erros: a função não pode travar, tem que devolver a mensagem certa
# ------------------------------------------------------------------
@pytest.mark.parametrize("area, espessura", [
    (0, 5),      # área zero
    (-40, 5),    # área negativa
    (40, 0),     # espessura zero
    (40, -5),    # espessura negativa
])
def test_contrapiso_area_ou_espessura_invalida(area, espessura):
    resultado = calcular_contrapiso(area, espessura)
    assert resultado == {"erro": "erro_area_espessura_zero"}


def test_contrapiso_perda_negativa():
    resultado = calcular_contrapiso(40, 5, -5)
    assert resultado == {"erro": "erro_perda_negativa"}


def test_contrapiso_traco_invalido():
    resultado = calcular_contrapiso(40, 5, 5, "abc")
    assert resultado == {"erro": "erro_traco_concreto_invalido"}