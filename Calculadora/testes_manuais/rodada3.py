r"""Rodada 3 (EUA, português): Piso, Azulejo, Rejunte, Pintura e Baldrame (impermeabilização), as 5 abas
da Parte 1 da versão EUA. Roda pelo mesmo caminho da tela (CalculatorScreen._calcular_aba), sem abrir
janela: kivy/kivymd são trocados por módulos falsos, igual ao rodada2.py.
O país é trocado pelo próprio SettingsScreen.alternar_pais (EUA, estado NY, $, ponto decimal e preços
dos EUA), como o botão País das Configurações faz, ANTES de criar as telas (o reiniciar escolhe a
argamassa pelo país). O idioma fica "pt".
Não grava nada no projeto (rodar com python -B).

Durante a rodada, o esperado NÃO fica neste arquivo: é LIDO do testes_rodada3.md toda vez que roda.
Cada caso começa numa linha "#### <NOME>" (o nome vai até o primeiro espaço) e o esperado é o primeiro
bloco entre ``` logo abaixo. O .md tem o que o app DEVE mostrar; os casos com ⚠️ no título são
pendências já conhecidas (P1 a P9), que dão DIFERENTE até o app ser corrigido. No fim, o script separa:
  - DIFERENTE com ⚠️ (já esperado): só a contagem por aba;
  - DIFERENTE SEM ⚠️ (surpresa): com o esperado e o que o app mostrou;
  - ⚠️ que deu OK (a pendência sumiu?).
Criado em 05/11/2026 a partir do rodada2.py.

Como rodar (no terminal, na pasta do projeto: C:\Calc\Calculadora ou C:\Calculadora\Calculadora):
  env311\Scripts\python.exe -B testes_manuais\rodada3.py           -> todos os casos
  env311\Scripts\python.exe -B testes_manuais\rodada3.py PI-        -> só uma aba (prefixo: PI-, AZ-, RJ-, PT-, BA-)
  env311\Scripts\python.exe -B testes_manuais\rodada3.py PI- --ver  -> mostra também o resultado de cada caso
                                                                      (e o esperado dos DIFERENTE com ⚠️)"""
import sys, types, importlib.abc, importlib.machinery
from pathlib import Path

# A pasta do projeto é a pasta de cima desta (testes_manuais), em qualquer PC.
PROJ = str(Path(__file__).resolve().parent.parent)
ARQ_MD = Path(PROJ) / "testes_manuais" / "testes_rodada3.md"
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


def ler_esperado(caminho=ARQ_MD):
    """Lê o testes_rodada3.md: {nome: (esperado, aviso)}. aviso = o que vem depois do nome no título
    (ex.: "⚠️ P1, P7"), ou "" se o caso não tem ⚠️."""
    linhas = caminho.read_text(encoding="utf-8").splitlines()
    esperado = {}
    i = 0
    while i < len(linhas):
        if not linhas[i].startswith("#### "):
            i += 1
            continue
        titulo = linhas[i][5:].strip()
        nome = titulo.split()[0]
        aviso = titulo[len(nome):].strip() if "⚠" in titulo else ""
        i += 1
        while i < len(linhas) and not linhas[i].startswith("```") and not linhas[i].startswith("#"):
            i += 1
        if i >= len(linhas) or not linhas[i].startswith("```"):
            continue  # caso sem bloco: fica sem esperado
        i += 1
        bloco = []
        while i < len(linhas) and not linhas[i].startswith("```"):
            bloco.append(linhas[i])
            i += 1
        i += 1
        if nome in esperado:
            raise ValueError(f"caso repetido no {caminho.name}: {nome}")
        esperado[nome] = ("\n".join(bloco), aviso)
    return esperado


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
    ESPERADO = ler_esperado()
    ok, sem_esperado = 0, []
    dif_aviso, surpresas, aviso_ok = [], [], []  # (nome, aviso[, esperado, resultado])
    for nome, aba, campos, esc, cont in CASOS:
        if not nome.startswith(filtro):
            continue
        resultado = rodar(aba, campos, esc, cont)
        if nome not in ESPERADO:
            sem_esperado.append(nome)
            print(f"SEM ESPERADO  {nome}\n{resultado}\n")
            continue
        esperado, aviso = ESPERADO[nome]
        if resultado.strip() == esperado.strip():
            ok += 1
            print(f"OK         {nome}" + (f"   ({aviso}: a pendência sumiu?)" if aviso else ""))
            if aviso:
                aviso_ok.append((nome, aviso))
            if ver:
                print(resultado + "\n")
        elif aviso:
            dif_aviso.append((nome, aviso))
            print(f"DIFERENTE  {nome}   ({aviso}, já esperado)")
            if ver:
                print("--- esperado:\n" + esperado.strip())
                print("--- o app mostrou:\n" + resultado.strip() + "\n")
        else:
            surpresas.append((nome, esperado, resultado))
            print(f"DIFERENTE  {nome}   (SEM ⚠️: surpresa)")
            print("--- esperado:\n" + esperado.strip())
            print("--- o app mostrou:\n" + resultado.strip() + "\n")

    dif = len(dif_aviso) + len(surpresas)
    print(f"\n{ok} OK, {dif} DIFERENTE(S)" + (f", {len(sem_esperado)} sem esperado" if sem_esperado else ""))
    nomes_casos = {c[0] for c in CASOS}
    fora = [n for n in ESPERADO if n not in nomes_casos and n.startswith(filtro)]
    if fora:
        print("No .md, mas fora da lista CASOS: " + ", ".join(fora))
    if sem_esperado:
        print("Sem esperado no .md: " + ", ".join(sem_esperado))

    print(f"\nDIFERENTE com ⚠️ (já esperado): {len(dif_aviso)}")
    por_aba = {}
    for nome, _ in dif_aviso:
        por_aba[nome.split("-")[0]] = por_aba.get(nome.split("-")[0], 0) + 1
    for pref in ("PI", "AZ", "RJ", "PT", "BA"):
        if pref in por_aba:
            print(f"  {pref}: {por_aba.pop(pref)}")
    for pref, n in por_aba.items():
        print(f"  {pref}: {n}")

    print(f"\nDIFERENTE SEM ⚠️ (surpresa): {len(surpresas)}")
    for nome, esperado, resultado in surpresas:
        print(f"  {nome}")
        print("  --- esperado:\n    " + esperado.strip().replace("\n", "\n    "))
        print("  --- o app mostrou:\n    " + resultado.strip().replace("\n", "\n    "))

    print(f"\n⚠️ que deu OK (a pendência sumiu?): {len(aviso_ok)}")
    for nome, aviso in aviso_ok:
        print(f"  {nome}   ({aviso})")


if __name__ == "__main__":
    main()
