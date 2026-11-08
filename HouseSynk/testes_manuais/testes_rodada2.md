# Testes da Rodada 2 (Brasil, inglês): Brocas até Esquadrias

Criado em 04/11/2026. **A versão principal fica no PC da Gabi** (testes_manuais\testes_rodada2.md, na pasta do app).

As contas são as mesmas da rodada 1: o que muda é o idioma. Todos os resultados abaixo foram tirados rodando o código real (com a parte 0 já colada), com o app em inglês e os mesmos preços iniciais da rodada 1. O roteiro (o que digitar) é o mesmo da rodada 1; o que você confere agora é o **texto em inglês**.

## Antes de começar

1. Cole os arquivos da parte 0 e rode o pytest: tem que dar **540 passed**.
2. No app: **Configurações** → País **BR (R$)** → botão **Idioma** até aparecer **"Language: English"**.
3. Dê **Clear** (Clear) antes de cada teste, igual na rodada 1.

## O que olhar em toda aba (foco da rodada 2)

- **Nenhuma palavra em português** no resultado, nas dicas dos campos, nos títulos, nos menus, nos botões, no "?" e nas janelas.
- **Nenhuma chave aparecendo no lugar do texto** (ex.: "erro_perda_negativa", "label_xxx", "hint_xxx"). Se aparecer, é texto que faltou no comum.py: me manda o print.
- **Mensagens de erro** em inglês, começando com "Error:" (ex.: "Error: Waste cannot be negative.").
- **Estribos** com "@": "Stirrups 5 mm @ 20 cm" (em português continua "c/").
- **Janela de limite:** título "Check the values", pergunta "Do you want to continue anyway?", botões "Cancel" e "Continue".
- **Limpar:** a janela pergunta "Clear the data in this tab? Other tabs will not be affected." com "Cancel" e "Confirm".
- **Antes de calcular** aparece "Fill in the fields and click calculate.".
- **Plural:** "1 bag", "2 bags", "1 roll of 50 m", "1 pail of 18 L".
- **Etapas no topo:** "1. Structure", "2. Installations", "3. Finishing".
- Textos em inglês que dizem "(Optional)" ou "(optional)" e dicas com "(e.g. 10)".

**Não é erro:** no Brasil os números continuam com **vírgula** e com R$ mesmo em inglês ("2,309 m³", "R$ 2.844,20"), porque o separador e a moeda seguem o **país**, não o idioma (regra 13 da especificação). Os exemplos dentro das dicas usam ponto ("e.g. 3.0"), e o app aceita os dois jeitos de digitar.

**O que a parte 0 mudou (04/11/2026):** as mensagens de erro das contas viraram chaves traduzidas pelo txt(); "Erro:" e "c/" passaram pelo txt(); e, no inglês, as embalagens ficaram na ordem do inglês ("4 rolls of 50 m", e não "4 50 m rolls"), "un" virou "pcs", "peça" da cumeeira e do rodapé virou "piece" e "ex:" virou "e.g.". Em português nada mudou (rodada 1: 353 OK).

**O que a parte 1 das correções mudou (05/11/2026, pendências 1, 2, 5, 7, 9, 10, 11, 13, 14, 15 e 16):** só textos do inglês no comum.py. Brocas virou "Piles" em tudo; "Steel Rebar" virou "Total rebar"; "EPS (styrofoam)" virou "EPS foam"; chuveiros com "5.500 W"; conexões "(estimated)"; Contrapiso virou "Floor screed"; só a primeira letra maiúscula ("Total volume", "Plaster volume", "Labor cost", "Estimated stage cost", "Waste rate %"); frase das classes AC-I, AC-II e AC-III no "?" do Piso e do Azulejo; dica "Baseboard piece in m" (a primeira versão, "Baseboard piece length, in m", ficou cortada no app); tinta e impermeabilizante em "pail of 18 L" e "can of 3,6 L"; massa "None". Esperados deste arquivo atualizados com as mesmas trocas. Em português nada mudou (rodada 1: 353 OK).

**O que a parte 2 das correções mudou (05/11/2026, pendências 4 e 6):** no inglês, os tijolos aparecem só com as unidades ("788 pcs"), sem o parêntese do milheiro (na aba, na lista de compras e no PDF); "pieces" e "piece" viraram "pcs" e "pc" ("33 pcs", "56 pcs of 0,60 m"); e quantidade 1 ficou no singular ("1 pc"). Esperados deste arquivo atualizados com as mesmas trocas. Em português nada mudou (rodada 1: 353 OK).

**O que a parte 3 das correções mudou (05/11/2026, pendências 3, 12 e 17; estas mudam também o português e a rodada 1):** Baldrame com comprimento, largura ou altura zero ou negativo: "Error: Length, width and height must be greater than zero."; Piso e Azulejo sem repetir a palavra: "Boxes: 21 (2,16 m² per box)"; Esquadrias com custo: uma linha em branco entre o "Estimated stage cost" e a frase "Doors and windows: use this list...". Esperados deste arquivo, do testes_rodada1.md e do rodada1.py atualizados com as mesmas trocas.

---

# BROCAS (Piles)

**Como aparece em inglês** (confira se nenhuma dica fica cortada):

- Dimensions (Required)
- Number of piles (e.g. 10)
- Diameter in cm (e.g. 20)
- Average depth in meters (e.g. 3.0)
- Concrete mix (cement:sand:gravel) (Optional)
- Waste rate % (optional, e.g. 10)
- Labor cost per meter (optional, e.g. 25.00)
- Rebar (Optional)
- Rebars per pile (optional, e.g. 4)
- Rebar size (mm)
- Stirrup spacing in cm (e.g. 20)
- Opções dos menus: Yes · No

### Teste A: todos os campos, opcionais trocados

| Campo | Digite / escolha |
|---|---|
| Quantidade | 12 |
| Diâmetro | 25 |
| Profundidade | 3,5 |
| Traço | 1:3:3 |
| Perda | 12 |
| Mão de obra | 30,00 |
| Nº de barras | 4 |
| Bitola | 10 mm |
| Espaçamento dos estribos | 15 |

```
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

Estimated stage cost: R$ 2.844,20
```

Pra entender: a gaiola vai até a metade da broca (3,5 ÷ 2 = 1,75 m). O estribo é uma espiral dentro do cobrimento de 3 cm (diâmetro de dentro: 25 − 2 × 3 = 19 cm). O arame mostra "1,4 kg", mas a conta usa 1,44 kg. Por isso dá R$ 21,60, e não R$ 21,00. Não é erro.

### Teste B: só os obrigatórios

Quantidade 10, Diâmetro 20, Profundidade 3. O resto fica como vem (perda 10, espaçamento 20, barras e mão de obra vazios).

```
Mix: 1:2:3
Total volume (with 10% waste): 1,037 m³
• Cement: 8 bags of 50 kg (R$ 288,00)
• Sand: 0,52 m³ (R$ 57,20)
• Gravel: 0,78 m³ (R$ 93,60)

Estimated stage cost: R$ 438,80
```

**B2:** igual ao B, só acrescente 4 barras (confere o espaçamento padrão de 20):

```
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

Estimated stage cost: R$ 756,16
```

### Teste C: erros de digitação

Base: Quantidade 10, Diâmetro 20, Profundidade 3. Mude só o indicado.

| # | O que mudar | Esperado na tela (em inglês) |
|---|---|---|
| C1 | Quantidade vazia | Please enter valid numbers in the fields! |
| C2 | Quantidade = dez | Please enter valid numbers in the fields! |
| C3 | Quantidade = 0 | Error: Quantity, depth and diameter must be greater than zero. |
| C4 | Profundidade = -3 | Error: Quantity, depth and diameter must be greater than zero. |
| C5 | Quantidade = 2,5 | Please enter valid numbers in the fields! |
| C6, C7, C8 | Profundidade = 2,5, depois 2.5, depois 2 1/2 (com espaço) | Todos: "Total volume (with 10% waste): 0,864 m³"; "• Cement: 7 bags of 50 kg (R$ 252,00)"; "• Sand: 0,43 m³ (R$ 47,30)"; "• Gravel: 0,65 m³ (R$ 78,00)"; "Estimated stage cost: R$ 377,30" |
| C9 | Perda = -5 | Error: Waste cannot be negative. |
| C10 | Perda = 2,5 | "Total volume (with 2,5% waste): 0,966 m³"; "• Sand: 0,48 m³ (R$ 52,80)"; "• Gravel: 0,72 m³ (R$ 86,40)"; "Estimated stage cost: R$ 427,20" |
| C11 | Diâmetro = 4 + 4 barras | Error: Diameter too small for stirrups. |
| C12 | Barras = -4 | Error: Bars and stirrup spacing cannot be negative. |
| C13 | Mão de obra = trinta | Please enter valid numbers in the fields! |
| C14 | Profundidade = 300 | Janela "Check the values": "Depth of 300 m: the limit is 30 m." Cancel → não calcula / Janela "Check the values": "Depth of 300 m: the limit is 30 m." Continue → "Total volume (with 10% waste): 103,673 m³"; "• Cement: 778 bags of 50 kg (R$ 28.008,00)"; "• Sand: 51,84 m³ (R$ 5.702,40)"; "• Gravel: 77,75 m³ (R$ 9.330,00)"; "Estimated stage cost: R$ 43.040,40" |
| C15 | 4 barras + espaçamento vazio | "Rebar cage: 1,50 m of each pile"; "• Rebar 8 mm: 26,1 kg (6 bars of 12 m)"; "• Total rebar: 26,1 kg (R$ 247,66)"; "• Tie wire: 0,5 kg (R$ 7,80)"; "Estimated stage cost: R$ 694,26" |
| C16 | 4 barras + espaçamento 12,5 | "Rebar cage: 1,50 m of each pile"; "• Rebar 8 mm: 26,1 kg (6 bars of 12 m)"; "• Stirrups 5 mm @ 12,5 cm: 9,5 kg (6 bars of 12 m)"; "• Total rebar: 35,5 kg (R$ 337,54)"; "• Tie wire: 0,7 kg (R$ 10,65)"; "Estimated stage cost: R$ 786,99" |
| C17 | Profundidade = 30 | "Total volume (with 10% waste): 10,367 m³"; "• Cement: 78 bags of 50 kg (R$ 2.808,00)"; "• Sand: 5,18 m³ (R$ 569,80)"; "• Gravel: 7,78 m³ (R$ 933,60)"; "Estimated stage cost: R$ 4.311,40" |
| C18 | Profundidade = 1-21/2 | Please enter valid numbers in the fields! |

### Visual (Brocas)

- Botões em inglês: Clear, Next, Finish. Calcular = "Calculate".
- O "?" abre "Help" com este texto (e o botão "Close"):

> Enter the number of piles, the diameter (e.g. 20 cm) and the average depth of each one. If you like, add the rebar. The app estimates the concrete and steel needed.
>
> Stirrups are only included if you enter the bars. To leave stirrups out, keep the spacing empty.
>
> Optional fields come with default values. Change them only if you want to.

- O que já valia na rodada 1 continua valendo:

- Botões: Limpar, Próximo e Finalizar. Sem Anterior, porque é a primeira aba.
- Limpar: pergunta antes de apagar e volta perda 10, espaçamento 20, traço 1:2:3 e bitola 8 mm.
- O "?" fala de brocas, explica que os estribos só entram com barras e termina com a nota dos valores padrão.
- Dicas dos campos inteiras; títulos "Traço do concreto" e "Bitola do ferro (mm)" perto do campo de cima e do botão, iguais ao "Armadura / Ferragem".
- Menus abrem alinhados no botão, sem sair da janela; o traço aparece com vírgula quando tiver decimal ("1,5:5:5").
- Tudo legível no tema claro e no escuro.

---

# BALDRAME (Grade Beam)

**Como aparece em inglês** (confira se nenhuma dica fica cortada):

- Dimensions (Required)
- Total length in meters (e.g. 12.5)
- Beam width in cm (e.g. 20)
- Beam height in cm (e.g. 30)
- Concrete mix (cement:sand:gravel) (Optional)
- Waste rate % (optional, e.g. 5)
- Labor cost per meter (optional, e.g. 25.00)
- Rebar (Optional)
- Number of bars per beam (optional, e.g. 4)
- Rebar size (mm)
- Stirrup spacing in cm (e.g. 20)
- Waterproofing (Optional)
- Opções dos menus: Yes · No

Preços dos testes: cimento R$ 36, areia R$ 110, brita R$ 120, aço R$ 9,50/kg, arame R$ 15/kg, impermeabilizante R$ 15,50 o litro (provisórios).

### Teste A: todos os campos, opcionais trocados

| Campo | Digite / escolha |
|---|---|
| Comprimento | 30 |
| Largura | 20 |
| Altura | 40 |
| Traço | 1:4:3 |
| Perda | 8 |
| Mão de obra | 40,00 |
| Nº de barras | 6 |
| Bitola | 12,5 mm |
| Espaçamento dos estribos | 15 |
| Impermeabilização | Sim |

```
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

Estimated stage cost: R$ 4.787,14
```

Pra entender: 30 m de viga = 2 emendas em cada barra (a cada 12 m); 6 barras × 2 emendas × 50 cm (40 × 12,5 mm) = 6 m de emendas. O estribo fica dentro do cobrimento de 3 cm (20 × 40 vira 14 × 34 por dentro). O impermeabilizante custa sobre os litros comprados (18 + 3,6 + 3,6 = 25,2 L × R$ 15,50), não sobre os 24 L usados.

### Teste B: só os obrigatórios

Comprimento 12,5, Largura 20, Altura 30. O resto como vem (perda 5, espaçamento 20, traço 1:2:3, impermeabilização Não).

```
Mix: 1:2:3
Total volume (with 5% waste): 0,788 m³
• Cement: 6 bags of 50 kg (R$ 216,00)
• Sand: 0,39 m³ (R$ 42,90)
• Gravel: 0,59 m³ (R$ 70,80)

Estimated stage cost: R$ 329,70
```

**B2:** igual ao B + 4 barras (bitola 8 mm e espaçamento 20, que já vêm):

```
Mix: 1:2:3
Total volume (with 5% waste): 0,788 m³
• Cement: 6 bags of 50 kg (R$ 216,00)
• Sand: 0,39 m³ (R$ 42,90)
• Gravel: 0,59 m³ (R$ 70,80)
• Rebar 8 mm: 22,3 kg (5 bars of 12 m) (includes 1,28 m of lap splices)
• Stirrups 5 mm @ 20 cm: 8,6 kg (5 bars of 12 m)
• Total rebar: 30,9 kg (R$ 293,74)
• Tie wire: 0,6 kg (R$ 9,30)

Estimated stage cost: R$ 632,74
```

**B3:** igual ao B (sem barras) + Impermeabilização: Sim:

