r"""Rodada 2 (Brasil, inglês): roda os MESMOS casos da rodada 1 (rodada1.py) com o app em inglês,
pelo mesmo caminho da tela (CalculatorScreen._calcular_aba), sem abrir janela: kivy/kivymd são trocados
por módulos falsos. O país continua BR, então números com vírgula e R$ não são erro.
Não grava nada no projeto (rodar com python -B).

O esperado NÃO fica neste arquivo: é lido do testes_rodada2.md (mesma pasta) a cada execução.
- Blocos completos do .md (Teste A, A2, B, "**B2:**"...): compara o texto inteiro.
- Tabelas (B2..., C1...): cada trecho entre aspas e cada número do .md tem que aparecer no que o app mostrou.
Criado em 04/11/2026 a partir do rodada1.py (parte que roda os casos e a lista CASOS copiadas sem mudança).

Como rodar (no terminal, na pasta C:\Calc\Calculadora):
  env311\Scripts\python.exe -B testes_manuais\rodada2.py           -> todos os casos
  env311\Scripts\python.exe -B testes_manuais\rodada2.py BR-        -> só uma aba (prefixo: BR-, BA-, PA-...)
  env311\Scripts\python.exe -B testes_manuais\rodada2.py BR- --ver  -> mostra também digitado, esperado e resultado

"! conferir palavras" lista palavras em português ou chaves (tipo erro_xxx) no que o app mostrou;
não muda o OK/DIFERENTE, é só para você olhar."""
import os, re, sys, types, difflib, itertools, importlib.abc, importlib.machinery

PROJ = r"C:\Calc\Calculadora"
sys.dont_write_bytecode = True
sys.path.insert(0, PROJ)


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
CONFIG_APP["idioma"] = "en"  # rodada 2: app em inglês; o país continua BR (vírgula e R$)
from src.views.calculator_screen import CalculatorScreen  # noqa: E402


def nova_tela():
    t = object.__new__(CalculatorScreen)
    t.reiniciar(montar=False)
    return t


PADRAO = {
    "brocas": {"perda": "10", "esp_estribo": "20"},
    "baldrame": {"perda": "5", "esp_estribo": "20"},
    "paredes": {"junta": "1", "quebra": "5"},
    "laje": {"capa": "4", "perda": "5"},
    "telhado": {"incl": "30", "perda": "5"},
    "eletrica": {"perda": "10"},
    "hidraulica": {"perda": "10"},
    "contrapiso": {"perda": "5"},
    "reboco": {"esp": "2", "perda": "10"},
    "piso": {},  # perda vazia = automática; AC-I e desenho Não vêm do reiniciar
    "azulejo": {},  # idem, com AC-II
    "rejunte": {"esp": "8", "perda": "10"},
    "pintura": {"demaos": "2", "rend": "12", "perda": "10"},
}


def rodar_esquadrias(campos, escolhas):
    """Esquadrias: cada ("add", tipo, material, qtd, larg, alt) digita no formulário e toca em
    "Adicionar à lista" (o método real da tela); ("rem", i) toca no X do item i; ("calc",) calcula.
    No fim, digita `campos` (formulário) e toca em Calcular."""
    t = nova_tela()
    t.aba_atual = "esquadrias"
    t.trocar_aba = lambda *a, **k: None  # sem tela: não remonta a aba
    t._lbl_resultado = types.SimpleNamespace(text="")
    t.in_esq_qtd, t.in_esq_larg, t.in_esq_alt = (types.SimpleNamespace(text="") for _ in range(3))
    t._campos = {"qtd": t.in_esq_qtd, "larg": t.in_esq_larg, "alt": t.in_esq_alt}
    t.esq_fixacao.update(escolhas.get("fix", {}))
    saida = []

    def janela(aba, avisos, depois):
        """Janela "Confira os valores" do Adicionar à lista: mostra e aperta Continuar."""
        saida.append("[JANELA no Adicionar] " + " | ".join(avisos))
        t._avisos_aceitos.setdefault(aba, set()).update(avisos)
        depois()
    t._pedir_confirmacao = janela
    for acao in escolhas.get("acoes", []):
        if acao[0] == "add":
            _, t.esq_tipo, t.esq_material, t.in_esq_qtd.text, t.in_esq_larg.text, t.in_esq_alt.text = acao
            t._lbl_resultado.text = ""
            antes = [dict(i) for i in t.esquadrias_itens]
            t._adicionar_esquadria()
            if t._lbl_resultado.text:
                saida.append(f"[Adicionar] {t._lbl_resultado.text}")
            if t.esquadrias_itens == antes:
                saida.append("[Adicionar] nada entrou na lista")
            elif any(c.text for c in t._campos.values()):
                saida.append("[Adicionar] campos NÃO ficaram vazios")
        elif acao[0] == "rem":
            t.textos_resultado["esquadrias"] = "(resultado antigo)"
            t._remover_esquadria(acao[1])
            saida.append(f"[X] lista: {[t._texto_item_esquadria(i) for i in t.esquadrias_itens]}; "
                         f"resultado antigo {'sumiu' if 'esquadrias' not in t.textos_resultado else 'FICOU'}")
    e = {"qtd": "", "larg": "", "alt": ""}
    e.update(campos)
    r = t._calcular_aba("esquadrias", e)
    saida.append(r.get("erro") or r.get("texto"))
    return "\n".join(saida)


def rodar(aba, campos, escolhas=None, continuar=True):
    """Limpar + digitar + Calcular. Se aparecer a janela de aviso: Continuar (ou Cancelar)."""
    if aba == "esquadrias":
        return rodar_esquadrias(campos, escolhas or {})
    t = nova_tela()
    t.aba_atual = aba
    e = dict(PADRAO[aba]); e.update(campos)
    extras = []  # [TROCA], [BOTÃO], [CAMPOS]: entram no resultado e são comparados também
    for attr, val in (escolhas or {}).items():
        if attr == "_trocar_telha":
            # Troca o tipo pelo método da tela, que ajusta o campo de inclinação
            t.in_tel_incl = types.SimpleNamespace(text=e.get("incl", ""))
            t._botao_telha_tipo = types.SimpleNamespace(text="")
            incl_vista = []
            for tipo in val:
                t._escolher_telha_tipo(tipo)
                incl_vista.append(f"{tipo}->{t.in_tel_incl.text}")
            e["incl"] = t.in_tel_incl.text
            extras.append("[TROCA] " + ", ".join(incl_vista))
        elif attr == "_usar_dados":
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
            setattr(t, attr, val)  # ex.: laje_tipo, laje_enchimento
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

