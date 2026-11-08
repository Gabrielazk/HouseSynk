# Testes da Rodada 3 (EUA, português): Piso, Azulejo, Rejunte, Pintura e Baldrame (impermeabilização)

Criado em 05/11/2026. **Rodada fechada em 06/11/2026:** as 9 pendências (P1 a P9) foram corrigidas, os 162 casos deram OK no rodada3.py e a Gabi conferiu o visual no app. O esperado completo agora fica dentro do rodada3.py (ESPERADO) e entra no pytest pelo tests\rodadas\test_rodada3.py. **A versão principal fica no PC da Gabi** (testes_manuais\testes_rodada3.md, na pasta do app).

Todos os resultados abaixo foram tirados rodando o código real (o mesmo caminho do botão Calcular), com o país trocado pelo próprio `alternar_pais` das Configurações (EUA, estado NY, `$`, ponto decimal e preços dos EUA) e o app em português. **O esperado é o que o app DEVE mostrar** (decisão da Gabi, 05/11/2026): durante a rodada, os casos das pendências ficaram marcados com ⚠️ e davam DIFERENTE até a correção (as marcas foram tiradas no fechamento, em 06/11/2026). Antes de montar este arquivo, o Leo aplicou as correções propostas numa cópia do código, fora do PC, só para tirar os números: com elas, o rodada1.py e o rodada2.py continuaram com 353 OK cada (o Brasil não muda).

## Antes de começar

1. Rode o pytest: tem que dar **1055 passed** (893 antes do fechamento da rodada 3).
2. No app: **Configurações** → botão **País** até aparecer **"País: EUA ($)"** (o estado vira NY). O idioma continua **Português**.
3. Dê **Limpar** antes de cada teste.
4. Se no fim quiser voltar para o Brasil: Configurações → País → **BR (R$)**. (Cuidado: ao voltar, o cimento fica R$ 32 e a brita R$ 95, e não R$ 36 e R$ 120; é o problema conhecido do passo de preços. Para as rodadas 1 e 2 no app, feche e abra o app de novo.)

## O que olhar em toda aba (foco da rodada 3)

- **Medidas digitadas em ft, in e sq ft** convertem certo, inclusive com fração ("2 1/2", "3/8", "11 3/4") e com o milhar americano ("1,500" = mil e quinhentos; "2,5" continua 2.5).
- **Números com ponto e milhar com vírgula:** "1,000.00 sq ft", "$ 2,197.16". Nenhuma vírgula decimal e nenhum "R$".
- **Embalagens americanas:** sacos de 50 lb (thinset), caixas de 10 lb, sacos de 25 lb e caixas de 7 lb (rejunte), baldes de 5 gal e galões de 1 gal (tinta, primer e impermeabilizante).
- **Nenhum texto do Brasil** nas 5 abas: m, cm, mm, m², kg, L, "lata", "AC-I", vírgula decimal. Única exceção: o concreto e o ferro do Baldrame (Parte 2).
- **Polegadas em fração:** "12 x 12 in", "1/8 in", "5/16 in", "11 3/4 x 12 in" (nunca "11.75" nem "0.031").
- **Avisos de limite** com as unidades dos EUA: "Área de 21,529 sq ft: o limite é 21,528 sq ft.", "Junta de 5/8 in: o normal é de 1/16 in a 9/16 in.".
- **"?"** de cada aba com a legenda das siglas no fim (só em português).
- O que já valia nas rodadas 1 e 2 continua: Limpar, Anterior, Próximo, Finalizar, tema claro e escuro, barra de rolagem, número e unidade sem quebra de linha.

**Não é erro nesta rodada:**
- No Baldrame, o concreto e o ferro saem em m³, sacos de 50 kg, kg e barras de 12 m (Parte 2 da versão EUA).
- Os preços são os provisórios (muitos são os do Brasil, só que em dólar, ex.: piso $ 50 por m², rodapé $ 15 por m). Confere-se só a quantidade e se o custo é a quantidade vezes o preço.
- Nas outras 9 abas, os resultados ainda saem em métrico.

## Pendências achadas ao montar este roteiro (o esperado já é o certo)

**Todas corrigidas em 06/11/2026**, em 4 partes (textos; Piso, Azulejo e Rejunte; Baldrame; Pintura). Junto entrou a **P10**, pedida pela Gabi: "ANSI A118.4" e as medidas com fração ("11 3/4 x 12 in") nunca quebram a linha no meio.

| # | O que é | Abas | O certo (já no esperado) |
|---|---|---|---|
| P1 | O custo das peças (e do rodapé) usa a área com perda **arredondada em m²**: 473 sq ft dá $ 2,197.00, e o certo é 473 sq ft = 43,943 m² × $ 50 = **$ 2,197.16**. Com área pequena erra mais (2.75 sq ft: $ 13.00 em vez de **$ 12.77**). | Piso, Azulejo | Custo = área com perda, sem arredondar, × preço. Continua cobrando pela área com perda (como no Brasil, aprovado nas rodadas 1 e 2), e não pelas caixas inteiras: cobrar por caixa mudaria o Brasil e fica para o passo da tabela de preços. |
| P2 | O "?" diz "10% até 28 in, 15% até 35 in", mas 28 in = 71,12 cm já dá 15%. | Piso, Azulejo (e o inglês, rodada 4) | Muda só o texto (a regra é do engenheiro, em cm): **"até 27 1/2 in"** (69,85 cm → 10%) e **"até 35 3/8 in"** (89,85 cm → 15%); 27 9/16 in (70,01 cm) já dá 15% e 35 7/16 in (90,01 cm) dá 20%. E o exemplo "(ex.: 12 x 12 in)". Visual, mais os casos PI-C24 a PI-C27. |
| P3 | Com a espessura **apagada**, o app usa 8 mm e mostra "0.315 in", e o campo vinha com 5/16 in. | Rejunte | Vazio = **5/16 in**, o mesmo número que o campo mostra (caso RJ-C18 = igual ao Teste B). |
| P4 | Viga de 7 7/8 x 11 7/8 in não dá aviso, mas o aviso diz que o mínimo é 8 in e 12 in. | Baldrame | Compara com o número mostrado no aviso (igual às outras abas, regra 12): 7 7/8 in **dá** aviso. |
| P5 | O custo do impermeabilizante usa os litros das embalagens compradas **arredondados** (3 galões = 11,356 L viram 11,4 L): $ 25.33. | Baldrame | O app já cobra pelos litros das embalagens compradas (o que a especificação pede): 3 galões de 1 gal = 11,356 L. Só não pode arredondar antes: **$ 25.23**. Um balde sozinho dá exatamente o preço da pesquisa, **$ 39.95** (hoje $ 39.99). |
| P6 | Você digita em ft e in e o app devolve em m e cm: "Mão de Obra: 12.2 m" e "Estribos 5 mm c/ 20.32 cm". | Baldrame | **"Mão de Obra: 40.0 ft ($ 320.00)"** e **"Estribos 5 mm c/ 8 in"**. |
| P7 | Visual das polegadas: "12x12 in" grudado; "11 3/4x12 in"; o botão do Rejunte em decimal ("11.75"); junta de 1/32 aparece "0.031 in". | Piso, Azulejo, Rejunte | **"12 x 12 in"**, **"11 3/4 x 12 in"** (com espaço, só nos EUA; o Brasil continua "60x60 cm"); botão e campos em fração ("11 3/4 x 11 3/4 in"); junta e espessura em fração até **1/32 in** (a opção mais simples: as medidas em mm passam a usar frações de 1/32, e 2/32 continua aparecendo 1/16). |
| P8 | Rendimento 12 (o costume do Brasil, em m²/L) é aceito como 12 sq ft/gal sem aviso e dá 183 gal de tinta. | Pintura | Limite novo com aviso (regra 12), criado pelo Leo (o engenheiro ainda vai conferir): **EUA de 150 a 800 sq ft/gal; Brasil de 4 a 20 m²/L**. Texto: "Rendimento de {valor}: o normal é de {min} a {max}." / "Coverage of {valor}: the usual is {min} to {max}.". **Não muda nenhum caso das rodadas 1 e 2** (os rendimentos delas são 10, 12 e 12,5 m²/L; o Leo conferiu: 353 OK nas duas). |
| P9 | O "?" do Baldrame diz "4,75 gal" (com vírgula). | Baldrame | **"4.75 gal"**. Visual. |

Fora das 5 abas (anotado para a Parte 2): as Brocas, nos EUA, também mostram a mão de obra em m e o estribo em cm.

---

# PISO

**43 casos.** Todos OK (os 31 das pendências P1 e P7 foram corrigidos em 06/11/2026).

**Como aparece** (confira se nenhuma dica fica cortada):

