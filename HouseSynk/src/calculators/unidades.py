"""Conversão de unidades: a camada de entrada e saída da versão EUA.

Regra 5 da especificação: as contas são sempre feitas em métrico, por dentro.
Este arquivo só traduz os números:
- entrada: o que a pessoa digitou em ft, in, sq ft... vira m, cm, m²... antes da conta;
- saída: o resultado da conta (em métrico) vira ft, sq ft, cu yd... para mostrar na tela.

Também lê o número digitado (ler_numero), aceitando decimal e fração (1/8, 2 1/2),
e escreve polegadas em fração (texto_polegadas), porque nos EUA as medidas em
polegadas costumam ser escritas assim.

Não tem nada de tela aqui (igual aos outros arquivos de src/calculators).
Quem decide se o sistema é métrico ou imperial é a tela, pelo país escolhido.
"""
import math
import re
from decimal import Decimal, ROUND_HALF_UP

METRICO = "metrico"    # Brasil
IMPERIAL = "imperial"  # EUA

# Fatores exatos usados também nas embalagens americanas (saco de 50 lb, balde de 5 gal...)
KG_POR_LB = 0.45359237        # 1 lb = 0,45359237 kg
L_POR_GAL = 3.785411784       # 1 galão americano = 3,785411784 L
M2_POR_SQFT = 0.09290304      # 1 sq ft = 0,3048 x 0,3048 m²

# Cada tipo de medida: (unidade métrica, unidade americana, quanto 1 unidade americana vale em métrico).
# Todos os fatores são exatos (definição oficial), não aproximados.
UNIDADES = {
    "comprimento": ("m", "ft", 0.3048),            # 1 ft = 0,3048 m
    "centimetro": ("cm", "in", 2.54),              # 1 in = 2,54 cm
    "milimetro": ("mm", "in", 25.4),               # 1 in = 25,4 mm
    "area": ("m²", "sq ft", M2_POR_SQFT),
    "volume": ("m³", "cu yd", 0.764554857984),     # 1 cu yd = (3 x 0,3048)³ m³
    "peso": ("kg", "lb", KG_POR_LB),
    "litro": ("L", "gal", L_POR_GAL),
    # Rendimento da tinta: 1 sq ft/gal = 0,09290304 m² / 3,785411784 L
    "rendimento": ("m²/L", "sq ft/gal", M2_POR_SQFT / L_POR_GAL),
    # Consumo por área (rejunte, argamassa): 1 lb/sq ft = 0,45359237 kg / 0,09290304 m²
    "consumo": ("kg/m²", "lb/sq ft", KG_POR_LB / M2_POR_SQFT),
    # Preço por comprimento (mão de obra): $ 1 por ft = $ 3,28 por m (1 m tem 1/0,3048 ft)
    "preco_comprimento": ("/m", "/ft", 1 / 0.3048),
}

# Fração: "1/8", "2 1/2" ou "2-1/2" (a parte inteira é opcional)
_FRACAO = re.compile(r"(?:(\d+)[\s-]+)?(\d+)\s*/\s*(\d+)")
# Milhar no jeito americano: "1,500" ou "12,000.5" (vírgula seguida de grupos de 3 dígitos)
_MILHAR_EUA = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?")


def arredondar(valor, casas=0):
    """Arredonda do jeito da escola (5 sobe): 1,575 -> 1,58 e 215,25 -> 215,3.

    O round() do Python erra nesses casos: o computador guarda 1,575 como 1,57499999...,
    e o round() arredonda para baixo (1,57). Aqui, o round(valor, 9) primeiro tira esse
    "lixo" do fim do número, e o Decimal faz o arredondamento certo (ROUND_HALF_UP)."""
    numero = Decimal(str(round(float(valor), 9)))
    return float(numero.quantize(Decimal(1).scaleb(-casas), rounding=ROUND_HALF_UP))


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
    Número inteiro + fração: a fração tem que ser menor que 1 ("2 1/2" vale; "1 21/2" é
    erro de digitação, porque ninguém escreve assim). Fração sozinha pode ser maior ("21/2" = 10,5).
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
    if inteiro is not None and int(numerador) >= int(denominador):
        raise ValueError(f"Número inválido: {texto}")  # ex.: "1 21/2" ou "2 2/2"
    return int(inteiro or 0) + int(numerador) / int(denominador)


