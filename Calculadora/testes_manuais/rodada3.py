r"""Rodada 3 (EUA, português): Piso, Azulejo, Rejunte, Pintura e Baldrame (impermeabilização), as 5 abas
da Parte 1 da versão EUA. Roda pelo mesmo caminho da tela (CalculatorScreen._calcular_aba), sem abrir
janela: kivy/kivymd são trocados por módulos falsos, igual ao rodada2.py.
O país é trocado pelo próprio SettingsScreen.alternar_pais (EUA, estado NY, $, ponto decimal e preços
dos EUA), como o botão País das Configurações faz, ANTES de criar as telas (o reiniciar escolhe a
argamassa pelo país). O idioma fica "pt".
Não grava nada no projeto (rodar com python -B).

O resultado esperado de cada caso fica no fim deste arquivo (ESPERADO), igual ao rodada1.py e ao rodada2.py.
O script compara o texto inteiro que o app mostra com o esperado e diz OK ou DIFERENTE em cada caso; no fim,
mostra quantos deram OK.
Criado em 05/11/2026 a partir do rodada2.py. Durante a rodada, o esperado era lido do testes_rodada3.md
(com ⚠️ nos casos das pendências P1 a P9, que davam DIFERENTE até a correção).
Mudado em 06/11/2026 (fechamento da rodada 3): as 9 pendências foram corrigidas, os 162 casos deram OK com o
testes_rodada3.md e a Gabi conferiu o visual no app. Só depois disso a saída do app (já aprovada) virou o
ESPERADO completo aqui dentro, com o texto inteiro dos 162 casos (versão principal: a do PC). O
tests\rodadas\test_rodada3.py leva estes casos para o pytest.

Como rodar (no terminal, na pasta do projeto: C:\Calc\Calculadora ou C:\Calculadora\Calculadora):
  env311\Scripts\python.exe -B testes_manuais\rodada3.py           -> todos os casos
  env311\Scripts\python.exe -B testes_manuais\rodada3.py PI-        -> só uma aba (prefixo: PI-, AZ-, RJ-, PT-, BA-)
  env311\Scripts\python.exe -B testes_manuais\rodada3.py PI- --ver  -> mostra também o resultado de cada caso

Quando uma mudança no código é DE PROPÓSITO (ex.: um texto novo), o esperado precisa ser atualizado aqui
e no testes_rodada3.md, sabendo o motivo. Quando é SEM QUERER, o script avisa (DIFERENTE)."""
import sys, types, importlib.abc, importlib.machinery
from pathlib import Path

# A pasta do projeto é a pasta de cima desta (testes_manuais), em qualquer PC.
PROJ = str(Path(__file__).resolve().parent.parent)
sys.dont_write_bytecode = True
sys.path.insert(0, PROJ)
try:
    sys.stdout.reconfigure(errors="replace")  # o ⚠️ não quebra a saída num terminal sem UTF-8
except Exception:
    pass


class _Dummy:
    def __init__(self, *a, **k): pass
    def __call__(self, *a, **k): return _Dummy()
    def __getattr__(self, n): return _Dummy()


class _FakeMod(types.ModuleType):
    def __getattr__(self, n):
        if n.startswith("__"):
            raise AttributeError(n)
        return type(n, (_Dummy,), {})


class _Finder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_spec(self, name, path, target=None):
        if name.split(".")[0] in ("kivy", "kivymd"):
            return importlib.machinery.ModuleSpec(name, self, is_package=True)
    def create_module(self, spec):
        m = _FakeMod(spec.name); m.__path__ = []; return m
    def exec_module(self, m): pass


sys.meta_path.insert(0, _Finder())
from src.views.comum import CONFIG_APP  # noqa: E402
from src.views.settings_screen import SettingsScreen  # noqa: E402
CONFIG_APP["idioma"] = "pt"  # rodada 3: app em português
# Botão País das Configurações: o próprio método, com um objeto falso no lugar da tela (sem manager)
SettingsScreen.alternar_pais(types.SimpleNamespace(manager=None), None)
assert CONFIG_APP.get("pais") == "EUA ($)", f"o país não virou EUA: {CONFIG_APP.get('pais')!r}"
from src.views.calculator_screen import CalculatorScreen  # noqa: E402


def nova_tela():
    t = object.__new__(CalculatorScreen)
    t.reiniciar(montar=False)
    return t


# Os opcionais que já vêm preenchidos no app dos EUA
PADRAO = {
    "baldrame": {"perda": "5", "esp_estribo": "8"},
    "piso": {},     # perda vazia = automática; A118.1 e desenho Não vêm do reiniciar (já com o país EUA)
    "azulejo": {},  # idem, com A118.4
    "rejunte": {"esp": "5/16", "perda": "10"},
    "pintura": {"demaos": "2", "rend": "400", "perda": "10"},
}


def rodar(aba, campos, escolhas=None, continuar=True):
    """Limpar + digitar + Calcular. Se aparecer a janela de aviso: Continuar (ou Cancelar)."""
    t = nova_tela()
    t.aba_atual = aba
    e = dict(PADRAO[aba]); e.update(campos)
    extras = []  # [BOTÃO], [CAMPOS]: entram no resultado e são comparados também
    for attr, val in (escolhas or {}).items():
        if attr == "_usar_dados":
            # Botão "Usar dados do Piso/Azulejo" do Rejunte: aba de origem preenchida, depois o toque
            origem, estado_origem = val
            t.estado_abas[origem] = estado_origem
            dados = t._dados_ceramica_digitados(origem)
            extras.append(f"[BOTÃO] {origem}: {dados}")
            t.in_rej_area, t.in_rej_larg, t.in_rej_alt = (types.SimpleNamespace(text="") for _ in range(3))
            t._usar_dados_ceramica(*dados)
            e.update(area=t.in_rej_area.text, larg=t.in_rej_larg.text, alt=t.in_rej_alt.text)
            extras.append(f"[CAMPOS] área {e['area']}, peça {e['larg']} x {e['alt']}")
        elif isinstance(getattr(t, attr), dict):
            getattr(t, attr)[aba] = val
        else:
            setattr(t, attr, val)  # ex.: massa_tipo
    saida = extras
    r = t._calcular_aba(aba, e)
    if "aviso" in r:
        saida.append("[JANELA] " + " | ".join(r["aviso"]))
        if not continuar:
            saida.append("[Cancelar] não calculou")
            return "\n".join(saida)
        t._avisos_aceitos.setdefault(aba, set()).update(r["aviso"])
        r = t._calcular_aba(aba, e)
    saida.append(r.get("erro") or r.get("texto"))
    return "\n".join(saida)


CASOS = []
def caso(nome, aba, campos, escolhas=None, continuar=True):
    CASOS.append((nome, aba, campos, escolhas, continuar))

# ----- Lista copiada do fim do testes_rodada3.md ("Para o rodada3.py"), na mesma ordem -----
# PISO
PI = {"area": "430", "larg": "12", "alt": "12"}
caso("PI-A", "piso", {"area": "430", "larg": "24", "alt": "24", "caixa": "15.5", "perda": "12", "rodape": "65", "rodape_peca": "8"},
     {"desenho": True, "argamassa": "A118.4"})