- Dimensões (Obrigatório)
- Área do piso em sq ft (ex: 430)
- Largura da peça em in (ex: 12)
- Altura da peça em in (ex: 12)
- sq ft por caixa (opcional, ex: 15)
- Assentamento com desenho, diagonal ou paginado (Opcional): Sim · Não
- Perda % (opcional; vazio = automática)
- Tipo de argamassa colante (thinset) (Opcional): Não modificada (ANSI A118.1) · Modificada (ANSI A118.4)
- Rodapé em ft (opcional, ex: 65)
- Peça do rodapé em ft (opcional, ex: 8)
- Com o Contrapiso preenchido (ex.: 430), aparece o botão "Usar a área do Contrapiso: 430 sq ft".

## Teste A: todos os campos, opcionais trocados

#### PI-A

Digite: Área **430**; Largura da peça **24**; Altura da peça **24**; sq ft por caixa **15.5**; Perda **12**; Rodapé **65**; Peça do rodapé **8**; Assentamento com desenho **Sim**; Argamassa **Modificada (ANSI A118.4)**.

```
Área: 430.00 sq ft
Área com perda (12%): 481.60 sq ft
Peça: 24 x 24 in
Assentamento: com desenho
• Peças: 121
• Caixas: 32 (15.50 sq ft por caixa) ($ 2,237.11)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 13 sacos de 50 lb (602.1 lb) ($ 233.74)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft
• Rodapé: 72.80 ft (10 peças de 8.00 ft) ($ 332.84)

Custo Estimado da Etapa: $ 2,803.69
```

Pra entender: A perda digitada (12) vale mesmo com desenho Sim (o 25% só entra com a perda vazia). 430 × 1,12 = 481,6 sq ft; a peça de 24 x 24 in tem 4 sq ft → 120,4 → **121 peças**; 481,6 ÷ 15,5 = 31,07 → **32 caixas**. Argamassa: a peça passa de 16 in, então desempenadeira 1/2 x 1/2 in, que rende 40 sq ft por saco: 481,6 ÷ 40 = 12,04 → **13 sacos** (602,1 lb). Rodapé: 65 × 1,12 = 72,8 ft ÷ 8 = 9,1 → **10 peças**. Custo das peças: 481,6 sq ft = 44,74 m² × $ 50 (preço provisório por m²) = **$ 2,237.11**.

## Teste B: só os obrigatórios (e variações)

#### PI-B

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**.

```
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 12 x 12 in
• Peças: 473 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.2 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,373.16
```

Pra entender: 430 × 1,10 = 473 sq ft; a peça de 12 x 12 in tem 1 sq ft → **473 peças**. A peça tem até 16 in: desempenadeira 1/4 x 3/8 in, 60 sq ft por saco de 50 lb → 473 ÷ 60 = 7,88 → **8 sacos** (473 × 50 ÷ 60 = 394,2 lb). Custo das peças: 473 sq ft = 43,94 m² × $ 50 = **$ 2,197.16** (hoje o app mostra $ 2,197.00: é a pendência P1). Argamassa: 8 × $ 22.00 = $ 176.00.

#### PI-B2

Digite: Área **430**; Largura da peça **6**; Altura da peça **6**.

```
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 6 x 6 in
• Peças: 1,892 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 6 sacos de 50 lb (278.2 lb) ($ 132.00)
  Desempenadeira: 1/4 x 1/4 in · Consumo: 0.588 lb/sq ft

Custo Estimado da Etapa: $ 2,329.16
```

#### PI-B3

Digite: Área **430**; Largura da peça **12**; Altura da peça **24**.

```
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 12 x 24 in
• Peças: 237 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 12 sacos de 50 lb (591.3 lb) ($ 264.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 2,461.16
```

#### PI-B4

Digite: Área **430**; Largura da peça **24**; Altura da peça **24**.

```
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 24 x 24 in
• Peças: 119 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 12 sacos de 50 lb (591.3 lb) ($ 264.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 2,461.16
```

#### PI-B5

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Assentamento com desenho **Sim**.

```
Área: 430.00 sq ft
Área com perda (25%, automática): 537.50 sq ft
Peça: 12 x 12 in
Assentamento: com desenho
• Peças: 538 ($ 2,496.77)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 9 sacos de 50 lb (448.0 lb) ($ 198.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,694.77
```

#### PI-B6

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; sq ft por caixa **15.5**.

```
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 12 x 12 in
• Peças: 473
• Caixas: 31 (15.50 sq ft por caixa) ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.2 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,373.16
```

#### PI-B7

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Rodapé **65**.

```
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 12 x 12 in
• Peças: 473 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.2 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft
• Rodapé: 71.50 ft ($ 326.90)

Custo Estimado da Etapa: $ 2,700.05
```

#### PI-B8

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Rodapé **65**; Peça do rodapé **8**.

```
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 12 x 12 in
• Peças: 473 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.2 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft
• Rodapé: 71.50 ft (9 peças de 8.00 ft) ($ 326.90)

Custo Estimado da Etapa: $ 2,700.05
```

#### PI-B9

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Argamassa **Modificada (ANSI A118.4)**.

```
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 12 x 12 in
• Peças: 473 ($ 2,197.16)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 8 sacos de 50 lb (394.2 lb) ($ 143.84)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,341.00
```

## Teste C: erros de digitação e limites

#### PI-C1

Digite: Área **(vazio)**; Largura da peça **12**; Altura da peça **12**.

```
Por favor, digite números válidos nos campos!
```

#### PI-C2

Digite: Área **430**; Largura da peça **(vazio)**; Altura da peça **12**.

```
Por favor, digite números válidos nos campos!
```

#### PI-C3

Digite: Área **quatrocentos**; Largura da peça **12**; Altura da peça **12**.

```
Por favor, digite números válidos nos campos!
```

#### PI-C4

Digite: Área **0**; Largura da peça **12**; Altura da peça **12**.

```
Erro: Área e tamanho da peça devem ser maiores que zero.
```

#### PI-C5

Digite: Área **-430**; Largura da peça **12**; Altura da peça **12**.

```
Erro: Área e tamanho da peça devem ser maiores que zero.
```

#### PI-C6

Digite: Área **430**; Largura da peça **0**; Altura da peça **12**.

```
Erro: Área e tamanho da peça devem ser maiores que zero.
```

#### PI-C7

Digite: Área **430,5**; Largura da peça **12**; Altura da peça **12**.

```
Área: 430.50 sq ft
Área com perda (10%, automática): 473.55 sq ft
Peça: 12 x 12 in
• Peças: 474 ($ 2,199.71)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.6 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,375.71
```

#### PI-C8

Digite: Área **430.5**; Largura da peça **12**; Altura da peça **12**.

```
Área: 430.50 sq ft
Área com perda (10%, automática): 473.55 sq ft
Peça: 12 x 12 in
• Peças: 474 ($ 2,199.71)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.6 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,375.71
```

#### PI-C9

Digite: Área **430 1/2**; Largura da peça **12**; Altura da peça **12**.

```
Área: 430.50 sq ft
Área com perda (10%, automática): 473.55 sq ft
Peça: 12 x 12 in
• Peças: 474 ($ 2,199.71)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.6 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,375.71
```

#### PI-C10

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Perda **-5**.

```
Erro: A perda não pode ser negativa.
```

#### PI-C11

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Perda **2.5**.

```
Área: 430.00 sq ft
Área com perda (2.5%): 440.75 sq ft
Peça: 12 x 12 in
• Peças: 441 ($ 2,047.35)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (367.3 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,223.35
```

#### PI-C12

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Perda **0**.

```
Área: 430.00 sq ft
Área com perda (0%): 430.00 sq ft
Peça: 12 x 12 in
• Peças: 430 ($ 1,997.42)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (358.3 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,173.42
```

#### PI-C13

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; sq ft por caixa **-15**.

```
Erro: Os valores não podem ser negativos.
```

#### PI-C14

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Rodapé **-65**.

```
Erro: Os valores não podem ser negativos.
```

#### PI-C15

Digite: Área **1 21/2**; Largura da peça **12**; Altura da peça **12**.

```
Por favor, digite números válidos nos campos!
```

#### PI-C16

Digite: Área **1-21/2**; Largura da peça **12**; Altura da peça **12**.

```
Por favor, digite números válidos nos campos!
```

#### PI-C17

Digite: Área **1,500**; Largura da peça **12**; Altura da peça **12**.

```
Área: 1,500.00 sq ft
Área com perda (10%, automática): 1,650.00 sq ft
Peça: 12 x 12 in
• Peças: 1,650 ($ 7,664.50)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 28 sacos de 50 lb (1,375.0 lb) ($ 616.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 8,280.50
```

#### PI-C18

Digite: Área **2,5**; Largura da peça **12**; Altura da peça **12**.

