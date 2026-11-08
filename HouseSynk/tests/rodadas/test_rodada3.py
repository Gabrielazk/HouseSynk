"""Rodada 3 (EUA, português) no pytest: os 162 casos do testes_manuais/rodada3.py.

Este arquivo não repete os casos: ele LÊ o rodada3.py (a lista CASOS, o resultado ESPERADO e a função
rodar) e transforma cada caso num teste do pytest. Assim existe um lugar só para manter: se um resultado
esperado mudar de propósito, muda no rodada3.py (e no testes_rodada3.md), e o pytest já usa o novo.
Criado em 06/11/2026 (fechamento da rodada 3), a partir do test_rodada2.py.

Diferença do test_rodada2.py: o país. O rodada3.py troca o país para EUA quando é carregado, com o
próprio alternar_pais das Configurações, que muda o CONFIG_APP (país, estado, moeda, ponto decimal e
preços) e a TABELA_PRECOS_GLOBAL (cimento, areia, brita, aço e mão de obra). Os dois ficam num lugar só,
que todos os testes usam. Se ficassem nos EUA, os casos das rodadas 1 e 2 (Brasil) dariam erro. Por isso:
  1. antes de carregar o rodada3.py, guarda uma cópia dos dois;
  2. logo depois, guarda como ficaram nos EUA e coloca tudo de volta como era (apagando o mao_obra_m2,
     que o alternar_pais cria). Não dá para usar o alternar_pais para voltar: ele volta com os preços
     do PRECOS_BR (cimento R$ 32 e brita R$ 95), e não com os preços iniciais (R$ 36 e R$ 120);
  3. a fixture "app_nos_eua" liga os EUA só durante cada caso da rodada 3, e o pytest volta tudo
     como estava no fim de cada caso (é o que o monkeypatch faz).

Como rodar (no terminal, na pasta do projeto):
  env311\\Scripts\\python.exe -B -m pytest                                   -> todos os testes
  env311\\Scripts\\python.exe -B -m pytest tests\\rodadas\\test_rodada3.py     -> só a rodada 3
  env311\\Scripts\\python.exe -B -m pytest -k "rodada3 and PI-"              -> só o Piso da rodada 3
"""
import importlib.util
from pathlib import Path

import pytest

from src.views.comum import CONFIG_APP, TABELA_PRECOS_GLOBAL

# Pasta do projeto (este arquivo fica em tests/rodadas/, por isso 3 vezes o .parent)
PASTA_APP = Path(__file__).resolve().parent.parent.parent

# 1. Como estava antes (Brasil, com os preços iniciais)
_config_antes = dict(CONFIG_APP)
_precos_antes = dict(vars(TABELA_PRECOS_GLOBAL))

# Carrega o testes_manuais/rodada3.py como um módulo (ele não é um pacote, então o import normal não acha)
_spec = importlib.util.spec_from_file_location("rodada3", PASTA_APP / "testes_manuais" / "rodada3.py")
rodada3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rodada3)

# 2. Como o rodada3.py deixou (EUA) e, logo depois, tudo de volta como era
_config_eua = dict(CONFIG_APP)
_precos_eua = dict(vars(TABELA_PRECOS_GLOBAL))
CONFIG_APP.clear()
CONFIG_APP.update(_config_antes)
for _campo in list(vars(TABELA_PRECOS_GLOBAL)):
    if _campo not in _precos_antes:
        delattr(TABELA_PRECOS_GLOBAL, _campo)  # o mao_obra_m2, que o alternar_pais cria
for _campo, _valor in _precos_antes.items():
    setattr(TABELA_PRECOS_GLOBAL, _campo, _valor)


@pytest.fixture
def app_nos_eua(monkeypatch):
    """3. Liga os EUA só durante o caso; no fim, o monkeypatch volta tudo como estava
    (e apaga o que não existia antes, como o mao_obra_m2)."""
    for chave, valor in _config_eua.items():
        monkeypatch.setitem(CONFIG_APP, chave, valor)
    for campo, valor in _precos_eua.items():
        monkeypatch.setattr(TABELA_PRECOS_GLOBAL, campo, valor, raising=False)


# parametrize: o mesmo teste roda uma vez para cada caso da lista; ids = o nome que aparece no relatório
@pytest.mark.parametrize(
    "nome, aba, campos, escolhas, continuar",
    rodada3.CASOS,
    ids=[caso[0] for caso in rodada3.CASOS],
)
def test_rodada3(app_nos_eua, nome, aba, campos, escolhas, continuar):
    resultado = rodada3.rodar(aba, campos, escolhas, continuar)   # o que o app mostra agora (EUA)
    assert resultado.strip() == rodada3.ESPERADO[nome].strip()    # tem que ser igual ao esperado
