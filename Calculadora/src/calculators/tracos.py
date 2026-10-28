"""
Traços (proporções em VOLUME) de concreto e de massa (argamassa).

Este é o único lugar onde os traços e as constantes de conversão ficam.
Para incluir/remover um traço, edite as tabelas abaixo; as telas e os
cálculos leem daqui.

ATENÇÃO (conferir na revisão dos cálculos): FATOR_VOLUME_APARENTE_CONCRETO e as
densidades são premissas de trabalho, não valores validados.
"""

# --- CONCRETO: cimento : areia : pedra ------------------------------------
# Usado nas Brocas, no Baldrame, na Laje e no Contrapiso.
TRACOS_CONCRETO = {
    "1:2:3":   {"cimento": 1.0, "areia": 2.0, "pedra": 3.0},
    "1:3:3":   {"cimento": 1.0, "areia": 3.0, "pedra": 3.0},
    "1:4:3":   {"cimento": 1.0, "areia": 4.0, "pedra": 3.0},
    "1.5:5:5": {"cimento": 1.5, "areia": 5.0, "pedra": 5.0},
}
TRACO_CONCRETO_PADRAO = "1:2:3"

# --- MASSA (assentamento / reboco / chapisco): cimento : cal : areia -------
# Usada nas abas de Paredes e Reboco (valores do app antigo).
TRACOS_MASSA = {
    "1:2:8":   {"cimento": 1.0, "cal": 2.0, "areia": 8.0},
    "1:0.5:6": {"cimento": 1.0, "cal": 0.5, "areia": 6.0},
    "1.5:1:8": {"cimento": 1.5, "cal": 1.0, "areia": 8.0},
    "1:0:3":   {"cimento": 1.0, "cal": 0.0, "areia": 3.0},
    "1.5:0:4": {"cimento": 1.5, "cal": 0.0, "areia": 4.0},
}
TRACO_MASSA_PADRAO = "1:2:8"

# --- Constantes de conversão (premissas) ----------------------------------
DENSIDADE_CIMENTO = 1500.0   # kg/m3 (aparente)
DENSIDADE_CAL = 1100.0       # kg/m3 (aparente)
SACO_CIMENTO_KG = 50.0
SACO_CAL_KG = 20.0

# m3 de material solto (cimento + areia + pedra) necessários para 1 m3 de concreto
FATOR_VOLUME_APARENTE_CONCRETO = 1.5

# Inchamento da areia na massa: a areia solta e úmida ocupa mais espaço, então é preciso
# comprar mais areia do que a conta pelo volume dá. Só a areia aumenta; o cimento e a cal não mudam.
# Decidido com o engenheiro em Oct 27, 2026 (ele confirmou que a massa precisava de mais material
# e que o cimento do reboco, uns 2,7 kg/m² em 2 cm, já estava certo). 1,25 = 25% a mais.
COEF_INCHAMENTO_AREIA = 1.25


def consumo_concreto_por_m3(traco: str):
    """Materiais para 1 m3 de concreto no traço informado.

    Retorna None se o traço não existir.
    """
    partes = TRACOS_CONCRETO.get(traco)
    if partes is None:
        return None

    total_partes = partes["cimento"] + partes["areia"] + partes["pedra"]
    vol_cimento = FATOR_VOLUME_APARENTE_CONCRETO * partes["cimento"] / total_partes
    vol_areia = FATOR_VOLUME_APARENTE_CONCRETO * partes["areia"] / total_partes
    vol_pedra = FATOR_VOLUME_APARENTE_CONCRETO * partes["pedra"] / total_partes

    return {
        "sacos_cimento": vol_cimento * DENSIDADE_CIMENTO / SACO_CIMENTO_KG,
        "areia_m3": vol_areia,
        "pedra_m3": vol_pedra,
    }


def materiais_da_massa(volume_m3: float, traco: str):
    """Cimento (kg), cal (kg) e areia (m3) para um volume de massa no traço informado.

    Mesma conta usada no app antigo: as partes do traço dividem o volume da massa.
    A areia ganha o inchamento (COEF_INCHAMENTO_AREIA).
    Retorna None se o traço não existir.
    """
    partes = TRACOS_MASSA.get(traco)
    if partes is None:
        return None
    total = partes["cimento"] + partes["cal"] + partes["areia"]
    return {
        "cimento_kg": volume_m3 * partes["cimento"] / total * DENSIDADE_CIMENTO,
        "cal_kg": volume_m3 * partes["cal"] / total * DENSIDADE_CAL,
        "areia_m3": volume_m3 * partes["areia"] / total * COEF_INCHAMENTO_AREIA,
    }