```
Área: 2.50 sq ft
Área com perda (10%, automática): 2.75 sq ft
Peça: 12 x 12 in
• Peças: 3 ($ 12.77)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 1 saco de 50 lb (2.2 lb) ($ 22.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 34.77
```

#### PI-C19

Digite: Área **430**; Largura da peça **11 3/4**; Altura da peça **12**.

```
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 11 3/4 x 12 in
• Peças: 484 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.2 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,373.16
```

#### PI-C20

Digite: Área **430**; Largura da peça **8**; Altura da peça **8**.

```
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 8 x 8 in
• Peças: 1,065 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 6 sacos de 50 lb (278.2 lb) ($ 132.00)
  Desempenadeira: 1/4 x 1/4 in · Consumo: 0.588 lb/sq ft

Custo Estimado da Etapa: $ 2,329.16
```

#### PI-C21

Digite: Área **430**; Largura da peça **8 1/16**; Altura da peça **8**.

```
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 8 1/16 x 8 in
• Peças: 1,056 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.2 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,373.16
```

#### PI-C22

Digite: Área **430**; Largura da peça **16**; Altura da peça **16**.

```
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 16 x 16 in
• Peças: 267 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.2 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,373.16
```

#### PI-C23

Digite: Área **430**; Largura da peça **16 1/8**; Altura da peça **16**.

```
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 16 1/8 x 16 in
• Peças: 264 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 12 sacos de 50 lb (591.3 lb) ($ 264.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 2,461.16
```

#### PI-C24

Digite: Área **430**; Largura da peça **27 1/2**; Altura da peça **27 1/2**.

```
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 27 1/2 x 27 1/2 in
• Peças: 91 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 12 sacos de 50 lb (591.3 lb) ($ 264.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 2,461.16
```

#### PI-C25

Digite: Área **430**; Largura da peça **27 9/16**; Altura da peça **27 9/16**.

```
Área: 430.00 sq ft
Área com perda (15%, automática): 494.50 sq ft
Peça: 27 9/16 x 27 9/16 in
• Peças: 94 ($ 2,297.03)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 13 sacos de 50 lb (618.2 lb) ($ 286.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 2,583.03
```

#### PI-C26

Digite: Área **430**; Largura da peça **35 3/8**; Altura da peça **35 3/8**.

```
Área: 430.00 sq ft
Área com perda (15%, automática): 494.50 sq ft
Peça: 35 3/8 x 35 3/8 in
• Peças: 57 ($ 2,297.03)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 13 sacos de 50 lb (618.2 lb) ($ 286.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 2,583.03
```

#### PI-C27

Digite: Área **430**; Largura da peça **35 7/16**; Altura da peça **35 7/16**.

```
Área: 430.00 sq ft
Área com perda (20%, automática): 516.00 sq ft
Peça: 35 7/16 x 35 7/16 in
• Peças: 60 ($ 2,396.90)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 13 sacos de 50 lb (645.1 lb) ($ 286.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 2,682.90
```

#### PI-C28

Digite: Área **21528**; Largura da peça **12**; Altura da peça **12**.

```
Área: 21,528.00 sq ft
Área com perda (10%, automática): 23,680.80 sq ft
Peça: 12 x 12 in
• Peças: 23,681 ($ 110,000.92)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 395 sacos de 50 lb (19,734.0 lb) ($ 8,690.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 118,690.92
```

#### PI-C29-cancelar

Digite: Área **21529**; Largura da peça **12**; Altura da peça **12**. Na janela, toque em **Cancelar**.

```
[JANELA] Área de 21,529 sq ft: o limite é 21,528 sq ft.
[Cancelar] não calculou
```

#### PI-C29-continuar

Digite: Área **21529**; Largura da peça **12**; Altura da peça **12**. Na janela, toque em **Continuar**.

```
[JANELA] Área de 21,529 sq ft: o limite é 21,528 sq ft.
Área: 21,529.00 sq ft
Área com perda (10%, automática): 23,681.90 sq ft
Peça: 12 x 12 in
• Peças: 23,682 ($ 110,006.03)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 395 sacos de 50 lb (19,734.9 lb) ($ 8,690.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 118,696.03
```

#### PI-C30

Digite: Área **430**; Largura da peça **1**; Altura da peça **1**. Na janela, toque em **Continuar**.

```
[JANELA] Peça de 1 in x 1 in: o normal é de 2 in a 118 in em cada lado.
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 1 x 1 in
• Peças: 68,112 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 6 sacos de 50 lb (278.2 lb) ($ 132.00)
  Desempenadeira: 1/4 x 1/4 in · Consumo: 0.588 lb/sq ft

Custo Estimado da Etapa: $ 2,329.16
```

#### PI-C31

Digite: Área **430**; Largura da peça **120**; Altura da peça **12**. Na janela, toque em **Continuar**.

```
[JANELA] Peça de 120 in x 12 in: o normal é de 2 in a 118 in em cada lado.
Área: 430.00 sq ft
Área com perda (20%, automática): 516.00 sq ft
Peça: 120 x 12 in
• Peças: 52 ($ 2,396.90)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 13 sacos de 50 lb (645.1 lb) ($ 286.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 2,682.90
```

#### PI-C32

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Peça do rodapé **8**.

```
Área: 430.00 sq ft
Área com perda (10%, automática): 473.00 sq ft
Peça: 12 x 12 in
• Peças: 473 ($ 2,197.16)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 8 sacos de 50 lb (394.2 lb) ($ 176.00)
  Desempenadeira: 1/4 x 3/8 in · Consumo: 0.833 lb/sq ft

Custo Estimado da Etapa: $ 2,373.16
```

## Visual (Piso)

- O "?" abre a Ajuda com o texto do Piso, a nota dos valores padrão e, no fim, a legenda: "Siglas: ft = pés · in = polegadas · sq ft = pés quadrados · cu yd = jardas cúbicas · lb = libras · gal = galões".
- **P2:** hoje o "?" diz "10% para peças de até 28 in, 15% até 35 in". O certo (a regra é do engenheiro, em cm: 70 e 90 cm) é **"10% para peças de até 27 1/2 in, 15% até 35 3/8 in e 20% acima disso"**, e o exemplo do começo fica "(ex.: 12 x 12 in)", igual ao resultado. Os casos PI-C24 a PI-C27 conferem esses limites.
- O menu da argamassa mostra os nomes inteiros, sem cortar: "Não modificada (ANSI A118.1)" e "Modificada (ANSI A118.4)".
- Limpar: perda vazia, A118.1, desenho Não, caixa e rodapé vazios.
- Botão "Usar a área do Contrapiso: 430 sq ft" (com o Contrapiso preenchido com 430): toque e a área do Piso fica 430.

---

# AZULEJO

**25 casos.** Todos OK (os 14 das pendências P1 e P7 foram corrigidos em 06/11/2026).

**Como aparece** (confira se nenhuma dica fica cortada):

- Dimensões (Obrigatório)
- Parede a revestir em sq ft (ex: 320)
- Largura da peça em in (ex: 12)
- Altura da peça em in (ex: 12)
- Portas/janelas em sq ft (opcional, ex: 50)
- sq ft por caixa (opcional, ex: 15)
- Assentamento com desenho, diagonal ou paginado (Opcional): Sim · Não
- Perda % (opcional; vazio = automática)
- Tipo de argamassa colante (thinset) (Opcional): já vem **Modificada (ANSI A118.4)**

## Teste A: todos os campos, opcionais trocados

#### AZ-A

Digite: Área **320**; Largura da peça **12**; Altura da peça **24**; Portas/janelas **50**; sq ft por caixa **15.5**; Perda **15**; Assentamento com desenho **Sim**; Argamassa **Não modificada (ANSI A118.1)**.

```
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

Custo Estimado da Etapa: $ 1,329.86
```

Pra entender: 320 − 50 = 270 sq ft × 1,15 = 310,5 sq ft; peça 12 x 24 in = 2 sq ft → 155,25 → **156 peças**; 310,5 ÷ 15,5 = 20,03 → **21 caixas**. Argamassa (peça acima de 16 in, 40 sq ft por saco): 310,5 ÷ 40 = 7,76 → **8 sacos** × $ 22.00 (A118.1).

## Teste B: só os obrigatórios (e variações)

#### AZ-B

Digite: Área **320**; Largura da peça **12**; Altura da peça **24**.

```
Área: 320.00 sq ft
Área com perda (10%, automática): 352.00 sq ft
Peça: 12 x 24 in
• Peças: 176 ($ 1,308.07)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 9 sacos de 50 lb (440.0 lb) ($ 161.82)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,469.89
```

Pra entender: 320 × 1,10 = 352 sq ft ÷ 2 sq ft por peça = **176 peças**. A peça tem 24 in (acima de 16): desempenadeira 1/2 x 1/2 in, 40 sq ft por saco → 352 ÷ 40 = 8,8 → **9 sacos** de A118.4 × $ 17.98 = $ 161.82.