```
Mix: 1:2:3
Total volume (with 5% waste): 0,788 m³
• Cement: 6 bags of 50 kg (R$ 216,00)
• Sand: 0,39 m³ (R$ 42,90)
• Gravel: 0,59 m³ (R$ 70,80)
• Waterproofing: 10,0 m² · 8,0 L = 3 cans of 3,6 L (R$ 167,40)

Estimated stage cost: R$ 497,10
```

### Teste C: erros de digitação

Base: Comprimento 12,5, Largura 20, Altura 30. Dê Limpar antes de cada um e mude só o indicado.

| # | O que mudar | Esperado na tela (em inglês) |
|---|---|---|
| C1 | Comprimento vazio | Please enter valid numbers in the fields! |
| C2 | Largura = vinte | Please enter valid numbers in the fields! |
| C3 | Altura = 0 | Error: Length, width and height must be greater than zero. |
| C4 | Comprimento = -5 | Error: Length, width and height must be greater than zero. |
| C5, C6 | Comprimento = 12.5, depois 12 1/2 (com espaço) | Todos: Igual ao Teste B |
| C7 | Perda = -2 | Error: Waste cannot be negative. |
| C8 | Perda = 2,5 | "Total volume (with 2,5% waste): 0,769 m³"; "• Sand: 0,38 m³ (R$ 41,80)"; "• Gravel: 0,58 m³ (R$ 69,60)"; "Estimated stage cost: R$ 327,40" |
| C9 | Largura = 4 + 4 barras | Janela "Check the values": "Beam of 4 cm x 30 cm: the minimum is 20 cm wide and 30 cm high." Continue → Error: Beam too small for stirrups. |
| C10 | Barras = -4 | Error: Bars and stirrup spacing cannot be negative. |
| C11 | Barras = 4,5 | Please enter valid numbers in the fields! |
| C12 | Mão de obra = quarenta | Please enter valid numbers in the fields! |
| C13 | 4 barras + espaçamento 12,5 | "• Rebar 8 mm: 22,3 kg (5 bars of 12 m) (includes 1,28 m of lap splices)"; "• Stirrups 5 mm @ 12,5 cm: 13,9 kg (8 bars of 12 m)"; "• Total rebar: 36,1 kg (R$ 343,33)"; "• Tie wire: 0,7 kg (R$ 10,80)"; "Estimated stage cost: R$ 683,83" |
| C14 | Comprimento = 12 + 4 barras | "Total volume (with 5% waste): 0,756 m³"; "• Sand: 0,38 m³ (R$ 41,80)"; "• Gravel: 0,57 m³ (R$ 68,40)"; "• Rebar 8 mm: 20,9 kg (5 bars of 12 m)"; "• Stirrups 5 mm @ 20 cm: 8,4 kg (5 bars of 12 m)"; "• Total rebar: 29,2 kg (R$ 277,69)"; "• Tie wire: 0,6 kg (R$ 8,70)"; "Estimated stage cost: R$ 612,59" |
| C15 | Comprimento = 24 + 4 barras | "Total volume (with 5% waste): 1,512 m³"; "• Cement: 12 bags of 50 kg (R$ 432,00)"; "• Sand: 0,76 m³ (R$ 83,60)"; "• Gravel: 1,13 m³ (R$ 135,60)"; "• Rebar 8 mm: 42,3 kg (9 bars of 12 m) (includes 1,28 m of lap splices)"; "• Stirrups 5 mm @ 20 cm: 16,6 kg (9 bars of 12 m)"; "• Total rebar: 58,9 kg (R$ 559,26)"; "• Tie wire: 1,2 kg (R$ 17,70)"; "Estimated stage cost: R$ 1.228,16" |
| C16 | 4 barras + espaçamento vazio | "• Rebar 8 mm: 22,3 kg (5 bars of 12 m) (includes 1,28 m of lap splices)"; "• Total rebar: 22,3 kg (R$ 211,66)"; "• Tie wire: 0,5 kg (R$ 6,75)"; "Estimated stage cost: R$ 548,11" |
| C17 | Comprimento = 5000 | "Total volume (with 5% waste): 315,000 m³"; "• Cement: 2.363 bags of 50 kg (R$ 85.068,00)"; "• Sand: 157,50 m³ (R$ 17.325,00)"; "• Gravel: 236,25 m³ (R$ 28.350,00)"; "Estimated stage cost: R$ 130.743,00" |
| C18 | Largura = 0,2 e Altura = 0,3 | Janela "Check the values": "Beam of 0,2 cm x 0,3 cm: the minimum is 20 cm wide and 30 cm high." Continue → "Total volume (with 5% waste): 0,000 m³"; "• Cement: 1 bag of 50 kg (R$ 36,00)"; "Estimated stage cost: R$ 36,00" |
| C19 | Largura = 19 | Janela "Check the values": "Beam of 19 cm x 30 cm: the minimum is 20 cm wide and 30 cm high." Continue → "Total volume (with 5% waste): 0,748 m³"; "• Sand: 0,37 m³ (R$ 40,70)"; "• Gravel: 0,56 m³ (R$ 67,20)"; "Estimated stage cost: R$ 323,90" |
| C20 | Altura = 29,5 | Janela "Check the values": "Beam of 20 cm x 29,5 cm: the minimum is 20 cm wide and 30 cm high." Continue → "Total volume (with 5% waste): 0,774 m³"; "• Gravel: 0,58 m³ (R$ 69,60)"; "Estimated stage cost: R$ 328,50" |
| C21 | Comprimento = 1-21/2 | Please enter valid numbers in the fields! |
| C22 | Comprimento = 2 1/2 | "Total volume (with 5% waste): 0,158 m³"; "• Cement: 2 bags of 50 kg (R$ 72,00)"; "• Sand: 0,08 m³ (R$ 8,80)"; "• Gravel: 0,12 m³ (R$ 14,40)"; "Estimated stage cost: R$ 95,20" |

**Limites com aviso** (janela "Check the values", com Cancel e Continue): viga com largura menor que 20 cm ou altura menor que 30 cm (confirmado pelo engenheiro). O comprimento não tem máximo.

### Visual (Baldrame)

- Botões em inglês: Clear, Previous, Next, Finish. Calcular = "Calculate".
- O "?" abre "Help" com este texto (e o botão "Close"):

> Enter the total length of the grade beams, their width and height. If you like, add the number of bars, bar size, stirrup spacing and waterproofing.
>
> Optional fields come with default values. Change them only if you want to.

- O que já valia na rodada 1 continua valendo:

- Botões: Limpar, Anterior, Próximo e Finalizar. O Anterior volta pra Brocas.
- Limpar: volta perda 5, espaçamento 20, traço 1:2:3, bitola 8 mm e impermeabilização Não.
- O "?" fala das vigas e termina com a nota dos valores padrão.
- Títulos dos menus (traço, bitola, impermeabilização) perto do campo de cima e do botão; menus alinhados no botão.
- No Teste A, a linha do ferro quebra em 2 linhas e continua legível.

---

# PAREDES (Walls)

**Como aparece em inglês** (confira se nenhuma dica fica cortada):

- Dimensions (Required)
- Gross wall area in m² (e.g. 30)
- Brick or block type and size
- Laying
- Doors and windows m² (optional, e.g. 5)
- Joint thickness in cm (optional, e.g. 1)
- Brick breakage % (optional, e.g. 5)
- Mortar mix (cement:lime:sand) (Optional)
- Opções dos menus: Clay brick (9x19x19) · Clay brick 9 holes (9x14x19) · Concrete block (9x19x39) · Concrete block (14x19x39) · Concrete block (19x19x39) · Upright · Flat

Preços dos testes: cimento R$ 36, cal R$ 18, areia R$ 110; tijolo baiano R$ 1,20, baiano 9 furos R$ 1,00, blocos de 9, 14 e 19 cm R$ 3,00, R$ 4,50 e R$ 6,00 (provisórios). A massa de assentar já tem 10% de perda.

### Teste A: todos os campos, opcionais trocados

| Campo | Digite / escolha |
|---|---|
| Área bruta | 80 |
| Tijolo | Bloco de concreto (14x19x39) |
| Assentamento | Deitado |
| Portas e janelas | 12,5 |
| Junta | 1,5 |
| Quebra | 8 |
| Traço | 1:0,5:6 |

```
Gross area: 80,00 m²
Openings (doors and windows): 12,50 m²
Net area: 67,50 m²
Mix: 1:0,5:6
• Concrete block (14x19x39): 1.162 pcs (R$ 5.229,00)
• Cement: 8 bags of 50 kg (R$ 288,00)
• Lime: 7 bags of 20 kg (R$ 126,00)
• Sand: 1,84 m³ (R$ 202,40)

Estimated stage cost: R$ 5.845,40
```

### Teste B: só os obrigatórios

Área 30. O resto como vem (tijolo baiano, em pé, junta 1, quebra 5, traço 1:2:8).

```
Gross area: 30,00 m²
Mix: 1:2:8
• Clay brick (9x19x19): 788 pcs (R$ 945,60)
• Cement: 1 bag of 50 kg (R$ 36,00)
• Lime: 3 bags of 20 kg (R$ 54,00)
• Sand: 0,26 m³ (R$ 28,60)

Estimated stage cost: R$ 1.064,20
```

Pra conferir o resto, use o Teste B (área 30) e mude só o indicado:

| # | Mudar | Esperado na tela (em inglês) |
|---|---|---|
| B2 | Bloco de concreto (19x19x39) | "• Concrete block (19x19x39): 394 pcs (R$ 2.364,00)"; "• Cement: 2 bags of 50 kg (R$ 72,00)"; "• Lime: 5 bags of 20 kg (R$ 90,00)"; "• Sand: 0,42 m³ (R$ 46,20)"; "Estimated stage cost: R$ 2.572,20" |
| B3 | Tijolo baiano 9 furos (9x14x19) + Deitado | "• Clay brick 9 holes (9x14x19): 1.575 pcs (R$ 1.575,00)"; "• Cement: 2 bags of 50 kg (R$ 72,00)"; "• Lime: 7 bags of 20 kg (R$ 126,00)"; "• Sand: 0,61 m³ (R$ 67,10)"; "Estimated stage cost: R$ 1.840,10" |
| B4 | Traço 1:0:3 | "Mix: 1:0:3"; "• Cement: 3 bags of 50 kg (R$ 108,00)"; "• Sand: 0,27 m³ (R$ 29,70)"; "Estimated stage cost: R$ 1.083,30" |

### Teste C: erros de digitação

Base: Área 30. Dê Limpar antes de cada um e mude só o indicado.

| # | O que mudar | Esperado na tela (em inglês) |
|---|---|---|
| C1 | Área vazia | Please enter valid numbers in the fields! |
| C2 | Área = trinta | Please enter valid numbers in the fields! |
| C3 | Área = 0 | Error: The wall area must be greater than zero. |
| C4 | Área = -30 | Error: The wall area must be greater than zero. |
| C5, C6, C7 | Área = 30,5, depois 30.5, depois 30 1/2 (com espaço) | Todos: "Gross area: 30,50 m²"; "• Clay brick (9x19x19): 801 pcs (R$ 961,20)"; "• Sand: 0,27 m³ (R$ 29,70)"; "Estimated stage cost: R$ 1.080,90" |
| C8 | Portas e janelas = 35 | Error: The openings deduction must be smaller than the area. |
| C9 | Portas e janelas = 30 | Error: The openings deduction must be smaller than the area. |
| C10 | Portas e janelas = -5 | Error: Deduction, joint and breakage cannot be negative. |
| C11 | Quebra = -5 | Error: Deduction, joint and breakage cannot be negative. |
| C12 | Junta vazia, e depois Quebra vazia | Todos: Igual ao Teste B |
| C13 | Quebra = 2,5 | "• Clay brick (9x19x19): 769 pcs (R$ 922,80)"; "Estimated stage cost: R$ 1.041,40" |
| C14 | Junta = 0 | Janela "Check the values": "Joint of 0 cm: the usual is 0,5 cm to 3 cm." Continue → "• Clay brick (9x19x19): 873 pcs (R$ 1.047,60)"; "Estimated stage cost: R$ 1.047,60" |
| C15 | Junta = 10 | Janela "Check the values": "Joint of 10 cm: the usual is 0,5 cm to 3 cm." Continue → "• Clay brick (9x19x19): 375 pcs (R$ 450,00)"; "• Cement: 5 bags of 50 kg (R$ 180,00)"; "• Lime: 17 bags of 20 kg (R$ 306,00)"; "• Sand: 1,54 m³ (R$ 169,40)"; "Estimated stage cost: R$ 1.105,40" |
| C16 | Área = 100000 | Janela "Check the values": "Area of 100.000 m²: the limit is 2.000 m²." Cancel → não calcula / Janela "Check the values": "Area of 100.000 m²: the limit is 2.000 m²." Continue → "Gross area: 100.000,00 m²"; "• Clay brick (9x19x19): 2.625.000 pcs (R$ 3.150.000,00)"; "• Cement: 2.633 bags of 50 kg (R$ 94.788,00)"; "• Lime: 9.653 bags of 20 kg (R$ 173.754,00)"; "• Sand: 877,50 m³ (R$ 96.525,00)"; "Estimated stage cost: R$ 3.515.067,00" |
| C17 | Quebra = 25 | Janela "Check the values": "Breakage of 25%: the limit is 20%." Continue → "• Clay brick (9x19x19): 938 pcs (R$ 1.125,60)"; "Estimated stage cost: R$ 1.244,20" |

**Limites com aviso** (janela "Check the values", com Cancel e Continue): área até 2.000 m², junta de 0,5 a 3 cm e quebra até 20%.

### Visual (Paredes)

- Botões em inglês: Clear, Previous, Next, Finish. Calcular = "Calculate".
- O "?" abre "Help" com este texto (e o botão "Close"):

> Enter the total wall area without any deductions, the brick type and whether it is laid upright or flat. Doors and windows have their own deduction field.
>
> Optional fields come with default values. Change them only if you want to.

- O que já valia na rodada 1 continua valendo:

- Botões: Limpar, Anterior (volta pro Baldrame), Próximo (vai pra Laje) e Finalizar.
- Limpar: volta tijolo baiano, em pé, junta 1, quebra 5 e traço 1:2:8.
- O "?" fala da área bruta, do tijolo e do desconto de portas e janelas.
- Menu do tijolo: os 5 nomes inteiros, alinhado no botão, sem sair da janela.
- Menu do traço com vírgula: 1:2:8, 1:0,5:6, 1,5:1:8, 1:0:3, 1,5:0:4.
- Títulos "Tipo e tamanho do tijolo ou bloco" e "Traço da massa (cimento:cal:areia) (Opcional)" perto do campo de cima e do botão.

---

# LAJE (Slab)

**Como aparece em inglês** (confira se nenhuma dica fica cortada):

