"""Reserva para imprevistos: um valor a mais sobre o total da obra, conforme o perfil escolhido.

Aparece sempre como linha separada no Resumo e no PDF, nunca misturada nos materiais.
"""

# Perfis da obra e o percentual de reserva de cada um (ordem em que aparecem na tela)
PERFIS_RESERVA = ["nenhuma", "tranquila", "antiga"]
PERCENTUAL_RESERVA = {"nenhuma": 0.0, "tranquila": 10.0, "antiga": 15.0}
PERFIL_RESERVA_PADRAO = "nenhuma"


def calcular_reserva(total_obra: float, perfil: str) -> float:
    """Valor da reserva em dinheiro (0 se o perfil for 'nenhuma' ou não existir)."""
    return round(total_obra * PERCENTUAL_RESERVA.get(perfil, 0.0) / 100.0, 2)