#### AZ-B2

Digite: Área **320**; Largura da peça **12**; Altura da peça **24**; Portas/janelas **50**.

```
Área: 320.00 sq ft
Vãos (portas e janelas): 50.00 sq ft
Área líquida: 270.00 sq ft
Área com perda (10%, automática): 297.00 sq ft
Peça: 12 x 24 in
• Peças: 149 ($ 1,103.69)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 8 sacos de 50 lb (371.3 lb) ($ 143.84)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,247.53
```

#### AZ-B3

Digite: Área **320**; Largura da peça **12**; Altura da peça **24**; sq ft por caixa **15.5**.

```
Área: 320.00 sq ft
Área com perda (10%, automática): 352.00 sq ft
Peça: 12 x 24 in
• Peças: 176
• Caixas: 23 (15.50 sq ft por caixa) ($ 1,308.07)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 9 sacos de 50 lb (440.0 lb) ($ 161.82)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,469.89
```

#### AZ-B4

Digite: Área **320**; Largura da peça **12**; Altura da peça **24**; Assentamento com desenho **Sim**.

```
Área: 320.00 sq ft
Área com perda (25%, automática): 400.00 sq ft
Peça: 12 x 24 in
Assentamento: com desenho
• Peças: 200 ($ 1,486.45)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 10 sacos de 50 lb (500.0 lb) ($ 179.80)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,666.25
```

#### AZ-B5

Digite: Área **320**; Largura da peça **12**; Altura da peça **24**; Argamassa **Não modificada (ANSI A118.1)**.

```
Área: 320.00 sq ft
Área com perda (10%, automática): 352.00 sq ft
Peça: 12 x 24 in
• Peças: 176 ($ 1,308.07)
• Argamassa colante (thinset) Não modificada (ANSI A118.1): 9 sacos de 50 lb (440.0 lb) ($ 198.00)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,506.07
```

#### AZ-B6

Digite: Área **320**; Largura da peça **4**; Altura da peça **4**.

```
Área: 320.00 sq ft
Área com perda (10%, automática): 352.00 sq ft
Peça: 4 x 4 in
• Peças: 3,168 ($ 1,308.07)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 5 sacos de 50 lb (207.0 lb) ($ 89.90)
  Desempenadeira: 1/4 x 1/4 in · Consumo: 0.588 lb/sq ft

Custo Estimado da Etapa: $ 1,397.97
```

## Teste C: erros de digitação e limites

#### AZ-C1

Digite: Área **(vazio)**; Largura da peça **12**; Altura da peça **24**.

```
Por favor, digite números válidos nos campos!
```

#### AZ-C2

Digite: Área **320**; Largura da peça **12**; Altura da peça **(vazio)**.

```
Por favor, digite números válidos nos campos!
```

#### AZ-C3

Digite: Área **trezentos**; Largura da peça **12**; Altura da peça **24**.

```
Por favor, digite números válidos nos campos!
```

#### AZ-C4

Digite: Área **0**; Largura da peça **12**; Altura da peça **24**.

```
Erro: Área e tamanho da peça devem ser maiores que zero.
```

#### AZ-C5

Digite: Área **-320**; Largura da peça **12**; Altura da peça **24**.

```
Erro: Área e tamanho da peça devem ser maiores que zero.
```

#### AZ-C6

Digite: Área **320,5**; Largura da peça **12**; Altura da peça **24**.

```
Área: 320.50 sq ft
Área com perda (10%, automática): 352.55 sq ft
Peça: 12 x 24 in
• Peças: 177 ($ 1,310.12)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 9 sacos de 50 lb (440.7 lb) ($ 161.82)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,471.94
```

#### AZ-C7

Digite: Área **320.5**; Largura da peça **12**; Altura da peça **24**.

```
Área: 320.50 sq ft
Área com perda (10%, automática): 352.55 sq ft
Peça: 12 x 24 in
• Peças: 177 ($ 1,310.12)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 9 sacos de 50 lb (440.7 lb) ($ 161.82)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,471.94
```

#### AZ-C8

Digite: Área **320 1/2**; Largura da peça **12**; Altura da peça **24**.

```
Área: 320.50 sq ft
Área com perda (10%, automática): 352.55 sq ft
Peça: 12 x 24 in
• Peças: 177 ($ 1,310.12)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 9 sacos de 50 lb (440.7 lb) ($ 161.82)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,471.94
```

#### AZ-C9

Digite: Área **320**; Largura da peça **12**; Altura da peça **24**; Portas/janelas **-50**.

```
Erro: Os valores não podem ser negativos.
```

#### AZ-C10

Digite: Área **320**; Largura da peça **12**; Altura da peça **24**; Portas/janelas **320**.

```
Erro: O desconto de vãos deve ser menor que a área.
```

#### AZ-C11

Digite: Área **320**; Largura da peça **12**; Altura da peça **24**; Portas/janelas **400**.

```
Erro: O desconto de vãos deve ser menor que a área.
```

#### AZ-C12

Digite: Área **320**; Largura da peça **12**; Altura da peça **24**; Portas/janelas **abc**.

```
Por favor, digite números válidos nos campos!
```

#### AZ-C13

Digite: Área **320**; Largura da peça **12**; Altura da peça **24**; Portas/janelas **50 1/2**.

```
Área: 320.00 sq ft
Vãos (portas e janelas): 50.50 sq ft
Área líquida: 269.50 sq ft
Área com perda (10%, automática): 296.45 sq ft
Peça: 12 x 24 in
• Peças: 149 ($ 1,101.64)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 8 sacos de 50 lb (370.6 lb) ($ 143.84)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,245.48
```

#### AZ-C14

Digite: Área **320**; Largura da peça **12**; Altura da peça **24**; Perda **-5**.

```
Erro: A perda não pode ser negativa.
```

#### AZ-C15

Digite: Área **320**; Largura da peça **12**; Altura da peça **24**; Perda **2.5**.

```
Área: 320.00 sq ft
Área com perda (2.5%): 328.00 sq ft
Peça: 12 x 24 in
• Peças: 164 ($ 1,218.89)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 9 sacos de 50 lb (410.1 lb) ($ 161.82)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 1,380.71
```

#### AZ-C16

Digite: Área **1-21/2**; Largura da peça **12**; Altura da peça **24**.

```
Por favor, digite números válidos nos campos!
```

#### AZ-C17

Digite: Área **1,500**; Largura da peça **12**; Altura da peça **24**.

```
Área: 1,500.00 sq ft
Área com perda (10%, automática): 1,650.00 sq ft
Peça: 12 x 24 in
• Peças: 825 ($ 6,131.60)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 42 sacos de 50 lb (2,062.4 lb) ($ 755.16)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 6,886.76
```

#### AZ-C18

Digite: Área **25000**; Largura da peça **12**; Altura da peça **24**. Na janela, toque em **Continuar**.

```
[JANELA] Área de 25,000 sq ft: o limite é 21,528 sq ft.
Área: 25,000.00 sq ft
Área com perda (10%, automática): 27,500.00 sq ft
Peça: 12 x 24 in
• Peças: 13,750 ($ 102,193.34)
• Argamassa colante (thinset) Modificada (ANSI A118.4): 688 sacos de 50 lb (34,374.9 lb) ($ 12,370.24)
  Desempenadeira: 1/2 x 1/2 in · Consumo: 1.250 lb/sq ft

Custo Estimado da Etapa: $ 114,563.58
```

## Visual (Azulejo)

- O "?" do Azulejo: mesmo texto da P2 (27 1/2 in e 35 3/8 in) e a legenda das siglas no fim.
- Limpar: A118.4 volta a vir escolhida.

---

# REJUNTE

**32 casos.** Todos OK (os 20 das pendências P3 e P7 foram corrigidos em 06/11/2026).

**Como aparece** (confira se nenhuma dica fica cortada):

- Dimensões (Obrigatório)
- (com Piso ou Azulejo preenchido) "Usar dados do Piso (430 sq ft, peça 12 x 12 in)" / "Usar dados do Azulejo (...)"
- Área a rejuntar em sq ft (ex: 430)
- Largura da peça em in (ex: 12)
- Altura da peça em in (ex: 12)
- Largura da junta em in (ex: 1/8)
- Espessura da peça em in (opcional, ex: 5/16): já vem **5/16**
- Taxa de Perda % (opcional, ex: 10): já vem **10**

## Teste A: todos os campos, opcionais trocados

#### RJ-A

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **3/16**; Espessura da peça **3/8**; Perda **15**.

```
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 3/16 in
Espessura da peça: 3/8 in
Consumo: 0.096 lb/sq ft
• Rejunte com areia (sanded) (com 15% de perda): 47.6 lb = 2 sacos de 25 lb ($ 73.22)

Custo Estimado da Etapa: $ 73.22
```

