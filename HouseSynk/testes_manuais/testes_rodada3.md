# Testes da Rodada 3 (EUA, português): Piso, Azulejo, Rejunte, Pintura e Baldrame (impermeabilização), e a rodada 3b (as abas da Parte A)

**Rodada 3b começou em 15/11/2026** (decisão da Gabi de 11/11/2026: entra neste mesmo roteiro): as abas da Parte A dos EUA, uma por vez, cada uma com a sua seção, **na ordem das abas do app**. Montadas até agora: **Brocas** (40 casos, BR-), o **ferro do Baldrame** (12 casos, BA-F) as **Paredes** (38 casos, PA-) a **Laje** (36 casos, LA-) e o **Telhado** (43 casos, TE-). Os 162 casos antigos não mudaram. **O teste passa pelas 13 abas dos EUA, na ordem do app** (pedido da Gabi, 15/11/2026): Brocas, Baldrame, Paredes, Laje, Telhado, Elétrica, Hidráulica, Reboco, Piso, Azulejo, Rejunte, Pintura e Esquadrias. Nas abas da rodada 3 (Piso, Azulejo, Rejunte, Pintura e os casos antigos do Baldrame), o Leo do terminal só roda e lista. Uma aba por vez: a Gabi diz quando ir para a próxima. As pendências da 3b ficam num arquivo só delas, o **pendencias_rodada3b.md** (na mesma pasta deste roteiro), e são corrigidas só depois de testar todas as abas; depois da correção, este roteiro, o rodada3.py e o test_rodada3.py são atualizados, o arquivo de pendências é apagado e a rodada 3 acaba. Os casos marcados com ⚠️ são das pendências: o esperado já é o certo, então dão DIFERENTE até a correção.

**O que o Leo do terminal faz em cada aba da 3b (pedido da Gabi, 15/11/2026):** coloca os casos da aba no rodada3.py, roda a aba (ex.: `rodada3.py BR-`) e **só lista** para a Gabi: (1) as **pendências**: os casos que deram DIFERENTE (dizendo se o caso já tem ⚠️ no roteiro ou se é novo, com o esperado e o que o app mostrou) e qualquer outra coisa estranha que ele vir; (2) o **visual que só a Gabi pode testar no app** (o que o script não confere: dicas dos campos, títulos, menus, "?", tema claro e escuro, quebra de linha, barra de rolagem, botões, Resumo e lista de compras), tirado da seção "Visual" da aba e do "O que olhar em toda aba". **Ele não corrige nada e não lê nem mexe no pendencias_rodada3b.md:** os ⚠️ do roteiro já dizem quais casos têm que dar DIFERENTE. As pendências novas a Gabi traz para o Leo do chat, e os dois anotam no arquivo de pendências.

Criado em 05/11/2026. **Atualizado em 09/11/2026 (Parte A da versão EUA, o resto do Baldrame):** o concreto e o ferro do Baldrame passaram para as embalagens americanas, e 18 casos do Baldrame mudaram (ver "BALDRAME" abaixo); o BA-A passou a usar a bitola **#5**. **Rodada fechada em 06/11/2026:** as 9 pendências (P1 a P9) foram corrigidas, os 162 casos deram OK no rodada3.py e a Gabi conferiu o visual no app. O esperado completo agora fica dentro do rodada3.py (ESPERADO) e entra no pytest pelo tests\rodadas\test_rodada3.py. **A versão principal fica no PC da Gabi** (testes_manuais\testes_rodada3.md, na pasta do app).

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
- **Nenhum texto do Brasil** nas 5 abas: m, cm, mm, m², kg, L, "lata", "AC-I", vírgula decimal (desde 09/11/2026, também no concreto e no ferro do Baldrame).
- **Polegadas em fração:** "12 x 12 in", "1/8 in", "5/16 in", "11 3/4 x 12 in" (nunca "11.75" nem "0.031").
- **Avisos de limite** com as unidades dos EUA: "Área de 21,529 sq ft: o limite é 21,528 sq ft.", "Junta de 5/8 in: o normal é de 1/16 in a 9/16 in.".
- **"?"** de cada aba com a legenda das siglas no fim (só em português).
- O que já valia nas rodadas 1 e 2 continua: Limpar, Anterior, Próximo, Finalizar, tema claro e escuro, barra de rolagem, número e unidade sem quebra de linha.

**Não é erro nesta rodada:**
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

Fora das 5 abas (anotado para a Parte 2): as Brocas, nos EUA, também mostram a mão de obra em m e o estribo em cm. (Corrigido na Parte A, 09/11/2026.)

---

# BROCAS (rodada 3b)

**40 casos** (montado em 15/11/2026). O esperado é o que o app DEVE mostrar: 2 casos marcados com ⚠️ (P11 e P12, ver o pendencias_rodada3b.md) dão DIFERENTE até a correção, que vem só depois de testar todas as abas da 3b.

No terminal (depois que o Leo do terminal colocar os casos no rodada3.py): `env311\Scripts\python.exe -B testes_manuais\rodada3.py BR-`.

**Como aparece** (confira se nenhuma dica fica cortada):

- Dimensões (Obrigatório)
- Quantidade de brocas (ex: 10)
- Diâmetro em in (ex: 12)
- Profundidade média em ft (ex: 10)
- Traço do concreto (cimento:areia:brita) (Opcional): já vem **1:2:3**
- Taxa de Perda % (opcional, ex: 10): já vem **10**
- Mão de obra por ft (opcional, ex: 8.00)
- Armadura / Ferragem (Opcional)
- Nº de barras por broca (opcional, ex: 4)
- Bitola do ferro: já vem **#4** (opções #3, #4 e #5)
- Espaçamento dos estribos em in (ex: 8): já vem **8**

## Teste A: todos os campos, opcionais trocados

#### BR-A

Digite: Quantidade **12**; Diâmetro **14**; Profundidade **12**; Perda **8**; Mão de obra **9.50**; Nº de barras **6**; Espaçamento dos estribos **6**; Traço **1:3:3**; Bitola **#5**.

```
Traço: 1:3:3
Volume Total (com 8% de perda): 6.16 cu yd
• Cimento: 36 sacos de 94 lb ($ 432.00)
• Areia: 3.96 cu yd ($ 136.35)
• Brita: 3.96 cu yd ($ 121.20)
• Ou concreto pronto: 278 sacos de 80 lb (no lugar de cimento, areia e brita)
Gaiola de ferro: 6.00 ft de cada broca
• Ferro #5: 495.6 lb (24 barras de 20 ft)
• Estribos #3 c/ 6 in: 129.9 lb (18 barras de 20 ft)
• Aço/Ferragem: 625.5 lb ($ 709.33)
• Arame recozido: 12.5 lb = 4 rolos de 3.5 lb ($ 85.05)
• Mão de Obra: 144.0 ft ($ 1,368.00)

Custo Estimado da Etapa: $ 2,851.93
```

