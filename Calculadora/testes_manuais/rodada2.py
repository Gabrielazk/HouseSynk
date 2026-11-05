r"""Rodada 2 (Brasil, inglês): roda os MESMOS casos da rodada 1 (rodada1.py) com o app em inglês,
pelo mesmo caminho da tela (CalculatorScreen._calcular_aba), sem abrir janela: kivy/kivymd são trocados
por módulos falsos. O país continua BR, então números com vírgula e R$ não são erro.
Não grava nada no projeto (rodar com python -B).

O resultado esperado de cada caso fica no fim deste arquivo (ESPERADO), igual ao rodada1.py. O script
compara o texto inteiro que o app mostra com o esperado e diz OK ou DIFERENTE em cada caso; no fim,
mostra quantos deram OK.
Criado em 04/11/2026 a partir do rodada1.py. Durante a rodada, o esperado era lido do testes_rodada2.md.
Mudado em 05/11/2026 (passo 2 do fim da rodada 2): as 17 pendências foram corrigidas, as 14 abas deram
353 OK com o testes_rodada2.md e a Gabi conferiu o visual no app. Só depois disso a saída do app (já
aprovada) virou o ESPERADO completo aqui dentro, com o texto inteiro dos 353 casos (versão principal: a do PC).

Como rodar (no terminal, na pasta C:\Calc\Calculadora):
  env311\Scripts\python.exe -B testes_manuais\rodada2.py           -> todos os casos
  env311\Scripts\python.exe -B testes_manuais\rodada2.py BR-        -> só uma aba (prefixo: BR-, BA-, PA-...)
  env311\Scripts\python.exe -B testes_manuais\rodada2.py BR- --ver  -> mostra também o resultado de cada caso

Quando uma mudança no código é DE PROPÓSITO (ex.: um texto novo), o esperado precisa ser atualizado aqui
e no testes_rodada2.md, sabendo o motivo. Quando é SEM QUERER, o script avisa (DIFERENTE)."""
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
Mix: 1:3:3
Total volume (with 12% waste): 2,309 m³
• Cement: 15 bags of 50 kg (R$ 540,00)
• Sand: 1,48 m³ (R$ 162,80)
• Gravel: 1,48 m³ (R$ 177,60)
Rebar cage: 1,75 m of each pile
• Rebar 10 mm: 57,0 kg (8 bars of 12 m)
• Stirrups 5 mm @ 15 cm: 14,8 kg (9 bars of 12 m)
• Total rebar: 71,8 kg (R$ 682,20)
• Tie wire: 1,4 kg (R$ 21,60)
• Labor cost: 42,0 m (R$ 1.260,00)

Estimated stage cost: R$ 2.844,20""",
"BR-B": """\
Mix: 1:2:3
Total volume (with 10% waste): 1,037 m³
• Cement: 8 bags of 50 kg (R$ 288,00)
• Sand: 0,52 m³ (R$ 57,20)
• Gravel: 0,78 m³ (R$ 93,60)

Estimated stage cost: R$ 438,80""",
"BR-B2": """\
Mix: 1:2:3
Total volume (with 10% waste): 1,037 m³
• Cement: 8 bags of 50 kg (R$ 288,00)
• Sand: 0,52 m³ (R$ 57,20)
• Gravel: 0,78 m³ (R$ 93,60)
Rebar cage: 1,50 m of each pile
• Rebar 8 mm: 26,1 kg (6 bars of 12 m)
• Stirrups 5 mm @ 20 cm: 6,3 kg (4 bars of 12 m)
• Total rebar: 32,4 kg (R$ 307,61)
• Tie wire: 0,7 kg (R$ 9,75)

Estimated stage cost: R$ 756,16""",
"BR-C1": """\
Please enter valid numbers in the fields!""",
"BR-C2": """\
Please enter valid numbers in the fields!""",
"BR-C3": """\
Error: Quantity, depth and diameter must be greater than zero.""",
"BR-C4": """\
Error: Quantity, depth and diameter must be greater than zero.""",
"BR-C5": """\
Please enter valid numbers in the fields!""",
"BR-C6": """\
Mix: 1:2:3
Total volume (with 10% waste): 0,864 m³
• Cement: 7 bags of 50 kg (R$ 252,00)
• Sand: 0,43 m³ (R$ 47,30)
• Gravel: 0,65 m³ (R$ 78,00)

Estimated stage cost: R$ 377,30""",
"BR-C7": """\
Mix: 1:2:3
Total volume (with 10% waste): 0,864 m³
• Cement: 7 bags of 50 kg (R$ 252,00)
• Sand: 0,43 m³ (R$ 47,30)
• Gravel: 0,65 m³ (R$ 78,00)

Estimated stage cost: R$ 377,30""",
"BR-C8": """\
Mix: 1:2:3
Total volume (with 10% waste): 0,864 m³
• Cement: 7 bags of 50 kg (R$ 252,00)
• Sand: 0,43 m³ (R$ 47,30)
• Gravel: 0,65 m³ (R$ 78,00)

Estimated stage cost: R$ 377,30""",
"BR-C9": """\
Error: Waste cannot be negative.""",
"BR-C10": """\
Mix: 1:2:3
Total volume (with 2,5% waste): 0,966 m³
• Cement: 8 bags of 50 kg (R$ 288,00)
• Sand: 0,48 m³ (R$ 52,80)
• Gravel: 0,72 m³ (R$ 86,40)

Estimated stage cost: R$ 427,20""",
"BR-C11": """\
Error: Diameter too small for stirrups.""",
"BR-C12": """\
Error: Bars and stirrup spacing cannot be negative.""",
"BR-C13": """\
Please enter valid numbers in the fields!""",
"BR-C14-cancelar": """\
[JANELA] Depth of 300 m: the limit is 30 m.
[Cancelar] não calculou""",
"BR-C14-continuar": """\
[JANELA] Depth of 300 m: the limit is 30 m.
Mix: 1:2:3
Total volume (with 10% waste): 103,673 m³
• Cement: 778 bags of 50 kg (R$ 28.008,00)
• Sand: 51,84 m³ (R$ 5.702,40)
• Gravel: 77,75 m³ (R$ 9.330,00)

Estimated stage cost: R$ 43.040,40""",
"BR-C15": """\
Mix: 1:2:3
Total volume (with 10% waste): 1,037 m³
• Cement: 8 bags of 50 kg (R$ 288,00)
• Sand: 0,52 m³ (R$ 57,20)
• Gravel: 0,78 m³ (R$ 93,60)
Rebar cage: 1,50 m of each pile
• Rebar 8 mm: 26,1 kg (6 bars of 12 m)
• Total rebar: 26,1 kg (R$ 247,66)
• Tie wire: 0,5 kg (R$ 7,80)

Estimated stage cost: R$ 694,26""",
"BR-C16": """\
Mix: 1:2:3
Total volume (with 10% waste): 1,037 m³
• Cement: 8 bags of 50 kg (R$ 288,00)
• Sand: 0,52 m³ (R$ 57,20)
• Gravel: 0,78 m³ (R$ 93,60)
Rebar cage: 1,50 m of each pile
• Rebar 8 mm: 26,1 kg (6 bars of 12 m)
• Stirrups 5 mm @ 12,5 cm: 9,5 kg (6 bars of 12 m)
• Total rebar: 35,5 kg (R$ 337,54)
• Tie wire: 0,7 kg (R$ 10,65)

Estimated stage cost: R$ 786,99""",
"BR-C17": """\
Mix: 1:2:3
Total volume (with 10% waste): 10,367 m³
• Cement: 78 bags of 50 kg (R$ 2.808,00)
• Sand: 5,18 m³ (R$ 569,80)
• Gravel: 7,78 m³ (R$ 933,60)

Estimated stage cost: R$ 4.311,40""",
"BR-C18": """\
Please enter valid numbers in the fields!""",
"BA-A": """\
Mix: 1:4:3
Total volume (with 8% waste): 2,592 m³
• Cement: 15 bags of 50 kg (R$ 540,00)
• Sand: 1,94 m³ (R$ 213,40)
• Gravel: 1,46 m³ (R$ 175,20)
• Rebar 12,5 mm: 197,0 kg (18 bars of 12 m) (includes 6,00 m of lap splices)
• Stirrups 5 mm @ 15 cm: 34,4 kg (19 bars of 12 m)
• Total rebar: 231,4 kg (R$ 2.198,49)
• Tie wire: 4,6 kg (R$ 69,45)
• Waterproofing: 30,0 m² · 24,0 L = 1 pail of 18 L and 2 cans of 3,6 L (R$ 390,60)
• Labor cost: 30,0 m (R$ 1.200,00)

Estimated stage cost: R$ 4.787,14""",
"BA-B": """\
Mix: 1:2:3
Total volume (with 5% waste): 0,788 m³
• Cement: 6 bags of 50 kg (R$ 216,00)
• Sand: 0,39 m³ (R$ 42,90)
• Gravel: 0,59 m³ (R$ 70,80)

Estimated stage cost: R$ 329,70""",
"BA-B2": """\
Mix: 1:2:3
Total volume (with 5% waste): 0,788 m³
• Cement: 6 bags of 50 kg (R$ 216,00)
• Sand: 0,39 m³ (R$ 42,90)
• Gravel: 0,59 m³ (R$ 70,80)
• Rebar 8 mm: 22,3 kg (5 bars of 12 m) (includes 1,28 m of lap splices)
• Stirrups 5 mm @ 20 cm: 8,6 kg (5 bars of 12 m)
• Total rebar: 30,9 kg (R$ 293,74)
• Tie wire: 0,6 kg (R$ 9,30)

Estimated stage cost: R$ 632,74""",
"BA-B3": """\
Mix: 1:2:3
Total volume (with 5% waste): 0,788 m³
• Cement: 6 bags of 50 kg (R$ 216,00)
• Sand: 0,39 m³ (R$ 42,90)
• Gravel: 0,59 m³ (R$ 70,80)
• Waterproofing: 10,0 m² · 8,0 L = 3 cans of 3,6 L (R$ 167,40)

Estimated stage cost: R$ 497,10""",
"BA-C1": """\
Please enter valid numbers in the fields!""",
"BA-C2": """\
Please enter valid numbers in the fields!""",
"BA-C3": """\
Error: Length, width and height must be greater than zero.""",
"BA-C4": """\
Error: Length, width and height must be greater than zero.""",
"BA-C5": """\
Mix: 1:2:3
Total volume (with 5% waste): 0,788 m³
• Cement: 6 bags of 50 kg (R$ 216,00)
• Sand: 0,39 m³ (R$ 42,90)
• Gravel: 0,59 m³ (R$ 70,80)

Estimated stage cost: R$ 329,70""",
"BA-C6": """\
Mix: 1:2:3
Total volume (with 5% waste): 0,788 m³
• Cement: 6 bags of 50 kg (R$ 216,00)
• Sand: 0,39 m³ (R$ 42,90)
• Gravel: 0,59 m³ (R$ 70,80)

Estimated stage cost: R$ 329,70""",
"BA-C7": """\
Error: Waste cannot be negative.""",
"BA-C8": """\
Mix: 1:2:3
Total volume (with 2,5% waste): 0,769 m³
• Cement: 6 bags of 50 kg (R$ 216,00)
• Sand: 0,38 m³ (R$ 41,80)
• Gravel: 0,58 m³ (R$ 69,60)

Estimated stage cost: R$ 327,40""",
"BA-C9": """\
[JANELA] Beam of 4 cm x 30 cm: the minimum is 20 cm wide and 30 cm high.
Error: Beam too small for stirrups.""",
"BA-C10": """\
Error: Bars and stirrup spacing cannot be negative.""",
"BA-C11": """\
Please enter valid numbers in the fields!""",
"BA-C12": """\
Please enter valid numbers in the fields!""",
"BA-C13": """\
Mix: 1:2:3
Total volume (with 5% waste): 0,788 m³
• Cement: 6 bags of 50 kg (R$ 216,00)
• Sand: 0,39 m³ (R$ 42,90)
• Gravel: 0,59 m³ (R$ 70,80)
• Rebar 8 mm: 22,3 kg (5 bars of 12 m) (includes 1,28 m of lap splices)
• Stirrups 5 mm @ 12,5 cm: 13,9 kg (8 bars of 12 m)
• Total rebar: 36,1 kg (R$ 343,33)
• Tie wire: 0,7 kg (R$ 10,80)

Estimated stage cost: R$ 683,83""",
"BA-C14": """\
Mix: 1:2:3
Total volume (with 5% waste): 0,756 m³
• Cement: 6 bags of 50 kg (R$ 216,00)
• Sand: 0,38 m³ (R$ 41,80)
• Gravel: 0,57 m³ (R$ 68,40)
• Rebar 8 mm: 20,9 kg (5 bars of 12 m)
• Stirrups 5 mm @ 20 cm: 8,4 kg (5 bars of 12 m)
• Total rebar: 29,2 kg (R$ 277,69)
• Tie wire: 0,6 kg (R$ 8,70)

Estimated stage cost: R$ 612,59""",
"BA-C15": """\
Mix: 1:2:3
Total volume (with 5% waste): 1,512 m³
• Cement: 12 bags of 50 kg (R$ 432,00)
• Sand: 0,76 m³ (R$ 83,60)
• Gravel: 1,13 m³ (R$ 135,60)
• Rebar 8 mm: 42,3 kg (9 bars of 12 m) (includes 1,28 m of lap splices)
• Stirrups 5 mm @ 20 cm: 16,6 kg (9 bars of 12 m)
• Total rebar: 58,9 kg (R$ 559,26)
• Tie wire: 1,2 kg (R$ 17,70)