Pra entender: Junta 3/16 in (acima de 1/8): rejunte **com areia** (sacos de 25 lb e caixas de 7 lb). Com espessura 3/8 in e perda 15%, dá 47,6 lb: 1 saco de 25 lb e o resto (22,6 lb) daria 4 caixas de 7 lb = 28 lb, que passa de um saco → o app troca por **2 sacos de 25 lb** (do jeito que sobra menos).

## Teste B: só os obrigatórios (e variações)

#### RJ-B

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **1/8**.

```
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 25.3 lb = 3 caixas de 10 lb ($ 101.49)

Custo Estimado da Etapa: $ 101.49
```

Pra entender: Fórmula dos fabricantes: ((C + L) ÷ (C × L)) × junta × espessura × 1,58, com tudo em mm: 12 in = 304,8 mm, junta 1/8 in = 3,175 mm, espessura 5/16 in = 7,9375 mm → 0,261 kg/m² = **0.053 lb/sq ft**. 430 sq ft × 1,10 → **25.3 lb**. Junta até 1/8 in: **sem areia**, só em caixa de 10 lb → **3 caixas** × $ 33.83 = $ 101.49.

#### RJ-B2

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **3/16**.

```
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 3/16 in
Espessura da peça: 5/16 in
Consumo: 0.080 lb/sq ft
• Rejunte com areia (sanded) (com 10% de perda): 38.0 lb = 1 saco de 25 lb e 2 caixas de 7 lb ($ 97.05)

Custo Estimado da Etapa: $ 97.05
```

#### RJ-B3

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **1/4**.

```
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 1/4 in
Espessura da peça: 5/16 in
Consumo: 0.107 lb/sq ft
• Rejunte com areia (sanded) (com 10% de perda): 50.6 lb = 2 sacos de 25 lb e 1 caixa de 7 lb ($ 103.44)

Custo Estimado da Etapa: $ 103.44
```

#### RJ-B4

Digite: Junta **1/8**; antes, preencha o **Piso** (Área 430, Largura da peça 11 3/4, Altura da peça 11 3/4); no Rejunte, toque no botão **"Usar dados do Piso"**.

```
[BOTÃO] piso: ('430', '11 3/4', '11 3/4')
[CAMPOS] área 430, peça 11 3/4 x 11 3/4
Área: 430.00 sq ft
Peça: 11 3/4 x 11 3/4 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.055 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 25.9 lb = 3 caixas de 10 lb ($ 101.49)

Custo Estimado da Etapa: $ 101.49
```

#### RJ-B5

Digite: Junta **3/16**; antes, preencha o **Azulejo** (Área 320, Portas/janelas 50 1/2, Largura da peça 12, Altura da peça 24); no Rejunte, toque no botão **"Usar dados do Azulejo"**.

```
[BOTÃO] azulejo: ('269.5', '12', '24')
[CAMPOS] área 269.5, peça 12 x 24
Área: 269.50 sq ft
Peça: 12 x 24 in
Junta: 3/16 in
Espessura da peça: 5/16 in
Consumo: 0.060 lb/sq ft
• Rejunte com areia (sanded) (com 10% de perda): 17.9 lb = 3 caixas de 7 lb ($ 90.66)

Custo Estimado da Etapa: $ 90.66
```

## Teste C: erros de digitação e limites

#### RJ-C1

Digite: Área **(vazio)**; Largura da peça **12**; Altura da peça **12**; Junta **1/8**.

```
Por favor, digite números válidos nos campos!
```

#### RJ-C2

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **(vazio)**.

```
Por favor, digite números válidos nos campos!
```

#### RJ-C3

Digite: Área **quatrocentos**; Largura da peça **12**; Altura da peça **12**; Junta **1/8**.

```
Por favor, digite números válidos nos campos!
```

#### RJ-C4

Digite: Área **0**; Largura da peça **12**; Altura da peça **12**; Junta **1/8**.

```
Erro: Área, tamanho da peça e junta devem ser maiores que zero.
```

#### RJ-C5

Digite: Área **-430**; Largura da peça **12**; Altura da peça **12**; Junta **1/8**.

```
Erro: Área, tamanho da peça e junta devem ser maiores que zero.
```

#### RJ-C6

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **0**.

```
Erro: Área, tamanho da peça e junta devem ser maiores que zero.
```

#### RJ-C7

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **-0.125**.

```
Erro: Área, tamanho da peça e junta devem ser maiores que zero.
```

#### RJ-C8

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **-1/8**.

```
Por favor, digite números válidos nos campos!
```

#### RJ-C9

Digite: Área **430,5**; Largura da peça **12**; Altura da peça **12**; Junta **1/8**.

```
Área: 430.50 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 25.3 lb = 3 caixas de 10 lb ($ 101.49)

Custo Estimado da Etapa: $ 101.49
```

#### RJ-C10

Digite: Área **430.5**; Largura da peça **12**; Altura da peça **12**; Junta **1/8**.

```
Área: 430.50 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 25.3 lb = 3 caixas de 10 lb ($ 101.49)

Custo Estimado da Etapa: $ 101.49
```

#### RJ-C11

Digite: Área **430 1/2**; Largura da peça **12**; Altura da peça **12**; Junta **1/8**.

```
Área: 430.50 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 25.3 lb = 3 caixas de 10 lb ($ 101.49)

Custo Estimado da Etapa: $ 101.49
```

#### RJ-C12

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **0.125**.

```
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 25.3 lb = 3 caixas de 10 lb ($ 101.49)

Custo Estimado da Etapa: $ 101.49
```

#### RJ-C13

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **1/16**.

```
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 1/16 in
Espessura da peça: 5/16 in
Consumo: 0.027 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 12.7 lb = 2 caixas de 10 lb ($ 67.66)

Custo Estimado da Etapa: $ 67.66
```

#### RJ-C14

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **1/32**. Na janela, toque em **Continuar**.

```
[JANELA] Junta de 1/32 in: o normal é de 1/16 in a 9/16 in.
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 1/32 in
Espessura da peça: 5/16 in
Consumo: 0.013 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 6.3 lb = 1 caixa de 10 lb ($ 33.83)

Custo Estimado da Etapa: $ 33.83
```

#### RJ-C15

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **9/16**.

```
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 9/16 in
Espessura da peça: 5/16 in
Consumo: 0.241 lb/sq ft
• Rejunte com areia (sanded) (com 10% de perda): 113.9 lb = 4 sacos de 25 lb e 2 caixas de 7 lb ($ 206.88)

Custo Estimado da Etapa: $ 206.88
```

#### RJ-C16

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **5/8**. Na janela, toque em **Continuar**.

```
[JANELA] Junta de 5/8 in: o normal é de 1/16 in a 9/16 in.
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 5/8 in
Espessura da peça: 5/16 in
Consumo: 0.267 lb/sq ft
• Rejunte com areia (sanded) (com 10% de perda): 126.6 lb = 5 sacos de 25 lb e 1 caixa de 7 lb ($ 213.27)

Custo Estimado da Etapa: $ 213.27
```

#### RJ-C17

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **3**. Na janela, toque em **Continuar**.

```
[JANELA] Junta de 3 in: o normal é de 1/16 in a 9/16 in.
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 3 in
Espessura da peça: 5/16 in
Consumo: 1.284 lb/sq ft
• Rejunte com areia (sanded) (com 10% de perda): 607.5 lb = 24 sacos de 25 lb e 2 caixas de 7 lb ($ 939.08)

Custo Estimado da Etapa: $ 939.08
```

#### RJ-C18

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **1/8**; Espessura da peça **(vazio)**.

```
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 25.3 lb = 3 caixas de 10 lb ($ 101.49)

Custo Estimado da Etapa: $ 101.49
```

#### RJ-C19

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **1/8**; Espessura da peça **0**.

```
Erro: A espessura da peça deve ser maior que zero.
```

#### RJ-C20

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **1/8**; Perda **-5**.

```
Erro: A perda não pode ser negativa.
```

#### RJ-C21

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **1/8**; Perda **2.5**.

```
Área: 430.00 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 2.5% de perda): 23.6 lb = 3 caixas de 10 lb ($ 101.49)

Custo Estimado da Etapa: $ 101.49
```

#### RJ-C22

Digite: Área **1-21/2**; Largura da peça **12**; Altura da peça **12**; Junta **1/8**.

```
Por favor, digite números válidos nos campos!
```

#### RJ-C23

Digite: Área **1**; Largura da peça **12**; Altura da peça **12**; Junta **1/8**.

```
Área: 1.00 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 0.1 lb = 1 caixa de 10 lb ($ 33.83)

Custo Estimado da Etapa: $ 33.83
```

#### RJ-C24

Digite: Área **25000**; Largura da peça **12**; Altura da peça **12**; Junta **1/8**. Na janela, toque em **Continuar**.

