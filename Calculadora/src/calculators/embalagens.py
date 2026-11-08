"""Quantas embalagens comprar: a conta é a mesma para tinta, impermeabilizante e rejunte.

Toda embalagem do app vem em dois tamanhos (um grande e um pequeno), nos dois países:
- tinta e impermeabilizante: lata de 18 L + galão de 3,6 L (Brasil); balde de 5 gal + galão de 1 gal (EUA)
- rejunte: lata de 2 kg + lata de 1 kg (Brasil); saco de 25 lb + caixa de 7 lb (EUA)

A regra é "do jeito que sobra menos": leva o máximo de embalagens grandes e completa com
pequenas. Se as pequenas somarem o mesmo que uma grande (ou mais), troca por mais uma grande.
No Brasil isso dá exatamente o mesmo resultado de antes (ex.: 5 galões de 3,6 L viram 1 lata).

Não tem nada de tela aqui (igual aos outros arquivos de src/calculators).
"""
import math


def grandes_e_pequenas(quantidade, grande, pequena=None):
    """Quantas embalagens grandes e pequenas comprar para a quantidade pedida.
    quantidade, grande e pequena na mesma unidade (litros ou kg).
    pequena=None: o produto só tem um tamanho (ex.: rejunte sem areia, caixa de 10 lb)."""
    if quantidade <= 1e-9:
        return 0, 0
    if pequena is None:
        return math.ceil(quantidade / grande - 1e-9), 0

    grandes = int((quantidade + 1e-9) // grande)
    resto = quantidade - grandes * grande
    pequenas = math.ceil(resto / pequena - 1e-9) if resto > 1e-9 else 0
    if pequenas * pequena >= grande - 1e-9:  # as pequenas já dão uma grande: leva a grande
        grandes += 1
        pequenas = 0
    return grandes, pequenas


if __name__ == "__main__":
    # Teste rápido: dentro da pasta do app (a que tem o main.py), rode
    #   py -m src.calculators.embalagens
    print("20 L em latas de 18 L e galões de 3,6 L:", grandes_e_pequenas(20, 18, 3.6))   # (1, 1)
    print("34 L:", grandes_e_pequenas(34, 18, 3.6))                                      # (2, 0): 5 galões viram 1 lata
    print("5 kg de rejunte em latas de 2 kg e 1 kg:", grandes_e_pequenas(5, 2, 1))        # (2, 1)
    print("10 lb (4,54 kg) em caixas de 10 lb:", grandes_e_pequenas(4.54, 4.5359237))    # (1, 0)