- Dimensions (Required)
- Slab area in m² (e.g. 50)
- Slab type
- Total slab thickness in cm (e.g. 10)
- Filler (Optional)
- Topping thickness in cm (optional, e.g. 4)
- Welded wire mesh in the topping (Optional)
- Concrete mix (cement:sand:gravel) (Optional)
- Waste rate % (optional, e.g. 5)
- Opções dos menus: Precast (lattice joists) · Solid slab · EPS foam · Ceramic block · Yes · No

Preços dos testes: cimento R$ 36, areia R$ 110, brita R$ 120; laje pré-moldada R$ 75,00/m² com isopor e R$ 65,00/m² com lajota cerâmica; tela soldada R$ 95,00 o painel de 2 x 3 m (provisórios).

### Teste A: pré-moldada, todos os campos, opcionais trocados

| Campo | Digite / escolha |
|---|---|
| Área | 50 |
| Tipo de laje | Pré-moldada treliçada |
| Enchimento | Lajota cerâmica |
| Capa de concreto | 5 |
| Tela soldada | Sim |
| Traço | 1:3:3 |
| Perda | 8 |

```
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

Estimated stage cost: R$ 5.486,50
```

Pra entender: o concreto é a capa (5 cm) + 1,2 cm entre as vigotas = 6,2 cm × 50 m² = 3,1 m³, com 8% de perda = 3,348 m³. As lajotas são 12 por m² × 50 × 1,08 = 648. A tela leva 10% a mais (55 m²) ÷ 6 m² por painel = 10 painéis.

### Teste A2: maciça, todos os campos

| Campo | Digite / escolha |
|---|---|
| Área | 30 |
| Tipo de laje | Maciça |
| Espessura total | 10 |
| Traço | 1,5:5:5 |
| Perda | 7 |

```
Area: 30,00 m²
Slab type: Solid slab
Thickness: 10 cm
Mix: 1,5:5:5
Total volume (with 7% waste): 3,210 m³
• Cement: 19 bags of 50 kg (R$ 684,00)
• Sand: 2,09 m³ (R$ 229,90)
• Gravel: 2,09 m³ (R$ 250,80)

Estimated stage cost: R$ 1.164,70
```

### Teste B: pré-moldada, só os obrigatórios

Área 50. O resto como vem (pré-moldada, isopor, capa 4, tela Não, traço 1:2:3, perda 5).

```
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

Estimated stage cost: R$ 4.902,70
```

**B2:** maciça, só os obrigatórios. Área 30, Tipo Maciça, Espessura 10:

```
Area: 30,00 m²
Slab type: Solid slab
Thickness: 10 cm
Mix: 1:2:3
Total volume (with 5% waste): 3,150 m³
• Cement: 24 bags of 50 kg (R$ 864,00)
• Sand: 1,58 m³ (R$ 173,80)
• Gravel: 2,36 m³ (R$ 283,20)

Estimated stage cost: R$ 1.321,00
```

Pra conferir o resto, use o Teste B (área 50) e mude só o indicado:

| # | Mudar | Esperado na tela (em inglês) |
|---|---|---|
| B3 | Tela soldada: Sim | "• Welded wire mesh: 55,00 m² = 10 panels of 2 x 3 m (R$ 950,00)"; "Estimated stage cost: R$ 5.852,70" |
| B4 | Enchimento: Lajota cerâmica | "Filler: Ceramic block"; "• Precast slab (joists + filler): 50,00 m² (R$ 3.250,00)"; "(Ceramic blocks: 630 pcs)"; "Estimated stage cost: R$ 4.402,70" |

### Teste C: erros de digitação

Base: pré-moldada, Área 50. Mude só o indicado.

| # | O que mudar | Esperado na tela (em inglês) |
|---|---|---|
| C1 | Área vazia | Please enter valid numbers in the fields! |
| C2 | Área = cinquenta | Please enter valid numbers in the fields! |
| C3 | Área = 0 | Error: The area must be greater than zero. |
| C4 | Área = -50 | Error: The area must be greater than zero. |
| C5, C6, C7 | Área = 50,5, depois 50.5, depois 50 1/2 (com espaço) | Todos: "Area: 50,50 m²"; "Total volume (with 5% waste): 2,757 m³"; "• Precast slab (joists + filler): 50,50 m² (R$ 3.787,50)"; "• Sand: 1,38 m³ (R$ 151,80)"; "• Gravel: 2,07 m³ (R$ 248,40)"; "Estimated stage cost: R$ 4.943,70" |
| C8 | Perda = -5 | Error: Waste cannot be negative. |
| C9 | Perda = 2,5 | "Total volume (with 2,5% waste): 2,665 m³"; "• Cement: 20 bags of 50 kg (R$ 720,00)"; "• Sand: 1,33 m³ (R$ 146,30)"; "• Gravel: 2,00 m³ (R$ 240,00)"; "Estimated stage cost: R$ 4.856,30" |
| C10 | Capa = 0 | Error: The topping thickness must be greater than zero. |
| C11 | Capa vazia | Igual ao Teste B |
| C12 | Capa = -4 | Error: The topping thickness must be greater than zero. |
| C13 | Maciça + Espessura vazia | Please enter valid numbers in the fields! |
| C14 | Maciça + Espessura = 0 | Error: Enter the total thickness of the solid slab. |
| C15 | Maciça + Espessura = dez | Please enter valid numbers in the fields! |
| C16 | Área = 1-21/2 | Please enter valid numbers in the fields! |
| C17 | Área = 5 + Tela Sim | "Area: 5,00 m²"; "Total volume (with 5% waste): 0,273 m³"; "• Precast slab (joists + filler): 5,00 m² (R$ 375,00)"; "• Welded wire mesh: 5,50 m² = 1 panel of 2 x 3 m (R$ 95,00)"; "• Cement: 3 bags of 50 kg (R$ 108,00)"; "• Sand: 0,14 m³ (R$ 15,40)"; "• Gravel: 0,20 m³ (R$ 24,00)"; "Estimated stage cost: R$ 617,40" |
| C18 | Capa = 4,5 | "Concrete topping: 4,5 cm"; "Total volume (with 5% waste): 2,992 m³"; "• Cement: 23 bags of 50 kg (R$ 828,00)"; "• Sand: 1,50 m³ (R$ 165,00)"; "• Gravel: 2,24 m³ (R$ 268,80)"; "Estimated stage cost: R$ 5.011,80" |
| C19 | Área = 100000 | Janela "Check the values": "Area of 100.000 m²: the limit is 2.000 m²." Continue → "Area: 100.000,00 m²"; "Total volume (with 5% waste): 5.460,000 m³"; "• Precast slab (joists + filler): 100.000,00 m² (R$ 7.500.000,00)"; "• Cement: 40.950 bags of 50 kg (R$ 1.474.200,00)"; "• Sand: 2.730,00 m³ (R$ 300.300,00)"; "• Gravel: 4.095,00 m³ (R$ 491.400,00)"; "Estimated stage cost: R$ 9.765.900,00" |
| C20 | Capa = 50 | Janela "Check the values": "Topping of 50 cm: the usual is 3 cm to 8 cm." Continue → "Concrete topping: 50 cm"; "Total volume (with 5% waste): 26,880 m³"; "• Cement: 202 bags of 50 kg (R$ 7.272,00)"; "• Sand: 13,44 m³ (R$ 1.478,40)"; "• Gravel: 20,16 m³ (R$ 2.419,20)"; "Estimated stage cost: R$ 14.919,60" |
| C21 | Maciça + Espessura = 200 | Janela "Check the values": "Thickness of 200 cm: the usual is 8 cm to 20 cm." Continue → "Slab type: Solid slab"; "Thickness: 200 cm"; "Total volume (with 5% waste): 105,000 m³"; "• Cement: 788 bags of 50 kg (R$ 28.368,00)"; "• Sand: 52,50 m³ (R$ 5.775,00)"; "• Gravel: 78,75 m³ (R$ 9.450,00)"; "Estimated stage cost: R$ 43.593,00" |

Troca de tipo (sem perder dados):

C22: preencha o Teste A (pré-moldada) e troque para "Solid slab". Aparece o campo "Total slab thickness in cm (e.g. 10)" e somem o enchimento, a capa e a tela. Volte para "Precast (lattice joists)": a capa 5 e a área 50 continuam lá, e o resultado antigo some (porque era do outro tipo).

**Limites com aviso** (janela "Check the values", com Cancel e Continue): área até 2.000 m², capa de 3 a 8 cm (só na pré-moldada) e espessura da maciça de 8 a 20 cm (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Laje)

- Botões em inglês: Clear, Previous, Next, Finish. Calcular = "Calculate".
- O "?" abre "Help" com este texto (e o botão "Close"):

> Enter the area and the slab type. For precast slabs, choose the filler (EPS or ceramic block) and the topping thickness. For solid slabs, enter the total thickness.
>
> If the topping has welded wire mesh, choose Yes: the app counts the 2 x 3 m panels, with 10% extra for the overlap.
>
> Optional fields come with default values. Change them only if you want to.

- O que já valia na rodada 1 continua valendo:

- Botões: Limpar, Anterior, Próximo e Finalizar. O Anterior volta pra Paredes e o Próximo vai pro Telhado.
- Limpar: volta pré-moldada, isopor, capa 4, tela Não, traço 1:2:3 e perda 5.
- O "?" fala dos dois tipos de laje e da tela soldada (painéis de 2 x 3 m com 10% a mais), e termina com a nota dos valores padrão.
- Menus (tipo de laje, enchimento, tela, traço) alinhados no botão, com os títulos perto do campo de cima.
- Menu do traço com vírgula: 1:2:3, 1:3:3, 1:4:3, 1,5:5:5.
- Na maciça, não aparece a opção de tela soldada.

---

# TELHADO (Roof)

**Como aparece em inglês** (confira se nenhuma dica fica cortada):

- Dimensions (Required)
- Roof plan area in m² (e.g. 80)
- Roof tile type
- Slope in % (optional, e.g. 30)
- Ridge in meters (optional, e.g. 10)
- Timber framing (Optional)
- Waste rate % (optional, e.g. 5)
- Opções dos menus: Clay · Concrete · Fiber cement · Yes · No

### Teste A: concreto, todos os campos, opcionais trocados

| Campo | Digite / escolha |
|---|---|
| Área em planta | 80 |
| Tipo de telha | Concreto |
| Inclinação | 35 |
| Cumeeira | 10 |
| Madeiramento | Sim |
| Perda | 8 |

```
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

Estimated stage cost: R$ 8.437,20
```

Pra entender: a área real é 80 × √(1 + 0,35²) = 84,76 m². Telhas de concreto: 10,5 por m² × 84,76 × 1,08 = 961,2 → 962. Cumeeira: 3 peças por metro × 10 × 1,08 = 32,4 → 33. Ripas: 3 m por m² × 84,76 × 1,08 = 274,6 m.

### Teste A2: fibrocimento, todos os campos

| Campo | Digite / escolha |
|---|---|
| Área em planta | 60 |
| Tipo de telha | Fibrocimento (a inclinação muda sozinha para 15) |
| Cumeeira | 8 |
| Madeiramento | Sim |
| Perda | 5 |

```
Plan area: 60,00 m²
Slope: 15%
Roof area: 60,67 m²
Roof tile type: Fiber cement
• Roof tiles (with 5% waste): 27 pcs (R$ 2.025,00)
• Ridge: 8,00 m = 9 pcs (R$ 405,00)
• Timber framing (estimate):
   - Purlins: 51,0 m (R$ 1.275,00)

Estimated stage cost: R$ 3.705,00
```

No fibrocimento só aparecem as terças (a telha vai direto nelas, sem ripas e caibros).

### Teste B: só os obrigatórios

Área 80. O resto como vem (cerâmica, inclinação 30, cumeeira vazia, madeiramento Não, perda 5).

```
Plan area: 80,00 m²
Slope: 30%
Roof area: 83,52 m²
Roof tile type: Clay
• Roof tiles (with 5% waste): 1.404 pcs (R$ 3.510,00)

Estimated stage cost: R$ 3.510,00
```

Pra conferir o resto, use o Teste B (área 80) e mude só o indicado:

| # | Mudar | Esperado na tela (em inglês) |
|---|---|---|
| B2 | Cumeeira: 10 | "• Ridge: 10,00 m = 32 pcs (R$ 128,00)"; "Estimated stage cost: R$ 3.638,00" |
| B3 | Madeiramento: Sim | "• Timber framing (estimate):"; "- Battens: 263,1 m (R$ 789,30)"; "- Rafters: 175,4 m (R$ 1.578,60)"; "- Purlins: 52,6 m (R$ 1.315,00)"; "Estimated stage cost: R$ 7.192,90" |
| B4 | Tipo: Fibrocimento | "Slope: 15%"; "Roof area: 80,89 m²"; "Roof tile type: Fiber cement"; "• Roof tiles (with 5% waste): 36 pcs (R$ 2.700,00)"; "Estimated stage cost: R$ 2.700,00" |
| B5 | Tipo: Concreto | "Roof tile type: Concrete"; "• Roof tiles (with 5% waste): 921 pcs (R$ 4.144,50)"; "Estimated stage cost: R$ 4.144,50" |

### Teste C: erros de digitação

Base: Teste B (área 80). Mude só o indicado.

| # | O que mudar | Esperado na tela (em inglês) |
|---|---|---|
| C1 | Área vazia | Please enter valid numbers in the fields! |
| C2 | Área = oitenta | Please enter valid numbers in the fields! |
| C3 | Área = 0 | Error: The area must be greater than zero. |
| C4 | Área = -80 | Error: The area must be greater than zero. |
| C5, C6, C7 | Área = 80,5, depois 80.5, depois 80 1/2 (com espaço) | Todos: "Plan area: 80,50 m²"; "Roof area: 84,04 m²"; "• Roof tiles (with 5% waste): 1.412 pcs (R$ 3.530,00)"; "Estimated stage cost: R$ 3.530,00" |
| C8 | Perda = -5 | Error: Values cannot be negative. |
| C9 | Perda = 2,5 | "• Roof tiles (with 2,5% waste): 1.370 pcs (R$ 3.425,00)"; "Estimated stage cost: R$ 3.425,00" |
| C10 | Inclinação = -30 | Error: Values cannot be negative. |
| C11 | Inclinação vazia | Igual ao Teste B |
| C12 | Inclinação = 0 | "Slope: 0%"; "Roof area: 80,00 m²"; "• Roof tiles (with 5% waste): 1.344 pcs (R$ 3.360,00)"; "Estimated stage cost: R$ 3.360,00" |
| C13 | Inclinação = 2,5 | "Slope: 2,5%"; "Roof area: 80,02 m²"; "• Roof tiles (with 5% waste): 1.345 pcs (R$ 3.362,50)"; "Estimated stage cost: R$ 3.362,50" |
| C14 | Cumeeira = -10 | Error: Values cannot be negative. |
| C15 | Cumeeira = 0 | Igual ao Teste B |
| C16 | Cumeeira = dez | Please enter valid numbers in the fields! |
| C17 | Área = 1-21/2 | Please enter valid numbers in the fields! |
| C18 | Cumeeira = 0,3 | "• Ridge: 0,30 m = 1 pc (R$ 4,00)"; "Estimated stage cost: R$ 3.514,00" |
| C19 | Área = 100000 | Janela "Check the values": "Area of 100.000 m²: the limit is 2.000 m²." Continue → "Plan area: 100.000,00 m²"; "Roof area: 104.403,07 m²"; "• Roof tiles (with 5% waste): 1.753.972 pcs (R$ 4.384.930,00)"; "Estimated stage cost: R$ 4.384.930,00" |
| C20 | Inclinação = 300 | Janela "Check the values": "Slope of 300%: the limit is 100%." Continue → "Slope: 300%"; "Roof area: 252,98 m²"; "• Roof tiles (with 5% waste): 4.251 pcs (R$ 10.627,50)"; "Estimated stage cost: R$ 10.627,50" |