```
[JANELA] Área de 25,000 sq ft: o limite é 21,528 sq ft.
Área: 25,000.00 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 1,471.6 lb = 148 caixas de 10 lb ($ 5,006.84)

Custo Estimado da Etapa: $ 5,006.84
```

#### RJ-C25

Digite: Área **430**; Largura da peça **12**; Altura da peça **12**; Junta **1/0**.

```
Por favor, digite números válidos nos campos!
```

#### RJ-C26

Digite: Área **1,500**; Largura da peça **12**; Altura da peça **12**; Junta **1/8**.

```
Área: 1,500.00 sq ft
Peça: 12 x 12 in
Junta: 1/8 in
Espessura da peça: 5/16 in
Consumo: 0.053 lb/sq ft
• Rejunte sem areia (non-sanded) (com 10% de perda): 88.3 lb = 9 caixas de 10 lb ($ 304.47)

Custo Estimado da Etapa: $ 304.47
```

## Visual (Rejunte)

- Os botões "Usar dados do Piso" e "Usar dados do Azulejo" mostram a peça **em fração e com espaço** (P7): "Usar dados do Piso (430 sq ft, peça 11 3/4 x 11 3/4 in)". Ao tocar, os campos também ficam em fração (11 3/4).
- O "?" fala do padrão 5/16 in e dos dois tipos (sem areia até 1/8 in, com areia acima), com a legenda no fim.
- Limpar: espessura volta a 5/16 e perda a 10.

---

# PINTURA

**33 casos.** Todos OK (os 3 da pendência P8 foram corrigidos em 06/11/2026).

**Como aparece** (confira se nenhuma dica fica cortada):

- Áreas e demãos
- Área de parede em sq ft (ex: 1000)
- Área de teto em sq ft (ex: 430)
- Número de demãos (ex: 2): já vem **2**
- Rendimento em sq ft/gal (opcional, ex: 400): já vem **400**
- Primer (Opcional): Sim · Não
- Taxa de Perda % (opcional, ex: 10): já vem **10**
- **Não aparecem** nos EUA: Selador e Massa (lá a parede é de drywall e só se usa o primer).

## Teste A: todos os campos, opcionais trocados

#### PT-A

Digite: Parede **1000**; Teto **430**; Demãos **3**; Rendimento **350**; Perda **15**; Primer **Sim**.

```
Parede: 1,000.00 sq ft
Teto: 430.00 sq ft
Demãos: 3
Rendimento: 350 sq ft/gal
• Tinta de parede (com 15% de perda): 9.9 gal = 2 baldes de 5 gal ($ 362.00)
• Tinta de teto (com 15% de perda): 4.2 gal = 1 balde de 5 gal ($ 181.00)
• Primer (com 15% de perda): 4.1 gal = 1 balde de 5 gal ($ 170.00)
Complementos (sobre parede + teto): Primer 1 demão

Custo Estimado da Etapa: $ 713.00
```

Pra entender: Parede: 1000 × 3 ÷ 350 × 1,15 = 9,86 gal → 1 balde de 5 gal + 4,86 gal, que dariam 5 galões (= 1 balde) → **2 baldes**. Teto: 430 × 3 ÷ 350 × 1,15 = 4,24 gal → 5 galões → **1 balde**. Primer: uma demão sobre parede + teto, 1430 ÷ 400 × 1,15 = 4,11 gal → **1 balde** (preço provisório do fundo do Brasil, em dólar).

## Teste B: só os obrigatórios (e variações)

#### PT-B

Digite: Parede **1000**.

```
Parede: 1,000.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)

Custo Estimado da Etapa: $ 215.98
```

Pra entender: 1000 × 2 ÷ 400 × 1,10 = **5.5 gal** → 1 balde de 5 gal + 0,5 gal → 1 galão de 1 gal. Custo: $ 181.00 + $ 34.98 = $ 215.98.

#### PT-B2

Digite: Parede **(vazio)**; Teto **430**.

```
Teto: 430.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de teto (com 10% de perda): 2.4 gal = 3 galões de 1 gal ($ 104.94)

Custo Estimado da Etapa: $ 104.94
```

#### PT-B3

Digite: Parede **1000**; Teto **430**.

```
Parede: 1,000.00 sq ft
Teto: 430.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)
• Tinta de teto (com 10% de perda): 2.4 gal = 3 galões de 1 gal ($ 104.94)

Custo Estimado da Etapa: $ 320.92
```

#### PT-B4

Digite: Parede **1000**; Primer **Sim**.

```
Parede: 1,000.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)
• Primer (com 10% de perda): 2.7 gal = 3 galões de 1 gal ($ 150.00)
Complementos (sobre parede + teto): Primer 1 demão

Custo Estimado da Etapa: $ 365.98
```

#### PT-B5

Digite: Parede **100**.

```
Parede: 100.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 0.6 gal = 1 galão de 1 gal ($ 34.98)

Custo Estimado da Etapa: $ 34.98
```

#### PT-B6

Digite: Parede **800**.

```
Parede: 800.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 4.4 gal = 1 balde de 5 gal ($ 181.00)

Custo Estimado da Etapa: $ 181.00
```

#### PT-B7

Digite: Parede **1000**; selador e massa corrida ligados **só por dentro** (no app dos EUA esses campos nem aparecem: no app, é igual ao Teste B).

```
Parede: 1,000.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)

Custo Estimado da Etapa: $ 215.98
```

## Teste C: erros de digitação e limites

#### PT-C1

Digite: Parede **(vazio)**; Teto **(vazio)**.

```
Por favor, digite números válidos nos campos!
```

#### PT-C2

Digite: Parede **1000**; Demãos **(vazio)**.

```
Por favor, digite números válidos nos campos!
```

#### PT-C3

Digite: Parede **mil**.

```
Por favor, digite números válidos nos campos!
```

#### PT-C4

Digite: Parede **0**.

```
Erro: Informe a área de parede ou a área de teto.
```

#### PT-C5

Digite: Parede **-1000**.

```
Erro: As áreas não podem ser negativas.
```

#### PT-C6

Digite: Parede **1000**; Demãos **0**.

```
Erro: Demãos e rendimento devem ser maiores que zero.
```

#### PT-C7

Digite: Parede **1000**; Demãos **-2**.

```
Erro: Demãos e rendimento devem ser maiores que zero.
```

#### PT-C8

Digite: Parede **1000**; Demãos **2.5**.

```
Por favor, digite números válidos nos campos!
```

#### PT-C9

Digite: Parede **1000**; Demãos **5**.

```
Parede: 1,000.00 sq ft
Demãos: 5
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 13.7 gal = 2 baldes de 5 gal e 4 galões de 1 gal ($ 501.92)

Custo Estimado da Etapa: $ 501.92
```

#### PT-C10

Digite: Parede **1000**; Demãos **6**. Na janela, toque em **Continuar**.

```
[JANELA] 6 demãos: o limite é 5 (normalmente são 2 ou 3).
Parede: 1,000.00 sq ft
Demãos: 6
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 16.5 gal = 3 baldes de 5 gal e 2 galões de 1 gal ($ 612.96)

Custo Estimado da Etapa: $ 612.96
```

#### PT-C11

Digite: Parede **1000**; Demãos **22**. Na janela, toque em **Continuar**.

```
[JANELA] 22 demãos: o limite é 5 (normalmente são 2 ou 3).
Parede: 1,000.00 sq ft
Demãos: 22
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 60.5 gal = 12 baldes de 5 gal e 1 galão de 1 gal ($ 2,206.98)

Custo Estimado da Etapa: $ 2,206.98
```

#### PT-C12

Digite: Parede **1000,5**.

```
Parede: 1,000.50 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)

Custo Estimado da Etapa: $ 215.98
```

#### PT-C13

Digite: Parede **1000.5**.

```
Parede: 1,000.50 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)

Custo Estimado da Etapa: $ 215.98
```

#### PT-C14

Digite: Parede **1000 1/2**.

```
Parede: 1,000.50 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)

Custo Estimado da Etapa: $ 215.98
```

#### PT-C15

Digite: Parede **1,000**.

```
Parede: 1,000.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)

Custo Estimado da Etapa: $ 215.98
```

#### PT-C16

Digite: Parede **1000**; Rendimento **0**.

```
Erro: Demãos e rendimento devem ser maiores que zero.
```

#### PT-C17

Digite: Parede **1000**; Rendimento **(vazio)**.

```
Parede: 1,000.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 5.5 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)

Custo Estimado da Etapa: $ 215.98
```

#### PT-C18-cancelar

Digite: Parede **1000**; Rendimento **12**. Na janela, toque em **Cancelar**.

```
[JANELA] Rendimento de 12 sq ft/gal: o normal é de 150 sq ft/gal a 800 sq ft/gal.
[Cancelar] não calculou
```