Estimated stage cost: R$ 1.228,16""",
"BA-C16": """\
Mix: 1:2:3
Total volume (with 5% waste): 0,788 m³
• Cement: 6 bags of 50 kg (R$ 216,00)
• Sand: 0,39 m³ (R$ 42,90)
• Gravel: 0,59 m³ (R$ 70,80)
• Rebar 8 mm: 22,3 kg (5 bars of 12 m) (includes 1,28 m of lap splices)
• Total rebar: 22,3 kg (R$ 211,66)
• Tie wire: 0,5 kg (R$ 6,75)

Estimated stage cost: R$ 548,11""",
"BA-C17": """\
Mix: 1:2:3
Total volume (with 5% waste): 315,000 m³
• Cement: 2.363 bags of 50 kg (R$ 85.068,00)
• Sand: 157,50 m³ (R$ 17.325,00)
• Gravel: 236,25 m³ (R$ 28.350,00)

Estimated stage cost: R$ 130.743,00""",
"BA-C18": """\
[JANELA] Beam of 0,2 cm x 0,3 cm: the minimum is 20 cm wide and 30 cm high.
Mix: 1:2:3
Total volume (with 5% waste): 0,000 m³
• Cement: 1 bag of 50 kg (R$ 36,00)

Estimated stage cost: R$ 36,00""",
"BA-C19": """\
[JANELA] Beam of 19 cm x 30 cm: the minimum is 20 cm wide and 30 cm high.
Mix: 1:2:3
Total volume (with 5% waste): 0,748 m³
• Cement: 6 bags of 50 kg (R$ 216,00)
• Sand: 0,37 m³ (R$ 40,70)
• Gravel: 0,56 m³ (R$ 67,20)

Estimated stage cost: R$ 323,90""",
"BA-C20": """\
[JANELA] Beam of 20 cm x 29,5 cm: the minimum is 20 cm wide and 30 cm high.
Mix: 1:2:3
Total volume (with 5% waste): 0,774 m³
• Cement: 6 bags of 50 kg (R$ 216,00)
• Sand: 0,39 m³ (R$ 42,90)
• Gravel: 0,58 m³ (R$ 69,60)

Estimated stage cost: R$ 328,50""",
"BA-C21": """\
Please enter valid numbers in the fields!""",
"BA-C22": """\
Mix: 1:2:3
Total volume (with 5% waste): 0,158 m³
• Cement: 2 bags of 50 kg (R$ 72,00)
• Sand: 0,08 m³ (R$ 8,80)
• Gravel: 0,12 m³ (R$ 14,40)

Estimated stage cost: R$ 95,20""",
"PA-A": """\
Gross area: 80,00 m²
Openings (doors and windows): 12,50 m²
Net area: 67,50 m²
Mix: 1:0,5:6
• Concrete block (14x19x39): 1.162 pcs (R$ 5.229,00)
• Cement: 8 bags of 50 kg (R$ 288,00)
• Lime: 7 bags of 20 kg (R$ 126,00)
• Sand: 1,84 m³ (R$ 202,40)

Estimated stage cost: R$ 5.845,40""",
"PA-B": """\
Gross area: 30,00 m²
Mix: 1:2:8
• Clay brick (9x19x19): 788 pcs (R$ 945,60)
• Cement: 1 bag of 50 kg (R$ 36,00)
• Lime: 3 bags of 20 kg (R$ 54,00)
• Sand: 0,26 m³ (R$ 28,60)

Estimated stage cost: R$ 1.064,20""",
"PA-B2": """\
Gross area: 30,00 m²
Mix: 1:2:8
• Concrete block (19x19x39): 394 pcs (R$ 2.364,00)
• Cement: 2 bags of 50 kg (R$ 72,00)
• Lime: 5 bags of 20 kg (R$ 90,00)
• Sand: 0,42 m³ (R$ 46,20)

Estimated stage cost: R$ 2.572,20""",
"PA-B3": """\
Gross area: 30,00 m²
Mix: 1:2:8
• Clay brick 9 holes (9x14x19): 1.575 pcs (R$ 1.575,00)
• Cement: 2 bags of 50 kg (R$ 72,00)
• Lime: 7 bags of 20 kg (R$ 126,00)
• Sand: 0,61 m³ (R$ 67,10)

Estimated stage cost: R$ 1.840,10""",
"PA-B4": """\
Gross area: 30,00 m²
Mix: 1:0:3
• Clay brick (9x19x19): 788 pcs (R$ 945,60)
• Cement: 3 bags of 50 kg (R$ 108,00)
• Sand: 0,27 m³ (R$ 29,70)

Estimated stage cost: R$ 1.083,30""",
"PA-C1": """\
Please enter valid numbers in the fields!""",
"PA-C2": """\
Please enter valid numbers in the fields!""",
"PA-C3": """\
Error: The wall area must be greater than zero.""",
"PA-C4": """\
Error: The wall area must be greater than zero.""",
"PA-C5": """\
Gross area: 30,50 m²
Mix: 1:2:8
• Clay brick (9x19x19): 801 pcs (R$ 961,20)
• Cement: 1 bag of 50 kg (R$ 36,00)
• Lime: 3 bags of 20 kg (R$ 54,00)
• Sand: 0,27 m³ (R$ 29,70)

Estimated stage cost: R$ 1.080,90""",
"PA-C6": """\
Gross area: 30,50 m²
Mix: 1:2:8
• Clay brick (9x19x19): 801 pcs (R$ 961,20)
• Cement: 1 bag of 50 kg (R$ 36,00)
• Lime: 3 bags of 20 kg (R$ 54,00)
• Sand: 0,27 m³ (R$ 29,70)

Estimated stage cost: R$ 1.080,90""",
"PA-C7": """\
Gross area: 30,50 m²
Mix: 1:2:8
• Clay brick (9x19x19): 801 pcs (R$ 961,20)
• Cement: 1 bag of 50 kg (R$ 36,00)
• Lime: 3 bags of 20 kg (R$ 54,00)
• Sand: 0,27 m³ (R$ 29,70)

Estimated stage cost: R$ 1.080,90""",
"PA-C8": """\
Error: The openings deduction must be smaller than the area.""",
"PA-C9": """\
Error: The openings deduction must be smaller than the area.""",
"PA-C10": """\
Error: Deduction, joint and breakage cannot be negative.""",
"PA-C11": """\
Error: Deduction, joint and breakage cannot be negative.""",
"PA-C12a": """\
Gross area: 30,00 m²
Mix: 1:2:8
• Clay brick (9x19x19): 788 pcs (R$ 945,60)
• Cement: 1 bag of 50 kg (R$ 36,00)
• Lime: 3 bags of 20 kg (R$ 54,00)
• Sand: 0,26 m³ (R$ 28,60)

Estimated stage cost: R$ 1.064,20""",
"PA-C12b": """\
Gross area: 30,00 m²
Mix: 1:2:8
• Clay brick (9x19x19): 788 pcs (R$ 945,60)
• Cement: 1 bag of 50 kg (R$ 36,00)
• Lime: 3 bags of 20 kg (R$ 54,00)
• Sand: 0,26 m³ (R$ 28,60)

Estimated stage cost: R$ 1.064,20""",
"PA-C13": """\
Gross area: 30,00 m²
Mix: 1:2:8
• Clay brick (9x19x19): 769 pcs (R$ 922,80)
• Cement: 1 bag of 50 kg (R$ 36,00)
• Lime: 3 bags of 20 kg (R$ 54,00)
• Sand: 0,26 m³ (R$ 28,60)

Estimated stage cost: R$ 1.041,40""",
"PA-C14": """\
[JANELA] Joint of 0 cm: the usual is 0,5 cm to 3 cm.
Gross area: 30,00 m²
Mix: 1:2:8
• Clay brick (9x19x19): 873 pcs (R$ 1.047,60)

Estimated stage cost: R$ 1.047,60""",
"PA-C15": """\
[JANELA] Joint of 10 cm: the usual is 0,5 cm to 3 cm.
Gross area: 30,00 m²
Mix: 1:2:8
• Clay brick (9x19x19): 375 pcs (R$ 450,00)
• Cement: 5 bags of 50 kg (R$ 180,00)
• Lime: 17 bags of 20 kg (R$ 306,00)
• Sand: 1,54 m³ (R$ 169,40)

Estimated stage cost: R$ 1.105,40""",
"PA-C16-cancelar": """\
[JANELA] Area of 100.000 m²: the limit is 2.000 m².
[Cancelar] não calculou""",
"PA-C16-continuar": """\
[JANELA] Area of 100.000 m²: the limit is 2.000 m².
Gross area: 100.000,00 m²
Mix: 1:2:8
• Clay brick (9x19x19): 2.625.000 pcs (R$ 3.150.000,00)
• Cement: 2.633 bags of 50 kg (R$ 94.788,00)
• Lime: 9.653 bags of 20 kg (R$ 173.754,00)
• Sand: 877,50 m³ (R$ 96.525,00)

Estimated stage cost: R$ 3.515.067,00""",
"PA-C17": """\
[JANELA] Breakage of 25%: the limit is 20%.
Gross area: 30,00 m²
Mix: 1:2:8
• Clay brick (9x19x19): 938 pcs (R$ 1.125,60)
• Cement: 1 bag of 50 kg (R$ 36,00)
• Lime: 3 bags of 20 kg (R$ 54,00)
• Sand: 0,26 m³ (R$ 28,60)

Estimated stage cost: R$ 1.244,20""",
"LA-A": """\
Area: 50,00 m²
Slab type: Precast (lattice joists)
Filler: Ceramic block
Concrete topping: 5 cm
Mix: 1:3:3
Total volume (with 8% waste): 3,348 m³
• Precast slab (joists + filler): 50,00 m² (R$ 3.250,00)
  (Ceramic blocks: 648 pcs)
• Welded wire mesh: 55,00 m² = 10 panels of 2 x 3 m (R$ 950,00)
• Cement: 22 bags of 50 kg (R$ 792,00)
• Sand: 2,15 m³ (R$ 236,50)
• Gravel: 2,15 m³ (R$ 258,00)

Estimated stage cost: R$ 5.486,50""",
"LA-A2": """\
Area: 30,00 m²
Slab type: Solid slab
Thickness: 10 cm
Mix: 1,5:5:5
Total volume (with 7% waste): 3,210 m³
• Cement: 19 bags of 50 kg (R$ 684,00)
• Sand: 2,09 m³ (R$ 229,90)
• Gravel: 2,09 m³ (R$ 250,80)

Estimated stage cost: R$ 1.164,70""",
"LA-B": """\
Area: 50,00 m²
Slab type: Precast (lattice joists)
Filler: EPS foam
Concrete topping: 4 cm
Mix: 1:2:3
Total volume (with 5% waste): 2,730 m³
• Precast slab (joists + filler): 50,00 m² (R$ 3.750,00)
• Cement: 21 bags of 50 kg (R$ 756,00)
• Sand: 1,37 m³ (R$ 150,70)
• Gravel: 2,05 m³ (R$ 246,00)

Estimated stage cost: R$ 4.902,70""",
"LA-B2": """\
Area: 30,00 m²
Slab type: Solid slab
Thickness: 10 cm
Mix: 1:2:3
Total volume (with 5% waste): 3,150 m³
• Cement: 24 bags of 50 kg (R$ 864,00)
• Sand: 1,58 m³ (R$ 173,80)
• Gravel: 2,36 m³ (R$ 283,20)

Estimated stage cost: R$ 1.321,00""",
"LA-B3": """\
Area: 50,00 m²
Slab type: Precast (lattice joists)
Filler: EPS foam
Concrete topping: 4 cm
Mix: 1:2:3
Total volume (with 5% waste): 2,730 m³
• Precast slab (joists + filler): 50,00 m² (R$ 3.750,00)
• Welded wire mesh: 55,00 m² = 10 panels of 2 x 3 m (R$ 950,00)
• Cement: 21 bags of 50 kg (R$ 756,00)
• Sand: 1,37 m³ (R$ 150,70)
• Gravel: 2,05 m³ (R$ 246,00)

Estimated stage cost: R$ 5.852,70""",
"LA-B4": """\
Area: 50,00 m²
Slab type: Precast (lattice joists)
Filler: Ceramic block
Concrete topping: 4 cm
Mix: 1:2:3
Total volume (with 5% waste): 2,730 m³
• Precast slab (joists + filler): 50,00 m² (R$ 3.250,00)
  (Ceramic blocks: 630 pcs)
• Cement: 21 bags of 50 kg (R$ 756,00)
• Sand: 1,37 m³ (R$ 150,70)
• Gravel: 2,05 m³ (R$ 246,00)

Estimated stage cost: R$ 4.402,70""",
"LA-C1": """\
Please enter valid numbers in the fields!""",
"LA-C2": """\
Please enter valid numbers in the fields!""",
"LA-C3": """\
Error: The area must be greater than zero.""",
"LA-C4": """\
Error: The area must be greater than zero.""",
"LA-C5": """\
Area: 50,50 m²
Slab type: Precast (lattice joists)
Filler: EPS foam
Concrete topping: 4 cm
Mix: 1:2:3
Total volume (with 5% waste): 2,757 m³
• Precast slab (joists + filler): 50,50 m² (R$ 3.787,50)
• Cement: 21 bags of 50 kg (R$ 756,00)
• Sand: 1,38 m³ (R$ 151,80)
• Gravel: 2,07 m³ (R$ 248,40)

Estimated stage cost: R$ 4.943,70""",
"LA-C6": """\
Area: 50,50 m²
Slab type: Precast (lattice joists)
Filler: EPS foam
Concrete topping: 4 cm
Mix: 1:2:3
Total volume (with 5% waste): 2,757 m³
• Precast slab (joists + filler): 50,50 m² (R$ 3.787,50)
• Cement: 21 bags of 50 kg (R$ 756,00)
• Sand: 1,38 m³ (R$ 151,80)
• Gravel: 2,07 m³ (R$ 248,40)