Troca de tipo (a inclinação acompanha):

C21: com a inclinação ainda em 30 (sem mexer), troque para "Fiber cement": ela vira 15. Volte para "Clay": vira 30 de novo.

C22: digite inclinação 35 e troque para "Fiber cement": continua 35 (você mexeu, então o app não troca). Resultado: "Roof tiles (with 5% waste): 38 pcs (R$ 2.850,00)".

**Limites com aviso** (janela "Check the values", com Cancel e Continue): área até 2.000 m² e inclinação até 100% (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Telhado)

- Botões em inglês: Clear, Previous, Next stage (linha própria), Finish. Calcular = "Calculate".
- O "?" abre "Help" com este texto (e o botão "Close"):

> Enter the roof area and the tile type. If you like, add the slope, ridge and timber framing.
>
> The area is the plan area (seen from above, including eaves). The app adjusts it for the slope.
>
> The ridge is the top line of the roof, where the two slopes meet. Enter its length in meters (on a hip roof, also add the sloped hips). A single-slope roof has no ridge.
>
> Optional fields come with default values. Change them only if you want to.

- O que já valia na rodada 1 continua valendo:

- Telhado é a última aba da Estrutura. Botões: Limpar e Anterior (volta pra Laje) numa linha; embaixo, "Avançar para a próxima etapa" (vai pra Elétrica) e Finalizar. **Não tem Próximo.**
- Limpar: volta cerâmica, inclinação 30, cumeeira vazia, madeiramento Não e perda 5.
- O "?" fala da área em planta (vista de cima, com os beirais), que o app corrige pela inclinação, e explica a cumeeira (no telhado de quatro águas, somar as quinas; telhado de uma água não tem). Termina com a nota dos valores padrão.
- Menus (tipo de telha, madeiramento) alinhados no botão, com os títulos perto do campo de cima.
- Menu do tipo de telha: Cerâmica, Concreto, Fibrocimento.

---

# ELÉTRICA (Electrical)

**Como aparece em inglês** (confira se nenhuma dica fica cortada):

- Quantities
- Number of outlets (e.g. 20)
- Number of switches (e.g. 10)
- Number of light points (e.g. 12)
- Showers above 5.500 W (e.g. 2)
- Showers up to 5.500 W (e.g. 1)
- Lengths from the plans (Optional)
- Conduit in meters (optional, e.g. 150)
- Wire 1,5 mm² in meters (optional)
- Waste rate % (optional, e.g. 10)

### Teste A: todos os campos (metragens do projeto)

| Campo | Digite / escolha |
|---|---|
| Tomadas | 20 |
| Interruptores | 10 |
| Pontos de luz | 12 |
| Chuveiros acima de 5.500 W | 2 |
| Chuveiros até 5.500 W | 1 |
| Conduíte | 150 |
| Fio 1,5 mm² | 200 |
| Fio 2,5 mm² | 250 |
| Fio 4 mm² | 40 |
| Fio 6 mm² | 60 |
| Perda | 5 |

```
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

Estimated stage cost: R$ 2.885,00
```

Pra entender: como tudo veio do projeto, o app só soma os 5% de perda (150 m → 157,5 m → 4 rolos de 50 m). Os chuveiros só aparecem no topo, porque o fio e o conduíte já vieram do projeto. As caixinhas são uma por tomada ou interruptor (20 + 10 = 30) e as octogonais, uma por ponto de luz (12).

### Teste B: só os obrigatórios (o app estima)

Tomadas 20, Interruptores 10, Pontos de luz 12. O resto como vem (os dois campos de chuveiro e as metragens vazios, perda 10).

```
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

Estimated stage cost: R$ 2.300,00
```

Pra entender: são 42 pontos × 5 m = 210 m de conduíte, com 10% = 231 m. Fio 1,5: (10 interruptores + 12 luzes) × 10 m = 220, com 10% = 242 m. Fio 2,5: 20 tomadas × 15 m = 300, com 10% = 330 m.

Pra conferir o resto, use o Teste B e mude só o indicado:

| # | Mudar | Esperado na tela (em inglês) |
|---|---|---|
| B2 | Chuveiros acima de 5.500 W: 2 | "Showers above 5.500 W: 2"; "• Conduit (estimated, with 10% waste): 253,0 m = 6 rolls of 50 m (R$ 450,00)"; "• Wire 6 mm² (estimated, with 10% waste): 66,0 m = 1 roll of 100 m (R$ 530,00)"; "Estimated stage cost: R$ 2.905,00" |
| B3 | Chuveiros até 5.500 W: 2 | "Showers up to 5.500 W: 2"; "• Conduit (estimated, with 10% waste): 253,0 m = 6 rolls of 50 m (R$ 450,00)"; "• Wire 4 mm² (estimated, with 10% waste): 66,0 m = 1 roll of 100 m (R$ 360,00)"; "Estimated stage cost: R$ 2.735,00" |
| B4 | Um de cada: acima 1 e até 5.500 W 1 | "Showers above 5.500 W: 1"; "Showers up to 5.500 W: 1"; "• Conduit (estimated, with 10% waste): 253,0 m = 6 rolls of 50 m (R$ 450,00)"; "• Wire 4 mm² (estimated, with 10% waste): 33,0 m = 1 roll of 100 m (R$ 360,00)"; "• Wire 6 mm² (estimated, with 10% waste): 33,0 m = 1 roll of 100 m (R$ 530,00)"; "Estimated stage cost: R$ 3.265,00" |
| B5 | Conduíte: 150 | "• Conduit (from plans, with 10% waste): 165,0 m = 4 rolls of 50 m (R$ 300,00)"; "Estimated stage cost: R$ 2.225,00" |
| B6 | Fio 2,5 mm²: 250 | "• Wire 2,5 mm² (from plans, with 10% waste): 275,0 m = 3 rolls of 100 m (R$ 690,00)"; "Estimated stage cost: R$ 2.070,00" |
| B7 | Limpar e digitar só Chuveiros acima de 5.500 W: 1 | "Showers above 5.500 W: 1"; "• Conduit (estimated, with 10% waste): 11,0 m = 1 roll of 50 m (R$ 75,00)"; "• Wire 6 mm² (estimated, with 10% waste): 33,0 m = 1 roll of 100 m (R$ 530,00)"; "Estimated stage cost: R$ 605,00" |
| B8 | Limpar e digitar só Chuveiros até 5.500 W: 1 | "Showers up to 5.500 W: 1"; "• Conduit (estimated, with 10% waste): 11,0 m = 1 roll of 50 m (R$ 75,00)"; "• Wire 4 mm² (estimated, with 10% waste): 33,0 m = 1 roll of 100 m (R$ 360,00)"; "Estimated stage cost: R$ 435,00" |
| B9 | Limpar e digitar só Tomadas: 1 | "Outlets: 1"; "• Conduit (estimated, with 10% waste): 5,5 m = 1 roll of 50 m (R$ 75,00)"; "• Wire 2,5 mm² (estimated, with 10% waste): 16,5 m = 1 roll of 100 m (R$ 230,00)"; "• 4x2 wall boxes: 1 pc (R$ 2,50)"; "• Outlets: 1 pc (R$ 15,00)"; "Estimated stage cost: R$ 322,50" |

Pra entender o chuveiro: cada um leva 10 m de conduíte e 30 m de fio (3 fios de 10 m), com 10% = 11 m e 33 m. O de até 5.500 W usa fio de 4 mm²; o mais forte, de 6 mm².

### Teste C: erros de digitação

Base: Teste B. Mude só o indicado.

| # | O que mudar | Esperado na tela (em inglês) |
|---|---|---|
| C1 | Tomadas, interruptores e luzes vazios | Error: Enter at least one outlet, switch, light point or shower. |
| C2 | Os três = 0 | Error: Enter at least one outlet, switch, light point or shower. |
| C3 | Tomadas = vinte | Please enter valid numbers in the fields! |
| C4 | Tomadas = -5 | Error: Quantities cannot be negative. |
| C5 | Tomadas = 2,5 | Please enter valid numbers in the fields! |
| C5b | Chuveiros até 5.500 W = -1 | Error: Quantities cannot be negative. |
| C5c | Chuveiros até 5.500 W = 1,5 | Please enter valid numbers in the fields! |
| C6 | Perda = -5 | Error: Values cannot be negative. |
| C7 | Perda = 2,5 | "• Conduit (estimated, with 2,5% waste): 215,3 m = 5 rolls of 50 m (R$ 375,00)"; "• Wire 1,5 mm² (estimated, with 2,5% waste): 225,5 m = 3 rolls of 100 m (R$ 450,00)"; "• Wire 2,5 mm² (estimated, with 2,5% waste): 307,5 m = 4 rolls of 100 m (R$ 920,00)" |
| C8 | Conduíte = -10 | Error: Values cannot be negative. |
| C9 | Conduíte = 0 | "Estimated stage cost: R$ 1.925,00" |
| C10, C11, C12 | Conduíte = 150,5, depois 150.5, depois 150 1/2 | Todos: "• Conduit (from plans, with 10% waste): 165,6 m = 4 rolls of 50 m (R$ 300,00)"; "Estimated stage cost: R$ 2.225,00" |
| C13 | Fio 1,5 mm² = abc | Please enter valid numbers in the fields! |
| C14 | Fio 1,5 mm² = 1-21/2 | Please enter valid numbers in the fields! |
| C15 | Chuveiros acima de 5.500 W: 2 + Fio 6 mm² = 0 | "Showers above 5.500 W: 2"; "• Conduit (estimated, with 10% waste): 253,0 m = 6 rolls of 50 m (R$ 450,00)"; "Estimated stage cost: R$ 2.375,00" |
| C15b | Chuveiros até 5.500 W: 2 + Fio 4 mm² = 0 | "Showers up to 5.500 W: 2"; "• Conduit (estimated, with 10% waste): 253,0 m = 6 rolls of 50 m (R$ 450,00)"; "Estimated stage cost: R$ 2.375,00" |
| C16 | Tomadas = 2000 | Janela "Check the values": "2.000 outlets: the limit is 300." Continue → "Outlets: 2.000"; "• Conduit (estimated, with 10% waste): 11.121,0 m = 223 rolls of 50 m (R$ 16.725,00)"; "• Wire 2,5 mm² (estimated, with 10% waste): 33.000,0 m = 330 rolls of 100 m (R$ 75.900,00)"; "• 4x2 wall boxes: 2.010 pcs (R$ 5.025,00)"; "• Outlets: 2.000 pcs (R$ 30.000,00)"; "Estimated stage cost: R$ 128.280,00" |
| C17 | Chuveiros acima de 5.500 W = 50 | Janela "Check the values": "50 showers: the limit is 10 (adding both fields)." Continue → "Showers above 5.500 W: 50"; "• Conduit (estimated, with 10% waste): 781,0 m = 16 rolls of 50 m (R$ 1.200,00)"; "• Wire 6 mm² (estimated, with 10% waste): 1.650,0 m = 17 rolls of 100 m (R$ 9.010,00)"; "Estimated stage cost: R$ 12.135,00" |

**Limites com aviso** (janela "Check the values", com Cancel e Continue): até 300 tomadas, 300 interruptores, 300 pontos de luz e 10 chuveiros (somando os dois campos) (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Elétrica)

- Botões em inglês: Clear, Previous, Next, Finish. Calcular = "Calculate".
- O "?" abre "Help" com este texto (e o botão "Close"):

> Enter how many outlets, switches and light points the project will have. The app estimates conduits, wires and boxes. If you have the plans, enter the lengths.
>
> Each electric shower has its own circuit from the breaker panel: 6 mm² wire for showers above 5.500 W and 4 mm² for showers up to 5.500 W (the power rating is on the shower box).
>
> Any length field left empty is estimated by the app.
>
> Optional fields come with default values. Change them only if you want to.

- O que já valia na rodada 1 continua valendo:

- Botões: Limpar, Anterior (volta pro Telhado), Próximo (vai pra Hidráulica) e Finalizar.
- Limpar: tudo vazio e perda 10.
- O "?" explica o que o app estima, que cada chuveiro tem um circuito só dele (fio de 6 mm² acima de 5.500 W e de 4 mm² até 5.500 W, com a potência na caixa do chuveiro) e que metragem vazia é estimada. Termina com a nota dos valores padrão.
- Os dois campos de chuveiro aparecem um embaixo do outro: "Chuveiros acima de 5.500 W (ex: 2)" e "Chuveiros até 5.500 W (ex: 1)", sem cortar a dica.
- Os títulos "Quantidades" e "Metragens do projeto (Opcional)" aparecem acima dos campos certos.
- Dicas dos fios sem cortar: "Fio 1,5 mm² em metros (opcional)" (e 2,5, 4 e 6).

---

# HIDRÁULICA (Plumbing)

**Como aparece em inglês** (confira se nenhuma dica fica cortada):

- Quantities
- Cold water points (e.g. 10)
- Hot water points (e.g. 3)
- Drain points (e.g. 8)
- Lengths from the plans (Optional)
- Cold water 25 mm, in meters (optional)
- Hot water 22 mm, in meters (optional)
- Drain 40 mm, in meters (optional)
- Drain 100 mm, in meters (optional)
- Waste rate % (optional, e.g. 10)

### Teste A: todos os campos (metragens do projeto)

| Campo | Digite / escolha |
|---|---|
| Pontos de água fria | 10 |
| Pontos de água quente | 3 |
| Pontos de esgoto | 8 |
| Água fria 25 mm | 50 |
| Água quente 22 mm | 20 |
| Esgoto 40 mm | 30 |
| Esgoto 100 mm | 18 |
| Perda | 5 |

```
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

Estimated stage cost: R$ 1.707,00
```