Pra entender: 12 brocas de 14 in com 12 ft: π × (7 in)² × 12 ft × 12 = 4,32 m³ × 1,08 = 4,71 m³ = **6.16 cu yd**. Gaiola até a metade: **6.00 ft**. Ferro em pé: 12 × 6 ft × 6 barras × 1,10 = 475.2 ft × 1.043 lb/ft (#5) = **495.6 lb** → 475.2 ÷ 20 = 23,8 → **24 barras**. Estribo em espiral: 14 in − 2 × 3 in de cobrimento = 8 in por dentro; 72 in ÷ 6 in = 12 voltas por broca, cada uma de √(25.13² + 6²) = 25.84 in, mais 2 ganchos de 5 cm; com 10% de perda = 345.4 ft × 0.376 lb/ft (#3) = **129.9 lb** → **18 barras**. Arame: 2% de 625.5 lb = **12.5 lb** → 12.5 ÷ 3.5 = 3,6 → **4 rolos**. Mão de obra: 12 × 12 ft = 144 ft × $ 9.50 = **$ 1,368.00**.

## Teste B: só os obrigatórios (e variações)

#### BR-B

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10**.

```
Traço: 1:2:3
Volume Total (com 10% de perda): 3.20 cu yd
• Cimento: 22 sacos de 94 lb ($ 264.00)
• Areia: 1.60 cu yd ($ 54.90)
• Brita: 2.40 cu yd ($ 73.20)
• Ou concreto pronto: 144 sacos de 80 lb (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 392.10
```

Pra entender: 10 × π × (6 in)² × 10 ft = 2,224 m³ × 1,10 = 2,447 m³ = **3.20 cu yd**. Cimento do traço 1:2:3: 2,447 m³ × 375 kg = 917 kg ÷ 42,64 kg (94 lb) = 21,5 → **22 sacos**. Concreto pronto: 2,447 m³ ÷ 0,01699 m³ (0.60 cu ft por saco) = 143,99 → **144 sacos de 80 lb**. Areia e brita continuam cobradas por m³ (preços provisórios).

#### BR-B2

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10**; Nº de barras **4**.

```
Traço: 1:2:3
Volume Total (com 10% de perda): 3.20 cu yd
• Cimento: 22 sacos de 94 lb ($ 264.00)
• Areia: 1.60 cu yd ($ 54.90)
• Brita: 2.40 cu yd ($ 73.20)
• Ou concreto pronto: 144 sacos de 80 lb (no lugar de cimento, areia e brita)
Gaiola de ferro: 5.00 ft de cada broca
• Ferro #4: 147.0 lb (11 barras de 20 ft)
• Estribos #3 c/ 8 in: 54.3 lb (8 barras de 20 ft)
• Aço/Ferragem: 201.3 lb ($ 228.23)
• Arame recozido: 4.0 lb = 2 rolos de 3.5 lb ($ 27.45)

Custo Estimado da Etapa: $ 647.78
```

#### BR-B3

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10**; Mão de obra **8.00**; Nº de barras **4**.

```
Traço: 1:2:3
Volume Total (com 10% de perda): 3.20 cu yd
• Cimento: 22 sacos de 94 lb ($ 264.00)
• Areia: 1.60 cu yd ($ 54.90)
• Brita: 2.40 cu yd ($ 73.20)
• Ou concreto pronto: 144 sacos de 80 lb (no lugar de cimento, areia e brita)
Gaiola de ferro: 5.00 ft de cada broca
• Ferro #4: 147.0 lb (11 barras de 20 ft)
• Estribos #3 c/ 8 in: 54.3 lb (8 barras de 20 ft)
• Aço/Ferragem: 201.3 lb ($ 228.23)
• Arame recozido: 4.0 lb = 2 rolos de 3.5 lb ($ 27.45)
• Mão de Obra: 100.0 ft ($ 800.00)

Custo Estimado da Etapa: $ 1,447.78
```

É o exemplo da Parte A (09/11/2026), conferido por você no app: **$ 1,447.78**. Mão de obra: 10 × 10 ft = 100 ft × $ 8.00 = $ 800.00.

#### BR-B4

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10**; Nº de barras **4**; Bitola **#3**.

```
Traço: 1:2:3
Volume Total (com 10% de perda): 3.20 cu yd
• Cimento: 22 sacos de 94 lb ($ 264.00)
• Areia: 1.60 cu yd ($ 54.90)
• Brita: 2.40 cu yd ($ 73.20)
• Ou concreto pronto: 144 sacos de 80 lb (no lugar de cimento, areia e brita)
Gaiola de ferro: 5.00 ft de cada broca
• Ferro #3: 82.7 lb (11 barras de 20 ft)
• Estribos #3 c/ 8 in: 54.3 lb (8 barras de 20 ft)
• Aço/Ferragem: 137.0 lb ($ 155.38)
• Arame recozido: 2.7 lb = 1 rolo de 3.5 lb ($ 18.60)

Custo Estimado da Etapa: $ 566.07
```

#### BR-B5

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10**; Nº de barras **4**; Bitola **#5**.

```
Traço: 1:2:3
Volume Total (com 10% de perda): 3.20 cu yd
• Cimento: 22 sacos de 94 lb ($ 264.00)
• Areia: 1.60 cu yd ($ 54.90)
• Brita: 2.40 cu yd ($ 73.20)
• Ou concreto pronto: 144 sacos de 80 lb (no lugar de cimento, areia e brita)
Gaiola de ferro: 5.00 ft de cada broca
• Ferro #5: 229.5 lb (11 barras de 20 ft)
• Estribos #3 c/ 8 in: 54.3 lb (8 barras de 20 ft)
• Aço/Ferragem: 283.8 lb ($ 321.78)
• Arame recozido: 5.7 lb = 2 rolos de 3.5 lb ($ 38.55)

Custo Estimado da Etapa: $ 752.42
```

#### BR-B6

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10**; Traço **1.5:5:5**.

```
Traço: 1.5:5:5
Volume Total (com 10% de perda): 3.20 cu yd
• Cimento: 17 sacos de 94 lb ($ 204.00)
• Areia: 2.09 cu yd ($ 72.00)
• Brita: 2.09 cu yd ($ 64.00)
• Ou concreto pronto: 144 sacos de 80 lb (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 340.00
```

#### BR-B7

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10**; Mão de obra **8.00**.

```
Traço: 1:2:3
Volume Total (com 10% de perda): 3.20 cu yd
• Cimento: 22 sacos de 94 lb ($ 264.00)
• Areia: 1.60 cu yd ($ 54.90)
• Brita: 2.40 cu yd ($ 73.20)
• Ou concreto pronto: 144 sacos de 80 lb (no lugar de cimento, areia e brita)
• Mão de Obra: 100.0 ft ($ 800.00)

Custo Estimado da Etapa: $ 1,192.10
```

#### BR-B8

Digite: Quantidade **1**; Diâmetro **8**; Profundidade **3**; Nº de barras **3**.

```
Traço: 1:2:3
Volume Total (com 10% de perda): 0.04 cu yd
• Cimento: 1 saco de 94 lb ($ 12.00)
• Areia: 0.02 cu yd ($ 0.90)
• Brita: 0.03 cu yd ($ 0.80)
• Ou concreto pronto: 2 sacos de 80 lb (no lugar de cimento, areia e brita)
Gaiola de ferro: 1.50 ft de cada broca
• Ferro #4: 3.3 lb (1 barra de 20 ft)
• Estribos #3 c/ 8 in: 0.9 lb (1 barra de 20 ft)
• Aço/Ferragem: 4.2 lb ($ 4.80)
• Arame recozido: 0.1 lb = 1 rolo de 3.5 lb ($ 0.60)

Custo Estimado da Etapa: $ 19.10
```

Confira o **singular**: "1 saco", "1 barra", "1 rolo". Estribo: 8 in − 6 in = só 2 in por dentro, mas ainda dá.

#### BR-B9

Digite: Quantidade **40**; Diâmetro **16**; Profundidade **20**; Nº de barras **6**.

```
Traço: 1:2:3
Volume Total (com 10% de perda): 45.51 cu yd
• Cimento: 307 sacos de 94 lb ($ 3,684.00)
• Areia: 22.75 cu yd ($ 783.00)
• Brita: 34.13 cu yd ($ 1,043.60)
• Ou concreto pronto: 2,048 sacos de 80 lb (no lugar de cimento, areia e brita)
Gaiola de ferro: 10.00 ft de cada broca
• Ferro #4: 1,763.5 lb (132 barras de 20 ft)
• Estribos #3 c/ 8 in: 675.8 lb (90 barras de 20 ft)
• Aço/Ferragem: 2,439.4 lb ($ 2,766.20)
• Arame recozido: 48.8 lb = 14 rolos de 3.5 lb ($ 331.95)

Custo Estimado da Etapa: $ 8,608.75
```

## Teste C: erros de digitação e limites

#### BR-C1

Digite: Quantidade **(vazio)**; Diâmetro **12**; Profundidade **10**.

```
Por favor, digite números válidos nos campos!
```

#### BR-C2

Digite: Quantidade **10**; Diâmetro **(vazio)**; Profundidade **10**.

```
Por favor, digite números válidos nos campos!
```

#### BR-C3

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **(vazio)**.

```
Por favor, digite números válidos nos campos!
```

#### BR-C4

Digite: Quantidade **dez**; Diâmetro **12**; Profundidade **10**.

```
Por favor, digite números válidos nos campos!
```

#### BR-C5

Digite: Quantidade **0**; Diâmetro **12**; Profundidade **10**.

```
Erro: Quantidade, profundidade e diâmetro devem ser maiores que zero.
```

#### BR-C6

Digite: Quantidade **10**; Diâmetro **0**; Profundidade **10**.

```
Erro: Quantidade, profundidade e diâmetro devem ser maiores que zero.
```

#### BR-C7

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **-10**.

```
Erro: Quantidade, profundidade e diâmetro devem ser maiores que zero.
```

#### BR-C8

Digite: Quantidade **-10**; Diâmetro **12**; Profundidade **10**.

```
Erro: Quantidade, profundidade e diâmetro devem ser maiores que zero.
```

#### BR-C9

Digite: Quantidade **2.5**; Diâmetro **12**; Profundidade **10**.

```
Por favor, digite números válidos nos campos!
```

#### BR-C10

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10,5**.

```
Traço: 1:2:3
Volume Total (com 10% de perda): 3.36 cu yd
• Cimento: 23 sacos de 94 lb ($ 276.00)
• Areia: 1.68 cu yd ($ 57.60)
• Brita: 2.52 cu yd ($ 77.20)
• Ou concreto pronto: 152 sacos de 80 lb (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 410.80
```

#### BR-C11

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10.5**.

```
Traço: 1:2:3
Volume Total (com 10% de perda): 3.36 cu yd
• Cimento: 23 sacos de 94 lb ($ 276.00)
• Areia: 1.68 cu yd ($ 57.60)
• Brita: 2.52 cu yd ($ 77.20)
• Ou concreto pronto: 152 sacos de 80 lb (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 410.80
```

#### BR-C12

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10 1/2**; Nº de barras **4**.

```
Traço: 1:2:3
Volume Total (com 10% de perda): 3.36 cu yd
• Cimento: 23 sacos de 94 lb ($ 276.00)
• Areia: 1.68 cu yd ($ 57.60)
• Brita: 2.52 cu yd ($ 77.20)
• Ou concreto pronto: 152 sacos de 80 lb (no lugar de cimento, areia e brita)
Gaiola de ferro: 5.25 ft de cada broca
• Ferro #4: 154.3 lb (12 barras de 20 ft)
• Estribos #3 c/ 8 in: 56.9 lb (8 barras de 20 ft)
• Aço/Ferragem: 211.2 lb ($ 239.55)
• Arame recozido: 4.2 lb = 2 rolos de 3.5 lb ($ 28.80)

Custo Estimado da Etapa: $ 679.15
```

#### BR-C13

Digite: Quantidade **10**; Diâmetro **11 3/4**; Profundidade **10**.

```
Traço: 1:2:3
Volume Total (com 10% de perda): 3.07 cu yd
• Cimento: 21 sacos de 94 lb ($ 252.00)
• Areia: 1.53 cu yd ($ 52.65)
• Brita: 2.30 cu yd ($ 70.40)
• Ou concreto pronto: 139 sacos de 80 lb (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 375.05
```

#### BR-C14

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10**; Perda **-5**.

```
Erro: A perda não pode ser negativa.
```

#### BR-C15

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10**; Perda **2.5**.

```
Traço: 1:2:3
Volume Total (com 2.5% de perda): 2.98 cu yd
• Cimento: 21 sacos de 94 lb ($ 252.00)
• Areia: 1.49 cu yd ($ 51.30)
• Brita: 2.24 cu yd ($ 68.40)
• Ou concreto pronto: 135 sacos de 80 lb (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 371.70
```

#### BR-C16

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10**; Nº de barras **-4**.

```
Erro: Barras e espaçamento dos estribos não podem ser negativos.
```

#### BR-C17

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10**; Nº de barras **4.5**.

```
Por favor, digite números válidos nos campos!
```

#### BR-C18

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10**; Nº de barras **4**; Espaçamento dos estribos **(vazio)**.

```
Traço: 1:2:3
Volume Total (com 10% de perda): 3.20 cu yd
• Cimento: 22 sacos de 94 lb ($ 264.00)
• Areia: 1.60 cu yd ($ 54.90)
• Brita: 2.40 cu yd ($ 73.20)
• Ou concreto pronto: 144 sacos de 80 lb (no lugar de cimento, areia e brita)
Gaiola de ferro: 5.00 ft de cada broca
• Ferro #4: 147.0 lb (11 barras de 20 ft)
• Aço/Ferragem: 147.0 lb ($ 166.65)
• Arame recozido: 2.9 lb = 1 rolo de 3.5 lb ($ 19.95)

Custo Estimado da Etapa: $ 578.70
```

#### BR-C19

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10**; Nº de barras **4**; Espaçamento dos estribos **4 1/2**.

```
Traço: 1:2:3
Volume Total (com 10% de perda): 3.20 cu yd
• Cimento: 22 sacos de 94 lb ($ 264.00)
• Areia: 1.60 cu yd ($ 54.90)
• Brita: 2.40 cu yd ($ 73.20)
• Ou concreto pronto: 144 sacos de 80 lb (no lugar de cimento, areia e brita)
Gaiola de ferro: 5.00 ft de cada broca
• Ferro #4: 147.0 lb (11 barras de 20 ft)
• Estribos #3 c/ 4 1/2 in: 90.4 lb (13 barras de 20 ft)
• Aço/Ferragem: 237.4 lb ($ 269.18)
• Arame recozido: 4.7 lb = 2 rolos de 3.5 lb ($ 32.25)

Custo Estimado da Etapa: $ 693.52
```

#### BR-C20

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10**; Nº de barras **4**; Espaçamento dos estribos **-8**.

```
Erro: Barras e espaçamento dos estribos não podem ser negativos.
```

#### BR-C21

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10**; Mão de obra **oito**.

```
Por favor, digite números válidos nos campos!
```

#### BR-C22 ⚠️ P12

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **10**; Mão de obra **-8**.

```
Erro: A mão de obra não pode ser negativa.
```

**P12:** hoje o app aceita a mão de obra negativa e mostra "Custo Estimado da Etapa: $ -407.90". O certo é o erro (decisão da Gabi, 15/11/2026).

#### BR-C23

Digite: Quantidade **10**; Diâmetro **6**; Profundidade **10**; Nº de barras **4**.

```
Erro: Diâmetro muito pequeno para colocar estribos.
```

Pra entender: 6 in − 2 × 3 in de cobrimento = 0 in por dentro, não cabe o estribo. Sem os estribos (BR-C24) a conta sai.

#### BR-C24

Digite: Quantidade **10**; Diâmetro **6**; Profundidade **10**; Nº de barras **4**; Espaçamento dos estribos **(vazio)**.

```
Traço: 1:2:3
Volume Total (com 10% de perda): 0.80 cu yd
• Cimento: 6 sacos de 94 lb ($ 72.00)
• Areia: 0.40 cu yd ($ 13.95)
• Brita: 0.60 cu yd ($ 18.40)
• Ou concreto pronto: 36 sacos de 80 lb (no lugar de cimento, areia e brita)
Gaiola de ferro: 5.00 ft de cada broca
• Ferro #4: 147.0 lb (11 barras de 20 ft)
• Aço/Ferragem: 147.0 lb ($ 166.65)
• Arame recozido: 2.9 lb = 1 rolo de 3.5 lb ($ 19.95)

Custo Estimado da Etapa: $ 290.95
```

#### BR-C25 ⚠️ P11

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **98.43**.

```
Traço: 1:2:3
Volume Total (com 10% de perda): 31.50 cu yd
• Cimento: 212 sacos de 94 lb ($ 2,544.00)
• Areia: 15.75 cu yd ($ 541.80)
• Brita: 23.62 cu yd ($ 722.40)
• Ou concreto pronto: 1,418 sacos de 80 lb (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 3,808.20
```

**P11:** hoje aparece a janela "Profundidade de 98.43 ft: o limite é 98.43 ft.". O limite (30 m = 98.425 ft) aparece arredondado, **98.43 ft**, e a conta tem que comparar com esse mesmo número (regra 12, como na P4 do Baldrame): 98.43 ft **não** dá aviso. 98 1/2 ft (BR-C27) dá.

#### BR-C26-cancelar

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **99**. Na janela, toque em **Cancelar**.

```
[JANELA] Profundidade de 99 ft: o limite é 98.43 ft.
[Cancelar] não calculou
```

#### BR-C26-continuar

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **99**. Na janela, toque em **Continuar**.

```
[JANELA] Profundidade de 99 ft: o limite é 98.43 ft.
Traço: 1:2:3
Volume Total (com 10% de perda): 31.68 cu yd
• Cimento: 214 sacos de 94 lb ($ 2,568.00)
• Areia: 15.84 cu yd ($ 544.95)
• Brita: 23.76 cu yd ($ 726.40)
• Ou concreto pronto: 1,426 sacos de 80 lb (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 3,839.35
```

#### BR-C27

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **98 1/2**. Na janela, toque em **Continuar**.

```
[JANELA] Profundidade de 98.5 ft: o limite é 98.43 ft.
Traço: 1:2:3
Volume Total (com 10% de perda): 31.52 cu yd
• Cimento: 212 sacos de 94 lb ($ 2,544.00)
• Areia: 15.76 cu yd ($ 542.25)
• Brita: 23.64 cu yd ($ 722.80)
• Ou concreto pronto: 1,419 sacos de 80 lb (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 3,809.05
```

#### BR-C28

Digite: Quantidade **10**; Diâmetro **12**; Profundidade **1-21/2**.

```
Por favor, digite números válidos nos campos!
```

#### BR-C29

Digite: Quantidade **1,000**; Diâmetro **12**; Profundidade **10**.

```
Por favor, digite números válidos nos campos!
```

Decisão da Gabi (15/11/2026): fica assim. Nos campos de quantidade, o milhar com vírgula ("1,000") não é aceito.

## Visual (Brocas)

- Perda vem com **10**, estribo com **8** (in) e bitola **#4**; o título é "Bitola do ferro", sem "(mm)".
- No resultado, nenhum m³, kg, m, cm, "sacos de 50 kg", "barras de 12 m" ou vírgula decimal; o estribo aparece em fração ("c/ 4 1/2 in", BR-C19).
- "?" das Brocas: fala do padrão americano (#3, #4 e #5, barras de 20 ft, estribo #3, 3 in de cobrimento, sacos de 94 lb e concreto pronto de 80 lb) e termina com a legenda das siglas.
- **Lista de compras** (Finalizar com o BR-B3, botão Lista de compras do Resumo), igual à aba (regra 17), no grupo MATERIAL BÁSICO:
  - Cimento: 22 sacos de 94 lb
  - Areia: 1.60 cu yd
  - Brita: 2.40 cu yd
  - Ou concreto pronto: 144 sacos de 80 lb (no lugar de cimento, areia e brita)
  - Aço/Ferragem: 201.3 lb (19 barras de 20 ft)
  - Arame recozido: 4.0 lb = 2 rolos de 3.5 lb
- No Orçamento do Resumo, as Brocas com **$ 1,447.78** (Mão de obra $ 800.00).

---

# BALDRAME (impermeabilização)

**29 casos.** Todos OK (os 13 das pendências P4, P5 e P6 foram corrigidos em 06/11/2026).

**Atualizado em 09/11/2026 (Parte A):** o concreto e o ferro saem como nos EUA, igual às Brocas: volume em cu yd, cimento em sacos de 94 lb, areia e brita em cu yd, a linha "Ou concreto pronto: X sacos de 80 lb" (sem preço, fora do custo), ferro #3, #4 e #5 em lb e barras de 20 ft (emenda de 40 vezes a bitola a cada 20 ft de viga), estribo #3 com 3 in de cobrimento, arame em lb e rolos de 3.5 lb. Mudaram 18 casos: BA-A, BA-B a BA-B7, BA-C5 a BA-C8, BA-C10, BA-C11-continuar, BA-C12, BA-C13, BA-C17 e BA-C18. A impermeabilização não mudou. Os preços continuam os provisórios (o saco de 94 lb custa o mesmo $ 12 do saco de 50 kg; areia e brita continuam cobradas por m³).

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
- Bitola do ferro: já vem **#4** (opções #3, #4 e #5)
- Espaçamento dos estribos em in (ex: 8): já vem **8**
- Impermeabilização (Opcional): Sim · Não

## Teste A: todos os campos, opcionais trocados

#### BA-A

Digite: Comprimento **100**; Largura **10**; Altura **16**; Perda **8**; Mão de obra **8.00**; Nº de barras **4**; Espaçamento dos estribos **6**; Traço **1:3:3**; Bitola **#5**; Impermeabilização **Sim**.

```
Traço: 1:3:3
Volume Total (com 8% de perda): 4.44 cu yd
• Cimento: 26 sacos de 94 lb ($ 312.00)
• Areia: 2.86 cu yd ($ 98.10)
• Brita: 2.86 cu yd ($ 87.20)
• Ou concreto pronto: 200 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ferro #5: 497.2 lb (24 barras de 20 ft) (inclui 33.33 ft de emendas)
• Estribos #3 c/ 6 in: 207.6 lb (28 barras de 20 ft)
• Aço/Ferragem: 704.8 lb ($ 799.20)
• Arame recozido: 14.1 lb = 5 rolos de 3.5 lb ($ 95.85)
• Impermeabilizante: 350.0 sq ft · 6.9 gal = 1 balde de 5 gal e 3 galões de 1 gal ($ 65.18)
• Mão de Obra: 100.0 ft ($ 800.00)

Custo Estimado da Etapa: $ 2,257.53
```

Pra entender: 100 ft de viga = 4 emendas em cada barra (a cada 20 ft); 4 barras × 4 emendas × 25 in (40 × 5/8 in, a bitola #5) = 400 in = **33.33 ft** de emendas. Ferro: (100 × 4 + 33.33) ft × 1,10 = 476.7 ft × 1.043 lb/ft = **497.2 lb** → 24 barras de 20 ft. Estribos: 10 × 16 in com 3 in de cobrimento ficam 4 × 10 in por dentro; 201 estribos (100 ft ÷ 6 in + 1) de 28 in + o gancho de 5 cm, com 10% de perda, em #3 (0.376 lb/ft) = **207.6 lb**. Impermeabilização: 100 ft × (10 + 2 × 16) in = 350 sq ft; 2 demãos de 0,4 L/m² → **6.9 gal** → 1 balde (4,75 gal de produto) + 2,1 gal → 3 galões. Custo sobre o que se compra: (4,75 + 3) gal × $ 39.95 ÷ 4,75 gal = **$ 65.18**. Mão de obra: 100 ft × $ 8.00 = $ 800.00.

## Teste B: só os obrigatórios (e variações)

#### BA-B

Digite: Comprimento **40**; Largura **8**; Altura **12**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 1.04 cu yd
• Cimento: 7 sacos de 94 lb ($ 84.00)
• Areia: 0.52 cu yd ($ 18.00)
• Brita: 0.78 cu yd ($ 23.60)
• Ou concreto pronto: 47 sacos de 80 lb (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 125.60
```

Pra entender: Sem impermeabilização: só o concreto. 40 ft × 8 in × 12 in = 0,755 m³ × 1,05 = 0,793 m³ = **1.04 cu yd**. Cimento do traço 1:2:3: 0,793 m³ × 375 kg = 297 kg ÷ 42,64 kg (94 lb) = 6,98 → **7 sacos de 94 lb**. Concreto pronto: 0,793 m³ ÷ 0,017 m³ (0.60 cu ft por saco) = 46,7 → **47 sacos de 80 lb**.

#### BA-B2

Digite: Comprimento **40**; Largura **8**; Altura **12**; Impermeabilização **Sim**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 1.04 cu yd
• Cimento: 7 sacos de 94 lb ($ 84.00)
• Areia: 0.52 cu yd ($ 18.00)
• Brita: 0.78 cu yd ($ 23.60)
• Ou concreto pronto: 47 sacos de 80 lb (no lugar de cimento, areia e brita)
• Impermeabilizante: 106.7 sq ft · 2.1 gal = 3 galões de 1 gal ($ 25.23)

Custo Estimado da Etapa: $ 150.83
```

Pra entender: Impermeabilização: 40 ft × (8 + 2 × 12) in = **106.7 sq ft** = 9,91 m² × 0,8 L/m² (2 demãos) = 7,93 L = **2.1 gal** → não chega aos 4,75 gal do balde → **3 galões de 1 gal**. Custo: 3 gal × $ 39.95 ÷ 4,75 gal = **$ 25.23**.

#### BA-B3

Digite: Comprimento **75**; Largura **8**; Altura **12**; Impermeabilização **Sim**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 1.94 cu yd
• Cimento: 14 sacos de 94 lb ($ 168.00)
• Areia: 0.97 cu yd ($ 33.30)
• Brita: 1.46 cu yd ($ 44.40)
• Ou concreto pronto: 88 sacos de 80 lb (no lugar de cimento, areia e brita)
• Impermeabilizante: 200.0 sq ft · 3.9 gal = 4 galões de 1 gal ($ 33.64)

Custo Estimado da Etapa: $ 279.34
```

#### BA-B4

Digite: Comprimento **80**; Largura **8**; Altura **12**; Impermeabilização **Sim**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 2.07 cu yd
• Cimento: 14 sacos de 94 lb ($ 168.00)
• Areia: 1.04 cu yd ($ 35.55)
• Brita: 1.56 cu yd ($ 47.60)
• Ou concreto pronto: 94 sacos de 80 lb (no lugar de cimento, areia e brita)
• Impermeabilizante: 213.3 sq ft · 4.2 gal = 1 balde de 5 gal ($ 39.95)

Custo Estimado da Etapa: $ 291.10
```

#### BA-B5

Digite: Comprimento **100**; Largura **8**; Altura **12**; Impermeabilização **Sim**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 2.59 cu yd
• Cimento: 18 sacos de 94 lb ($ 216.00)
• Areia: 1.30 cu yd ($ 44.55)
• Brita: 1.94 cu yd ($ 59.60)
• Ou concreto pronto: 117 sacos de 80 lb (no lugar de cimento, areia e brita)
• Impermeabilizante: 266.6 sq ft · 5.2 gal = 1 balde de 5 gal e 1 galão de 1 gal ($ 48.36)

Custo Estimado da Etapa: $ 368.51
```

#### BA-B6

Digite: Comprimento **40**; Largura **8**; Altura **12**; Nº de barras **4**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 1.04 cu yd
• Cimento: 7 sacos de 94 lb ($ 84.00)
• Areia: 0.52 cu yd ($ 18.00)
• Brita: 0.78 cu yd ($ 23.60)
• Ou concreto pronto: 47 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ferro #4: 122.5 lb (10 barras de 20 ft) (inclui 6.67 ft de emendas)
• Estribos #3 c/ 8 in: 37.8 lb (6 barras de 20 ft)
• Aço/Ferragem: 160.3 lb ($ 181.72)
• Arame recozido: 3.2 lb = 1 rolo de 3.5 lb ($ 21.75)

Custo Estimado da Etapa: $ 329.07
```

#### BA-B7

Digite: Comprimento **40**; Largura **8**; Altura **12**; Mão de obra **8.00**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 1.04 cu yd
• Cimento: 7 sacos de 94 lb ($ 84.00)
• Areia: 0.52 cu yd ($ 18.00)
• Brita: 0.78 cu yd ($ 23.60)
• Ou concreto pronto: 47 sacos de 80 lb (no lugar de cimento, areia e brita)
• Mão de Obra: 40.0 ft ($ 320.00)

Custo Estimado da Etapa: $ 445.60
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
Volume Total (com 5% de perda): 1.05 cu yd
• Cimento: 8 sacos de 94 lb ($ 96.00)
• Areia: 0.53 cu yd ($ 18.00)
• Brita: 0.79 cu yd ($ 24.00)
• Ou concreto pronto: 48 sacos de 80 lb (no lugar de cimento, areia e brita)
• Impermeabilizante: 108.0 sq ft · 2.1 gal = 3 galões de 1 gal ($ 25.23)

Custo Estimado da Etapa: $ 163.23
```

#### BA-C6

Digite: Comprimento **40.5**; Largura **8**; Altura **12**; Impermeabilização **Sim**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 1.05 cu yd
• Cimento: 8 sacos de 94 lb ($ 96.00)
• Areia: 0.53 cu yd ($ 18.00)
• Brita: 0.79 cu yd ($ 24.00)
• Ou concreto pronto: 48 sacos de 80 lb (no lugar de cimento, areia e brita)
• Impermeabilizante: 108.0 sq ft · 2.1 gal = 3 galões de 1 gal ($ 25.23)

Custo Estimado da Etapa: $ 163.23
```

#### BA-C7

Digite: Comprimento **40 1/2**; Largura **8**; Altura **12**; Impermeabilização **Sim**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 1.05 cu yd
• Cimento: 8 sacos de 94 lb ($ 96.00)
• Areia: 0.53 cu yd ($ 18.00)
• Brita: 0.79 cu yd ($ 24.00)
• Ou concreto pronto: 48 sacos de 80 lb (no lugar de cimento, areia e brita)
• Impermeabilizante: 108.0 sq ft · 2.1 gal = 3 galões de 1 gal ($ 25.23)

Custo Estimado da Etapa: $ 163.23
```

#### BA-C8

Digite: Comprimento **1,500**; Largura **8**; Altura **12**; Impermeabilização **Sim**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 38.89 cu yd
• Cimento: 262 sacos de 94 lb ($ 3,144.00)
• Areia: 19.44 cu yd ($ 669.15)
• Brita: 29.17 cu yd ($ 892.00)
• Ou concreto pronto: 1,750 sacos de 80 lb (no lugar de cimento, areia e brita)
• Impermeabilizante: 4,000.0 sq ft · 78.5 gal = 16 baldes de 5 gal e 3 galões de 1 gal ($ 664.43)

Custo Estimado da Etapa: $ 5,369.58
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
Volume Total (com 2.5% de perda): 1.01 cu yd
• Cimento: 7 sacos de 94 lb ($ 84.00)
• Areia: 0.51 cu yd ($ 17.55)
• Brita: 0.76 cu yd ($ 23.20)
• Ou concreto pronto: 46 sacos de 80 lb (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 124.75
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
Volume Total (com 5% de perda): 0.91 cu yd
• Cimento: 7 sacos de 94 lb ($ 84.00)
• Areia: 0.45 cu yd ($ 15.75)
• Brita: 0.68 cu yd ($ 20.80)
• Ou concreto pronto: 41 sacos de 80 lb (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 120.55
```

#### BA-C12

Digite: Comprimento **40**; Largura **7 7/8**; Altura **11 7/8**. Na janela, toque em **Continuar**.

```
[JANELA] Viga de 7 7/8 in x 11 7/8 in: o mínimo é 8 in de largura e 12 in de altura.
Traço: 1:2:3
Volume Total (com 5% de perda): 1.01 cu yd
• Cimento: 7 sacos de 94 lb ($ 84.00)
• Areia: 0.51 cu yd ($ 17.55)
• Brita: 0.76 cu yd ($ 23.20)
• Ou concreto pronto: 46 sacos de 80 lb (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 124.75
```

#### BA-C13

Digite: Comprimento **40**; Largura **0.2**; Altura **0.3**. Na janela, toque em **Continuar**.

```
[JANELA] Viga de 0.2 in x 0.3 in: o mínimo é 8 in de largura e 12 in de altura.
Traço: 1:2:3
Volume Total (com 5% de perda): 0.00 cu yd
• Cimento: 1 saco de 94 lb ($ 12.00)
• Ou concreto pronto: 1 saco de 80 lb (no lugar de cimento, areia e brita)

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
Volume Total (com 5% de perda): 1.04 cu yd
• Cimento: 7 sacos de 94 lb ($ 84.00)
• Areia: 0.52 cu yd ($ 18.00)
• Brita: 0.78 cu yd ($ 23.60)
• Ou concreto pronto: 47 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ferro #4: 122.5 lb (10 barras de 20 ft) (inclui 6.67 ft de emendas)
• Aço/Ferragem: 122.5 lb ($ 138.88)
• Arame recozido: 2.4 lb = 1 rolo de 3.5 lb ($ 16.65)

Custo Estimado da Etapa: $ 281.12
```

#### BA-C18

Digite: Comprimento **40**; Largura **8**; Altura **12**; Nº de barras **4**; Espaçamento dos estribos **4 1/2**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 1.04 cu yd
• Cimento: 7 sacos de 94 lb ($ 84.00)
• Areia: 0.52 cu yd ($ 18.00)
• Brita: 0.78 cu yd ($ 23.60)
• Ou concreto pronto: 47 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ferro #4: 122.5 lb (10 barras de 20 ft) (inclui 6.67 ft de emendas)
• Estribos #3 c/ 4 1/2 in: 66.3 lb (9 barras de 20 ft)
• Aço/Ferragem: 188.7 lb ($ 214.03)
• Arame recozido: 3.8 lb = 2 rolos de 3.5 lb ($ 25.65)

Custo Estimado da Etapa: $ 365.27
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

## Rodada 3b: o ferro dos EUA (casos novos, BA-F)

**12 casos novos** (montados em 15/11/2026): as bitolas #3 e #5, as emendas (viga de 20 ft sem emenda, de 21 ft com uma, e mais compridas), todos os campos trocados, menos barras, espaçamento 0 e negativo e o singular. Os 29 casos BA- de cima (da rodada 3) não mudaram e continuam com o esperado dentro do rodada3.py. 1 caso com ⚠️ (P12) dá DIFERENTE até a correção.

#### BA-F1

Digite: Comprimento **40**; Largura **8**; Altura **12**; Nº de barras **4**; Bitola **#3**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 1.04 cu yd
• Cimento: 7 sacos de 94 lb ($ 84.00)
• Areia: 0.52 cu yd ($ 18.00)
• Brita: 0.78 cu yd ($ 23.60)
• Ou concreto pronto: 47 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ferro #3: 68.2 lb (10 barras de 20 ft) (inclui 5.00 ft de emendas)
• Estribos #3 c/ 8 in: 37.8 lb (6 barras de 20 ft)
• Aço/Ferragem: 106.0 lb ($ 120.23)
• Arame recozido: 2.1 lb = 1 rolo de 3.5 lb ($ 14.40)

Custo Estimado da Etapa: $ 260.22
```

Pra entender: 40 ft de viga = 1 emenda em cada barra; 4 barras × 15 in (40 × 3/8 in, a bitola #3) = 60 in = **5.00 ft** de emendas. Ferro: (160 + 5) ft × 1,10 × 0.376 lb/ft = **68.2 lb** → 10 barras.

#### BA-F2

Digite: Comprimento **40**; Largura **8**; Altura **12**; Nº de barras **4**; Bitola **#5**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 1.04 cu yd
• Cimento: 7 sacos de 94 lb ($ 84.00)
• Areia: 0.52 cu yd ($ 18.00)
• Brita: 0.78 cu yd ($ 23.60)
• Ou concreto pronto: 47 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ferro #5: 193.1 lb (10 barras de 20 ft) (inclui 8.33 ft de emendas)
• Estribos #3 c/ 8 in: 37.8 lb (6 barras de 20 ft)
• Aço/Ferragem: 230.9 lb ($ 261.85)
• Arame recozido: 4.6 lb = 2 rolos de 3.5 lb ($ 31.35)

Custo Estimado da Etapa: $ 418.80
```

Pra entender: emenda da #5 = 40 × 5/8 in = 25 in; 4 × 25 in = 100 in = **8.33 ft**. Ferro: (160 + 8.33) ft × 1,10 × 1.043 lb/ft = **193.1 lb**.

#### BA-F3

Digite: Comprimento **20**; Largura **8**; Altura **12**; Nº de barras **4**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 0.52 cu yd
• Cimento: 4 sacos de 94 lb ($ 48.00)
• Areia: 0.26 cu yd ($ 9.00)
• Brita: 0.39 cu yd ($ 12.00)
• Ou concreto pronto: 24 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ferro #4: 58.8 lb (5 barras de 20 ft)
• Estribos #3 c/ 8 in: 19.2 lb (3 barras de 20 ft)
• Aço/Ferragem: 78.0 lb ($ 88.42)
• Arame recozido: 1.6 lb = 1 rolo de 3.5 lb ($ 10.65)

Custo Estimado da Etapa: $ 168.08
```

Viga de **20 ft** (o tamanho da barra): **sem emenda**, e o "(inclui ... de emendas)" não aparece.

#### BA-F4

Digite: Comprimento **21**; Largura **8**; Altura **12**; Nº de barras **4**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 0.54 cu yd
• Cimento: 4 sacos de 94 lb ($ 48.00)
• Areia: 0.27 cu yd ($ 9.45)
• Brita: 0.41 cu yd ($ 12.40)
• Ou concreto pronto: 25 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ferro #4: 66.6 lb (5 barras de 20 ft) (inclui 6.67 ft de emendas)
• Estribos #3 c/ 8 in: 19.8 lb (3 barras de 20 ft)
• Aço/Ferragem: 86.4 lb ($ 98.03)
• Arame recozido: 1.7 lb = 1 rolo de 3.5 lb ($ 11.70)

Custo Estimado da Etapa: $ 179.57
```

Viga de **21 ft**: já passa da barra, então 1 emenda em cada uma: 4 × 20 in = **6.67 ft**.

#### BA-F5

Digite: Comprimento **60**; Largura **8**; Altura **12**; Nº de barras **4**; Bitola **#5**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 1.56 cu yd
• Cimento: 11 sacos de 94 lb ($ 132.00)
• Areia: 0.78 cu yd ($ 26.55)
• Brita: 1.17 cu yd ($ 35.60)
• Ou concreto pronto: 70 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ferro #5: 294.5 lb (15 barras de 20 ft) (inclui 16.67 ft de emendas)
• Estribos #3 c/ 8 in: 56.4 lb (8 barras de 20 ft)
• Aço/Ferragem: 350.8 lb ($ 397.82)
• Arame recozido: 7.0 lb = 3 rolos de 3.5 lb ($ 47.70)

Custo Estimado da Etapa: $ 639.68
```

60 ft = 2 emendas em cada barra: 4 × 2 × 25 in = 200 in = **16.67 ft**.

#### BA-F6

Digite: Comprimento **100**; Largura **8**; Altura **12**; Nº de barras **4**; Espaçamento dos estribos **6**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 2.59 cu yd
• Cimento: 18 sacos de 94 lb ($ 216.00)
• Areia: 1.30 cu yd ($ 44.55)
• Brita: 1.94 cu yd ($ 59.60)
• Ou concreto pronto: 117 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ferro #4: 313.5 lb (24 barras de 20 ft) (inclui 26.67 ft de emendas)
• Estribos #3 c/ 6 in: 124.5 lb (17 barras de 20 ft)
• Aço/Ferragem: 438.0 lb ($ 496.67)
• Arame recozido: 8.8 lb = 3 rolos de 3.5 lb ($ 59.55)

Custo Estimado da Etapa: $ 876.38
```

100 ft com estribo a cada 6 in = **201 estribos** (100 ft ÷ 6 in + o da ponta; é a folguinha de 09/11/2026). Emendas: 4 barras × 4 × 20 in = 320 in = **26.67 ft**.

#### BA-F7

Digite: Comprimento **250**; Largura **12**; Altura **16**; Mão de obra **6.50**; Nº de barras **6**; Espaçamento dos estribos **10**; Traço **1:4:3**; Bitola **#3**; Impermeabilização **Sim**.

```
Traço: 1:4:3
Volume Total (com 5% de perda): 12.96 cu yd
• Cimento: 66 sacos de 94 lb ($ 792.00)
• Areia: 9.72 cu yd ($ 334.35)
• Brita: 7.29 cu yd ($ 222.80)
• Ou concreto pronto: 584 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ferro #3: 657.6 lb (88 barras de 20 ft) (inclui 90.00 ft de emendas)
• Estribos #3 c/ 10 in: 352.4 lb (47 barras de 20 ft)
• Aço/Ferragem: 1,010.0 lb ($ 1,145.35)
• Arame recozido: 20.2 lb = 6 rolos de 3.5 lb ($ 137.40)
• Impermeabilizante: 916.7 sq ft · 18.0 gal = 3 baldes de 5 gal e 4 galões de 1 gal ($ 153.49)
• Mão de Obra: 250.0 ft ($ 1,625.00)

Custo Estimado da Etapa: $ 4,410.39
```

Todos os campos trocados, com outros valores que o BA-A: 250 ft = 12 emendas em cada barra; 6 × 12 × 15 in (#3) = 1080 in = **90.00 ft**. Impermeabilização: 250 ft × (12 + 2 × 16) in = **916.7 sq ft**. Mão de obra: 250 ft × $ 6.50 = $ 1,625.00.

#### BA-F8

Digite: Comprimento **40**; Largura **8**; Altura **12**; Nº de barras **2**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 1.04 cu yd
• Cimento: 7 sacos de 94 lb ($ 84.00)
• Areia: 0.52 cu yd ($ 18.00)
• Brita: 0.78 cu yd ($ 23.60)
• Ou concreto pronto: 47 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ferro #4: 61.2 lb (5 barras de 20 ft) (inclui 3.33 ft de emendas)
• Estribos #3 c/ 8 in: 37.8 lb (6 barras de 20 ft)
• Aço/Ferragem: 99.0 lb ($ 112.27)
• Arame recozido: 2.0 lb = 1 rolo de 3.5 lb ($ 13.50)

Custo Estimado da Etapa: $ 251.38
```

Só 2 barras: 2 × 20 in = 40 in = **3.33 ft** de emendas.

#### BA-F9

Digite: Comprimento **40**; Largura **8**; Altura **12**; Nº de barras **4**; Espaçamento dos estribos **0**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 1.04 cu yd
• Cimento: 7 sacos de 94 lb ($ 84.00)
• Areia: 0.52 cu yd ($ 18.00)
• Brita: 0.78 cu yd ($ 23.60)
• Ou concreto pronto: 47 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ferro #4: 122.5 lb (10 barras de 20 ft) (inclui 6.67 ft de emendas)
• Aço/Ferragem: 122.5 lb ($ 138.88)
• Arame recozido: 2.4 lb = 1 rolo de 3.5 lb ($ 16.65)

Custo Estimado da Etapa: $ 281.12
```

Espaçamento **0** = sem estribos (igual ao campo vazio, BA-C17).

#### BA-F10 ⚠️ P12

Digite: Comprimento **40**; Largura **8**; Altura **12**; Mão de obra **-8**.

```
Erro: A mão de obra não pode ser negativa.
```

**P12** (a mesma das Brocas): hoje o app aceita a mão de obra negativa e mostra "Custo Estimado da Etapa: $ -194.40", sem a linha da mão de obra. O certo é o erro (decisão da Gabi, 15/11/2026).

#### BA-F11

Digite: Comprimento **40**; Largura **8**; Altura **12**; Nº de barras **4**; Espaçamento dos estribos **-6**.

```
Erro: Barras e espaçamento dos estribos não podem ser negativos.
```

#### BA-F12

Digite: Comprimento **1**; Largura **8**; Altura **12**; Nº de barras **4**.

```
Traço: 1:2:3
Volume Total (com 5% de perda): 0.03 cu yd
• Cimento: 1 saco de 94 lb ($ 12.00)
• Areia: 0.01 cu yd ($ 0.45)
• Brita: 0.02 cu yd ($ 0.40)
• Ou concreto pronto: 2 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ferro #4: 2.9 lb (1 barra de 20 ft)
• Estribos #3 c/ 8 in: 1.2 lb (1 barra de 20 ft)
• Aço/Ferragem: 4.2 lb ($ 4.72)
• Arame recozido: 0.1 lb = 1 rolo de 3.5 lb ($ 0.60)

Custo Estimado da Etapa: $ 18.18
```

Viga de 1 ft: confira o **singular** ("1 saco", "1 barra", "1 rolo").

## Visual (Baldrame)

- Estribo vem com **8** (in) e perda com **5**.
- **P9:** o "?" diz "baldes de 5 gal (com 4,75 gal de produto)": nos EUA o certo é **"4.75 gal"** (com ponto).
- **Desde 09/11/2026 (Parte A):** o título "Bitola do ferro" (sem "(mm)") com #3, #4 e #5; o "?" fala do padrão americano do ferro e do concreto pronto; nenhum m³, kg, "sacos de 50 kg", "barras de 12 m" ou "mm" no resultado.
- **Rodada 3b, lista de compras com Brocas e Baldrame juntos** (BR-B3 nas Brocas + BA-B6 no Baldrame, depois Finalizar e Lista de compras): um "Cimento" só, somando as duas abas, no grupo MATERIAL BÁSICO:
  - Cimento: 29 sacos de 94 lb
  - Areia: 2.12 cu yd
  - Brita: 3.18 cu yd
  - Ou concreto pronto: 191 sacos de 80 lb (no lugar de cimento, areia e brita)
  - Aço/Ferragem: 361.6 lb (35 barras de 20 ft)
  - Arame recozido: 7.2 lb = 3 rolos de 3.5 lb (os rolos saem do total somado: 4.0 + 3.2 lb = 7.2 lb, e não 2 + 1 rolos)
- No Orçamento do Resumo: Brocas $ 1,447.78 e Baldrame $ 329.07.

---

# PAREDES (rodada 3b)

**38 casos** (montado em 15/11/2026). 5 casos com ⚠️ (P13 e P14, ver o pendencias_rodada3b.md) dão DIFERENTE até a correção.

**Como aparece** (confira se nenhuma dica fica cortada):

- Dimensões (Obrigatório)
- Área bruta das paredes em sq ft (ex: 320)
- Tipo e tamanho do tijolo ou bloco: já vem **Bloco de concreto CMU (8x8x16)** (só essa opção)
- Portas/janelas em sq ft (opcional, ex: 50)
- Espessura da junta em in (opcional, ex: 3/8): já vem **3/8**
- Quebra de blocos % (opcional, ex: 5): já vem **5**

## Teste A: todos os campos, opcionais trocados

#### PA-A

Digite: Área **640**; Portas/janelas **80**; Junta **1/2**; Quebra **10**.

```
Área bruta: 640.00 sq ft
Vãos (portas e janelas): 80.00 sq ft
Área líquida: 560.00 sq ft
• Bloco de concreto CMU (8x8x16): 678 un ($ 4,068.00)
• Massa pronta tipo S: 53 sacos de 80 lb ($ 636.00)
• Ou: 15 sacos de cimento de alvenaria tipo S de 70 lb + 3,600 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 4,704.00
```

Pra entender: 560 sq ft = 52,03 m²; com a junta de 1/2 in, o bloco + junta ocupa 16 1/8 x 8 1/8 in → 1.100 bloco por sq ft × 560 × 1,10 = 677,4 → **678 blocos**. Massa: os blocos sem a quebra (616) + 10% de perda ÷ 13 blocos por saco = **53 sacos de 80 lb**. Alternativa: 15 sacos de 70 lb × 240 lb = 3,600 lb de areia.

## Teste B: só os obrigatórios (e variações)

#### PA-B

Digite: Área **320**.

```
Área bruta: 320.00 sq ft
• Bloco de concreto CMU (8x8x16): 378 un ($ 2,268.00)
• Massa pronta tipo S: 31 sacos de 80 lb ($ 372.00)
• Ou: 9 sacos de cimento de alvenaria tipo S de 70 lb + 2,160 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,640.00
```

É o exemplo da Parte A (09/11/2026), conferido por você no app: 320 sq ft × 1.125 bloco por sq ft × 1,05 = **378 blocos**; massa: 360 blocos sem a quebra × 1,10 ÷ 13 = 30,5 → **31 sacos**; custo **$ 2,640.00**.

#### PA-B2

Digite: Área **320**; Portas/janelas **50**.

```
Área bruta: 320.00 sq ft
Vãos (portas e janelas): 50.00 sq ft
Área líquida: 270.00 sq ft
• Bloco de concreto CMU (8x8x16): 319 un ($ 1,914.00)
• Massa pronta tipo S: 26 sacos de 80 lb ($ 312.00)
• Ou: 8 sacos de cimento de alvenaria tipo S de 70 lb + 1,920 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,226.00
```

#### PA-B3

Digite: Área **320**; Junta **1/4**.

```
Área bruta: 320.00 sq ft
• Bloco de concreto CMU (8x8x16): 388 un ($ 2,328.00)
• Massa pronta tipo S: 32 sacos de 80 lb ($ 384.00)
• Ou: 9 sacos de cimento de alvenaria tipo S de 70 lb + 2,160 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,712.00
```

#### PA-B4

Digite: Área **320**; Quebra **8**.

```
Área bruta: 320.00 sq ft
• Bloco de concreto CMU (8x8x16): 389 un ($ 2,334.00)
• Massa pronta tipo S: 31 sacos de 80 lb ($ 372.00)
• Ou: 9 sacos de cimento de alvenaria tipo S de 70 lb + 2,160 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,706.00
```

#### PA-B5

Digite: Área **4**.

```
Área bruta: 4.00 sq ft
• Bloco de concreto CMU (8x8x16): 5 un ($ 30.00)
• Massa pronta tipo S: 1 saco de 80 lb ($ 12.00)
• Ou: 1 saco de cimento de alvenaria tipo S de 70 lb + 240 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 42.00
```

Confira o **singular**: "1 saco de 80 lb" e "1 saco de cimento de alvenaria".

#### PA-B6

Digite: Área **5000**.

```
Área bruta: 5,000.00 sq ft
• Bloco de concreto CMU (8x8x16): 5,907 un ($ 35,442.00)
• Massa pronta tipo S: 476 sacos de 80 lb ($ 5,712.00)
• Ou: 135 sacos de cimento de alvenaria tipo S de 70 lb + 32,400 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 41,154.00
```

## Teste C: erros de digitação e limites

#### PA-C1

Digite: Área **(vazio)**.

```
Por favor, digite números válidos nos campos!
```

#### PA-C2

Digite: Área **trezentos**.

```
Por favor, digite números válidos nos campos!
```

#### PA-C3

Digite: Área **0**.

```
Erro: A área da parede deve ser maior que zero.
```

#### PA-C4

Digite: Área **-320**.

```
Erro: A área da parede deve ser maior que zero.
```

#### PA-C5

Digite: Área **320**; Portas/janelas **-50**.

```
Erro: Desconto, junta e quebra não podem ser negativos.
```

#### PA-C6

Digite: Área **320**; Portas/janelas **320**.

```
Erro: O desconto de vãos deve ser menor que a área.
```

#### PA-C7

Digite: Área **320**; Portas/janelas **400**.

```
Erro: O desconto de vãos deve ser menor que a área.
```

#### PA-C8

Digite: Área **320**; Portas/janelas **abc**.

```
Por favor, digite números válidos nos campos!
```

#### PA-C9

Digite: Área **320,5**.

```
Área bruta: 320.50 sq ft
• Bloco de concreto CMU (8x8x16): 379 un ($ 2,274.00)
• Massa pronta tipo S: 31 sacos de 80 lb ($ 372.00)
• Ou: 9 sacos de cimento de alvenaria tipo S de 70 lb + 2,160 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,646.00
```

#### PA-C10

Digite: Área **320.5**.

```
Área bruta: 320.50 sq ft
• Bloco de concreto CMU (8x8x16): 379 un ($ 2,274.00)
• Massa pronta tipo S: 31 sacos de 80 lb ($ 372.00)
• Ou: 9 sacos de cimento de alvenaria tipo S de 70 lb + 2,160 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,646.00
```

#### PA-C11

Digite: Área **320 1/2**.

```
Área bruta: 320.50 sq ft
• Bloco de concreto CMU (8x8x16): 379 un ($ 2,274.00)
• Massa pronta tipo S: 31 sacos de 80 lb ($ 372.00)
• Ou: 9 sacos de cimento de alvenaria tipo S de 70 lb + 2,160 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,646.00
```

#### PA-C12

Digite: Área **1,500**.

```
Área bruta: 1,500.00 sq ft
• Bloco de concreto CMU (8x8x16): 1,772 un ($ 10,632.00)
• Massa pronta tipo S: 143 sacos de 80 lb ($ 1,716.00)
• Ou: 41 sacos de cimento de alvenaria tipo S de 70 lb + 9,840 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 12,348.00
```

#### PA-C13

Digite: Área **320**; Junta **-3/8**.

```
Por favor, digite números válidos nos campos!
```

A fração negativa ("-3/8") dá a mensagem geral, igual ao Rejunte da rodada 3 (RJ-C8).

#### PA-C14

Digite: Área **320**; Quebra **-5**.

```
Erro: Desconto, junta e quebra não podem ser negativos.
```

#### PA-C15

Digite: Área **320**; Quebra **2.5**.

```
Área bruta: 320.00 sq ft
• Bloco de concreto CMU (8x8x16): 369 un ($ 2,214.00)
• Massa pronta tipo S: 31 sacos de 80 lb ($ 372.00)
• Ou: 9 sacos de cimento de alvenaria tipo S de 70 lb + 2,160 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,586.00
```

#### PA-C16

Digite: Área **320**; Junta **0**. Na janela, toque em **Continuar**.

```
[JANELA] Junta de 0 in: o normal é de 3/16 in a 1 1/4 in.
Área bruta: 320.00 sq ft
• Bloco de concreto CMU (8x8x16): 407 un ($ 2,442.00)
• Massa pronta tipo S: 33 sacos de 80 lb ($ 396.00)
• Ou: 10 sacos de cimento de alvenaria tipo S de 70 lb + 2,400 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,838.00
```

Junta 0 não é erro: dá o aviso (é menor que 3/16 in) e, com Continuar, calcula.

#### PA-C17 ⚠️ P13

Digite: Área **320**; Junta **3/16**.

```
Área bruta: 320.00 sq ft
• Bloco de concreto CMU (8x8x16): 392 un ($ 2,352.00)
• Massa pronta tipo S: 32 sacos de 80 lb ($ 384.00)
• Ou: 9 sacos de cimento de alvenaria tipo S de 70 lb + 2,160 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,736.00
```

**P13:** hoje aparece a janela "Junta de 3/16 in: o normal é de 3/16 in a 1 1/4 in.". O aviso mostra 3/16 in e 1 1/4 in, então a conta tem que comparar com esses números (regra 12): de 3/16 a 1 1/4 in **não** dá aviso.

#### PA-C18

Digite: Área **320**; Junta **1/8**. Na janela, toque em **Continuar**.

```
[JANELA] Junta de 1/8 in: o normal é de 3/16 in a 1 1/4 in.
Área bruta: 320.00 sq ft
• Bloco de concreto CMU (8x8x16): 397 un ($ 2,382.00)
• Massa pronta tipo S: 32 sacos de 80 lb ($ 384.00)
• Ou: 10 sacos de cimento de alvenaria tipo S de 70 lb + 2,400 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,766.00
```

#### PA-C19 ⚠️ P13

Digite: Área **320**; Junta **1 3/16**.

```
Área bruta: 320.00 sq ft
• Bloco de concreto CMU (8x8x16): 327 un ($ 1,962.00)
• Massa pronta tipo S: 27 sacos de 80 lb ($ 324.00)
• Ou: 8 sacos de cimento de alvenaria tipo S de 70 lb + 1,920 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,286.00
```

**P13:** hoje dá a janela (1 3/16 in passa dos 3 cm), mas está dentro de "3/16 in a 1 1/4 in", que é o que o aviso mostra.

#### PA-C20 ⚠️ P13

Digite: Área **320**; Junta **1 1/4**.

```
Área bruta: 320.00 sq ft
• Bloco de concreto CMU (8x8x16): 324 un ($ 1,944.00)
• Massa pronta tipo S: 27 sacos de 80 lb ($ 324.00)
• Ou: 8 sacos de cimento de alvenaria tipo S de 70 lb + 1,920 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,268.00
```

**P13:** hoje aparece "Junta de 1 1/4 in: o normal é de 3/16 in a 1 1/4 in.". 1 1/4 in é o próprio limite mostrado: **não** dá aviso.

#### PA-C21

Digite: Área **320**; Junta **1 5/16**. Na janela, toque em **Continuar**.

```
[JANELA] Junta de 1 5/16 in: o normal é de 3/16 in a 1 1/4 in.
Área bruta: 320.00 sq ft
• Bloco de concreto CMU (8x8x16): 320 un ($ 1,920.00)
• Massa pronta tipo S: 26 sacos de 80 lb ($ 312.00)
• Ou: 8 sacos de cimento de alvenaria tipo S de 70 lb + 1,920 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,232.00
```

1 5/16 in já passa de 1 1/4 in: dá o aviso.

#### PA-C22-cancelar

Digite: Área **320**; Junta **1 1/2**. Na janela, toque em **Cancelar**.

```
[JANELA] Junta de 1 1/2 in: o normal é de 3/16 in a 1 1/4 in.
[Cancelar] não calculou
```

#### PA-C22-continuar

Digite: Área **320**; Junta **1 1/2**. Na janela, toque em **Continuar**.

```
[JANELA] Junta de 1 1/2 in: o normal é de 3/16 in a 1 1/4 in.
Área bruta: 320.00 sq ft
• Bloco de concreto CMU (8x8x16): 310 un ($ 1,860.00)
• Massa pronta tipo S: 25 sacos de 80 lb ($ 300.00)
• Ou: 8 sacos de cimento de alvenaria tipo S de 70 lb + 1,920 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,160.00
```

#### PA-C23

Digite: Área **320**; Quebra **20**.

```
Área bruta: 320.00 sq ft
• Bloco de concreto CMU (8x8x16): 432 un ($ 2,592.00)
• Massa pronta tipo S: 31 sacos de 80 lb ($ 372.00)
• Ou: 9 sacos de cimento de alvenaria tipo S de 70 lb + 2,160 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,964.00
```

#### PA-C24

Digite: Área **320**; Quebra **25**. Na janela, toque em **Continuar**.

```
[JANELA] Quebra de 25%: o limite é 20%.
Área bruta: 320.00 sq ft
• Bloco de concreto CMU (8x8x16): 450 un ($ 2,700.00)
• Massa pronta tipo S: 31 sacos de 80 lb ($ 372.00)
• Ou: 9 sacos de cimento de alvenaria tipo S de 70 lb + 2,160 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 3,072.00
```

#### PA-C25 ⚠️ P13

Digite: Área **21528**.

```
Área bruta: 21,528.00 sq ft
• Bloco de concreto CMU (8x8x16): 25,430 un ($ 152,580.00)
• Massa pronta tipo S: 2,050 sacos de 80 lb ($ 24,600.00)
• Ou: 580 sacos de cimento de alvenaria tipo S de 70 lb + 139,200 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 177,180.00
```

**P13:** hoje aparece "Área de 21,528 sq ft: o limite é 21,528 sq ft.". No Piso (PI-C28) isso já foi corrigido na rodada 3: 21,528 sq ft **não** dá aviso; 21,529 dá (PA-C26).

#### PA-C26

Digite: Área **21529**. Na janela, toque em **Continuar**.

```
[JANELA] Área de 21,529 sq ft: o limite é 21,528 sq ft.
Área bruta: 21,529.00 sq ft
• Bloco de concreto CMU (8x8x16): 25,432 un ($ 152,592.00)
• Massa pronta tipo S: 2,050 sacos de 80 lb ($ 24,600.00)
• Ou: 580 sacos de cimento de alvenaria tipo S de 70 lb + 139,200 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 177,192.00
```

#### PA-C27

Digite: Área **1-21/2**.

```
Por favor, digite números válidos nos campos!
```

#### PA-C28 ⚠️ P14

Digite: Área **320**; Junta **(vazio)**.

```
Área bruta: 320.00 sq ft
• Bloco de concreto CMU (8x8x16): 378 un ($ 2,268.00)
• Massa pronta tipo S: 31 sacos de 80 lb ($ 372.00)
• Ou: 9 sacos de cimento de alvenaria tipo S de 70 lb + 2,160 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,640.00
```

**P14:** com a junta **apagada**, hoje o app usa 1 cm (0.394 in) e dá **377 blocos** ($ 2,634.00). O campo vem com 3/8 in, então vazio = **3/8 in**, igual ao PA-B (como a P3 do Rejunte na rodada 3).

#### PA-C29

Digite: Área **320**; Quebra **(vazio)**.

```
Área bruta: 320.00 sq ft
• Bloco de concreto CMU (8x8x16): 378 un ($ 2,268.00)
• Massa pronta tipo S: 31 sacos de 80 lb ($ 372.00)
• Ou: 9 sacos de cimento de alvenaria tipo S de 70 lb + 2,160 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,640.00
```

Quebra apagada = 5%, igual ao PA-B.

#### PA-C30

Digite: Área **320**; Portas/janelas **50 1/2**.

```
Área bruta: 320.00 sq ft
Vãos (portas e janelas): 50.50 sq ft
Área líquida: 269.50 sq ft
• Bloco de concreto CMU (8x8x16): 319 un ($ 1,914.00)
• Massa pronta tipo S: 26 sacos de 80 lb ($ 312.00)
• Ou: 8 sacos de cimento de alvenaria tipo S de 70 lb + 1,920 lb de areia (no lugar da massa pronta)

Custo Estimado da Etapa: $ 2,226.00
```

## Visual (Paredes)

- Os campos **Assentamento** e **Traço da massa não aparecem** nos EUA (o bloco vai sempre do mesmo jeito e a massa vem pronta).
- O menu do bloco só tem **"Bloco de concreto CMU (8x8x16)"**.
- Junta vem com **3/8** e quebra com **5**.
- No resultado, nenhum m², m³, kg, "milheiro", "un (0,38 milheiro)", "cimento", "cal" ou vírgula decimal; os blocos só em peças ("378 un").
- "?" das Paredes: fala do bloco CMU 8x8x16 (7 5/8 x 7 5/8 x 15 5/8 in, 1.125 bloco por sq ft), da massa pronta tipo S de 80 lb (13 blocos por saco), da opção com cimento de alvenaria de 70 lb e areia, dos 10% de perda da massa, e termina com a legenda das siglas.
- **Lista de compras** (Finalizar com o PA-B, botão Lista de compras do Resumo), no grupo MATERIAL BÁSICO:
  - Bloco de concreto CMU (8x8x16): 378 un
  - Massa pronta tipo S: 31 sacos de 80 lb
  - Ou: 9 sacos de cimento de alvenaria tipo S de 70 lb + 2,160 lb de areia (no lugar da massa pronta)
- No Orçamento do Resumo, as Paredes com **$ 2,640.00**.

---

# LAJE (rodada 3b)

**36 casos** (montado em 15/11/2026). Nenhuma pendência achada ao montar: todos devem dar OK.

**Como aparece** (confira se nenhuma dica fica cortada):

- Dimensões (Obrigatório)
- Área da laje em sq ft (ex: 500)
- Espessura da laje em in (opcional, ex: 4): já vem **4**
- Tela soldada (Opcional): Sim · Não (já vem **Não**)
- Lona plástica por baixo (vapor retarder) (Opcional): Sim · Não (já vem **Sim**)
- Base de brita de 4 in (Opcional): Sim · Não (já vem **Sim**)
- Traço do concreto (cimento:areia:brita) (Opcional): já vem **1:2:3**
- Taxa de Perda % (opcional, ex: 5): já vem **5**

## Teste A: todos os campos, opcionais trocados

#### LA-A

Digite: Área **1200**; Espessura **6**; Perda **8**; Traço **1:3:3**; Tela soldada **Sim**; Lona **Não**; Base de brita **Não**.

```
Área: 1,200.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 6 in
Traço: 1:3:3
Volume Total (com 8% de perda): 24.00 cu yd
• Tela soldada: 1,320.00 sq ft = 27 painéis de 5 x 10 ft ($ 2,565.00)
• Cimento: 139 sacos de 94 lb ($ 1,668.00)
• Areia: 15.43 cu yd ($ 531.00)
• Brita: 15.43 cu yd ($ 472.00)
• Ou concreto pronto: 1,080 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 24.00 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 5,236.00
```

Todos os opcionais trocados: tela Sim, lona e base **Não** (as duas linhas somem). 1,200 sq ft × 6 in = 600 cu ft = 22,2 cu yd × 1,08 = **24.00 cu yd**; caminhão de 1/4 em 1/4: **24.00**. Tela: 1,200 × 1,10 = 1,320 sq ft ÷ 50 = 26,4 → **27 painéis**.

## Teste B: só os obrigatórios (e variações)

#### LA-B

Digite: Área **500**.

```
Área: 500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1:2:3
Volume Total (com 5% de perda): 6.48 cu yd
• Brita da base (4 in): 6.48 cu yd ($ 198.20)
• Lona plástica (vapor retarder): 550.00 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Cimento: 44 sacos de 94 lb ($ 528.00)
• Areia: 3.24 cu yd ($ 111.60)
• Brita: 4.86 cu yd ($ 148.80)
• Ou concreto pronto: 292 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 6.50 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 1,076.60
```

Só a área: espessura 4 in, lona e base **Sim** (o padrão), tela **Não**. 500 sq ft × 4 in = 166,7 cu ft = 6,17 cu yd × 1,05 = **6.48 cu yd**; caminhão: 6.48 → **6.50 cu yd**. Base: 500 × 4 in × 1,05 = **6.48 cu yd**. Lona: 500 × 1,10 = **550 sq ft** → 1 rolo de 1,000 sq ft.

#### LA-B2

Digite: Área **500**; Tela soldada **Sim**.

```
Área: 500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1:2:3
Volume Total (com 5% de perda): 6.48 cu yd
• Brita da base (4 in): 6.48 cu yd ($ 198.20)
• Lona plástica (vapor retarder): 550.00 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Tela soldada: 550.00 sq ft = 11 painéis de 5 x 10 ft ($ 1,045.00)
• Cimento: 44 sacos de 94 lb ($ 528.00)
• Areia: 3.24 cu yd ($ 111.60)
• Brita: 4.86 cu yd ($ 148.80)
• Ou concreto pronto: 292 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 6.50 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 2,121.60
```

É o exemplo da Parte A (09/11/2026), conferido por você no app: **$ 2,121.60**.

#### LA-B3

Digite: Área **500**; Lona **Não**.

```
Área: 500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1:2:3
Volume Total (com 5% de perda): 6.48 cu yd
• Brita da base (4 in): 6.48 cu yd ($ 198.20)
• Cimento: 44 sacos de 94 lb ($ 528.00)
• Areia: 3.24 cu yd ($ 111.60)
• Brita: 4.86 cu yd ($ 148.80)
• Ou concreto pronto: 292 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 6.50 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 986.60
```

#### LA-B4

Digite: Área **500**; Base de brita **Não**.

```
Área: 500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1:2:3
Volume Total (com 5% de perda): 6.48 cu yd
• Lona plástica (vapor retarder): 550.00 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Cimento: 44 sacos de 94 lb ($ 528.00)
• Areia: 3.24 cu yd ($ 111.60)
• Brita: 4.86 cu yd ($ 148.80)
• Ou concreto pronto: 292 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 6.50 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 878.40
```

#### LA-B5

Digite: Área **500**; Lona **Não**; Base de brita **Não**.

```
Área: 500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1:2:3
Volume Total (com 5% de perda): 6.48 cu yd
• Cimento: 44 sacos de 94 lb ($ 528.00)
• Areia: 3.24 cu yd ($ 111.60)
• Brita: 4.86 cu yd ($ 148.80)
• Ou concreto pronto: 292 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 6.50 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 788.40
```

#### LA-B6

Digite: Área **500**; Espessura **5**.

```
Área: 500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 5 in
Traço: 1:2:3
Volume Total (com 5% de perda): 8.10 cu yd
• Brita da base (4 in): 6.48 cu yd ($ 198.20)
• Lona plástica (vapor retarder): 550.00 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Cimento: 55 sacos de 94 lb ($ 660.00)
• Areia: 4.05 cu yd ($ 139.50)
• Brita: 6.08 cu yd ($ 186.00)
• Ou concreto pronto: 365 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 8.25 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 1,273.70
```

A base continua com 4 in (6.48 cu yd): só o concreto muda com a espessura.

#### LA-B7

Digite: Área **500**; Traço **1.5:5:5**.

```
Área: 500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1.5:5:5
Volume Total (com 5% de perda): 6.48 cu yd
• Brita da base (4 in): 6.48 cu yd ($ 198.20)
• Lona plástica (vapor retarder): 550.00 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Cimento: 35 sacos de 94 lb ($ 420.00)
• Areia: 4.23 cu yd ($ 145.35)
• Brita: 4.23 cu yd ($ 129.20)
• Ou concreto pronto: 292 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 6.50 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 982.75
```

#### LA-B8

Digite: Área **20**; Tela soldada **Sim**.

```
Área: 20.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1:2:3
Volume Total (com 5% de perda): 0.26 cu yd
• Brita da base (4 in): 0.26 cu yd ($ 7.92)
• Lona plástica (vapor retarder): 22.00 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Tela soldada: 22.00 sq ft = 1 painel de 5 x 10 ft ($ 95.00)
• Cimento: 2 sacos de 94 lb ($ 24.00)
• Areia: 0.13 cu yd ($ 4.50)
• Brita: 0.19 cu yd ($ 6.00)
• Ou concreto pronto: 12 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 0.50 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 227.42
```

Confira o **singular**: "1 rolo" e "1 painel".

#### LA-B9

Digite: Área **10000**; Tela soldada **Sim**.

```
Área: 10,000.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1:2:3
Volume Total (com 5% de perda): 129.63 cu yd
• Brita da base (4 in): 129.63 cu yd ($ 3,964.36)
• Lona plástica (vapor retarder): 11,000.00 sq ft = 11 rolos de 10 x 100 ft ($ 990.00)
• Tela soldada: 11,000.00 sq ft = 220 painéis de 5 x 10 ft ($ 20,900.00)
• Cimento: 872 sacos de 94 lb ($ 10,464.00)
• Areia: 64.81 cu yd ($ 2,229.75)
• Brita: 97.22 cu yd ($ 2,973.20)
• Ou concreto pronto: 5,834 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 129.75 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 41,521.31
```

## Teste C: erros de digitação e limites

#### LA-C1

Digite: Área **(vazio)**.

```
Por favor, digite números válidos nos campos!
```

#### LA-C2

Digite: Área **quinhentos**.

```
Por favor, digite números válidos nos campos!
```

#### LA-C3

Digite: Área **0**.

```
Erro: A área deve ser maior que zero.
```

#### LA-C4

Digite: Área **-500**.

```
Erro: A área deve ser maior que zero.
```

#### LA-C5

Digite: Área **500,5**.

```
Área: 500.50 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1:2:3
Volume Total (com 5% de perda): 6.49 cu yd
• Brita da base (4 in): 6.49 cu yd ($ 198.40)
• Lona plástica (vapor retarder): 550.55 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Cimento: 44 sacos de 94 lb ($ 528.00)
• Areia: 3.24 cu yd ($ 111.60)
• Brita: 4.87 cu yd ($ 148.80)
• Ou concreto pronto: 292 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 6.50 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 1,076.80
```

#### LA-C6

Digite: Área **500.5**.

```
Área: 500.50 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1:2:3
Volume Total (com 5% de perda): 6.49 cu yd
• Brita da base (4 in): 6.49 cu yd ($ 198.40)
• Lona plástica (vapor retarder): 550.55 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Cimento: 44 sacos de 94 lb ($ 528.00)
• Areia: 3.24 cu yd ($ 111.60)
• Brita: 4.87 cu yd ($ 148.80)
• Ou concreto pronto: 292 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 6.50 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 1,076.80
```

#### LA-C7

Digite: Área **500 1/2**.

```
Área: 500.50 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1:2:3
Volume Total (com 5% de perda): 6.49 cu yd
• Brita da base (4 in): 6.49 cu yd ($ 198.40)
• Lona plástica (vapor retarder): 550.55 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Cimento: 44 sacos de 94 lb ($ 528.00)
• Areia: 3.24 cu yd ($ 111.60)
• Brita: 4.87 cu yd ($ 148.80)
• Ou concreto pronto: 292 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 6.50 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 1,076.80
```

#### LA-C8

Digite: Área **1,500**.

```
Área: 1,500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1:2:3
Volume Total (com 5% de perda): 19.44 cu yd
• Brita da base (4 in): 19.44 cu yd ($ 594.64)
• Lona plástica (vapor retarder): 1,650.00 sq ft = 2 rolos de 10 x 100 ft ($ 180.00)
• Cimento: 131 sacos de 94 lb ($ 1,572.00)
• Areia: 9.72 cu yd ($ 334.35)
• Brita: 14.58 cu yd ($ 446.00)
• Ou concreto pronto: 875 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 19.50 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 3,126.99
```

#### LA-C9

Digite: Área **500**; Espessura **(vazio)**.

```
Área: 500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1:2:3
Volume Total (com 5% de perda): 6.48 cu yd
• Brita da base (4 in): 6.48 cu yd ($ 198.20)
• Lona plástica (vapor retarder): 550.00 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Cimento: 44 sacos de 94 lb ($ 528.00)
• Areia: 3.24 cu yd ($ 111.60)
• Brita: 4.86 cu yd ($ 148.80)
• Ou concreto pronto: 292 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 6.50 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 1,076.60
```

Espessura apagada = **4 in**, igual ao LA-B.

#### LA-C10

Digite: Área **500**; Espessura **0**.

```
Erro: A espessura da laje deve ser maior que zero.
```

#### LA-C11

Digite: Área **500**; Espessura **-4**.

```
Erro: A espessura da laje deve ser maior que zero.
```

#### LA-C12-cancelar

Digite: Área **500**; Espessura **3**. Na janela, toque em **Cancelar**.

```
[JANELA] Espessura de 3 in: o normal é de 3 1/2 in a 8 in.
[Cancelar] não calculou
```

#### LA-C12-continuar

Digite: Área **500**; Espessura **3**. Na janela, toque em **Continuar**.

```
[JANELA] Espessura de 3 in: o normal é de 3 1/2 in a 8 in.
Área: 500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 3 in
Traço: 1:2:3
Volume Total (com 5% de perda): 4.86 cu yd
• Brita da base (4 in): 6.48 cu yd ($ 198.20)
• Lona plástica (vapor retarder): 550.00 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Cimento: 33 sacos de 94 lb ($ 396.00)
• Areia: 2.43 cu yd ($ 83.70)
• Brita: 3.65 cu yd ($ 111.60)
• Ou concreto pronto: 219 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 5.00 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 879.50
```

#### LA-C13

Digite: Área **500**; Espessura **3 7/16**. Na janela, toque em **Continuar**.

```
[JANELA] Espessura de 3 7/16 in: o normal é de 3 1/2 in a 8 in.
Área: 500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 3 7/16 in
Traço: 1:2:3
Volume Total (com 5% de perda): 5.57 cu yd
• Brita da base (4 in): 6.48 cu yd ($ 198.20)
• Lona plástica (vapor retarder): 550.00 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Cimento: 38 sacos de 94 lb ($ 456.00)
• Areia: 2.79 cu yd ($ 95.85)
• Brita: 4.18 cu yd ($ 127.60)
• Ou concreto pronto: 251 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 5.75 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 967.65
```

3 7/16 in fica abaixo de 3 1/2 in (o mínimo do IRC): dá o aviso.

#### LA-C14

Digite: Área **500**; Espessura **3 1/2**.

```
Área: 500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 3 1/2 in
Traço: 1:2:3
Volume Total (com 5% de perda): 5.67 cu yd
• Brita da base (4 in): 6.48 cu yd ($ 198.20)
• Lona plástica (vapor retarder): 550.00 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Cimento: 39 sacos de 94 lb ($ 468.00)
• Areia: 2.84 cu yd ($ 97.65)
• Brita: 4.25 cu yd ($ 130.00)
• Ou concreto pronto: 256 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 5.75 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 983.85
```

3 1/2 in é o próprio mínimo: sem aviso. 8 in (LA-C15) também.

#### LA-C15

Digite: Área **500**; Espessura **8**.

```
Área: 500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 8 in
Traço: 1:2:3
Volume Total (com 5% de perda): 12.96 cu yd
• Brita da base (4 in): 6.48 cu yd ($ 198.20)
• Lona plástica (vapor retarder): 550.00 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Cimento: 88 sacos de 94 lb ($ 1,056.00)
• Areia: 6.48 cu yd ($ 223.20)
• Brita: 9.72 cu yd ($ 297.20)
• Ou concreto pronto: 584 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 13.00 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 1,864.60
```

#### LA-C16

Digite: Área **500**; Espessura **8 1/8**. Na janela, toque em **Continuar**.

```
[JANELA] Espessura de 8 1/8 in: o normal é de 3 1/2 in a 8 in.
Área: 500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 8 1/8 in
Traço: 1:2:3
Volume Total (com 5% de perda): 13.17 cu yd
• Brita da base (4 in): 6.48 cu yd ($ 198.20)
• Lona plástica (vapor retarder): 550.00 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Cimento: 89 sacos de 94 lb ($ 1,068.00)
• Areia: 6.58 cu yd ($ 226.35)
• Brita: 9.87 cu yd ($ 302.00)
• Ou concreto pronto: 593 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 13.25 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 1,884.55
```

#### LA-C17

Digite: Área **500**; Espessura **10**. Na janela, toque em **Continuar**.

```
[JANELA] Espessura de 10 in: o normal é de 3 1/2 in a 8 in.
Área: 500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 10 in
Traço: 1:2:3
Volume Total (com 5% de perda): 16.20 cu yd
• Brita da base (4 in): 6.48 cu yd ($ 198.20)
• Lona plástica (vapor retarder): 550.00 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Cimento: 109 sacos de 94 lb ($ 1,308.00)
• Areia: 8.10 cu yd ($ 278.55)
• Brita: 12.15 cu yd ($ 371.60)
• Ou concreto pronto: 730 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 16.25 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 2,246.35
```

#### LA-C18

Digite: Área **500**; Espessura **quatro**.

```
Por favor, digite números válidos nos campos!
```

#### LA-C19

Digite: Área **500**; Perda **-5**.

```
Erro: A perda não pode ser negativa.
```

#### LA-C20

Digite: Área **500**; Perda **2.5**.

```
Área: 500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1:2:3
Volume Total (com 2.5% de perda): 6.33 cu yd
• Brita da base (4 in): 6.33 cu yd ($ 193.48)
• Lona plástica (vapor retarder): 550.00 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Cimento: 43 sacos de 94 lb ($ 516.00)
• Areia: 3.16 cu yd ($ 108.90)
• Brita: 4.75 cu yd ($ 145.20)
• Ou concreto pronto: 285 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 6.50 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 1,053.58
```

#### LA-C21

Digite: Área **500**; Perda **(vazio)**.

```
Área: 500.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1:2:3
Volume Total (com 5% de perda): 6.48 cu yd
• Brita da base (4 in): 6.48 cu yd ($ 198.20)
• Lona plástica (vapor retarder): 550.00 sq ft = 1 rolo de 10 x 100 ft ($ 90.00)
• Cimento: 44 sacos de 94 lb ($ 528.00)
• Areia: 3.24 cu yd ($ 111.60)
• Brita: 4.86 cu yd ($ 148.80)
• Ou concreto pronto: 292 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 6.50 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 1,076.60
```

#### LA-C22

Digite: Área **21528**.

```
Área: 21,528.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1:2:3
Volume Total (com 5% de perda): 279.07 cu yd
• Brita da base (4 in): 279.07 cu yd ($ 8,534.48)
• Lona plástica (vapor retarder): 23,680.80 sq ft = 24 rolos de 10 x 100 ft ($ 2,160.00)
• Cimento: 1,877 sacos de 94 lb ($ 22,524.00)
• Areia: 139.53 cu yd ($ 4,800.60)
• Brita: 209.30 cu yd ($ 6,400.80)
• Ou concreto pronto: 12,558 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 279.25 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 44,419.88
```

21,528 sq ft é o próprio limite mostrado: sem aviso (a regra 12 já funciona na Laje).

#### LA-C23

Digite: Área **21529**. Na janela, toque em **Continuar**.

```
[JANELA] Área de 21,529 sq ft: o limite é 21,528 sq ft.
Área: 21,529.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 4 in
Traço: 1:2:3
Volume Total (com 5% de perda): 279.08 cu yd
• Brita da base (4 in): 279.08 cu yd ($ 8,534.88)
• Lona plástica (vapor retarder): 23,681.90 sq ft = 24 rolos de 10 x 100 ft ($ 2,160.00)
• Cimento: 1,877 sacos de 94 lb ($ 22,524.00)
• Areia: 139.54 cu yd ($ 4,801.05)
• Brita: 209.31 cu yd ($ 6,401.20)
• Ou concreto pronto: 12,559 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 279.25 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 44,421.13
```

#### LA-C24

Digite: Área **25000**; Espessura **10**. Na janela, toque em **Continuar**.

```
[JANELA] Área de 25,000 sq ft: o limite é 21,528 sq ft. | Espessura de 10 in: o normal é de 3 1/2 in a 8 in.
Área: 25,000.00 sq ft
Tipo de laje: Piso de concreto no chão (slab-on-grade)
Espessura: 10 in
Traço: 1:2:3
Volume Total (com 5% de perda): 810.19 cu yd
• Brita da base (4 in): 324.07 cu yd ($ 9,910.88)
• Lona plástica (vapor retarder): 27,500.00 sq ft = 28 rolos de 10 x 100 ft ($ 2,520.00)
• Cimento: 5,448 sacos de 94 lb ($ 65,376.00)
• Areia: 405.09 cu yd ($ 13,937.40)
• Brita: 607.64 cu yd ($ 18,582.80)
• Ou concreto pronto: 36,459 sacos de 80 lb (no lugar de cimento, areia e brita)
• Ou concreto usinado (caminhão): 810.25 cu yd (no lugar de cimento, areia e brita)

Custo Estimado da Etapa: $ 110,327.08
```

Os dois avisos aparecem juntos na mesma janela.

#### LA-C25

Digite: Área **1-21/2**.

```
Por favor, digite números válidos nos campos!
```

## Visual (Laje)

- Nos EUA **não aparecem**: o menu "Tipo de laje", o enchimento (isopor ou lajota), a capa e a espessura da maciça.
- Espessura vem com **4**, perda com **5**; tela **Não**, lona **Sim**, base **Sim**.
- No resultado aparece "Tipo de laje: Piso de concreto no chão (slab-on-grade)"; nenhum m², m³, kg, "sacos de 50 kg", "painéis de 2 x 3 m", "lajotas" ou vírgula decimal.
- "?" da Laje: fala do slab-on-grade, da espessura de 4 in (mínimo de 3 1/2 in do IRC), da base de brita de 4 in, da lona em rolos de 10 x 100 ft, da tela em painéis de 5 x 10 ft, do concreto pronto e do concreto usinado (caminhão), e termina com a legenda das siglas.
- **Lista de compras** (Finalizar com o LA-B2, botão Lista de compras do Resumo), no grupo MATERIAL BÁSICO:
  - Cimento: 44 sacos de 94 lb
  - Areia: 3.24 cu yd
  - Brita: 4.86 cu yd
  - Ou concreto pronto: 292 sacos de 80 lb (no lugar de cimento, areia e brita)
  - Ou concreto usinado (caminhão): 6.50 cu yd (no lugar de cimento, areia e brita)
  - Brita da base (4 in): 6.48 cu yd
  - Lona plástica (vapor retarder): 1 rolo de 10 x 100 ft
  - Tela soldada: 11 painéis de 5 x 10 ft
- **Lista de compras com Brocas e Laje juntas** (BR-B3 nas Brocas + LA-B2 na Laje): um "Cimento" só, somando as duas abas:
  - Cimento: 66 sacos de 94 lb
  - Areia: 4.84 cu yd
  - Brita: 7.26 cu yd
  - Ou concreto pronto: 436 sacos de 80 lb (no lugar de cimento, areia e brita)
  - Ou concreto usinado (caminhão): 6.50 cu yd (no lugar de cimento, areia e brita)
  - Aço/Ferragem: 201.3 lb (19 barras de 20 ft)
  - Arame recozido: 4.0 lb = 2 rolos de 3.5 lb
  - Brita da base (4 in): 6.48 cu yd
  - Lona plástica (vapor retarder): 1 rolo de 10 x 100 ft
  - Tela soldada: 11 painéis de 5 x 10 ft
  - Repare: o concreto usinado (6.50 cu yd) é só da Laje, mas fica logo embaixo do cimento somado. Se achar que confunde, me fale (não é pendência por enquanto).
- No Orçamento do Resumo: Brocas $ 1,447.78 e Laje $ 2,121.60.

---

# TELHADO (rodada 3b)

**43 casos** (montado em 15/11/2026). Todos devem dar OK. Ao montar, só apareceu uma pendência de texto da tela (P15, ver o pendencias_rodada3b.md), que nenhum caso confere.

**Como aparece** (confira se nenhuma dica fica cortada):

- Dimensões (Obrigatório)
- Área em planta, em sq ft (ex: 860)
- Tipo de telha: já vem **Shingle asfáltico** (opções: Shingle asfáltico e Telha de concreto)
- Inclinação (pitch) em x/12 (opcional, ex: 6): já vem **6/12**
- Cumeeira em ft (opcional, ex: 30)
- Perímetro em ft (opcional, ex: 140)
- Manta (underlayment) (Opcional): Sim · Não (já vem **Sim**)
- Base de OSB 4 x 8 ft (Opcional): Sim · Não (já vem **Não**)
- Taxa de Perda % (opcional, ex: 5): já vem **10** (**P15:** nos EUA a dica tem que ser "ex: 10")

## Teste A: todos os campos, opcionais trocados

#### TE-A

Digite: Área **1200**; Inclinação **8**; Cumeeira **40**; Perímetro **160**; Perda **15**; Base de OSB **Sim**.

```
Área em planta: 1,200.00 sq ft
Inclinação: 8/12 (66.7%)
Área do telhado: 1,442.22 sq ft
Tipo de telha: Shingle asfáltico
• Chapas de OSB 4 x 8 ft: 52 chapas ($ 1,040.00)
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Pingadeira (drip edge): 160.0 ft = 19 peças de 10 ft ($ 190.00)
• Starter (primeira fiada): 160.0 ft = 2 fardos de 120 ft ($ 110.00)
• Shingle asfáltico (com 15% de perda): 16.59 squares = 50 fardos ($ 2,000.00)
• Cumeeira: 40.0 ft = 2 fardos de 33.3 ft ($ 120.00)
• Pregos de telhado 1 1/4 in: 6 caixas de 5 lb ($ 108.00)

Custo Estimado da Etapa: $ 3,808.00
```

Todos os opcionais trocados (shingle, que é o padrão; a telha de concreto está nos B). 8/12 = 66,7%: área do telhado = 1,200 × √(1 + 0,667²) = **1,442.22 sq ft** × 1,15 = **16.59 squares** × 3 = 49,8 → **50 fardos**. OSB: 1,442.22 × 1,15 ÷ 32 = 51,8 → **52 chapas**. Cumeeira: 40 ÷ 33.3 = 1,2 → **2 fardos**. Pregos: 16.59 × 320 = 5,309 ÷ 978 = 5,4 → **6 caixas**.

## Teste B: só os obrigatórios (e variações)

#### TE-B

Digite: Área **860**.

```
Área em planta: 860.00 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 961.51 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Shingle asfáltico (com 10% de perda): 10.58 squares = 32 fardos ($ 1,280.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,592.00
```

Só a área: shingle, 6/12, manta Sim, OSB Não, sem cumeeira e sem perímetro (pingadeira, starter e cumeeira não aparecem). 860 × √(1 + 0,5²) = **961.51 sq ft** × 1,10 = **10.58 squares** × 3 = 31,7 → **32 fardos**. Manta: 1,057.7 ÷ 937.5 = 1,1 → **2 rolos**. Pregos: 10.58 × 320 = 3,385 ÷ 978 = 3,5 → **4 caixas**.

#### TE-B2

Digite: Área **860**; Cumeeira **30**; Perímetro **140**; Base de OSB **Sim**.

```
Área em planta: 860.00 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 961.51 sq ft
Tipo de telha: Shingle asfáltico
• Chapas de OSB 4 x 8 ft: 34 chapas ($ 680.00)
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Pingadeira (drip edge): 140.0 ft = 16 peças de 10 ft ($ 160.00)
• Starter (primeira fiada): 140.0 ft = 2 fardos de 120 ft ($ 110.00)
• Shingle asfáltico (com 10% de perda): 10.58 squares = 32 fardos ($ 1,280.00)
• Cumeeira: 30.0 ft = 1 fardo de 33.3 ft ($ 60.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 2,602.00
```

É o exemplo da Parte A (11/11/2026), conferido por você no app: **$ 2,602.00**.

#### TE-B3

Digite: Área **860**; Inclinação **6/12**.

```
Área em planta: 860.00 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 961.51 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Shingle asfáltico (com 10% de perda): 10.58 squares = 32 fardos ($ 1,280.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,592.00
```

"6/12" dá o mesmo que "6" (TE-B): o "/12" é tirado antes de ler o número.

#### TE-B4

Digite: Área **860**; Inclinação **3**.

```
Área em planta: 860.00 sq ft
Inclinação: 3/12 (25%)
Área do telhado: 886.47 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment), 2 camadas (abaixo de 4/12): 3 rolos de 10 squares ($ 360.00)
• Shingle asfáltico (com 10% de perda): 9.75 squares = 30 fardos ($ 1,200.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,632.00
```

Abaixo de 4/12, a manta vai em **2 camadas** (IRC): 3 rolos.

#### TE-B5

Digite: Área **860**; Manta **Não**.

```
Área em planta: 860.00 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 961.51 sq ft
Tipo de telha: Shingle asfáltico
• Shingle asfáltico (com 10% de perda): 10.58 squares = 32 fardos ($ 1,280.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,352.00
```

#### TE-B6

Digite: Área **860**; Tipo de telha **Telha de concreto**.

```
Área em planta: 860.00 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 961.51 sq ft
Tipo de telha: Telha de concreto
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Telha de concreto (com 10% de perda): 10.58 squares = 921 un ($ 4,144.50)

Custo Estimado da Etapa: $ 4,384.50
```

Telha de concreto: **87 telhas por square** (10.58 × 87 = 920,5 → 921). Sem pregos e sem starter.

#### TE-B7

Digite: Área **860**; Inclinação **3**; Cumeeira **30**; Tipo de telha **Telha de concreto**.

```
Área em planta: 860.00 sq ft
Inclinação: 3/12 (25%)
Área do telhado: 886.47 sq ft
Tipo de telha: Telha de concreto
• Manta (underlayment), 2 camadas (abaixo de 4/12): 3 rolos de 10 squares ($ 360.00)
• Telha de concreto (com 10% de perda): 9.75 squares = 849 un ($ 3,820.50)
• Cumeeira: 30.0 ft = 33 peças ($ 264.00)

Custo Estimado da Etapa: $ 4,444.50
```

É o outro exemplo da Parte A: **$ 4,444.50**. Cumeeira de concreto: 30 ft × 1 peça por ft × 1,10 = **33 peças**.

#### TE-B8

Digite: Área **860**; Cumeeira **30**.

```
Área em planta: 860.00 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 961.51 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Shingle asfáltico (com 10% de perda): 10.58 squares = 32 fardos ($ 1,280.00)
• Cumeeira: 30.0 ft = 1 fardo de 33.3 ft ($ 60.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,652.00
```

#### TE-B9

Digite: Área **860**; Perímetro **140**.

```
Área em planta: 860.00 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 961.51 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Pingadeira (drip edge): 140.0 ft = 16 peças de 10 ft ($ 160.00)
• Starter (primeira fiada): 140.0 ft = 2 fardos de 120 ft ($ 110.00)
• Shingle asfáltico (com 10% de perda): 10.58 squares = 32 fardos ($ 1,280.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,862.00
```

#### TE-B10

Digite: Área **860**; Perímetro **140**; Tipo de telha **Telha de concreto**.

```
Área em planta: 860.00 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 961.51 sq ft
Tipo de telha: Telha de concreto
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Pingadeira (drip edge): 140.0 ft = 16 peças de 10 ft ($ 160.00)
• Telha de concreto (com 10% de perda): 10.58 squares = 921 un ($ 4,144.50)

Custo Estimado da Etapa: $ 4,544.50
```

Na telha de concreto, o perímetro dá só a **pingadeira** (o starter é só do shingle).

#### TE-B11

Digite: Área **50**; Cumeeira **10**; Perímetro **30**.

```
Área em planta: 50.00 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 55.90 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 1 rolo de 10 squares ($ 120.00)
• Pingadeira (drip edge): 30.0 ft = 4 peças de 10 ft ($ 40.00)
• Starter (primeira fiada): 30.0 ft = 1 fardo de 120 ft ($ 55.00)
• Shingle asfáltico (com 10% de perda): 0.61 squares = 2 fardos ($ 80.00)
• Cumeeira: 10.0 ft = 1 fardo de 33.3 ft ($ 60.00)
• Pregos de telhado 1 1/4 in: 1 caixa de 5 lb ($ 18.00)

Custo Estimado da Etapa: $ 373.00
```

Confira o **singular**: "1 rolo", "1 fardo" e "1 caixa".

#### TE-B12

Digite: Área **860**; Inclinação **4**.

```
Área em planta: 860.00 sq ft
Inclinação: 4/12 (33.3%)
Área do telhado: 906.52 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Shingle asfáltico (com 10% de perda): 9.97 squares = 30 fardos ($ 1,200.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,512.00
```

4/12 já **não** é "abaixo de 4/12": manta em 1 camada.

#### TE-B13

Digite: Área **860**; Inclinação **12**.

```
Área em planta: 860.00 sq ft
Inclinação: 12/12 (100%)
Área do telhado: 1,216.22 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Shingle asfáltico (com 10% de perda): 13.38 squares = 41 fardos ($ 1,640.00)
• Pregos de telhado 1 1/4 in: 5 caixas de 5 lb ($ 90.00)

Custo Estimado da Etapa: $ 1,970.00
```

12/12 é o próprio limite: sem aviso.

## Teste C: erros de digitação e limites

#### TE-C1

Digite: Área **(vazio)**.

```
Por favor, digite números válidos nos campos!
```

#### TE-C2

Digite: Área **oitocentos**.

```
Por favor, digite números válidos nos campos!
```

#### TE-C3

Digite: Área **0**.

```
Erro: A área deve ser maior que zero.
```

#### TE-C4

Digite: Área **-860**.

```
Erro: A área deve ser maior que zero.
```

#### TE-C5

Digite: Área **860,5**.

```
Área em planta: 860.50 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 962.07 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Shingle asfáltico (com 10% de perda): 10.58 squares = 32 fardos ($ 1,280.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,592.00
```

#### TE-C6

Digite: Área **860.5**.

```
Área em planta: 860.50 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 962.07 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Shingle asfáltico (com 10% de perda): 10.58 squares = 32 fardos ($ 1,280.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,592.00
```

#### TE-C7

Digite: Área **860 1/2**.

```
Área em planta: 860.50 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 962.07 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Shingle asfáltico (com 10% de perda): 10.58 squares = 32 fardos ($ 1,280.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,592.00
```

#### TE-C8

Digite: Área **1,500**.

```
Área em planta: 1,500.00 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 1,677.05 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Shingle asfáltico (com 10% de perda): 18.45 squares = 56 fardos ($ 2,240.00)
• Pregos de telhado 1 1/4 in: 7 caixas de 5 lb ($ 126.00)

Custo Estimado da Etapa: $ 2,606.00
```

#### TE-C9

Digite: Área **860**; Inclinação **(vazio)**.

```
Área em planta: 860.00 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 961.51 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Shingle asfáltico (com 10% de perda): 10.58 squares = 32 fardos ($ 1,280.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,592.00
```

Inclinação apagada = **6/12**, igual ao TE-B.

#### TE-C10-cancelar

Digite: Área **860**; Inclinação **1 1/2**. Na janela, toque em **Cancelar**.

```
[JANELA] Inclinação de 1.5/12: o mínimo para shingle asfáltico é 2/12 (código IRC).
[Cancelar] não calculou
```

#### TE-C10-continuar

Digite: Área **860**; Inclinação **1 1/2**. Na janela, toque em **Continuar**.

```
[JANELA] Inclinação de 1.5/12: o mínimo para shingle asfáltico é 2/12 (código IRC).
Área em planta: 860.00 sq ft
Inclinação: 1.5/12 (12.5%)
Área do telhado: 866.69 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment), 2 camadas (abaixo de 4/12): 3 rolos de 10 squares ($ 360.00)
• Shingle asfáltico (com 10% de perda): 9.53 squares = 29 fardos ($ 1,160.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,592.00
```

#### TE-C11

Digite: Área **860**; Inclinação **2**.

```
Área em planta: 860.00 sq ft
Inclinação: 2/12 (16.7%)
Área do telhado: 871.86 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment), 2 camadas (abaixo de 4/12): 3 rolos de 10 squares ($ 360.00)
• Shingle asfáltico (com 10% de perda): 9.59 squares = 29 fardos ($ 1,160.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,592.00
```

2/12 é o próprio mínimo do shingle: sem aviso.

#### TE-C12

Digite: Área **860**; Inclinação **2**; Tipo de telha **Telha de concreto**. Na janela, toque em **Continuar**.

```
[JANELA] Inclinação de 2/12: o mínimo para telha de concreto é 2.5/12 (código IRC).
Área em planta: 860.00 sq ft
Inclinação: 2/12 (16.7%)
Área do telhado: 871.86 sq ft
Tipo de telha: Telha de concreto
• Manta (underlayment), 2 camadas (abaixo de 4/12): 3 rolos de 10 squares ($ 360.00)
• Telha de concreto (com 10% de perda): 9.59 squares = 835 un ($ 3,757.50)

Custo Estimado da Etapa: $ 4,117.50
```

#### TE-C13

Digite: Área **860**; Inclinação **2 1/2**; Tipo de telha **Telha de concreto**.

```
Área em planta: 860.00 sq ft
Inclinação: 2.5/12 (20.8%)
Área do telhado: 878.46 sq ft
Tipo de telha: Telha de concreto
• Manta (underlayment), 2 camadas (abaixo de 4/12): 3 rolos de 10 squares ($ 360.00)
• Telha de concreto (com 10% de perda): 9.66 squares = 841 un ($ 3,784.50)

Custo Estimado da Etapa: $ 4,144.50
```

2 1/2/12 é o próprio mínimo da telha de concreto: sem aviso.

#### TE-C14

Digite: Área **860**; Inclinação **14**. Na janela, toque em **Continuar**.

```
[JANELA] Inclinação de 14/12: o limite é 12/12.
Área em planta: 860.00 sq ft
Inclinação: 14/12 (116.7%)
Área do telhado: 1,321.47 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Shingle asfáltico (com 10% de perda): 14.54 squares = 44 fardos ($ 1,760.00)
• Pregos de telhado 1 1/4 in: 5 caixas de 5 lb ($ 90.00)

Custo Estimado da Etapa: $ 2,090.00
```

#### TE-C15

Digite: Área **860**; Inclinação **12 1/2**. Na janela, toque em **Continuar**.

```
[JANELA] Inclinação de 12.5/12: o limite é 12/12.
Área em planta: 860.00 sq ft
Inclinação: 12.5/12 (104.2%)
Área do telhado: 1,241.82 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Shingle asfáltico (com 10% de perda): 13.66 squares = 41 fardos ($ 1,640.00)
• Pregos de telhado 1 1/4 in: 5 caixas de 5 lb ($ 90.00)

Custo Estimado da Etapa: $ 1,970.00
```

#### TE-C16

Digite: Área **860**; Inclinação **6.5**.

```
Área em planta: 860.00 sq ft
Inclinação: 6.5/12 (54.2%)
Área do telhado: 978.06 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Shingle asfáltico (com 10% de perda): 10.76 squares = 33 fardos ($ 1,320.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,632.00
```

#### TE-C17

Digite: Área **860**; Inclinação **0**. Na janela, toque em **Continuar**.

```
[JANELA] Inclinação de 0/12: o mínimo para shingle asfáltico é 2/12 (código IRC).
Área em planta: 860.00 sq ft
Inclinação: 0/12 (0%)
Área do telhado: 860.00 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment), 2 camadas (abaixo de 4/12): 3 rolos de 10 squares ($ 360.00)
• Shingle asfáltico (com 10% de perda): 9.46 squares = 29 fardos ($ 1,160.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,592.00
```

Inclinação 0 (telhado plano) não é erro: dá o aviso do mínimo e, com Continuar, calcula.

#### TE-C18

Digite: Área **860**; Inclinação **-6**.

```
Erro: Os valores não podem ser negativos.
```

#### TE-C19

Digite: Área **860**; Inclinação **seis**.

```
Por favor, digite números válidos nos campos!
```

#### TE-C20

Digite: Área **860**; Cumeeira **-30**.

```
Erro: Os valores não podem ser negativos.
```

#### TE-C21

Digite: Área **860**; Perímetro **-140**.

```
Erro: Os valores não podem ser negativos.
```

#### TE-C22

Digite: Área **860**; Perímetro **abc**.

```
Por favor, digite números válidos nos campos!
```

#### TE-C23

Digite: Área **860**; Perda **-5**.

```
Erro: Os valores não podem ser negativos.
```

#### TE-C24

Digite: Área **860**; Perda **(vazio)**.

```
Área em planta: 860.00 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 961.51 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Shingle asfáltico (com 10% de perda): 10.58 squares = 32 fardos ($ 1,280.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,592.00
```

Perda apagada = **10%**, igual ao TE-B.

#### TE-C25

Digite: Área **860**; Perda **2.5**.

```
Área em planta: 860.00 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 961.51 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 2 rolos de 10 squares ($ 240.00)
• Shingle asfáltico (com 2.5% de perda): 9.86 squares = 30 fardos ($ 1,200.00)
• Pregos de telhado 1 1/4 in: 4 caixas de 5 lb ($ 72.00)

Custo Estimado da Etapa: $ 1,512.00
```

#### TE-C26

Digite: Área **21528**.

```
Área em planta: 21,528.00 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 24,069.04 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 29 rolos de 10 squares ($ 3,480.00)
• Shingle asfáltico (com 10% de perda): 264.76 squares = 795 fardos ($ 31,800.00)
• Pregos de telhado 1 1/4 in: 87 caixas de 5 lb ($ 1,566.00)

Custo Estimado da Etapa: $ 36,846.00
```

21,528 sq ft é o próprio limite: sem aviso.

#### TE-C27

Digite: Área **25000**. Na janela, toque em **Continuar**.

```
[JANELA] Área de 25,000 sq ft: o limite é 21,528 sq ft.
Área em planta: 25,000.00 sq ft
Inclinação: 6/12 (50%)
Área do telhado: 27,950.85 sq ft
Tipo de telha: Shingle asfáltico
• Manta (underlayment): 33 rolos de 10 squares ($ 3,960.00)
• Shingle asfáltico (com 10% de perda): 307.46 squares = 923 fardos ($ 36,920.00)
• Pregos de telhado 1 1/4 in: 101 caixas de 5 lb ($ 1,818.00)

Custo Estimado da Etapa: $ 42,698.00
```

#### TE-C28

Digite: Área **1-21/2**.

```
Por favor, digite números válidos nos campos!
```

## Visual (Telhado)

- O menu "Tipo de telha" só tem **Shingle asfáltico** (já vem escolhido) e **Telha de concreto** (sem cerâmica e sem fibrocimento).
- Inclinação vem com **6/12**, perda com **10**; manta **Sim**, OSB **Não**. O campo **Perímetro** aparece e o **Madeiramento não aparece**.
- A dica do perímetro ("Perímetro em ft (opcional, ex: 140)") não fica cortada.
- Ao trocar para Telha de concreto, a inclinação continua 6/12.
- No resultado, nenhum m², m, %, "telhas" do Brasil (cerâmica), ripa, caibro, terça ou vírgula decimal; a inclinação aparece "6/12 (50%)".
- "?" do Telhado: explica o pitch, o shingle sobre OSB e manta, o square (100 sq ft), os mínimos do IRC (2/12 e 2 1/2/12), a manta em 2 camadas abaixo de 4/12, a cumeeira, o perímetro (beirais e oitões) com a pingadeira e o starter, os pregos e a perda de 10% (15% no telhado de quatro águas), e termina com a legenda das siglas.
- **Lista de compras** (Finalizar com o TE-B2), no grupo MATERIAL BÁSICO:
  - Shingle asfáltico: 32 fardos
  - Cumeeira: 1 fardo de 33.3 ft
  - Manta (underlayment): 2 rolos de 10 squares
  - Chapas de OSB 4 x 8 ft: 34 chapas
  - Pingadeira (drip edge): 16 peças de 10 ft
  - Starter (primeira fiada): 2 fardos de 120 ft
  - Pregos de telhado 1 1/4 in: 4 caixas de 5 lb
- **Lista de compras da telha de concreto** (Finalizar com o TE-B7): Telha de concreto: 849 un · Cumeeira: 33 peças · Manta (underlayment): 3 rolos de 10 squares.
- No Orçamento do Resumo: Telhado **$ 2,602.00** (TE-B2) ou **$ 4,444.50** (TE-B7).
- **PDF** (botão Gerar PDF do Resumo, com o TE-B2, opção "Os dois juntos"): o Telhado com as mesmas linhas da aba e a lista de compras igual à de cima.

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

# Para o rodada3.py (Leo do terminal)

- **Desde o fechamento (06/11/2026), os 162 casos antigos têm o esperado no ESPERADO dentro do rodada3.py.** **Na rodada 3b (desde 15/11/2026), quem atualiza o rodada3.py é o Leo do terminal**, aba por aba: entram os casos novos da lista abaixo ("RODADA 3b") e o PADRAO da aba, e o esperado deles é lido daqui, deste roteiro (os 162 antigos continuam com o ESPERADO de dentro). O test_rodada3.py só é atualizado no fim da 3b, junto com o ESPERADO dos casos novos (decisão da Gabi, 15/11/2026). Em cada aba, depois de rodar, ele **só lista** para a Gabi as pendências (os DIFERENTE, novos ou já com ⚠️ no roteiro, e o que mais achar estranho) e o visual que só ela pode testar no app; **não corrige nada** e não precisa do pendencias_rodada3b.md (quem anota lá é a Gabi com o Leo do chat). O jeito de ler o esperado daqui é o mesmo da rodada 3:
- **Como ler o esperado deste arquivo:** cada caso começa numa linha `#### <NOME>` (o nome vai até o primeiro espaço; o "⚠️ P1..." depois era só aviso) e o esperado é o **primeiro bloco** entre ``` logo abaixo. Linhas `[JANELA]`, `[Cancelar] não calculou`, `[BOTÃO]` e `[CAMPOS]` fazem parte do esperado, igual no rodada2.py.
- **Valores padrão dos EUA (PADRAO do rodada3.py):** os opcionais que já vêm preenchidos no app dos EUA:
  - brocas (3b): perda "10", esp_estribo **"8"** (in); a bitola #4 vem do reiniciar
  - paredes (3b): junta **"3/8"** (in), quebra "5"; o bloco CMU 8x8x16 vem do reiniciar
  - laje (3b): esp_slab **"4"** (in), perda "5"; tela Não, lona e base Sim vêm do reiniciar
  - telhado (3b): incl **"6"** (pitch), perda **"10"**; o shingle, a manta Sim e o OSB Não vêm do reiniciar
  - baldrame: perda "5", esp_estribo **"8"** (in)
  - piso e azulejo: nada (perda vazia = automática; A118.1 no Piso e A118.4 no Azulejo vêm do reiniciar, já com o país EUA)
  - rejunte: esp **"5/16"**, perda "10"
  - pintura: demaos "2", rend **"400"**, perda "10"
- **Trocar o país do mesmo jeito que o app:** chamar o próprio `SettingsScreen.alternar_pais` com um objeto falso no lugar da tela (manager=None), **antes** de criar as telas (o reiniciar escolhe a argamassa pelo país). O idioma continua "pt".
- **No test_rodada3.py:** fica para o fim da 3b. Atenção: enquanto os casos novos não têm ESPERADO dentro do rodada3.py, o pytest daria erro neles; por isso, ao colocar os casos no rodada3.py, eles precisam ficar fora do pytest até o fechamento (ver o passo 3 de "Como montar a rodada 3b" no plano). Do fechamento da rodada 3: guardar uma cópia do CONFIG_APP e dos campos da TABELA_PRECOS_GLOBAL **antes** de carregar o rodada3.py, colocar tudo de volta logo depois (apagando o `mao_obra_m2`, que o alternar_pais cria) e ligar os EUA só durante cada caso (fixture com monkeypatch), igual à fixture do inglês na rodada 2. Não usar o alternar_pais para voltar: ele volta com o PRECOS_BR (cimento 32, brita 95), e não com os preços iniciais (36 e 120), e quebraria as rodadas 1 e 2.
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
     {"traco": "1:3:3", "bitola": 15.875, "imperm": True})
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

# ===== RODADA 3b =====
# BROCAS (rodada 3b)
BR = {"qtd": "10", "diam": "12", "prof": "10"}
caso("BR-A", "brocas", {"qtd": "12", "diam": "14", "prof": "12", "perda": "8", "mo": "9.50", "barras": "6", "esp_estribo": "6"},
     {"traco": "1:3:3", "bitola": 15.875})
caso("BR-B", "brocas", BR)
caso("BR-B2", "brocas", {**BR, "barras": "4"})
caso("BR-B3", "brocas", {**BR, "barras": "4", "mo": "8.00"})
caso("BR-B4", "brocas", {**BR, "barras": "4"}, {"bitola": 9.525})
caso("BR-B5", "brocas", {**BR, "barras": "4"}, {"bitola": 15.875})
caso("BR-B6", "brocas", BR, {"traco": "1.5:5:5"})
caso("BR-B7", "brocas", {**BR, "mo": "8.00"})
caso("BR-B8", "brocas", {"qtd": "1", "diam": "8", "prof": "3", "barras": "3"})
caso("BR-B9", "brocas", {"qtd": "40", "diam": "16", "prof": "20", "barras": "6"})
caso("BR-C1", "brocas", {**BR, "qtd": ""})
caso("BR-C2", "brocas", {**BR, "diam": ""})
caso("BR-C3", "brocas", {**BR, "prof": ""})
caso("BR-C4", "brocas", {**BR, "qtd": "dez"})
caso("BR-C5", "brocas", {**BR, "qtd": "0"})
caso("BR-C6", "brocas", {**BR, "diam": "0"})
caso("BR-C7", "brocas", {**BR, "prof": "-10"})
caso("BR-C8", "brocas", {**BR, "qtd": "-10"})
caso("BR-C9", "brocas", {**BR, "qtd": "2.5"})
caso("BR-C10", "brocas", {**BR, "prof": "10,5"})
caso("BR-C11", "brocas", {**BR, "prof": "10.5"})
caso("BR-C12", "brocas", {**BR, "prof": "10 1/2", "barras": "4"})
caso("BR-C13", "brocas", {**BR, "diam": "11 3/4"})
caso("BR-C14", "brocas", {**BR, "perda": "-5"})
caso("BR-C15", "brocas", {**BR, "perda": "2.5"})
caso("BR-C16", "brocas", {**BR, "barras": "-4"})
caso("BR-C17", "brocas", {**BR, "barras": "4.5"})
caso("BR-C18", "brocas", {**BR, "barras": "4", "esp_estribo": ""})
caso("BR-C19", "brocas", {**BR, "barras": "4", "esp_estribo": "4 1/2"})
caso("BR-C20", "brocas", {**BR, "barras": "4", "esp_estribo": "-8"})
caso("BR-C21", "brocas", {**BR, "mo": "oito"})
caso("BR-C22", "brocas", {**BR, "mo": "-8"})
caso("BR-C23", "brocas", {**BR, "diam": "6", "barras": "4"})
caso("BR-C24", "brocas", {**BR, "diam": "6", "barras": "4", "esp_estribo": ""})
caso("BR-C25", "brocas", {**BR, "prof": "98.43"})
caso("BR-C26-cancelar", "brocas", {**BR, "prof": "99"}, continuar=False)
caso("BR-C26-continuar", "brocas", {**BR, "prof": "99"})
caso("BR-C27", "brocas", {**BR, "prof": "98 1/2"})
caso("BR-C28", "brocas", {**BR, "prof": "1-21/2"})
caso("BR-C29", "brocas", {**BR, "qtd": "1,000"})

# BALDRAME (rodada 3b, o ferro; usa o BA = {...} de cima, da rodada 3)
caso("BA-F1", "baldrame", {**BA, "barras": "4"}, {"bitola": 9.525})
caso("BA-F2", "baldrame", {**BA, "barras": "4"}, {"bitola": 15.875})
caso("BA-F3", "baldrame", {**BA, "comp": "20", "barras": "4"})
caso("BA-F4", "baldrame", {**BA, "comp": "21", "barras": "4"})
caso("BA-F5", "baldrame", {**BA, "comp": "60", "barras": "4"}, {"bitola": 15.875})
caso("BA-F6", "baldrame", {**BA, "comp": "100", "barras": "4", "esp_estribo": "6"})
caso("BA-F7", "baldrame", {"comp": "250", "larg": "12", "alt": "16", "barras": "6", "esp_estribo": "10", "mo": "6.50"},
     {"traco": "1:4:3", "bitola": 9.525, "imperm": True})
caso("BA-F8", "baldrame", {**BA, "barras": "2"})
caso("BA-F9", "baldrame", {**BA, "barras": "4", "esp_estribo": "0"})
caso("BA-F10", "baldrame", {**BA, "mo": "-8"})
caso("BA-F11", "baldrame", {**BA, "barras": "4", "esp_estribo": "-6"})
caso("BA-F12", "baldrame", {**BA, "comp": "1", "barras": "4"})

# PAREDES (rodada 3b)
PA = {"area": "320"}
caso("PA-A", "paredes", {"area": "640", "vaos": "80", "junta": "1/2", "quebra": "10"})
caso("PA-B", "paredes", PA)
caso("PA-B2", "paredes", {**PA, "vaos": "50"})
caso("PA-B3", "paredes", {**PA, "junta": "1/4"})
caso("PA-B4", "paredes", {**PA, "quebra": "8"})
caso("PA-B5", "paredes", {"area": "4"})
caso("PA-B6", "paredes", {"area": "5000"})
caso("PA-C1", "paredes", {"area": ""})
caso("PA-C2", "paredes", {"area": "trezentos"})
caso("PA-C3", "paredes", {"area": "0"})
caso("PA-C4", "paredes", {"area": "-320"})
caso("PA-C5", "paredes", {**PA, "vaos": "-50"})
caso("PA-C6", "paredes", {**PA, "vaos": "320"})
caso("PA-C7", "paredes", {**PA, "vaos": "400"})
caso("PA-C8", "paredes", {**PA, "vaos": "abc"})
caso("PA-C9", "paredes", {"area": "320,5"})
caso("PA-C10", "paredes", {"area": "320.5"})
caso("PA-C11", "paredes", {"area": "320 1/2"})
caso("PA-C12", "paredes", {"area": "1,500"})
caso("PA-C13", "paredes", {**PA, "junta": "-3/8"})
caso("PA-C14", "paredes", {**PA, "quebra": "-5"})
caso("PA-C15", "paredes", {**PA, "quebra": "2.5"})
caso("PA-C16", "paredes", {**PA, "junta": "0"})
caso("PA-C17", "paredes", {**PA, "junta": "3/16"})
caso("PA-C18", "paredes", {**PA, "junta": "1/8"})
caso("PA-C19", "paredes", {**PA, "junta": "1 3/16"})
caso("PA-C20", "paredes", {**PA, "junta": "1 1/4"})
caso("PA-C21", "paredes", {**PA, "junta": "1 5/16"})
caso("PA-C22-cancelar", "paredes", {**PA, "junta": "1 1/2"}, continuar=False)
caso("PA-C22-continuar", "paredes", {**PA, "junta": "1 1/2"})
caso("PA-C23", "paredes", {**PA, "quebra": "20"})
caso("PA-C24", "paredes", {**PA, "quebra": "25"})
caso("PA-C25", "paredes", {"area": "21528"})
caso("PA-C26", "paredes", {"area": "21529"})
caso("PA-C27", "paredes", {"area": "1-21/2"})
caso("PA-C28", "paredes", {**PA, "junta": ""})
caso("PA-C29", "paredes", {**PA, "quebra": ""})
caso("PA-C30", "paredes", {**PA, "vaos": "50 1/2"})

# LAJE (rodada 3b)
LA = {"area": "500"}
caso("LA-A", "laje", {"area": "1200", "esp_slab": "6", "perda": "8"}, {"traco": "1:3:3", "tela": True, "lona": False, "base_brita": False})
caso("LA-B", "laje", LA)
caso("LA-B2", "laje", LA, {"tela": True})
caso("LA-B3", "laje", LA, {"lona": False})
caso("LA-B4", "laje", LA, {"base_brita": False})
caso("LA-B5", "laje", LA, {"lona": False, "base_brita": False})
caso("LA-B6", "laje", {**LA, "esp_slab": "5"})
caso("LA-B7", "laje", LA, {"traco": "1.5:5:5"})
caso("LA-B8", "laje", {"area": "20"}, {"tela": True})
caso("LA-B9", "laje", {"area": "10000"}, {"tela": True})
caso("LA-C1", "laje", {"area": ""})
caso("LA-C2", "laje", {"area": "quinhentos"})
caso("LA-C3", "laje", {"area": "0"})
caso("LA-C4", "laje", {"area": "-500"})
caso("LA-C5", "laje", {"area": "500,5"})
caso("LA-C6", "laje", {"area": "500.5"})
caso("LA-C7", "laje", {"area": "500 1/2"})
caso("LA-C8", "laje", {"area": "1,500"})
caso("LA-C9", "laje", {**LA, "esp_slab": ""})
caso("LA-C10", "laje", {**LA, "esp_slab": "0"})
caso("LA-C11", "laje", {**LA, "esp_slab": "-4"})
caso("LA-C12-cancelar", "laje", {**LA, "esp_slab": "3"}, continuar=False)
caso("LA-C12-continuar", "laje", {**LA, "esp_slab": "3"})
caso("LA-C13", "laje", {**LA, "esp_slab": "3 7/16"})
caso("LA-C14", "laje", {**LA, "esp_slab": "3 1/2"})
caso("LA-C15", "laje", {**LA, "esp_slab": "8"})
caso("LA-C16", "laje", {**LA, "esp_slab": "8 1/8"})
caso("LA-C17", "laje", {**LA, "esp_slab": "10"})
caso("LA-C18", "laje", {**LA, "esp_slab": "quatro"})
caso("LA-C19", "laje", {**LA, "perda": "-5"})
caso("LA-C20", "laje", {**LA, "perda": "2.5"})
caso("LA-C21", "laje", {**LA, "perda": ""})
caso("LA-C22", "laje", {"area": "21528"})
caso("LA-C23", "laje", {"area": "21529"})
caso("LA-C24", "laje", {"area": "25000", "esp_slab": "10"})
caso("LA-C25", "laje", {"area": "1-21/2"})

# TELHADO (rodada 3b; "telha_tipo" é a telha escolhida no menu)
TE = {"area": "860"}
caso("TE-A", "telhado", {"area": "1200", "incl": "8", "cumeeira": "40", "perimetro": "160", "perda": "15"}, {"osb": True})
caso("TE-B", "telhado", TE)
caso("TE-B2", "telhado", {**TE, "cumeeira": "30", "perimetro": "140"}, {"osb": True})
caso("TE-B3", "telhado", {**TE, "incl": "6/12"})
caso("TE-B4", "telhado", {**TE, "incl": "3"})
caso("TE-B5", "telhado", TE, {"manta": False})
caso("TE-B6", "telhado", TE, {"telha_tipo": "concreto"})
caso("TE-B7", "telhado", {**TE, "incl": "3", "cumeeira": "30"}, {"telha_tipo": "concreto"})
caso("TE-B8", "telhado", {**TE, "cumeeira": "30"})
caso("TE-B9", "telhado", {**TE, "perimetro": "140"})
caso("TE-B10", "telhado", {**TE, "perimetro": "140"}, {"telha_tipo": "concreto"})
caso("TE-B11", "telhado", {"area": "50", "cumeeira": "10", "perimetro": "30"})
caso("TE-B12", "telhado", {**TE, "incl": "4"})
caso("TE-B13", "telhado", {**TE, "incl": "12"})
caso("TE-C1", "telhado", {"area": ""})
caso("TE-C2", "telhado", {"area": "oitocentos"})
caso("TE-C3", "telhado", {"area": "0"})
caso("TE-C4", "telhado", {"area": "-860"})
caso("TE-C5", "telhado", {"area": "860,5"})
caso("TE-C6", "telhado", {"area": "860.5"})
caso("TE-C7", "telhado", {"area": "860 1/2"})
caso("TE-C8", "telhado", {"area": "1,500"})
caso("TE-C9", "telhado", {**TE, "incl": ""})
caso("TE-C10-cancelar", "telhado", {**TE, "incl": "1 1/2"}, continuar=False)
caso("TE-C10-continuar", "telhado", {**TE, "incl": "1 1/2"})
caso("TE-C11", "telhado", {**TE, "incl": "2"})
caso("TE-C12", "telhado", {**TE, "incl": "2"}, {"telha_tipo": "concreto"})
caso("TE-C13", "telhado", {**TE, "incl": "2 1/2"}, {"telha_tipo": "concreto"})
caso("TE-C14", "telhado", {**TE, "incl": "14"})
caso("TE-C15", "telhado", {**TE, "incl": "12 1/2"})
caso("TE-C16", "telhado", {**TE, "incl": "6.5"})
caso("TE-C17", "telhado", {**TE, "incl": "0"})
caso("TE-C18", "telhado", {**TE, "incl": "-6"})
caso("TE-C19", "telhado", {**TE, "incl": "seis"})
caso("TE-C20", "telhado", {**TE, "cumeeira": "-30"})
caso("TE-C21", "telhado", {**TE, "perimetro": "-140"})
caso("TE-C22", "telhado", {**TE, "perimetro": "abc"})
caso("TE-C23", "telhado", {**TE, "perda": "-5"})
caso("TE-C24", "telhado", {**TE, "perda": ""})
caso("TE-C25", "telhado", {**TE, "perda": "2.5"})
caso("TE-C26", "telhado", {"area": "21528"})
caso("TE-C27", "telhado", {"area": "25000"})
caso("TE-C28", "telhado", {"area": "1-21/2"})
```