Estimated stage cost: R$ 4.943,70""",
"LA-C7": """\
Area: 50,50 m²
Slab type: Precast (lattice joists)
Filler: EPS foam
Concrete topping: 4 cm
Mix: 1:2:3
Total volume (with 5% waste): 2,757 m³
• Precast slab (joists + filler): 50,50 m² (R$ 3.787,50)
• Cement: 21 bags of 50 kg (R$ 756,00)
• Sand: 1,38 m³ (R$ 151,80)
• Gravel: 2,07 m³ (R$ 248,40)

Estimated stage cost: R$ 4.943,70""",
"LA-C8": """\
Error: Waste cannot be negative.""",
"LA-C9": """\
Area: 50,00 m²
Slab type: Precast (lattice joists)
Filler: EPS foam
Concrete topping: 4 cm
Mix: 1:2:3
Total volume (with 2,5% waste): 2,665 m³
• Precast slab (joists + filler): 50,00 m² (R$ 3.750,00)
• Cement: 20 bags of 50 kg (R$ 720,00)
• Sand: 1,33 m³ (R$ 146,30)
• Gravel: 2,00 m³ (R$ 240,00)

Estimated stage cost: R$ 4.856,30""",
"LA-C10": """\
Error: The topping thickness must be greater than zero.""",
"LA-C11": """\
Area: 50,00 m²
Slab type: Precast (lattice joists)
Filler: EPS foam
Concrete topping: 4 cm
Mix: 1:2:3
Total volume (with 5% waste): 2,730 m³
• Precast slab (joists + filler): 50,00 m² (R$ 3.750,00)
• Cement: 21 bags of 50 kg (R$ 756,00)
• Sand: 1,37 m³ (R$ 150,70)
• Gravel: 2,05 m³ (R$ 246,00)

Estimated stage cost: R$ 4.902,70""",
"LA-C12": """\
Error: The topping thickness must be greater than zero.""",
"LA-C13": """\
Please enter valid numbers in the fields!""",
"LA-C14": """\
Error: Enter the total thickness of the solid slab.""",
"LA-C15": """\
Please enter valid numbers in the fields!""",
"LA-C16": """\
Please enter valid numbers in the fields!""",
"LA-C17": """\
Area: 5,00 m²
Slab type: Precast (lattice joists)
Filler: EPS foam
Concrete topping: 4 cm
Mix: 1:2:3
Total volume (with 5% waste): 0,273 m³
• Precast slab (joists + filler): 5,00 m² (R$ 375,00)
• Welded wire mesh: 5,50 m² = 1 panel of 2 x 3 m (R$ 95,00)
• Cement: 3 bags of 50 kg (R$ 108,00)
• Sand: 0,14 m³ (R$ 15,40)
• Gravel: 0,20 m³ (R$ 24,00)

Estimated stage cost: R$ 617,40""",
"LA-C18": """\
Area: 50,00 m²
Slab type: Precast (lattice joists)
Filler: EPS foam
Concrete topping: 4,5 cm
Mix: 1:2:3
Total volume (with 5% waste): 2,992 m³
• Precast slab (joists + filler): 50,00 m² (R$ 3.750,00)
• Cement: 23 bags of 50 kg (R$ 828,00)
• Sand: 1,50 m³ (R$ 165,00)
• Gravel: 2,24 m³ (R$ 268,80)

Estimated stage cost: R$ 5.011,80""",
"LA-C19": """\
[JANELA] Area of 100.000 m²: the limit is 2.000 m².
Area: 100.000,00 m²
Slab type: Precast (lattice joists)
Filler: EPS foam
Concrete topping: 4 cm
Mix: 1:2:3
Total volume (with 5% waste): 5.460,000 m³
• Precast slab (joists + filler): 100.000,00 m² (R$ 7.500.000,00)
• Cement: 40.950 bags of 50 kg (R$ 1.474.200,00)
• Sand: 2.730,00 m³ (R$ 300.300,00)
• Gravel: 4.095,00 m³ (R$ 491.400,00)

Estimated stage cost: R$ 9.765.900,00""",
"LA-C20": """\
[JANELA] Topping of 50 cm: the usual is 3 cm to 8 cm.
Area: 50,00 m²
Slab type: Precast (lattice joists)
Filler: EPS foam
Concrete topping: 50 cm
Mix: 1:2:3
Total volume (with 5% waste): 26,880 m³
• Precast slab (joists + filler): 50,00 m² (R$ 3.750,00)
• Cement: 202 bags of 50 kg (R$ 7.272,00)
• Sand: 13,44 m³ (R$ 1.478,40)
• Gravel: 20,16 m³ (R$ 2.419,20)

Estimated stage cost: R$ 14.919,60""",
"LA-C21": """\
[JANELA] Thickness of 200 cm: the usual is 8 cm to 20 cm.
Area: 50,00 m²
Slab type: Solid slab
Thickness: 200 cm
Mix: 1:2:3
Total volume (with 5% waste): 105,000 m³
• Cement: 788 bags of 50 kg (R$ 28.368,00)
• Sand: 52,50 m³ (R$ 5.775,00)
• Gravel: 78,75 m³ (R$ 9.450,00)

Estimated stage cost: R$ 43.593,00""",
"LA-C22-volta": """\
Area: 50,00 m²
Slab type: Precast (lattice joists)
Filler: Ceramic block
Concrete topping: 5 cm
Mix: 1:3:3
Total volume (with 8% waste): 3,348 m³
• Precast slab (joists + filler): 50,00 m² (R$ 3.250,00)
  (Ceramic blocks: 648 pcs)
• Welded wire mesh: 55,00 m² = 10 panels of 2 x 3 m (R$ 950,00)
• Cement: 22 bags of 50 kg (R$ 792,00)
• Sand: 2,15 m³ (R$ 236,50)
• Gravel: 2,15 m³ (R$ 258,00)

Estimated stage cost: R$ 5.486,50""",
"TE-A": """\
[TROCA] concreto->35
Plan area: 80,00 m²
Slope: 35%
Roof area: 84,76 m²
Roof tile type: Concrete
• Roof tiles (with 8% waste): 962 pcs (R$ 4.329,00)
• Ridge: 10,00 m = 33 pcs (R$ 264,00)
• Timber framing (estimate):
   - Battens: 274,6 m (R$ 823,80)
   - Rafters: 183,1 m (R$ 1.647,90)
   - Purlins: 54,9 m (R$ 1.372,50)

Estimated stage cost: R$ 8.437,20""",
"TE-A2": """\
[TROCA] fibrocimento->15
Plan area: 60,00 m²
Slope: 15%
Roof area: 60,67 m²
Roof tile type: Fiber cement
• Roof tiles (with 5% waste): 27 pcs (R$ 2.025,00)
• Ridge: 8,00 m = 9 pcs (R$ 405,00)
• Timber framing (estimate):
   - Purlins: 51,0 m (R$ 1.275,00)

Estimated stage cost: R$ 3.705,00""",
"TE-B": """\
Plan area: 80,00 m²
Slope: 30%
Roof area: 83,52 m²
Roof tile type: Clay
• Roof tiles (with 5% waste): 1.404 pcs (R$ 3.510,00)

Estimated stage cost: R$ 3.510,00""",
"TE-B2": """\
Plan area: 80,00 m²
Slope: 30%
Roof area: 83,52 m²
Roof tile type: Clay
• Roof tiles (with 5% waste): 1.404 pcs (R$ 3.510,00)
• Ridge: 10,00 m = 32 pcs (R$ 128,00)

Estimated stage cost: R$ 3.638,00""",
"TE-B3": """\
Plan area: 80,00 m²
Slope: 30%
Roof area: 83,52 m²
Roof tile type: Clay
• Roof tiles (with 5% waste): 1.404 pcs (R$ 3.510,00)
• Timber framing (estimate):
   - Battens: 263,1 m (R$ 789,30)
   - Rafters: 175,4 m (R$ 1.578,60)
   - Purlins: 52,6 m (R$ 1.315,00)

Estimated stage cost: R$ 7.192,90""",
"TE-B4": """\
[TROCA] fibrocimento->15
Plan area: 80,00 m²
Slope: 15%
Roof area: 80,89 m²
Roof tile type: Fiber cement
• Roof tiles (with 5% waste): 36 pcs (R$ 2.700,00)

Estimated stage cost: R$ 2.700,00""",
"TE-B5": """\
[TROCA] concreto->30
Plan area: 80,00 m²
Slope: 30%
Roof area: 83,52 m²
Roof tile type: Concrete
• Roof tiles (with 5% waste): 921 pcs (R$ 4.144,50)

Estimated stage cost: R$ 4.144,50""",
"TE-C1": """\
Please enter valid numbers in the fields!""",
"TE-C2": """\
Please enter valid numbers in the fields!""",
"TE-C3": """\
Error: The area must be greater than zero.""",
"TE-C4": """\
Error: The area must be greater than zero.""",
"TE-C5": """\
Plan area: 80,50 m²
Slope: 30%
Roof area: 84,04 m²
Roof tile type: Clay
• Roof tiles (with 5% waste): 1.412 pcs (R$ 3.530,00)

Estimated stage cost: R$ 3.530,00""",
"TE-C6": """\
Plan area: 80,50 m²
Slope: 30%
Roof area: 84,04 m²
Roof tile type: Clay
• Roof tiles (with 5% waste): 1.412 pcs (R$ 3.530,00)

Estimated stage cost: R$ 3.530,00""",
"TE-C7": """\
Plan area: 80,50 m²
Slope: 30%
Roof area: 84,04 m²
Roof tile type: Clay
• Roof tiles (with 5% waste): 1.412 pcs (R$ 3.530,00)

Estimated stage cost: R$ 3.530,00""",
"TE-C8": """\
Error: Values cannot be negative.""",
"TE-C9": """\
Plan area: 80,00 m²
Slope: 30%
Roof area: 83,52 m²
Roof tile type: Clay
• Roof tiles (with 2,5% waste): 1.370 pcs (R$ 3.425,00)

Estimated stage cost: R$ 3.425,00""",
"TE-C10": """\
Error: Values cannot be negative.""",
"TE-C11": """\
Plan area: 80,00 m²
Slope: 30%
Roof area: 83,52 m²
Roof tile type: Clay
• Roof tiles (with 5% waste): 1.404 pcs (R$ 3.510,00)

Estimated stage cost: R$ 3.510,00""",
"TE-C12": """\
Plan area: 80,00 m²
Slope: 0%
Roof area: 80,00 m²
Roof tile type: Clay
• Roof tiles (with 5% waste): 1.344 pcs (R$ 3.360,00)

Estimated stage cost: R$ 3.360,00""",
"TE-C13": """\
Plan area: 80,00 m²
Slope: 2,5%
Roof area: 80,02 m²
Roof tile type: Clay
• Roof tiles (with 5% waste): 1.345 pcs (R$ 3.362,50)

Estimated stage cost: R$ 3.362,50""",
"TE-C14": """\
Error: Values cannot be negative.""",
"TE-C15": """\
Plan area: 80,00 m²
Slope: 30%
Roof area: 83,52 m²
Roof tile type: Clay
• Roof tiles (with 5% waste): 1.404 pcs (R$ 3.510,00)

Estimated stage cost: R$ 3.510,00""",
"TE-C16": """\
Please enter valid numbers in the fields!""",
"TE-C17": """\
Please enter valid numbers in the fields!""",
"TE-C18": """\
Plan area: 80,00 m²
Slope: 30%
Roof area: 83,52 m²
Roof tile type: Clay
• Roof tiles (with 5% waste): 1.404 pcs (R$ 3.510,00)
• Ridge: 0,30 m = 1 pc (R$ 4,00)

Estimated stage cost: R$ 3.514,00""",
"TE-C19": """\
[JANELA] Area of 100.000 m²: the limit is 2.000 m².
Plan area: 100.000,00 m²
Slope: 30%
Roof area: 104.403,07 m²
Roof tile type: Clay
• Roof tiles (with 5% waste): 1.753.972 pcs (R$ 4.384.930,00)

Estimated stage cost: R$ 4.384.930,00""",
"TE-C20": """\
[JANELA] Slope of 300%: the limit is 100%.
Plan area: 80,00 m²
Slope: 300%
Roof area: 252,98 m²
Roof tile type: Clay
• Roof tiles (with 5% waste): 4.251 pcs (R$ 10.627,50)

Estimated stage cost: R$ 10.627,50""",
"TE-C21": """\
[TROCA] fibrocimento->15, ceramica->30
Plan area: 80,00 m²
Slope: 30%
Roof area: 83,52 m²
Roof tile type: Clay
• Roof tiles (with 5% waste): 1.404 pcs (R$ 3.510,00)

Estimated stage cost: R$ 3.510,00""",
"TE-C22": """\
[TROCA] fibrocimento->35
Plan area: 80,00 m²
Slope: 35%
Roof area: 84,76 m²
Roof tile type: Fiber cement
• Roof tiles (with 5% waste): 38 pcs (R$ 2.850,00)

Estimated stage cost: R$ 2.850,00""",
"EL-A": """\
Outlets: 20
Switches: 10
Light points: 12
Showers above 5.500 W: 2
Showers up to 5.500 W: 1
• Conduit (from plans, with 5% waste): 157,5 m = 4 rolls of 50 m (R$ 300,00)
• Wire 1,5 mm² (from plans, with 5% waste): 210,0 m = 3 rolls of 100 m (R$ 450,00)
• Wire 2,5 mm² (from plans, with 5% waste): 262,5 m = 3 rolls of 100 m (R$ 690,00)
• Wire 4 mm² (from plans, with 5% waste): 42,0 m = 1 roll of 100 m (R$ 360,00)
• Wire 6 mm² (from plans, with 5% waste): 63,0 m = 1 roll of 100 m (R$ 530,00)
• 4x2 wall boxes: 30 pcs (R$ 75,00)
• Octagonal ceiling boxes: 12 pcs (R$ 60,00)
• Outlets: 20 pcs (R$ 300,00)
• Switches: 10 pcs (R$ 120,00)