Pra entender: a água quente vem em barras de 3 m (CPVC), por isso 21 m dá 7 barras; os outros tubos são barras de 6 m. As conexões são sempre estimadas: 4 por ponto de água e 3 por ponto de esgoto. Registros: 1 a cada 4 pontos de água (13 ÷ 4 = 3,25 → 4).

### Teste B: só os obrigatórios (o app estima)

Pontos de água fria 10, água quente 3, esgoto 8. O resto como vem (metragens vazias, perda 10).

```
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

Estimated stage cost: R$ 1.507,00
```

Pra entender: água fria 10 × 4 m = 40, com 10% = 44 m. Água quente 3 × 5 m = 15, com 10% = 16,5 m. Esgoto: 8 × 3 m = 24 → 26,4 m de 40 mm, e 8 × 2 m = 16 → 17,6 m de 100 mm.

Pra conferir o resto, use o Teste B e mude só o indicado:

| # | Mudar | Esperado na tela (em inglês) |
|---|---|---|
| B2 | Limpar e digitar só água fria: 1 | "Cold water points: 1"; "• Cold water PVC pipe 25 mm (estimated, with 10% waste): 4,4 m = 1 length of 6 m (R$ 30,00)"; "• Cold water fittings (estimated): 4 pcs (R$ 12,00)"; "• Gate valves: 1 pc (R$ 45,00)"; "Estimated stage cost: R$ 87,00" |
| B3 | Água fria 25 mm: 50 | "• Cold water PVC pipe 25 mm (from plans, with 10% waste): 55,0 m = 10 lengths of 6 m (R$ 300,00)"; "Estimated stage cost: R$ 1.567,00" |
| B4 | Limpar e digitar só esgoto: 8 | "Estimated stage cost: R$ 589,00" |

### Teste C: erros de digitação

Base: Teste B. Mude só o indicado.

| # | O que mudar | Esperado na tela (em inglês) |
|---|---|---|
| C1 | Os três pontos vazios | Error: Enter at least one cold water, hot water or drain point. |
| C2 | Os três = 0 | Error: Enter at least one cold water, hot water or drain point. |
| C3 | Água fria = dez | Please enter valid numbers in the fields! |
| C4 | Água fria = -10 | Error: Quantities cannot be negative. |
| C5 | Água fria = 2,5 | Please enter valid numbers in the fields! |
| C6 | Perda = -5 | Error: Values cannot be negative. |
| C7 | Perda = 2,5 | "• Cold water PVC pipe 25 mm (estimated, with 2,5% waste): 41,0 m = 7 lengths of 6 m (R$ 210,00)"; "• Hot water CPVC pipe 22 mm (estimated, with 2,5% waste): 15,4 m = 6 lengths of 3 m (R$ 270,00)"; "• Drain PVC pipe 40 mm (estimated, with 2,5% waste): 24,6 m = 5 lengths of 6 m (R$ 175,00)"; "• Drain PVC pipe 100 mm (estimated, with 2,5% waste): 16,4 m = 3 lengths of 6 m (R$ 270,00)"; "Estimated stage cost: R$ 1.477,00" |
| C8 | Água fria 25 mm = -10 | Error: Values cannot be negative. |
| C9 | Água fria 25 mm = 0 | "Estimated stage cost: R$ 1.267,00" |
| C10, C11, C12 | Água fria 25 mm = 50,5, depois 50.5, depois 50 1/2 | Todos: "• Cold water PVC pipe 25 mm (from plans, with 10% waste): 55,6 m = 10 lengths of 6 m (R$ 300,00)"; "Estimated stage cost: R$ 1.567,00" |
| C13 | Água fria 25 mm = abc | Please enter valid numbers in the fields! |
| C14 | Água fria 25 mm = 1-21/2 | Please enter valid numbers in the fields! |
| C15 | Água fria = 1000 | Janela "Check the values": "1.000 cold water points: the limit is 200." Continue → "Cold water points: 1.000"; "• Cold water PVC pipe 25 mm (estimated, with 10% waste): 4.400,0 m = 734 lengths of 6 m (R$ 22.020,00)"; "• Cold water fittings (estimated): 4.000 pcs (R$ 12.000,00)"; "• Gate valves: 251 pcs (R$ 11.295,00)"; "Estimated stage cost: R$ 46.282,00" |

**Limites com aviso** (janela "Check the values", com Cancel e Continue): até 200 pontos de cada tipo (água fria, água quente e esgoto) (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Hidráulica)

- Botões em inglês: Clear, Previous, Next stage (linha própria), Finish. Calcular = "Calculate".
- O "?" abre "Help" com este texto (e o botão "Close"):

> Enter the cold water, hot water and drain points. The app estimates pipes, fittings and valves. If you have the plans, enter the lengths.
>
> A point is each outlet: faucet, shower, toilet, floor drain, washing machine... Any length field left empty is estimated by the app.
>
> Optional fields come with default values. Change them only if you want to.

- O que já valia na rodada 1 continua valendo:

- Hidráulica é a última aba das Instalações. Botões: Limpar e Anterior (volta pra Elétrica); embaixo, "Avançar para a próxima etapa" (vai pro Contrapiso) e Finalizar. **Não tem Próximo.**
- Limpar: tudo vazio e perda 10.
- O "?" explica o que é ponto (torneira, chuveiro, vaso, ralo, máquina) e que metragem vazia é estimada. Termina com a nota dos valores padrão.
- Repare nas dicas dos tubos: "Água fria 25 mm, em metros" não diz "(opcional)", diferente da Elétrica. Me fala se quer que eu acrescente.

---

# CONTRAPISO (Floor screed)

**Como aparece em inglês** (confira se nenhuma dica fica cortada):

- Dimensions (Required)
- Floor screed area in m² (e.g. 40)
- Average thickness in cm (usually 5 to 7)
- Concrete mix (cement:sand:gravel) (Optional)
- Waste rate % (optional, e.g. 5)

### Teste A: todos os campos, opcionais trocados

| Campo | Digite / escolha |
|---|---|
| Área | 40 |
| Espessura média | 6 |
| Traço | 1:2:3 |
| Perda | 8 |

```
Floor screed area: 40,00 m²
Average thickness: 6 cm
Mix: 1:2:3
Total volume (with 8% waste): 2,592 m³
• Cement: 20 bags of 50 kg (R$ 720,00)
• Sand: 1,30 m³ (R$ 143,00)
• Gravel: 1,94 m³ (R$ 232,80)

Estimated stage cost: R$ 1.095,80
```

Pra entender: 40 m² × 0,06 m = 2,4 m³, com 8% = 2,592 m³. No traço 1:2:3 são 7,5 sacos por m³: 2,592 × 7,5 = 19,44 → 20 sacos.

### Teste B: só os obrigatórios

Área 40, Espessura 5. O resto como vem (traço 1:3:3, perda 5).

```
Floor screed area: 40,00 m²
Average thickness: 5 cm
Mix: 1:3:3
Total volume (with 5% waste): 2,100 m³
• Cement: 14 bags of 50 kg (R$ 504,00)
• Sand: 1,35 m³ (R$ 148,50)
• Gravel: 1,35 m³ (R$ 162,00)

Estimated stage cost: R$ 814,50
```

| # | Mudar | Esperado na tela (em inglês) |
|---|---|---|
| B2 | Traço: 1,5:5:5 | "Mix: 1,5:5:5"; "• Cement: 13 bags of 50 kg (R$ 468,00)"; "• Sand: 1,37 m³ (R$ 150,70)"; "• Gravel: 1,37 m³ (R$ 164,40)"; "Estimated stage cost: R$ 783,10" |

### Teste C: erros de digitação

Base: Teste B (área 40, espessura 5). Mude só o indicado.

| # | O que mudar | Esperado na tela (em inglês) |
|---|---|---|
| C1 | Área vazia | Please enter valid numbers in the fields! |
| C2 | Espessura vazia | Please enter valid numbers in the fields! |
| C3 | Área = quarenta | Please enter valid numbers in the fields! |
| C4 | Área = 0 | Error: Area and thickness must be greater than zero. |
| C5 | Área = -40 | Error: Area and thickness must be greater than zero. |
| C6 | Espessura = 0 | Error: Area and thickness must be greater than zero. |
| C7 | Espessura = -5 | Error: Area and thickness must be greater than zero. |
| C8, C9, C10 | Área = 40,5, depois 40.5, depois 40 1/2 | Todos: "Floor screed area: 40,50 m²"; "Total volume (with 5% waste): 2,126 m³"; "• Sand: 1,37 m³ (R$ 150,70)"; "• Gravel: 1,37 m³ (R$ 164,40)"; "Estimated stage cost: R$ 819,10" |
| C11 | Espessura = 5,5 | "Average thickness: 5,5 cm"; "Total volume (with 5% waste): 2,310 m³"; "• Cement: 15 bags of 50 kg (R$ 540,00)"; "• Sand: 1,49 m³ (R$ 163,90)"; "• Gravel: 1,49 m³ (R$ 178,80)"; "Estimated stage cost: R$ 882,70" |
| C12 | Perda = -5 | Error: Waste cannot be negative. |
| C13 | Perda = 2,5 | "Total volume (with 2,5% waste): 2,050 m³"; "• Sand: 1,32 m³ (R$ 145,20)"; "• Gravel: 1,32 m³ (R$ 158,40)"; "Estimated stage cost: R$ 807,60" |
| C14 | Perda vazia | Igual ao Teste B |
| C15 | Área = 1-21/2 | Please enter valid numbers in the fields! |
| C16 | Área = 100000 | Janela "Check the values": "Area of 100.000 m²: the limit is 2.000 m²." Continue → "Floor screed area: 100.000,00 m²"; "Total volume (with 5% waste): 5.250,000 m³"; "• Cement: 33.750 bags of 50 kg (R$ 1.215.000,00)"; "• Sand: 3.375,00 m³ (R$ 371.250,00)"; "• Gravel: 3.375,00 m³ (R$ 405.000,00)"; "Estimated stage cost: R$ 1.991.250,00" |
| C17 | Espessura = 50 | Janela "Check the values": "Thickness of 50 cm: the usual is 3 cm to 10 cm." Continue → "Average thickness: 50 cm"; "Total volume (with 5% waste): 21,000 m³"; "• Cement: 135 bags of 50 kg (R$ 4.860,00)"; "• Sand: 13,50 m³ (R$ 1.485,00)"; "• Gravel: 13,50 m³ (R$ 1.620,00)"; "Estimated stage cost: R$ 7.965,00" |
| C18 | Espessura = 0,5 | Janela "Check the values": "Thickness of 0,5 cm: the usual is 3 cm to 10 cm." Continue → "Average thickness: 0,5 cm"; "Total volume (with 5% waste): 0,210 m³"; "• Cement: 2 bags of 50 kg (R$ 72,00)"; "• Sand: 0,14 m³ (R$ 15,40)"; "• Gravel: 0,14 m³ (R$ 16,80)"; "Estimated stage cost: R$ 104,20" |

**Limites com aviso** (janela "Check the values", com Cancel e Continue): área até 2.000 m² e espessura de 3 a 10 cm (o normal, segundo o engenheiro, é de 5 a 7 cm) (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Contrapiso)

- Botões em inglês: Clear, Previous, Next, Finish. Calcular = "Calculate".
- O "?" abre "Help" com este texto (e o botão "Close"):

> Enter the room area and the average thickness. The app estimates the cement, sand and gravel for the concrete.
>
> Optional fields come with default values. Change them only if you want to.

- O que já valia na rodada 1 continua valendo:

- Botões: Limpar, Anterior (volta pra Hidráulica), Próximo (vai pro Reboco) e Finalizar.
- Limpar: área e espessura vazias, traço 1:3:3 e perda 5.
- O "?" fala da área dos cômodos e da espessura média. Termina com a nota dos valores padrão.
- Menu do traço com vírgula: 1:2:3, 1:3:3, 1:4:3, 1,5:5:5 (o 1:3:3 vem marcado).

---

# REBOCO (Plaster)

**Como aparece em inglês** (confira se nenhuma dica fica cortada):

- Dimensions (Required)
- Area to plaster in m² (e.g. 30)
- Plaster thickness in cm (e.g. 2)
- Mortar mix (cement:lime:sand)
- Doors and windows m² (optional, e.g. 5)
- Waste rate % (optional, e.g. 10)
- Plaster both sides (Optional)
- Scratch coat (Optional)
- Opções dos menus: Yes · No

### Teste A: todos os campos, opcionais trocados

| Campo | Digite / escolha |
|---|---|
| Área a rebocar | 30 |
| Espessura | 2,5 |
| Traço da massa | 1:0,5:6 |
| Portas e janelas | 5 |
| Perda | 12 |
| Rebocar os dois lados | Sim |
| Chapisco | Sim |

```
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

Estimated stage cost: R$ 578,60
```

Pra entender: 30 − 5 = 25 m², nos dois lados = 50 m². 50 × 0,025 m × 1,12 = 1,4 m³ de reboco. O chapisco (1:3, 0,5 cm) soma mais cimento e areia, mas não aparece como volume separado.

### Teste B: só os obrigatórios

Área 30. O resto como vem (espessura 2, traço 1:2:8, vãos vazio, perda 10, dois lados Não, chapisco Não).

```
Gross area: 30,00 m²
Thickness: 2 cm
Mix: 1:2:8
Plaster volume (with 10% waste): 0,660 m³
• Cement: 2 bags of 50 kg (R$ 72,00)
• Lime: 7 bags of 20 kg (R$ 126,00)
• Sand: 0,60 m³ (R$ 66,00)

Estimated stage cost: R$ 264,00
```

Pra entender: 30 × 0,02 × 1,10 = 0,66 m³. No 1:2:8 (11 partes): cimento 0,66 ÷ 11 × 1500 = 90 kg → 2 sacos; cal 0,66 × 2 ÷ 11 × 1100 = 132 kg → 7 sacos; areia 0,66 × 8 ÷ 11 × 1,25 (inchamento) = 0,60 m³.

Pra conferir o resto, use o Teste B e mude só o indicado:

| # | Mudar | Esperado na tela (em inglês) |
|---|---|---|
| B2 | Portas e janelas: 5 | "Openings (doors and windows): 5,00 m²"; "Net area: 25,00 m²"; "Plaster volume (with 10% waste): 0,550 m³"; "• Lime: 6 bags of 20 kg (R$ 108,00)"; "• Sand: 0,50 m³ (R$ 55,00)"; "Estimated stage cost: R$ 235,00" |
| B3 | Dois lados: Sim | "Area to plaster (both sides): 60,00 m²"; "Plaster volume (with 10% waste): 1,320 m³"; "• Cement: 4 bags of 50 kg (R$ 144,00)"; "• Lime: 14 bags of 20 kg (R$ 252,00)"; "• Sand: 1,20 m³ (R$ 132,00)"; "Estimated stage cost: R$ 528,00" |
| B4 | Chapisco: Sim | "Scratch coat: included (1:3, 0,5 cm)"; "• Cement: 4 bags of 50 kg (R$ 144,00)"; "• Sand: 0,75 m³ (R$ 82,50)"; "Estimated stage cost: R$ 352,50" |
| B5 | Traço: 1:0:3 | "Mix: 1:0:3"; "• Cement: 5 bags of 50 kg (R$ 180,00)"; "• Sand: 0,62 m³ (R$ 68,20)"; "Estimated stage cost: R$ 248,20" |

