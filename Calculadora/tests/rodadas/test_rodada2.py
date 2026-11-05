"""Rodada 2 (Brasil, inglês) no pytest: os 353 casos do testes_manuais/rodada2.py.

Este arquivo não repete os casos: ele LÊ o rodada2.py (a lista CASOS, o resultado ESPERADO e a função
rodar) e transforma cada caso num teste do pytest. Assim existe um lugar só para manter: se um resultado
esperado mudar de propósito, muda no rodada2.py (e no testes_rodada2.md), e o pytest já usa o novo.
Criado em 05/11/2026 (passo 3 do fim da rodada 2), a partir do test_rodada1.py.
Mudado em 05/11/2026 (passo 4): foi para a pasta tests/rodadas/.

Diferença do test_rodada1.py: o idioma. O rodada2.py liga o inglês quando é carregado, e o idioma fica
num lugar só (CONFIG_APP, no comum.py), que todos os testes usam. Se ficasse em inglês, os casos da
rodada 1 (em português) dariam erro. Por isso:
  1. logo depois de carregar o rodada2.py, o idioma volta para o português (o padrão do app);
  2. a fixture "app_em_ingles" liga o inglês só durante cada caso da rodada 2, e o pytest
     volta o idioma como estava no fim de cada caso (é o que o monkeypatch faz).

Como rodar (no terminal, na pasta C:\\Calc\\Calculadora):
  env311\\Scripts\\python.exe -B -m pytest                          -> todos os testes
  env311\\Scripts\\python.exe -B -m pytest tests\\rodadas\\test_rodada2.py    -> só a rodada 2
  env311\\Scripts\\python.exe -B -m pytest -k "rodada2 and CP-"     -> só o Contrapiso da rodada 2
"""
import importlib.util
from pathlib import Path

import pytest

# Pasta Calculadora (este arquivo fica em Calculadora/tests/rodadas/, por isso 3 vezes o .parent)
PASTA_APP = Path(__file__).resolve().parent.parent.parent

# Carrega o testes_manuais/rodada2.py como um módulo (ele não é um pacote, então o import normal não acha)
_spec = importlib.util.spec_from_file_location("rodada2", PASTA_APP / "testes_manuais" / "rodada2.py")
rodada2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rodada2)

# O rodada2.py acabou de ligar o inglês: volta para o português, para não estragar os outros testes
rodada2.CONFIG_APP["idioma"] = "pt"


@pytest.fixture
def app_em_ingles(monkeypatch):
    """Liga o inglês só durante o caso; no fim, o monkeypatch volta o idioma como estava."""
    monkeypatch.setitem(rodada2.CONFIG_APP, "idioma", "en")


# parametrize: o mesmo teste roda uma vez para cada caso da lista; ids = o nome que aparece no relatório
@pytest.mark.parametrize(
    "nome, aba, campos, escolhas, continuar",
    rodada2.CASOS,
    ids=[caso[0] for caso in rodada2.CASOS],
)
def test_rodada2(app_em_ingles, nome, aba, campos, escolhas, continuar):
    resultado = rodada2.rodar(aba, campos, escolhas, continuar)   # o que o app mostra agora (em inglês)
    assert resultado.strip() == rodada2.ESPERADO[nome].strip()    # tem que ser igual ao esperado