Estimated stage cost: R$ 2.885,00""",
"EL-B": """\
Outlets: 20
Switches: 10
Light points: 12
• Conduit (estimated, with 10% waste): 231,0 m = 5 rolls of 50 m (R$ 375,00)
• Wire 1,5 mm² (estimated, with 10% waste): 242,0 m = 3 rolls of 100 m (R$ 450,00)
• Wire 2,5 mm² (estimated, with 10% waste): 330,0 m = 4 rolls of 100 m (R$ 920,00)
• 4x2 wall boxes: 30 pcs (R$ 75,00)
• Octagonal ceiling boxes: 12 pcs (R$ 60,00)
• Outlets: 20 pcs (R$ 300,00)
• Switches: 10 pcs (R$ 120,00)

Estimated stage cost: R$ 2.300,00""",
"EL-B2": """\
Outlets: 20
Switches: 10
Light points: 12
Showers above 5.500 W: 2
• Conduit (estimated, with 10% waste): 253,0 m = 6 rolls of 50 m (R$ 450,00)
• Wire 1,5 mm² (estimated, with 10% waste): 242,0 m = 3 rolls of 100 m (R$ 450,00)
• Wire 2,5 mm² (estimated, with 10% waste): 330,0 m = 4 rolls of 100 m (R$ 920,00)
• Wire 6 mm² (estimated, with 10% waste): 66,0 m = 1 roll of 100 m (R$ 530,00)
• 4x2 wall boxes: 30 pcs (R$ 75,00)
• Octagonal ceiling boxes: 12 pcs (R$ 60,00)
• Outlets: 20 pcs (R$ 300,00)
• Switches: 10 pcs (R$ 120,00)

Estimated stage cost: R$ 2.905,00""",
"EL-B3": """\
Outlets: 20
Switches: 10
Light points: 12
Showers up to 5.500 W: 2
• Conduit (estimated, with 10% waste): 253,0 m = 6 rolls of 50 m (R$ 450,00)
• Wire 1,5 mm² (estimated, with 10% waste): 242,0 m = 3 rolls of 100 m (R$ 450,00)
• Wire 2,5 mm² (estimated, with 10% waste): 330,0 m = 4 rolls of 100 m (R$ 920,00)
• Wire 4 mm² (estimated, with 10% waste): 66,0 m = 1 roll of 100 m (R$ 360,00)
• 4x2 wall boxes: 30 pcs (R$ 75,00)
• Octagonal ceiling boxes: 12 pcs (R$ 60,00)
• Outlets: 20 pcs (R$ 300,00)
• Switches: 10 pcs (R$ 120,00)

Estimated stage cost: R$ 2.735,00""",
"EL-B4": """\
Outlets: 20
Switches: 10
Light points: 12
Showers above 5.500 W: 1
Showers up to 5.500 W: 1
• Conduit (estimated, with 10% waste): 253,0 m = 6 rolls of 50 m (R$ 450,00)
• Wire 1,5 mm² (estimated, with 10% waste): 242,0 m = 3 rolls of 100 m (R$ 450,00)
• Wire 2,5 mm² (estimated, with 10% waste): 330,0 m = 4 rolls of 100 m (R$ 920,00)
• Wire 4 mm² (estimated, with 10% waste): 33,0 m = 1 roll of 100 m (R$ 360,00)
• Wire 6 mm² (estimated, with 10% waste): 33,0 m = 1 roll of 100 m (R$ 530,00)
• 4x2 wall boxes: 30 pcs (R$ 75,00)
• Octagonal ceiling boxes: 12 pcs (R$ 60,00)
• Outlets: 20 pcs (R$ 300,00)
• Switches: 10 pcs (R$ 120,00)

Estimated stage cost: R$ 3.265,00""",
"EL-B5": """\
Outlets: 20
Switches: 10
Light points: 12
• Conduit (from plans, with 10% waste): 165,0 m = 4 rolls of 50 m (R$ 300,00)
• Wire 1,5 mm² (estimated, with 10% waste): 242,0 m = 3 rolls of 100 m (R$ 450,00)
• Wire 2,5 mm² (estimated, with 10% waste): 330,0 m = 4 rolls of 100 m (R$ 920,00)
• 4x2 wall boxes: 30 pcs (R$ 75,00)
• Octagonal ceiling boxes: 12 pcs (R$ 60,00)
• Outlets: 20 pcs (R$ 300,00)
• Switches: 10 pcs (R$ 120,00)

Estimated stage cost: R$ 2.225,00""",
"EL-B6": """\
Outlets: 20
Switches: 10
Light points: 12
• Conduit (estimated, with 10% waste): 231,0 m = 5 rolls of 50 m (R$ 375,00)
• Wire 1,5 mm² (estimated, with 10% waste): 242,0 m = 3 rolls of 100 m (R$ 450,00)
• Wire 2,5 mm² (from plans, with 10% waste): 275,0 m = 3 rolls of 100 m (R$ 690,00)
• 4x2 wall boxes: 30 pcs (R$ 75,00)
• Octagonal ceiling boxes: 12 pcs (R$ 60,00)
• Outlets: 20 pcs (R$ 300,00)
• Switches: 10 pcs (R$ 120,00)

Estimated stage cost: R$ 2.070,00""",
"EL-B7": """\
Showers above 5.500 W: 1
• Conduit (estimated, with 10% waste): 11,0 m = 1 roll of 50 m (R$ 75,00)
• Wire 6 mm² (estimated, with 10% waste): 33,0 m = 1 roll of 100 m (R$ 530,00)

Estimated stage cost: R$ 605,00""",
"EL-B8": """\
Showers up to 5.500 W: 1
• Conduit (estimated, with 10% waste): 11,0 m = 1 roll of 50 m (R$ 75,00)
• Wire 4 mm² (estimated, with 10% waste): 33,0 m = 1 roll of 100 m (R$ 360,00)

Estimated stage cost: R$ 435,00""",
"EL-B9": """\
Outlets: 1
• Conduit (estimated, with 10% waste): 5,5 m = 1 roll of 50 m (R$ 75,00)
• Wire 2,5 mm² (estimated, with 10% waste): 16,5 m = 1 roll of 100 m (R$ 230,00)
• 4x2 wall boxes: 1 pc (R$ 2,50)
• Outlets: 1 pc (R$ 15,00)

Estimated stage cost: R$ 322,50""",
"EL-C1": """\
Error: Enter at least one outlet, switch, light point or shower.""",
"EL-C2": """\
Error: Enter at least one outlet, switch, light point or shower.""",
"EL-C3": """\
Please enter valid numbers in the fields!""",
"EL-C4": """\
Error: Quantities cannot be negative.""",
"EL-C5": """\
Please enter valid numbers in the fields!""",
"EL-C5b": """\
Error: Quantities cannot be negative.""",
"EL-C5c": """\
Please enter valid numbers in the fields!""",
"EL-C6": """\
Error: Values cannot be negative.""",
"EL-C7": """\
Outlets: 20
Switches: 10
Light points: 12
• Conduit (estimated, with 2,5% waste): 215,3 m = 5 rolls of 50 m (R$ 375,00)
• Wire 1,5 mm² (estimated, with 2,5% waste): 225,5 m = 3 rolls of 100 m (R$ 450,00)
• Wire 2,5 mm² (estimated, with 2,5% waste): 307,5 m = 4 rolls of 100 m (R$ 920,00)
• 4x2 wall boxes: 30 pcs (R$ 75,00)
• Octagonal ceiling boxes: 12 pcs (R$ 60,00)
• Outlets: 20 pcs (R$ 300,00)
• Switches: 10 pcs (R$ 120,00)

Estimated stage cost: R$ 2.300,00""",
"EL-C8": """\
Error: Values cannot be negative.""",
"EL-C9": """\
Outlets: 20
Switches: 10
Light points: 12
• Wire 1,5 mm² (estimated, with 10% waste): 242,0 m = 3 rolls of 100 m (R$ 450,00)
• Wire 2,5 mm² (estimated, with 10% waste): 330,0 m = 4 rolls of 100 m (R$ 920,00)
• 4x2 wall boxes: 30 pcs (R$ 75,00)
• Octagonal ceiling boxes: 12 pcs (R$ 60,00)
• Outlets: 20 pcs (R$ 300,00)
• Switches: 10 pcs (R$ 120,00)

Estimated stage cost: R$ 1.925,00""",
"EL-C10": """\
Outlets: 20
Switches: 10
Light points: 12
• Conduit (from plans, with 10% waste): 165,6 m = 4 rolls of 50 m (R$ 300,00)
• Wire 1,5 mm² (estimated, with 10% waste): 242,0 m = 3 rolls of 100 m (R$ 450,00)
• Wire 2,5 mm² (estimated, with 10% waste): 330,0 m = 4 rolls of 100 m (R$ 920,00)
• 4x2 wall boxes: 30 pcs (R$ 75,00)
• Octagonal ceiling boxes: 12 pcs (R$ 60,00)
• Outlets: 20 pcs (R$ 300,00)
• Switches: 10 pcs (R$ 120,00)

Estimated stage cost: R$ 2.225,00""",
"EL-C11": """\
Outlets: 20
Switches: 10
Light points: 12
• Conduit (from plans, with 10% waste): 165,6 m = 4 rolls of 50 m (R$ 300,00)
• Wire 1,5 mm² (estimated, with 10% waste): 242,0 m = 3 rolls of 100 m (R$ 450,00)
• Wire 2,5 mm² (estimated, with 10% waste): 330,0 m = 4 rolls of 100 m (R$ 920,00)
• 4x2 wall boxes: 30 pcs (R$ 75,00)
• Octagonal ceiling boxes: 12 pcs (R$ 60,00)
• Outlets: 20 pcs (R$ 300,00)
• Switches: 10 pcs (R$ 120,00)

Estimated stage cost: R$ 2.225,00""",
"EL-C12": """\
Outlets: 20
Switches: 10
Light points: 12
• Conduit (from plans, with 10% waste): 165,6 m = 4 rolls of 50 m (R$ 300,00)
• Wire 1,5 mm² (estimated, with 10% waste): 242,0 m = 3 rolls of 100 m (R$ 450,00)
• Wire 2,5 mm² (estimated, with 10% waste): 330,0 m = 4 rolls of 100 m (R$ 920,00)
• 4x2 wall boxes: 30 pcs (R$ 75,00)
• Octagonal ceiling boxes: 12 pcs (R$ 60,00)
• Outlets: 20 pcs (R$ 300,00)
• Switches: 10 pcs (R$ 120,00)

Estimated stage cost: R$ 2.225,00""",
"EL-C13": """\
Please enter valid numbers in the fields!""",
"EL-C14": """\
Please enter valid numbers in the fields!""",
"EL-C15": """\
Outlets: 20
Switches: 10
Light points: 12
Showers above 5.500 W: 2
• Conduit (estimated, with 10% waste): 253,0 m = 6 rolls of 50 m (R$ 450,00)
• Wire 1,5 mm² (estimated, with 10% waste): 242,0 m = 3 rolls of 100 m (R$ 450,00)
• Wire 2,5 mm² (estimated, with 10% waste): 330,0 m = 4 rolls of 100 m (R$ 920,00)
• 4x2 wall boxes: 30 pcs (R$ 75,00)
• Octagonal ceiling boxes: 12 pcs (R$ 60,00)
• Outlets: 20 pcs (R$ 300,00)
• Switches: 10 pcs (R$ 120,00)

Estimated stage cost: R$ 2.375,00""",
"EL-C15b": """\
Outlets: 20
Switches: 10
Light points: 12
Showers up to 5.500 W: 2
• Conduit (estimated, with 10% waste): 253,0 m = 6 rolls of 50 m (R$ 450,00)
• Wire 1,5 mm² (estimated, with 10% waste): 242,0 m = 3 rolls of 100 m (R$ 450,00)
• Wire 2,5 mm² (estimated, with 10% waste): 330,0 m = 4 rolls of 100 m (R$ 920,00)
• 4x2 wall boxes: 30 pcs (R$ 75,00)
• Octagonal ceiling boxes: 12 pcs (R$ 60,00)
• Outlets: 20 pcs (R$ 300,00)
• Switches: 10 pcs (R$ 120,00)

Estimated stage cost: R$ 2.375,00""",
"EL-C16": """\
[JANELA] 2.000 outlets: the limit is 300.
Outlets: 2.000
Switches: 10
Light points: 12
• Conduit (estimated, with 10% waste): 11.121,0 m = 223 rolls of 50 m (R$ 16.725,00)
• Wire 1,5 mm² (estimated, with 10% waste): 242,0 m = 3 rolls of 100 m (R$ 450,00)
• Wire 2,5 mm² (estimated, with 10% waste): 33.000,0 m = 330 rolls of 100 m (R$ 75.900,00)
• 4x2 wall boxes: 2.010 pcs (R$ 5.025,00)
• Octagonal ceiling boxes: 12 pcs (R$ 60,00)
• Outlets: 2.000 pcs (R$ 30.000,00)
• Switches: 10 pcs (R$ 120,00)

Estimated stage cost: R$ 128.280,00""",
"EL-C17": """\
[JANELA] 50 showers: the limit is 10 (adding both fields).
Outlets: 20
Switches: 10
Light points: 12
Showers above 5.500 W: 50
• Conduit (estimated, with 10% waste): 781,0 m = 16 rolls of 50 m (R$ 1.200,00)
• Wire 1,5 mm² (estimated, with 10% waste): 242,0 m = 3 rolls of 100 m (R$ 450,00)
• Wire 2,5 mm² (estimated, with 10% waste): 330,0 m = 4 rolls of 100 m (R$ 920,00)
• Wire 6 mm² (estimated, with 10% waste): 1.650,0 m = 17 rolls of 100 m (R$ 9.010,00)
• 4x2 wall boxes: 30 pcs (R$ 75,00)
• Octagonal ceiling boxes: 12 pcs (R$ 60,00)
• Outlets: 20 pcs (R$ 300,00)
• Switches: 10 pcs (R$ 120,00)