### Teste C: erros de digitação

Base: Teste B (área 30). Mude só o indicado.

| # | O que mudar | Esperado na tela (em inglês) |
|---|---|---|
| C1 | Área vazia | Please enter valid numbers in the fields! |
| C2 | Espessura vazia (apague o 2) | Please enter valid numbers in the fields! |
| C3 | Área = trinta | Please enter valid numbers in the fields! |
| C4 | Área = 0 | Error: Area and thickness must be greater than zero. |
| C5 | Área = -30 | Error: Area and thickness must be greater than zero. |
| C6 | Espessura = 0 | Error: Area and thickness must be greater than zero. |
| C7, C8, C9 | Área = 30,5, depois 30.5, depois 30 1/2 | Todos: "Gross area: 30,50 m²"; "Plaster volume (with 10% waste): 0,671 m³"; "• Sand: 0,61 m³ (R$ 67,10)"; "Estimated stage cost: R$ 265,10" |
| C10 | Portas e janelas = -5 | Error: Deduction and waste cannot be negative. |
| C11 | Portas e janelas = 30 | Error: The openings deduction must be smaller than the area. |
| C12 | Portas e janelas = 40 | Error: The openings deduction must be smaller than the area. |
| C13 | Perda = -5 | Error: Deduction and waste cannot be negative. |
| C14 | Perda = 2,5 | "Plaster volume (with 2,5% waste): 0,615 m³"; "• Sand: 0,56 m³ (R$ 61,60)"; "Estimated stage cost: R$ 259,60" |
| C15 | Área = 1-21/2 | Please enter valid numbers in the fields! |
| C16 | Portas e janelas = abc | Please enter valid numbers in the fields! |
| C17 | Área = 100000 | Janela "Check the values": "Area of 100.000 m²: the limit is 2.000 m²." Continue → "Gross area: 100.000,00 m²"; "Plaster volume (with 10% waste): 2.200,000 m³"; "• Cement: 6.000 bags of 50 kg (R$ 216.000,00)"; "• Lime: 22.000 bags of 20 kg (R$ 396.000,00)"; "• Sand: 2.000,00 m³ (R$ 220.000,00)"; "Estimated stage cost: R$ 832.000,00" |
| C18 | Espessura = 20 | Janela "Check the values": "Thickness of 20 cm: the usual is 0,5 cm to 4 cm." Continue → "Thickness: 20 cm"; "Plaster volume (with 10% waste): 6,600 m³"; "• Cement: 19 bags of 50 kg (R$ 684,00)"; "• Lime: 67 bags of 20 kg (R$ 1.206,00)"; "• Sand: 6,00 m³ (R$ 660,00)"; "Estimated stage cost: R$ 2.550,00" |

**Limites com aviso** (janela "Check the values", com Cancel e Continue): área até 2.000 m² e espessura de 0,5 a 4 cm (o normal é 2 cm) (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Reboco)

- Botões em inglês: Clear, Previous, Next, Finish. Calcular = "Calculate".
- O "?" abre "Help" com este texto (e o botão "Close"):

> Enter the area to plaster, the thickness and the mortar mix. Check whether both sides of the wall will be plastered and whether a scratch coat is needed.
>
> Optional fields come with default values. Change them only if you want to.

- O que já valia na rodada 1 continua valendo:

- Botões: Limpar, Anterior (volta pro Contrapiso), Próximo (vai pro Piso) e Finalizar.
- Limpar: espessura 2, traço 1:2:8, vãos vazio, perda 10, dois lados Não e chapisco Não.
- O "?" fala da área, da espessura, do traço, dos dois lados e do chapisco. Termina com a nota dos valores padrão.
- Menus (traço, dois lados, chapisco) alinhados no botão, com os títulos perto do campo de cima.
- Menu do traço com vírgula: 1:2:8, 1:0,5:6, 1,5:1:8, 1:0:3, 1,5:0:4.

---

# PISO (Floor)

**Como aparece em inglês** (confira se nenhuma dica fica cortada):

- Dimensions (Required)
- Floor area in m² (e.g. 40)
- Tile width in cm (e.g. 60)
- Tile height in cm (e.g. 60)
- m² per box (optional, e.g. 2)
- Patterned layout, diagonal or design (Optional)
- Waste % (optional; empty = automatic)
- Tile adhesive type (Optional)
- Baseboard in meters (optional, e.g. 20)
- Baseboard piece in m (optional, e.g. 2.40)
- Opções dos menus: Yes · No

### Teste A: todos os campos, opcionais trocados

| Campo | Digite / escolha |
|---|---|
| Área | 40 |
| Largura da peça | 60 |
| Altura da peça | 60 |
| m² por caixa | 2,16 |
| Assentamento com desenho | Sim |
| Perda | 12 |
| Argamassa | AC-II |
| Rodapé | 30 |
| Peça do rodapé | 0,6 |

```
Area: 40,00 m²
Area with waste (12%): 44,80 m²
Tile: 60x60 cm
Laying: patterned
• Tiles: 125
• Boxes: 21 (2,16 m² per box) (R$ 2.240,00)
• Tile adhesive AC-II: 12 bags of 20 kg (224,0 kg) (R$ 360,00)
• Baseboard: 33,60 m (56 pcs of 0,60 m) (R$ 504,00)

Estimated stage cost: R$ 3.104,00
```

Pra entender: como você digitou a perda (12), ela vale mesmo com desenho Sim (o 25% só entra com a perda vazia). 40 × 1,12 = 44,8 m² ÷ 0,36 m² por peça = 124,4 → 125 peças. Argamassa: a peça tem 60 cm (não passa de 60), então são 5 kg por m²: 44,8 × 5 = 224 kg ÷ 20 = 11,2 → 12 sacos. Rodapé: 30 × 1,12 = 33,6 m ÷ 0,6 = 56 peças.

### Teste B: só os obrigatórios

Área 40, Largura 60, Altura 60. O resto como vem (perda vazia, AC-I, desenho Não, caixa e rodapé vazios).

```
Area: 40,00 m²
Area with waste (10%, automatic): 44,00 m²
Tile: 60x60 cm
• Tiles: 123 (R$ 2.200,00)
• Tile adhesive AC-I: 11 bags of 20 kg (220,0 kg) (R$ 242,00)

Estimated stage cost: R$ 2.442,00
```

Pra entender: 40 × 1,10 = 44 m² ÷ 0,36 m² por peça = 122,2 → 123 peças. Argamassa: 44 × 5 kg = 220 kg ÷ 20 = 11 sacos. Se a peça tiver um lado acima de 60 cm, são 8 kg por m² (dupla colagem).

Pra conferir o resto, use o Teste B e mude só o indicado:

| # | Mudar | Esperado na tela (em inglês) |
|---|---|---|
| B2 | Peça 80 x 80 | "Area with waste (15%, automatic): 46,00 m²"; "Tile: 80x80 cm"; "• Tiles: 72 (R$ 2.300,00)"; "• Tile adhesive AC-I: 19 bags of 20 kg (368,0 kg) (R$ 418,00)"; "Estimated stage cost: R$ 2.718,00" |
| B3 | Peça 120 x 60 | "Area with waste (20%, automatic): 48,00 m²"; "Tile: 120x60 cm"; "• Tiles: 67 (R$ 2.400,00)"; "• Tile adhesive AC-I: 20 bags of 20 kg (384,0 kg) (R$ 440,00)"; "Estimated stage cost: R$ 2.840,00" |
| B4 | Desenho: Sim | "Area with waste (25%, automatic): 50,00 m²"; "Laying: patterned"; "• Tiles: 139 (R$ 2.500,00)"; "• Tile adhesive AC-I: 13 bags of 20 kg (250,0 kg) (R$ 286,00)"; "Estimated stage cost: R$ 2.786,00" |
| B5 | m² por caixa: 2,16 | "• Tiles: 123"; "• Boxes: 21 (2,16 m² per box) (R$ 2.200,00)" |
| B6 | Rodapé: 30 | "• Baseboard: 33,00 m (R$ 495,00)"; "Estimated stage cost: R$ 2.937,00" |
| B7 | Rodapé 30 + Peça do rodapé 0,6 | "• Baseboard: 33,00 m (55 pcs of 0,60 m) (R$ 495,00)"; "Estimated stage cost: R$ 2.937,00" |
| B8 | Argamassa: AC-III | "• Tile adhesive AC-III: 11 bags of 20 kg (220,0 kg) (R$ 462,00)"; "Estimated stage cost: R$ 2.662,00" |

### Teste C: erros de digitação

Base: Teste B (área 40, peça 60 x 60). Mude só o indicado.

| # | O que mudar | Esperado na tela (em inglês) |
|---|---|---|
| C1 | Área vazia | Please enter valid numbers in the fields! |
| C2 | Largura vazia | Please enter valid numbers in the fields! |
| C3 | Área = quarenta | Please enter valid numbers in the fields! |
| C4 | Área = 0 | Error: Area and tile size must be greater than zero. |
| C5 | Área = -40 | Error: Area and tile size must be greater than zero. |
| C6 | Largura = 0 | Error: Area and tile size must be greater than zero. |
| C7, C8, C9 | Área = 40,5, depois 40.5, depois 40 1/2 | Todos: "Area: 40,50 m²"; "Area with waste (10%, automatic): 44,55 m²"; "• Tiles: 124 (R$ 2.227,50)"; "• Tile adhesive AC-I: 12 bags of 20 kg (222,8 kg) (R$ 264,00)"; "Estimated stage cost: R$ 2.491,50" |
| C10 | Perda = -5 | Error: Waste cannot be negative. |
| C11 | Perda = 2,5 | "Area with waste (2,5%): 41,00 m²"; "• Tiles: 114 (R$ 2.050,00)"; "• Tile adhesive AC-I: 11 bags of 20 kg (205,0 kg) (R$ 242,00)"; "Estimated stage cost: R$ 2.292,00" |
| C12 | Perda = 0 | "Area with waste (0%): 40,00 m²"; "• Tiles: 112 (R$ 2.000,00)"; "• Tile adhesive AC-I: 10 bags of 20 kg (200,0 kg) (R$ 220,00)"; "Estimated stage cost: R$ 2.220,00" |
| C13 | m² por caixa = -2 | Error: Values cannot be negative. |
| C14 | Rodapé = -10 | Error: Values cannot be negative. |
| C15 | Área = 1-21/2 | Please enter valid numbers in the fields! |
| C16 | Peça 70 x 70 | "Tile: 70x70 cm"; "• Tiles: 90 (R$ 2.200,00)"; "• Tile adhesive AC-I: 18 bags of 20 kg (352,0 kg) (R$ 396,00)"; "Estimated stage cost: R$ 2.596,00" |
| C17 | Peça 90 x 90 | "Area with waste (15%, automatic): 46,00 m²"; "Tile: 90x90 cm"; "• Tiles: 57 (R$ 2.300,00)"; "• Tile adhesive AC-I: 19 bags of 20 kg (368,0 kg) (R$ 418,00)"; "Estimated stage cost: R$ 2.718,00" |
| C18 | Largura = 60,5 | "Tile: 60,5x60 cm"; "• Tiles: 122 (R$ 2.200,00)"; "• Tile adhesive AC-I: 18 bags of 20 kg (352,0 kg) (R$ 396,00)"; "Estimated stage cost: R$ 2.596,00" |
| C19 | Só a peça do rodapé (0,6), sem rodapé | Igual ao Teste B |
| C20 | Área = 100000 | Janela "Check the values": "Area of 100.000 m²: the limit is 2.000 m²." Continue → "Area: 100.000,00 m²"; "Area with waste (10%, automatic): 110.000,00 m²"; "• Tiles: 305.556 (R$ 5.500.000,00)"; "• Tile adhesive AC-I: 27.500 bags of 20 kg (550.000,0 kg) (R$ 605.000,00)"; "Estimated stage cost: R$ 6.105.000,00" |

Dica de botão: se o Contrapiso estiver preenchido (ex.: área 40), aparece no Piso o botão "Use the Floor screed area: 40 m²". Toque nele: a área do Piso fica 40.

**Limites com aviso** (janela "Check the values", com Cancel e Continue): área até 2.000 m² e peça de 5 a 300 cm em cada lado (existe porcelanato de 120 x 240) (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Piso)

- Botões em inglês: Clear, Previous, Next, Finish. Calcular = "Calculate".
- O "?" abre "Help" com este texto (e o botão "Close"):

> Enter the area and the tile size (e.g. 60x60 cm). If you like, add the m² per box, the adhesive type and the baseboard. The app estimates boxes and bags of tile adhesive. AC-I, AC-II and AC-III are Brazilian tile adhesive classes (AC-III for wet areas).
>
> Tile adhesive: 5 kg per m²; for tiles with a side over 60 cm, 8 kg per m², because the adhesive goes on the tile and on the floor (back-buttering).
>
> If you leave the waste empty, the app uses 10% for tiles up to 70 cm, 15% up to 90 cm and 20% above that (25% for a patterned layout). For the baseboard, also enter the length of each piece so the app can count the pieces.
>
> Optional fields come with default values. Change them only if you want to.

- O que já valia na rodada 1 continua valendo:

- Botões: Limpar, Anterior (volta pro Reboco), Próximo (vai pro Azulejo) e Finalizar.
- Limpar: perda vazia, AC-I, desenho Não, caixa e rodapé vazios.
- O "?" explica a argamassa (5 kg por m²; 8 kg por m² com um lado acima de 60 cm, dupla colagem), a perda automática (10% até 70 cm, 15% até 90 cm, 20% acima, 25% com desenho) e o tamanho da peça do rodapé. Termina com a nota dos valores padrão.
- Título comprido "Assentamento com desenho, diagonal ou paginado (Opcional)": se quebrar em 2 linhas, não pode invadir o campo de cima.
- Menu da argamassa: AC-I, AC-II, AC-III.

---

# AZULEJO (Wall Tile)

**Como aparece em inglês** (confira se nenhuma dica fica cortada):

- Dimensions (Required)
- Wall area to tile in m² (e.g. 30)
- Tile width in cm (e.g. 60)
- Tile height in cm (e.g. 60)
- Doors and windows m² (optional, e.g. 5)
- m² per box (optional, e.g. 2)
- Patterned layout, diagonal or design (Optional)
- Waste % (optional; empty = automatic)
- Tile adhesive type (Optional)
- Opções dos menus: Yes · No