caso("PI-B", "piso", PI)
caso("PI-B2", "piso", {**PI, "larg": "6", "alt": "6"})
caso("PI-B3", "piso", {**PI, "alt": "24"})
caso("PI-B4", "piso", {**PI, "larg": "24", "alt": "24"})
caso("PI-B5", "piso", PI, {"desenho": True})
caso("PI-B6", "piso", {**PI, "caixa": "15.5"})
caso("PI-B7", "piso", {**PI, "rodape": "65"})
caso("PI-B8", "piso", {**PI, "rodape": "65", "rodape_peca": "8"})
caso("PI-B9", "piso", PI, {"argamassa": "A118.4"})
caso("PI-C1", "piso", {**PI, "area": ""})
caso("PI-C2", "piso", {**PI, "larg": ""})
caso("PI-C3", "piso", {**PI, "area": "quatrocentos"})
caso("PI-C4", "piso", {**PI, "area": "0"})
caso("PI-C5", "piso", {**PI, "area": "-430"})
caso("PI-C6", "piso", {**PI, "larg": "0"})
caso("PI-C7", "piso", {**PI, "area": "430,5"})
caso("PI-C8", "piso", {**PI, "area": "430.5"})
caso("PI-C9", "piso", {**PI, "area": "430 1/2"})
caso("PI-C10", "piso", {**PI, "perda": "-5"})
caso("PI-C11", "piso", {**PI, "perda": "2.5"})
caso("PI-C12", "piso", {**PI, "perda": "0"})
caso("PI-C13", "piso", {**PI, "caixa": "-15"})
caso("PI-C14", "piso", {**PI, "rodape": "-65"})
caso("PI-C15", "piso", {**PI, "area": "1 21/2"})
caso("PI-C16", "piso", {**PI, "area": "1-21/2"})
caso("PI-C17", "piso", {**PI, "area": "1,500"})
caso("PI-C18", "piso", {**PI, "area": "2,5"})
caso("PI-C19", "piso", {**PI, "larg": "11 3/4"})
caso("PI-C20", "piso", {**PI, "larg": "8", "alt": "8"})
caso("PI-C21", "piso", {**PI, "larg": "8 1/16", "alt": "8"})
caso("PI-C22", "piso", {**PI, "larg": "16", "alt": "16"})
caso("PI-C23", "piso", {**PI, "larg": "16 1/8", "alt": "16"})
caso("PI-C24", "piso", {**PI, "larg": "27 1/2", "alt": "27 1/2"})
caso("PI-C25", "piso", {**PI, "larg": "27 9/16", "alt": "27 9/16"})
caso("PI-C26", "piso", {**PI, "larg": "35 3/8", "alt": "35 3/8"})
caso("PI-C27", "piso", {**PI, "larg": "35 7/16", "alt": "35 7/16"})
caso("PI-C28", "piso", {**PI, "area": "21528"})
caso("PI-C29-cancelar", "piso", {**PI, "area": "21529"}, continuar=False)
caso("PI-C29-continuar", "piso", {**PI, "area": "21529"})
caso("PI-C30", "piso", {**PI, "larg": "1", "alt": "1"})
caso("PI-C31", "piso", {**PI, "larg": "120"})
caso("PI-C32", "piso", {**PI, "rodape_peca": "8"})

# AZULEJO
AZ = {"area": "320", "larg": "12", "alt": "24"}
caso("AZ-A", "azulejo", {**AZ, "vaos": "50", "caixa": "15.5", "perda": "15"}, {"desenho": True, "argamassa": "A118.1"})
caso("AZ-B", "azulejo", AZ)
caso("AZ-B2", "azulejo", {**AZ, "vaos": "50"})
caso("AZ-B3", "azulejo", {**AZ, "caixa": "15.5"})
caso("AZ-B4", "azulejo", AZ, {"desenho": True})
caso("AZ-B5", "azulejo", AZ, {"argamassa": "A118.1"})
caso("AZ-B6", "azulejo", {**AZ, "larg": "4", "alt": "4"})
caso("AZ-C1", "azulejo", {**AZ, "area": ""})
caso("AZ-C2", "azulejo", {**AZ, "alt": ""})
caso("AZ-C3", "azulejo", {**AZ, "area": "trezentos"})
caso("AZ-C4", "azulejo", {**AZ, "area": "0"})
caso("AZ-C5", "azulejo", {**AZ, "area": "-320"})
caso("AZ-C6", "azulejo", {**AZ, "area": "320,5"})
caso("AZ-C7", "azulejo", {**AZ, "area": "320.5"})
caso("AZ-C8", "azulejo", {**AZ, "area": "320 1/2"})
caso("AZ-C9", "azulejo", {**AZ, "vaos": "-50"})
caso("AZ-C10", "azulejo", {**AZ, "vaos": "320"})
caso("AZ-C11", "azulejo", {**AZ, "vaos": "400"})
caso("AZ-C12", "azulejo", {**AZ, "vaos": "abc"})
caso("AZ-C13", "azulejo", {**AZ, "vaos": "50 1/2"})
caso("AZ-C14", "azulejo", {**AZ, "perda": "-5"})
caso("AZ-C15", "azulejo", {**AZ, "perda": "2.5"})
caso("AZ-C16", "azulejo", {**AZ, "area": "1-21/2"})
caso("AZ-C17", "azulejo", {**AZ, "area": "1,500"})
caso("AZ-C18", "azulejo", {**AZ, "area": "25000"})

# REJUNTE
RJ = {"area": "430", "larg": "12", "alt": "12", "junta": "1/8"}
caso("RJ-A", "rejunte", {**RJ, "junta": "3/16", "esp": "3/8", "perda": "15"})
caso("RJ-B", "rejunte", RJ)
caso("RJ-B2", "rejunte", {**RJ, "junta": "3/16"})
caso("RJ-B3", "rejunte", {**RJ, "junta": "1/4"})
caso("RJ-B4", "rejunte", {"junta": "1/8"}, {"_usar_dados": ("piso", {"area": "430", "larg": "11 3/4", "alt": "11 3/4"})})
caso("RJ-B5", "rejunte", {"junta": "3/16"},
     {"_usar_dados": ("azulejo", {"area": "320", "vaos": "50 1/2", "larg": "12", "alt": "24"})})