Estimated stage cost: R$ 12.135,00""",
"HI-A": """\
Cold water points: 10
Hot water points: 3
Drain points: 8
• Cold water PVC pipe 25 mm (from plans, with 5% waste): 52,5 m = 9 lengths of 6 m (R$ 270,00)
• Hot water CPVC pipe 22 mm (from plans, with 5% waste): 21,0 m = 7 lengths of 3 m (R$ 315,00)
• Drain PVC pipe 40 mm (from plans, with 5% waste): 31,5 m = 6 lengths of 6 m (R$ 210,00)
• Drain PVC pipe 100 mm (from plans, with 5% waste): 18,9 m = 4 lengths of 6 m (R$ 360,00)
• Cold water fittings (estimated): 40 pcs (R$ 120,00)
• Hot water fittings (estimated): 12 pcs (R$ 108,00)
• Drain fittings (estimated): 24 pcs (R$ 144,00)
• Gate valves: 4 pcs (R$ 180,00)

Estimated stage cost: R$ 1.707,00""",
"HI-B": """\
Cold water points: 10
Hot water points: 3
Drain points: 8
• Cold water PVC pipe 25 mm (estimated, with 10% waste): 44,0 m = 8 lengths of 6 m (R$ 240,00)
• Hot water CPVC pipe 22 mm (estimated, with 10% waste): 16,5 m = 6 lengths of 3 m (R$ 270,00)
• Drain PVC pipe 40 mm (estimated, with 10% waste): 26,4 m = 5 lengths of 6 m (R$ 175,00)
• Drain PVC pipe 100 mm (estimated, with 10% waste): 17,6 m = 3 lengths of 6 m (R$ 270,00)
• Cold water fittings (estimated): 40 pcs (R$ 120,00)
• Hot water fittings (estimated): 12 pcs (R$ 108,00)
• Drain fittings (estimated): 24 pcs (R$ 144,00)
• Gate valves: 4 pcs (R$ 180,00)

Estimated stage cost: R$ 1.507,00""",
"HI-B2": """\
Cold water points: 1
• Cold water PVC pipe 25 mm (estimated, with 10% waste): 4,4 m = 1 length of 6 m (R$ 30,00)
• Cold water fittings (estimated): 4 pcs (R$ 12,00)
• Gate valves: 1 pc (R$ 45,00)

Estimated stage cost: R$ 87,00""",
"HI-B3": """\
Cold water points: 10
Hot water points: 3
Drain points: 8
• Cold water PVC pipe 25 mm (from plans, with 10% waste): 55,0 m = 10 lengths of 6 m (R$ 300,00)
• Hot water CPVC pipe 22 mm (estimated, with 10% waste): 16,5 m = 6 lengths of 3 m (R$ 270,00)
• Drain PVC pipe 40 mm (estimated, with 10% waste): 26,4 m = 5 lengths of 6 m (R$ 175,00)
• Drain PVC pipe 100 mm (estimated, with 10% waste): 17,6 m = 3 lengths of 6 m (R$ 270,00)
• Cold water fittings (estimated): 40 pcs (R$ 120,00)
• Hot water fittings (estimated): 12 pcs (R$ 108,00)
• Drain fittings (estimated): 24 pcs (R$ 144,00)
• Gate valves: 4 pcs (R$ 180,00)

Estimated stage cost: R$ 1.567,00""",
"HI-B4": """\
Drain points: 8
• Drain PVC pipe 40 mm (estimated, with 10% waste): 26,4 m = 5 lengths of 6 m (R$ 175,00)
• Drain PVC pipe 100 mm (estimated, with 10% waste): 17,6 m = 3 lengths of 6 m (R$ 270,00)
• Drain fittings (estimated): 24 pcs (R$ 144,00)

Estimated stage cost: R$ 589,00""",
"HI-C1": """\
Error: Enter at least one cold water, hot water or drain point.""",
"HI-C2": """\
Error: Enter at least one cold water, hot water or drain point.""",
"HI-C3": """\
Please enter valid numbers in the fields!""",
"HI-C4": """\
Error: Quantities cannot be negative.""",
"HI-C5": """\
Please enter valid numbers in the fields!""",
"HI-C6": """\
Error: Values cannot be negative.""",
"HI-C7": """\
Cold water points: 10
Hot water points: 3
Drain points: 8
• Cold water PVC pipe 25 mm (estimated, with 2,5% waste): 41,0 m = 7 lengths of 6 m (R$ 210,00)
• Hot water CPVC pipe 22 mm (estimated, with 2,5% waste): 15,4 m = 6 lengths of 3 m (R$ 270,00)
• Drain PVC pipe 40 mm (estimated, with 2,5% waste): 24,6 m = 5 lengths of 6 m (R$ 175,00)
• Drain PVC pipe 100 mm (estimated, with 2,5% waste): 16,4 m = 3 lengths of 6 m (R$ 270,00)
• Cold water fittings (estimated): 40 pcs (R$ 120,00)
• Hot water fittings (estimated): 12 pcs (R$ 108,00)
• Drain fittings (estimated): 24 pcs (R$ 144,00)
• Gate valves: 4 pcs (R$ 180,00)

Estimated stage cost: R$ 1.477,00""",
"HI-C8": """\
Error: Values cannot be negative.""",
"HI-C9": """\
Cold water points: 10
Hot water points: 3
Drain points: 8
• Hot water CPVC pipe 22 mm (estimated, with 10% waste): 16,5 m = 6 lengths of 3 m (R$ 270,00)
• Drain PVC pipe 40 mm (estimated, with 10% waste): 26,4 m = 5 lengths of 6 m (R$ 175,00)
• Drain PVC pipe 100 mm (estimated, with 10% waste): 17,6 m = 3 lengths of 6 m (R$ 270,00)
• Cold water fittings (estimated): 40 pcs (R$ 120,00)
• Hot water fittings (estimated): 12 pcs (R$ 108,00)
• Drain fittings (estimated): 24 pcs (R$ 144,00)
• Gate valves: 4 pcs (R$ 180,00)

Estimated stage cost: R$ 1.267,00""",
"HI-C10": """\
Cold water points: 10
Hot water points: 3
Drain points: 8
• Cold water PVC pipe 25 mm (from plans, with 10% waste): 55,6 m = 10 lengths of 6 m (R$ 300,00)
• Hot water CPVC pipe 22 mm (estimated, with 10% waste): 16,5 m = 6 lengths of 3 m (R$ 270,00)
• Drain PVC pipe 40 mm (estimated, with 10% waste): 26,4 m = 5 lengths of 6 m (R$ 175,00)
• Drain PVC pipe 100 mm (estimated, with 10% waste): 17,6 m = 3 lengths of 6 m (R$ 270,00)
• Cold water fittings (estimated): 40 pcs (R$ 120,00)
• Hot water fittings (estimated): 12 pcs (R$ 108,00)
• Drain fittings (estimated): 24 pcs (R$ 144,00)
• Gate valves: 4 pcs (R$ 180,00)

Estimated stage cost: R$ 1.567,00""",
"HI-C11": """\
Cold water points: 10
Hot water points: 3
Drain points: 8
• Cold water PVC pipe 25 mm (from plans, with 10% waste): 55,6 m = 10 lengths of 6 m (R$ 300,00)
• Hot water CPVC pipe 22 mm (estimated, with 10% waste): 16,5 m = 6 lengths of 3 m (R$ 270,00)
• Drain PVC pipe 40 mm (estimated, with 10% waste): 26,4 m = 5 lengths of 6 m (R$ 175,00)
• Drain PVC pipe 100 mm (estimated, with 10% waste): 17,6 m = 3 lengths of 6 m (R$ 270,00)
• Cold water fittings (estimated): 40 pcs (R$ 120,00)
• Hot water fittings (estimated): 12 pcs (R$ 108,00)
• Drain fittings (estimated): 24 pcs (R$ 144,00)
• Gate valves: 4 pcs (R$ 180,00)

Estimated stage cost: R$ 1.567,00""",
"HI-C12": """\
Cold water points: 10
Hot water points: 3
Drain points: 8
• Cold water PVC pipe 25 mm (from plans, with 10% waste): 55,6 m = 10 lengths of 6 m (R$ 300,00)
• Hot water CPVC pipe 22 mm (estimated, with 10% waste): 16,5 m = 6 lengths of 3 m (R$ 270,00)
• Drain PVC pipe 40 mm (estimated, with 10% waste): 26,4 m = 5 lengths of 6 m (R$ 175,00)
• Drain PVC pipe 100 mm (estimated, with 10% waste): 17,6 m = 3 lengths of 6 m (R$ 270,00)
• Cold water fittings (estimated): 40 pcs (R$ 120,00)
• Hot water fittings (estimated): 12 pcs (R$ 108,00)
• Drain fittings (estimated): 24 pcs (R$ 144,00)
• Gate valves: 4 pcs (R$ 180,00)

Estimated stage cost: R$ 1.567,00""",
"HI-C13": """\
Please enter valid numbers in the fields!""",
"HI-C14": """\
Please enter valid numbers in the fields!""",
"HI-C15": """\
[JANELA] 1.000 cold water points: the limit is 200.
Cold water points: 1.000
Hot water points: 3
Drain points: 8
• Cold water PVC pipe 25 mm (estimated, with 10% waste): 4.400,0 m = 734 lengths of 6 m (R$ 22.020,00)
• Hot water CPVC pipe 22 mm (estimated, with 10% waste): 16,5 m = 6 lengths of 3 m (R$ 270,00)
• Drain PVC pipe 40 mm (estimated, with 10% waste): 26,4 m = 5 lengths of 6 m (R$ 175,00)
• Drain PVC pipe 100 mm (estimated, with 10% waste): 17,6 m = 3 lengths of 6 m (R$ 270,00)
• Cold water fittings (estimated): 4.000 pcs (R$ 12.000,00)
• Hot water fittings (estimated): 12 pcs (R$ 108,00)
• Drain fittings (estimated): 24 pcs (R$ 144,00)
• Gate valves: 251 pcs (R$ 11.295,00)

Estimated stage cost: R$ 46.282,00""",
"CP-A": """\
Floor screed area: 40,00 m²
Average thickness: 6 cm
Mix: 1:2:3
Total volume (with 8% waste): 2,592 m³
• Cement: 20 bags of 50 kg (R$ 720,00)
• Sand: 1,30 m³ (R$ 143,00)
• Gravel: 1,94 m³ (R$ 232,80)

Estimated stage cost: R$ 1.095,80""",
"CP-B": """\
Floor screed area: 40,00 m²
Average thickness: 5 cm
Mix: 1:3:3
Total volume (with 5% waste): 2,100 m³
• Cement: 14 bags of 50 kg (R$ 504,00)
• Sand: 1,35 m³ (R$ 148,50)
• Gravel: 1,35 m³ (R$ 162,00)

Estimated stage cost: R$ 814,50""",
"CP-B2": """\
Floor screed area: 40,00 m²
Average thickness: 5 cm
Mix: 1,5:5:5
Total volume (with 5% waste): 2,100 m³
• Cement: 13 bags of 50 kg (R$ 468,00)
• Sand: 1,37 m³ (R$ 150,70)
• Gravel: 1,37 m³ (R$ 164,40)

Estimated stage cost: R$ 783,10""",
"CP-C1": """\
Please enter valid numbers in the fields!""",
"CP-C2": """\
Please enter valid numbers in the fields!""",
"CP-C3": """\
Please enter valid numbers in the fields!""",
"CP-C4": """\
Error: Area and thickness must be greater than zero.""",
"CP-C5": """\
Error: Area and thickness must be greater than zero.""",
"CP-C6": """\
Error: Area and thickness must be greater than zero.""",
"CP-C7": """\
Error: Area and thickness must be greater than zero.""",
"CP-C8": """\
Floor screed area: 40,50 m²
Average thickness: 5 cm
Mix: 1:3:3
Total volume (with 5% waste): 2,126 m³
• Cement: 14 bags of 50 kg (R$ 504,00)
• Sand: 1,37 m³ (R$ 150,70)
• Gravel: 1,37 m³ (R$ 164,40)

Estimated stage cost: R$ 819,10""",
"CP-C9": """\
Floor screed area: 40,50 m²
Average thickness: 5 cm
Mix: 1:3:3
Total volume (with 5% waste): 2,126 m³
• Cement: 14 bags of 50 kg (R$ 504,00)
• Sand: 1,37 m³ (R$ 150,70)
• Gravel: 1,37 m³ (R$ 164,40)

Estimated stage cost: R$ 819,10""",
"CP-C10": """\
Floor screed area: 40,50 m²
Average thickness: 5 cm
Mix: 1:3:3
Total volume (with 5% waste): 2,126 m³
• Cement: 14 bags of 50 kg (R$ 504,00)
• Sand: 1,37 m³ (R$ 150,70)
• Gravel: 1,37 m³ (R$ 164,40)

Estimated stage cost: R$ 819,10""",
"CP-C11": """\
Floor screed area: 40,00 m²
Average thickness: 5,5 cm
Mix: 1:3:3
Total volume (with 5% waste): 2,310 m³
• Cement: 15 bags of 50 kg (R$ 540,00)
• Sand: 1,49 m³ (R$ 163,90)
• Gravel: 1,49 m³ (R$ 178,80)