# ---------------- BROCAS ----------------
B = {"qtd": "10", "diam": "20", "prof": "3"}
caso("BR-A", "brocas", {"qtd": "12", "diam": "25", "prof": "3,5", "perda": "12", "mo": "30,00", "barras": "4", "esp_estribo": "15"},
     {"traco": "1:3:3", "bitola": 10.0})
caso("BR-B", "brocas", B)
caso("BR-B2", "brocas", {**B, "barras": "4"})
caso("BR-C1", "brocas", {**B, "qtd": ""})
caso("BR-C2", "brocas", {**B, "qtd": "dez"})
caso("BR-C3", "brocas", {**B, "qtd": "0"})
caso("BR-C4", "brocas", {**B, "prof": "-3"})
caso("BR-C5", "brocas", {**B, "qtd": "2,5"})
caso("BR-C6", "brocas", {**B, "prof": "2,5"})
caso("BR-C7", "brocas", {**B, "prof": "2.5"})
caso("BR-C8", "brocas", {**B, "prof": "2 1/2"})
caso("BR-C9", "brocas", {**B, "perda": "-5"})
caso("BR-C10", "brocas", {**B, "perda": "2,5"})
caso("BR-C11", "brocas", {**B, "diam": "4", "barras": "4"})
caso("BR-C12", "brocas", {**B, "barras": "-4"})
caso("BR-C13", "brocas", {**B, "mo": "trinta"})
caso("BR-C14-cancelar", "brocas", {**B, "prof": "300"}, continuar=False)
caso("BR-C14-continuar", "brocas", {**B, "prof": "300"})
caso("BR-C15", "brocas", {**B, "barras": "4", "esp_estribo": ""})
caso("BR-C16", "brocas", {**B, "barras": "4", "esp_estribo": "12,5"})
caso("BR-C17", "brocas", {**B, "prof": "30"})
caso("BR-C18", "brocas", {**B, "prof": "1-21/2"})

# ---------------- BALDRAME ----------------
D = {"comp": "12,5", "larg": "20", "alt": "30"}
caso("BA-A", "baldrame", {"comp": "30", "larg": "20", "alt": "40", "perda": "8", "mo": "40,00", "barras": "6", "esp_estribo": "15"},
     {"traco": "1:4:3", "bitola": 12.5, "imperm": True})
caso("BA-B", "baldrame", D)
caso("BA-B2", "baldrame", {**D, "barras": "4"})
caso("BA-B3", "baldrame", D, {"imperm": True})
caso("BA-C1", "baldrame", {**D, "comp": ""})
caso("BA-C2", "baldrame", {**D, "larg": "vinte"})
caso("BA-C3", "baldrame", {**D, "alt": "0"})
caso("BA-C4", "baldrame", {**D, "comp": "-5"})
caso("BA-C5", "baldrame", {**D, "comp": "12.5"})
caso("BA-C6", "baldrame", {**D, "comp": "12 1/2"})
caso("BA-C7", "baldrame", {**D, "perda": "-2"})
caso("BA-C8", "baldrame", {**D, "perda": "2,5"})
caso("BA-C9", "baldrame", {**D, "larg": "4", "barras": "4"})
caso("BA-C10", "baldrame", {**D, "barras": "-4"})
caso("BA-C11", "baldrame", {**D, "barras": "4,5"})
caso("BA-C12", "baldrame", {**D, "mo": "quarenta"})
caso("BA-C13", "baldrame", {**D, "barras": "4", "esp_estribo": "12,5"})
caso("BA-C14", "baldrame", {**D, "comp": "12", "barras": "4"})
caso("BA-C15", "baldrame", {**D, "comp": "24", "barras": "4"})
caso("BA-C16", "baldrame", {**D, "barras": "4", "esp_estribo": ""})
caso("BA-C17", "baldrame", {**D, "comp": "5000"})
caso("BA-C18", "baldrame", {**D, "larg": "0,2", "alt": "0,3"})
caso("BA-C19", "baldrame", {**D, "larg": "19"})
caso("BA-C20", "baldrame", {**D, "alt": "29,5"})
caso("BA-C21", "baldrame", {**D, "comp": "1-21/2"})
caso("BA-C22", "baldrame", {**D, "comp": "2 1/2"})

# ---------------- PAREDES ----------------
P = {"area": "30"}
caso("PA-A", "paredes", {"area": "80", "vaos": "12,5", "junta": "1,5", "quebra": "8"},
     {"tijolo": "bloco_14", "assent": "deitado", "traco": "1:0.5:6"})
caso("PA-B", "paredes", P)
caso("PA-B2", "paredes", P, {"tijolo": "bloco_19"})
caso("PA-B3", "paredes", P, {"tijolo": "baiano_9f", "assent": "deitado"})
caso("PA-B4", "paredes", P, {"traco": "1:0:3"})
caso("PA-C1", "paredes", {"area": ""})
caso("PA-C2", "paredes", {"area": "trinta"})
caso("PA-C3", "paredes", {"area": "0"})
caso("PA-C4", "paredes", {"area": "-30"})
caso("PA-C5", "paredes", {"area": "30,5"})
caso("PA-C6", "paredes", {"area": "30.5"})
caso("PA-C7", "paredes", {"area": "30 1/2"})
caso("PA-C8", "paredes", {**P, "vaos": "35"})
caso("PA-C9", "paredes", {**P, "vaos": "30"})
caso("PA-C10", "paredes", {**P, "vaos": "-5"})
caso("PA-C11", "paredes", {**P, "quebra": "-5"})
caso("PA-C12a", "paredes", {**P, "junta": ""})
caso("PA-C12b", "paredes", {**P, "quebra": ""})
caso("PA-C13", "paredes", {**P, "quebra": "2,5"})
caso("PA-C14", "paredes", {**P, "junta": "0"})
caso("PA-C15", "paredes", {**P, "junta": "10"})
caso("PA-C16-cancelar", "paredes", {"area": "100000"}, continuar=False)
caso("PA-C16-continuar", "paredes", {"area": "100000"})
caso("PA-C17", "paredes", {**P, "quebra": "25"})