caso("RJ-C1", "rejunte", {**RJ, "area": ""})
caso("RJ-C2", "rejunte", {**RJ, "junta": ""})
caso("RJ-C3", "rejunte", {**RJ, "area": "quatrocentos"})
caso("RJ-C4", "rejunte", {**RJ, "area": "0"})
caso("RJ-C5", "rejunte", {**RJ, "area": "-430"})
caso("RJ-C6", "rejunte", {**RJ, "junta": "0"})
caso("RJ-C7", "rejunte", {**RJ, "junta": "-0.125"})
caso("RJ-C8", "rejunte", {**RJ, "junta": "-1/8"})
caso("RJ-C9", "rejunte", {**RJ, "area": "430,5"})
caso("RJ-C10", "rejunte", {**RJ, "area": "430.5"})
caso("RJ-C11", "rejunte", {**RJ, "area": "430 1/2"})
caso("RJ-C12", "rejunte", {**RJ, "junta": "0.125"})
caso("RJ-C13", "rejunte", {**RJ, "junta": "1/16"})
caso("RJ-C14", "rejunte", {**RJ, "junta": "1/32"})
caso("RJ-C15", "rejunte", {**RJ, "junta": "9/16"})
caso("RJ-C16", "rejunte", {**RJ, "junta": "5/8"})
caso("RJ-C17", "rejunte", {**RJ, "junta": "3"})
caso("RJ-C18", "rejunte", {**RJ, "esp": ""})
caso("RJ-C19", "rejunte", {**RJ, "esp": "0"})
caso("RJ-C20", "rejunte", {**RJ, "perda": "-5"})
caso("RJ-C21", "rejunte", {**RJ, "perda": "2.5"})
caso("RJ-C22", "rejunte", {**RJ, "area": "1-21/2"})
caso("RJ-C23", "rejunte", {**RJ, "area": "1"})
caso("RJ-C24", "rejunte", {**RJ, "area": "25000"})
caso("RJ-C25", "rejunte", {**RJ, "junta": "1/0"})
caso("RJ-C26", "rejunte", {**RJ, "area": "1,500"})

# PINTURA
PT = {"parede": "1000"}
caso("PT-A", "pintura", {"parede": "1000", "teto": "430", "demaos": "3", "rend": "350", "perda": "15"}, {"fundo": True})
caso("PT-B", "pintura", PT)
caso("PT-B2", "pintura", {"parede": "", "teto": "430"})
caso("PT-B3", "pintura", {**PT, "teto": "430"})
caso("PT-B4", "pintura", PT, {"fundo": True})
caso("PT-B5", "pintura", {"parede": "100"})
caso("PT-B6", "pintura", {"parede": "800"})
caso("PT-B7", "pintura", PT, {"selador": True, "massa_tipo": "corrida"})
caso("PT-C1", "pintura", {"parede": "", "teto": ""})
caso("PT-C2", "pintura", {**PT, "demaos": ""})
caso("PT-C3", "pintura", {"parede": "mil"})
caso("PT-C4", "pintura", {"parede": "0"})
caso("PT-C5", "pintura", {"parede": "-1000"})
caso("PT-C6", "pintura", {**PT, "demaos": "0"})
caso("PT-C7", "pintura", {**PT, "demaos": "-2"})
caso("PT-C8", "pintura", {**PT, "demaos": "2.5"})
caso("PT-C9", "pintura", {**PT, "demaos": "5"})
caso("PT-C10", "pintura", {**PT, "demaos": "6"})
caso("PT-C11", "pintura", {**PT, "demaos": "22"})
caso("PT-C12", "pintura", {"parede": "1000,5"})
caso("PT-C13", "pintura", {"parede": "1000.5"})
caso("PT-C14", "pintura", {"parede": "1000 1/2"})
caso("PT-C15", "pintura", {"parede": "1,000"})
caso("PT-C16", "pintura", {**PT, "rend": "0"})
caso("PT-C17", "pintura", {**PT, "rend": ""})
caso("PT-C18-cancelar", "pintura", {**PT, "rend": "12"}, continuar=False)
caso("PT-C18-continuar", "pintura", {**PT, "rend": "12"})
caso("PT-C19", "pintura", {**PT, "rend": "900"})
caso("PT-C20", "pintura", {**PT, "perda": "-5"})
caso("PT-C21", "pintura", {**PT, "perda": "2.5"})
caso("PT-C22", "pintura", {"parede": "1-21/2"})
caso("PT-C23", "pintura", {"parede": "53820"})
caso("PT-C24", "pintura", {"parede": "53821"})

# BALDRAME (impermeabilização)
BA = {"comp": "40", "larg": "8", "alt": "12"}
caso("BA-A", "baldrame", {"comp": "100", "larg": "10", "alt": "16", "perda": "8", "mo": "8.00", "barras": "4", "esp_estribo": "6"},
     {"traco": "1:3:3", "bitola": 12.5, "imperm": True})
caso("BA-B", "baldrame", BA)
caso("BA-B2", "baldrame", BA, {"imperm": True})
caso("BA-B3", "baldrame", {**BA, "comp": "75"}, {"imperm": True})
caso("BA-B4", "baldrame", {**BA, "comp": "80"}, {"imperm": True})
caso("BA-B5", "baldrame", {**BA, "comp": "100"}, {"imperm": True})
caso("BA-B6", "baldrame", {**BA, "barras": "4"})
caso("BA-B7", "baldrame", {**BA, "mo": "8.00"})
caso("BA-C1", "baldrame", {**BA, "comp": ""})
caso("BA-C2", "baldrame", {**BA, "larg": "oito"})
caso("BA-C3", "baldrame", {**BA, "alt": "0"})
caso("BA-C4", "baldrame", {**BA, "comp": "-40"})
caso("BA-C5", "baldrame", {**BA, "comp": "40,5"}, {"imperm": True})
caso("BA-C6", "baldrame", {**BA, "comp": "40.5"}, {"imperm": True})
caso("BA-C7", "baldrame", {**BA, "comp": "40 1/2"}, {"imperm": True})
caso("BA-C8", "baldrame", {**BA, "comp": "1,500"}, {"imperm": True})
caso("BA-C9", "baldrame", {**BA, "perda": "-2"})
caso("BA-C10", "baldrame", {**BA, "perda": "2.5"})
caso("BA-C11-cancelar", "baldrame", {**BA, "larg": "7"}, continuar=False)
caso("BA-C11-continuar", "baldrame", {**BA, "larg": "7"})
caso("BA-C12", "baldrame", {**BA, "larg": "7 7/8", "alt": "11 7/8"})
caso("BA-C13", "baldrame", {**BA, "larg": "0.2", "alt": "0.3"})
caso("BA-C14", "baldrame", {**BA, "barras": "-4"})
caso("BA-C15", "baldrame", {**BA, "barras": "4.5"})
caso("BA-C16", "baldrame", {**BA, "mo": "oito"})
caso("BA-C17", "baldrame", {**BA, "barras": "4", "esp_estribo": ""})
caso("BA-C18", "baldrame", {**BA, "barras": "4", "esp_estribo": "4 1/2"})
caso("BA-C19", "baldrame", {**BA, "comp": "1-21/2"})
caso("BA-C20", "baldrame", {**BA, "larg": "1 1/2", "barras": "4"})


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ver = "--ver" in sys.argv
    filtro = args[0] if args else ""
    ok, diferentes, sem_esperado = 0, [], []
    for nome, aba, campos, esc, cont in CASOS:
        if not nome.startswith(filtro):
            continue
        resultado = rodar(aba, campos, esc, cont)
        esperado = ESPERADO.get(nome)
        if esperado is None:
            sem_esperado.append(nome)
            print(f"SEM ESPERADO  {nome}\n{resultado}\n")
        elif resultado.strip() == esperado.strip():
            ok += 1
            print(f"OK         {nome}")
            if ver:
                print(resultado + "\n")
        else:
            diferentes.append(nome)
            print(f"DIFERENTE  {nome}")
            print("--- esperado:\n" + esperado.strip())
            print("--- o app mostrou:\n" + resultado.strip() + "\n")
    print(f"\n{ok} OK, {len(diferentes)} DIFERENTE(S)" + (f", {len(sem_esperado)} sem esperado" if sem_esperado else ""))
    if diferentes:
        print("Diferentes: " + ", ".join(diferentes))