Estimated stage cost: R$ 882,70""",
"CP-C12": """\
Error: Waste cannot be negative.""",
"CP-C13": """\
Floor screed area: 40,00 m²
Average thickness: 5 cm
Mix: 1:3:3
Total volume (with 2,5% waste): 2,050 m³
• Cement: 14 bags of 50 kg (R$ 504,00)
• Sand: 1,32 m³ (R$ 145,20)
• Gravel: 1,32 m³ (R$ 158,40)

Estimated stage cost: R$ 807,60""",
"CP-C14": """\
Floor screed area: 40,00 m²
Average thickness: 5 cm
Mix: 1:3:3
Total volume (with 5% waste): 2,100 m³
• Cement: 14 bags of 50 kg (R$ 504,00)
• Sand: 1,35 m³ (R$ 148,50)
• Gravel: 1,35 m³ (R$ 162,00)

Estimated stage cost: R$ 814,50""",
"CP-C15": """\
Please enter valid numbers in the fields!""",
"CP-C16": """\
[JANELA] Area of 100.000 m²: the limit is 2.000 m².
Floor screed area: 100.000,00 m²
Average thickness: 5 cm
Mix: 1:3:3
Total volume (with 5% waste): 5.250,000 m³
• Cement: 33.750 bags of 50 kg (R$ 1.215.000,00)
• Sand: 3.375,00 m³ (R$ 371.250,00)
• Gravel: 3.375,00 m³ (R$ 405.000,00)

Estimated stage cost: R$ 1.991.250,00""",
"CP-C17": """\
[JANELA] Thickness of 50 cm: the usual is 3 cm to 10 cm.
Floor screed area: 40,00 m²
Average thickness: 50 cm
Mix: 1:3:3
Total volume (with 5% waste): 21,000 m³
• Cement: 135 bags of 50 kg (R$ 4.860,00)
• Sand: 13,50 m³ (R$ 1.485,00)
• Gravel: 13,50 m³ (R$ 1.620,00)

Estimated stage cost: R$ 7.965,00""",
"CP-C18": """\
[JANELA] Thickness of 0,5 cm: the usual is 3 cm to 10 cm.
Floor screed area: 40,00 m²
Average thickness: 0,5 cm
Mix: 1:3:3
Total volume (with 5% waste): 0,210 m³
• Cement: 2 bags of 50 kg (R$ 72,00)
• Sand: 0,14 m³ (R$ 15,40)
• Gravel: 0,14 m³ (R$ 16,80)

Estimated stage cost: R$ 104,20""",
"RE-A": """\
Gross area: 30,00 m²
Openings (doors and windows): 5,00 m²
Net area: 25,00 m²
Area to plaster (both sides): 50,00 m²
Thickness: 2,5 cm
Mix: 1:0,5:6
Plaster volume (with 12% waste): 1,400 m³
Scratch coat: included (1:3, 0,5 cm)
• Cement: 8 bags of 50 kg (R$ 288,00)
• Lime: 6 bags of 20 kg (R$ 108,00)
• Sand: 1,66 m³ (R$ 182,60)

Estimated stage cost: R$ 578,60""",
"RE-B": """\
Gross area: 30,00 m²
Thickness: 2 cm
Mix: 1:2:8
Plaster volume (with 10% waste): 0,660 m³
• Cement: 2 bags of 50 kg (R$ 72,00)
• Lime: 7 bags of 20 kg (R$ 126,00)
• Sand: 0,60 m³ (R$ 66,00)

Estimated stage cost: R$ 264,00""",
"RE-B2": """\
Gross area: 30,00 m²
Openings (doors and windows): 5,00 m²
Net area: 25,00 m²
Thickness: 2 cm
Mix: 1:2:8
Plaster volume (with 10% waste): 0,550 m³
• Cement: 2 bags of 50 kg (R$ 72,00)
• Lime: 6 bags of 20 kg (R$ 108,00)
• Sand: 0,50 m³ (R$ 55,00)

Estimated stage cost: R$ 235,00""",
"RE-B3": """\
Gross area: 30,00 m²
Area to plaster (both sides): 60,00 m²
Thickness: 2 cm
Mix: 1:2:8
Plaster volume (with 10% waste): 1,320 m³
• Cement: 4 bags of 50 kg (R$ 144,00)
• Lime: 14 bags of 20 kg (R$ 252,00)
• Sand: 1,20 m³ (R$ 132,00)

Estimated stage cost: R$ 528,00""",
"RE-B4": """\
Gross area: 30,00 m²
Thickness: 2 cm
Mix: 1:2:8
Plaster volume (with 10% waste): 0,660 m³
Scratch coat: included (1:3, 0,5 cm)
• Cement: 4 bags of 50 kg (R$ 144,00)
• Lime: 7 bags of 20 kg (R$ 126,00)
• Sand: 0,75 m³ (R$ 82,50)

Estimated stage cost: R$ 352,50""",
"RE-B5": """\
Gross area: 30,00 m²
Thickness: 2 cm
Mix: 1:0:3
Plaster volume (with 10% waste): 0,660 m³
• Cement: 5 bags of 50 kg (R$ 180,00)
• Sand: 0,62 m³ (R$ 68,20)

Estimated stage cost: R$ 248,20""",
"RE-C1": """\
Please enter valid numbers in the fields!""",
"RE-C2": """\
Please enter valid numbers in the fields!""",
"RE-C3": """\
Please enter valid numbers in the fields!""",
"RE-C4": """\
Error: Area and thickness must be greater than zero.""",
"RE-C5": """\
Error: Area and thickness must be greater than zero.""",
"RE-C6": """\
Error: Area and thickness must be greater than zero.""",
"RE-C7": """\
Gross area: 30,50 m²
Thickness: 2 cm
Mix: 1:2:8
Plaster volume (with 10% waste): 0,671 m³
• Cement: 2 bags of 50 kg (R$ 72,00)
• Lime: 7 bags of 20 kg (R$ 126,00)
• Sand: 0,61 m³ (R$ 67,10)

Estimated stage cost: R$ 265,10""",
"RE-C8": """\
Gross area: 30,50 m²
Thickness: 2 cm
Mix: 1:2:8
Plaster volume (with 10% waste): 0,671 m³
• Cement: 2 bags of 50 kg (R$ 72,00)
• Lime: 7 bags of 20 kg (R$ 126,00)
• Sand: 0,61 m³ (R$ 67,10)

Estimated stage cost: R$ 265,10""",
"RE-C9": """\
Gross area: 30,50 m²
Thickness: 2 cm
Mix: 1:2:8
Plaster volume (with 10% waste): 0,671 m³
• Cement: 2 bags of 50 kg (R$ 72,00)
• Lime: 7 bags of 20 kg (R$ 126,00)
• Sand: 0,61 m³ (R$ 67,10)

Estimated stage cost: R$ 265,10""",
"RE-C10": """\
Error: Deduction and waste cannot be negative.""",
"RE-C11": """\
Error: The openings deduction must be smaller than the area.""",
"RE-C12": """\
Error: The openings deduction must be smaller than the area.""",
"RE-C13": """\
Error: Deduction and waste cannot be negative.""",
"RE-C14": """\
Gross area: 30,00 m²
Thickness: 2 cm
Mix: 1:2:8
Plaster volume (with 2,5% waste): 0,615 m³
• Cement: 2 bags of 50 kg (R$ 72,00)
• Lime: 7 bags of 20 kg (R$ 126,00)
• Sand: 0,56 m³ (R$ 61,60)

Estimated stage cost: R$ 259,60""",
"RE-C15": """\
Please enter valid numbers in the fields!""",
"RE-C16": """\
Please enter valid numbers in the fields!""",
"RE-C17": """\
[JANELA] Area of 100.000 m²: the limit is 2.000 m².
Gross area: 100.000,00 m²
Thickness: 2 cm
Mix: 1:2:8
Plaster volume (with 10% waste): 2.200,000 m³
• Cement: 6.000 bags of 50 kg (R$ 216.000,00)
• Lime: 22.000 bags of 20 kg (R$ 396.000,00)
• Sand: 2.000,00 m³ (R$ 220.000,00)

Estimated stage cost: R$ 832.000,00""",
"RE-C18": """\
[JANELA] Thickness of 20 cm: the usual is 0,5 cm to 4 cm.
Gross area: 30,00 m²
Thickness: 20 cm
Mix: 1:2:8
Plaster volume (with 10% waste): 6,600 m³
• Cement: 19 bags of 50 kg (R$ 684,00)
• Lime: 67 bags of 20 kg (R$ 1.206,00)
• Sand: 6,00 m³ (R$ 660,00)

Estimated stage cost: R$ 2.550,00""",
"PI-A": """\
Area: 40,00 m²
Area with waste (12%): 44,80 m²
Tile: 60x60 cm
Laying: patterned
• Tiles: 125
• Boxes: 21 (2,16 m² per box) (R$ 2.240,00)
• Tile adhesive AC-II: 12 bags of 20 kg (224,0 kg) (R$ 360,00)
• Baseboard: 33,60 m (56 pcs of 0,60 m) (R$ 504,00)

Estimated stage cost: R$ 3.104,00""",
"PI-B": """\
Area: 40,00 m²
Area with waste (10%, automatic): 44,00 m²
Tile: 60x60 cm
• Tiles: 123 (R$ 2.200,00)
• Tile adhesive AC-I: 11 bags of 20 kg (220,0 kg) (R$ 242,00)

Estimated stage cost: R$ 2.442,00""",
"PI-B2": """\
Area: 40,00 m²
Area with waste (15%, automatic): 46,00 m²
Tile: 80x80 cm
• Tiles: 72 (R$ 2.300,00)
• Tile adhesive AC-I: 19 bags of 20 kg (368,0 kg) (R$ 418,00)

Estimated stage cost: R$ 2.718,00""",
"PI-B3": """\
Area: 40,00 m²
Area with waste (20%, automatic): 48,00 m²
Tile: 120x60 cm
• Tiles: 67 (R$ 2.400,00)
• Tile adhesive AC-I: 20 bags of 20 kg (384,0 kg) (R$ 440,00)

Estimated stage cost: R$ 2.840,00""",
"PI-B4": """\
Area: 40,00 m²
Area with waste (25%, automatic): 50,00 m²
Tile: 60x60 cm
Laying: patterned
• Tiles: 139 (R$ 2.500,00)
• Tile adhesive AC-I: 13 bags of 20 kg (250,0 kg) (R$ 286,00)

Estimated stage cost: R$ 2.786,00""",
"PI-B5": """\
Area: 40,00 m²
Area with waste (10%, automatic): 44,00 m²
Tile: 60x60 cm
• Tiles: 123
• Boxes: 21 (2,16 m² per box) (R$ 2.200,00)
• Tile adhesive AC-I: 11 bags of 20 kg (220,0 kg) (R$ 242,00)

Estimated stage cost: R$ 2.442,00""",
"PI-B6": """\
Area: 40,00 m²
Area with waste (10%, automatic): 44,00 m²
Tile: 60x60 cm
• Tiles: 123 (R$ 2.200,00)
• Tile adhesive AC-I: 11 bags of 20 kg (220,0 kg) (R$ 242,00)
• Baseboard: 33,00 m (R$ 495,00)

Estimated stage cost: R$ 2.937,00""",
"PI-B7": """\
Area: 40,00 m²
Area with waste (10%, automatic): 44,00 m²
Tile: 60x60 cm
• Tiles: 123 (R$ 2.200,00)
• Tile adhesive AC-I: 11 bags of 20 kg (220,0 kg) (R$ 242,00)
• Baseboard: 33,00 m (55 pcs of 0,60 m) (R$ 495,00)

Estimated stage cost: R$ 2.937,00""",
"PI-B8": """\
Area: 40,00 m²
Area with waste (10%, automatic): 44,00 m²
Tile: 60x60 cm
• Tiles: 123 (R$ 2.200,00)
• Tile adhesive AC-III: 11 bags of 20 kg (220,0 kg) (R$ 462,00)

Estimated stage cost: R$ 2.662,00""",
"PI-C1": """\
Please enter valid numbers in the fields!""",
"PI-C2": """\
Please enter valid numbers in the fields!""",
"PI-C3": """\
Please enter valid numbers in the fields!""",
"PI-C4": """\
Error: Area and tile size must be greater than zero.""",
"PI-C5": """\
Error: Area and tile size must be greater than zero.""",
"PI-C6": """\
Error: Area and tile size must be greater than zero.""",
"PI-C7": """\
Area: 40,50 m²
Area with waste (10%, automatic): 44,55 m²
Tile: 60x60 cm
• Tiles: 124 (R$ 2.227,50)
• Tile adhesive AC-I: 12 bags of 20 kg (222,8 kg) (R$ 264,00)

Estimated stage cost: R$ 2.491,50""",
"PI-C8": """\
Area: 40,50 m²
Area with waste (10%, automatic): 44,55 m²
Tile: 60x60 cm
• Tiles: 124 (R$ 2.227,50)
• Tile adhesive AC-I: 12 bags of 20 kg (222,8 kg) (R$ 264,00)

Estimated stage cost: R$ 2.491,50""",
"PI-C9": """\
Area: 40,50 m²
Area with waste (10%, automatic): 44,55 m²
Tile: 60x60 cm
• Tiles: 124 (R$ 2.227,50)
• Tile adhesive AC-I: 12 bags of 20 kg (222,8 kg) (R$ 264,00)

Estimated stage cost: R$ 2.491,50""",
"PI-C10": """\
Error: Waste cannot be negative.""",
"PI-C11": """\
Area: 40,00 m²
Area with waste (2,5%): 41,00 m²
Tile: 60x60 cm
• Tiles: 114 (R$ 2.050,00)
• Tile adhesive AC-I: 11 bags of 20 kg (205,0 kg) (R$ 242,00)