def texto_polegadas(valor, aproximar=False, divisao=16):
    """Escreve polegadas do jeito americano: 0.375 -> "3/8", 1.5 -> "1 1/2", 12.0 -> "12".
    divisao: o menor pedaço usado (16 = até 1/16 in, 8 = até 1/8 in).
    aproximar=True: arredonda para o pedaço mais próximo (usado nos valores que já vêm preenchidos).
    aproximar=False: só vira fração se o número for exatamente um múltiplo do pedaço;
    se não for, fica em decimal (ex.: 5.906), para não mudar o que a pessoa digitou."""
    pedacos = round(valor * divisao)
    if not aproximar and abs(valor * divisao - pedacos) > 0.01:
        return f"{round(valor, 3):g}"
    inteiro, resto = divmod(pedacos, divisao)
    if resto == 0:
        return str(inteiro)
    divisor = math.gcd(resto, divisao)
    fracao = f"{resto // divisor}/{divisao // divisor}"
    return f"{inteiro} {fracao}" if inteiro else fracao


if __name__ == "__main__":
    # Teste rápido: dentro da pasta do app (a que tem o main.py), rode
    #   py -m src.calculators.unidades
    print("10 ft em metros:", round(para_metrico(10, "comprimento", IMPERIAL), 4))   # 3.048
    print("1 m³ em cu yd:", round(do_metrico(1, "volume", IMPERIAL), 3))             # 1.308
    print("50 kg em lb:", round(do_metrico(50, "peso", IMPERIAL), 2))                # 110.23
    print("Brasil não muda (5 m):", para_metrico(5, "comprimento", METRICO))         # 5
    print("Unidades:", nome_unidade("area", METRICO), "/", nome_unidade("area", IMPERIAL))  # m² / sq ft
    print("1/8:", ler_numero("1/8", "."))            # 0.125
    print("2 1/2:", ler_numero("2 1/2", "."))        # 2.5
    print("2-1/2:", ler_numero("2-1/2", "."))        # 2.5
    print("21/2:", ler_numero("21/2", "."))          # 10.5 (fração sozinha pode ser maior que 1)
    print("0,125 (Brasil):", ler_numero("0,125"))    # 0.125
    print("1,500 (EUA):", ler_numero("1,500", "."))  # 1500.0
    print("2,5 (EUA):", ler_numero("2,5", "."))      # 2.5
    print("Vazio:", ler_numero(""))                  # 0.0
    for errado in ("abc", "1-21/2", "1 21/2", "2 2/2"):
        try:
            ler_numero(errado)
        except ValueError:
            print(f"{errado}: dá erro, como esperado")
    print("400 sq ft/gal em m²/L:", round(para_metrico(400, "rendimento", IMPERIAL), 2))     # 9.82
    print("3,5 kg/m² em lb/sq ft:", round(do_metrico(3.5, "consumo", IMPERIAL), 3))          # 0.717
    print("$ 8 por ft em $ por m:", round(para_metrico(8, "preco_comprimento", IMPERIAL), 2))  # 26.25
    print("0.375 in:", texto_polegadas(0.375))                   # 3/8
    print("1.5 in:", texto_polegadas(1.5))                       # 1 1/2
    print("12 in:", texto_polegadas(12.0))                       # 12
    print("5.906 in (sem aproximar):", texto_polegadas(5.906))   # 5.906
    print("1 cm em in (aproximando):", texto_polegadas(do_metrico(1, "centimetro", IMPERIAL), aproximar=True))  # 3/8
    print("1/16 in:", texto_polegadas(0.0625))                   # 1/16
    print("8 mm em in (aproximando):", texto_polegadas(do_metrico(8, "milimetro", IMPERIAL), aproximar=True))  # 5/16