# ---------------- LAJE ----------------
L = {"area": "50"}
MAC = {"laje_tipo": "macica"}
caso("LA-A", "laje", {"area": "50", "capa": "5", "perda": "8"},
     {"laje_enchimento": "lajota", "tela": True, "traco": "1:3:3"})
caso("LA-A2", "laje", {"area": "30", "esp": "10", "perda": "7"}, {**MAC, "traco": "1.5:5:5"})
caso("LA-B", "laje", L)
caso("LA-B2", "laje", {"area": "30", "esp": "10"}, MAC)
caso("LA-B3", "laje", L, {"tela": True})
caso("LA-B4", "laje", L, {"laje_enchimento": "lajota"})
caso("LA-C1", "laje", {"area": ""})
caso("LA-C2", "laje", {"area": "cinquenta"})
caso("LA-C3", "laje", {"area": "0"})
caso("LA-C4", "laje", {"area": "-50"})
caso("LA-C5", "laje", {"area": "50,5"})
caso("LA-C6", "laje", {"area": "50.5"})
caso("LA-C7", "laje", {"area": "50 1/2"})
caso("LA-C8", "laje", {**L, "perda": "-5"})
caso("LA-C9", "laje", {**L, "perda": "2,5"})
caso("LA-C10", "laje", {**L, "capa": "0"})
caso("LA-C11", "laje", {**L, "capa": ""})
caso("LA-C12", "laje", {**L, "capa": "-4"})
caso("LA-C13", "laje", {**L, "esp": ""}, MAC)
caso("LA-C14", "laje", {**L, "esp": "0"}, MAC)
caso("LA-C15", "laje", {**L, "esp": "dez"}, MAC)
caso("LA-C16", "laje", {"area": "1-21/2"})
caso("LA-C17", "laje", {"area": "5"}, {"tela": True})
caso("LA-C18", "laje", {**L, "capa": "4,5"})
caso("LA-C19", "laje", {"area": "100000"})
caso("LA-C20", "laje", {**L, "capa": "50"})
caso("LA-C21", "laje", {**L, "esp": "200"}, MAC)
# C22 (troca de tipo): o texto da capa/área fica no estado; calcula de novo como pré-moldada
caso("LA-C22-volta", "laje", {"area": "50", "capa": "5", "perda": "8", "esp": ""},
     {"laje_enchimento": "lajota", "tela": True, "traco": "1:3:3"})

# ---------------- TELHADO ----------------
T = {"area": "80"}
caso("TE-A", "telhado", {"area": "80", "incl": "35", "cumeeira": "10", "perda": "8"},
     {"_trocar_telha": ["concreto"], "madeiramento": True})
caso("TE-A2", "telhado", {"area": "60", "cumeeira": "8", "perda": "5"},
     {"_trocar_telha": ["fibrocimento"], "madeiramento": True})
caso("TE-B", "telhado", T)
caso("TE-B2", "telhado", {**T, "cumeeira": "10"})
caso("TE-B3", "telhado", T, {"madeiramento": True})
caso("TE-B4", "telhado", T, {"_trocar_telha": ["fibrocimento"]})
caso("TE-B5", "telhado", T, {"_trocar_telha": ["concreto"]})
caso("TE-C1", "telhado", {"area": ""})
caso("TE-C2", "telhado", {"area": "oitenta"})
caso("TE-C3", "telhado", {"area": "0"})
caso("TE-C4", "telhado", {"area": "-80"})
caso("TE-C5", "telhado", {"area": "80,5"})
caso("TE-C6", "telhado", {"area": "80.5"})
caso("TE-C7", "telhado", {"area": "80 1/2"})
caso("TE-C8", "telhado", {**T, "perda": "-5"})
caso("TE-C9", "telhado", {**T, "perda": "2,5"})
caso("TE-C10", "telhado", {**T, "incl": "-30"})
caso("TE-C11", "telhado", {**T, "incl": ""})
caso("TE-C12", "telhado", {**T, "incl": "0"})
caso("TE-C13", "telhado", {**T, "incl": "2,5"})
caso("TE-C14", "telhado", {**T, "cumeeira": "-10"})
caso("TE-C15", "telhado", {**T, "cumeeira": "0"})
caso("TE-C16", "telhado", {**T, "cumeeira": "dez"})
caso("TE-C17", "telhado", {"area": "1-21/2"})
caso("TE-C18", "telhado", {**T, "cumeeira": "0,3"})
caso("TE-C19", "telhado", {"area": "100000"})
caso("TE-C20", "telhado", {**T, "incl": "300"})
caso("TE-C21", "telhado", T, {"_trocar_telha": ["fibrocimento", "ceramica"]})
caso("TE-C22", "telhado", {**T, "incl": "35"}, {"_trocar_telha": ["fibrocimento"]})

# ---------------- ELÉTRICA ----------------
E = {"tomadas": "20", "interruptores": "10", "luzes": "12"}
caso("EL-A", "eletrica", {**E, "chuveiros": "2", "chuveiros4": "1", "conduite": "150", "fio1.5": "200",
                          "fio2.5": "250", "fio4": "40", "fio6": "60", "perda": "5"})
caso("EL-B", "eletrica", E)
caso("EL-B2", "eletrica", {**E, "chuveiros": "2"})
caso("EL-B3", "eletrica", {**E, "chuveiros4": "2"})
caso("EL-B4", "eletrica", {**E, "chuveiros": "1", "chuveiros4": "1"})
caso("EL-B5", "eletrica", {**E, "conduite": "150"})
caso("EL-B6", "eletrica", {**E, "fio2.5": "250"})
caso("EL-B7", "eletrica", {"chuveiros": "1"})
caso("EL-B8", "eletrica", {"chuveiros4": "1"})
caso("EL-B9", "eletrica", {"tomadas": "1"})
caso("EL-C1", "eletrica", {"tomadas": "", "interruptores": "", "luzes": ""})
caso("EL-C2", "eletrica", {"tomadas": "0", "interruptores": "0", "luzes": "0"})
caso("EL-C3", "eletrica", {**E, "tomadas": "vinte"})
caso("EL-C4", "eletrica", {**E, "tomadas": "-5"})
caso("EL-C5", "eletrica", {**E, "tomadas": "2,5"})
caso("EL-C5b", "eletrica", {**E, "chuveiros4": "-1"})
caso("EL-C5c", "eletrica", {**E, "chuveiros4": "1,5"})
caso("EL-C6", "eletrica", {**E, "perda": "-5"})
caso("EL-C7", "eletrica", {**E, "perda": "2,5"})
caso("EL-C8", "eletrica", {**E, "conduite": "-10"})
caso("EL-C9", "eletrica", {**E, "conduite": "0"})
caso("EL-C10", "eletrica", {**E, "conduite": "150,5"})
caso("EL-C11", "eletrica", {**E, "conduite": "150.5"})
caso("EL-C12", "eletrica", {**E, "conduite": "150 1/2"})
caso("EL-C13", "eletrica", {**E, "fio1.5": "abc"})
caso("EL-C14", "eletrica", {**E, "fio1.5": "1-21/2"})
caso("EL-C15", "eletrica", {**E, "chuveiros": "2", "fio6": "0"})
caso("EL-C15b", "eletrica", {**E, "chuveiros4": "2", "fio4": "0"})
caso("EL-C16", "eletrica", {**E, "tomadas": "2000"})
caso("EL-C17", "eletrica", {**E, "chuveiros": "50"})