### Teste A: todos os campos, opcionais trocados

| Campo | Digite / escolha |
|---|---|
| Área de parede | 30 |
| Largura da peça | 30 |
| Altura da peça | 60 |
| Portas e janelas | 4 |
| m² por caixa | 1,8 |
| Assentamento com desenho | Sim |
| Perda | 15 |
| Argamassa | AC-III |

```
Area: 30,00 m²
Openings (doors and windows): 4,00 m²
Net area: 26,00 m²
Area with waste (15%): 29,90 m²
Tile: 30x60 cm
Laying: patterned
• Tiles: 167
• Boxes: 17 (1,80 m² per box) (R$ 1.196,00)
• Tile adhesive AC-III: 8 bags of 20 kg (149,5 kg) (R$ 336,00)

Estimated stage cost: R$ 1.532,00
```

Pra entender: 30 − 4 = 26 m² × 1,15 = 29,9 m² ÷ 0,18 m² por peça = 166,1 → 167 peças; ÷ 1,8 m² por caixa = 16,6 → 17 caixas. Argamassa: 29,9 × 5 kg = 149,5 kg → 8 sacos.

### Teste B: só os obrigatórios

Área 30, Largura 30, Altura 60. O resto como vem (vãos vazio, perda vazia, AC-II, desenho Não, caixa vazia).

```
Area: 30,00 m²
Area with waste (10%, automatic): 33,00 m²
Tile: 30x60 cm
• Tiles: 184 (R$ 1.320,00)
• Tile adhesive AC-II: 9 bags of 20 kg (165,0 kg) (R$ 270,00)

Estimated stage cost: R$ 1.590,00
```

| # | Mudar | Esperado na tela (em inglês) |
|---|---|---|
| B2 | Portas e janelas: 4 | "Openings (doors and windows): 4,00 m²"; "Net area: 26,00 m²"; "Area with waste (10%, automatic): 28,60 m²"; "• Tiles: 159 (R$ 1.144,00)"; "• Tile adhesive AC-II: 8 bags of 20 kg (143,0 kg) (R$ 240,00)"; "Estimated stage cost: R$ 1.384,00" |
| B3 | m² por caixa: 1,8 | "• Tiles: 184"; "• Boxes: 19 (1,80 m² per box) (R$ 1.320,00)" |
| B4 | Desenho: Sim | "Area with waste (25%, automatic): 37,50 m²"; "Laying: patterned"; "• Tiles: 209 (R$ 1.500,00)"; "• Tile adhesive AC-II: 10 bags of 20 kg (187,5 kg) (R$ 300,00)"; "Estimated stage cost: R$ 1.800,00" |
| B5 | Argamassa: AC-III | "• Tile adhesive AC-III: 9 bags of 20 kg (165,0 kg) (R$ 378,00)"; "Estimated stage cost: R$ 1.698,00" |
| B6 | Peça 30 x 90 | "Area with waste (15%, automatic): 34,50 m²"; "Tile: 30x90 cm"; "• Tiles: 128 (R$ 1.380,00)"; "• Tile adhesive AC-II: 14 bags of 20 kg (276,0 kg) (R$ 420,00)"; "Estimated stage cost: R$ 1.800,00" |

### Teste C: erros de digitação

Base: Teste B (área 30, peça 30 x 60). Mude só o indicado.

| # | O que mudar | Esperado na tela (em inglês) |
|---|---|---|
| C1 | Área vazia | Please enter valid numbers in the fields! |
| C2 | Altura vazia | Please enter valid numbers in the fields! |
| C3 | Área = trinta | Please enter valid numbers in the fields! |
| C4 | Área = 0 | Error: Area and tile size must be greater than zero. |
| C5 | Área = -30 | Error: Area and tile size must be greater than zero. |
| C6, C7, C8 | Área = 30,5, depois 30.5, depois 30 1/2 | Todos: "Area: 30,50 m²"; "Area with waste (10%, automatic): 33,55 m²"; "• Tiles: 187 (R$ 1.342,00)"; "• Tile adhesive AC-II: 9 bags of 20 kg (167,8 kg) (R$ 270,00)"; "Estimated stage cost: R$ 1.612,00" |
| C9 | Portas e janelas = -4 | Error: Values cannot be negative. |
| C10 | Portas e janelas = 30 | Error: The openings deduction must be smaller than the area. |
| C11 | Portas e janelas = 40 | Error: The openings deduction must be smaller than the area. |
| C12 | Perda = -5 | Error: Waste cannot be negative. |
| C13 | Perda = 2,5 | "Area with waste (2,5%): 30,75 m²"; "• Tiles: 171 (R$ 1.230,00)"; "• Tile adhesive AC-II: 8 bags of 20 kg (153,8 kg) (R$ 240,00)"; "Estimated stage cost: R$ 1.470,00" |
| C14 | Área = 1-21/2 | Please enter valid numbers in the fields! |
| C15 | Portas e janelas = abc | Please enter valid numbers in the fields! |
| C16 | Área = 100000 | Janela "Check the values": "Area of 100.000 m²: the limit is 2.000 m²." Continue → "Area: 100.000,00 m²"; "Area with waste (10%, automatic): 110.000,00 m²"; "• Tiles: 611.112 (R$ 4.400.000,00)"; "• Tile adhesive AC-II: 27.500 bags of 20 kg (550.000,0 kg) (R$ 825.000,00)"; "Estimated stage cost: R$ 5.225.000,00" |

**Limites com aviso** (janela "Check the values", com Cancel e Continue): os mesmos do Piso (área até 2.000 m² e peça de 5 a 300 cm em cada lado).

### Visual (Azulejo)

- Botões em inglês: Clear, Previous, Next, Finish. Calcular = "Calculate".
- O "?" abre "Help" com este texto (e o botão "Close"):

> Enter the wall area to tile and the tile size. Deduct doors and windows and, if you like, enter the m² per box and the adhesive type. AC-I, AC-II and AC-III are Brazilian tile adhesive classes (AC-III for wet areas).
>
> Tile adhesive: 5 kg per m²; for tiles with a side over 60 cm, 8 kg per m², because the adhesive goes on the tile and on the wall (back-buttering).
>
> If you leave the waste empty, the app uses 10% for tiles up to 70 cm, 15% up to 90 cm and 20% above that (25% for a patterned layout).
>
> Optional fields come with default values. Change them only if you want to.

- O que já valia na rodada 1 continua valendo:

- Botões: Limpar, Anterior (volta pro Piso), Próximo (vai pro Rejunte) e Finalizar.
- Limpar: vãos, caixa e perda vazios, AC-II e desenho Não.
- No Azulejo não aparecem o rodapé nem o botão do Contrapiso.
- O "?" fala dos vãos, do AC-III para áreas molhadas, da argamassa (5 ou 8 kg por m²) e da perda automática. Termina com a nota dos valores padrão.

---

# REJUNTE (Grout)

**Como aparece em inglês** (confira se nenhuma dica fica cortada):

- Dimensions (Required)
- Area to grout in m² (e.g. 40)
- Tile width in cm (e.g. 60)
- Tile height in cm (e.g. 60)
- Joint width in mm (e.g. 3)
- Tile thickness in mm (optional, e.g. 8)
- Waste rate % (optional, e.g. 10)

### Teste A: todos os campos, opcionais trocados

| Campo | Digite / escolha |
|---|---|
| Área | 40 |
| Largura da peça | 60 |
| Altura da peça | 60 |
| Junta | 3 |
| Espessura da peça | 10 |
| Perda | 15 |

```
Area: 40,00 m²
Tile: 60x60 cm
Joint: 3 mm
Tile thickness: 10 mm
Consumption: 0,158 kg/m²
• Grout (with 15% waste): 7,3 kg = 4 tubs of 2 kg (R$ 72,00)

Estimated stage cost: R$ 72,00
```

Pra entender: a fórmula é ((600 + 600) ÷ (600 × 600)) × 3 × 10 × 1,58 = 0,158 kg/m². × 40 m² × 1,15 = 7,27 kg (na tela aparece 7,3 kg, com 1 casa). Ficam 3 latas de 2 kg (6 kg) e faltam 1,27 kg; 2 latas de 1 kg somariam 2 kg, igual a uma de 2 kg, então o app troca por mais uma de 2 kg: 4 latas de 2 kg.

### Teste B: só os obrigatórios

Área 40, Largura 60, Altura 60, Junta 3. O resto como vem (espessura 8, perda 10).

```
Area: 40,00 m²
Tile: 60x60 cm
Joint: 3 mm
Tile thickness: 8 mm
Consumption: 0,126 kg/m²
• Grout (with 10% waste): 5,6 kg = 3 tubs of 2 kg (R$ 54,00)

Estimated stage cost: R$ 54,00
```

| # | Mudar | Esperado na tela (em inglês) |
|---|---|---|
| B2 | Peça 30 x 30 + Junta 5 | "Tile: 30x30 cm"; "Joint: 5 mm"; "Consumption: 0,421 kg/m²"; "• Grout (with 10% waste): 18,5 kg = 9 tubs of 2 kg and 1 tub of 1 kg (R$ 172,00)"; "Estimated stage cost: R$ 172,00" |
| B3 | Botão "Use Floor data" (com o Teste B do Piso preenchido) | Igual ao Teste B |
| B4 | Botão "Use Wall Tile data" (com o B2 do Azulejo: área 30, vãos 4, peça 30 x 60) | "Area: 26,00 m²"; "Tile: 30x60 cm"; "Joint: 2 mm"; "• Grout (with 10% waste): 3,6 kg = 2 tubs of 2 kg (R$ 36,00)"; "Estimated stage cost: R$ 36,00" |

### Teste C: erros de digitação

Base: Teste B. Mude só o indicado.

| # | O que mudar | Esperado na tela (em inglês) |
|---|---|---|
| C1 | Área vazia | Please enter valid numbers in the fields! |
| C2 | Junta vazia | Please enter valid numbers in the fields! |
| C3 | Área = quarenta | Please enter valid numbers in the fields! |
| C4 | Área = 0 | Error: Area, tile size and joint must be greater than zero. |
| C5 | Área = -40 | Error: Area, tile size and joint must be greater than zero. |
| C6 | Junta = 0 | Error: Area, tile size and joint must be greater than zero. |
| C7 | Junta = -3 | Error: Area, tile size and joint must be greater than zero. |
| C8, C9, C10 | Área = 40,5, depois 40.5, depois 40 1/2 | Todos: "Area: 40,50 m²" |
| C11 | Junta = 1,5 | "Joint: 1,5 mm"; "Consumption: 0,063 kg/m²"; "• Grout (with 10% waste): 2,8 kg = 1 tub of 2 kg and 1 tub of 1 kg (R$ 28,00)"; "Estimated stage cost: R$ 28,00" |
| C12 | Junta = 1/2 | Janela "Check the values": "Joint of 0,5 mm: the usual is 1 mm to 15 mm." Continue → "Joint: 0,5 mm"; "Consumption: 0,021 kg/m²"; "• Grout (with 10% waste): 0,9 kg = 1 tub of 1 kg (R$ 10,00)"; "Estimated stage cost: R$ 10,00" |
| C13 | Espessura vazia | Igual ao Teste B |
| C14 | Espessura = 0 | Error: The tile thickness must be greater than zero. |
| C15 | Perda = -5 | Error: Waste cannot be negative. |
| C16 | Perda = 2,5 | "• Grout (with 2,5% waste): 5,2 kg = 3 tubs of 2 kg (R$ 54,00)" |
| C17 | Área = 1-21/2 | Please enter valid numbers in the fields! |
| C18 | Área = 1 | "Area: 1,00 m²"; "• Grout (with 10% waste): 0,1 kg = 1 tub of 1 kg (R$ 10,00)"; "Estimated stage cost: R$ 10,00" |
| C19 | Área = 100000 | Janela "Check the values": "Area of 100.000 m²: the limit is 2.000 m²." Continue → "Area: 100.000,00 m²"; "• Grout (with 10% waste): 13.904,0 kg = 6.952 tubs of 2 kg (R$ 125.136,00)"; "Estimated stage cost: R$ 125.136,00" |
| C20 | Junta = 30 | Janela "Check the values": "Joint of 30 mm: the usual is 1 mm to 15 mm." Continue → "Joint: 30 mm"; "Consumption: 1,264 kg/m²"; "• Grout (with 10% waste): 55,6 kg = 28 tubs of 2 kg (R$ 504,00)"; "Estimated stage cost: R$ 504,00" |

**Limites com aviso** (janela "Check the values", com Cancel e Continue): área até 2.000 m² e junta de 1 a 15 mm (junta de 30 mm é quase certeza de quem digitou em cm) (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Rejunte)

- Botões em inglês: Clear, Previous, Next, Finish. Calcular = "Calculate".
- O "?" abre "Help" com este texto (e o botão "Close"):

> Enter the area, the tile size and the joint width. If you already filled in Floor or Wall Tile, tap "Use Floor data" (or Wall Tile) at the top of the tab to fill in the area and tile size. Tile thickness is optional (default 8 mm). The app estimates the kg of grout and how many 1 kg and 2 kg tubs to buy.
>
> Optional fields come with default values. Change them only if you want to.

- O que já valia na rodada 1 continua valendo:

- Botões: Limpar, Anterior (volta pro Azulejo), Próximo (vai pra Pintura) e Finalizar.
- Limpar: área, peça e junta vazias, espessura 8 e perda 10.
- Os botões "Use Floor data (40 m², tile 60x60 cm)" e "Use Wall Tile data (26 m², tile 30x60 cm)" só aparecem se essas abas estiverem preenchidas.
- O "?" fala dos botões "Use ... data", da espessura padrão de 8 mm e das latinhas de 1 kg e 2 kg. Termina com a nota dos valores padrão.

---

# PINTURA (Painting)

**Como aparece em inglês** (confira se nenhuma dica fica cortada):

- Areas and coats
- Wall area in m² (e.g. 100)
- Ceiling area in m² (e.g. 40)
- Number of coats (e.g. 2)
- Coverage in m²/L (optional, e.g. 12)
- Sealer (Optional)
- Putty (Optional)
- Primer (Optional)
- Waste rate % (optional, e.g. 10)
- Opções dos menus: Yes · No · None · Wall putty · Acrylic putty

### Teste A: todos os campos, opcionais trocados

| Campo | Digite / escolha |
|---|---|
| Área de parede | 100 |
| Área de teto | 40 |
| Demãos | 3 |
| Rendimento | 10 |
| Selador | Sim |
| Massa | Massa corrida |
| Fundo preparador | Sim |
| Perda | 15 |

```
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

Estimated stage cost: R$ 1.825,00
```

