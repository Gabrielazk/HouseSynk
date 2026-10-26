"""Conversão de unidades: a camada de entrada e saída da versão EUA.

Regra 5 da especificação: as contas são sempre feitas em métrico, por dentro.
Este arquivo só traduz os números:
- entrada: o que a pessoa digitou em ft, in, sq ft... vira m, cm, m²... antes da conta;
- saída: o resultado da conta (em métrico) vira ft, sq ft, cu yd... para mostrar na tela.

Também lê o número digitado (ler_numero), aceitando decimal e fração (1/8, 2 1/2),
porque nos EUA as medidas em polegadas costumam ser escritas em fração.

Não tem nada de tela aqui (igual aos outros arquivos de src/calculators).
Quem decide se o sistema é métrico ou imperial é a tela, pelo país escolhido.
"""
import re

METRICO = "metrico"    # Brasil
IMPERIAL = "imperial"  # EUA

# Cada tipo de medida: (unidade métrica, unidade americana, quanto 1 unidade americana vale em métrico).
# Todos os fatores são exatos (definição oficial), não aproximados.
UNIDADES = {
    "comprimento": ("m", "ft", 0.3048),            # 1 ft = 0,3048 m
    "centimetro": ("cm", "in", 2.54),              # 1 in = 2,54 cm
    "milimetro": ("mm", "in", 25.4),               # 1 in = 25,4 mm
    "area": ("m²", "sq ft", 0.09290304),           # 1 sq ft = 0,3048 x 0,3048 m²
    "volume": ("m³", "cu yd", 0.764554857984),     # 1 cu yd = (3 x 0,3048)³ m³
    "peso": ("kg", "lb", 0.45359237),              # 1 lb = 0,45359237 kg
    "litro": ("L", "gal", 3.785411784),            # 1 galão americano = 3,785411784 L
}

# Fração: "1/8", "2 1/2" ou "2-1/2" (a parte inteira é opcional)
_FRACAO = re.compile(r"(?:(\d+)[\s-]+)?(\d+)\s*/\s*(\d+)")
# Milhar no jeito americano: "1,500" ou "12,000.5" (vírgula seguida de grupos de 3 dígitos)
_MILHAR_EUA = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?")


def para_metrico(valor, tipo, sistema):
    """Entrada: converte o número digitado para métrico (ex.: 10 ft -> 3,048 m).
    No Brasil (métrico), devolve o mesmo número."""
    if sistema != IMPERIAL:
        return valor
    return valor * UNIDADES[tipo][2]


def do_metrico(valor, tipo, sistema):
    """Saída: converte o resultado (em métrico) para mostrar na tela (ex.: 3,048 m -> 10 ft).
    No Brasil (métrico), devolve o mesmo número."""
    if sistema != IMPERIAL:
        return valor
    return valor / UNIDADES[tipo][2]


def nome_unidade(tipo, sistema):
    """O nome da unidade para mostrar na tela (ex.: "m" no Brasil, "ft" nos EUA)."""
    metrica, americana, _ = UNIDADES[tipo]
    return americana if sistema == IMPERIAL else metrica


def ler_numero(texto, separador_decimal=",", padrao=0.0):
    """Lê o número que a pessoa digitou. Aceita:
    - decimal: "2,5" ou "2.5"
    - fração: "1/8", "2 1/2" ou "2-1/2"
    Nos EUA (separador "."), "1,500" é mil e quinhentos; mas "2,5" continua sendo 2,5
    (para quem mora nos EUA e escreve do jeito brasileiro).
    No Brasil, fica como sempre foi: vírgula ou ponto viram decimal.
    Campo vazio devolve o padrão. Texto inválido dá ValueError (as telas já tratam esse erro)."""
    texto = (texto or "").strip()
    if not texto:
        return padrao

    if separador_decimal == "." and _MILHAR_EUA.fullmatch(texto):
        texto = texto.replace(",", "")     # "1,500" -> "1500"
    else:
        texto = texto.replace(",", ".")    # "2,5" -> "2.5"

    if "/" not in texto:
        return float(texto)

    partes = _FRACAO.fullmatch(texto)
    if not partes:
        raise ValueError(f"Número inválido: {texto}")
    inteiro, numerador, denominador = partes.groups()
    if int(denominador) == 0:
        raise ValueError(f"Número inválido: {texto}")
    return int(inteiro or 0) + int(numerador) / int(denominador)


if __name__ == "__main__":
    # Teste rápido: dentro da pasta Calculadora, rode
    #   py -m src.calculators.unidades
    print("10 ft em metros:", round(para_metrico(10, "comprimento", IMPERIAL), 4))   # 3.048
    print("1 m³ em cu yd:", round(do_metrico(1, "volume", IMPERIAL), 3))             # 1.308
    print("50 kg em lb:", round(do_metrico(50, "peso", IMPERIAL), 2))                # 110.23
    print("Brasil não muda (5 m):", para_metrico(5, "comprimento", METRICO))         # 5
    print("Unidades:", nome_unidade("area", METRICO), "/", nome_unidade("area", IMPERIAL))  # m² / sq ft
    print("1/8:", ler_numero("1/8", "."))            # 0.125
    print("2 1/2:", ler_numero("2 1/2", "."))        # 2.5
    print("2-1/2:", ler_numero("2-1/2", "."))        # 2.5
    print("0,125 (Brasil):", ler_numero("0,125"))    # 0.125
    print("1,500 (EUA):", ler_numero("1,500", "."))  # 1500.0
    print("2,5 (EUA):", ler_numero("2,5", "."))      # 2.5
    print("Vazio:", ler_numero(""))                  # 0.0
    try:
        ler_numero("abc")
    except ValueError:
        print("abc: dá erro, como esperado")