# ---------------- HIDRÁULICA ----------------
H = {"fria": "10", "quente": "3", "esgoto": "8"}
caso("HI-A", "hidraulica", {**H, "tubo_fria": "50", "tubo_quente": "20", "tubo_esg40": "30", "tubo_esg100": "18",
                            "perda": "5"})
caso("HI-B", "hidraulica", H)
caso("HI-B2", "hidraulica", {"fria": "1"})
caso("HI-B3", "hidraulica", {**H, "tubo_fria": "50"})
caso("HI-B4", "hidraulica", {"esgoto": "8"})
caso("HI-C1", "hidraulica", {"fria": "", "quente": "", "esgoto": ""})
caso("HI-C2", "hidraulica", {"fria": "0", "quente": "0", "esgoto": "0"})
caso("HI-C3", "hidraulica", {**H, "fria": "dez"})
caso("HI-C4", "hidraulica", {**H, "fria": "-10"})
caso("HI-C5", "hidraulica", {**H, "fria": "2,5"})
caso("HI-C6", "hidraulica", {**H, "perda": "-5"})
caso("HI-C7", "hidraulica", {**H, "perda": "2,5"})
caso("HI-C8", "hidraulica", {**H, "tubo_fria": "-10"})
caso("HI-C9", "hidraulica", {**H, "tubo_fria": "0"})
caso("HI-C10", "hidraulica", {**H, "tubo_fria": "50,5"})
caso("HI-C11", "hidraulica", {**H, "tubo_fria": "50.5"})
caso("HI-C12", "hidraulica", {**H, "tubo_fria": "50 1/2"})
caso("HI-C13", "hidraulica", {**H, "tubo_fria": "abc"})
caso("HI-C14", "hidraulica", {**H, "tubo_fria": "1-21/2"})
caso("HI-C15", "hidraulica", {**H, "fria": "1000"})

# ---------------- CONTRAPISO ----------------
CP = {"area": "40", "esp": "5"}
caso("CP-A", "contrapiso", {"area": "40", "esp": "6", "perda": "8"}, {"traco": "1:2:3"})
caso("CP-B", "contrapiso", CP)
caso("CP-B2", "contrapiso", CP, {"traco": "1.5:5:5"})
caso("CP-C1", "contrapiso", {**CP, "area": ""})
caso("CP-C2", "contrapiso", {**CP, "esp": ""})
caso("CP-C3", "contrapiso", {**CP, "area": "quarenta"})
caso("CP-C4", "contrapiso", {**CP, "area": "0"})
caso("CP-C5", "contrapiso", {**CP, "area": "-40"})
caso("CP-C6", "contrapiso", {**CP, "esp": "0"})
caso("CP-C7", "contrapiso", {**CP, "esp": "-5"})
caso("CP-C8", "contrapiso", {**CP, "area": "40,5"})
caso("CP-C9", "contrapiso", {**CP, "area": "40.5"})
caso("CP-C10", "contrapiso", {**CP, "area": "40 1/2"})
caso("CP-C11", "contrapiso", {**CP, "esp": "5,5"})
caso("CP-C12", "contrapiso", {**CP, "perda": "-5"})
caso("CP-C13", "contrapiso", {**CP, "perda": "2,5"})
caso("CP-C14", "contrapiso", {**CP, "perda": ""})
caso("CP-C15", "contrapiso", {**CP, "area": "1-21/2"})
caso("CP-C16", "contrapiso", {**CP, "area": "100000"})
caso("CP-C17", "contrapiso", {**CP, "esp": "50"})
caso("CP-C18", "contrapiso", {**CP, "esp": "0,5"})

# ---------------- REBOCO ----------------
R = {"area": "30"}
caso("RE-A", "reboco", {"area": "30", "esp": "2,5", "vaos": "5", "perda": "12"},
     {"traco": "1:0.5:6", "dois_lados": True, "chapisco": True})
caso("RE-B", "reboco", R)
caso("RE-B2", "reboco", {**R, "vaos": "5"})
caso("RE-B3", "reboco", R, {"dois_lados": True})
caso("RE-B4", "reboco", R, {"chapisco": True})
caso("RE-B5", "reboco", R, {"traco": "1:0:3"})
caso("RE-C1", "reboco", {"area": ""})
caso("RE-C2", "reboco", {**R, "esp": ""})
caso("RE-C3", "reboco", {"area": "trinta"})
caso("RE-C4", "reboco", {"area": "0"})
caso("RE-C5", "reboco", {"area": "-30"})
caso("RE-C6", "reboco", {**R, "esp": "0"})
caso("RE-C7", "reboco", {"area": "30,5"})
caso("RE-C8", "reboco", {"area": "30.5"})
caso("RE-C9", "reboco", {"area": "30 1/2"})
caso("RE-C10", "reboco", {**R, "vaos": "-5"})
caso("RE-C11", "reboco", {**R, "vaos": "30"})
caso("RE-C12", "reboco", {**R, "vaos": "40"})
caso("RE-C13", "reboco", {**R, "perda": "-5"})
caso("RE-C14", "reboco", {**R, "perda": "2,5"})
caso("RE-C15", "reboco", {"area": "1-21/2"})
caso("RE-C16", "reboco", {**R, "vaos": "abc"})
caso("RE-C17", "reboco", {"area": "100000"})
caso("RE-C18", "reboco", {**R, "esp": "20"})