Pra entender: parede 100 × 3 demãos ÷ 10 × 1,15 = 34,5 L. Os complementos são uma demão sobre parede + teto (140 m²): selador 140 ÷ 8 × 1,15 = 20,1 L; fundo 140 ÷ 10 × 1,15 = 16,1 L; massa 140 × 0,5 kg × 2 demãos × 1,15 = 161 kg ÷ 25 = 6,4 → 7 baldes. No fundo, 16,1 L precisaria de 5 galões (18 L), que é o mesmo que 1 lata, então o app leva 1 lata.

### Teste B: só os obrigatórios

Área de parede 100. O resto como vem (teto vazio, demãos 2, rendimento 12, selador Não, massa Não, fundo Não, perda 10).

```
Walls: 100,00 m²
Coats: 2
Coverage: 12 m²/L
• Wall paint (with 10% waste): 18,3 L = 1 pail of 18 L and 1 can of 3,6 L (R$ 390,00)

Estimated stage cost: R$ 390,00
```

Pra conferir o resto, use o Teste B e mude só o indicado:

| # | Mudar | Esperado na tela (em inglês) |
|---|---|---|
| B2 | Parede vazia + Teto 40 | "Ceiling: 40,00 m²"; "• Ceiling paint (with 10% waste): 7,3 L = 3 cans of 3,6 L (R$ 225,00)"; "Estimated stage cost: R$ 225,00" |
| B3 | Teto: 40 (com a parede 100) | "Ceiling: 40,00 m²"; "• Ceiling paint (with 10% waste): 7,3 L = 3 cans of 3,6 L (R$ 225,00)"; "Estimated stage cost: R$ 615,00" |
| B4 | Selador: Sim | "• Sealer (with 10% waste): 13,8 L = 4 cans of 3,6 L (R$ 180,00)"; "Add-ons (over wall + ceiling): Sealer 1 coat"; "Estimated stage cost: R$ 570,00" |
| B5 | Massa: Massa acrílica | "• Acrylic putty (with 10% waste): 110,0 kg = 5 buckets of 25 kg (R$ 650,00)"; "Add-ons (over wall + ceiling): Acrylic putty 2 coats"; "Estimated stage cost: R$ 1.040,00" |
| B6 | Fundo preparador: Sim | "• Primer (with 10% waste): 11,0 L = 4 cans of 3,6 L (R$ 200,00)"; "Add-ons (over wall + ceiling): Primer 1 coat"; "Estimated stage cost: R$ 590,00" |
| B7 | Parede: 180 | "Walls: 180,00 m²"; "• Wall paint (with 10% waste): 33,0 L = 2 pails of 18 L (R$ 600,00)"; "Estimated stage cost: R$ 600,00" |
| B8 | Parede: 10 | "Walls: 10,00 m²"; "• Wall paint (with 10% waste): 1,8 L = 1 can of 3,6 L (R$ 90,00)"; "Estimated stage cost: R$ 90,00" |

### Teste C: erros de digitação

Base: Teste B (parede 100). Mude só o indicado.

| # | O que mudar | Esperado na tela (em inglês) |
|---|---|---|
| C1 | Parede e teto vazios | Please enter valid numbers in the fields! |
| C2 | Demãos vazia | Please enter valid numbers in the fields! |
| C3 | Parede = cem | Please enter valid numbers in the fields! |
| C4 | Parede = 0 | Error: Enter the wall area or the ceiling area. |
| C5 | Parede = -100 | Error: Areas cannot be negative. |
| C6 | Demãos = 0 | Error: Coats and coverage must be greater than zero. |
| C7 | Demãos = -2 | Error: Coats and coverage must be greater than zero. |
| C8 | Demãos = 2,5 | Please enter valid numbers in the fields! |
| C9 | Demãos = 5 | "Coats: 5"; "• Wall paint (with 10% waste): 45,8 L = 2 pails of 18 L and 3 cans of 3,6 L (R$ 870,00)"; "Estimated stage cost: R$ 870,00" |
| C10 | Demãos = 6 | Janela "Check the values": "6 coats: the limit is 5 (usually 2 or 3)." Continue → "Coats: 6"; "• Wall paint (with 10% waste): 55,0 L = 3 pails of 18 L and 1 can of 3,6 L (R$ 990,00)"; "Estimated stage cost: R$ 990,00" |
| C11 | Demãos = 22 | Janela "Check the values": "22 coats: the limit is 5 (usually 2 or 3)." Continue → "Coats: 22"; "• Wall paint (with 10% waste): 201,7 L = 11 pails of 18 L and 2 cans of 3,6 L (R$ 3.480,00)"; "Estimated stage cost: R$ 3.480,00" |
| C12, C13, C14 | Parede = 100,5, depois 100.5, depois 100 1/2 | Todos: "Walls: 100,50 m²"; "• Wall paint (with 10% waste): 18,4 L = 1 pail of 18 L and 1 can of 3,6 L (R$ 390,00)" |
| C15 | Rendimento = 0 | Error: Coats and coverage must be greater than zero. |
| C16 | Rendimento vazio | Igual ao Teste B |
| C17 | Rendimento = 12,5 | "Coverage: 12,5 m²/L"; "• Wall paint (with 10% waste): 17,6 L = 1 pail of 18 L (R$ 300,00)"; "Estimated stage cost: R$ 300,00" |
| C18 | Perda = -5 | Error: Waste cannot be negative. |
| C19 | Perda = 2,5 | "• Wall paint (with 2,5% waste): 17,1 L = 1 pail of 18 L (R$ 300,00)"; "Estimated stage cost: R$ 300,00" |
| C20 | Parede = 1-21/2 | Please enter valid numbers in the fields! |
| C21 | Parede = 100000 | Janela "Check the values": "Wall area of 100.000 m²: the limit is 5.000 m²." Continue → "Walls: 100.000,00 m²"; "• Wall paint (with 10% waste): 18.333,3 L = 1.018 pails of 18 L and 3 cans of 3,6 L (R$ 305.670,00)"; "Estimated stage cost: R$ 305.670,00" |

**Limites com aviso** (janela "Check the values", com Cancel e Continue): demãos até 5 (antes era erro) e área de parede e de teto até 5.000 m² cada (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Pintura)

- Botões em inglês: Clear, Previous, Next, Finish. Calcular = "Calculate".
- O "?" abre "Help" com este texto (e o botão "Close"):

> Enter the wall area, ceiling area and number of coats. Paint coverage is already filled in. If you like, add sealer, wall putty and primer.
>
> You can fill in only walls or only ceiling. Coverage is how many m² 1 liter of paint covers in one coat (see the can).
>
> Wall putty is for dry indoor areas; acrylic putty, for outdoor or damp areas. Putty is counted with 2 coats.
>
> Optional fields come with default values. Change them only if you want to.

- O que já valia na rodada 1 continua valendo:

- Botões: Limpar, Anterior (volta pro Rejunte), Próximo (vai pra Esquadrias) e Finalizar.
- Limpar: parede e teto vazios, demãos 2, rendimento 12, perda 10, selador Não, massa Não e fundo Não.
- O "?" explica que dá para preencher só parede ou só teto, o que é o rendimento, a diferença entre massa corrida e acrílica e que a massa é contada em 2 demãos. Termina com a nota dos valores padrão.
- Menu da massa: Não, Massa corrida, Massa acrílica.

---

# ESQUADRIAS (Doors & Windows)

**Como aparece em inglês** (confira se nenhuma dica fica cortada):

- New door or window
- Type
- Material (Optional)
- Quantity (e.g. 3)
- Opening width in cm (e.g. 80)
- Opening height in cm (e.g. 210)
- Add to list
- List for quotes
- No doors or windows on the list yet.
- Fixing materials
- Expanding foam (Optional)
- Screws and anchors (Optional)
- Fixing mortar (Optional)
- Opções dos menus: Door · Window · Not specified · Aluminum · Wood · Tempered glass · Yes · No

Aqui o jeito de preencher é diferente: para cada tamanho, escolha o Tipo e o Material, digite Quantidade, Largura e Altura e toque em **Adicionar à lista**. Depois toque em Calcular.

### Teste A: todos os campos, insumos em Sim

Adicione estes 4 itens:

| Tipo | Material | Quantidade | Largura | Altura |
|---|---|---|---|---|
| Porta | Madeira | 3 | 80 | 210 |
| Porta | Alumínio | 1 | 90 | 210 |
| Janela | Alumínio | 4 | 120 | 100 |
| Janela | Vidro temperado | 1 | 60 | 60 |

Espuma expansiva: Sim. Parafusos com bucha: Sim. Argamassa de fixação: Sim.

```
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

Doors and windows: use this list to request a quote from the supplier.
```

Pra entender: o contorno da porta é os dois lados + a parte de cima (2 × 2,10 + 0,80 = 5,0 m); o da janela, os quatro lados (2 × (1,20 + 1,00) = 4,4 m). Tudo somado dá 40,1 m. Espuma: 40,1 ÷ 6 = 6,7 → 7 tubos. Parafusos: 40,1 ÷ 0,4 = 100,25 → 101. Argamassa: 40,1 × 1,5 = 60,2 kg → 4 sacos.

### Teste B: só os obrigatórios

Adicione: Porta, 3, 80, 210 e Janela, 2, 120, 100 (material como vem: Não informado). Insumos todos em Não.

```
Doors:
• 3x Door 80 x 210 cm: 1,68 m² each

Windows:
• 2x Window 120 x 100 cm: 1,20 m² each

Total: 3 doors and 2 windows
Total opening area: 7,44 m²

Doors and windows: use this list to request a quote from the supplier.
```

Pra conferir o resto, use o Teste B e mude só o indicado:

| # | Mudar | Esperado na tela (em inglês) |
|---|---|---|
| B2 | Espuma: Sim | "Fixing materials:"; "• Expanding foam: 4 cans of 500 ml (R$ 140,00)"; "Estimated stage cost: R$ 140,00" |
| B3 | Parafusos: Sim | "Fixing materials:"; "• Screws and anchors: 60 pcs (R$ 48,00)"; "Estimated stage cost: R$ 48,00" |
| B4 | Argamassa: Sim | "Fixing materials:"; "• Fixing mortar: 35,7 kg = 2 bags of 20 kg (R$ 50,00)"; "Estimated stage cost: R$ 50,00" |
| B5 | Adicione de novo: Porta, 2, 80, 210 | "• 5x Door 80 x 210 cm: 1,68 m² each"; "Total: 5 doors and 2 windows"; "Total opening area: 10,80 m²" |
| B6 | Toque no X da janela | "Total: 3 doors"; "Total opening area: 5,04 m²" |

### Teste C: erros de digitação

| # | O que fazer | Esperado na tela (em inglês) |
|---|---|---|
| C1 | Lista vazia + Calcular | No doors or windows on the list yet. |
| C2 | Quantidade vazia + Adicionar à lista | Please enter valid numbers in the fields! (nada entra na lista) |
| C3 | Quantidade = três + Adicionar | Please enter valid numbers in the fields! (nada entra na lista) |
| C4 | Quantidade = 0 + Adicionar | Please enter valid numbers in the fields! (nada entra na lista) |
| C5 | Quantidade = -3 + Adicionar | Please enter valid numbers in the fields! (nada entra na lista) |
| C6 | Quantidade = 2,5 + Adicionar | Please enter valid numbers in the fields! (nada entra na lista) |
| C7 | Largura = 0 + Adicionar | Please enter valid numbers in the fields! (nada entra na lista) |
| C8 | Largura = 1-21/2 + Adicionar | Please enter valid numbers in the fields! (nada entra na lista) |
| C9 | Digitar uma porta (3, 80, 210) e tocar em Calcular sem Adicionar | You entered a door or window but did not tap "Add to list". |
| C10 | Janela 1, 120,5, 100 (depois 120.5, depois 120 1/2) | Todos: "• 1x Window 120,5 x 100 cm: 1,21 m² each"; "Total: 1 window"; "Total opening area: 1,21 m²" |
| C11 | Só 1 porta 80 x 210 com os 3 insumos em Sim | "• 1x Door 80 x 210 cm: 1,68 m² each"; "Total: 1 door"; "Total opening area: 1,68 m²"; "Fixing materials:"; "• Expanding foam: 1 can of 500 ml (R$ 35,00)"; "• Screws and anchors: 13 pcs (R$ 10,40)"; "• Fixing mortar: 7,5 kg = 1 bag of 20 kg (R$ 25,00)"; "Estimated stage cost: R$ 70,40" |
| C12 | Porta, 1000, 80, 210 com os 3 insumos | Janela "Check the values" no "Add to list": "Quantity of 1.000: the limit is 100 of each item." Continue → "• 1.000x Door 80 x 210 cm: 1,68 m² each"; "Total: 1.000 doors"; "Total opening area: 1.680,00 m²"; "Fixing materials:"; "• Expanding foam: 834 cans of 500 ml (R$ 29.190,00)"; "• Screws and anchors: 12.500 pcs (R$ 10.000,00)"; "• Fixing mortar: 7.500,0 kg = 375 bags of 20 kg (R$ 9.375,00)"; "Estimated stage cost: R$ 48.565,00" |
| C13 | Porta, 3, 8000, 210 | Janela "Check the values" no "Add to list": "Width of 8.000 cm: the limit is 500 cm." Continue → "• 3x Door 8.000 x 210 cm: 168,00 m² each"; "Total: 3 doors"; "Total opening area: 504,00 m²" |

**Limites com aviso** (janela "Check the values", com Cancel e Continue): até 100 de cada item, largura até 500 cm e altura até 400 cm (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir). Na Esquadrias, a janela aparece no "Adicionar à lista", antes de o item entrar na lista.

### Visual (Esquadrias)

- Botões em inglês: Clear, Previous, Finish. Calcular = "Calculate".
- O "?" abre "Help" com este texto (e o botão "Close"):

> List the doors and windows with quantity and size. The app organizes the list for quotes and estimates the fixing materials.
>
> For each size, choose the type, enter the quantity, the opening width and height, and tap "Add to list". Identical items are added together. The material is only for the quote.
>
> Optional fields come with default values. Change them only if you want to.

- O que já valia na rodada 1 continua valendo:

- Esquadrias é a última aba do app. Botões: Limpar, Anterior (volta pra Pintura) e Finalizar. **Não tem Próximo nem Avançar.**
- Limpar: lista vazia, Tipo Porta, Material Não informado e os 3 insumos em Não.
- Depois de Adicionar à lista, os campos de quantidade, largura e altura ficam vazios para a próxima.
- Cada item da lista tem um X à direita, sem cortar o texto (teste com "3x Porta 80 x 210 cm (Vidro temperado)").
- O "?" explica como usar a lista (tipo, quantidade, medidas, Adicionar), que itens iguais são somados e que o material é só para a cotação. Termina com a nota dos valores padrão.
- Menus: Tipo (Porta, Janela) e Material (Não informado, Alumínio, Madeira, Vidro temperado).

---

Quando terminar cada aba, me manda "ok" ou os prints. 😉