# =====================================================================
# RESULTADO ESPERADO DE CADA CASO (o que aparece na tela, linha por linha)
# [JANELA] = janela "Confira os valores"; [Cancelar] / Continuar = botão apertado.
# [BOTÃO] e [CAMPOS] = botão "Usar dados do Piso/Azulejo" do Rejunte e o que ele preenche.
# =====================================================================
ESPERADO = {
"PI-A": """\
Área: 430.00 sq ft
Área com perda (12%): 481.60 sq ft
Peça: 24 x 24 in
Assentamento: com desenho
• Peças: 121
• Caixas: 32 (15.50 sq ft por caixa) ($ 2,237.11)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 13 sacos de 50 lb (602.1 lb) ($ 233.74)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft
• Rodapé: 72.80 ft (10 peças de 8.00 ft) ($ 332.84)

Custo Estimado da Etapa: $ 2,803.69""",
"PI-B": """\
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 12 x 12 in
• Peças: 473 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.2 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,373.16""",
"PI-B2": """\
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 6 x 6 in
• Peças: 1,892 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 6 sacos de 50 lb (278.2 lb) ($ 132.00)
  Desempenadeira: 1/4 x 1/4 in · Consumo: 0.588 lb/sq ft

Custo Estimado da Etapa: $ 2,329.16""",
"PI-B3": """\
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 12 x 24 in
• Peças: 237 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 12 sacos de 50 lb (591.3 lb) ($ 264.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 2,461.16""",
"PI-B4": """\
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 24 x 24 in
• Peças: 119 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 12 sacos de 50 lb (591.3 lb) ($ 264.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 2,461.16""",
"PI-B5": """\
Área: 430.00 sq ft
Área com perda (25%, automática): 537.50 sq ft
Peça: 12 x 12 in
Assentamento: com desenho
• Peças: 538 ($ 2,496.77)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 9 sacos de 50 lb (448.0 lb) ($ 198.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,694.77""",
"PI-B6": """\
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 12 x 12 in
• Peças: 473
• Caixas: 31 (15.50 sq ft por caixa) ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.2 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,373.16""",
"PI-B7": """\
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 12 x 12 in
• Peças: 473 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.2 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft
• Rodapé: 71.50 ft ($ 326.90)

Custo Estimado da Etapa: $ 2,700.05""",
"PI-B8": """\
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 12 x 12 in
• Peças: 473 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.2 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft
• Rodapé: 71.50 ft (9 peças de 8.00 ft) ($ 326.90)

Custo Estimado da Etapa: $ 2,700.05""",
"PI-B9": """\
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 12 x 12 in
• Peças: 473 ($ 2,197.16)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 8 sacos de 50 lb (394.2 lb) ($ 143.84)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,341.00""",
"PI-C1": """\
Por favor, digite números válidos nos campos!""",
"PI-C2": """\
Por favor, digite números válidos nos campos!""",
"PI-C3": """\
Por favor, digite números válidos nos campos!""",
"PI-C4": """\
Erro: Área e tamanho da peça devem ser maiores que zero.""",
"PI-C5": """\
Erro: Área e tamanho da peça devem ser maiores que zero.""",
"PI-C6": """\
Erro: Área e tamanho da peça devem ser maiores que zero.""",
"PI-C7": """\
Área: 430.50 sq ft
Área com perda (10%, automática): 473.55 sq ft
Peça: 12 x 12 in
• Peças: 474 ($ 2,199.71)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.6 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,375.71""",
"PI-C8": """\
Área: 430.50 sq ft
Área com perda (10%, automática): 473.55 sq ft
Peça: 12 x 12 in
• Peças: 474 ($ 2,199.71)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.6 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,375.71""",
"PI-C9": """\
Área: 430.50 sq ft
Área com perda (10%, automática): 473.55 sq ft
Peça: 12 x 12 in
• Peças: 474 ($ 2,199.71)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.6 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,375.71""",
"PI-C10": """\
Erro: A perda não pode ser negativa.""",
"PI-C11": """\
Área: 430.00 sq ft
Área com perda (2.5%): 440.75 sq ft
Peça: 12 x 12 in
• Peças: 441 ($ 2,047.35)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (367.3 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,223.35""",
"PI-C12": """\
Área: 430.00 sq ft
Área com perda (0%): 430.00 sq ft
Peça: 12 x 12 in
• Peças: 430 ($ 1,997.42)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (358.3 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,173.42""",
"PI-C13": """\
Erro: Os valores não podem ser negativos.""",
"PI-C14": """\
Erro: Os valores não podem ser negativos.""",
"PI-C15": """\
Por favor, digite números válidos nos campos!""",
"PI-C16": """\
Por favor, digite números válidos nos campos!""",
"PI-C17": """\
Área: 1,500.00 sq ft
Área com perda (10%, automática): 1,650.00 sq ft
Peça: 12 x 12 in
• Peças: 1,650 ($ 7,664.50)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 28 sacos de 50 lb (1,375.0 lb) ($ 616.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 8,280.50""",
"PI-C18": """\
Área: 2.50 sq ft
Área com perda (10%, automática): 2.75 sq ft
Peça: 12 x 12 in
• Peças: 3 ($ 12.77)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 1 saco de 50 lb (2.2 lb) ($ 22.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 34.77""",
"PI-C19": """\
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 11 3/4 x 12 in
• Peças: 484 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.2 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,373.16""",
"PI-C20": """\
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 8 x 8 in
• Peças: 1,065 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 6 sacos de 50 lb (278.2 lb) ($ 132.00)
  Desempenadeira: 1/4 x 1/4 in · Consumo: 0.588 lb/sq ft

Custo Estimado da Etapa: $ 2,329.16""",
"PI-C21": """\
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 8 1/16 x 8 in
• Peças: 1,056 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.2 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,373.16""",
"PI-C22": """\
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 16 x 16 in
• Peças: 267 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.2 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,373.16""",
"PI-C23": """\
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 16 1/8 x 16 in
• Peças: 264 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 12 sacos de 50 lb (591.3 lb) ($ 264.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 2,461.16""",
"PI-C24": """\
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 27 1/2 x 27 1/2 in
• Peças: 91 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 12 sacos de 50 lb (591.3 lb) ($ 264.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 2,461.16""",
"PI-C25": """\
Área: 430.00 sq ft
Área com perda (15%, automática): 494.50 sq ft
Peça: 27 9/16 x 27 9/16 in
• Peças: 94 ($ 2,297.03)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 13 sacos de 50 lb (618.2 lb) ($ 286.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 2,583.03""",
"PI-C26": """\
Área: 430.00 sq ft
Área com perda (15%, automática): 494.50 sq ft
Peça: 35 3/8 x 35 3/8 in
• Peças: 57 ($ 2,297.03)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 13 sacos de 50 lb (618.2 lb) ($ 286.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 2,583.03""",
"PI-C27": """\
Área: 430.00 sq ft
Área com perda (20%, automática): 516.00 sq ft
Peça: 35 7/16 x 35 7/16 in
• Peças: 60 ($ 2,396.90)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 13 sacos de 50 lb (645.1 lb) ($ 286.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 2,682.90""",
"PI-C28": """\
Área: 21,528.00 sq ft
Área com perda (10%, automática): 23,680.80 sq ft
Peça: 12 x 12 in
• Peças: 23,681 ($ 110,000.92)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 395 sacos de 50 lb (19,734.0 lb) ($ 8,690.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 118,690.92""",
"PI-C29-cancelar": """\
[JANELA] Área de 21,529 sq ft: o limite é 21,528 sq ft.
[Cancelar] não calculou""",
"PI-C29-continuar": """\
[JANELA] Área de 21,529 sq ft: o limite é 21,528 sq ft.
Área: 21,529.00 sq ft
Área com perda (10%, automática): 23,681.90 sq ft
Peça: 12 x 12 in
• Peças: 23,682 ($ 110,006.03)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 395 sacos de 50 lb (19,734.9 lb) ($ 8,690.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 118,696.03""",
"PI-C30": """\
[JANELA] Peça de 1 in x 1 in: o normal é de 2 in a 118 in em cada lado.
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 1 x 1 in
• Peças: 68,112 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 6 sacos de 50 lb (278.2 lb) ($ 132.00)
  Desempenadeira: 1/4 x 1/4 in · Consumo: 0.588 lb/sq ft

Custo Estimado da Etapa: $ 2,329.16""",
"PI-C31": """\
[JANELA] Peça de 120 in x 12 in: o normal é de 2 in a 118 in em cada lado.
Área: 430.00 sq ft
Área com perda (20%, automática): 516.00 sq ft
Peça: 120 x 12 in
• Peças: 52 ($ 2,396.90)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 13 sacos de 50 lb (645.1 lb) ($ 286.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 2,682.90""",
"PI-C32": """\
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 12 x 12 in
• Peças: 473 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.2 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,373.16""",
"AZ-A": """\
Área: 320.00 sq ft
Vãos (portas e janelas): 50.00 sq ft
Área líquida: 270.00 sq ft
Área com perda (15%): 310.50 sq ft
Peça: 12 x 24 in
Assentamento: com desenho
• Peças: 156
• Caixas: 21 (15.50 sq ft por caixa) ($ 1,153.86)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (388.2 lb) ($ 176.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,329.86""",
"AZ-B": """\
Área: 320.00 sq ft
Área com perda (10%, automática): 352.00 sq ft
Peça: 12 x 24 in
• Peças: 176 ($ 1,308.07)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 9 sacos de 50 lb (440.0 lb) ($ 161.82)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,469.89""",
"AZ-B2": """\
Área: 320.00 sq ft
Vãos (portas e janelas): 50.00 sq ft
Área líquida: 270.00 sq ft
Área com perda (10%, automática): 297.00 sq ft
Peça: 12 x 24 in
• Peças: 149 ($ 1,103.69)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 8 sacos de 50 lb (371.3 lb) ($ 143.84)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,247.53""",
"AZ-B3": """\
Área: 320.00 sq ft
Área com perda (10%, automática): 352.00 sq ft
Peça: 12 x 24 in
• Peças: 176
• Caixas: 23 (15.50 sq ft por caixa) ($ 1,308.07)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 9 sacos de 50 lb (440.0 lb) ($ 161.82)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,469.89""",
"AZ-B4": """\
Área: 320.00 sq ft
Área com perda (25%, automática): 400.00 sq ft
Peça: 12 x 24 in
Assentamento: com desenho
• Peças: 200 ($ 1,486.45)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 10 sacos de 50 lb (500.0 lb) ($ 179.80)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,666.25""",
"AZ-B5": """\
Área: 320.00 sq ft
Área com perda (10%, automática): 352.00 sq ft
Peça: 12 x 24 in
• Peças: 176 ($ 1,308.07)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 9 sacos de 50 lb (440.0 lb) ($ 198.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,506.07""",
"AZ-B6": """\
Área: 320.00 sq ft
Área com perda (10%, automática): 352.00 sq ft
Peça: 4 x 4 in
• Peças: 3,168 ($ 1,308.07)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 5 sacos de 50 lb (207.0 lb) ($ 89.90)
  Desempenadeira: 1/4 x 1/4 in · Consumo: 0.588 lb/sq ft

Custo Estimado da Etapa: $ 1,397.97""",
"AZ-C1": """\
Por favor, digite números válidos nos campos!""",
"AZ-C2": """\
Por favor, digite números válidos nos campos!""",
"AZ-C3": """\
Por favor, digite números válidos nos campos!""",
"AZ-C4": """\
Erro: Área e tamanho da peça devem ser maiores que zero.""",
"AZ-C5": """\
Erro: Área e tamanho da peça devem ser maiores que zero.""",
"AZ-C6": """\
Área: 320.50 sq ft
Área com perda (10%, automática): 352.55 sq ft
Peça: 12 x 24 in
• Peças: 177 ($ 1,310.12)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 9 sacos de 50 lb (440.7 lb) ($ 161.82)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,471.94""",
"AZ-C7": """\
Área: 320.50 sq ft
Área com perda (10%, automática): 352.55 sq ft
Peça: 12 x 24 in
• Peças: 177 ($ 1,310.12)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 9 sacos de 50 lb (440.7 lb) ($ 161.82)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,471.94""",
"AZ-C8": """\
Área: 320.50 sq ft
Área com perda (10%, automática): 352.55 sq ft
Peça: 12 x 24 in
• Peças: 177 ($ 1,310.12)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 9 sacos de 50 lb (440.7 lb) ($ 161.82)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,471.94""",
"AZ-C9": """\
Erro: Os valores não podem ser negativos.""",
"AZ-C10": """\
Erro: O desconto de vãos deve ser menor que a área.""",
"AZ-C11": """\
Erro: O desconto de vãos deve ser menor que a área.""",
"AZ-C12": """\
Por favor, digite números válidos nos campos!""",
"AZ-C13": """\
Área: 320.00 sq ft
Vãos (portas e janelas): 50.50 sq ft
Área líquida: 269.50 sq ft
Área com perda (10%, automática): 296.45 sq ft
Peça: 12 x 24 in
• Peças: 149 ($ 1,101.64)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 8 sacos de 50 lb (370.6 lb) ($ 143.84)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,245.48""",
"AZ-C14": """\
Erro: A perda não pode ser negativa.""",
"AZ-C15": """\
Área: 320.00 sq ft
Área com perda (2.5%): 328.00 sq ft
Peça: 12 x 24 in
• Peças: 164 ($ 1,218.89)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 9 sacos de 50 lb (410.1 lb) ($ 161.82)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,380.71""",
"AZ-C16": """\
Por favor, digite números válidos nos campos!""",
"AZ-C17": """\
Área: 1,500.00 sq ft
Área com perda (10%, automática): 1,650.00 sq ft
Peça: 12 x 24 in
• Peças: 825 ($ 6,131.60)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 42 sacos de 50 lb (2,062.4 lb) ($ 755.16)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 6,886.76""",
"AZ-C18": """\
[JANELA] Área de 25,000 sq ft: o limite é 21,528 sq ft.
Área: 25,000.00 sq ft
Área com perda (10%, automática): 27,500.00 sq ft
Peça: 12 x 24 in
• Peças: 13,750 ($ 102,193.34)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 688 sacos de 50 lb (34,374.9 lb) ($ 12,370.24)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 114,563.58""",
"RJ-A": """\
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 3/16 in
Espessura da peça: 3/8 in
Consumo: 0.096 lb/sq ft
• Rejunte com areia (sanded) (com 15% de perda): 47.6 lb = 2 sacos de 25 lb ($ 73.22)

Custo Estimado da Etapa: $ 73.22""",
"RJ-B": """\
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 25.3 lb = 3 caixas de 10 lb ($ 101.49)

Custo Estimado da Etapa: $ 101.49""",
"RJ-B2": """\
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 3/16 in
Espessura da peça: 5/16 in
Consumo: 0.080 lb/sq ft
• Rejunte com areia (sanded) (com 10% de perda): 38.0 lb = 1 saco de 25 lb e 2 caixas de 7 lb ($ 97.05)

Custo Estimado da Etapa: $ 97.05""",
"RJ-B3": """\
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 1/4 in
Espessura da peça: 5/16 in
Consumo: 0.107 lb/sq ft
• Rejunte com areia (sanded) (com 10% de perda): 50.6 lb = 2 sacos de 25 lb e 1 caixa de 7 lb ($ 103.44)

Custo Estimado da Etapa: $ 103.44""",
"RJ-B4": """\
[BOTÃO] piso: ('430', '11 3/4', '11 3/4')
[CAMPOS] área 430, peça 11 3/4 x 11 3/4
Área: 430.00 sq ft
Peça: 11 3/4 x 11 3/4 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.055 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 25.9 lb = 3 caixas de 10 lb ($ 101.49)

Custo Estimado da Etapa: $ 101.49""",
"RJ-B5": """\
[BOTÃO] azulejo: ('269.5', '12', '24')
[CAMPOS] área 269.5, peça 12 x 24
Área: 269.50 sq ft
Peça: 12 x 24 in
Junta: 3/16 in
Espessura da peça: 5/16 in
Consumo: 0.060 lb/sq ft
• Rejunte com areia (sanded) (com 10% de perda): 17.9 lb = 3 caixas de 7 lb ($ 90.66)

Custo Estimado da Etapa: $ 90.66""",
"RJ-C1": """\
Por favor, digite números válidos nos campos!""",
"RJ-C2": """\
Por favor, digite números válidos nos campos!""",
"RJ-C3": """\
Por favor, digite números válidos nos campos!""",
"RJ-C4": """\
Erro: Área, tamanho da peça e junta devem ser maiores que zero.""",
"RJ-C5": """\
Erro: Área, tamanho da peça e junta devem ser maiores que zero.""",
"RJ-C6": """\
Erro: Área, tamanho da peça e junta devem ser maiores que zero.""",
"RJ-C7": """\
Erro: Área, tamanho da peça e junta devem ser maiores que zero.""",
"RJ-C8": """\
Por favor, digite números válidos nos campos!""",
"RJ-C9": """\
Área: 430.50 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 25.3 lb = 3 caixas de 10 lb ($ 101.49)

Custo Estimado da Etapa: $ 101.49""",
"RJ-C10": """\
Área: 430.50 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 25.3 lb = 3 caixas de 10 lb ($ 101.49)

Custo Estimado da Etapa: $ 101.49""",
"RJ-C11": """\
Área: 430.50 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 25.3 lb = 3 caixas de 10 lb ($ 101.49)

Custo Estimado da Etapa: $ 101.49""",
"RJ-C12": """\
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 25.3 lb = 3 caixas de 10 lb ($ 101.49)

Custo Estimado da Etapa: $ 101.49""",
"RJ-C13": """\
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 1/16 in
Espessura da peça: 5/16 in
Consumo: 0.027 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 12.7 lb = 2 caixas de 10 lb ($ 67.66)

Custo Estimado da Etapa: $ 67.66""",
"RJ-C14": """\
[JANELA] Junta de 1/32 in: o normal é de 1/16 in a 9/16 in.
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 1/32 in
Espessura da peça: 5/16 in
Consumo: 0.013 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 6.3 lb = 1 caixa de 10 lb ($ 33.83)

Custo Estimado da Etapa: $ 33.83""",
"RJ-C15": """\
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 9/16 in
Espessura da peça: 5/16 in
Consumo: 0.241 lb/sq ft
• Rejunte com areia (sanded) (com 10% de perda): 113.9 lb = 4 sacos de 25 lb e 2 caixas de 7 lb ($ 206.88)

Custo Estimado da Etapa: $ 206.88""",
"RJ-C16": """\
[JANELA] Junta de 5/8 in: o normal é de 1/16 in a 9/16 in.
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 5/8 in
Espessura da peça: 5/16 in
Consumo: 0.267 lb/sq ft
• Rejunte com areia (sanded) (com 10% de perda): 126.6 lb = 5 sacos de 25 lb e 1 caixa de 7 lb ($ 213.27)

Custo Estimado da Etapa: $ 213.27""",
"RJ-C17": """\
[JANELA] Junta de 3 in: o normal é de 1/16 in a 9/16 in.
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 3 in
Espessura da peça: 5/16 in
Consumo: 1.284 lb/sq ft
• Rejunte com areia (sanded) (com 10% de perda): 607.5 lb = 24 sacos de 25 lb e 2 caixas de 7 lb ($ 939.08)

Custo Estimado da Etapa: $ 939.08""",
"RJ-C18": """\
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 25.3 lb = 3 caixas de 10 lb ($ 101.49)

Custo Estimado da Etapa: $ 101.49""",
"RJ-C19": """\
Erro: A espessura da peça deve ser maior que zero.""",
"RJ-C20": """\
Erro: A perda não pode ser negativa.""",
"RJ-C21": """\
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 2.5% de perda): 23.6 lb = 3 caixas de 10 lb ($ 101.49)

Custo Estimado da Etapa: $ 101.49""",
"RJ-C22": """\
Por favor, digite números válidos nos campos!""",
"RJ-C23": """\
Área: 1.00 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 0.1 lb = 1 caixa de 10 lb ($ 33.83)

Custo Estimado da Etapa: $ 33.83""",
"RJ-C24": """\
[JANELA] Área de 25,000 sq ft: o limite é 21,528 sq ft.
Área: 25,000.00 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 1,471.6 lb = 148 caixas de 10 lb ($ 5,006.84)

Custo Estimado da Etapa: $ 5,006.84""",
"RJ-C25": """\
Por favor, digite números válidos nos campos!""",
"RJ-C26": """\
Área: 1,500.00 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 88.3 lb = 9 caixas de 10 lb ($ 304.47)

Custo Estimado da Etapa: $ 304.47""",
"PT-A": """\
Parede: 1,000.00 sq ft
Teto: 430.00 sq ft
Demãos: 3
Rendimento: 350 sq ft/gal
• Tinta de parede (com 15% de perda): 9.9 gal = 2 baldes de 5 gal ($ 362.00)
• Tinta de teto (com 15% de perda): 4.2 gal = 1 balde de 5 gal ($ 181.00)
• Primer (com 15% de perda): 4.1 gal = 1 balde de 5 gal ($ 170.00)
Complementos (sobre parede + teto): Primer 1 demão

Custo Estimado da Etapa: $ 713.00""",
"PT-B": """\
Parede: 1,000.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)

Custo Estimado da Etapa: $ 215.98""",
"PT-B2": """\
Teto: 430.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de teto (com 10% de perda): 2.4 gal = 3 galões de 1 gal ($ 104.94)

Custo Estimado da Etapa: $ 104.94""",
"PT-B3": """\
Parede: 1,000.00 sq ft
Teto: 430.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)
• Tinta de teto (com 10% de perda): 2.4 gal = 3 galões de 1 gal ($ 104.94)

Custo Estimado da Etapa: $ 320.92""",
"PT-B4": """\
Parede: 1,000.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)
• Primer (com 10% de perda): 2.7 gal = 3 galões de 1 gal ($ 150.00)
Complementos (sobre parede + teto): Primer 1 demão

Custo Estimado da Etapa: $ 365.98""",
"PT-B5": """\
Parede: 100.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 0.6 gal = 1 galão de 1 gal ($ 34.98)

Custo Estimado da Etapa: $ 34.98""",
"PT-B6": """\
Parede: 800.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 4.4 gal = 1 balde de 5 gal ($ 181.00)

Custo Estimado da Etapa: $ 181.00""",
"PT-B7": """\
Parede: 1,000.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)

Custo Estimado da Etapa: $ 215.98""",
"PT-C1": """\
Por favor, digite números válidos nos campos!""",
"PT-C2": """\
Por favor, digite números válidos nos campos!""",
"PT-C3": """\
Por favor, digite números válidos nos campos!""",
"PT-C4": """\
Erro: Informe a área de parede ou a área de teto.""",
"PT-C5": """\
Erro: As áreas não podem ser negativas.""",
"PT-C6": """\
Erro: Demãos e rendimento devem ser maiores que zero.""",
"PT-C7": """\
Erro: Demãos e rendimento devem ser maiores que zero.""",
"PT-C8": """\
Por favor, digite números válidos nos campos!""",
"PT-C9": """\
Parede: 1,000.00 sq ft
Demãos: 5
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 13.7 gal = 2 baldes de 5 gal e 4 galões de 1 gal ($ 501.92)

Custo Estimado da Etapa: $ 501.92""",
"PT-C10": """\
[JANELA] 6 demãos: o limite é 5 (normalmente são 2 ou 3).
Parede: 1,000.00 sq ft
Demãos: 6
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 16.5 gal = 3 baldes de 5 gal e 2 galões de 1 gal ($ 612.96)

Custo Estimado da Etapa: $ 612.96""",
"PT-C11": """\
[JANELA] 22 demãos: o limite é 5 (normalmente são 2 ou 3).
Parede: 1,000.00 sq ft
Demãos: 22
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 60.5 gal = 12 baldes de 5 gal e 1 galão de 1 gal ($ 2,206.98)

Custo Estimado da Etapa: $ 2,206.98""",
"PT-C12": """\
Parede: 1,000.50 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)

Custo Estimado da Etapa: $ 215.98""",
"PT-C13": """\
Parede: 1,000.50 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)

Custo Estimado da Etapa: $ 215.98""",
"PT-C14": """\
Parede: 1,000.50 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)

Custo Estimado da Etapa: $ 215.98""",
"PT-C15": """\
Parede: 1,000.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)

Custo Estimado da Etapa: $ 215.98""",
"PT-C16": """\
Erro: Demãos e rendimento devem ser maiores que zero.""",
"PT-C17": """\
Parede: 1,000.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)

Custo Estimado da Etapa: $ 215.98""",
"PT-C18-cancelar": """\
[JANELA] Rendimento de 12 sq ft/gal: o normal é de 150 sq ft/gal a 800 sq ft/gal.
[Cancelar] não calculou""",
"PT-C18-continuar": """\
[JANELA] Rendimento de 12 sq ft/gal: o normal é de 150 sq ft/gal a 800 sq ft/gal.
Parede: 1,000.00 sq ft
Demãos: 2
Rendimento: 12 sq ft/gal
• Tinta de parede (com 10% de perda): 183.3 gal = 36 baldes de 5 gal e 4 galões de 1 gal ($ 6,655.92)

Custo Estimado da Etapa: $ 6,655.92""",
"PT-C19": """\
[JANELA] Rendimento de 900 sq ft/gal: o normal é de 150 sq ft/gal a 800 sq ft/gal.
Parede: 1,000.00 sq ft
Demãos: 2
Rendimento: 900 sq ft/gal
• Tinta de parede (com 10% de perda): 2.5 gal = 3 galões de 1 gal ($ 104.94)

Custo Estimado da Etapa: $ 104.94""",
"PT-C20": """\
Erro: A perda não pode ser negativa.""",
"PT-C21": """\
Parede: 1,000.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 2.5% de perda): 5.1 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)

Custo Estimado da Etapa: $ 215.98""",
"PT-C22": """\
Por favor, digite números válidos nos campos!""",
"PT-C23": """\
Parede: 53,820.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 296.0 gal = 59 baldes de 5 gal e 2 galões de 1 gal ($ 10,748.96)

Custo Estimado da Etapa: $ 10,748.96""",
"PT-C24": """\
[JANELA] Área de parede de 53,821 sq ft: o limite é 53,820 sq ft.
Parede: 53,821.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 296.0 gal = 59 baldes de 5 gal e 2 galões de 1 gal ($ 10,748.96)

Custo Estimado da Etapa: $ 10,748.96""",
"BA-A": """\
Traço: 1:3:3
Volume Total (com 8% de perda): 3.398 m³
• Cimento: 22 sacos de 50 kg ($ 264.00)
• Areia: 2.18 m³ ($ 98.10)
• Brita: 2.18 m³ ($ 87.20)
• Ferro 12.5 mm: 133.4 kg (12 barras de 12 m) (inclui 4.00 m de emendas)
• Estribos 5 mm c/ 6 in: 38.3 kg (21 barras de 12 m)
• Aço/Ferragem: 171.7 kg ($ 429.25)
• Arame recozido: 3.4 kg ($ 51.45)
• Impermeabilizante: 350.0 sq ft · 6.9 gal = 1 balde de 5 gal e 3 galões de 1 gal ($ 65.18)
• Mão de Obra: 100.0 ft ($ 800.00)

Custo Estimado da Etapa: $ 1,795.18""",
"BA-B": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0.793 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.59 m³ ($ 23.60)

Custo Estimado da Etapa: $ 113.60""",
"BA-B2": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0.793 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.59 m³ ($ 23.60)
• Impermeabilizante: 106.7 sq ft · 2.1 gal = 3 galões de 1 gal ($ 25.23)

Custo Estimado da Etapa: $ 138.83""",
"BA-B3": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 1.487 m³
• Cimento: 12 sacos de 50 kg ($ 144.00)
• Areia: 0.74 m³ ($ 33.30)
• Brita: 1.11 m³ ($ 44.40)
• Impermeabilizante: 200.0 sq ft · 3.9 gal = 4 galões de 1 gal ($ 33.64)

Custo Estimado da Etapa: $ 255.34""",
"BA-B4": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 1.586 m³
• Cimento: 12 sacos de 50 kg ($ 144.00)
• Areia: 0.79 m³ ($ 35.55)
• Brita: 1.19 m³ ($ 47.60)
• Impermeabilizante: 213.3 sq ft · 4.2 gal = 1 balde de 5 gal ($ 39.95)

Custo Estimado da Etapa: $ 267.10""",
"BA-B5": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 1.982 m³
• Cimento: 15 sacos de 50 kg ($ 180.00)
• Areia: 0.99 m³ ($ 44.55)
• Brita: 1.49 m³ ($ 59.60)
• Impermeabilizante: 266.6 sq ft · 5.2 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 48.36)