# ---------------- PISO ----------------
PI = {"area": "40", "larg": "60", "alt": "60"}
caso("PI-A", "piso", {**PI, "caixa": "2,16", "perda": "12", "rodape": "30", "rodape_peca": "0,6"},
     {"desenho": True, "argamassa": "AC-II"})
caso("PI-B", "piso", PI)
caso("PI-B2", "piso", {**PI, "larg": "80", "alt": "80"})
caso("PI-B3", "piso", {**PI, "larg": "120", "alt": "60"})
caso("PI-B4", "piso", PI, {"desenho": True})
caso("PI-B5", "piso", {**PI, "caixa": "2,16"})
caso("PI-B6", "piso", {**PI, "rodape": "30"})
caso("PI-B7", "piso", {**PI, "rodape": "30", "rodape_peca": "0,6"})
caso("PI-B8", "piso", PI, {"argamassa": "AC-III"})
caso("PI-C1", "piso", {**PI, "area": ""})
caso("PI-C2", "piso", {**PI, "larg": ""})
caso("PI-C3", "piso", {**PI, "area": "quarenta"})
caso("PI-C4", "piso", {**PI, "area": "0"})
caso("PI-C5", "piso", {**PI, "area": "-40"})
caso("PI-C6", "piso", {**PI, "larg": "0"})
caso("PI-C7", "piso", {**PI, "area": "40,5"})
caso("PI-C8", "piso", {**PI, "area": "40.5"})
caso("PI-C9", "piso", {**PI, "area": "40 1/2"})
caso("PI-C10", "piso", {**PI, "perda": "-5"})
caso("PI-C11", "piso", {**PI, "perda": "2,5"})
caso("PI-C12", "piso", {**PI, "perda": "0"})
caso("PI-C13", "piso", {**PI, "caixa": "-2"})
caso("PI-C14", "piso", {**PI, "rodape": "-10"})
caso("PI-C15", "piso", {**PI, "area": "1-21/2"})
caso("PI-C16", "piso", {**PI, "larg": "70", "alt": "70"})
caso("PI-C17", "piso", {**PI, "larg": "90", "alt": "90"})
caso("PI-C18", "piso", {**PI, "larg": "60,5"})
caso("PI-C19", "piso", {**PI, "rodape_peca": "0,6"})
caso("PI-C20", "piso", {**PI, "area": "100000"})

# ---------------- AZULEJO ----------------
AZ = {"area": "30", "larg": "30", "alt": "60"}
caso("AZ-A", "azulejo", {**AZ, "vaos": "4", "caixa": "1,8", "perda": "15"},
     {"desenho": True, "argamassa": "AC-III"})
caso("AZ-B", "azulejo", AZ)
caso("AZ-B2", "azulejo", {**AZ, "vaos": "4"})
caso("AZ-B3", "azulejo", {**AZ, "caixa": "1,8"})
caso("AZ-B4", "azulejo", AZ, {"desenho": True})
caso("AZ-B5", "azulejo", AZ, {"argamassa": "AC-III"})
caso("AZ-B6", "azulejo", {**AZ, "alt": "90"})
caso("AZ-C1", "azulejo", {**AZ, "area": ""})
caso("AZ-C2", "azulejo", {**AZ, "alt": ""})
caso("AZ-C3", "azulejo", {**AZ, "area": "trinta"})
caso("AZ-C4", "azulejo", {**AZ, "area": "0"})
caso("AZ-C5", "azulejo", {**AZ, "area": "-30"})
caso("AZ-C6", "azulejo", {**AZ, "area": "30,5"})
caso("AZ-C7", "azulejo", {**AZ, "area": "30.5"})
caso("AZ-C8", "azulejo", {**AZ, "area": "30 1/2"})
caso("AZ-C9", "azulejo", {**AZ, "vaos": "-4"})
caso("AZ-C10", "azulejo", {**AZ, "vaos": "30"})
caso("AZ-C11", "azulejo", {**AZ, "vaos": "40"})
caso("AZ-C12", "azulejo", {**AZ, "perda": "-5"})
caso("AZ-C13", "azulejo", {**AZ, "perda": "2,5"})
caso("AZ-C14", "azulejo", {**AZ, "area": "1-21/2"})
caso("AZ-C15", "azulejo", {**AZ, "vaos": "abc"})
caso("AZ-C16", "azulejo", {**AZ, "area": "100000"})

# ---------------- REJUNTE ----------------
RJ = {"area": "40", "larg": "60", "alt": "60", "junta": "3"}
caso("RJ-A", "rejunte", {**RJ, "esp": "10", "perda": "15"})
caso("RJ-B", "rejunte", RJ)
caso("RJ-B2", "rejunte", {**RJ, "larg": "30", "alt": "30", "junta": "5"})
caso("RJ-B3", "rejunte", {"junta": "3"}, {"_usar_dados": ("piso", {"area": "40", "larg": "60", "alt": "60"})})
caso("RJ-B4", "rejunte", {"junta": "2"},
     {"_usar_dados": ("azulejo", {"area": "30", "vaos": "4", "larg": "30", "alt": "60"})})
caso("RJ-C1", "rejunte", {**RJ, "area": ""})
caso("RJ-C2", "rejunte", {**RJ, "junta": ""})
caso("RJ-C3", "rejunte", {**RJ, "area": "quarenta"})
caso("RJ-C4", "rejunte", {**RJ, "area": "0"})
caso("RJ-C5", "rejunte", {**RJ, "area": "-40"})
caso("RJ-C6", "rejunte", {**RJ, "junta": "0"})
caso("RJ-C7", "rejunte", {**RJ, "junta": "-3"})
caso("RJ-C8", "rejunte", {**RJ, "area": "40,5"})
caso("RJ-C9", "rejunte", {**RJ, "area": "40.5"})
caso("RJ-C10", "rejunte", {**RJ, "area": "40 1/2"})
caso("RJ-C11", "rejunte", {**RJ, "junta": "1,5"})
caso("RJ-C12", "rejunte", {**RJ, "junta": "1/2"})
caso("RJ-C13", "rejunte", {**RJ, "esp": ""})
caso("RJ-C14", "rejunte", {**RJ, "esp": "0"})
caso("RJ-C15", "rejunte", {**RJ, "perda": "-5"})
caso("RJ-C16", "rejunte", {**RJ, "perda": "2,5"})
caso("RJ-C17", "rejunte", {**RJ, "area": "1-21/2"})
caso("RJ-C18", "rejunte", {**RJ, "area": "1"})
caso("RJ-C19", "rejunte", {**RJ, "area": "100000"})
caso("RJ-C20", "rejunte", {**RJ, "junta": "30"})

