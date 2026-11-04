r"""Rodada 1 (Brasil, português): roda os casos das 14 abas do testes_rodada1.md pelo mesmo caminho da tela
(CalculatorScreen._calcular_aba), sem abrir janela: kivy/kivymd são trocados por módulos falsos.
Não grava nada no projeto (rodar com python -B).

O resultado esperado de cada caso fica no fim deste arquivo (ESPERADO). O script compara o que o app
mostra com o esperado e diz OK ou DIFERENTE em cada caso; no fim, mostra quantos deram OK.
Atualizado em 04/11/2026, no fim das correções de visual da rodada 1 (versão principal: a do PC).

Como rodar (no terminal, na pasta C:\Calc\Calculadora):
  env311\Scripts\python.exe -B testes_manuais\rodada1.py           -> todos os casos
  env311\Scripts\python.exe -B testes_manuais\rodada1.py PI-        -> só uma aba (prefixo: BR-, BA-, PA-...)
  env311\Scripts\python.exe -B testes_manuais\rodada1.py PI- --ver  -> mostra também o resultado de cada caso

Quando uma mudança no código é DE PROPÓSITO (ex.: um texto novo), o esperado precisa ser atualizado aqui
e no testes_rodada1.md, sabendo o motivo. Quando é SEM QUERER, o script avisa (DIFERENTE)."""
import sys, types, importlib.abc, importlib.machinery

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
# =====================================================================
ESPERADO = {
"BR-A": """\
Traço: 1:3:3
Volume Total (com 12% de perda): 2,309 m³
• Cimento: 15 sacos de 50 kg (R$ 540,00)
• Areia: 1,48 m³ (R$ 162,80)
• Brita: 1,48 m³ (R$ 177,60)
Gaiola de ferro: 1,75 m de cada broca
• Ferro 10 mm: 57,0 kg (8 barras de 12 m)
• Estribos 5 mm c/ 15 cm: 14,8 kg (9 barras de 12 m)
• Aço/Ferragem: 71,8 kg (R$ 682,20)
• Arame recozido: 1,4 kg (R$ 21,60)
• Mão de Obra: 42,0 m (R$ 1.260,00)

Custo Estimado da Etapa: R$ 2.844,20""",
"BR-B": """\
Traço: 1:2:3
Volume Total (com 10% de perda): 1,037 m³
• Cimento: 8 sacos de 50 kg (R$ 288,00)
• Areia: 0,52 m³ (R$ 57,20)
• Brita: 0,78 m³ (R$ 93,60)

Custo Estimado da Etapa: R$ 438,80""",
"BR-B2": """\
Traço: 1:2:3
Volume Total (com 10% de perda): 1,037 m³
• Cimento: 8 sacos de 50 kg (R$ 288,00)
• Areia: 0,52 m³ (R$ 57,20)
• Brita: 0,78 m³ (R$ 93,60)
Gaiola de ferro: 1,50 m de cada broca
• Ferro 8 mm: 26,1 kg (6 barras de 12 m)
• Estribos 5 mm c/ 20 cm: 6,3 kg (4 barras de 12 m)
• Aço/Ferragem: 32,4 kg (R$ 307,61)
• Arame recozido: 0,7 kg (R$ 9,75)

Custo Estimado da Etapa: R$ 756,16""",
"BR-C1": """\
Por favor, digite números válidos nos campos!""",
"BR-C2": """\
Por favor, digite números válidos nos campos!""",
"BR-C3": """\
Erro: Quantidade, profundidade e diâmetro devem ser maiores que zero.""",
"BR-C4": """\
Erro: Quantidade, profundidade e diâmetro devem ser maiores que zero.""",
"BR-C5": """\
Por favor, digite números válidos nos campos!""",
"BR-C6": """\
Traço: 1:2:3
Volume Total (com 10% de perda): 0,864 m³
• Cimento: 7 sacos de 50 kg (R$ 252,00)
• Areia: 0,43 m³ (R$ 47,30)
• Brita: 0,65 m³ (R$ 78,00)

Custo Estimado da Etapa: R$ 377,30""",
"BR-C7": """\
Traço: 1:2:3
Volume Total (com 10% de perda): 0,864 m³
• Cimento: 7 sacos de 50 kg (R$ 252,00)
• Areia: 0,43 m³ (R$ 47,30)
• Brita: 0,65 m³ (R$ 78,00)

Custo Estimado da Etapa: R$ 377,30""",
"BR-C8": """\
Traço: 1:2:3
Volume Total (com 10% de perda): 0,864 m³
• Cimento: 7 sacos de 50 kg (R$ 252,00)
• Areia: 0,43 m³ (R$ 47,30)
• Brita: 0,65 m³ (R$ 78,00)

Custo Estimado da Etapa: R$ 377,30""",
"BR-C9": """\
Erro: A perda não pode ser negativa.""",
"BR-C10": """\
Traço: 1:2:3
Volume Total (com 2,5% de perda): 0,966 m³
• Cimento: 8 sacos de 50 kg (R$ 288,00)
• Areia: 0,48 m³ (R$ 52,80)
• Brita: 0,72 m³ (R$ 86,40)

Custo Estimado da Etapa: R$ 427,20""",
"BR-C11": """\
Erro: Diâmetro muito pequeno para colocar estribos.""",
"BR-C12": """\
Erro: Barras e espaçamento dos estribos não podem ser negativos.""",
"BR-C13": """\
Por favor, digite números válidos nos campos!""",
"BR-C14-cancelar": """\
[JANELA] Profundidade de 300 m: o limite é 30 m.
[Cancelar] não calculou""",
"BR-C14-continuar": """\
[JANELA] Profundidade de 300 m: o limite é 30 m.
Traço: 1:2:3
Volume Total (com 10% de perda): 103,673 m³
• Cimento: 778 sacos de 50 kg (R$ 28.008,00)
• Areia: 51,84 m³ (R$ 5.702,40)
• Brita: 77,75 m³ (R$ 9.330,00)

Custo Estimado da Etapa: R$ 43.040,40""",
"BR-C15": """\
Traço: 1:2:3
Volume Total (com 10% de perda): 1,037 m³
• Cimento: 8 sacos de 50 kg (R$ 288,00)
• Areia: 0,52 m³ (R$ 57,20)
• Brita: 0,78 m³ (R$ 93,60)
Gaiola de ferro: 1,50 m de cada broca
• Ferro 8 mm: 26,1 kg (6 barras de 12 m)
• Aço/Ferragem: 26,1 kg (R$ 247,66)
• Arame recozido: 0,5 kg (R$ 7,80)

Custo Estimado da Etapa: R$ 694,26""",
"BR-C16": """\
Traço: 1:2:3
Volume Total (com 10% de perda): 1,037 m³
• Cimento: 8 sacos de 50 kg (R$ 288,00)
• Areia: 0,52 m³ (R$ 57,20)
• Brita: 0,78 m³ (R$ 93,60)
Gaiola de ferro: 1,50 m de cada broca
• Ferro 8 mm: 26,1 kg (6 barras de 12 m)
• Estribos 5 mm c/ 12,5 cm: 9,5 kg (6 barras de 12 m)
• Aço/Ferragem: 35,5 kg (R$ 337,54)
• Arame recozido: 0,7 kg (R$ 10,65)

Custo Estimado da Etapa: R$ 786,99""",
"BR-C17": """\
Traço: 1:2:3
Volume Total (com 10% de perda): 10,367 m³
• Cimento: 78 sacos de 50 kg (R$ 2.808,00)
• Areia: 5,18 m³ (R$ 569,80)
• Brita: 7,78 m³ (R$ 933,60)

Custo Estimado da Etapa: R$ 4.311,40""",
"BR-C18": """\
Por favor, digite números válidos nos campos!""",
"BA-A": """\
Traço: 1:4:3
Volume Total (com 8% de perda): 2,592 m³
• Cimento: 15 sacos de 50 kg (R$ 540,00)
• Areia: 1,94 m³ (R$ 213,40)
• Brita: 1,46 m³ (R$ 175,20)
• Ferro 12,5 mm: 197,0 kg (18 barras de 12 m) (inclui 6,00 m de emendas)
• Estribos 5 mm c/ 15 cm: 34,4 kg (19 barras de 12 m)
• Aço/Ferragem: 231,4 kg (R$ 2.198,49)
• Arame recozido: 4,6 kg (R$ 69,45)
• Impermeabilizante: 30,0 m² · 24,0 L = 1 lata de 18 L e 2 galões de 3,6 L (R$ 390,60)
• Mão de Obra: 30,0 m (R$ 1.200,00)

Custo Estimado da Etapa: R$ 4.787,14""",
"BA-B": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0,788 m³
• Cimento: 6 sacos de 50 kg (R$ 216,00)
• Areia: 0,39 m³ (R$ 42,90)
• Brita: 0,59 m³ (R$ 70,80)

Custo Estimado da Etapa: R$ 329,70""",
"BA-B2": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0,788 m³
• Cimento: 6 sacos de 50 kg (R$ 216,00)
• Areia: 0,39 m³ (R$ 42,90)
• Brita: 0,59 m³ (R$ 70,80)
• Ferro 8 mm: 22,3 kg (5 barras de 12 m) (inclui 1,28 m de emendas)
• Estribos 5 mm c/ 20 cm: 8,6 kg (5 barras de 12 m)
• Aço/Ferragem: 30,9 kg (R$ 293,74)
• Arame recozido: 0,6 kg (R$ 9,30)

Custo Estimado da Etapa: R$ 632,74""",
"BA-B3": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0,788 m³
• Cimento: 6 sacos de 50 kg (R$ 216,00)
• Areia: 0,39 m³ (R$ 42,90)
• Brita: 0,59 m³ (R$ 70,80)
• Impermeabilizante: 10,0 m² · 8,0 L = 3 galões de 3,6 L (R$ 167,40)

Custo Estimado da Etapa: R$ 497,10""",
"BA-C1": """\
Por favor, digite números válidos nos campos!""",
"BA-C2": """\
Por favor, digite números válidos nos campos!""",
"BA-C3": """\
Erro: Valores devem ser maiores que zero.""",
"BA-C4": """\
Erro: Valores devem ser maiores que zero.""",
"BA-C5": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0,788 m³
• Cimento: 6 sacos de 50 kg (R$ 216,00)
• Areia: 0,39 m³ (R$ 42,90)
• Brita: 0,59 m³ (R$ 70,80)

Custo Estimado da Etapa: R$ 329,70""",
"BA-C6": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0,788 m³
• Cimento: 6 sacos de 50 kg (R$ 216,00)
• Areia: 0,39 m³ (R$ 42,90)
• Brita: 0,59 m³ (R$ 70,80)

Custo Estimado da Etapa: R$ 329,70""",
"BA-C7": """\
Erro: A perda não pode ser negativa.""",
"BA-C8": """\
Traço: 1:2:3
Volume Total (com 2,5% de perda): 0,769 m³
• Cimento: 6 sacos de 50 kg (R$ 216,00)
• Areia: 0,38 m³ (R$ 41,80)
• Brita: 0,58 m³ (R$ 69,60)

Custo Estimado da Etapa: R$ 327,40""",
"BA-C9": """\
[JANELA] Viga de 4 cm x 30 cm: o mínimo é 20 cm de largura e 30 cm de altura.
Erro: Viga muito pequena para colocar estribos.""",
"BA-C10": """\
Erro: Barras e espaçamento dos estribos não podem ser negativos.""",
"BA-C11": """\
Por favor, digite números válidos nos campos!""",
"BA-C12": """\
Por favor, digite números válidos nos campos!""",
"BA-C13": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0,788 m³
• Cimento: 6 sacos de 50 kg (R$ 216,00)
• Areia: 0,39 m³ (R$ 42,90)
• Brita: 0,59 m³ (R$ 70,80)
• Ferro 8 mm: 22,3 kg (5 barras de 12 m) (inclui 1,28 m de emendas)
• Estribos 5 mm c/ 12,5 cm: 13,9 kg (8 barras de 12 m)
• Aço/Ferragem: 36,1 kg (R$ 343,33)
• Arame recozido: 0,7 kg (R$ 10,80)

Custo Estimado da Etapa: R$ 683,83""",
"BA-C14": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0,756 m³
• Cimento: 6 sacos de 50 kg (R$ 216,00)
• Areia: 0,38 m³ (R$ 41,80)
• Brita: 0,57 m³ (R$ 68,40)
• Ferro 8 mm: 20,9 kg (5 barras de 12 m)
• Estribos 5 mm c/ 20 cm: 8,4 kg (5 barras de 12 m)
• Aço/Ferragem: 29,2 kg (R$ 277,69)
• Arame recozido: 0,6 kg (R$ 8,70)

Custo Estimado da Etapa: R$ 612,59""",
"BA-C15": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 1,512 m³
• Cimento: 12 sacos de 50 kg (R$ 432,00)
• Areia: 0,76 m³ (R$ 83,60)
• Brita: 1,13 m³ (R$ 135,60)
• Ferro 8 mm: 42,3 kg (9 barras de 12 m) (inclui 1,28 m de emendas)
• Estribos 5 mm c/ 20 cm: 16,6 kg (9 barras de 12 m)
• Aço/Ferragem: 58,9 kg (R$ 559,26)
• Arame recozido: 1,2 kg (R$ 17,70)

Custo Estimado da Etapa: R$ 1.228,16""",
"BA-C16": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0,788 m³
• Cimento: 6 sacos de 50 kg (R$ 216,00)
• Areia: 0,39 m³ (R$ 42,90)
• Brita: 0,59 m³ (R$ 70,80)
• Ferro 8 mm: 22,3 kg (5 barras de 12 m) (inclui 1,28 m de emendas)
• Aço/Ferragem: 22,3 kg (R$ 211,66)
• Arame recozido: 0,5 kg (R$ 6,75)

Custo Estimado da Etapa: R$ 548,11""",
"BA-C17": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 315,000 m³
• Cimento: 2.363 sacos de 50 kg (R$ 85.068,00)
• Areia: 157,50 m³ (R$ 17.325,00)
• Brita: 236,25 m³ (R$ 28.350,00)

Custo Estimado da Etapa: R$ 130.743,00""",
"BA-C18": """\
[JANELA] Viga de 0,2 cm x 0,3 cm: o mínimo é 20 cm de largura e 30 cm de altura.
Traço: 1:2:3
Volume Total (com 5% de perda): 0,000 m³
• Cimento: 1 saco de 50 kg (R$ 36,00)

Custo Estimado da Etapa: R$ 36,00""",
"BA-C19": """\
[JANELA] Viga de 19 cm x 30 cm: o mínimo é 20 cm de largura e 30 cm de altura.
Traço: 1:2:3
Volume Total (com 5% de perda): 0,748 m³
• Cimento: 6 sacos de 50 kg (R$ 216,00)
• Areia: 0,37 m³ (R$ 40,70)
• Brita: 0,56 m³ (R$ 67,20)

Custo Estimado da Etapa: R$ 323,90""",
"BA-C20": """\
[JANELA] Viga de 20 cm x 29,5 cm: o mínimo é 20 cm de largura e 30 cm de altura.
Traço: 1:2:3
Volume Total (com 5% de perda): 0,774 m³
• Cimento: 6 sacos de 50 kg (R$ 216,00)
• Areia: 0,39 m³ (R$ 42,90)
• Brita: 0,58 m³ (R$ 69,60)

Custo Estimado da Etapa: R$ 328,50""",
"BA-C21": """\
Por favor, digite números válidos nos campos!""",
"BA-C22": """\
Traço: 1:2:3
Volume Total (com 5% de perda): 0,158 m³
• Cimento: 2 sacos de 50 kg (R$ 72,00)
• Areia: 0,08 m³ (R$ 8,80)
• Brita: 0,12 m³ (R$ 14,40)

Custo Estimado da Etapa: R$ 95,20""",
"PA-A": """\
Área bruta: 80,00 m²
Vãos (portas e janelas): 12,50 m²
Área líquida: 67,50 m²
Traço: 1:0,5:6
• Bloco de concreto (14x19x39): 1.162 un (1,16 milheiro) (R$ 5.229,00)
• Cimento: 8 sacos de 50 kg (R$ 288,00)
• Cal: 7 sacos de 20 kg (R$ 126,00)
• Areia: 1,84 m³ (R$ 202,40)

Custo Estimado da Etapa: R$ 5.845,40""",
"PA-B": """\
Área bruta: 30,00 m²
Traço: 1:2:8
• Tijolo baiano (9x19x19): 788 un (0,79 milheiro) (R$ 945,60)
• Cimento: 1 saco de 50 kg (R$ 36,00)
• Cal: 3 sacos de 20 kg (R$ 54,00)
• Areia: 0,26 m³ (R$ 28,60)

Custo Estimado da Etapa: R$ 1.064,20""",
"PA-B2": """\
Área bruta: 30,00 m²
Traço: 1:2:8
• Bloco de concreto (19x19x39): 394 un (0,39 milheiro) (R$ 2.364,00)
• Cimento: 2 sacos de 50 kg (R$ 72,00)
• Cal: 5 sacos de 20 kg (R$ 90,00)
• Areia: 0,42 m³ (R$ 46,20)

Custo Estimado da Etapa: R$ 2.572,20""",
"PA-B3": """\
Área bruta: 30,00 m²
Traço: 1:2:8
• Tijolo baiano 9 furos (9x14x19): 1.575 un (1,58 milheiro) (R$ 1.575,00)
• Cimento: 2 sacos de 50 kg (R$ 72,00)
• Cal: 7 sacos de 20 kg (R$ 126,00)
• Areia: 0,61 m³ (R$ 67,10)

Custo Estimado da Etapa: R$ 1.840,10""",
"PA-B4": """\
Área bruta: 30,00 m²
Traço: 1:0:3
• Tijolo baiano (9x19x19): 788 un (0,79 milheiro) (R$ 945,60)
• Cimento: 3 sacos de 50 kg (R$ 108,00)
• Areia: 0,27 m³ (R$ 29,70)

Custo Estimado da Etapa: R$ 1.083,30""",
"PA-C1": """\
Por favor, digite números válidos nos campos!""",
"PA-C2": """\
Por favor, digite números válidos nos campos!""",
"PA-C3": """\
Erro: A área da parede deve ser maior que zero.""",
"PA-C4": """\
Erro: A área da parede deve ser maior que zero.""",
"PA-C5": """\
Área bruta: 30,50 m²
Traço: 1:2:8
• Tijolo baiano (9x19x19): 801 un (0,80 milheiro) (R$ 961,20)
• Cimento: 1 saco de 50 kg (R$ 36,00)
• Cal: 3 sacos de 20 kg (R$ 54,00)
• Areia: 0,27 m³ (R$ 29,70)

Custo Estimado da Etapa: R$ 1.080,90""",
"PA-C6": """\
Área bruta: 30,50 m²
Traço: 1:2:8
• Tijolo baiano (9x19x19): 801 un (0,80 milheiro) (R$ 961,20)
• Cimento: 1 saco de 50 kg (R$ 36,00)
• Cal: 3 sacos de 20 kg (R$ 54,00)
• Areia: 0,27 m³ (R$ 29,70)

Custo Estimado da Etapa: R$ 1.080,90""",
"PA-C7": """\
Área bruta: 30,50 m²
Traço: 1:2:8
• Tijolo baiano (9x19x19): 801 un (0,80 milheiro) (R$ 961,20)
• Cimento: 1 saco de 50 kg (R$ 36,00)
• Cal: 3 sacos de 20 kg (R$ 54,00)
• Areia: 0,27 m³ (R$ 29,70)

Custo Estimado da Etapa: R$ 1.080,90""",
"PA-C8": """\
Erro: O desconto de vãos deve ser menor que a área.""",
"PA-C9": """\
Erro: O desconto de vãos deve ser menor que a área.""",
"PA-C10": """\
Erro: Desconto, junta e quebra não podem ser negativos.""",
"PA-C11": """\
Erro: Desconto, junta e quebra não podem ser negativos.""",
"PA-C12a": """\
Área bruta: 30,00 m²
Traço: 1:2:8
• Tijolo baiano (9x19x19): 788 un (0,79 milheiro) (R$ 945,60)
• Cimento: 1 saco de 50 kg (R$ 36,00)
• Cal: 3 sacos de 20 kg (R$ 54,00)
• Areia: 0,26 m³ (R$ 28,60)

Custo Estimado da Etapa: R$ 1.064,20""",
"PA-C12b": """\
Área bruta: 30,00 m²
Traço: 1:2:8
• Tijolo baiano (9x19x19): 788 un (0,79 milheiro) (R$ 945,60)
• Cimento: 1 saco de 50 kg (R$ 36,00)
• Cal: 3 sacos de 20 kg (R$ 54,00)
• Areia: 0,26 m³ (R$ 28,60)

Custo Estimado da Etapa: R$ 1.064,20""",
"PA-C13": """\
Área bruta: 30,00 m²
Traço: 1:2:8
• Tijolo baiano (9x19x19): 769 un (0,77 milheiro) (R$ 922,80)
• Cimento: 1 saco de 50 kg (R$ 36,00)
• Cal: 3 sacos de 20 kg (R$ 54,00)
• Areia: 0,26 m³ (R$ 28,60)

Custo Estimado da Etapa: R$ 1.041,40""",
"PA-C14": """\
[JANELA] Junta de 0 cm: o normal é de 0,5 cm a 3 cm.
Área bruta: 30,00 m²
Traço: 1:2:8
• Tijolo baiano (9x19x19): 873 un (0,87 milheiro) (R$ 1.047,60)

Custo Estimado da Etapa: R$ 1.047,60""",
"PA-C15": """\
[JANELA] Junta de 10 cm: o normal é de 0,5 cm a 3 cm.
Área bruta: 30,00 m²
Traço: 1:2:8
• Tijolo baiano (9x19x19): 375 un (0,38 milheiro) (R$ 450,00)
• Cimento: 5 sacos de 50 kg (R$ 180,00)
• Cal: 17 sacos de 20 kg (R$ 306,00)
• Areia: 1,54 m³ (R$ 169,40)

Custo Estimado da Etapa: R$ 1.105,40""",
"PA-C16-cancelar": """\
[JANELA] Área de 100.000 m²: o limite é 2.000 m².
[Cancelar] não calculou""",
"PA-C16-continuar": """\
[JANELA] Área de 100.000 m²: o limite é 2.000 m².
Área bruta: 100.000,00 m²
Traço: 1:2:8
• Tijolo baiano (9x19x19): 2.625.000 un (2.625,00 milheiros) (R$ 3.150.000,00)
• Cimento: 2.633 sacos de 50 kg (R$ 94.788,00)
• Cal: 9.653 sacos de 20 kg (R$ 173.754,00)
• Areia: 877,50 m³ (R$ 96.525,00)

Custo Estimado da Etapa: R$ 3.515.067,00""",
"PA-C17": """\
[JANELA] Quebra de 25%: o limite é 20%.
Área bruta: 30,00 m²
Traço: 1:2:8
• Tijolo baiano (9x19x19): 938 un (0,94 milheiro) (R$ 1.125,60)
• Cimento: 1 saco de 50 kg (R$ 36,00)
• Cal: 3 sacos de 20 kg (R$ 54,00)
• Areia: 0,26 m³ (R$ 28,60)

Custo Estimado da Etapa: R$ 1.244,20""",
"LA-A": """\
Área: 50,00 m²
Tipo de laje: Pré-moldada treliçada
Enchimento: Lajota cerâmica
Capa de concreto: 5 cm
Traço: 1:3:3
Volume Total (com 8% de perda): 3,348 m³
• Laje pré-moldada (vigotas + enchimento): 50,00 m² (R$ 3.250,00)
  (Lajotas cerâmicas: 648 un)
• Tela soldada: 55,00 m² = 10 painéis de 2 x 3 m (R$ 950,00)
• Cimento: 22 sacos de 50 kg (R$ 792,00)
• Areia: 2,15 m³ (R$ 236,50)
• Brita: 2,15 m³ (R$ 258,00)

Custo Estimado da Etapa: R$ 5.486,50""",
"LA-A2": """\
Área: 30,00 m²
Tipo de laje: Maciça
Espessura: 10 cm
Traço: 1,5:5:5
Volume Total (com 7% de perda): 3,210 m³
• Cimento: 19 sacos de 50 kg (R$ 684,00)
• Areia: 2,09 m³ (R$ 229,90)
• Brita: 2,09 m³ (R$ 250,80)

Custo Estimado da Etapa: R$ 1.164,70""",
"LA-B": """\
Área: 50,00 m²
Tipo de laje: Pré-moldada treliçada
Enchimento: Isopor (EPS)
Capa de concreto: 4 cm
Traço: 1:2:3
Volume Total (com 5% de perda): 2,730 m³
• Laje pré-moldada (vigotas + enchimento): 50,00 m² (R$ 3.750,00)
• Cimento: 21 sacos de 50 kg (R$ 756,00)
• Areia: 1,37 m³ (R$ 150,70)
• Brita: 2,05 m³ (R$ 246,00)

Custo Estimado da Etapa: R$ 4.902,70""",
"LA-B2": """\
Área: 30,00 m²
Tipo de laje: Maciça
Espessura: 10 cm
Traço: 1:2:3
Volume Total (com 5% de perda): 3,150 m³
• Cimento: 24 sacos de 50 kg (R$ 864,00)
• Areia: 1,58 m³ (R$ 173,80)
• Brita: 2,36 m³ (R$ 283,20)

Custo Estimado da Etapa: R$ 1.321,00""",
"LA-B3": """\
Área: 50,00 m²
Tipo de laje: Pré-moldada treliçada
Enchimento: Isopor (EPS)
Capa de concreto: 4 cm
Traço: 1:2:3
Volume Total (com 5% de perda): 2,730 m³
• Laje pré-moldada (vigotas + enchimento): 50,00 m² (R$ 3.750,00)
• Tela soldada: 55,00 m² = 10 painéis de 2 x 3 m (R$ 950,00)
• Cimento: 21 sacos de 50 kg (R$ 756,00)
• Areia: 1,37 m³ (R$ 150,70)
• Brita: 2,05 m³ (R$ 246,00)

Custo Estimado da Etapa: R$ 5.852,70""",
"LA-B4": """\
Área: 50,00 m²
Tipo de laje: Pré-moldada treliçada
Enchimento: Lajota cerâmica
Capa de concreto: 4 cm
Traço: 1:2:3
Volume Total (com 5% de perda): 2,730 m³
• Laje pré-moldada (vigotas + enchimento): 50,00 m² (R$ 3.250,00)
  (Lajotas cerâmicas: 630 un)
• Cimento: 21 sacos de 50 kg (R$ 756,00)
• Areia: 1,37 m³ (R$ 150,70)
• Brita: 2,05 m³ (R$ 246,00)

Custo Estimado da Etapa: R$ 4.402,70""",
"LA-C1": """\
Por favor, digite números válidos nos campos!""",
"LA-C2": """\
Por favor, digite números válidos nos campos!""",
"LA-C3": """\
Erro: A área deve ser maior que zero.""",
"LA-C4": """\
Erro: A área deve ser maior que zero.""",
"LA-C5": """\
Área: 50,50 m²
Tipo de laje: Pré-moldada treliçada
Enchimento: Isopor (EPS)
Capa de concreto: 4 cm
Traço: 1:2:3
Volume Total (com 5% de perda): 2,757 m³
• Laje pré-moldada (vigotas + enchimento): 50,50 m² (R$ 3.787,50)
• Cimento: 21 sacos de 50 kg (R$ 756,00)
• Areia: 1,38 m³ (R$ 151,80)
• Brita: 2,07 m³ (R$ 248,40)

Custo Estimado da Etapa: R$ 4.943,70""",
"LA-C6": """\
Área: 50,50 m²
Tipo de laje: Pré-moldada treliçada
Enchimento: Isopor (EPS)
Capa de concreto: 4 cm
Traço: 1:2:3
Volume Total (com 5% de perda): 2,757 m³
• Laje pré-moldada (vigotas + enchimento): 50,50 m² (R$ 3.787,50)
• Cimento: 21 sacos de 50 kg (R$ 756,00)
• Areia: 1,38 m³ (R$ 151,80)
• Brita: 2,07 m³ (R$ 248,40)

Custo Estimado da Etapa: R$ 4.943,70""",
"LA-C7": """\
Área: 50,50 m²
Tipo de laje: Pré-moldada treliçada
Enchimento: Isopor (EPS)
Capa de concreto: 4 cm
Traço: 1:2:3
Volume Total (com 5% de perda): 2,757 m³
• Laje pré-moldada (vigotas + enchimento): 50,50 m² (R$ 3.787,50)
• Cimento: 21 sacos de 50 kg (R$ 756,00)
• Areia: 1,38 m³ (R$ 151,80)
• Brita: 2,07 m³ (R$ 248,40)

Custo Estimado da Etapa: R$ 4.943,70""",
"LA-C8": """\
Erro: A perda não pode ser negativa.""",
"LA-C9": """\
Área: 50,00 m²
Tipo de laje: Pré-moldada treliçada
Enchimento: Isopor (EPS)
Capa de concreto: 4 cm
Traço: 1:2:3
Volume Total (com 2,5% de perda): 2,665 m³
• Laje pré-moldada (vigotas + enchimento): 50,00 m² (R$ 3.750,00)
• Cimento: 20 sacos de 50 kg (R$ 720,00)
• Areia: 1,33 m³ (R$ 146,30)
• Brita: 2,00 m³ (R$ 240,00)

Custo Estimado da Etapa: R$ 4.856,30""",
"LA-C10": """\
Erro: A espessura da capa deve ser maior que zero.""",
"LA-C11": """\
Área: 50,00 m²
Tipo de laje: Pré-moldada treliçada
Enchimento: Isopor (EPS)
Capa de concreto: 4 cm
Traço: 1:2:3
Volume Total (com 5% de perda): 2,730 m³
• Laje pré-moldada (vigotas + enchimento): 50,00 m² (R$ 3.750,00)
• Cimento: 21 sacos de 50 kg (R$ 756,00)
• Areia: 1,37 m³ (R$ 150,70)
• Brita: 2,05 m³ (R$ 246,00)

Custo Estimado da Etapa: R$ 4.902,70""",
"LA-C12": """\
Erro: A espessura da capa deve ser maior que zero.""",
"LA-C13": """\
Por favor, digite números válidos nos campos!""",
"LA-C14": """\
Erro: Informe a espessura total da laje maciça.""",
"LA-C15": """\
Por favor, digite números válidos nos campos!""",
"LA-C16": """\
Por favor, digite números válidos nos campos!""",
"LA-C17": """\
Área: 5,00 m²
Tipo de laje: Pré-moldada treliçada
Enchimento: Isopor (EPS)
Capa de concreto: 4 cm
Traço: 1:2:3
Volume Total (com 5% de perda): 0,273 m³
• Laje pré-moldada (vigotas + enchimento): 5,00 m² (R$ 375,00)
• Tela soldada: 5,50 m² = 1 painel de 2 x 3 m (R$ 95,00)
• Cimento: 3 sacos de 50 kg (R$ 108,00)
• Areia: 0,14 m³ (R$ 15,40)
• Brita: 0,20 m³ (R$ 24,00)

Custo Estimado da Etapa: R$ 617,40""",
"LA-C18": """\
Área: 50,00 m²
Tipo de laje: Pré-moldada treliçada
Enchimento: Isopor (EPS)
Capa de concreto: 4,5 cm
Traço: 1:2:3
Volume Total (com 5% de perda): 2,992 m³
• Laje pré-moldada (vigotas + enchimento): 50,00 m² (R$ 3.750,00)
• Cimento: 23 sacos de 50 kg (R$ 828,00)
• Areia: 1,50 m³ (R$ 165,00)
• Brita: 2,24 m³ (R$ 268,80)

Custo Estimado da Etapa: R$ 5.011,80""",
"LA-C19": """\
[JANELA] Área de 100.000 m²: o limite é 2.000 m².
Área: 100.000,00 m²
Tipo de laje: Pré-moldada treliçada
Enchimento: Isopor (EPS)
Capa de concreto: 4 cm
Traço: 1:2:3
Volume Total (com 5% de perda): 5.460,000 m³
• Laje pré-moldada (vigotas + enchimento): 100.000,00 m² (R$ 7.500.000,00)
• Cimento: 40.950 sacos de 50 kg (R$ 1.474.200,00)
• Areia: 2.730,00 m³ (R$ 300.300,00)
• Brita: 4.095,00 m³ (R$ 491.400,00)

Custo Estimado da Etapa: R$ 9.765.900,00""",
"LA-C20": """\
[JANELA] Capa de 50 cm: o normal é de 3 cm a 8 cm.
Área: 50,00 m²
Tipo de laje: Pré-moldada treliçada
Enchimento: Isopor (EPS)
Capa de concreto: 50 cm
Traço: 1:2:3
Volume Total (com 5% de perda): 26,880 m³
• Laje pré-moldada (vigotas + enchimento): 50,00 m² (R$ 3.750,00)
• Cimento: 202 sacos de 50 kg (R$ 7.272,00)
• Areia: 13,44 m³ (R$ 1.478,40)
• Brita: 20,16 m³ (R$ 2.419,20)

Custo Estimado da Etapa: R$ 14.919,60""",
"LA-C21": """\
[JANELA] Espessura de 200 cm: o normal é de 8 cm a 20 cm.
Área: 50,00 m²
Tipo de laje: Maciça
Espessura: 200 cm
Traço: 1:2:3
Volume Total (com 5% de perda): 105,000 m³
• Cimento: 788 sacos de 50 kg (R$ 28.368,00)
• Areia: 52,50 m³ (R$ 5.775,00)
• Brita: 78,75 m³ (R$ 9.450,00)

Custo Estimado da Etapa: R$ 43.593,00""",
"LA-C22-volta": """\
Área: 50,00 m²
Tipo de laje: Pré-moldada treliçada
Enchimento: Lajota cerâmica
Capa de concreto: 5 cm
Traço: 1:3:3
Volume Total (com 8% de perda): 3,348 m³
• Laje pré-moldada (vigotas + enchimento): 50,00 m² (R$ 3.250,00)
  (Lajotas cerâmicas: 648 un)
• Tela soldada: 55,00 m² = 10 painéis de 2 x 3 m (R$ 950,00)
• Cimento: 22 sacos de 50 kg (R$ 792,00)
• Areia: 2,15 m³ (R$ 236,50)
• Brita: 2,15 m³ (R$ 258,00)

Custo Estimado da Etapa: R$ 5.486,50""",
"TE-A": """\
[TROCA] concreto->35
Área em planta: 80,00 m²
Inclinação: 35%
Área do telhado: 84,76 m²
Tipo de telha: Concreto
• Telhas (com 8% de perda): 962 un (R$ 4.329,00)
• Cumeeira: 10,00 m = 33 peças (R$ 264,00)
• Madeiramento (estimativa):
   - Ripas: 274,6 m (R$ 823,80)
   - Caibros: 183,1 m (R$ 1.647,90)
   - Terças: 54,9 m (R$ 1.372,50)

Custo Estimado da Etapa: R$ 8.437,20""",
"TE-A2": """\
[TROCA] fibrocimento->15
Área em planta: 60,00 m²
Inclinação: 15%
Área do telhado: 60,67 m²
Tipo de telha: Fibrocimento
• Telhas (com 5% de perda): 27 un (R$ 2.025,00)
• Cumeeira: 8,00 m = 9 peças (R$ 405,00)
• Madeiramento (estimativa):
   - Terças: 51,0 m (R$ 1.275,00)

Custo Estimado da Etapa: R$ 3.705,00""",
"TE-B": """\
Área em planta: 80,00 m²
Inclinação: 30%
Área do telhado: 83,52 m²
Tipo de telha: Cerâmica
• Telhas (com 5% de perda): 1.404 un (R$ 3.510,00)

Custo Estimado da Etapa: R$ 3.510,00""",
"TE-B2": """\
Área em planta: 80,00 m²
Inclinação: 30%
Área do telhado: 83,52 m²
Tipo de telha: Cerâmica
• Telhas (com 5% de perda): 1.404 un (R$ 3.510,00)
• Cumeeira: 10,00 m = 32 peças (R$ 128,00)

Custo Estimado da Etapa: R$ 3.638,00""",
"TE-B3": """\
Área em planta: 80,00 m²
Inclinação: 30%
Área do telhado: 83,52 m²
Tipo de telha: Cerâmica
• Telhas (com 5% de perda): 1.404 un (R$ 3.510,00)
• Madeiramento (estimativa):
   - Ripas: 263,1 m (R$ 789,30)
   - Caibros: 175,4 m (R$ 1.578,60)
   - Terças: 52,6 m (R$ 1.315,00)

Custo Estimado da Etapa: R$ 7.192,90""",
"TE-B4": """\
[TROCA] fibrocimento->15
Área em planta: 80,00 m²
Inclinação: 15%
Área do telhado: 80,89 m²
Tipo de telha: Fibrocimento
• Telhas (com 5% de perda): 36 un (R$ 2.700,00)

Custo Estimado da Etapa: R$ 2.700,00""",
"TE-B5": """\
[TROCA] concreto->30
Área em planta: 80,00 m²
Inclinação: 30%
Área do telhado: 83,52 m²
Tipo de telha: Concreto
• Telhas (com 5% de perda): 921 un (R$ 4.144,50)

Custo Estimado da Etapa: R$ 4.144,50""",
"TE-C1": """\
Por favor, digite números válidos nos campos!""",
"TE-C2": """\
Por favor, digite números válidos nos campos!""",
"TE-C3": """\
Erro: A área deve ser maior que zero.""",
"TE-C4": """\
Erro: A área deve ser maior que zero.""",
"TE-C5": """\
Área em planta: 80,50 m²
Inclinação: 30%
Área do telhado: 84,04 m²
Tipo de telha: Cerâmica
• Telhas (com 5% de perda): 1.412 un (R$ 3.530,00)

Custo Estimado da Etapa: R$ 3.530,00""",
"TE-C6": """\
Área em planta: 80,50 m²
Inclinação: 30%
Área do telhado: 84,04 m²
Tipo de telha: Cerâmica
• Telhas (com 5% de perda): 1.412 un (R$ 3.530,00)

Custo Estimado da Etapa: R$ 3.530,00""",
"TE-C7": """\
Área em planta: 80,50 m²
Inclinação: 30%
Área do telhado: 84,04 m²
Tipo de telha: Cerâmica
• Telhas (com 5% de perda): 1.412 un (R$ 3.530,00)

Custo Estimado da Etapa: R$ 3.530,00""",
"TE-C8": """\
Erro: Os valores não podem ser negativos.""",
"TE-C9": """\
Área em planta: 80,00 m²
Inclinação: 30%
Área do telhado: 83,52 m²
Tipo de telha: Cerâmica
• Telhas (com 2,5% de perda): 1.370 un (R$ 3.425,00)

Custo Estimado da Etapa: R$ 3.425,00""",
"TE-C10": """\
Erro: Os valores não podem ser negativos.""",
"TE-C11": """\
Área em planta: 80,00 m²
Inclinação: 30%
Área do telhado: 83,52 m²
Tipo de telha: Cerâmica
• Telhas (com 5% de perda): 1.404 un (R$ 3.510,00)

Custo Estimado da Etapa: R$ 3.510,00""",
"TE-C12": """\
Área em planta: 80,00 m²
Inclinação: 0%
Área do telhado: 80,00 m²
Tipo de telha: Cerâmica
• Telhas (com 5% de perda): 1.344 un (R$ 3.360,00)

Custo Estimado da Etapa: R$ 3.360,00""",
"TE-C13": """\
Área em planta: 80,00 m²
Inclinação: 2,5%
Área do telhado: 80,02 m²
Tipo de telha: Cerâmica
• Telhas (com 5% de perda): 1.345 un (R$ 3.362,50)

Custo Estimado da Etapa: R$ 3.362,50""",
"TE-C14": """\
Erro: Os valores não podem ser negativos.""",
"TE-C15": """\
Área em planta: 80,00 m²
Inclinação: 30%
Área do telhado: 83,52 m²
Tipo de telha: Cerâmica
• Telhas (com 5% de perda): 1.404 un (R$ 3.510,00)

Custo Estimado da Etapa: R$ 3.510,00""",
"TE-C16": """\
Por favor, digite números válidos nos campos!""",
"TE-C17": """\
Por favor, digite números válidos nos campos!""",
"TE-C18": """\
Área em planta: 80,00 m²
Inclinação: 30%
Área do telhado: 83,52 m²
Tipo de telha: Cerâmica
• Telhas (com 5% de perda): 1.404 un (R$ 3.510,00)
• Cumeeira: 0,30 m = 1 peça (R$ 4,00)

Custo Estimado da Etapa: R$ 3.514,00""",
"TE-C19": """\
[JANELA] Área de 100.000 m²: o limite é 2.000 m².
Área em planta: 100.000,00 m²
Inclinação: 30%
Área do telhado: 104.403,07 m²
Tipo de telha: Cerâmica
• Telhas (com 5% de perda): 1.753.972 un (R$ 4.384.930,00)

Custo Estimado da Etapa: R$ 4.384.930,00""",
"TE-C20": """\
[JANELA] Inclinação de 300%: o limite é 100%.
Área em planta: 80,00 m²
Inclinação: 300%
Área do telhado: 252,98 m²
Tipo de telha: Cerâmica
• Telhas (com 5% de perda): 4.251 un (R$ 10.627,50)

Custo Estimado da Etapa: R$ 10.627,50""",
"TE-C21": """\
[TROCA] fibrocimento->15, ceramica->30
Área em planta: 80,00 m²
Inclinação: 30%
Área do telhado: 83,52 m²
Tipo de telha: Cerâmica
• Telhas (com 5% de perda): 1.404 un (R$ 3.510,00)

Custo Estimado da Etapa: R$ 3.510,00""",
"TE-C22": """\
[TROCA] fibrocimento->35
Área em planta: 80,00 m²
Inclinação: 35%
Área do telhado: 84,76 m²
Tipo de telha: Fibrocimento
• Telhas (com 5% de perda): 38 un (R$ 2.850,00)

Custo Estimado da Etapa: R$ 2.850,00""",
"EL-A": """\
Tomadas: 20
Interruptores: 10
Pontos de luz: 12
Chuveiros acima de 5.500 W: 2
Chuveiros até 5.500 W: 1
• Conduíte (do projeto, com 5% de perda): 157,5 m = 4 rolos de 50 m (R$ 300,00)
• Fio 1,5 mm² (do projeto, com 5% de perda): 210,0 m = 3 rolos de 100 m (R$ 450,00)
• Fio 2,5 mm² (do projeto, com 5% de perda): 262,5 m = 3 rolos de 100 m (R$ 690,00)
• Fio 4 mm² (do projeto, com 5% de perda): 42,0 m = 1 rolo de 100 m (R$ 360,00)
• Fio 6 mm² (do projeto, com 5% de perda): 63,0 m = 1 rolo de 100 m (R$ 530,00)
• Caixinhas 4x2: 30 un (R$ 75,00)
• Caixas octogonais (teto): 12 un (R$ 60,00)
• Tomadas: 20 un (R$ 300,00)
• Interruptores: 10 un (R$ 120,00)

Custo Estimado da Etapa: R$ 2.885,00""",
"EL-B": """\
Tomadas: 20
Interruptores: 10
Pontos de luz: 12
• Conduíte (estimado, com 10% de perda): 231,0 m = 5 rolos de 50 m (R$ 375,00)
• Fio 1,5 mm² (estimado, com 10% de perda): 242,0 m = 3 rolos de 100 m (R$ 450,00)
• Fio 2,5 mm² (estimado, com 10% de perda): 330,0 m = 4 rolos de 100 m (R$ 920,00)
• Caixinhas 4x2: 30 un (R$ 75,00)
• Caixas octogonais (teto): 12 un (R$ 60,00)
• Tomadas: 20 un (R$ 300,00)
• Interruptores: 10 un (R$ 120,00)

Custo Estimado da Etapa: R$ 2.300,00""",
"EL-B2": """\
Tomadas: 20
Interruptores: 10
Pontos de luz: 12
Chuveiros acima de 5.500 W: 2
• Conduíte (estimado, com 10% de perda): 253,0 m = 6 rolos de 50 m (R$ 450,00)
• Fio 1,5 mm² (estimado, com 10% de perda): 242,0 m = 3 rolos de 100 m (R$ 450,00)
• Fio 2,5 mm² (estimado, com 10% de perda): 330,0 m = 4 rolos de 100 m (R$ 920,00)
• Fio 6 mm² (estimado, com 10% de perda): 66,0 m = 1 rolo de 100 m (R$ 530,00)
• Caixinhas 4x2: 30 un (R$ 75,00)
• Caixas octogonais (teto): 12 un (R$ 60,00)
• Tomadas: 20 un (R$ 300,00)
• Interruptores: 10 un (R$ 120,00)

Custo Estimado da Etapa: R$ 2.905,00""",
"EL-B3": """\
Tomadas: 20
Interruptores: 10
Pontos de luz: 12
Chuveiros até 5.500 W: 2
• Conduíte (estimado, com 10% de perda): 253,0 m = 6 rolos de 50 m (R$ 450,00)
• Fio 1,5 mm² (estimado, com 10% de perda): 242,0 m = 3 rolos de 100 m (R$ 450,00)
• Fio 2,5 mm² (estimado, com 10% de perda): 330,0 m = 4 rolos de 100 m (R$ 920,00)
• Fio 4 mm² (estimado, com 10% de perda): 66,0 m = 1 rolo de 100 m (R$ 360,00)
• Caixinhas 4x2: 30 un (R$ 75,00)
• Caixas octogonais (teto): 12 un (R$ 60,00)
• Tomadas: 20 un (R$ 300,00)
• Interruptores: 10 un (R$ 120,00)

Custo Estimado da Etapa: R$ 2.735,00""",
"EL-B4": """\
Tomadas: 20
Interruptores: 10
Pontos de luz: 12
Chuveiros acima de 5.500 W: 1
Chuveiros até 5.500 W: 1
• Conduíte (estimado, com 10% de perda): 253,0 m = 6 rolos de 50 m (R$ 450,00)
• Fio 1,5 mm² (estimado, com 10% de perda): 242,0 m = 3 rolos de 100 m (R$ 450,00)
• Fio 2,5 mm² (estimado, com 10% de perda): 330,0 m = 4 rolos de 100 m (R$ 920,00)
• Fio 4 mm² (estimado, com 10% de perda): 33,0 m = 1 rolo de 100 m (R$ 360,00)
• Fio 6 mm² (estimado, com 10% de perda): 33,0 m = 1 rolo de 100 m (R$ 530,00)
• Caixinhas 4x2: 30 un (R$ 75,00)
• Caixas octogonais (teto): 12 un (R$ 60,00)
• Tomadas: 20 un (R$ 300,00)
• Interruptores: 10 un (R$ 120,00)

Custo Estimado da Etapa: R$ 3.265,00""",
"EL-B5": """\
Tomadas: 20
Interruptores: 10
Pontos de luz: 12
• Conduíte (do projeto, com 10% de perda): 165,0 m = 4 rolos de 50 m (R$ 300,00)
• Fio 1,5 mm² (estimado, com 10% de perda): 242,0 m = 3 rolos de 100 m (R$ 450,00)
• Fio 2,5 mm² (estimado, com 10% de perda): 330,0 m = 4 rolos de 100 m (R$ 920,00)
• Caixinhas 4x2: 30 un (R$ 75,00)
• Caixas octogonais (teto): 12 un (R$ 60,00)
• Tomadas: 20 un (R$ 300,00)
• Interruptores: 10 un (R$ 120,00)

Custo Estimado da Etapa: R$ 2.225,00""",
"EL-B6": """\
Tomadas: 20
Interruptores: 10
Pontos de luz: 12
• Conduíte (estimado, com 10% de perda): 231,0 m = 5 rolos de 50 m (R$ 375,00)
• Fio 1,5 mm² (estimado, com 10% de perda): 242,0 m = 3 rolos de 100 m (R$ 450,00)
• Fio 2,5 mm² (do projeto, com 10% de perda): 275,0 m = 3 rolos de 100 m (R$ 690,00)
• Caixinhas 4x2: 30 un (R$ 75,00)
• Caixas octogonais (teto): 12 un (R$ 60,00)
• Tomadas: 20 un (R$ 300,00)
• Interruptores: 10 un (R$ 120,00)

Custo Estimado da Etapa: R$ 2.070,00""",
"EL-B7": """\
Chuveiros acima de 5.500 W: 1
• Conduíte (estimado, com 10% de perda): 11,0 m = 1 rolo de 50 m (R$ 75,00)
• Fio 6 mm² (estimado, com 10% de perda): 33,0 m = 1 rolo de 100 m (R$ 530,00)

Custo Estimado da Etapa: R$ 605,00""",
"EL-B8": """\
Chuveiros até 5.500 W: 1
• Conduíte (estimado, com 10% de perda): 11,0 m = 1 rolo de 50 m (R$ 75,00)
• Fio 4 mm² (estimado, com 10% de perda): 33,0 m = 1 rolo de 100 m (R$ 360,00)

Custo Estimado da Etapa: R$ 435,00""",
"EL-B9": """\
Tomadas: 1
• Conduíte (estimado, com 10% de perda): 5,5 m = 1 rolo de 50 m (R$ 75,00)
• Fio 2,5 mm² (estimado, com 10% de perda): 16,5 m = 1 rolo de 100 m (R$ 230,00)
• Caixinhas 4x2: 1 un (R$ 2,50)
• Tomadas: 1 un (R$ 15,00)

Custo Estimado da Etapa: R$ 322,50""",
"EL-C1": """\
Erro: Informe pelo menos uma tomada, interruptor, ponto de luz ou chuveiro.""",
"EL-C2": """\
Erro: Informe pelo menos uma tomada, interruptor, ponto de luz ou chuveiro.""",
"EL-C3": """\
Por favor, digite números válidos nos campos!""",
"EL-C4": """\
Erro: As quantidades não podem ser negativas.""",
"EL-C5": """\
Por favor, digite números válidos nos campos!""",
"EL-C5b": """\
Erro: As quantidades não podem ser negativas.""",
"EL-C5c": """\
Por favor, digite números válidos nos campos!""",
"EL-C6": """\
Erro: Os valores não podem ser negativos.""",
"EL-C7": """\
Tomadas: 20
Interruptores: 10
Pontos de luz: 12
• Conduíte (estimado, com 2,5% de perda): 215,3 m = 5 rolos de 50 m (R$ 375,00)
• Fio 1,5 mm² (estimado, com 2,5% de perda): 225,5 m = 3 rolos de 100 m (R$ 450,00)
• Fio 2,5 mm² (estimado, com 2,5% de perda): 307,5 m = 4 rolos de 100 m (R$ 920,00)
• Caixinhas 4x2: 30 un (R$ 75,00)
• Caixas octogonais (teto): 12 un (R$ 60,00)
• Tomadas: 20 un (R$ 300,00)
• Interruptores: 10 un (R$ 120,00)

Custo Estimado da Etapa: R$ 2.300,00""",
"EL-C8": """\
Erro: Os valores não podem ser negativos.""",
"EL-C9": """\
Tomadas: 20
Interruptores: 10
Pontos de luz: 12
• Fio 1,5 mm² (estimado, com 10% de perda): 242,0 m = 3 rolos de 100 m (R$ 450,00)
• Fio 2,5 mm² (estimado, com 10% de perda): 330,0 m = 4 rolos de 100 m (R$ 920,00)
• Caixinhas 4x2: 30 un (R$ 75,00)
• Caixas octogonais (teto): 12 un (R$ 60,00)
• Tomadas: 20 un (R$ 300,00)
• Interruptores: 10 un (R$ 120,00)

Custo Estimado da Etapa: R$ 1.925,00""",
"EL-C10": """\
Tomadas: 20
Interruptores: 10
Pontos de luz: 12
• Conduíte (do projeto, com 10% de perda): 165,6 m = 4 rolos de 50 m (R$ 300,00)
• Fio 1,5 mm² (estimado, com 10% de perda): 242,0 m = 3 rolos de 100 m (R$ 450,00)
• Fio 2,5 mm² (estimado, com 10% de perda): 330,0 m = 4 rolos de 100 m (R$ 920,00)
• Caixinhas 4x2: 30 un (R$ 75,00)
• Caixas octogonais (teto): 12 un (R$ 60,00)
• Tomadas: 20 un (R$ 300,00)
• Interruptores: 10 un (R$ 120,00)

Custo Estimado da Etapa: R$ 2.225,00""",
"EL-C11": """\
Tomadas: 20
Interruptores: 10
Pontos de luz: 12
• Conduíte (do projeto, com 10% de perda): 165,6 m = 4 rolos de 50 m (R$ 300,00)
• Fio 1,5 mm² (estimado, com 10% de perda): 242,0 m = 3 rolos de 100 m (R$ 450,00)
• Fio 2,5 mm² (estimado, com 10% de perda): 330,0 m = 4 rolos de 100 m (R$ 920,00)
• Caixinhas 4x2: 30 un (R$ 75,00)
• Caixas octogonais (teto): 12 un (R$ 60,00)
• Tomadas: 20 un (R$ 300,00)
• Interruptores: 10 un (R$ 120,00)

Custo Estimado da Etapa: R$ 2.225,00""",
"EL-C12": """\
Tomadas: 20
Interruptores: 10
Pontos de luz: 12
• Conduíte (do projeto, com 10% de perda): 165,6 m = 4 rolos de 50 m (R$ 300,00)
• Fio 1,5 mm² (estimado, com 10% de perda): 242,0 m = 3 rolos de 100 m (R$ 450,00)
• Fio 2,5 mm² (estimado, com 10% de perda): 330,0 m = 4 rolos de 100 m (R$ 920,00)
• Caixinhas 4x2: 30 un (R$ 75,00)
• Caixas octogonais (teto): 12 un (R$ 60,00)
• Tomadas: 20 un (R$ 300,00)
• Interruptores: 10 un (R$ 120,00)

Custo Estimado da Etapa: R$ 2.225,00""",
"EL-C13": """\
Por favor, digite números válidos nos campos!""",
"EL-C14": """\
Por favor, digite números válidos nos campos!""",
"EL-C15": """\
Tomadas: 20
Interruptores: 10
Pontos de luz: 12
Chuveiros acima de 5.500 W: 2
• Conduíte (estimado, com 10% de perda): 253,0 m = 6 rolos de 50 m (R$ 450,00)
• Fio 1,5 mm² (estimado, com 10% de perda): 242,0 m = 3 rolos de 100 m (R$ 450,00)
• Fio 2,5 mm² (estimado, com 10% de perda): 330,0 m = 4 rolos de 100 m (R$ 920,00)
• Caixinhas 4x2: 30 un (R$ 75,00)
• Caixas octogonais (teto): 12 un (R$ 60,00)
• Tomadas: 20 un (R$ 300,00)
• Interruptores: 10 un (R$ 120,00)

Custo Estimado da Etapa: R$ 2.375,00""",
"EL-C15b": """\
Tomadas: 20
Interruptores: 10
Pontos de luz: 12
Chuveiros até 5.500 W: 2
• Conduíte (estimado, com 10% de perda): 253,0 m = 6 rolos de 50 m (R$ 450,00)
• Fio 1,5 mm² (estimado, com 10% de perda): 242,0 m = 3 rolos de 100 m (R$ 450,00)
• Fio 2,5 mm² (estimado, com 10% de perda): 330,0 m = 4 rolos de 100 m (R$ 920,00)
• Caixinhas 4x2: 30 un (R$ 75,00)
• Caixas octogonais (teto): 12 un (R$ 60,00)
• Tomadas: 20 un (R$ 300,00)
• Interruptores: 10 un (R$ 120,00)

Custo Estimado da Etapa: R$ 2.375,00""",
"EL-C16": """\
[JANELA] 2.000 tomadas: o limite é 300.
Tomadas: 2.000
Interruptores: 10
Pontos de luz: 12
• Conduíte (estimado, com 10% de perda): 11.121,0 m = 223 rolos de 50 m (R$ 16.725,00)
• Fio 1,5 mm² (estimado, com 10% de perda): 242,0 m = 3 rolos de 100 m (R$ 450,00)
• Fio 2,5 mm² (estimado, com 10% de perda): 33.000,0 m = 330 rolos de 100 m (R$ 75.900,00)
• Caixinhas 4x2: 2.010 un (R$ 5.025,00)
• Caixas octogonais (teto): 12 un (R$ 60,00)
• Tomadas: 2.000 un (R$ 30.000,00)
• Interruptores: 10 un (R$ 120,00)

Custo Estimado da Etapa: R$ 128.280,00""",
"EL-C17": """\
[JANELA] 50 chuveiros: o limite é 10 (somando os dois campos).
Tomadas: 20
Interruptores: 10
Pontos de luz: 12
Chuveiros acima de 5.500 W: 50
• Conduíte (estimado, com 10% de perda): 781,0 m = 16 rolos de 50 m (R$ 1.200,00)
• Fio 1,5 mm² (estimado, com 10% de perda): 242,0 m = 3 rolos de 100 m (R$ 450,00)
• Fio 2,5 mm² (estimado, com 10% de perda): 330,0 m = 4 rolos de 100 m (R$ 920,00)
• Fio 6 mm² (estimado, com 10% de perda): 1.650,0 m = 17 rolos de 100 m (R$ 9.010,00)
• Caixinhas 4x2: 30 un (R$ 75,00)
• Caixas octogonais (teto): 12 un (R$ 60,00)
• Tomadas: 20 un (R$ 300,00)
• Interruptores: 10 un (R$ 120,00)

Custo Estimado da Etapa: R$ 12.135,00""",
"HI-A": """\
Pontos de água fria: 10
Pontos de água quente: 3
Pontos de esgoto: 8
• Tubo água fria PVC 25 mm (do projeto, com 5% de perda): 52,5 m = 9 barras de 6 m (R$ 270,00)
• Tubo água quente CPVC 22 mm (do projeto, com 5% de perda): 21,0 m = 7 barras de 3 m (R$ 315,00)
• Tubo esgoto PVC 40 mm (do projeto, com 5% de perda): 31,5 m = 6 barras de 6 m (R$ 210,00)
• Tubo esgoto PVC 100 mm (do projeto, com 5% de perda): 18,9 m = 4 barras de 6 m (R$ 360,00)
• Conexões de água fria (estimativa): 40 un (R$ 120,00)
• Conexões de água quente (estimativa): 12 un (R$ 108,00)
• Conexões de esgoto (estimativa): 24 un (R$ 144,00)
• Registros de gaveta: 4 un (R$ 180,00)

Custo Estimado da Etapa: R$ 1.707,00""",
"HI-B": """\
Pontos de água fria: 10
Pontos de água quente: 3
Pontos de esgoto: 8
• Tubo água fria PVC 25 mm (estimado, com 10% de perda): 44,0 m = 8 barras de 6 m (R$ 240,00)
• Tubo água quente CPVC 22 mm (estimado, com 10% de perda): 16,5 m = 6 barras de 3 m (R$ 270,00)
• Tubo esgoto PVC 40 mm (estimado, com 10% de perda): 26,4 m = 5 barras de 6 m (R$ 175,00)
• Tubo esgoto PVC 100 mm (estimado, com 10% de perda): 17,6 m = 3 barras de 6 m (R$ 270,00)
• Conexões de água fria (estimativa): 40 un (R$ 120,00)
• Conexões de água quente (estimativa): 12 un (R$ 108,00)
• Conexões de esgoto (estimativa): 24 un (R$ 144,00)
• Registros de gaveta: 4 un (R$ 180,00)

Custo Estimado da Etapa: R$ 1.507,00""",
"HI-B2": """\
Pontos de água fria: 1
• Tubo água fria PVC 25 mm (estimado, com 10% de perda): 4,4 m = 1 barra de 6 m (R$ 30,00)
• Conexões de água fria (estimativa): 4 un (R$ 12,00)
• Registros de gaveta: 1 un (R$ 45,00)

Custo Estimado da Etapa: R$ 87,00""",
"HI-B3": """\
Pontos de água fria: 10
Pontos de água quente: 3
Pontos de esgoto: 8
• Tubo água fria PVC 25 mm (do projeto, com 10% de perda): 55,0 m = 10 barras de 6 m (R$ 300,00)
• Tubo água quente CPVC 22 mm (estimado, com 10% de perda): 16,5 m = 6 barras de 3 m (R$ 270,00)
• Tubo esgoto PVC 40 mm (estimado, com 10% de perda): 26,4 m = 5 barras de 6 m (R$ 175,00)
• Tubo esgoto PVC 100 mm (estimado, com 10% de perda): 17,6 m = 3 barras de 6 m (R$ 270,00)
• Conexões de água fria (estimativa): 40 un (R$ 120,00)
• Conexões de água quente (estimativa): 12 un (R$ 108,00)
• Conexões de esgoto (estimativa): 24 un (R$ 144,00)
• Registros de gaveta: 4 un (R$ 180,00)

Custo Estimado da Etapa: R$ 1.567,00""",
"HI-B4": """\
Pontos de esgoto: 8
• Tubo esgoto PVC 40 mm (estimado, com 10% de perda): 26,4 m = 5 barras de 6 m (R$ 175,00)
• Tubo esgoto PVC 100 mm (estimado, com 10% de perda): 17,6 m = 3 barras de 6 m (R$ 270,00)
• Conexões de esgoto (estimativa): 24 un (R$ 144,00)

Custo Estimado da Etapa: R$ 589,00""",
"HI-C1": """\
Erro: Informe pelo menos um ponto de água fria, água quente ou esgoto.""",
"HI-C2": """\
Erro: Informe pelo menos um ponto de água fria, água quente ou esgoto.""",
"HI-C3": """\
Por favor, digite números válidos nos campos!""",
"HI-C4": """\
Erro: As quantidades não podem ser negativas.""",
"HI-C5": """\
Por favor, digite números válidos nos campos!""",
"HI-C6": """\
Erro: Os valores não podem ser negativos.""",
"HI-C7": """\
Pontos de água fria: 10
Pontos de água quente: 3
Pontos de esgoto: 8
• Tubo água fria PVC 25 mm (estimado, com 2,5% de perda): 41,0 m = 7 barras de 6 m (R$ 210,00)
• Tubo água quente CPVC 22 mm (estimado, com 2,5% de perda): 15,4 m = 6 barras de 3 m (R$ 270,00)
• Tubo esgoto PVC 40 mm (estimado, com 2,5% de perda): 24,6 m = 5 barras de 6 m (R$ 175,00)
• Tubo esgoto PVC 100 mm (estimado, com 2,5% de perda): 16,4 m = 3 barras de 6 m (R$ 270,00)
• Conexões de água fria (estimativa): 40 un (R$ 120,00)
• Conexões de água quente (estimativa): 12 un (R$ 108,00)
• Conexões de esgoto (estimativa): 24 un (R$ 144,00)
• Registros de gaveta: 4 un (R$ 180,00)

Custo Estimado da Etapa: R$ 1.477,00""",
"HI-C8": """\
Erro: Os valores não podem ser negativos.""",
"HI-C9": """\
Pontos de água fria: 10
Pontos de água quente: 3
Pontos de esgoto: 8
• Tubo água quente CPVC 22 mm (estimado, com 10% de perda): 16,5 m = 6 barras de 3 m (R$ 270,00)
• Tubo esgoto PVC 40 mm (estimado, com 10% de perda): 26,4 m = 5 barras de 6 m (R$ 175,00)
• Tubo esgoto PVC 100 mm (estimado, com 10% de perda): 17,6 m = 3 barras de 6 m (R$ 270,00)
• Conexões de água fria (estimativa): 40 un (R$ 120,00)
• Conexões de água quente (estimativa): 12 un (R$ 108,00)
• Conexões de esgoto (estimativa): 24 un (R$ 144,00)
• Registros de gaveta: 4 un (R$ 180,00)

Custo Estimado da Etapa: R$ 1.267,00""",
"HI-C10": """\
Pontos de água fria: 10
Pontos de água quente: 3
Pontos de esgoto: 8
• Tubo água fria PVC 25 mm (do projeto, com 10% de perda): 55,6 m = 10 barras de 6 m (R$ 300,00)
• Tubo água quente CPVC 22 mm (estimado, com 10% de perda): 16,5 m = 6 barras de 3 m (R$ 270,00)
• Tubo esgoto PVC 40 mm (estimado, com 10% de perda): 26,4 m = 5 barras de 6 m (R$ 175,00)
• Tubo esgoto PVC 100 mm (estimado, com 10% de perda): 17,6 m = 3 barras de 6 m (R$ 270,00)
• Conexões de água fria (estimativa): 40 un (R$ 120,00)
• Conexões de água quente (estimativa): 12 un (R$ 108,00)
• Conexões de esgoto (estimativa): 24 un (R$ 144,00)
• Registros de gaveta: 4 un (R$ 180,00)

Custo Estimado da Etapa: R$ 1.567,00""",
"HI-C11": """\
Pontos de água fria: 10
Pontos de água quente: 3
Pontos de esgoto: 8
• Tubo água fria PVC 25 mm (do projeto, com 10% de perda): 55,6 m = 10 barras de 6 m (R$ 300,00)
• Tubo água quente CPVC 22 mm (estimado, com 10% de perda): 16,5 m = 6 barras de 3 m (R$ 270,00)
• Tubo esgoto PVC 40 mm (estimado, com 10% de perda): 26,4 m = 5 barras de 6 m (R$ 175,00)
• Tubo esgoto PVC 100 mm (estimado, com 10% de perda): 17,6 m = 3 barras de 6 m (R$ 270,00)
• Conexões de água fria (estimativa): 40 un (R$ 120,00)
• Conexões de água quente (estimativa): 12 un (R$ 108,00)
• Conexões de esgoto (estimativa): 24 un (R$ 144,00)
• Registros de gaveta: 4 un (R$ 180,00)

Custo Estimado da Etapa: R$ 1.567,00""",
"HI-C12": """\
Pontos de água fria: 10
Pontos de água quente: 3
Pontos de esgoto: 8
• Tubo água fria PVC 25 mm (do projeto, com 10% de perda): 55,6 m = 10 barras de 6 m (R$ 300,00)
• Tubo água quente CPVC 22 mm (estimado, com 10% de perda): 16,5 m = 6 barras de 3 m (R$ 270,00)
• Tubo esgoto PVC 40 mm (estimado, com 10% de perda): 26,4 m = 5 barras de 6 m (R$ 175,00)
• Tubo esgoto PVC 100 mm (estimado, com 10% de perda): 17,6 m = 3 barras de 6 m (R$ 270,00)
• Conexões de água fria (estimativa): 40 un (R$ 120,00)
• Conexões de água quente (estimativa): 12 un (R$ 108,00)
• Conexões de esgoto (estimativa): 24 un (R$ 144,00)
• Registros de gaveta: 4 un (R$ 180,00)

Custo Estimado da Etapa: R$ 1.567,00""",
"HI-C13": """\
Por favor, digite números válidos nos campos!""",
"HI-C14": """\
Por favor, digite números válidos nos campos!""",
"HI-C15": """\
[JANELA] 1.000 pontos de água fria: o limite é 200.
Pontos de água fria: 1.000
Pontos de água quente: 3
Pontos de esgoto: 8
• Tubo água fria PVC 25 mm (estimado, com 10% de perda): 4.400,0 m = 734 barras de 6 m (R$ 22.020,00)
• Tubo água quente CPVC 22 mm (estimado, com 10% de perda): 16,5 m = 6 barras de 3 m (R$ 270,00)
• Tubo esgoto PVC 40 mm (estimado, com 10% de perda): 26,4 m = 5 barras de 6 m (R$ 175,00)
• Tubo esgoto PVC 100 mm (estimado, com 10% de perda): 17,6 m = 3 barras de 6 m (R$ 270,00)
• Conexões de água fria (estimativa): 4.000 un (R$ 12.000,00)
• Conexões de água quente (estimativa): 12 un (R$ 108,00)
• Conexões de esgoto (estimativa): 24 un (R$ 144,00)
• Registros de gaveta: 251 un (R$ 11.295,00)

Custo Estimado da Etapa: R$ 46.282,00""",
"CP-A": """\
Área do contrapiso: 40,00 m²
Espessura média: 6 cm
Traço: 1:2:3
Volume Total (com 8% de perda): 2,592 m³
• Cimento: 20 sacos de 50 kg (R$ 720,00)
• Areia: 1,30 m³ (R$ 143,00)
• Brita: 1,94 m³ (R$ 232,80)

Custo Estimado da Etapa: R$ 1.095,80""",
"CP-B": """\
Área do contrapiso: 40,00 m²
Espessura média: 5 cm
Traço: 1:3:3
Volume Total (com 5% de perda): 2,100 m³
• Cimento: 14 sacos de 50 kg (R$ 504,00)
• Areia: 1,35 m³ (R$ 148,50)
• Brita: 1,35 m³ (R$ 162,00)

Custo Estimado da Etapa: R$ 814,50""",
"CP-B2": """\
Área do contrapiso: 40,00 m²
Espessura média: 5 cm
Traço: 1,5:5:5
Volume Total (com 5% de perda): 2,100 m³
• Cimento: 13 sacos de 50 kg (R$ 468,00)
• Areia: 1,37 m³ (R$ 150,70)
• Brita: 1,37 m³ (R$ 164,40)

Custo Estimado da Etapa: R$ 783,10""",
"CP-C1": """\
Por favor, digite números válidos nos campos!""",
"CP-C2": """\
Por favor, digite números válidos nos campos!""",
"CP-C3": """\
Por favor, digite números válidos nos campos!""",
"CP-C4": """\
Erro: Área e espessura devem ser maiores que zero.""",
"CP-C5": """\
Erro: Área e espessura devem ser maiores que zero.""",
"CP-C6": """\
Erro: Área e espessura devem ser maiores que zero.""",
"CP-C7": """\
Erro: Área e espessura devem ser maiores que zero.""",
"CP-C8": """\
Área do contrapiso: 40,50 m²
Espessura média: 5 cm
Traço: 1:3:3
Volume Total (com 5% de perda): 2,126 m³
• Cimento: 14 sacos de 50 kg (R$ 504,00)
• Areia: 1,37 m³ (R$ 150,70)
• Brita: 1,37 m³ (R$ 164,40)

Custo Estimado da Etapa: R$ 819,10""",
"CP-C9": """\
Área do contrapiso: 40,50 m²
Espessura média: 5 cm
Traço: 1:3:3
Volume Total (com 5% de perda): 2,126 m³
• Cimento: 14 sacos de 50 kg (R$ 504,00)
• Areia: 1,37 m³ (R$ 150,70)
• Brita: 1,37 m³ (R$ 164,40)

Custo Estimado da Etapa: R$ 819,10""",
"CP-C10": """\
Área do contrapiso: 40,50 m²
Espessura média: 5 cm
Traço: 1:3:3
Volume Total (com 5% de perda): 2,126 m³
• Cimento: 14 sacos de 50 kg (R$ 504,00)
• Areia: 1,37 m³ (R$ 150,70)
• Brita: 1,37 m³ (R$ 164,40)

Custo Estimado da Etapa: R$ 819,10""",
"CP-C11": """\
Área do contrapiso: 40,00 m²
Espessura média: 5,5 cm
Traço: 1:3:3
Volume Total (com 5% de perda): 2,310 m³
• Cimento: 15 sacos de 50 kg (R$ 540,00)
• Areia: 1,49 m³ (R$ 163,90)
• Brita: 1,49 m³ (R$ 178,80)

Custo Estimado da Etapa: R$ 882,70""",
"CP-C12": """\
Erro: A perda não pode ser negativa.""",
"CP-C13": """\
Área do contrapiso: 40,00 m²
Espessura média: 5 cm
Traço: 1:3:3
Volume Total (com 2,5% de perda): 2,050 m³
• Cimento: 14 sacos de 50 kg (R$ 504,00)
• Areia: 1,32 m³ (R$ 145,20)
• Brita: 1,32 m³ (R$ 158,40)

Custo Estimado da Etapa: R$ 807,60""",
"CP-C14": """\
Área do contrapiso: 40,00 m²
Espessura média: 5 cm
Traço: 1:3:3
Volume Total (com 5% de perda): 2,100 m³
• Cimento: 14 sacos de 50 kg (R$ 504,00)
• Areia: 1,35 m³ (R$ 148,50)
• Brita: 1,35 m³ (R$ 162,00)

Custo Estimado da Etapa: R$ 814,50""",
"CP-C15": """\
Por favor, digite números válidos nos campos!""",
"CP-C16": """\
[JANELA] Área de 100.000 m²: o limite é 2.000 m².
Área do contrapiso: 100.000,00 m²
Espessura média: 5 cm
Traço: 1:3:3
Volume Total (com 5% de perda): 5.250,000 m³
• Cimento: 33.750 sacos de 50 kg (R$ 1.215.000,00)
• Areia: 3.375,00 m³ (R$ 371.250,00)
• Brita: 3.375,00 m³ (R$ 405.000,00)

Custo Estimado da Etapa: R$ 1.991.250,00""",
"CP-C17": """\
[JANELA] Espessura de 50 cm: o normal é de 3 cm a 10 cm.
Área do contrapiso: 40,00 m²
Espessura média: 50 cm
Traço: 1:3:3
Volume Total (com 5% de perda): 21,000 m³
• Cimento: 135 sacos de 50 kg (R$ 4.860,00)
• Areia: 13,50 m³ (R$ 1.485,00)
• Brita: 13,50 m³ (R$ 1.620,00)

Custo Estimado da Etapa: R$ 7.965,00""",
"CP-C18": """\
[JANELA] Espessura de 0,5 cm: o normal é de 3 cm a 10 cm.
Área do contrapiso: 40,00 m²
Espessura média: 0,5 cm
Traço: 1:3:3
Volume Total (com 5% de perda): 0,210 m³
• Cimento: 2 sacos de 50 kg (R$ 72,00)
• Areia: 0,14 m³ (R$ 15,40)
• Brita: 0,14 m³ (R$ 16,80)

Custo Estimado da Etapa: R$ 104,20""",
"RE-A": """\
Área bruta: 30,00 m²
Vãos (portas e janelas): 5,00 m²
Área líquida: 25,00 m²
Área a rebocar (dois lados): 50,00 m²
Espessura: 2,5 cm
Traço: 1:0,5:6
Volume do Reboco (com 12% de perda): 1,400 m³
Chapisco: incluído (1:3, 0,5 cm)
• Cimento: 8 sacos de 50 kg (R$ 288,00)
• Cal: 6 sacos de 20 kg (R$ 108,00)
• Areia: 1,66 m³ (R$ 182,60)

Custo Estimado da Etapa: R$ 578,60""",
"RE-B": """\
Área bruta: 30,00 m²
Espessura: 2 cm
Traço: 1:2:8
Volume do Reboco (com 10% de perda): 0,660 m³
• Cimento: 2 sacos de 50 kg (R$ 72,00)
• Cal: 7 sacos de 20 kg (R$ 126,00)
• Areia: 0,60 m³ (R$ 66,00)

Custo Estimado da Etapa: R$ 264,00""",
"RE-B2": """\
Área bruta: 30,00 m²
Vãos (portas e janelas): 5,00 m²
Área líquida: 25,00 m²
Espessura: 2 cm
Traço: 1:2:8
Volume do Reboco (com 10% de perda): 0,550 m³
• Cimento: 2 sacos de 50 kg (R$ 72,00)
• Cal: 6 sacos de 20 kg (R$ 108,00)
• Areia: 0,50 m³ (R$ 55,00)

Custo Estimado da Etapa: R$ 235,00""",
"RE-B3": """\
Área bruta: 30,00 m²
Área a rebocar (dois lados): 60,00 m²
Espessura: 2 cm
Traço: 1:2:8
Volume do Reboco (com 10% de perda): 1,320 m³
• Cimento: 4 sacos de 50 kg (R$ 144,00)
• Cal: 14 sacos de 20 kg (R$ 252,00)
• Areia: 1,20 m³ (R$ 132,00)

Custo Estimado da Etapa: R$ 528,00""",
"RE-B4": """\
Área bruta: 30,00 m²
Espessura: 2 cm
Traço: 1:2:8
Volume do Reboco (com 10% de perda): 0,660 m³
Chapisco: incluído (1:3, 0,5 cm)
• Cimento: 4 sacos de 50 kg (R$ 144,00)
• Cal: 7 sacos de 20 kg (R$ 126,00)
• Areia: 0,75 m³ (R$ 82,50)

Custo Estimado da Etapa: R$ 352,50""",
"RE-B5": """\
Área bruta: 30,00 m²
Espessura: 2 cm
Traço: 1:0:3
Volume do Reboco (com 10% de perda): 0,660 m³
• Cimento: 5 sacos de 50 kg (R$ 180,00)
• Areia: 0,62 m³ (R$ 68,20)

Custo Estimado da Etapa: R$ 248,20""",
"RE-C1": """\
Por favor, digite números válidos nos campos!""",
"RE-C2": """\
Por favor, digite números válidos nos campos!""",
"RE-C3": """\
Por favor, digite números válidos nos campos!""",
"RE-C4": """\
Erro: Área e espessura devem ser maiores que zero.""",
"RE-C5": """\
Erro: Área e espessura devem ser maiores que zero.""",
"RE-C6": """\
Erro: Área e espessura devem ser maiores que zero.""",
"RE-C7": """\
Área bruta: 30,50 m²
Espessura: 2 cm
Traço: 1:2:8
Volume do Reboco (com 10% de perda): 0,671 m³
• Cimento: 2 sacos de 50 kg (R$ 72,00)
• Cal: 7 sacos de 20 kg (R$ 126,00)
• Areia: 0,61 m³ (R$ 67,10)

Custo Estimado da Etapa: R$ 265,10""",
"RE-C8": """\
Área bruta: 30,50 m²
Espessura: 2 cm
Traço: 1:2:8
Volume do Reboco (com 10% de perda): 0,671 m³
• Cimento: 2 sacos de 50 kg (R$ 72,00)
• Cal: 7 sacos de 20 kg (R$ 126,00)
• Areia: 0,61 m³ (R$ 67,10)

Custo Estimado da Etapa: R$ 265,10""",
"RE-C9": """\
Área bruta: 30,50 m²
Espessura: 2 cm
Traço: 1:2:8
Volume do Reboco (com 10% de perda): 0,671 m³
• Cimento: 2 sacos de 50 kg (R$ 72,00)
• Cal: 7 sacos de 20 kg (R$ 126,00)
• Areia: 0,61 m³ (R$ 67,10)

Custo Estimado da Etapa: R$ 265,10""",
"RE-C10": """\
Erro: Desconto e perda não podem ser negativos.""",
"RE-C11": """\
Erro: O desconto de vãos deve ser menor que a área.""",
"RE-C12": """\
Erro: O desconto de vãos deve ser menor que a área.""",
"RE-C13": """\
Erro: Desconto e perda não podem ser negativos.""",
"RE-C14": """\
Área bruta: 30,00 m²
Espessura: 2 cm
Traço: 1:2:8
Volume do Reboco (com 2,5% de perda): 0,615 m³
• Cimento: 2 sacos de 50 kg (R$ 72,00)
• Cal: 7 sacos de 20 kg (R$ 126,00)
• Areia: 0,56 m³ (R$ 61,60)

Custo Estimado da Etapa: R$ 259,60""",
"RE-C15": """\
Por favor, digite números válidos nos campos!""",
"RE-C16": """\
Por favor, digite números válidos nos campos!""",
"RE-C17": """\
[JANELA] Área de 100.000 m²: o limite é 2.000 m².
Área bruta: 100.000,00 m²
Espessura: 2 cm
Traço: 1:2:8
Volume do Reboco (com 10% de perda): 2.200,000 m³
• Cimento: 6.000 sacos de 50 kg (R$ 216.000,00)
• Cal: 22.000 sacos de 20 kg (R$ 396.000,00)
• Areia: 2.000,00 m³ (R$ 220.000,00)

Custo Estimado da Etapa: R$ 832.000,00""",
"RE-C18": """\
[JANELA] Espessura de 20 cm: o normal é de 0,5 cm a 4 cm.
Área bruta: 30,00 m²
Espessura: 20 cm
Traço: 1:2:8
Volume do Reboco (com 10% de perda): 6,600 m³
• Cimento: 19 sacos de 50 kg (R$ 684,00)
• Cal: 67 sacos de 20 kg (R$ 1.206,00)
• Areia: 6,00 m³ (R$ 660,00)

Custo Estimado da Etapa: R$ 2.550,00""",
"PI-A": """\
Área: 40,00 m²
Área com perda (12%): 44,80 m²
Peça: 60x60 cm
Assentamento: com desenho
• Peças: 125
• Caixas: 21 caixas (2,16 m² por caixa) (R$ 2.240,00)
• Argamassa colante AC-II: 12 sacos de 20 kg (224,0 kg) (R$ 360,00)
• Rodapé: 33,60 m (56 peças de 0,60 m) (R$ 504,00)

Custo Estimado da Etapa: R$ 3.104,00""",
"PI-B": """\
Área: 40,00 m²
Área com perda (10%, automática): 44,00 m²
Peça: 60x60 cm
• Peças: 123 (R$ 2.200,00)
• Argamassa colante AC-I: 11 sacos de 20 kg (220,0 kg) (R$ 242,00)

Custo Estimado da Etapa: R$ 2.442,00""",
"PI-B2": """\
Área: 40,00 m²
Área com perda (15%, automática): 46,00 m²
Peça: 80x80 cm
• Peças: 72 (R$ 2.300,00)
• Argamassa colante AC-I: 19 sacos de 20 kg (368,0 kg) (R$ 418,00)

Custo Estimado da Etapa: R$ 2.718,00""",
"PI-B3": """\
Área: 40,00 m²
Área com perda (20%, automática): 48,00 m²
Peça: 120x60 cm
• Peças: 67 (R$ 2.400,00)
• Argamassa colante AC-I: 20 sacos de 20 kg (384,0 kg) (R$ 440,00)

Custo Estimado da Etapa: R$ 2.840,00""",
"PI-B4": """\
Área: 40,00 m²
Área com perda (25%, automática): 50,00 m²
Peça: 60x60 cm
Assentamento: com desenho
• Peças: 139 (R$ 2.500,00)
• Argamassa colante AC-I: 13 sacos de 20 kg (250,0 kg) (R$ 286,00)

Custo Estimado da Etapa: R$ 2.786,00""",
"PI-B5": """\
Área: 40,00 m²
Área com perda (10%, automática): 44,00 m²
Peça: 60x60 cm
• Peças: 123
• Caixas: 21 caixas (2,16 m² por caixa) (R$ 2.200,00)
• Argamassa colante AC-I: 11 sacos de 20 kg (220,0 kg) (R$ 242,00)

Custo Estimado da Etapa: R$ 2.442,00""",
"PI-B6": """\
Área: 40,00 m²
Área com perda (10%, automática): 44,00 m²
Peça: 60x60 cm
• Peças: 123 (R$ 2.200,00)
• Argamassa colante AC-I: 11 sacos de 20 kg (220,0 kg) (R$ 242,00)
• Rodapé: 33,00 m (R$ 495,00)

Custo Estimado da Etapa: R$ 2.937,00""",
"PI-B7": """\
Área: 40,00 m²
Área com perda (10%, automática): 44,00 m²
Peça: 60x60 cm
• Peças: 123 (R$ 2.200,00)
• Argamassa colante AC-I: 11 sacos de 20 kg (220,0 kg) (R$ 242,00)
• Rodapé: 33,00 m (55 peças de 0,60 m) (R$ 495,00)

Custo Estimado da Etapa: R$ 2.937,00""",
"PI-B8": """\
Área: 40,00 m²
Área com perda (10%, automática): 44,00 m²
Peça: 60x60 cm
• Peças: 123 (R$ 2.200,00)
• Argamassa colante AC-III: 11 sacos de 20 kg (220,0 kg) (R$ 462,00)

Custo Estimado da Etapa: R$ 2.662,00""",
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
Área: 40,50 m²
Área com perda (10%, automática): 44,55 m²
Peça: 60x60 cm
• Peças: 124 (R$ 2.227,50)
• Argamassa colante AC-I: 12 sacos de 20 kg (222,8 kg) (R$ 264,00)

Custo Estimado da Etapa: R$ 2.491,50""",
"PI-C8": """\
Área: 40,50 m²
Área com perda (10%, automática): 44,55 m²
Peça: 60x60 cm
• Peças: 124 (R$ 2.227,50)
• Argamassa colante AC-I: 12 sacos de 20 kg (222,8 kg) (R$ 264,00)

Custo Estimado da Etapa: R$ 2.491,50""",
"PI-C9": """\
Área: 40,50 m²
Área com perda (10%, automática): 44,55 m²
Peça: 60x60 cm
• Peças: 124 (R$ 2.227,50)
• Argamassa colante AC-I: 12 sacos de 20 kg (222,8 kg) (R$ 264,00)

Custo Estimado da Etapa: R$ 2.491,50""",
"PI-C10": """\
Erro: A perda não pode ser negativa.""",
"PI-C11": """\
Área: 40,00 m²
Área com perda (2,5%): 41,00 m²
Peça: 60x60 cm
• Peças: 114 (R$ 2.050,00)
• Argamassa colante AC-I: 11 sacos de 20 kg (205,0 kg) (R$ 242,00)

Custo Estimado da Etapa: R$ 2.292,00""",
"PI-C12": """\
Área: 40,00 m²
Área com perda (0%): 40,00 m²
Peça: 60x60 cm
• Peças: 112 (R$ 2.000,00)
• Argamassa colante AC-I: 10 sacos de 20 kg (200,0 kg) (R$ 220,00)

Custo Estimado da Etapa: R$ 2.220,00""",
"PI-C13": """\
Erro: Os valores não podem ser negativos.""",
"PI-C14": """\
Erro: Os valores não podem ser negativos.""",
"PI-C15": """\
Por favor, digite números válidos nos campos!""",
"PI-C16": """\
Área: 40,00 m²
Área com perda (10%, automática): 44,00 m²
Peça: 70x70 cm
• Peças: 90 (R$ 2.200,00)
• Argamassa colante AC-I: 18 sacos de 20 kg (352,0 kg) (R$ 396,00)

Custo Estimado da Etapa: R$ 2.596,00""",
"PI-C17": """\
Área: 40,00 m²
Área com perda (15%, automática): 46,00 m²
Peça: 90x90 cm
• Peças: 57 (R$ 2.300,00)
• Argamassa colante AC-I: 19 sacos de 20 kg (368,0 kg) (R$ 418,00)

Custo Estimado da Etapa: R$ 2.718,00""",
"PI-C18": """\
Área: 40,00 m²
Área com perda (10%, automática): 44,00 m²
Peça: 60,5x60 cm
• Peças: 122 (R$ 2.200,00)
• Argamassa colante AC-I: 18 sacos de 20 kg (352,0 kg) (R$ 396,00)

Custo Estimado da Etapa: R$ 2.596,00""",
"PI-C19": """\
Área: 40,00 m²
Área com perda (10%, automática): 44,00 m²
Peça: 60x60 cm
• Peças: 123 (R$ 2.200,00)
• Argamassa colante AC-I: 11 sacos de 20 kg (220,0 kg) (R$ 242,00)

Custo Estimado da Etapa: R$ 2.442,00""",
"PI-C20": """\
[JANELA] Área de 100.000 m²: o limite é 2.000 m².
Área: 100.000,00 m²
Área com perda (10%, automática): 110.000,00 m²
Peça: 60x60 cm
• Peças: 305.556 (R$ 5.500.000,00)
• Argamassa colante AC-I: 27.500 sacos de 20 kg (550.000,0 kg) (R$ 605.000,00)

Custo Estimado da Etapa: R$ 6.105.000,00""",
"AZ-A": """\
Área: 30,00 m²
Vãos (portas e janelas): 4,00 m²
Área líquida: 26,00 m²
Área com perda (15%): 29,90 m²
Peça: 30x60 cm
Assentamento: com desenho
• Peças: 167
• Caixas: 17 caixas (1,80 m² por caixa) (R$ 1.196,00)
• Argamassa colante AC-III: 8 sacos de 20 kg (149,5 kg) (R$ 336,00)

Custo Estimado da Etapa: R$ 1.532,00""",
"AZ-B": """\
Área: 30,00 m²
Área com perda (10%, automática): 33,00 m²
Peça: 30x60 cm
• Peças: 184 (R$ 1.320,00)
• Argamassa colante AC-II: 9 sacos de 20 kg (165,0 kg) (R$ 270,00)

Custo Estimado da Etapa: R$ 1.590,00""",
"AZ-B2": """\
Área: 30,00 m²
Vãos (portas e janelas): 4,00 m²
Área líquida: 26,00 m²
Área com perda (10%, automática): 28,60 m²
Peça: 30x60 cm
• Peças: 159 (R$ 1.144,00)
• Argamassa colante AC-II: 8 sacos de 20 kg (143,0 kg) (R$ 240,00)

Custo Estimado da Etapa: R$ 1.384,00""",
"AZ-B3": """\
Área: 30,00 m²
Área com perda (10%, automática): 33,00 m²
Peça: 30x60 cm
• Peças: 184
• Caixas: 19 caixas (1,80 m² por caixa) (R$ 1.320,00)
• Argamassa colante AC-II: 9 sacos de 20 kg (165,0 kg) (R$ 270,00)

Custo Estimado da Etapa: R$ 1.590,00""",
"AZ-B4": """\
Área: 30,00 m²
Área com perda (25%, automática): 37,50 m²
Peça: 30x60 cm
Assentamento: com desenho
• Peças: 209 (R$ 1.500,00)
• Argamassa colante AC-II: 10 sacos de 20 kg (187,5 kg) (R$ 300,00)

Custo Estimado da Etapa: R$ 1.800,00""",
"AZ-B5": """\
Área: 30,00 m²
Área com perda (10%, automática): 33,00 m²
Peça: 30x60 cm
• Peças: 184 (R$ 1.320,00)
• Argamassa colante AC-III: 9 sacos de 20 kg (165,0 kg) (R$ 378,00)

Custo Estimado da Etapa: R$ 1.698,00""",
"AZ-B6": """\
Área: 30,00 m²
Área com perda (15%, automática): 34,50 m²
Peça: 30x90 cm
• Peças: 128 (R$ 1.380,00)
• Argamassa colante AC-II: 14 sacos de 20 kg (276,0 kg) (R$ 420,00)

Custo Estimado da Etapa: R$ 1.800,00""",
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
Área: 30,50 m²
Área com perda (10%, automática): 33,55 m²
Peça: 30x60 cm
• Peças: 187 (R$ 1.342,00)
• Argamassa colante AC-II: 9 sacos de 20 kg (167,8 kg) (R$ 270,00)

Custo Estimado da Etapa: R$ 1.612,00""",
"AZ-C7": """\
Área: 30,50 m²
Área com perda (10%, automática): 33,55 m²
Peça: 30x60 cm
• Peças: 187 (R$ 1.342,00)
• Argamassa colante AC-II: 9 sacos de 20 kg (167,8 kg) (R$ 270,00)

Custo Estimado da Etapa: R$ 1.612,00""",
"AZ-C8": """\
Área: 30,50 m²
Área com perda (10%, automática): 33,55 m²
Peça: 30x60 cm
• Peças: 187 (R$ 1.342,00)
• Argamassa colante AC-II: 9 sacos de 20 kg (167,8 kg) (R$ 270,00)

Custo Estimado da Etapa: R$ 1.612,00""",
"AZ-C9": """\
Erro: Os valores não podem ser negativos.""",
"AZ-C10": """\
Erro: O desconto de vãos deve ser menor que a área.""",
"AZ-C11": """\
Erro: O desconto de vãos deve ser menor que a área.""",
"AZ-C12": """\
Erro: A perda não pode ser negativa.""",
"AZ-C13": """\
Área: 30,00 m²
Área com perda (2,5%): 30,75 m²
Peça: 30x60 cm
• Peças: 171 (R$ 1.230,00)
• Argamassa colante AC-II: 8 sacos de 20 kg (153,8 kg) (R$ 240,00)

Custo Estimado da Etapa: R$ 1.470,00""",
"AZ-C14": """\
Por favor, digite números válidos nos campos!""",
"AZ-C15": """\
Por favor, digite números válidos nos campos!""",
"AZ-C16": """\
[JANELA] Área de 100.000 m²: o limite é 2.000 m².
Área: 100.000,00 m²
Área com perda (10%, automática): 110.000,00 m²
Peça: 30x60 cm
• Peças: 611.112 (R$ 4.400.000,00)
• Argamassa colante AC-II: 27.500 sacos de 20 kg (550.000,0 kg) (R$ 825.000,00)

Custo Estimado da Etapa: R$ 5.225.000,00""",
"RJ-A": """\
Área: 40,00 m²
Peça: 60x60 cm
Junta: 3 mm
Espessura da peça: 10 mm
Consumo: 0,158 kg/m²
• Rejunte (com 15% de perda): 7,3 kg = 4 latas de 2 kg (R$ 72,00)

Custo Estimado da Etapa: R$ 72,00""",
"RJ-B": """\
Área: 40,00 m²
Peça: 60x60 cm
Junta: 3 mm
Espessura da peça: 8 mm
Consumo: 0,126 kg/m²
• Rejunte (com 10% de perda): 5,6 kg = 3 latas de 2 kg (R$ 54,00)

Custo Estimado da Etapa: R$ 54,00""",
"RJ-B2": """\
Área: 40,00 m²
Peça: 30x30 cm
Junta: 5 mm
Espessura da peça: 8 mm
Consumo: 0,421 kg/m²
• Rejunte (com 10% de perda): 18,5 kg = 9 latas de 2 kg e 1 lata de 1 kg (R$ 172,00)

Custo Estimado da Etapa: R$ 172,00""",
"RJ-B3": """\
[BOTÃO] piso: ('40', '60', '60')
[CAMPOS] área 40, peça 60 x 60
Área: 40,00 m²
Peça: 60x60 cm
Junta: 3 mm
Espessura da peça: 8 mm
Consumo: 0,126 kg/m²
• Rejunte (com 10% de perda): 5,6 kg = 3 latas de 2 kg (R$ 54,00)

Custo Estimado da Etapa: R$ 54,00""",
"RJ-B4": """\
[BOTÃO] azulejo: ('26', '30', '60')
[CAMPOS] área 26, peça 30 x 60
Área: 26,00 m²
Peça: 30x60 cm
Junta: 2 mm
Espessura da peça: 8 mm
Consumo: 0,126 kg/m²
• Rejunte (com 10% de perda): 3,6 kg = 2 latas de 2 kg (R$ 36,00)

Custo Estimado da Etapa: R$ 36,00""",
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
Área: 40,50 m²
Peça: 60x60 cm
Junta: 3 mm
Espessura da peça: 8 mm
Consumo: 0,126 kg/m²
• Rejunte (com 10% de perda): 5,6 kg = 3 latas de 2 kg (R$ 54,00)

Custo Estimado da Etapa: R$ 54,00""",
"RJ-C9": """\
Área: 40,50 m²
Peça: 60x60 cm
Junta: 3 mm
Espessura da peça: 8 mm
Consumo: 0,126 kg/m²
• Rejunte (com 10% de perda): 5,6 kg = 3 latas de 2 kg (R$ 54,00)

Custo Estimado da Etapa: R$ 54,00""",
"RJ-C10": """\
Área: 40,50 m²
Peça: 60x60 cm
Junta: 3 mm
Espessura da peça: 8 mm
Consumo: 0,126 kg/m²
• Rejunte (com 10% de perda): 5,6 kg = 3 latas de 2 kg (R$ 54,00)

Custo Estimado da Etapa: R$ 54,00""",
"RJ-C11": """\
Área: 40,00 m²
Peça: 60x60 cm
Junta: 1,5 mm
Espessura da peça: 8 mm
Consumo: 0,063 kg/m²
• Rejunte (com 10% de perda): 2,8 kg = 1 lata de 2 kg e 1 lata de 1 kg (R$ 28,00)

Custo Estimado da Etapa: R$ 28,00""",
"RJ-C12": """\
[JANELA] Junta de 0,5 mm: o normal é de 1 mm a 15 mm.
Área: 40,00 m²
Peça: 60x60 cm
Junta: 0,5 mm
Espessura da peça: 8 mm
Consumo: 0,021 kg/m²
• Rejunte (com 10% de perda): 0,9 kg = 1 lata de 1 kg (R$ 10,00)

Custo Estimado da Etapa: R$ 10,00""",
"RJ-C13": """\
Área: 40,00 m²
Peça: 60x60 cm
Junta: 3 mm
Espessura da peça: 8 mm
Consumo: 0,126 kg/m²
• Rejunte (com 10% de perda): 5,6 kg = 3 latas de 2 kg (R$ 54,00)

Custo Estimado da Etapa: R$ 54,00""",
"RJ-C14": """\
Erro: A espessura da peça deve ser maior que zero.""",
"RJ-C15": """\
Erro: A perda não pode ser negativa.""",
"RJ-C16": """\
Área: 40,00 m²
Peça: 60x60 cm
Junta: 3 mm
Espessura da peça: 8 mm
Consumo: 0,126 kg/m²
• Rejunte (com 2,5% de perda): 5,2 kg = 3 latas de 2 kg (R$ 54,00)

Custo Estimado da Etapa: R$ 54,00""",
"RJ-C17": """\
Por favor, digite números válidos nos campos!""",
"RJ-C18": """\
Área: 1,00 m²
Peça: 60x60 cm
Junta: 3 mm
Espessura da peça: 8 mm
Consumo: 0,126 kg/m²
• Rejunte (com 10% de perda): 0,1 kg = 1 lata de 1 kg (R$ 10,00)

Custo Estimado da Etapa: R$ 10,00""",
"RJ-C19": """\
[JANELA] Área de 100.000 m²: o limite é 2.000 m².
Área: 100.000,00 m²
Peça: 60x60 cm
Junta: 3 mm
Espessura da peça: 8 mm
Consumo: 0,126 kg/m²
• Rejunte (com 10% de perda): 13.904,0 kg = 6.952 latas de 2 kg (R$ 125.136,00)

Custo Estimado da Etapa: R$ 125.136,00""",
"RJ-C20": """\
[JANELA] Junta de 30 mm: o normal é de 1 mm a 15 mm.
Área: 40,00 m²
Peça: 60x60 cm
Junta: 30 mm
Espessura da peça: 8 mm
Consumo: 1,264 kg/m²
• Rejunte (com 10% de perda): 55,6 kg = 28 latas de 2 kg (R$ 504,00)

Custo Estimado da Etapa: R$ 504,00""",
"PT-A": """\
Parede: 100,00 m²
Teto: 40,00 m²
Demãos: 3
Rendimento: 10 m²/L
• Tinta de parede (com 15% de perda): 34,5 L = 2 latas de 18 L (R$ 600,00)
• Tinta de teto (com 15% de perda): 13,8 L = 4 galões de 3,6 L (R$ 300,00)
• Selador (com 15% de perda): 20,1 L = 1 lata de 18 L e 1 galão de 3,6 L (R$ 195,00)
• Fundo preparador (com 15% de perda): 16,1 L = 1 lata de 18 L (R$ 170,00)
• Massa corrida (com 15% de perda): 161,0 kg = 7 baldes de 25 kg (R$ 560,00)
Complementos (sobre parede + teto): Selador 1 demão, Fundo preparador 1 demão, Massa corrida 2 demãos

Custo Estimado da Etapa: R$ 1.825,00""",
"PT-B": """\
Parede: 100,00 m²
Demãos: 2
Rendimento: 12 m²/L
• Tinta de parede (com 10% de perda): 18,3 L = 1 lata de 18 L e 1 galão de 3,6 L (R$ 390,00)

Custo Estimado da Etapa: R$ 390,00""",
"PT-B2": """\
Teto: 40,00 m²
Demãos: 2
Rendimento: 12 m²/L
• Tinta de teto (com 10% de perda): 7,3 L = 3 galões de 3,6 L (R$ 225,00)

Custo Estimado da Etapa: R$ 225,00""",
"PT-B3": """\
Parede: 100,00 m²
Teto: 40,00 m²
Demãos: 2
Rendimento: 12 m²/L
• Tinta de parede (com 10% de perda): 18,3 L = 1 lata de 18 L e 1 galão de 3,6 L (R$ 390,00)
• Tinta de teto (com 10% de perda): 7,3 L = 3 galões de 3,6 L (R$ 225,00)

Custo Estimado da Etapa: R$ 615,00""",
"PT-B4": """\
Parede: 100,00 m²
Demãos: 2
Rendimento: 12 m²/L
• Tinta de parede (com 10% de perda): 18,3 L = 1 lata de 18 L e 1 galão de 3,6 L (R$ 390,00)
• Selador (com 10% de perda): 13,8 L = 4 galões de 3,6 L (R$ 180,00)
Complementos (sobre parede + teto): Selador 1 demão

Custo Estimado da Etapa: R$ 570,00""",
"PT-B5": """\
Parede: 100,00 m²
Demãos: 2
Rendimento: 12 m²/L
• Tinta de parede (com 10% de perda): 18,3 L = 1 lata de 18 L e 1 galão de 3,6 L (R$ 390,00)
• Massa acrílica (com 10% de perda): 110,0 kg = 5 baldes de 25 kg (R$ 650,00)
Complementos (sobre parede + teto): Massa acrílica 2 demãos

Custo Estimado da Etapa: R$ 1.040,00""",
"PT-B6": """\
Parede: 100,00 m²
Demãos: 2
Rendimento: 12 m²/L
• Tinta de parede (com 10% de perda): 18,3 L = 1 lata de 18 L e 1 galão de 3,6 L (R$ 390,00)
• Fundo preparador (com 10% de perda): 11,0 L = 4 galões de 3,6 L (R$ 200,00)
Complementos (sobre parede + teto): Fundo preparador 1 demão

Custo Estimado da Etapa: R$ 590,00""",
"PT-B7": """\
Parede: 180,00 m²
Demãos: 2
Rendimento: 12 m²/L
• Tinta de parede (com 10% de perda): 33,0 L = 2 latas de 18 L (R$ 600,00)

Custo Estimado da Etapa: R$ 600,00""",
"PT-B8": """\
Parede: 10,00 m²
Demãos: 2
Rendimento: 12 m²/L
• Tinta de parede (com 10% de perda): 1,8 L = 1 galão de 3,6 L (R$ 90,00)

Custo Estimado da Etapa: R$ 90,00""",
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
Parede: 100,00 m²
Demãos: 5
Rendimento: 12 m²/L
• Tinta de parede (com 10% de perda): 45,8 L = 2 latas de 18 L e 3 galões de 3,6 L (R$ 870,00)

Custo Estimado da Etapa: R$ 870,00""",
"PT-C10": """\
[JANELA] 6 demãos: o limite é 5 (normalmente são 2 ou 3).
Parede: 100,00 m²
Demãos: 6
Rendimento: 12 m²/L
• Tinta de parede (com 10% de perda): 55,0 L = 3 latas de 18 L e 1 galão de 3,6 L (R$ 990,00)

Custo Estimado da Etapa: R$ 990,00""",
"PT-C11": """\
[JANELA] 22 demãos: o limite é 5 (normalmente são 2 ou 3).
Parede: 100,00 m²
Demãos: 22
Rendimento: 12 m²/L
• Tinta de parede (com 10% de perda): 201,7 L = 11 latas de 18 L e 2 galões de 3,6 L (R$ 3.480,00)

Custo Estimado da Etapa: R$ 3.480,00""",
"PT-C12": """\
Parede: 100,50 m²
Demãos: 2
Rendimento: 12 m²/L
• Tinta de parede (com 10% de perda): 18,4 L = 1 lata de 18 L e 1 galão de 3,6 L (R$ 390,00)

Custo Estimado da Etapa: R$ 390,00""",
"PT-C13": """\
Parede: 100,50 m²
Demãos: 2
Rendimento: 12 m²/L
• Tinta de parede (com 10% de perda): 18,4 L = 1 lata de 18 L e 1 galão de 3,6 L (R$ 390,00)

Custo Estimado da Etapa: R$ 390,00""",
"PT-C14": """\
Parede: 100,50 m²
Demãos: 2
Rendimento: 12 m²/L
• Tinta de parede (com 10% de perda): 18,4 L = 1 lata de 18 L e 1 galão de 3,6 L (R$ 390,00)

Custo Estimado da Etapa: R$ 390,00""",
"PT-C15": """\
Erro: Demãos e rendimento devem ser maiores que zero.""",
"PT-C16": """\
Parede: 100,00 m²
Demãos: 2
Rendimento: 12 m²/L
• Tinta de parede (com 10% de perda): 18,3 L = 1 lata de 18 L e 1 galão de 3,6 L (R$ 390,00)

Custo Estimado da Etapa: R$ 390,00""",
"PT-C17": """\
Parede: 100,00 m²
Demãos: 2
Rendimento: 12,5 m²/L
• Tinta de parede (com 10% de perda): 17,6 L = 1 lata de 18 L (R$ 300,00)

Custo Estimado da Etapa: R$ 300,00""",
"PT-C18": """\
Erro: A perda não pode ser negativa.""",
"PT-C19": """\
Parede: 100,00 m²
Demãos: 2
Rendimento: 12 m²/L
• Tinta de parede (com 2,5% de perda): 17,1 L = 1 lata de 18 L (R$ 300,00)

Custo Estimado da Etapa: R$ 300,00""",
"PT-C20": """\
Por favor, digite números válidos nos campos!""",
"PT-C21": """\
[JANELA] Área de parede de 100.000 m²: o limite é 5.000 m².
Parede: 100.000,00 m²
Demãos: 2
Rendimento: 12 m²/L
• Tinta de parede (com 10% de perda): 18.333,3 L = 1.018 latas de 18 L e 3 galões de 3,6 L (R$ 305.670,00)

Custo Estimado da Etapa: R$ 305.670,00""",
"ES-A": """\
Portas:
• 3x Porta 80 x 210 cm (Madeira): 1,68 m² cada
• 1x Porta 90 x 210 cm (Alumínio): 1,89 m² cada

Janelas:
• 4x Janela 120 x 100 cm (Alumínio): 1,20 m² cada
• 1x Janela 60 x 60 cm (Vidro temperado): 0,36 m² cada

Total: 4 portas e 5 janelas
Área total dos vãos: 12,09 m²

Insumos de fixação:
• Espuma expansiva: 7 tubos de 500 ml (R$ 245,00)
• Parafusos com bucha: 101 un (R$ 80,80)
• Argamassa de fixação: 60,2 kg = 4 sacos de 20 kg (R$ 100,00)

Custo Estimado da Etapa: R$ 425,80
Portas e janelas: use esta lista para pedir orçamento ao fornecedor.""",
"ES-B": """\
Portas:
• 3x Porta 80 x 210 cm: 1,68 m² cada

Janelas:
• 2x Janela 120 x 100 cm: 1,20 m² cada

Total: 3 portas e 2 janelas
Área total dos vãos: 7,44 m²

Portas e janelas: use esta lista para pedir orçamento ao fornecedor.""",
"ES-B2": """\
Portas:
• 3x Porta 80 x 210 cm: 1,68 m² cada

Janelas:
• 2x Janela 120 x 100 cm: 1,20 m² cada

Total: 3 portas e 2 janelas
Área total dos vãos: 7,44 m²

Insumos de fixação:
• Espuma expansiva: 4 tubos de 500 ml (R$ 140,00)

Custo Estimado da Etapa: R$ 140,00
Portas e janelas: use esta lista para pedir orçamento ao fornecedor.""",
"ES-B3": """\
Portas:
• 3x Porta 80 x 210 cm: 1,68 m² cada

Janelas:
• 2x Janela 120 x 100 cm: 1,20 m² cada

Total: 3 portas e 2 janelas
Área total dos vãos: 7,44 m²

Insumos de fixação:
• Parafusos com bucha: 60 un (R$ 48,00)

Custo Estimado da Etapa: R$ 48,00
Portas e janelas: use esta lista para pedir orçamento ao fornecedor.""",
"ES-B4": """\
Portas:
• 3x Porta 80 x 210 cm: 1,68 m² cada

Janelas:
• 2x Janela 120 x 100 cm: 1,20 m² cada

Total: 3 portas e 2 janelas
Área total dos vãos: 7,44 m²

Insumos de fixação:
• Argamassa de fixação: 35,7 kg = 2 sacos de 20 kg (R$ 50,00)

Custo Estimado da Etapa: R$ 50,00
Portas e janelas: use esta lista para pedir orçamento ao fornecedor.""",
"ES-B5": """\
Portas:
• 5x Porta 80 x 210 cm: 1,68 m² cada

Janelas:
• 2x Janela 120 x 100 cm: 1,20 m² cada

Total: 5 portas e 2 janelas
Área total dos vãos: 10,80 m²

Portas e janelas: use esta lista para pedir orçamento ao fornecedor.""",
"ES-B6": """\
[X] lista: ['3x Porta 80 x 210 cm']; resultado antigo sumiu
Portas:
• 3x Porta 80 x 210 cm: 1,68 m² cada

Total: 3 portas
Área total dos vãos: 5,04 m²

Portas e janelas: use esta lista para pedir orçamento ao fornecedor.""",
"ES-C1": """\
Nenhuma porta ou janela na lista ainda.""",
"ES-C2": """\
[Adicionar] Por favor, digite números válidos nos campos!
[Adicionar] nada entrou na lista
Nenhuma porta ou janela na lista ainda.""",
"ES-C3": """\
[Adicionar] Por favor, digite números válidos nos campos!
[Adicionar] nada entrou na lista
Nenhuma porta ou janela na lista ainda.""",
"ES-C4": """\
[Adicionar] Por favor, digite números válidos nos campos!
[Adicionar] nada entrou na lista
Nenhuma porta ou janela na lista ainda.""",
"ES-C5": """\
[Adicionar] Por favor, digite números válidos nos campos!
[Adicionar] nada entrou na lista
Nenhuma porta ou janela na lista ainda.""",
"ES-C6": """\
[Adicionar] Por favor, digite números válidos nos campos!
[Adicionar] nada entrou na lista
Nenhuma porta ou janela na lista ainda.""",
"ES-C7": """\
[Adicionar] Por favor, digite números válidos nos campos!
[Adicionar] nada entrou na lista
Nenhuma porta ou janela na lista ainda.""",
"ES-C8": """\
[Adicionar] Por favor, digite números válidos nos campos!
[Adicionar] nada entrou na lista
Nenhuma porta ou janela na lista ainda.""",
"ES-C9": """\
Você digitou uma porta ou janela, mas não tocou em "Adicionar à lista".""",
"ES-C10a": """\
Janelas:
• 1x Janela 120,5 x 100 cm: 1,21 m² cada

Total: 1 janela
Área total dos vãos: 1,21 m²

Portas e janelas: use esta lista para pedir orçamento ao fornecedor.""",
"ES-C10b": """\
Janelas:
• 1x Janela 120,5 x 100 cm: 1,21 m² cada

Total: 1 janela
Área total dos vãos: 1,21 m²

Portas e janelas: use esta lista para pedir orçamento ao fornecedor.""",
"ES-C10c": """\
Janelas:
• 1x Janela 120,5 x 100 cm: 1,21 m² cada

Total: 1 janela
Área total dos vãos: 1,21 m²

Portas e janelas: use esta lista para pedir orçamento ao fornecedor.""",
"ES-C11": """\
Portas:
• 1x Porta 80 x 210 cm: 1,68 m² cada

Total: 1 porta
Área total dos vãos: 1,68 m²

Insumos de fixação:
• Espuma expansiva: 1 tubo de 500 ml (R$ 35,00)
• Parafusos com bucha: 13 un (R$ 10,40)
• Argamassa de fixação: 7,5 kg = 1 saco de 20 kg (R$ 25,00)

Custo Estimado da Etapa: R$ 70,40
Portas e janelas: use esta lista para pedir orçamento ao fornecedor.""",
"ES-C12": """\
[JANELA no Adicionar] Quantidade de 1.000: o limite é 100 de cada item.
Portas:
• 1.000x Porta 80 x 210 cm: 1,68 m² cada

Total: 1.000 portas
Área total dos vãos: 1.680,00 m²

Insumos de fixação:
• Espuma expansiva: 834 tubos de 500 ml (R$ 29.190,00)
• Parafusos com bucha: 12.500 un (R$ 10.000,00)
• Argamassa de fixação: 7.500,0 kg = 375 sacos de 20 kg (R$ 9.375,00)

Custo Estimado da Etapa: R$ 48.565,00
Portas e janelas: use esta lista para pedir orçamento ao fornecedor.""",
"ES-C13": """\
[JANELA no Adicionar] Largura de 8.000 cm: o limite é 500 cm.
Portas:
• 3x Porta 8.000 x 210 cm: 168,00 m² cada

Total: 3 portas
Área total dos vãos: 504,00 m²

Portas e janelas: use esta lista para pedir orçamento ao fornecedor.""",
}


if __name__ == "__main__":
    main()