#### PT-C18-continuar

Digite: Parede **1000**; Rendimento **12**. Na janela, toque em **Continuar**.

```
[JANELA] Rendimento de 12 sq ft/gal: o normal é de 150 sq ft/gal a 800 sq ft/gal.
Parede: 1,000.00 sq ft
Demãos: 2
Rendimento: 12 sq ft/gal
• Tinta de parede (com 10% de perda): 183.3 gal = 36 baldes de 5 gal e 4 galões de 1 gal ($ 6,655.92)

Custo Estimado da Etapa: $ 6,655.92
```

#### PT-C19

Digite: Parede **1000**; Rendimento **900**. Na janela, toque em **Continuar**.

```
[JANELA] Rendimento de 900 sq ft/gal: o normal é de 150 sq ft/gal a 800 sq ft/gal.
Parede: 1,000.00 sq ft
Demãos: 2
Rendimento: 900 sq ft/gal
• Tinta de parede (com 10% de perda): 2.5 gal = 3 galões de 1 gal ($ 104.94)

Custo Estimado da Etapa: $ 104.94
```

#### PT-C20

Digite: Parede **1000**; Perda **-5**.

```
Erro: A perda não pode ser negativa.
```

#### PT-C21

Digite: Parede **1000**; Perda **2.5**.

```
Parede: 1,000.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 2.5% de perda): 5.1 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 215.98)

Custo Estimado da Etapa: $ 215.98
```

#### PT-C22

Digite: Parede **1-21/2**.

```
Por favor, digite números válidos nos campos!
```

#### PT-C23

Digite: Parede **53820**.

```
Parede: 53,820.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 296.0 gal = 59 baldes de 5 gal e 2 galões de 1 gal ($ 10,748.96)

Custo Estimado da Etapa: $ 10,748.96
```

#### PT-C24

Digite: Parede **53821**. Na janela, toque em **Continuar**.

```
[JANELA] Área de parede de 53,821 sq ft: o limite é 53,820 sq ft.
Parede: 53,821.00 sq ft
Demãos: 2
Rendimento: 400 sq ft/gal
• Tinta de parede (com 10% de perda): 296.0 gal = 59 baldes de 5 gal e 2 galões de 1 gal ($ 10,748.96)

Custo Estimado da Etapa: $ 10,748.96
```

## Visual (Pintura)

- Selador e Massa **não aparecem**; Primer aparece.
- Rendimento já vem 400.
- O "?" fala de 400 sq ft por galão, de baldes de 5 gal e galões de 1 gal, com a legenda no fim.
- P8 (limite novo do rendimento): a janela "Confira os valores" aparece com 12 sq ft/gal (o costume do Brasil, em m²/L) e com 900 sq ft/gal.

---

# BALDRAME (impermeabilização)

**29 casos.** Todos OK (os 13 das pendências P4, P5 e P6 foram corrigidos em 06/11/2026).

**Como aparece** (confira se nenhuma dica fica cortada):

- Dimensões (Obrigatório)
- Comprimento total em ft (ex: 40)
- Largura da viga em in (ex: 8)
- Altura da viga em in (ex: 12)
- Traço do concreto (cimento:areia:brita) (Opcional)
- Taxa de Perda % (opcional, ex: 5): já vem **5**
- Mão de obra por ft (opcional, ex: 8.00)
- Armadura / Ferragem (Opcional)
- Nº de barras por viga (opcional, ex: 4)
- Bitola do ferro (mm) (Parte 2: ainda em mm, não é erro)
- Espaçamento dos estribos em in (ex: 8): já vem **8**
- Impermeabilização (Opcional): Sim · Não

## Teste A: todos os campos, opcionais trocados

#### BA-A

Digite: Comprimento **100**; Largura **10**; Altura **16**; Perda **8**; Mão de obra **8.00**; Nº de barras **4**; Espaçamento dos estribos **6**; Traço **1:3:3**; Bitola **12.5 mm**; Impermeabilização **Sim**.

```
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

Custo Estimado da Etapa: $ 1,795.18
```

Pra entender: O concreto e o ferro continuam em m³, kg e barras de 12 m (Parte 2: não é erro). Impermeabilização: 100 ft × (10 + 2 × 16) in = 350 sq ft; 2 demãos de 0,4 L/m² → **6.9 gal** → 1 balde (4,75 gal de produto) + 2,1 gal → 3 galões. Custo sobre o que se compra: (4,75 + 3) gal × $ 39.95 ÷ 4,75 gal = **$ 65.18**. Mão de obra: 100 ft × $ 8.00 = $ 800.00.

## Teste B: só os obrigatórios (e variações)

#### BA-B

Digite: Comprimento **40**; Largura **8**; Altura **12**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 0.793 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.59 m³ ($ 23.60)

Custo Estimado da Etapa: $ 113.60
```

Pra entender: Sem impermeabilização: só o concreto (Parte 2: m³ e sacos de 50 kg ainda são do Brasil, não é erro). 40 ft × 8 in × 12 in = 0,755 m³ × 1,05 = 0,793 m³.

#### BA-B2

Digite: Comprimento **40**; Largura **8**; Altura **12**; Impermeabilização **Sim**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 0.793 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.59 m³ ($ 23.60)
• Impermeabilizante: 106.7 sq ft · 2.1 gal = 3 galões de 1 gal ($ 25.23)

Custo Estimado da Etapa: $ 138.83
```

Pra entender: Impermeabilização: 40 ft × (8 + 2 × 12) in = **106.7 sq ft** = 9,91 m² × 0,8 L/m² (2 demãos) = 7,93 L = **2.1 gal** → não chega aos 4,75 gal do balde → **3 galões de 1 gal**. Custo: 3 gal × $ 39.95 ÷ 4,75 gal = **$ 25.23** (hoje o app mostra $ 25.33: é a pendência P5).

#### BA-B3

Digite: Comprimento **75**; Largura **8**; Altura **12**; Impermeabilização **Sim**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 1.487 m³
• Cimento: 12 sacos de 50 kg ($ 144.00)
• Areia: 0.74 m³ ($ 33.30)
• Brita: 1.11 m³ ($ 44.40)
• Impermeabilizante: 200.0 sq ft · 3.9 gal = 4 galões de 1 gal ($ 33.64)

Custo Estimado da Etapa: $ 255.34
```

#### BA-B4

Digite: Comprimento **80**; Largura **8**; Altura **12**; Impermeabilização **Sim**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 1.586 m³
• Cimento: 12 sacos de 50 kg ($ 144.00)
• Areia: 0.79 m³ ($ 35.55)
• Brita: 1.19 m³ ($ 47.60)
• Impermeabilizante: 213.3 sq ft · 4.2 gal = 1 balde de 5 gal ($ 39.95)

Custo Estimado da Etapa: $ 267.10
```

#### BA-B5

Digite: Comprimento **100**; Largura **8**; Altura **12**; Impermeabilização **Sim**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 1.982 m³
• Cimento: 15 sacos de 50 kg ($ 180.00)
• Areia: 0.99 m³ ($ 44.55)
• Brita: 1.49 m³ ($ 59.60)
• Impermeabilizante: 266.6 sq ft · 5.2 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 48.36)

Custo Estimado da Etapa: $ 332.51
```

#### BA-B6

Digite: Comprimento **40**; Largura **8**; Altura **12**; Nº de barras **4**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 0.793 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.59 m³ ($ 23.60)
• Ferro 8 mm: 21.8 kg (5 barras de 12 m) (inclui 1.28 m de emendas)
• Estribos 5 mm c/ 8 in: 8.5 kg (5 barras de 12 m)
• Aço/Ferragem: 30.3 kg ($ 75.72)
• Arame recozido: 0.6 kg ($ 9.15)

Custo Estimado da Etapa: $ 198.47
```

#### BA-B7

Digite: Comprimento **40**; Largura **8**; Altura **12**; Mão de obra **8.00**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 0.793 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.59 m³ ($ 23.60)
• Mão de Obra: 40.0 ft ($ 320.00)

Custo Estimado da Etapa: $ 433.60
```

## Teste C: erros de digitação e limites

#### BA-C1

Digite: Comprimento **(vazio)**; Largura **8**; Altura **12**.

```
Por favor, digite números válidos nos campos!
```

#### BA-C2

Digite: Comprimento **40**; Largura **oito**; Altura **12**.

```
Por favor, digite números válidos nos campos!
```

#### BA-C3

Digite: Comprimento **40**; Largura **8**; Altura **0**.

```
Erro: Comprimento, largura e altura devem ser maiores que zero.
```

#### BA-C4

Digite: Comprimento **-40**; Largura **8**; Altura **12**.

```
Erro: Comprimento, largura e altura devem ser maiores que zero.
```

#### BA-C5

Digite: Comprimento **40,5**; Largura **8**; Altura **12**; Impermeabilização **Sim**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 0.803 m³
• Cimento: 7 sacos de 50 kg ($ 84.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.60 m³ ($ 24.00)
• Impermeabilizante: 108.0 sq ft · 2.1 gal = 3 galões de 1 gal ($ 25.23)

Custo Estimado da Etapa: $ 151.23
```