# ---------------- PINTURA ----------------
PT = {"parede": "100"}
caso("PT-A", "pintura", {"parede": "100", "teto": "40", "demaos": "3", "rend": "10", "perda": "15"},
     {"selador": True, "massa_tipo": "corrida", "fundo": True})
caso("PT-B", "pintura", PT)
caso("PT-B2", "pintura", {"parede": "", "teto": "40"})
caso("PT-B3", "pintura", {**PT, "teto": "40"})
caso("PT-B4", "pintura", PT, {"selador": True})
caso("PT-B5", "pintura", PT, {"massa_tipo": "acrilica"})
caso("PT-B6", "pintura", PT, {"fundo": True})
caso("PT-B7", "pintura", {"parede": "180"})
caso("PT-B8", "pintura", {"parede": "10"})
caso("PT-C1", "pintura", {"parede": "", "teto": ""})
caso("PT-C2", "pintura", {**PT, "demaos": ""})
caso("PT-C3", "pintura", {"parede": "cem"})
caso("PT-C4", "pintura", {"parede": "0"})
caso("PT-C5", "pintura", {"parede": "-100"})
caso("PT-C6", "pintura", {**PT, "demaos": "0"})
caso("PT-C7", "pintura", {**PT, "demaos": "-2"})
caso("PT-C8", "pintura", {**PT, "demaos": "2,5"})
caso("PT-C9", "pintura", {**PT, "demaos": "5"})
caso("PT-C10", "pintura", {**PT, "demaos": "6"})
caso("PT-C11", "pintura", {**PT, "demaos": "22"})
caso("PT-C12", "pintura", {"parede": "100,5"})
caso("PT-C13", "pintura", {"parede": "100.5"})
caso("PT-C14", "pintura", {"parede": "100 1/2"})
caso("PT-C15", "pintura", {**PT, "rend": "0"})
caso("PT-C16", "pintura", {**PT, "rend": ""})
caso("PT-C17", "pintura", {**PT, "rend": "12,5"})
caso("PT-C18", "pintura", {**PT, "perda": "-5"})
caso("PT-C19", "pintura", {**PT, "perda": "2,5"})
caso("PT-C20", "pintura", {"parede": "1-21/2"})
caso("PT-C21", "pintura", {"parede": "100000"})

# ---------------- ESQUADRIAS ----------------
TODOS = {"espuma": True, "parafusos": True, "argamassa": True}
P3 = ("add", "porta", "nao_informado", "3", "80", "210")
J2 = ("add", "janela", "nao_informado", "2", "120", "100")
def esq(*acoes, fix=None):
    return {"acoes": list(acoes), "fix": fix or {}}
caso("ES-A", "esquadrias", {}, esq(
    ("add", "porta", "madeira", "3", "80", "210"), ("add", "porta", "aluminio", "1", "90", "210"),
    ("add", "janela", "aluminio", "4", "120", "100"), ("add", "janela", "vidro", "1", "60", "60"), fix=TODOS))
caso("ES-B", "esquadrias", {}, esq(P3, J2))
caso("ES-B2", "esquadrias", {}, esq(P3, J2, fix={"espuma": True}))
caso("ES-B3", "esquadrias", {}, esq(P3, J2, fix={"parafusos": True}))
caso("ES-B4", "esquadrias", {}, esq(P3, J2, fix={"argamassa": True}))
caso("ES-B5", "esquadrias", {}, esq(P3, J2, ("add", "porta", "nao_informado", "2", "80", "210")))
caso("ES-B6", "esquadrias", {}, esq(P3, J2, ("rem", 1)))
caso("ES-C1", "esquadrias", {}, esq())
caso("ES-C2", "esquadrias", {}, esq(("add", "porta", "nao_informado", "", "80", "210")))
caso("ES-C3", "esquadrias", {}, esq(("add", "porta", "nao_informado", "três", "80", "210")))
caso("ES-C4", "esquadrias", {}, esq(("add", "porta", "nao_informado", "0", "80", "210")))
caso("ES-C5", "esquadrias", {}, esq(("add", "porta", "nao_informado", "-3", "80", "210")))
caso("ES-C6", "esquadrias", {}, esq(("add", "porta", "nao_informado", "2,5", "80", "210")))
caso("ES-C7", "esquadrias", {}, esq(("add", "porta", "nao_informado", "3", "0", "210")))
caso("ES-C8", "esquadrias", {}, esq(("add", "porta", "nao_informado", "3", "1-21/2", "210")))
caso("ES-C9", "esquadrias", {"qtd": "3", "larg": "80", "alt": "210"}, esq())
caso("ES-C10a", "esquadrias", {}, esq(("add", "janela", "nao_informado", "1", "120,5", "100")))
caso("ES-C10b", "esquadrias", {}, esq(("add", "janela", "nao_informado", "1", "120.5", "100")))
caso("ES-C10c", "esquadrias", {}, esq(("add", "janela", "nao_informado", "1", "120 1/2", "100")))
caso("ES-C11", "esquadrias", {}, esq(("add", "porta", "nao_informado", "1", "80", "210"), fix=TODOS))
caso("ES-C12", "esquadrias", {}, esq(("add", "porta", "nao_informado", "1000", "80", "210"), fix=TODOS))
caso("ES-C13", "esquadrias", {}, esq(("add", "porta", "nao_informado", "3", "8000", "210")))