Custo Estimado da Etapa: $ 332.51""",
"BA-B6": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0.793 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.59 m³ ($ 23.60)
• Ferro 8 mm: 21.8 kg (5 barras de 12 m) (inclui 1.28 m de emendas)
• Estribos 5 mm c/ 8 in: 8.5 kg (5 barras de 12 m)
• Aço/Ferragem: 30.3 kg ($ 75.72)
• Arame recozido: 0.6 kg ($ 9.15)

Custo Estimado da Etapa: $ 198.47""",
"BA-B7": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0.793 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.59 m³ ($ 23.60)
• Mão de Obra: 40.0 ft ($ 320.00)

Custo Estimado da Etapa: $ 433.60""",
"BA-C1": """\
Por favor, digite números válidos nos campos!""",
"BA-C2": """\
Por favor, digite números válidos nos campos!""",
"BA-C3": """\
Erro: Comprimento, largura e altura devem ser maiores que zero.""",
"BA-C4": """\
Erro: Comprimento, largura e altura devem ser maiores que zero.""",
"BA-C5": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0.803 m³
• Cimento: 7 sacos de 50 kg ($ 84.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.60 m³ ($ 24.00)
• Impermeabilizante: 108.0 sq ft · 2.1 gal = 3 galões de 1 gal ($ 25.23)

Custo Estimado da Etapa: $ 151.23""",
"BA-C6": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0.803 m³
• Cimento: 7 sacos de 50 kg ($ 84.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.60 m³ ($ 24.00)
• Impermeabilizante: 108.0 sq ft · 2.1 gal = 3 galões de 1 gal ($ 25.23)

Custo Estimado da Etapa: $ 151.23""",
"BA-C7": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0.803 m³
• Cimento: 7 sacos de 50 kg ($ 84.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.60 m³ ($ 24.00)
• Impermeabilizante: 108.0 sq ft · 2.1 gal = 3 galões de 1 gal ($ 25.23)

Custo Estimado da Etapa: $ 151.23""",
"BA-C8": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 29.733 m³
• Cimento: 223 sacos de 50 kg ($ 2,676.00)
• Areia: 14.87 m³ ($ 669.15)
• Brita: 22.30 m³ ($ 892.00)
• Impermeabilizante: 4,000.0 sq ft · 78.5 gal = 16 baldes de 5 gal e 3 galões de 1 gal ($ 664.43)

Custo Estimado da Etapa: $ 4,901.58""",
"BA-C9": """\
Erro: A perda não pode ser negativa.""",
"BA-C10": """\
Traço: 1:2:3
Volume Total (com 2.5% de perda): 0.774 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.39 m³ ($ 17.55)
• Brita: 0.58 m³ ($ 23.20)

Custo Estimado da Etapa: $ 112.75""",
"BA-C11-cancelar": """\
[JANELA] Viga de 7 in x 12 in: o mínimo é 8 in de largura e 12 in de altura.
[Cancelar] não calculou""",
"BA-C11-continuar": """\
[JANELA] Viga de 7 in x 12 in: o mínimo é 8 in de largura e 12 in de altura.
Traço: 1:2:3
Volume Total (com 5% de perda): 0.694 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.35 m³ ($ 15.75)
• Brita: 0.52 m³ ($ 20.80)

Custo Estimado da Etapa: $ 108.55""",
"BA-C12": """\
[JANELA] Viga de 7 7/8 in x 11 7/8 in: o mínimo é 8 in de largura e 12 in de altura.
Traço: 1:2:3
Volume Total (com 5% de perda): 0.772 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.39 m³ ($ 17.55)
• Brita: 0.58 m³ ($ 23.20)

Custo Estimado da Etapa: $ 112.75""",
"BA-C13": """\
[JANELA] Viga de 0.2 in x 0.3 in: o mínimo é 8 in de largura e 12 in de altura.
Traço: 1:2:3
Volume Total (com 5% de perda): 0.000 m³
• Cimento: 1 saco de 50 kg ($ 12.00)

Custo Estimado da Etapa: $ 12.00""",
"BA-C14": """\
Erro: Barras e espaçamento dos estribos não podem ser negativos.""",
"BA-C15": """\
Por favor, digite números válidos nos campos!""",
"BA-C16": """\
Por favor, digite números válidos nos campos!""",
"BA-C17": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0.793 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.59 m³ ($ 23.60)
• Ferro 8 mm: 21.8 kg (5 barras de 12 m) (inclui 1.28 m de emendas)
• Aço/Ferragem: 21.8 kg ($ 54.38)
• Arame recozido: 0.4 kg ($ 6.45)

Custo Estimado da Etapa: $ 174.43""",
"BA-C18": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0.793 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.59 m³ ($ 23.60)
• Ferro 8 mm: 21.8 kg (5 barras de 12 m) (inclui 1.28 m de emendas)
• Estribos 5 mm c/ 4 1/2 in: 15.0 kg (9 barras de 12 m)
• Aço/Ferragem: 36.7 kg ($ 91.80)
• Arame recozido: 0.7 kg ($ 10.95)

Custo Estimado da Etapa: $ 216.35""",
"BA-C19": """\
Por favor, digite números válidos nos campos!""",
"BA-C20": """\
[JANELA] Viga de 1 1/2 in x 12 in: o mínimo é 8 in de largura e 12 in de altura.
Erro: Viga muito pequena para colocar estribos.""",
}


if __name__ == "__main__":
    main()
