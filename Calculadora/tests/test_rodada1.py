"""Rodada 1 (Brasil, português) no pytest: os 353 casos do testes_manuais/rodada1.py.

Este arquivo não repete os casos: ele LÊ o rodada1.py (a lista CASOS, o resultado ESPERADO e a função
rodar) e transforma cada caso num teste do pytest. Assim existe um lugar só para manter: se um resultado
esperado mudar de propósito, muda no rodada1.py (e no testes_rodada1.md), e o pytest já usa o novo.

Como rodar (no terminal, na pasta C:\\Calc\\Calculadora):
  env311\\Scripts\\python.exe -B -m pytest                 -> todos os testes
  env311\\Scripts\\python.exe -B -m pytest -k CP-          -> só os casos que têm "CP-" no nome (Contrapiso)
"""
import importlib.util
from pathlib import Path

import pytest

# Pasta Calculadora (este arquivo fica em Calculadora/tests/)
PASTA_APP = Path(__file__).resolve().parent.parent

# Carrega o testes_manuais/rodada1.py como um módulo (ele não é um pacote, então o import normal não acha)
_spec = importlib.util.spec_from_file_location("rodada1", PASTA_APP / "testes_manuais" / "rodada1.py")
rodada1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rodada1)


# parametrize: o mesmo teste roda uma vez para cada caso da lista; ids = o nome que aparece no relatório
@pytest.mark.parametrize(
    "nome, aba, campos, escolhas, continuar",
    rodada1.CASOS,
    ids=[caso[0] for caso in rodada1.CASOS],
)
def test_rodada1(nome, aba, campos, escolhas, continuar):
    resultado = rodada1.rodar(aba, campos, escolhas, continuar)   # o que o app mostra agora
    assert resultado.strip() == rodada1.ESPERADO[nome].strip()    # tem que ser igual ao esperado