Estimated stage cost: R$ 2.292,00""",
"PI-C12": """\
Area: 40,00 m²
Area with waste (0%): 40,00 m²
Tile: 60x60 cm
• Tiles: 112 (R$ 2.000,00)
• Tile adhesive AC-I: 10 bags of 20 kg (200,0 kg) (R$ 220,00)

Estimated stage cost: R$ 2.220,00""",
"PI-C13": """\
Error: Values cannot be negative.""",
"PI-C14": """\
Error: Values cannot be negative.""",
"PI-C15": """\
Please enter valid numbers in the fields!""",
"PI-C16": """\
Area: 40,00 m²
Area with waste (10%, automatic): 44,00 m²
Tile: 70x70 cm
• Tiles: 90 (R$ 2.200,00)
• Tile adhesive AC-I: 18 bags of 20 kg (352,0 kg) (R$ 396,00)

Estimated stage cost: R$ 2.596,00""",
"PI-C17": """\
Area: 40,00 m²
Area with waste (15%, automatic): 46,00 m²
Tile: 90x90 cm
• Tiles: 57 (R$ 2.300,00)
• Tile adhesive AC-I: 19 bags of 20 kg (368,0 kg) (R$ 418,00)

Estimated stage cost: R$ 2.718,00""",
"PI-C18": """\
Area: 40,00 m²
Area with waste (10%, automatic): 44,00 m²
Tile: 60,5x60 cm
• Tiles: 122 (R$ 2.200,00)
• Tile adhesive AC-I: 18 bags of 20 kg (352,0 kg) (R$ 396,00)

Estimated stage cost: R$ 2.596,00""",
"PI-C19": """\
Area: 40,00 m²
Area with waste (10%, automatic): 44,00 m²
Tile: 60x60 cm
• Tiles: 123 (R$ 2.200,00)
• Tile adhesive AC-I: 11 bags of 20 kg (220,0 kg) (R$ 242,00)

Estimated stage cost: R$ 2.442,00""",
"PI-C20": """\
[JANELA] Area of 100.000 m²: the limit is 2.000 m².
Area: 100.000,00 m²
Area with waste (10%, automatic): 110.000,00 m²
Tile: 60x60 cm
• Tiles: 305.556 (R$ 5.500.000,00)
• Tile adhesive AC-I: 27.500 bags of 20 kg (550.000,0 kg) (R$ 605.000,00)

Estimated stage cost: R$ 6.105.000,00""",
"AZ-A": """\
Area: 30,00 m²
Openings (doors and windows): 4,00 m²
Net area: 26,00 m²
Area with waste (15%): 29,90 m²
Tile: 30x60 cm
Laying: patterned
• Tiles: 167
• Boxes: 17 (1,80 m² per box) (R$ 1.196,00)
• Tile adhesive AC-III: 8 bags of 20 kg (149,5 kg) (R$ 336,00)

Estimated stage cost: R$ 1.532,00""",
"AZ-B": """\
Area: 30,00 m²
Area with waste (10%, automatic): 33,00 m²
Tile: 30x60 cm
• Tiles: 184 (R$ 1.320,00)
• Tile adhesive AC-II: 9 bags of 20 kg (165,0 kg) (R$ 270,00)

Estimated stage cost: R$ 1.590,00""",
"AZ-B2": """\
Area: 30,00 m²
Openings (doors and windows): 4,00 m²
Net area: 26,00 m²
Area with waste (10%, automatic): 28,60 m²
Tile: 30x60 cm
• Tiles: 159 (R$ 1.144,00)
• Tile adhesive AC-II: 8 bags of 20 kg (143,0 kg) (R$ 240,00)

Estimated stage cost: R$ 1.384,00""",
"AZ-B3": """\
Area: 30,00 m²
Area with waste (10%, automatic): 33,00 m²
Tile: 30x60 cm
• Tiles: 184
• Boxes: 19 (1,80 m² per box) (R$ 1.320,00)
• Tile adhesive AC-II: 9 bags of 20 kg (165,0 kg) (R$ 270,00)

Estimated stage cost: R$ 1.590,00""",
"AZ-B4": """\
Area: 30,00 m²
Area with waste (25%, automatic): 37,50 m²
Tile: 30x60 cm
Laying: patterned
• Tiles: 209 (R$ 1.500,00)
• Tile adhesive AC-II: 10 bags of 20 kg (187,5 kg) (R$ 300,00)

Estimated stage cost: R$ 1.800,00""",
"AZ-B5": """\
Area: 30,00 m²
Area with waste (10%, automatic): 33,00 m²
Tile: 30x60 cm
• Tiles: 184 (R$ 1.320,00)
• Tile adhesive AC-III: 9 bags of 20 kg (165,0 kg) (R$ 378,00)

Estimated stage cost: R$ 1.698,00""",
"AZ-B6": """\
Area: 30,00 m²
Area with waste (15%, automatic): 34,50 m²
Tile: 30x90 cm
• Tiles: 128 (R$ 1.380,00)
• Tile adhesive AC-II: 14 bags of 20 kg (276,0 kg) (R$ 420,00)

Estimated stage cost: R$ 1.800,00""",
"AZ-C1": """\
Please enter valid numbers in the fields!""",
"AZ-C2": """\
Please enter valid numbers in the fields!""",
"AZ-C3": """\
Please enter valid numbers in the fields!""",
"AZ-C4": """\
Error: Area and tile size must be greater than zero.""",
"AZ-C5": """\
Error: Area and tile size must be greater than zero.""",
"AZ-C6": """\
Area: 30,50 m²
Area with waste (10%, automatic): 33,55 m²
Tile: 30x60 cm
• Tiles: 187 (R$ 1.342,00)
• Tile adhesive AC-II: 9 bags of 20 kg (167,8 kg) (R$ 270,00)

Estimated stage cost: R$ 1.612,00""",
"AZ-C7": """\
Area: 30,50 m²
Area with waste (10%, automatic): 33,55 m²
Tile: 30x60 cm
• Tiles: 187 (R$ 1.342,00)
• Tile adhesive AC-II: 9 bags of 20 kg (167,8 kg) (R$ 270,00)

Estimated stage cost: R$ 1.612,00""",
"AZ-C8": """\
Area: 30,50 m²
Area with waste (10%, automatic): 33,55 m²
Tile: 30x60 cm
• Tiles: 187 (R$ 1.342,00)
• Tile adhesive AC-II: 9 bags of 20 kg (167,8 kg) (R$ 270,00)

Estimated stage cost: R$ 1.612,00""",
"AZ-C9": """\
Error: Values cannot be negative.""",
"AZ-C10": """\
Error: The openings deduction must be smaller than the area.""",
"AZ-C11": """\
Error: The openings deduction must be smaller than the area.""",
"AZ-C12": """\
Error: Waste cannot be negative.""",
"AZ-C13": """\
Area: 30,00 m²
Area with waste (2,5%): 30,75 m²
Tile: 30x60 cm
• Tiles: 171 (R$ 1.230,00)
• Tile adhesive AC-II: 8 bags of 20 kg (153,8 kg) (R$ 240,00)

Estimated stage cost: R$ 1.470,00""",
"AZ-C14": """\
Please enter valid numbers in the fields!""",
"AZ-C15": """\
Please enter valid numbers in the fields!""",
"AZ-C16": """\
[JANELA] Area of 100.000 m²: the limit is 2.000 m².
Area: 100.000,00 m²
Area with waste (10%, automatic): 110.000,00 m²
Tile: 30x60 cm
• Tiles: 611.112 (R$ 4.400.000,00)
• Tile adhesive AC-II: 27.500 bags of 20 kg (550.000,0 kg) (R$ 825.000,00)

Estimated stage cost: R$ 5.225.000,00""",
"RJ-A": """\
Area: 40,00 m²
Tile: 60x60 cm
Joint: 3 mm
Tile thickness: 10 mm
Consumption: 0,158 kg/m²
• Grout (with 15% waste): 7,3 kg = 4 tubs of 2 kg (R$ 72,00)

Estimated stage cost: R$ 72,00""",
"RJ-B": """\
Area: 40,00 m²
Tile: 60x60 cm
Joint: 3 mm
Tile thickness: 8 mm
Consumption: 0,126 kg/m²
• Grout (with 10% waste): 5,6 kg = 3 tubs of 2 kg (R$ 54,00)

Estimated stage cost: R$ 54,00""",
"RJ-B2": """\
Area: 40,00 m²
Tile: 30x30 cm
Joint: 5 mm
Tile thickness: 8 mm
Consumption: 0,421 kg/m²
• Grout (with 10% waste): 18,5 kg = 9 tubs of 2 kg and 1 tub of 1 kg (R$ 172,00)

Estimated stage cost: R$ 172,00""",
"RJ-B3": """\
[BOTÃO] piso: ('40', '60', '60')
[CAMPOS] área 40, peça 60 x 60
Area: 40,00 m²
Tile: 60x60 cm
Joint: 3 mm
Tile thickness: 8 mm
Consumption: 0,126 kg/m²
• Grout (with 10% waste): 5,6 kg = 3 tubs of 2 kg (R$ 54,00)

Estimated stage cost: R$ 54,00""",
"RJ-B4": """\
[BOTÃO] azulejo: ('26', '30', '60')
[CAMPOS] área 26, peça 30 x 60
Area: 26,00 m²
Tile: 30x60 cm
Joint: 2 mm
Tile thickness: 8 mm
Consumption: 0,126 kg/m²
• Grout (with 10% waste): 3,6 kg = 2 tubs of 2 kg (R$ 36,00)

Estimated stage cost: R$ 36,00""",
"RJ-C1": """\
Please enter valid numbers in the fields!""",
"RJ-C2": """\
Please enter valid numbers in the fields!""",
"RJ-C3": """\
Please enter valid numbers in the fields!""",
"RJ-C4": """\
Error: Area, tile size and joint must be greater than zero.""",
"RJ-C5": """\
Error: Area, tile size and joint must be greater than zero.""",
"RJ-C6": """\
Error: Area, tile size and joint must be greater than zero.""",
"RJ-C7": """\
Error: Area, tile size and joint must be greater than zero.""",
"RJ-C8": """\
Area: 40,50 m²
Tile: 60x60 cm
Joint: 3 mm
Tile thickness: 8 mm
Consumption: 0,126 kg/m²
• Grout (with 10% waste): 5,6 kg = 3 tubs of 2 kg (R$ 54,00)

Estimated stage cost: R$ 54,00""",
"RJ-C9": """\
Area: 40,50 m²
Tile: 60x60 cm
Joint: 3 mm
Tile thickness: 8 mm
Consumption: 0,126 kg/m²
• Grout (with 10% waste): 5,6 kg = 3 tubs of 2 kg (R$ 54,00)

Estimated stage cost: R$ 54,00""",
"RJ-C10": """\
Area: 40,50 m²
Tile: 60x60 cm
Joint: 3 mm
Tile thickness: 8 mm
Consumption: 0,126 kg/m²
• Grout (with 10% waste): 5,6 kg = 3 tubs of 2 kg (R$ 54,00)

Estimated stage cost: R$ 54,00""",
"RJ-C11": """\
Area: 40,00 m²
Tile: 60x60 cm
Joint: 1,5 mm
Tile thickness: 8 mm
Consumption: 0,063 kg/m²
• Grout (with 10% waste): 2,8 kg = 1 tub of 2 kg and 1 tub of 1 kg (R$ 28,00)

Estimated stage cost: R$ 28,00""",
"RJ-C12": """\
[JANELA] Joint of 0,5 mm: the usual is 1 mm to 15 mm.
Area: 40,00 m²
Tile: 60x60 cm
Joint: 0,5 mm
Tile thickness: 8 mm
Consumption: 0,021 kg/m²
• Grout (with 10% waste): 0,9 kg = 1 tub of 1 kg (R$ 10,00)

Estimated stage cost: R$ 10,00""",
"RJ-C13": """\
Area: 40,00 m²
Tile: 60x60 cm
Joint: 3 mm
Tile thickness: 8 mm
Consumption: 0,126 kg/m²
• Grout (with 10% waste): 5,6 kg = 3 tubs of 2 kg (R$ 54,00)

Estimated stage cost: R$ 54,00""",
"RJ-C14": """\
Error: The tile thickness must be greater than zero.""",
"RJ-C15": """\
Error: Waste cannot be negative.""",
"RJ-C16": """\
Area: 40,00 m²
Tile: 60x60 cm
Joint: 3 mm
Tile thickness: 8 mm
Consumption: 0,126 kg/m²
• Grout (with 2,5% waste): 5,2 kg = 3 tubs of 2 kg (R$ 54,00)

Estimated stage cost: R$ 54,00""",
"RJ-C17": """\
Please enter valid numbers in the fields!""",
"RJ-C18": """\
Area: 1,00 m²
Tile: 60x60 cm
Joint: 3 mm
Tile thickness: 8 mm
Consumption: 0,126 kg/m²
• Grout (with 10% waste): 0,1 kg = 1 tub of 1 kg (R$ 10,00)

Estimated stage cost: R$ 10,00""",
"RJ-C19": """\
[JANELA] Area of 100.000 m²: the limit is 2.000 m².
Area: 100.000,00 m²
Tile: 60x60 cm
Joint: 3 mm
Tile thickness: 8 mm
Consumption: 0,126 kg/m²
• Grout (with 10% waste): 13.904,0 kg = 6.952 tubs of 2 kg (R$ 125.136,00)

Estimated stage cost: R$ 125.136,00""",
"RJ-C20": """\
[JANELA] Joint of 30 mm: the usual is 1 mm to 15 mm.
Area: 40,00 m²
Tile: 60x60 cm
Joint: 30 mm
Tile thickness: 8 mm
Consumption: 1,264 kg/m²
• Grout (with 10% waste): 55,6 kg = 28 tubs of 2 kg (R$ 504,00)