# =====================================================================
# RESULTADO ESPERADO: lido do testes_rodada2.md a cada execução (nunca da saída do app)
# - Blocos completos do .md (Teste A, A2, B e "**B2:**"...): compara o texto inteiro.
# - Linhas das tabelas (B2..., C1...): cada trecho entre aspas e cada número tem que aparecer
#   no que o app mostrou; mensagem sem aspas (ex.: "Error: ...") tem que ser a linha inteira;
#   "Igual ao Teste B" = bloco inteiro do Teste B da aba.
# - Texto fora das aspas que é explicação (Janela, Cancel → não calcula, Continue →, Todos:,
#   (nada entra na lista), no "Add to list", / e ;) não é comparado. O título "Check the values"
#   e os botões só dá pra ver na tela.
# - Janela que o .md não cita e problemas na lista da Esquadrias aparecem como "! aviso"
#   (não mudam o OK/DIFERENTE).
# =====================================================================
MD = os.path.join(PROJ, "testes_manuais", "testes_rodada2.md")
SECOES = {"BROCAS": "BR", "BALDRAME": "BA", "PAREDES": "PA", "LAJE": "LA", "TELHADO": "TE",
          "ELÉTRICA": "EL", "HIDRÁULICA": "HI", "CONTRAPISO": "CP", "REBOCO": "RE", "PISO": "PI",
          "AZULEJO": "AZ", "REJUNTE": "RJ", "PINTURA": "PT", "ESQUADRIAS": "ES"}
MARCAS_SCRIPT = ("[TROCA]", "[BOTÃO]", "[CAMPOS]")  # linhas escritas pelo script, não pelo app


def ler_md():
    """blocos["BR-A"] = texto do bloco; linhas["BR-C3"] = célula "Esperado" da tabela;
    prosa["TE"] = linhas soltas da seção (para os casos C21/C22 de troca de tipo)."""
    blocos, linhas, prosa = {}, {}, {}
    prefixo = rotulo = None
    em_bloco, buf = False, []
    with open(MD, encoding="utf-8") as f:
        texto = f.read()
    for ln in texto.splitlines():
        m = re.match(r"^# (\S+)", ln)
        if m and m.group(1) in SECOES:
            prefixo, rotulo = SECOES[m.group(1)], None
            continue
        if prefixo is None:
            continue
        if ln.startswith("```"):
            if em_bloco and rotulo:
                blocos[f"{prefixo}-{rotulo}"] = "\n".join(buf)
            em_bloco, buf = not em_bloco, []
            continue
        if em_bloco:
            buf.append(ln)
            continue
        m = re.match(r"^### Teste (A2|A|B)\b", ln) or re.match(r"^\*\*(B\d+):\*\*", ln)
        if m:
            rotulo = m.group(1)
            continue
        if ln.startswith("### "):
            rotulo = None
        m = re.match(r"^\|\s*([ABC]\d+[a-z]?(?:,\s*[ABC]\d+[a-z]?)*)\s*\|", ln)
        if m:
            celulas = [c.strip() for c in ln.strip().strip("|").split("|")]
            for r in re.split(r",\s*", m.group(1)):
                linhas[f"{prefixo}-{r}"] = celulas[-1]
            continue
        prosa.setdefault(prefixo, []).append(ln)
    return blocos, linhas, prosa


BLOCOS, LINHAS, PROSA = ler_md()


def _linha_md(nome):
    """Acha a linha da tabela do caso: BR-C6 (exata), BR-C14 para BR-C14-cancelar, PA-C12 para PA-C12a."""
    if nome in LINHAS:
        return LINHAS[nome]
    for chave in sorted(LINHAS, key=len, reverse=True):
        if nome.startswith(chave) and not nome[len(chave)].isdigit():
            return LINHAS[chave]
    return None


def _prosa(prefixo, inicio):
    return next((l for l in PROSA.get(prefixo, []) if l.startswith(inicio)), "")


def _sem_marcas(saida):
    return "\n".join(l for l in saida.splitlines() if not l.startswith(MARCAS_SCRIPT)).strip()


def _numeros(texto):
    return re.findall(r"\d+(?:[.,]\d+)*", texto)


# Cada conferência vira um par (esperado, o que o app mostrou, ok?), para mostrar lado a lado.

def checar_texto(esperado, saida):
    """Bloco completo (Teste A/B, "**B2:**", "Igual ao Teste B"): texto inteiro, linha por linha."""
    esp, app = esperado.strip().splitlines(), _sem_marcas(saida).splitlines()
    return [(e or "", a or "", e == a) for e, a in itertools.zip_longest(esp, app)]


def _parecida(trecho, linhas):
    """A linha do app mais parecida com o trecho (só para mostrar ao lado)."""
    return max(linhas, key=lambda l: difflib.SequenceMatcher(None, trecho, l).ratio(), default="")


def checar_trechos(trechos, saida, linhas=None):
    """Cada trecho entre aspas tem que aparecer; os números de dentro dele também."""
    linhas = linhas if linhas is not None else saida.splitlines()
    pares = []
    for t in trechos:
        ok = t in saida and all(n in saida for n in _numeros(t))
        pares.append((f'"{t}"', next((l for l in linhas if t in l), _parecida(t, linhas)), ok))
    return pares


def checar_celula(cel, saida, nome):
    """Regras da tabela: "Igual ao Teste B" = bloco inteiro; mensagem sem aspas = linha exata;
    o resto fora das aspas (Janela, Cancel →, Continue →, Todos:, (nada entra na lista), / e ;)
    é explicação: só os trechos entre aspas (e os números de dentro deles) são conferidos."""
    linhas = saida.splitlines()
    cel = cel.strip()
    if " / " in cel and "Cancel →" in cel:  # C14/C16: a parte do Cancel e a do Continue na mesma célula
        quer = "Cancel →" if nome.endswith("-cancelar") else "Continue →"
        cel = next(p for p in cel.split(" / ") if quer in p).strip()
    pares = []
    m = re.match(r'^Janela "[^"]*"(?: no "[^"]*")?: "([^"]*)" (?:Cancel|Continue) →\s*(.*)$', cel)
    if m:  # a mensagem da janela é trecho entre aspas; o título e o botão são explicação
        msg, cel = m.groups()
        janelas = [l for l in linhas if l.startswith("[JANELA")]
        pares += checar_trechos([msg], "\n".join(janelas), janelas)
    cel = re.sub(r"^Todos:\s*", "", cel)
    m = re.fullmatch(r"[Ii]gual ao Teste (\w+)", cel)
    if m:
        return pares + checar_texto(BLOCOS[f"{nome[:2]}-{m.group(1)}"], saida)
    if not re.match(r"^(Error:|Please enter valid numbers|No doors or windows|You entered a door)", cel):
        # não é mensagem: só os trechos entre aspas (ex.: "não calcula" depois do Cancel não tem nenhum)
        return pares + checar_trechos(re.findall(r'"([^"]*)"', cel), saida)
    msg = cel.replace("(nada entra na lista)", "").strip()
    # Mensagem sozinha: é o texto exato de uma linha da tela (na Esquadrias, pode ser a do Adicionar)
    candidatas = [l.removeprefix("[Adicionar] ") for l in linhas] if nome.startswith("ES-") else linhas[-1:]
    ok = msg in candidatas
    return pares + [(msg, msg if ok else (candidatas[-1] if candidatas else ""), ok)]