#### BA-C6

Digite: Comprimento **40.5**; Largura **8**; Altura **12**; Impermeabilização **Sim**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 0.803 m³
• Cimento: 7 sacos de 50 kg ($ 84.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.60 m³ ($ 24.00)
• Impermeabilizante: 108.0 sq ft · 2.1 gal = 3 galões de 1 gal ($ 25.23)

Custo Estimado da Etapa: $ 151.23
```

#### BA-C7

Digite: Comprimento **40 1/2**; Largura **8**; Altura **12**; Impermeabilização **Sim**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 0.803 m³
• Cimento: 7 sacos de 50 kg ($ 84.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.60 m³ ($ 24.00)
• Impermeabilizante: 108.0 sq ft · 2.1 gal = 3 galões de 1 gal ($ 25.23)

Custo Estimado da Etapa: $ 151.23
```

#### BA-C8

Digite: Comprimento **1,500**; Largura **8**; Altura **12**; Impermeabilização **Sim**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 29.733 m³
• Cimento: 223 sacos de 50 kg ($ 2,676.00)
• Areia: 14.87 m³ ($ 669.15)
• Brita: 22.30 m³ ($ 892.00)
• Impermeabilizante: 4,000.0 sq ft · 78.5 gal = 16 baldes de 5 gal e 3 galões de 1 gal ($ 664.43)

Custo Estimado da Etapa: $ 4,901.58
```

#### BA-C9

Digite: Comprimento **40**; Largura **8**; Altura **12**; Perda **-2**.

```
Erro: A perda não pode ser negativa.
```

#### BA-C10

Digite: Comprimento **40**; Largura **8**; Altura **12**; Perda **2.5**.

```
Traço: 1:2:3
Volume Total (com 2.5% de perda): 0.774 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.39 m³ ($ 17.55)
• Brita: 0.58 m³ ($ 23.20)

Custo Estimado da Etapa: $ 112.75
```

#### BA-C11-cancelar

Digite: Comprimento **40**; Largura **7**; Altura **12**. Na janela, toque em **Cancelar**.

```
[JANELA] Viga de 7 in x 12 in: o mínimo é 8 in de largura e 12 in de altura.
[Cancelar] não calculou
```

#### BA-C11-continuar

Digite: Comprimento **40**; Largura **7**; Altura **12**. Na janela, toque em **Continuar**.

```
[JANELA] Viga de 7 in x 12 in: o mínimo é 8 in de largura e 12 in de altura.
Traço: 1:2:3
Volume Total (com 5% de perda): 0.694 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.35 m³ ($ 15.75)
• Brita: 0.52 m³ ($ 20.80)

Custo Estimado da Etapa: $ 108.55
```

#### BA-C12

Digite: Comprimento **40**; Largura **7 7/8**; Altura **11 7/8**. Na janela, toque em **Continuar**.

```
[JANELA] Viga de 7 7/8 in x 11 7/8 in: o mínimo é 8 in de largura e 12 in de altura.
Traço: 1:2:3
Volume Total (com 5% de perda): 0.772 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.39 m³ ($ 17.55)
• Brita: 0.58 m³ ($ 23.20)

Custo Estimado da Etapa: $ 112.75
```

#### BA-C13

Digite: Comprimento **40**; Largura **0.2**; Altura **0.3**. Na janela, toque em **Continuar**.

```
[JANELA] Viga de 0.2 in x 0.3 in: o mínimo é 8 in de largura e 12 in de altura.
Traço: 1:2:3
Volume Total (com 5% de perda): 0.000 m³
• Cimento: 1 saco de 50 kg ($ 12.00)

Custo Estimado da Etapa: $ 12.00
```

#### BA-C14

Digite: Comprimento **40**; Largura **8**; Altura **12**; Nº de barras **-4**.

```
Erro: Barras e espaçamento dos estribos não podem ser negativos.
```

#### BA-C15

Digite: Comprimento **40**; Largura **8**; Altura **12**; Nº de barras **4.5**.

```
Por favor, digite números válidos nos campos!
```

#### BA-C16

Digite: Comprimento **40**; Largura **8**; Altura **12**; Mão de obra **oito**.

```
Por favor, digite números válidos nos campos!
```

#### BA-C17

Digite: Comprimento **40**; Largura **8**; Altura **12**; Nº de barras **4**; Espaçamento dos estribos **(vazio)**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 0.793 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.59 m³ ($ 23.60)
• Ferro 8 mm: 21.8 kg (5 barras de 12 m) (inclui 1.28 m de emendas)
• Aço/Ferragem: 21.8 kg ($ 54.38)
• Arame recozido: 0.4 kg ($ 6.45)

Custo Estimado da Etapa: $ 174.43
```

#### BA-C18

Digite: Comprimento **40**; Largura **8**; Altura **12**; Nº de barras **4**; Espaçamento dos estribos **4 1/2**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 0.793 m³
• Cimento: 6 sacos de 50 kg ($ 72.00)
• Areia: 0.40 m³ ($ 18.00)
• Brita: 0.59 m³ ($ 23.60)
• Ferro 8 mm: 21.8 kg (5 barras de 12 m) (inclui 1.28 m de emendas)
• Estribos 5 mm c/ 4 1/2 in: 15.0 kg (9 barras de 12 m)
• Aço/Ferragem: 36.7 kg ($ 91.80)
• Arame recozido: 0.7 kg ($ 10.95)

Custo Estimado da Etapa: $ 216.35
```

#### BA-C19

Digite: Comprimento **1-21/2**; Largura **8**; Altura **12**.

```
Por favor, digite números válidos nos campos!
```

#### BA-C20

Digite: Comprimento **40**; Largura **1 1/2**; Altura **12**; Nº de barras **4**. Na janela, toque em **Continuar**.

```
[JANELA] Viga de 1 1/2 in x 12 in: o mínimo é 8 in de largura e 12 in de altura.
Erro: Viga muito pequena para colocar estribos.
```

## Visual (Baldrame)

- Estribo vem com **8** (in) e perda com **5**.
- **P9:** o "?" diz "baldes de 5 gal (com 4,75 gal de produto)": nos EUA o certo é **"4.75 gal"** (com ponto).
- **Parte 2 (não é erro nesta rodada):** traço, m³ do volume, sacos de 50 kg, m³ de areia e brita, "Ferro 8 mm", kg, "barras de 12 m", "(inclui 1.28 m de emendas)", "Arame recozido ... kg" e o título "Bitola do ferro (mm)".

---

# Para o rodada3.py (Leo do terminal)

- **Desde o fechamento (06/11/2026), o rodada3.py não lê mais este arquivo:** o esperado fica no ESPERADO dentro dele. Durante a rodada, ele lia daqui assim:
- **Como ler o esperado deste arquivo:** cada caso começa numa linha `#### <NOME>` (o nome vai até o primeiro espaço; o "⚠️ P1..." depois era só aviso) e o esperado é o **primeiro bloco** entre ``` logo abaixo. Linhas `[JANELA]`, `[Cancelar] não calculou`, `[BOTÃO]` e `[CAMPOS]` fazem parte do esperado, igual no rodada2.py.
- **Valores padrão dos EUA (PADRAO do rodada3.py):** os opcionais que já vêm preenchidos no app dos EUA:
  - baldrame: perda "5", esp_estribo **"8"** (in)
  - piso e azulejo: nada (perda vazia = automática; A118.1 no Piso e A118.4 no Azulejo vêm do reiniciar, já com o país EUA)
  - rejunte: esp **"5/16"**, perda "10"
  - pintura: demaos "2", rend **"400"**, perda "10"
- **Trocar o país do mesmo jeito que o app:** chamar o próprio `SettingsScreen.alternar_pais` com um objeto falso no lugar da tela (manager=None), **antes** de criar as telas (o reiniciar escolhe a argamassa pelo país). O idioma continua "pt".
- **No test_rodada3.py:** guardar uma cópia do CONFIG_APP e dos campos da TABELA_PRECOS_GLOBAL **antes** de carregar o rodada3.py, colocar tudo de volta logo depois (apagando o `mao_obra_m2`, que o alternar_pais cria) e ligar os EUA só durante cada caso (fixture com monkeypatch), igual à fixture do inglês na rodada 2. Não usar o alternar_pais para voltar: ele volta com o PRECOS_BR (cimento 32, brita 95), e não com os preços iniciais (36 e 120), e quebraria as rodadas 1 e 2.
- **Lista de casos** (a mesma deste roteiro, na mesma ordem):

```python
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
```