Estimated stage cost: R$ 504,00""",
"PT-A": """\
Walls: 100,00 m²
Ceiling: 40,00 m²
Coats: 3
Coverage: 10 m²/L
• Wall paint (with 15% waste): 34,5 L = 2 pails of 18 L (R$ 600,00)
• Ceiling paint (with 15% waste): 13,8 L = 4 cans of 3,6 L (R$ 300,00)
• Sealer (with 15% waste): 20,1 L = 1 pail of 18 L and 1 can of 3,6 L (R$ 195,00)
• Primer (with 15% waste): 16,1 L = 1 pail of 18 L (R$ 170,00)
• Wall putty (with 15% waste): 161,0 kg = 7 buckets of 25 kg (R$ 560,00)
Add-ons (over wall + ceiling): Sealer 1 coat, Primer 1 coat, Wall putty 2 coats

Estimated stage cost: R$ 1.825,00""",
"PT-B": """\
Walls: 100,00 m²
Coats: 2
Coverage: 12 m²/L
• Wall paint (with 10% waste): 18,3 L = 1 pail of 18 L and 1 can of 3,6 L (R$ 390,00)

Estimated stage cost: R$ 390,00""",
"PT-B2": """\
Ceiling: 40,00 m²
Coats: 2
Coverage: 12 m²/L
• Ceiling paint (with 10% waste): 7,3 L = 3 cans of 3,6 L (R$ 225,00)

Estimated stage cost: R$ 225,00""",
"PT-B3": """\
Walls: 100,00 m²
Ceiling: 40,00 m²
Coats: 2
Coverage: 12 m²/L
• Wall paint (with 10% waste): 18,3 L = 1 pail of 18 L and 1 can of 3,6 L (R$ 390,00)
• Ceiling paint (with 10% waste): 7,3 L = 3 cans of 3,6 L (R$ 225,00)

Estimated stage cost: R$ 615,00""",
"PT-B4": """\
Walls: 100,00 m²
Coats: 2
Coverage: 12 m²/L
• Wall paint (with 10% waste): 18,3 L = 1 pail of 18 L and 1 can of 3,6 L (R$ 390,00)
• Sealer (with 10% waste): 13,8 L = 4 cans of 3,6 L (R$ 180,00)
Add-ons (over wall + ceiling): Sealer 1 coat

Estimated stage cost: R$ 570,00""",
"PT-B5": """\
Walls: 100,00 m²
Coats: 2
Coverage: 12 m²/L
• Wall paint (with 10% waste): 18,3 L = 1 pail of 18 L and 1 can of 3,6 L (R$ 390,00)
• Acrylic putty (with 10% waste): 110,0 kg = 5 buckets of 25 kg (R$ 650,00)
Add-ons (over wall + ceiling): Acrylic putty 2 coats

Estimated stage cost: R$ 1.040,00""",
"PT-B6": """\
Walls: 100,00 m²
Coats: 2
Coverage: 12 m²/L
• Wall paint (with 10% waste): 18,3 L = 1 pail of 18 L and 1 can of 3,6 L (R$ 390,00)
• Primer (with 10% waste): 11,0 L = 4 cans of 3,6 L (R$ 200,00)
Add-ons (over wall + ceiling): Primer 1 coat

Estimated stage cost: R$ 590,00""",
"PT-B7": """\
Walls: 180,00 m²
Coats: 2
Coverage: 12 m²/L
• Wall paint (with 10% waste): 33,0 L = 2 pails of 18 L (R$ 600,00)

Estimated stage cost: R$ 600,00""",
"PT-B8": """\
Walls: 10,00 m²
Coats: 2
Coverage: 12 m²/L
• Wall paint (with 10% waste): 1,8 L = 1 can of 3,6 L (R$ 90,00)

Estimated stage cost: R$ 90,00""",
"PT-C1": """\
Please enter valid numbers in the fields!""",
"PT-C2": """\
Please enter valid numbers in the fields!""",
"PT-C3": """\
Please enter valid numbers in the fields!""",
"PT-C4": """\
Error: Enter the wall area or the ceiling area.""",
"PT-C5": """\
Error: Areas cannot be negative.""",
"PT-C6": """\
Error: Coats and coverage must be greater than zero.""",
"PT-C7": """\
Error: Coats and coverage must be greater than zero.""",
"PT-C8": """\
Please enter valid numbers in the fields!""",
"PT-C9": """\
Walls: 100,00 m²
Coats: 5
Coverage: 12 m²/L
• Wall paint (with 10% waste): 45,8 L = 2 pails of 18 L and 3 cans of 3,6 L (R$ 870,00)

Estimated stage cost: R$ 870,00""",
"PT-C10": """\
[JANELA] 6 coats: the limit is 5 (usually 2 or 3).
Walls: 100,00 m²
Coats: 6
Coverage: 12 m²/L
• Wall paint (with 10% waste): 55,0 L = 3 pails of 18 L and 1 can of 3,6 L (R$ 990,00)

Estimated stage cost: R$ 990,00""",
"PT-C11": """\
[JANELA] 22 coats: the limit is 5 (usually 2 or 3).
Walls: 100,00 m²
Coats: 22
Coverage: 12 m²/L
• Wall paint (with 10% waste): 201,7 L = 11 pails of 18 L and 2 cans of 3,6 L (R$ 3.480,00)

Estimated stage cost: R$ 3.480,00""",
"PT-C12": """\
Walls: 100,50 m²
Coats: 2
Coverage: 12 m²/L
• Wall paint (with 10% waste): 18,4 L = 1 pail of 18 L and 1 can of 3,6 L (R$ 390,00)

Estimated stage cost: R$ 390,00""",
"PT-C13": """\
Walls: 100,50 m²
Coats: 2
Coverage: 12 m²/L
• Wall paint (with 10% waste): 18,4 L = 1 pail of 18 L and 1 can of 3,6 L (R$ 390,00)

Estimated stage cost: R$ 390,00""",
"PT-C14": """\
Walls: 100,50 m²
Coats: 2
Coverage: 12 m²/L
• Wall paint (with 10% waste): 18,4 L = 1 pail of 18 L and 1 can of 3,6 L (R$ 390,00)

Estimated stage cost: R$ 390,00""",
"PT-C15": """\
Error: Coats and coverage must be greater than zero.""",
"PT-C16": """\
Walls: 100,00 m²
Coats: 2
Coverage: 12 m²/L
• Wall paint (with 10% waste): 18,3 L = 1 pail of 18 L and 1 can of 3,6 L (R$ 390,00)

Estimated stage cost: R$ 390,00""",
"PT-C17": """\
Walls: 100,00 m²
Coats: 2
Coverage: 12,5 m²/L
• Wall paint (with 10% waste): 17,6 L = 1 pail of 18 L (R$ 300,00)

Estimated stage cost: R$ 300,00""",
"PT-C18": """\
Error: Waste cannot be negative.""",
"PT-C19": """\
Walls: 100,00 m²
Coats: 2
Coverage: 12 m²/L
• Wall paint (with 2,5% waste): 17,1 L = 1 pail of 18 L (R$ 300,00)

Estimated stage cost: R$ 300,00""",
"PT-C20": """\
Please enter valid numbers in the fields!""",
"PT-C21": """\
[JANELA] Wall area of 100.000 m²: the limit is 5.000 m².
Walls: 100.000,00 m²
Coats: 2
Coverage: 12 m²/L
• Wall paint (with 10% waste): 18.333,3 L = 1.018 pails of 18 L and 3 cans of 3,6 L (R$ 305.670,00)

Estimated stage cost: R$ 305.670,00""",
"ES-A": """\
Doors:
• 3x Door 80 x 210 cm (Wood): 1,68 m² each
• 1x Door 90 x 210 cm (Aluminum): 1,89 m² each

Windows:
• 4x Window 120 x 100 cm (Aluminum): 1,20 m² each
• 1x Window 60 x 60 cm (Tempered glass): 0,36 m² each

Total: 4 doors and 5 windows
Total opening area: 12,09 m²

Fixing materials:
• Expanding foam: 7 cans of 500 ml (R$ 245,00)
• Screws and anchors: 101 pcs (R$ 80,80)
• Fixing mortar: 60,2 kg = 4 bags of 20 kg (R$ 100,00)

Estimated stage cost: R$ 425,80

Doors and windows: use this list to request a quote from the supplier.""",
"ES-B": """\
Doors:
• 3x Door 80 x 210 cm: 1,68 m² each

Windows:
• 2x Window 120 x 100 cm: 1,20 m² each

Total: 3 doors and 2 windows
Total opening area: 7,44 m²

Doors and windows: use this list to request a quote from the supplier.""",
"ES-B2": """\
Doors:
• 3x Door 80 x 210 cm: 1,68 m² each

Windows:
• 2x Window 120 x 100 cm: 1,20 m² each

Total: 3 doors and 2 windows
Total opening area: 7,44 m²

Fixing materials:
• Expanding foam: 4 cans of 500 ml (R$ 140,00)

Estimated stage cost: R$ 140,00

Doors and windows: use this list to request a quote from the supplier.""",
"ES-B3": """\
Doors:
• 3x Door 80 x 210 cm: 1,68 m² each

Windows:
• 2x Window 120 x 100 cm: 1,20 m² each

Total: 3 doors and 2 windows
Total opening area: 7,44 m²

Fixing materials:
• Screws and anchors: 60 pcs (R$ 48,00)

Estimated stage cost: R$ 48,00

Doors and windows: use this list to request a quote from the supplier.""",
"ES-B4": """\
Doors:
• 3x Door 80 x 210 cm: 1,68 m² each

Windows:
• 2x Window 120 x 100 cm: 1,20 m² each

Total: 3 doors and 2 windows
Total opening area: 7,44 m²

Fixing materials:
• Fixing mortar: 35,7 kg = 2 bags of 20 kg (R$ 50,00)

Estimated stage cost: R$ 50,00

Doors and windows: use this list to request a quote from the supplier.""",
"ES-B5": """\
Doors:
• 5x Door 80 x 210 cm: 1,68 m² each

Windows:
• 2x Window 120 x 100 cm: 1,20 m² each

Total: 5 doors and 2 windows
Total opening area: 10,80 m²

Doors and windows: use this list to request a quote from the supplier.""",
"ES-B6": """\
[X] lista: ['3x Door 80 x 210 cm']; resultado antigo sumiu
Doors:
• 3x Door 80 x 210 cm: 1,68 m² each

Total: 3 doors
Total opening area: 5,04 m²

Doors and windows: use this list to request a quote from the supplier.""",
"ES-C1": """\
No doors or windows on the list yet.""",
"ES-C2": """\
[Adicionar] Please enter valid numbers in the fields!
[Adicionar] nada entrou na lista
No doors or windows on the list yet.""",
"ES-C3": """\
[Adicionar] Please enter valid numbers in the fields!
[Adicionar] nada entrou na lista
No doors or windows on the list yet.""",
"ES-C4": """\
[Adicionar] Please enter valid numbers in the fields!
[Adicionar] nada entrou na lista
No doors or windows on the list yet.""",
"ES-C5": """\
[Adicionar] Please enter valid numbers in the fields!
[Adicionar] nada entrou na lista
No doors or windows on the list yet.""",
"ES-C6": """\
[Adicionar] Please enter valid numbers in the fields!
[Adicionar] nada entrou na lista
No doors or windows on the list yet.""",
"ES-C7": """\
[Adicionar] Please enter valid numbers in the fields!
[Adicionar] nada entrou na lista
No doors or windows on the list yet.""",
"ES-C8": """\
[Adicionar] Please enter valid numbers in the fields!
[Adicionar] nada entrou na lista
No doors or windows on the list yet.""",
"ES-C9": """\
You entered a door or window but did not tap "Add to list".""",
"ES-C10a": """\
Windows:
• 1x Window 120,5 x 100 cm: 1,21 m² each

Total: 1 window
Total opening area: 1,21 m²

Doors and windows: use this list to request a quote from the supplier.""",
"ES-C10b": """\
Windows:
• 1x Window 120,5 x 100 cm: 1,21 m² each

Total: 1 window
Total opening area: 1,21 m²

Doors and windows: use this list to request a quote from the supplier.""",
"ES-C10c": """\
Windows:
• 1x Window 120,5 x 100 cm: 1,21 m² each

Total: 1 window
Total opening area: 1,21 m²

Doors and windows: use this list to request a quote from the supplier.""",
"ES-C11": """\
Doors:
• 1x Door 80 x 210 cm: 1,68 m² each

Total: 1 door
Total opening area: 1,68 m²

Fixing materials:
• Expanding foam: 1 can of 500 ml (R$ 35,00)
• Screws and anchors: 13 pcs (R$ 10,40)
• Fixing mortar: 7,5 kg = 1 bag of 20 kg (R$ 25,00)

Estimated stage cost: R$ 70,40

Doors and windows: use this list to request a quote from the supplier.""",
"ES-C12": """\
[JANELA no Adicionar] Quantity of 1.000: the limit is 100 of each item.
Doors:
• 1.000x Door 80 x 210 cm: 1,68 m² each

Total: 1.000 doors
Total opening area: 1.680,00 m²

Fixing materials:
• Expanding foam: 834 cans of 500 ml (R$ 29.190,00)
• Screws and anchors: 12.500 pcs (R$ 10.000,00)
• Fixing mortar: 7.500,0 kg = 375 bags of 20 kg (R$ 9.375,00)

Estimated stage cost: R$ 48.565,00

Doors and windows: use this list to request a quote from the supplier.""",
"ES-C13": """\
[JANELA no Adicionar] Width of 8.000 cm: the limit is 500 cm.
Doors:
• 3x Door 8.000 x 210 cm: 168,00 m² each

Total: 3 doors
Total opening area: 504,00 m²

Doors and windows: use this list to request a quote from the supplier.""",
}


if __name__ == "__main__":
    main()