def checar(nome, saida):
    """Lista de pares (esperado, app, ok), ou None se o .md não tem esperado para o caso."""
    if nome in BLOCOS:
        return checar_texto(BLOCOS[nome], saida)
    linha = _linha_md(nome)
    if linha is not None:
        return checar_celula(linha, saida, nome)
    troca = next((l for l in saida.splitlines() if l.startswith("[TROCA]")), "")
    if nome == "TE-C21":  # "troque para Fiber cement: ela vira 15. Volte para Clay: vira 30 de novo."
        a, b = re.findall(r"vira (\d+)", _prosa("TE", "C21:"))[:2]
        esp = f"[TROCA] fibrocimento->{a}, ceramica->{b}"
        return [(f"inclinação vira {a}, depois {b}", troca, esp == troca)]
    if nome == "TE-C22":  # "continua 35 ... Resultado: "Roof tiles ...""
        p = _prosa("TE", "C22:")
        incl = re.search(r"continua (\d+)", p).group(1)
        return ([(f"inclinação continua {incl}", troca, troca == f"[TROCA] fibrocimento->{incl}")]
                + checar_trechos(re.findall(r'"([^"]*)"', p.split("Resultado:")[1]), saida))
    if nome == "LA-C22-volta":  # o .md diz que os dados do Teste A continuam lá ao voltar para pré-moldada
        return checar_texto(BLOCOS["LA-A"], saida)
    return None


def avisos(nome, saida):
    """Coisas para olhar que não são comparação de texto (não mudam o OK/DIFERENTE)."""
    av = []
    if "FICOU" in saida:
        av.append("o resultado antigo ficou na tela depois do X")
    if "NÃO ficaram vazios" in saida:
        av.append("os campos não ficaram vazios depois do Adicionar")
    linha = _linha_md(nome) or ""
    if "nada entrou na lista" in saida and "(nada entra na lista)" not in linha:
        av.append("um item não entrou na lista")
    if "Janela" not in linha and any(l.startswith("[JANELA") for l in saida.splitlines()):
        av.append("abriu uma janela que o .md não cita")
    return av


def lado_a_lado(pares, largura=62):
    corta = lambda s: s if len(s) <= largura else s[:largura - 1] + "…"
    out = [f"   {'ESPERADO (.md)':<{largura}} | O APP MOSTROU"]
    for e, a, ok in pares:
        out.append(f" {' ' if ok else '≠'} {corta(e):<{largura}} | {a}")
    return "\n".join(out)


# ---------------- PALAVRAS PARA CONFERIR (não mudam o OK/DIFERENTE) ----------------
_PT = set("""de do da dos das com sem para por favor digite campos deve devem maiores menores que
sacos saco barras barra perda custo estimado etapa erro areia cimento brita ferro estribos estribo arame obra
rolos rolo latas lata galões galao baldes balde caixas caixa cada mil tijolo bloco cal tomadas interruptores
portas porta janelas janela fio esgoto fria quente rejunte argamassa massa selador fundo tinta parede paredes
teto lista piso azulejo junta espessura consumo cumeeira madeiramento ripas caibros terças laje enchimento capa
tela painéis estimado projeto incluso inclui emendas un peças peça telhas telha área limite mínimo
é ou e até acima pontos conexões registros tubos tubo barras metros""".split())
_PREFIXOS_SCRIPT = ("[JANELA no Adicionar] ", "[JANELA] ", "[Adicionar] ", "[X] ")


def suspeitas(saida):
    """Palavras em português e chaves (tipo erro_xxx) no que o app mostrou."""
    achou = []
    for l in saida.splitlines():
        if l.startswith(MARCAS_SCRIPT) or l.startswith("[X] ") or l in ("[Cancelar] não calculou",
                                                                        "[Adicionar] nada entrou na lista"):
            continue
        for p in _PREFIXOS_SCRIPT:
            if l.startswith(p):
                l = l[len(p):]
        for chave in re.findall(r"\b[a-z]+_[a-z0-9_]+\b", l):
            achou.append(f"chave? {chave}")
        for pal in re.findall(r"[A-Za-zÀ-ÿ]+", l):
            if pal.lower() in _PT or re.search(r"[ãõçáéíóúâêôà]", pal.lower()):
                achou.append(pal)
        if "c/" in l:
            achou.append("c/")
    return sorted(set(achou))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ver = "--ver" in sys.argv
    filtro = args[0] if args else ""
    ok, diferentes, sem_esperado = 0, [], []
    for nome, aba, campos, esc, cont in CASOS:
        if not nome.startswith(filtro):
            continue
        resultado = rodar(aba, campos, esc, cont)
        pares = checar(nome, resultado)
        if pares is None:
            sem_esperado.append(nome)
            print(f"SEM ESPERADO  {nome}\n{resultado}\n")
            continue
        igual = all(p[2] for p in pares)
        if igual:
            ok += 1
            print(f"OK         {nome}")
        else:
            diferentes.append(nome)
            print(f"DIFERENTE  {nome}")
        for a in avisos(nome, resultado):
            print(f"   ! aviso: {a}")
        sus = suspeitas(resultado)
        if sus:
            print(f"   ! conferir palavras: {', '.join(sus)}")
        if ver or not igual:
            print(f"--- digitado: {campos}" + (f" | escolhas: {esc}" if esc else "")
                  + ("" if cont else " | Cancelar na janela"))
            print(lado_a_lado(pares))
            if ver:
                print("--- o app mostrou (tudo):\n" + resultado.strip())
            print()
    print(f"\n{ok} OK, {len(diferentes)} DIFERENTE(S)" + (f", {len(sem_esperado)} sem esperado" if sem_esperado else ""))
    if diferentes:
        print("Diferentes: " + ", ".join(diferentes))


if __name__ == "__main__":
    main()
