# Testes da Rodada 1 (Brasil, português): Brocas até Esquadrias

Os resultados foram tirados rodando as contas do código, com os preços iniciais do app (cimento R$ 36, cal R$ 18, areia R$ 110, brita R$ 120).

**Atualizado em 04/11/2026, no fim das correções de visual da rodada 1.** Os resultados já são os do código com todas as correções (modo claro, ponto de milhar, texto da perda "(com X% de perda)", arredondamento, plural, linhas com zero, janela "Confira os valores" em todas as abas, detalhes de cada aba e quebra de linha). Nenhuma conta mudou nas correções: só o jeito de escrever.

**Mudado em 05/11/2026 (parte 3 das correções da rodada 2, pendências 3, 12 e 17): mensagem do Baldrame com o campo ("Comprimento, largura e altura devem ser maiores que zero."), "Caixas: 21 (2,16 m² por caixa)" no Piso e no Azulejo, e linha em branco entre o custo e a frase da Esquadrias.** Nenhuma conta mudou.

O resultado completo de cada caso, linha por linha, fica dentro do testes_manuais/rodada1.py, que compara com o app e diz OK ou DIFERENTE. Aqui ficam o roteiro (o que digitar) e o resumo do que conferir.

Dica: dê **Limpar** antes de cada teste, para não sobrar valor do teste anterior.

---

# BROCAS

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

Custo Estimado da Etapa: R$ 2.844,20
```

Pra entender: a gaiola vai até a metade da broca (3,5 ÷ 2 = 1,75 m). O estribo é uma espiral dentro do cobrimento de 3 cm (diâmetro de dentro: 25 − 2 × 3 = 19 cm). O arame mostra "1,4 kg", mas a conta usa 1,44 kg. Por isso dá R$ 21,60, e não R$ 21,00. Não é erro.

### Teste B: só os obrigatórios

Quantidade 10, Diâmetro 20, Profundidade 3. O resto fica como vem (perda 10, espaçamento 20, barras e mão de obra vazios).

```
Traço: 1:2:3
Volume Total (com 10% de perda): 1,037 m³
• Cimento: 8 sacos de 50 kg (R$ 288,00)
• Areia: 0,52 m³ (R$ 57,20)
• Brita: 0,78 m³ (R$ 93,60)

Custo Estimado da Etapa: R$ 438,80
```

**B2:** igual ao B, só acrescente 4 barras (confere o espaçamento padrão de 20):

```
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

Custo Estimado da Etapa: R$ 756,16
```

### Teste C: erros de digitação

Base: Quantidade 10, Diâmetro 20, Profundidade 3. Mude só o indicado.

| # | O que mudar | Esperado na tela |
|---|---|---|
| C1 | Quantidade vazia | Por favor, digite números válidos nos campos! |
| C2 | Quantidade = dez | (mesma mensagem) |
| C3 | Quantidade = 0 | Erro: Quantidade, profundidade e diâmetro devem ser maiores que zero. |
| C4 | Profundidade = -3 | (mesma do C3) |
| C5 | Quantidade = 2,5 | Por favor, digite números válidos nos campos! (quantidade é número inteiro) |
| C6, C7, C8 | Profundidade = 2,5, depois 2.5, depois 2 1/2 (com espaço) | Os três: Volume 0,864 m³, 7 sacos, Areia 0,43 m³, Brita 0,65 m³, R$ 377,30 |
| C9 | Perda = -5 | Erro: A perda não pode ser negativa. |
| C10 | Perda = 2,5 | "Volume Total (com 2,5% de perda): 0,966 m³", 8 sacos, R$ 427,20 |
| C11 | Diâmetro = 4 + 4 barras | Erro: Diâmetro muito pequeno para colocar estribos. |
| C12 | Barras = -4 | Erro: Barras e espaçamento dos estribos não podem ser negativos. |
| C13 | Mão de obra = trinta | Por favor, digite números válidos nos campos! |
| C14 | Profundidade = 300 | Janela "Confira os valores": "Profundidade de 300 m: o limite é 30 m." Cancelar não calcula; Continuar → 103,673 m³, 778 sacos, R$ 43.040,40 |
| C15 | 4 barras + espaçamento vazio | Sem a linha de Estribos; Aço 26,1 kg (R$ 247,66); Arame 0,5 kg (R$ 7,80); R$ 694,26 |
| C16 | 4 barras + espaçamento 12,5 | "Estribos 5 mm c/ 12,5 cm: 9,5 kg (6 barras de 12 m)"; Aço 35,5 kg; R$ 786,99 |
| C17 | Profundidade = 30 | Calcula sem janela (30 m ainda vale): 10,367 m³, 78 sacos, R$ 4.311,40 |
| C18 | Profundidade = 1-21/2 | Por favor, digite números válidos nos campos! |

### Visual (Brocas)

- Botões: Limpar, Próximo e Finalizar. Sem Anterior, porque é a primeira aba.
- Limpar: pergunta antes de apagar e volta perda 10, espaçamento 20, traço 1:2:3 e bitola 8 mm.
- O "?" fala de brocas, explica que os estribos só entram com barras e termina com a nota dos valores padrão.
- Dicas dos campos inteiras; títulos "Traço do concreto" e "Bitola do ferro (mm)" perto do campo de cima e do botão, iguais ao "Armadura / Ferragem".
- Menus abrem alinhados no botão, sem sair da janela; o traço aparece com vírgula quando tiver decimal ("1,5:5:5").
- Tudo legível no tema claro e no escuro.

---

# BALDRAME

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

Custo Estimado da Etapa: R$ 4.787,14
```

Pra entender: 30 m de viga = 2 emendas em cada barra (a cada 12 m); 6 barras × 2 emendas × 50 cm (40 × 12,5 mm) = 6 m de emendas. O estribo fica dentro do cobrimento de 3 cm (20 × 40 vira 14 × 34 por dentro). O impermeabilizante custa sobre os litros comprados (18 + 3,6 + 3,6 = 25,2 L × R$ 15,50), não sobre os 24 L usados.

### Teste B: só os obrigatórios

Comprimento 12,5, Largura 20, Altura 30. O resto como vem (perda 5, espaçamento 20, traço 1:2:3, impermeabilização Não).

```
Traço: 1:2:3
Volume Total (com 5% de perda): 0,788 m³
• Cimento: 6 sacos de 50 kg (R$ 216,00)
• Areia: 0,39 m³ (R$ 42,90)
• Brita: 0,59 m³ (R$ 70,80)

Custo Estimado da Etapa: R$ 329,70
```

**B2:** igual ao B + 4 barras (bitola 8 mm e espaçamento 20, que já vêm):

```
Traço: 1:2:3
Volume Total (com 5% de perda): 0,788 m³
• Cimento: 6 sacos de 50 kg (R$ 216,00)
• Areia: 0,39 m³ (R$ 42,90)
• Brita: 0,59 m³ (R$ 70,80)
• Ferro 8 mm: 22,3 kg (5 barras de 12 m) (inclui 1,28 m de emendas)
• Estribos 5 mm c/ 20 cm: 8,6 kg (5 barras de 12 m)
• Aço/Ferragem: 30,9 kg (R$ 293,74)
• Arame recozido: 0,6 kg (R$ 9,30)

Custo Estimado da Etapa: R$ 632,74
```

**B3:** igual ao B (sem barras) + Impermeabilização: Sim:

```
Traço: 1:2:3
Volume Total (com 5% de perda): 0,788 m³
• Cimento: 6 sacos de 50 kg (R$ 216,00)
• Areia: 0,39 m³ (R$ 42,90)
• Brita: 0,59 m³ (R$ 70,80)
• Impermeabilizante: 10,0 m² · 8,0 L = 3 galões de 3,6 L (R$ 167,40)

Custo Estimado da Etapa: R$ 497,10
```

### Teste C: erros de digitação

Base: Comprimento 12,5, Largura 20, Altura 30. Dê Limpar antes de cada um e mude só o indicado.

| # | O que mudar | Esperado na tela |
|---|---|---|
| C1 | Comprimento vazio | Por favor, digite números válidos nos campos! |
| C2 | Largura = vinte | (mesma mensagem) |
| C3 | Altura = 0 | Erro: Comprimento, largura e altura devem ser maiores que zero. |
| C4 | Comprimento = -5 | (mesma do C3) |
| C5, C6 | Comprimento = 12.5, depois 12 1/2 (com espaço) | Iguais ao Teste B: 0,788 m³, 6 sacos, R$ 329,70 |
| C7 | Perda = -2 | Erro: A perda não pode ser negativa. |
| C8 | Perda = 2,5 | "Volume Total (com 2,5% de perda): 0,769 m³", 6 sacos, Areia 0,38, Brita 0,58, R$ 327,40 |
| C9 | Largura = 4 + 4 barras | Janela "Confira os valores": "Viga de 4 cm x 30 cm: o mínimo é 20 cm de largura e 30 cm de altura." Continuar → Erro: Viga muito pequena para colocar estribos. |
| C10 | Barras = -4 | Erro: Barras e espaçamento dos estribos não podem ser negativos. |
| C11 | Barras = 4,5 | Por favor, digite números válidos nos campos! |
| C12 | Mão de obra = quarenta | (mesma mensagem) |
| C13 | 4 barras + espaçamento 12,5 | "Estribos 5 mm c/ 12,5 cm: 13,9 kg (8 barras de 12 m)"; Aço 36,1 kg; Arame 0,7 kg; R$ 683,83 |
| C14 | Comprimento = 12 + 4 barras | Ferro 20,9 kg (5 barras), sem "inclui ... emendas"; R$ 612,59 |
| C15 | Comprimento = 24 + 4 barras | "Ferro 8 mm: 42,3 kg (9 barras de 12 m) (inclui 1,28 m de emendas)"; R$ 1.228,16 |
| C16 | 4 barras + espaçamento vazio | Sem a linha de Estribos; Aço 22,3 kg; Arame 0,5 kg; R$ 548,11 |
| C17 | Comprimento = 5000 | Calcula sem janela (comprimento não tem máximo): 315,000 m³, 2.363 sacos, R$ 130.743,00 |
| C18 | Largura = 0,2 e Altura = 0,3 | Janela: "Viga de 0,2 cm x 0,3 cm: o mínimo é 20 cm de largura e 30 cm de altura." Continuar → 0,000 m³, "• Cimento: 1 saco de 50 kg (R$ 36,00)" (areia e brita dão zero e não aparecem), R$ 36,00 |
| C19 | Largura = 19 | Janela: "Viga de 19 cm x 30 cm: ..." Continuar → 0,748 m³, 6 sacos, R$ 323,90 |
| C20 | Altura = 29,5 | Janela: "Viga de 20 cm x 29,5 cm: ..." Continuar → 0,774 m³, 6 sacos, R$ 328,50 |
| C21 | Comprimento = 1-21/2 | Por favor, digite números válidos nos campos! |
| C22 | Comprimento = 2 1/2 | 0,158 m³, 2 sacos, Areia 0,08, Brita 0,12, R$ 95,20 |

**Limites com aviso** (janela "Confira os valores", com Cancelar e Continuar): viga com largura menor que 20 cm ou altura menor que 30 cm (confirmado pelo engenheiro). O comprimento não tem máximo.

### Visual (Baldrame)

- Botões: Limpar, Anterior, Próximo e Finalizar. O Anterior volta pra Brocas.
- Limpar: volta perda 5, espaçamento 20, traço 1:2:3, bitola 8 mm e impermeabilização Não.
- O "?" fala das vigas e termina com a nota dos valores padrão.
- Títulos dos menus (traço, bitola, impermeabilização) perto do campo de cima e do botão; menus alinhados no botão.
- No Teste A, a linha do ferro quebra em 2 linhas e continua legível.

---

# PAREDES

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
Área bruta: 80,00 m²
Vãos (portas e janelas): 12,50 m²
Área líquida: 67,50 m²
Traço: 1:0,5:6
• Bloco de concreto (14x19x39): 1.162 un (1,16 milheiro) (R$ 5.229,00)
• Cimento: 8 sacos de 50 kg (R$ 288,00)
• Cal: 7 sacos de 20 kg (R$ 126,00)
• Areia: 1,84 m³ (R$ 202,40)

Custo Estimado da Etapa: R$ 5.845,40
```

### Teste B: só os obrigatórios

Área 30. O resto como vem (tijolo baiano, em pé, junta 1, quebra 5, traço 1:2:8).

```
Área bruta: 30,00 m²
Traço: 1:2:8
• Tijolo baiano (9x19x19): 788 un (0,79 milheiro) (R$ 945,60)
• Cimento: 1 saco de 50 kg (R$ 36,00)
• Cal: 3 sacos de 20 kg (R$ 54,00)
• Areia: 0,26 m³ (R$ 28,60)

Custo Estimado da Etapa: R$ 1.064,20
```

Pra conferir o resto, use o Teste B (área 30) e mude só o indicado:

| # | Mudar | O que muda no resultado | Custo |
|---|---|---|---|
| B2 | Bloco de concreto (19x19x39) | 394 un (0,39 milheiro); 2 sacos de cimento; 5 de cal; Areia 0,42 m³ | R$ 2.572,20 |
| B3 | Tijolo baiano 9 furos (9x14x19) + Deitado | 1.575 un (1,58 milheiro), R$ 1.575,00; 2 de cimento; 7 de cal; Areia 0,61 m³ | R$ 1.840,10 |
| B4 | Traço 1:0:3 | 788 un; 3 sacos de cimento; a linha da Cal não aparece; Areia 0,27 m³ | R$ 1.083,30 |

### Teste C: erros de digitação

Base: Área 30. Dê Limpar antes de cada um e mude só o indicado.

| # | O que mudar | Esperado na tela |
|---|---|---|
| C1 | Área vazia | Por favor, digite números válidos nos campos! |
| C2 | Área = trinta | (mesma mensagem) |
| C3 | Área = 0 | Erro: A área da parede deve ser maior que zero. |
| C4 | Área = -30 | (mesma do C3) |
| C5, C6, C7 | Área = 30,5, depois 30.5, depois 30 1/2 (com espaço) | Os três: 801 un (0,80 milheiro), 1 saco de cimento, 3 de cal, 0,27 m³, R$ 1.080,90 |
| C8 | Portas e janelas = 35 | Erro: O desconto de portas e janelas não pode ser maior que a área da parede. |
| C9 | Portas e janelas = 30 | (mesma do C8) |
| C10 | Portas e janelas = -5 | Erro: Desconto, junta e quebra não podem ser negativos. |
| C11 | Quebra = -5 | (mesma do C10) |
| C12 | Junta vazia, e depois Quebra vazia | Os dois iguais ao Teste B (usa o padrão: 1 cm e 5%) |
| C13 | Quebra = 2,5 | 769 un (0,77 milheiro), R$ 1.041,40 |
| C14 | Junta = 0 | Janela "Confira os valores": "Junta de 0 cm: o normal é de 0,5 cm a 3 cm." Continuar → só a linha dos tijolos (873 un), R$ 1.047,60 |
| C15 | Junta = 10 | Janela: "Junta de 10 cm: o normal é de 0,5 cm a 3 cm." Continuar → 375 un, Cimento 5, Cal 17, Areia 1,54 m³, R$ 1.105,40 |
| C16 | Área = 100000 | Janela: "Área de 100.000 m²: o limite é 2.000 m²." Cancelar não calcula; Continuar → 2.625.000 un (2.625,00 milheiros), R$ 3.515.067,00 |
| C17 | Quebra = 25 | Janela: "Quebra de 25%: o limite é 20%." Continuar → 938 un (0,94 milheiro), R$ 1.244,20 |

**Limites com aviso** (janela "Confira os valores", com Cancelar e Continuar): área até 2.000 m², junta de 0,5 a 3 cm e quebra até 20%.

### Visual (Paredes)

- Botões: Limpar, Anterior (volta pro Baldrame), Próximo (vai pra Laje) e Finalizar.
- Limpar: volta tijolo baiano, em pé, junta 1, quebra 5 e traço 1:2:8.
- O "?" fala da área bruta, do tijolo e do desconto de portas e janelas.
- Menu do tijolo: os 5 nomes inteiros, alinhado no botão, sem sair da janela.
- Menu do traço com vírgula: 1:2:8, 1:0,5:6, 1,5:1:8, 1:0:3, 1,5:0:4.
- Títulos "Tipo e tamanho do tijolo ou bloco" e "Traço da massa (cimento:cal:areia) (Opcional)" perto do campo de cima e do botão.

---

# LAJE

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

Custo Estimado da Etapa: R$ 5.486,50
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
Área: 30,00 m²
Tipo de laje: Maciça
Espessura: 10 cm
Traço: 1,5:5:5
Volume Total (com 7% de perda): 3,210 m³
• Cimento: 19 sacos de 50 kg (R$ 684,00)
• Areia: 2,09 m³ (R$ 229,90)
• Brita: 2,09 m³ (R$ 250,80)

Custo Estimado da Etapa: R$ 1.164,70
```

### Teste B: pré-moldada, só os obrigatórios

Área 50. O resto como vem (pré-moldada, isopor, capa 4, tela Não, traço 1:2:3, perda 5).

```
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

Custo Estimado da Etapa: R$ 4.902,70
```

**B2:** maciça, só os obrigatórios. Área 30, Tipo Maciça, Espessura 10:

```
Área: 30,00 m²
Tipo de laje: Maciça
Espessura: 10 cm
Traço: 1:2:3
Volume Total (com 5% de perda): 3,150 m³
• Cimento: 24 sacos de 50 kg (R$ 864,00)
• Areia: 1,58 m³ (R$ 173,80)
• Brita: 2,36 m³ (R$ 283,20)

Custo Estimado da Etapa: R$ 1.321,00
```

Pra conferir o resto, use o Teste B (área 50) e mude só o indicado:

| # | Mudar | O que muda no resultado | Custo |
|---|---|---|---|
| B3 | Tela soldada: Sim | Aparece "• Tela soldada: 55,00 m² = 10 painéis de 2 x 3 m (R$ 950,00)" | R$ 5.852,70 |
| B4 | Enchimento: Lajota cerâmica | Enchimento: Lajota cerâmica; laje a R$ 3.250,00; aparece "(Lajotas cerâmicas: 630 un)" | R$ 4.402,70 |

### Teste C: erros de digitação

Base: pré-moldada, Área 50. Mude só o indicado.

| # | O que mudar | Esperado na tela |
|---|---|---|
| C1 | Área vazia | Por favor, digite números válidos nos campos! |
| C2 | Área = cinquenta | (mesma mensagem) |
| C3 | Área = 0 | Erro: A área deve ser maior que zero. |
| C4 | Área = -50 | (mesma do C3) |
| C5, C6, C7 | Área = 50,5, depois 50.5, depois 50 1/2 (com espaço) | Os três: 2,757 m³, 21 sacos, Areia 1,38 m³, Brita 2,07 m³, laje R$ 3.787,50, Custo R$ 4.943,70 |
| C8 | Perda = -5 | Erro: A perda não pode ser negativa. |
| C9 | Perda = 2,5 | "Volume Total (com 2,5% de perda): 2,665 m³", 20 sacos, R$ 4.856,30 |
| C10 | Capa = 0 | Erro: A espessura da capa deve ser maior que zero. |
| C11 | Capa vazia | Igual ao Teste B (usa o padrão de 4 cm) |
| C12 | Capa = -4 | (mesma do C10) |
| C13 | Maciça + Espessura vazia | Por favor, digite números válidos nos campos! |
| C14 | Maciça + Espessura = 0 | Erro: Informe a espessura total da laje maciça. |
| C15 | Maciça + Espessura = dez | Por favor, digite números válidos nos campos! |
| C16 | Área = 1-21/2 | Por favor, digite números válidos nos campos! |
| C17 | Área = 5 + Tela Sim | "Tela soldada: 5,50 m² = 1 painel de 2 x 3 m (R$ 95,00)" (no singular), R$ 617,40 |
| C18 | Capa = 4,5 | "Capa de concreto: 4,5 cm", 2,992 m³, 23 sacos, R$ 5.011,80 |
| C19 | Área = 100000 | Janela: "Área de 100.000 m²: o limite é 2.000 m²." Continuar → 5.460,000 m³, 40.950 sacos, R$ 9.765.900,00 |
| C20 | Capa = 50 | Janela: "Capa de 50 cm: o normal é de 3 cm a 8 cm." Continuar → 26,880 m³, 202 sacos, R$ 14.919,60 |
| C21 | Maciça + Espessura = 200 | Janela: "Espessura de 200 cm: o normal é de 8 cm a 20 cm." Continuar → 105,000 m³, 788 sacos, R$ 43.593,00 |

Troca de tipo (sem perder dados):

C22: preencha o Teste A (pré-moldada) e troque para Maciça. Aparece o campo "Espessura total" e somem o enchimento, a capa e a tela. Volte para Pré-moldada: a capa 5 e a área 50 continuam lá, e o resultado antigo some (porque era do outro tipo).

**Limites com aviso** (janela "Confira os valores", com Cancelar e Continuar): área até 2.000 m², capa de 3 a 8 cm (só na pré-moldada) e espessura da maciça de 8 a 20 cm (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Laje)

- Botões: Limpar, Anterior, Próximo e Finalizar. O Anterior volta pra Paredes e o Próximo vai pro Telhado.
- Limpar: volta pré-moldada, isopor, capa 4, tela Não, traço 1:2:3 e perda 5.
- O "?" fala dos dois tipos de laje e da tela soldada (painéis de 2 x 3 m com 10% a mais), e termina com a nota dos valores padrão.
- Menus (tipo de laje, enchimento, tela, traço) alinhados no botão, com os títulos perto do campo de cima.
- Menu do traço com vírgula: 1:2:3, 1:3:3, 1:4:3, 1,5:5:5.
- Na maciça, não aparece a opção de tela soldada.

---

# TELHADO

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

Custo Estimado da Etapa: R$ 8.437,20
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
Área em planta: 60,00 m²
Inclinação: 15%
Área do telhado: 60,67 m²
Tipo de telha: Fibrocimento
• Telhas (com 5% de perda): 27 un (R$ 2.025,00)
• Cumeeira: 8,00 m = 9 peças (R$ 405,00)
• Madeiramento (estimativa):
   - Terças: 51,0 m (R$ 1.275,00)

Custo Estimado da Etapa: R$ 3.705,00
```

No fibrocimento só aparecem as terças (a telha vai direto nelas, sem ripas e caibros).

### Teste B: só os obrigatórios

Área 80. O resto como vem (cerâmica, inclinação 30, cumeeira vazia, madeiramento Não, perda 5).

```
Área em planta: 80,00 m²
Inclinação: 30%
Área do telhado: 83,52 m²
Tipo de telha: Cerâmica
• Telhas (com 5% de perda): 1.404 un (R$ 3.510,00)

Custo Estimado da Etapa: R$ 3.510,00
```

Pra conferir o resto, use o Teste B (área 80) e mude só o indicado:

| # | Mudar | O que muda no resultado | Custo |
|---|---|---|---|
| B2 | Cumeeira: 10 | Aparece "• Cumeeira: 10,00 m = 32 peças (R$ 128,00)" | R$ 3.638,00 |
| B3 | Madeiramento: Sim | Aparecem Ripas 263,1 m (R$ 789,30), Caibros 175,4 m (R$ 1.578,60), Terças 52,6 m (R$ 1.315,00) | R$ 7.192,90 |
| B4 | Tipo: Fibrocimento | A inclinação muda sozinha para 15; Área do telhado 80,89 m²; 36 telhas (R$ 2.700,00) | R$ 2.700,00 |
| B5 | Tipo: Concreto | A inclinação continua 30; 921 telhas (R$ 4.144,50) | R$ 4.144,50 |

### Teste C: erros de digitação

Base: Teste B (área 80). Mude só o indicado.

| # | O que mudar | Esperado na tela |
|---|---|---|
| C1 | Área vazia | Por favor, digite números válidos nos campos! |
| C2 | Área = oitenta | (mesma mensagem) |
| C3 | Área = 0 | Erro: A área deve ser maior que zero. |
| C4 | Área = -80 | (mesma do C3) |
| C5, C6, C7 | Área = 80,5, depois 80.5, depois 80 1/2 (com espaço) | Os três: Área em planta 80,50 m², Área do telhado 84,04 m², 1.412 telhas, R$ 3.530,00 |
| C8 | Perda = -5 | Erro: Os valores não podem ser negativos. |
| C9 | Perda = 2,5 | "Telhas (com 2,5% de perda): 1.370 un", R$ 3.425,00 |
| C10 | Inclinação = -30 | (mesma do C8) |
| C11 | Inclinação vazia | Igual ao Teste B (usa o padrão de 30%) |
| C12 | Inclinação = 0 | "Inclinação: 0%", Área do telhado 80,00 m², 1.344 telhas, R$ 3.360,00 |
| C13 | Inclinação = 2,5 | "Inclinação: 2,5%", Área do telhado 80,02 m², 1.345 telhas, R$ 3.362,50 |
| C14 | Cumeeira = -10 | (mesma do C8) |
| C15 | Cumeeira = 0 | Igual ao Teste B (a linha da cumeeira não aparece) |
| C16 | Cumeeira = dez | Por favor, digite números válidos nos campos! |
| C17 | Área = 1-21/2 | Por favor, digite números válidos nos campos! |
| C18 | Cumeeira = 0,3 | "• Cumeeira: 0,30 m = 1 peça (R$ 4,00)", R$ 3.514,00 |
| C19 | Área = 100000 | Janela: "Área de 100.000 m²: o limite é 2.000 m²." Continuar → Área do telhado 104.403,07 m², 1.753.972 telhas, R$ 4.384.930,00 |
| C20 | Inclinação = 300 | Janela: "Inclinação de 300%: o limite é 100%." Continuar → Área do telhado 252,98 m², 4.251 telhas, R$ 10.627,50 |

Troca de tipo (a inclinação acompanha):

C21: com a inclinação ainda em 30 (sem mexer), troque para Fibrocimento: ela vira 15. Volte para Cerâmica: vira 30 de novo.

C22: digite inclinação 35 e troque para Fibrocimento: continua 35 (você mexeu, então o app não troca). Resultado: 38 telhas, R$ 2.850,00.

**Limites com aviso** (janela "Confira os valores", com Cancelar e Continuar): área até 2.000 m² e inclinação até 100% (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Telhado)

- Telhado é a última aba da Estrutura. Botões: Limpar e Anterior (volta pra Laje) numa linha; embaixo, "Avançar para a próxima etapa" (vai pra Elétrica) e Finalizar. **Não tem Próximo.**
- Limpar: volta cerâmica, inclinação 30, cumeeira vazia, madeiramento Não e perda 5.
- O "?" fala da área em planta (vista de cima, com os beirais), que o app corrige pela inclinação, e explica a cumeeira (no telhado de quatro águas, somar as quinas; telhado de uma água não tem). Termina com a nota dos valores padrão.
- Menus (tipo de telha, madeiramento) alinhados no botão, com os títulos perto do campo de cima.
- Menu do tipo de telha: Cerâmica, Concreto, Fibrocimento.

---

# ELÉTRICA

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

Custo Estimado da Etapa: R$ 2.885,00
```

Pra entender: como tudo veio do projeto, o app só soma os 5% de perda (150 m → 157,5 m → 4 rolos de 50 m). Os chuveiros só aparecem no topo, porque o fio e o conduíte já vieram do projeto. As caixinhas são uma por tomada ou interruptor (20 + 10 = 30) e as octogonais, uma por ponto de luz (12).

### Teste B: só os obrigatórios (o app estima)

Tomadas 20, Interruptores 10, Pontos de luz 12. O resto como vem (os dois campos de chuveiro e as metragens vazios, perda 10).

```
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

Custo Estimado da Etapa: R$ 2.300,00
```

Pra entender: são 42 pontos × 5 m = 210 m de conduíte, com 10% = 231 m. Fio 1,5: (10 interruptores + 12 luzes) × 10 m = 220, com 10% = 242 m. Fio 2,5: 20 tomadas × 15 m = 300, com 10% = 330 m.

Pra conferir o resto, use o Teste B e mude só o indicado:

| # | Mudar | O que muda no resultado | Custo |
|---|---|---|---|
| B2 | Chuveiros acima de 5.500 W: 2 | Aparece "Chuveiros acima de 5.500 W: 2"; conduíte 253,0 m = 6 rolos (R$ 450,00); aparece "• Fio 6 mm² (estimado, com 10% de perda): 66,0 m = 1 rolo de 100 m (R$ 530,00)" | R$ 2.905,00 |
| B3 | Chuveiros até 5.500 W: 2 | Aparece "Chuveiros até 5.500 W: 2"; conduíte 253,0 m = 6 rolos (R$ 450,00); aparece "• Fio 4 mm² (estimado, com 10% de perda): 66,0 m = 1 rolo de 100 m (R$ 360,00)" | R$ 2.735,00 |
| B4 | Um de cada: acima 1 e até 5.500 W 1 | As duas linhas de chuveiro; conduíte 253,0 m = 6 rolos; Fio 4 mm² 33,0 m = 1 rolo (R$ 360,00) e Fio 6 mm² 33,0 m = 1 rolo (R$ 530,00) | R$ 3.265,00 |
| B5 | Conduíte: 150 | "Conduíte (do projeto, com 10% de perda): 165,0 m = 4 rolos de 50 m (R$ 300,00)" | R$ 2.225,00 |
| B6 | Fio 2,5 mm²: 250 | "Fio 2,5 mm² (do projeto, com 10% de perda): 275,0 m = 3 rolos de 100 m (R$ 690,00)"; os outros continuam "(estimado)" | R$ 2.070,00 |
| B7 | Limpar e digitar só Chuveiros acima de 5.500 W: 1 | Tomadas 0, Interruptores 0, Pontos de luz 0; conduíte 11,0 m = 1 rolo de 50 m (R$ 75,00); Fio 6 mm² 33,0 m = 1 rolo de 100 m (R$ 530,00) | R$ 605,00 |
| B8 | Limpar e digitar só Chuveiros até 5.500 W: 1 | conduíte 11,0 m = 1 rolo (R$ 75,00); Fio 4 mm² 33,0 m = 1 rolo de 100 m (R$ 360,00) | R$ 435,00 |
| B9 | Limpar e digitar só Tomadas: 1 | conduíte 5,5 m = 1 rolo; Fio 2,5 mm² 16,5 m = 1 rolo; Caixinhas 1 un; Tomadas 1 un | R$ 322,50 |

Pra entender o chuveiro: cada um leva 10 m de conduíte e 30 m de fio (3 fios de 10 m), com 10% = 11 m e 33 m. O de até 5.500 W usa fio de 4 mm²; o mais forte, de 6 mm².

### Teste C: erros de digitação

Base: Teste B. Mude só o indicado.

| # | O que mudar | Esperado na tela |
|---|---|---|
| C1 | Tomadas, interruptores e luzes vazios | Erro: Informe pelo menos uma tomada, interruptor, ponto de luz ou chuveiro. |
| C2 | Os três = 0 | (mesma do C1) |
| C3 | Tomadas = vinte | Por favor, digite números válidos nos campos! |
| C4 | Tomadas = -5 | Erro: As quantidades não podem ser negativas. |
| C5 | Tomadas = 2,5 | Por favor, digite números válidos nos campos! (quantidade é número inteiro) |
| C5b | Chuveiros até 5.500 W = -1 | (mesma do C4) |
| C5c | Chuveiros até 5.500 W = 1,5 | (mesma do C5) |
| C6 | Perda = -5 | Erro: Os valores não podem ser negativos. |
| C7 | Perda = 2,5 | "(estimado, com 2,5% de perda)", conduíte 215,3 m, R$ 2.300,00 |
| C8 | Conduíte = -10 | (mesma do C6) |
| C9 | Conduíte = 0 | A linha do conduíte some, R$ 1.925,00 |
| C10, C11, C12 | Conduíte = 150,5, depois 150.5, depois 150 1/2 | Os três: "Conduíte (do projeto, com 10% de perda): 165,6 m = 4 rolos de 50 m", R$ 2.225,00 |
| C13 | Fio 1,5 mm² = abc | Por favor, digite números válidos nos campos! |
| C14 | Fio 1,5 mm² = 1-21/2 | (mesma do C13) |
| C15 | Chuveiros acima de 5.500 W: 2 + Fio 6 mm² = 0 | A linha do Fio 6 mm² some (o projeto disse 0), R$ 2.375,00 |
| C15b | Chuveiros até 5.500 W: 2 + Fio 4 mm² = 0 | A linha do Fio 4 mm² some, R$ 2.375,00 |
| C16 | Tomadas = 2000 | Janela: "2.000 tomadas: o limite é 300." Continuar → Conduíte 11.121,0 m = 223 rolos, Fio 2,5 mm² 33.000,0 m = 330 rolos, R$ 128.280,00 |
| C17 | Chuveiros acima de 5.500 W = 50 | Janela: "50 chuveiros: o limite é 10 (somando os dois campos)." Continuar → Fio 6 mm² 1.650,0 m = 17 rolos, R$ 12.135,00 |

**Limites com aviso** (janela "Confira os valores", com Cancelar e Continuar): até 300 tomadas, 300 interruptores, 300 pontos de luz e 10 chuveiros (somando os dois campos) (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Elétrica)

- Botões: Limpar, Anterior (volta pro Telhado), Próximo (vai pra Hidráulica) e Finalizar.
- Limpar: tudo vazio e perda 10.
- O "?" explica o que o app estima, que cada chuveiro tem um circuito só dele (fio de 6 mm² acima de 5.500 W e de 4 mm² até 5.500 W, com a potência na caixa do chuveiro) e que metragem vazia é estimada. Termina com a nota dos valores padrão.
- Os dois campos de chuveiro aparecem um embaixo do outro: "Chuveiros acima de 5.500 W (ex: 2)" e "Chuveiros até 5.500 W (ex: 1)", sem cortar a dica.
- Os títulos "Quantidades" e "Metragens do projeto (Opcional)" aparecem acima dos campos certos.
- Dicas dos fios sem cortar: "Fio 1,5 mm² em metros (opcional)" (e 2,5, 4 e 6).

---

# HIDRÁULICA

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

Custo Estimado da Etapa: R$ 1.707,00
```

Pra entender: a água quente vem em barras de 3 m (CPVC), por isso 21 m dá 7 barras; os outros tubos são barras de 6 m. As conexões são sempre estimadas: 4 por ponto de água e 3 por ponto de esgoto. Registros: 1 a cada 4 pontos de água (13 ÷ 4 = 3,25 → 4).

### Teste B: só os obrigatórios (o app estima)

Pontos de água fria 10, água quente 3, esgoto 8. O resto como vem (metragens vazias, perda 10).

```
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

Custo Estimado da Etapa: R$ 1.507,00
```

Pra entender: água fria 10 × 4 m = 40, com 10% = 44 m. Água quente 3 × 5 m = 15, com 10% = 16,5 m. Esgoto: 8 × 3 m = 24 → 26,4 m de 40 mm, e 8 × 2 m = 16 → 17,6 m de 100 mm.

Pra conferir o resto, use o Teste B e mude só o indicado:

| # | Mudar | O que muda no resultado | Custo |
|---|---|---|---|
| B2 | Limpar e digitar só água fria: 1 | "Tubo água fria ... 4,4 m = 1 barra de 6 m (R$ 30,00)" (no singular); Conexões de água fria 4 un; Registros 1 un | R$ 87,00 |
| B3 | Água fria 25 mm: 50 | "Tubo água fria PVC 25 mm (do projeto, com 10% de perda): 55,0 m = 10 barras de 6 m (R$ 300,00)" | R$ 1.567,00 |
| B4 | Limpar e digitar só esgoto: 8 | Só os dois tubos de esgoto e as conexões de esgoto; sem registro | R$ 589,00 |

### Teste C: erros de digitação

Base: Teste B. Mude só o indicado.

| # | O que mudar | Esperado na tela |
|---|---|---|
| C1 | Os três pontos vazios | Erro: Informe pelo menos um ponto de água fria, água quente ou esgoto. |
| C2 | Os três = 0 | (mesma do C1) |
| C3 | Água fria = dez | Por favor, digite números válidos nos campos! |
| C4 | Água fria = -10 | Erro: As quantidades não podem ser negativas. |
| C5 | Água fria = 2,5 | Por favor, digite números válidos nos campos! (ponto é número inteiro) |
| C6 | Perda = -5 | Erro: Os valores não podem ser negativos. |
| C7 | Perda = 2,5 | "(estimado, com 2,5% de perda)", água fria 41,0 m = 7 barras, R$ 1.477,00 |
| C8 | Água fria 25 mm = -10 | (mesma do C6) |
| C9 | Água fria 25 mm = 0 | A linha do tubo de água fria some (as conexões continuam), R$ 1.267,00 |
| C10, C11, C12 | Água fria 25 mm = 50,5, depois 50.5, depois 50 1/2 | Os três: "55,6 m = 10 barras de 6 m", R$ 1.567,00 |
| C13 | Água fria 25 mm = abc | Por favor, digite números válidos nos campos! |
| C14 | Água fria 25 mm = 1-21/2 | (mesma do C13) |
| C15 | Água fria = 1000 | Janela: "1.000 pontos de água fria: o limite é 200." Continuar → 4.400,0 m = 734 barras, 4.000 conexões, 251 registros, R$ 46.282,00 |

**Limites com aviso** (janela "Confira os valores", com Cancelar e Continuar): até 200 pontos de cada tipo (água fria, água quente e esgoto) (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Hidráulica)

- Hidráulica é a última aba das Instalações. Botões: Limpar e Anterior (volta pra Elétrica); embaixo, "Avançar para a próxima etapa" (vai pro Contrapiso) e Finalizar. **Não tem Próximo.**
- Limpar: tudo vazio e perda 10.
- O "?" explica o que é ponto (torneira, chuveiro, vaso, ralo, máquina) e que metragem vazia é estimada. Termina com a nota dos valores padrão.
- Repare nas dicas dos tubos: "Água fria 25 mm, em metros" não diz "(opcional)", diferente da Elétrica. Me fala se quer que eu acrescente.

---

# CONTRAPISO

### Teste A: todos os campos, opcionais trocados

| Campo | Digite / escolha |
|---|---|
| Área | 40 |
| Espessura média | 6 |
| Traço | 1:2:3 |
| Perda | 8 |

```
Área do contrapiso: 40,00 m²
Espessura média: 6 cm
Traço: 1:2:3
Volume Total (com 8% de perda): 2,592 m³
• Cimento: 20 sacos de 50 kg (R$ 720,00)
• Areia: 1,30 m³ (R$ 143,00)
• Brita: 1,94 m³ (R$ 232,80)

Custo Estimado da Etapa: R$ 1.095,80
```

Pra entender: 40 m² × 0,06 m = 2,4 m³, com 8% = 2,592 m³. No traço 1:2:3 são 7,5 sacos por m³: 2,592 × 7,5 = 19,44 → 20 sacos.

### Teste B: só os obrigatórios

Área 40, Espessura 5. O resto como vem (traço 1:3:3, perda 5).

```
Área do contrapiso: 40,00 m²
Espessura média: 5 cm
Traço: 1:3:3
Volume Total (com 5% de perda): 2,100 m³
• Cimento: 14 sacos de 50 kg (R$ 504,00)
• Areia: 1,35 m³ (R$ 148,50)
• Brita: 1,35 m³ (R$ 162,00)

Custo Estimado da Etapa: R$ 814,50
```

| # | Mudar | O que muda no resultado | Custo |
|---|---|---|---|
| B2 | Traço: 1,5:5:5 | "Traço: 1,5:5:5"; 13 sacos; Areia 1,37 m³; Brita 1,37 m³ | R$ 783,10 |

### Teste C: erros de digitação

Base: Teste B (área 40, espessura 5). Mude só o indicado.

| # | O que mudar | Esperado na tela |
|---|---|---|
| C1 | Área vazia | Por favor, digite números válidos nos campos! |
| C2 | Espessura vazia | (mesma mensagem) |
| C3 | Área = quarenta | (mesma mensagem) |
| C4 | Área = 0 | Erro: Área e espessura devem ser maiores que zero. |
| C5 | Área = -40 | (mesma do C4) |
| C6 | Espessura = 0 | (mesma do C4) |
| C7 | Espessura = -5 | (mesma do C4) |
| C8, C9, C10 | Área = 40,5, depois 40.5, depois 40 1/2 | Os três: Área 40,50 m², 2,126 m³, 14 sacos, Areia 1,37 m³, Brita 1,37 m³, R$ 819,10 |
| C11 | Espessura = 5,5 | 2,310 m³, 15 sacos, R$ 882,70 |
| C12 | Perda = -5 | Erro: A perda não pode ser negativa. |
| C13 | Perda = 2,5 | "Volume Total (com 2,5% de perda): 2,050 m³", R$ 807,60 |
| C14 | Perda vazia | Igual ao Teste B (usa o padrão de 5%) |
| C15 | Área = 1-21/2 | Por favor, digite números válidos nos campos! |
| C16 | Área = 100000 | Janela: "Área de 100.000 m²: o limite é 2.000 m²." Continuar → 5.250,000 m³, 33.750 sacos, R$ 1.991.250,00 |
| C17 | Espessura = 50 | Janela: "Espessura de 50 cm: o normal é de 3 cm a 10 cm." Continuar → 21,000 m³, 135 sacos, R$ 7.965,00 |
| C18 | Espessura = 0,5 | Janela: "Espessura de 0,5 cm: o normal é de 3 cm a 10 cm." Continuar → 0,210 m³, 2 sacos, R$ 104,20 |

**Limites com aviso** (janela "Confira os valores", com Cancelar e Continuar): área até 2.000 m² e espessura de 3 a 10 cm (o normal, segundo o engenheiro, é de 5 a 7 cm) (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Contrapiso)

- Botões: Limpar, Anterior (volta pra Hidráulica), Próximo (vai pro Reboco) e Finalizar.
- Limpar: área e espessura vazias, traço 1:3:3 e perda 5.
- O "?" fala da área dos cômodos e da espessura média. Termina com a nota dos valores padrão.
- Menu do traço com vírgula: 1:2:3, 1:3:3, 1:4:3, 1,5:5:5 (o 1:3:3 vem marcado).

---

# REBOCO

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

Custo Estimado da Etapa: R$ 578,60
```

Pra entender: 30 − 5 = 25 m², nos dois lados = 50 m². 50 × 0,025 m × 1,12 = 1,4 m³ de reboco. O chapisco (1:3, 0,5 cm) soma mais cimento e areia, mas não aparece como volume separado.

### Teste B: só os obrigatórios

Área 30. O resto como vem (espessura 2, traço 1:2:8, vãos vazio, perda 10, dois lados Não, chapisco Não).

```
Área bruta: 30,00 m²
Espessura: 2 cm
Traço: 1:2:8
Volume do Reboco (com 10% de perda): 0,660 m³
• Cimento: 2 sacos de 50 kg (R$ 72,00)
• Cal: 7 sacos de 20 kg (R$ 126,00)
• Areia: 0,60 m³ (R$ 66,00)

Custo Estimado da Etapa: R$ 264,00
```

Pra entender: 30 × 0,02 × 1,10 = 0,66 m³. No 1:2:8 (11 partes): cimento 0,66 ÷ 11 × 1500 = 90 kg → 2 sacos; cal 0,66 × 2 ÷ 11 × 1100 = 132 kg → 7 sacos; areia 0,66 × 8 ÷ 11 × 1,25 (inchamento) = 0,60 m³.

Pra conferir o resto, use o Teste B e mude só o indicado:

| # | Mudar | O que muda no resultado | Custo |
|---|---|---|---|
| B2 | Portas e janelas: 5 | Aparecem "Vãos (portas e janelas): 5,00 m²" e "Área líquida: 25,00 m²"; 0,550 m³; 2 sacos de cimento, 6 de cal, 0,50 m³ | R$ 235,00 |
| B3 | Dois lados: Sim | Aparece "Área a rebocar (dois lados): 60,00 m²"; 1,320 m³; 4 de cimento, 14 de cal, 1,20 m³ | R$ 528,00 |
| B4 | Chapisco: Sim | Aparece "Chapisco: incluído (1:3, 0,5 cm)"; 4 de cimento, 7 de cal, 0,75 m³ | R$ 352,50 |
| B5 | Traço: 1:0:3 | 5 sacos de cimento; Areia 0,62 m³; a linha da cal não aparece (deu zero) | R$ 248,20 |

### Teste C: erros de digitação

Base: Teste B (área 30). Mude só o indicado.

| # | O que mudar | Esperado na tela |
|---|---|---|
| C1 | Área vazia | Por favor, digite números válidos nos campos! |
| C2 | Espessura vazia (apague o 2) | (mesma mensagem) |
| C3 | Área = trinta | (mesma mensagem) |
| C4 | Área = 0 | Erro: Área e espessura devem ser maiores que zero. |
| C5 | Área = -30 | (mesma do C4) |
| C6 | Espessura = 0 | (mesma do C4) |
| C7, C8, C9 | Área = 30,5, depois 30.5, depois 30 1/2 | Os três: Área bruta 30,50 m², 0,671 m³, 2 de cimento, 7 de cal, Areia 0,61 m³, R$ 265,10 |
| C10 | Portas e janelas = -5 | Erro: Desconto e perda não podem ser negativos. |
| C11 | Portas e janelas = 30 | Erro: O desconto de portas e janelas não pode ser maior que a área da parede. |
| C12 | Portas e janelas = 40 | (mesma do C11) |
| C13 | Perda = -5 | (mesma do C10) |
| C14 | Perda = 2,5 | "Volume do Reboco (com 2,5% de perda): 0,615 m³", Areia 0,56 m³, R$ 259,60 |
| C15 | Área = 1-21/2 | Por favor, digite números válidos nos campos! |
| C16 | Portas e janelas = abc | (mesma do C15) |
| C17 | Área = 100000 | Janela: "Área de 100.000 m²: o limite é 2.000 m²." Continuar → 2.200,000 m³, 6.000 de cimento, 22.000 de cal, R$ 832.000,00 |
| C18 | Espessura = 20 | Janela: "Espessura de 20 cm: o normal é de 0,5 cm a 4 cm." Continuar → 6,600 m³, 19 de cimento, 67 de cal, R$ 2.550,00 |

**Limites com aviso** (janela "Confira os valores", com Cancelar e Continuar): área até 2.000 m² e espessura de 0,5 a 4 cm (o normal é 2 cm) (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Reboco)

- Botões: Limpar, Anterior (volta pro Contrapiso), Próximo (vai pro Piso) e Finalizar.
- Limpar: espessura 2, traço 1:2:8, vãos vazio, perda 10, dois lados Não e chapisco Não.
- O "?" fala da área, da espessura, do traço, dos dois lados e do chapisco. Termina com a nota dos valores padrão.
- Menus (traço, dois lados, chapisco) alinhados no botão, com os títulos perto do campo de cima.
- Menu do traço com vírgula: 1:2:8, 1:0,5:6, 1,5:1:8, 1:0:3, 1,5:0:4.

---

# PISO

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
Área: 40,00 m²
Área com perda (12%): 44,80 m²
Peça: 60x60 cm
Assentamento: com desenho
• Peças: 125
• Caixas: 21 (2,16 m² por caixa) (R$ 2.240,00)
• Argamassa colante AC-II: 12 sacos de 20 kg (224,0 kg) (R$ 360,00)
• Rodapé: 33,60 m (56 peças de 0,60 m) (R$ 504,00)

Custo Estimado da Etapa: R$ 3.104,00
```

Pra entender: como você digitou a perda (12), ela vale mesmo com desenho Sim (o 25% só entra com a perda vazia). 40 × 1,12 = 44,8 m² ÷ 0,36 m² por peça = 124,4 → 125 peças. Argamassa: a peça tem 60 cm (não passa de 60), então são 5 kg por m²: 44,8 × 5 = 224 kg ÷ 20 = 11,2 → 12 sacos. Rodapé: 30 × 1,12 = 33,6 m ÷ 0,6 = 56 peças.

### Teste B: só os obrigatórios

Área 40, Largura 60, Altura 60. O resto como vem (perda vazia, AC-I, desenho Não, caixa e rodapé vazios).

```
Área: 40,00 m²
Área com perda (10%, automática): 44,00 m²
Peça: 60x60 cm
• Peças: 123 (R$ 2.200,00)
• Argamassa colante AC-I: 11 sacos de 20 kg (220,0 kg) (R$ 242,00)

Custo Estimado da Etapa: R$ 2.442,00
```

Pra entender: 40 × 1,10 = 44 m² ÷ 0,36 m² por peça = 122,2 → 123 peças. Argamassa: 44 × 5 kg = 220 kg ÷ 20 = 11 sacos. Se a peça tiver um lado acima de 60 cm, são 8 kg por m² (dupla colagem).

Pra conferir o resto, use o Teste B e mude só o indicado:

| # | Mudar | O que muda no resultado | Custo |
|---|---|---|---|
| B2 | Peça 80 x 80 | "Área com perda (15%, automática): 46,00 m²"; 72 peças; 19 sacos (368,0 kg), porque passa de 60 cm (8 kg/m²) | R$ 2.718,00 |
| B3 | Peça 120 x 60 | "(20%, automática): 48,00 m²"; 67 peças; 20 sacos (384,0 kg) | R$ 2.840,00 |
| B4 | Desenho: Sim | "(25%, automática): 50,00 m²"; 139 peças; 13 sacos (250,0 kg) | R$ 2.786,00 |
| B5 | m² por caixa: 2,16 | "• Peças: 123" (sem preço) e "• Caixas: 21 (2,16 m² por caixa) (R$ 2.200,00)" | R$ 2.442,00 |
| B6 | Rodapé: 30 | Aparece "• Rodapé: 33,00 m (R$ 495,00)" | R$ 2.937,00 |
| B7 | Rodapé 30 + Peça do rodapé 0,6 | "• Rodapé: 33,00 m (55 peças de 0,60 m) (R$ 495,00)" | R$ 2.937,00 |
| B8 | Argamassa: AC-III | "Argamassa colante AC-III: 11 sacos ... (R$ 462,00)" | R$ 2.662,00 |

### Teste C: erros de digitação

Base: Teste B (área 40, peça 60 x 60). Mude só o indicado.

| # | O que mudar | Esperado na tela |
|---|---|---|
| C1 | Área vazia | Por favor, digite números válidos nos campos! |
| C2 | Largura vazia | (mesma mensagem) |
| C3 | Área = quarenta | (mesma mensagem) |
| C4 | Área = 0 | Erro: Área e tamanho da peça devem ser maiores que zero. |
| C5 | Área = -40 | (mesma do C4) |
| C6 | Largura = 0 | (mesma do C4) |
| C7, C8, C9 | Área = 40,5, depois 40.5, depois 40 1/2 | Os três: Área 40,50 m², 44,55 m², 124 peças, 12 sacos (222,8 kg), R$ 2.491,50 |
| C10 | Perda = -5 | Erro: A perda não pode ser negativa. |
| C11 | Perda = 2,5 | "Área com perda (2,5%): 41,00 m²" (sem "automática"), 114 peças, 11 sacos, R$ 2.292,00 |
| C12 | Perda = 0 | "Área com perda (0%): 40,00 m²", 112 peças, 10 sacos (200,0 kg), R$ 2.220,00 |
| C13 | m² por caixa = -2 | Erro: Os valores não podem ser negativos. |
| C14 | Rodapé = -10 | (mesma do C13) |
| C15 | Área = 1-21/2 | Por favor, digite números válidos nos campos! |
| C16 | Peça 70 x 70 | "(10%, automática)", 90 peças (70 ainda é 10% de perda), mas 18 sacos (352,0 kg), porque passa de 60 cm, R$ 2.596,00 |
| C17 | Peça 90 x 90 | "(15%, automática)", 57 peças (90 ainda é 15%), 19 sacos, R$ 2.718,00 |
| C18 | Largura = 60,5 | "Peça: 60,5x60 cm", 122 peças, 18 sacos (352,0 kg): é só passar de 60 que vira 8 kg/m², R$ 2.596,00 |
| C19 | Só a peça do rodapé (0,6), sem rodapé | Igual ao Teste B (sem linha de rodapé) |
| C20 | Área = 100000 | Janela: "Área de 100.000 m²: o limite é 2.000 m²." Continuar → 110.000,00 m², 305.556 peças, 27.500 sacos, R$ 6.105.000,00 |

Dica de botão: se o Contrapiso estiver preenchido (ex.: área 40), aparece no Piso o botão "Usar a área do Contrapiso: 40 m²". Toque nele: a área do Piso fica 40.

**Limites com aviso** (janela "Confira os valores", com Cancelar e Continuar): área até 2.000 m² e peça de 5 a 300 cm em cada lado (existe porcelanato de 120 x 240) (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Piso)

- Botões: Limpar, Anterior (volta pro Reboco), Próximo (vai pro Azulejo) e Finalizar.
- Limpar: perda vazia, AC-I, desenho Não, caixa e rodapé vazios.
- O "?" explica a argamassa (5 kg por m²; 8 kg por m² com um lado acima de 60 cm, dupla colagem), a perda automática (10% até 70 cm, 15% até 90 cm, 20% acima, 25% com desenho) e o tamanho da peça do rodapé. Termina com a nota dos valores padrão.
- Título comprido "Assentamento com desenho, diagonal ou paginado (Opcional)": se quebrar em 2 linhas, não pode invadir o campo de cima.
- Menu da argamassa: AC-I, AC-II, AC-III.

---

# AZULEJO

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
Área: 30,00 m²
Vãos (portas e janelas): 4,00 m²
Área líquida: 26,00 m²
Área com perda (15%): 29,90 m²
Peça: 30x60 cm
Assentamento: com desenho
• Peças: 167
• Caixas: 17 (1,80 m² por caixa) (R$ 1.196,00)
• Argamassa colante AC-III: 8 sacos de 20 kg (149,5 kg) (R$ 336,00)

Custo Estimado da Etapa: R$ 1.532,00
```

Pra entender: 30 − 4 = 26 m² × 1,15 = 29,9 m² ÷ 0,18 m² por peça = 166,1 → 167 peças; ÷ 1,8 m² por caixa = 16,6 → 17 caixas. Argamassa: 29,9 × 5 kg = 149,5 kg → 8 sacos.

### Teste B: só os obrigatórios

Área 30, Largura 30, Altura 60. O resto como vem (vãos vazio, perda vazia, AC-II, desenho Não, caixa vazia).

```
Área: 30,00 m²
Área com perda (10%, automática): 33,00 m²
Peça: 30x60 cm
• Peças: 184 (R$ 1.320,00)
• Argamassa colante AC-II: 9 sacos de 20 kg (165,0 kg) (R$ 270,00)

Custo Estimado da Etapa: R$ 1.590,00
```

| # | Mudar | O que muda no resultado | Custo |
|---|---|---|---|
| B2 | Portas e janelas: 4 | Aparecem "Vãos (portas e janelas): 4,00 m²" e "Área líquida: 26,00 m²"; 28,60 m²; 159 peças; 8 sacos | R$ 1.384,00 |
| B3 | m² por caixa: 1,8 | "• Peças: 184" e "• Caixas: 19 (1,80 m² por caixa) (R$ 1.320,00)" | R$ 1.590,00 |
| B4 | Desenho: Sim | "(25%, automática): 37,50 m²"; 209 peças; 10 sacos (187,5 kg) | R$ 1.800,00 |
| B5 | Argamassa: AC-III | "Argamassa colante AC-III: 9 sacos ... (R$ 378,00)" | R$ 1.698,00 |
| B6 | Peça 30 x 90 | "(15%, automática): 34,50 m²"; 128 peças; 14 sacos (276,0 kg), porque passa de 60 cm (8 kg/m²) | R$ 1.800,00 |

### Teste C: erros de digitação

Base: Teste B (área 30, peça 30 x 60). Mude só o indicado.

| # | O que mudar | Esperado na tela |
|---|---|---|
| C1 | Área vazia | Por favor, digite números válidos nos campos! |
| C2 | Altura vazia | (mesma mensagem) |
| C3 | Área = trinta | (mesma mensagem) |
| C4 | Área = 0 | Erro: Área e tamanho da peça devem ser maiores que zero. |
| C5 | Área = -30 | (mesma do C4) |
| C6, C7, C8 | Área = 30,5, depois 30.5, depois 30 1/2 | Os três: Área 30,50 m², 33,55 m², 187 peças, 9 sacos (167,8 kg), R$ 1.612,00 |
| C9 | Portas e janelas = -4 | Erro: Os valores não podem ser negativos. |
| C10 | Portas e janelas = 30 | Erro: O desconto de vãos deve ser menor que a área. |
| C11 | Portas e janelas = 40 | (mesma do C10) |
| C12 | Perda = -5 | Erro: A perda não pode ser negativa. |
| C13 | Perda = 2,5 | "Área com perda (2,5%): 30,75 m²", 171 peças, 8 sacos, R$ 1.470,00 |
| C14 | Área = 1-21/2 | Por favor, digite números válidos nos campos! |
| C15 | Portas e janelas = abc | (mesma do C14) |
| C16 | Área = 100000 | Janela: "Área de 100.000 m²: o limite é 2.000 m²." Continuar → 110.000,00 m², 611.112 peças, 27.500 sacos, R$ 5.225.000,00 |

**Limites com aviso** (janela "Confira os valores", com Cancelar e Continuar): os mesmos do Piso (área até 2.000 m² e peça de 5 a 300 cm em cada lado).

### Visual (Azulejo)

- Botões: Limpar, Anterior (volta pro Piso), Próximo (vai pro Rejunte) e Finalizar.
- Limpar: vãos, caixa e perda vazios, AC-II e desenho Não.
- No Azulejo não aparecem o rodapé nem o botão do Contrapiso.
- O "?" fala dos vãos, do AC-III para áreas molhadas, da argamassa (5 ou 8 kg por m²) e da perda automática. Termina com a nota dos valores padrão.

---

# REJUNTE

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
Área: 40,00 m²
Peça: 60x60 cm
Junta: 3 mm
Espessura da peça: 10 mm
Consumo: 0,158 kg/m²
• Rejunte (com 15% de perda): 7,3 kg = 4 latas de 2 kg (R$ 72,00)

Custo Estimado da Etapa: R$ 72,00
```

Pra entender: a fórmula é ((600 + 600) ÷ (600 × 600)) × 3 × 10 × 1,58 = 0,158 kg/m². × 40 m² × 1,15 = 7,27 kg (na tela aparece 7,3 kg, com 1 casa). Ficam 3 latas de 2 kg (6 kg) e faltam 1,27 kg; 2 latas de 1 kg somariam 2 kg, igual a uma de 2 kg, então o app troca por mais uma de 2 kg: 4 latas de 2 kg.

### Teste B: só os obrigatórios

Área 40, Largura 60, Altura 60, Junta 3. O resto como vem (espessura 8, perda 10).

```
Área: 40,00 m²
Peça: 60x60 cm
Junta: 3 mm
Espessura da peça: 8 mm
Consumo: 0,126 kg/m²
• Rejunte (com 10% de perda): 5,6 kg = 3 latas de 2 kg (R$ 54,00)

Custo Estimado da Etapa: R$ 54,00
```

| # | Mudar | O que muda no resultado | Custo |
|---|---|---|---|
| B2 | Peça 30 x 30 + Junta 5 | Consumo 0,421 kg/m²; "• Rejunte (com 10% de perda): 18,5 kg = 9 latas de 2 kg e 1 lata de 1 kg (R$ 172,00)" | R$ 172,00 |
| B3 | Botão "Usar dados do Piso" (com o Teste B do Piso preenchido) | Preenche Área 40 e peça 60 x 60 (a junta você digita) | (igual ao B, com a junta 3) |
| B4 | Botão "Usar dados do Azulejo" (com o B2 do Azulejo: área 30, vãos 4, peça 30 x 60) | Preenche Área 26 (já sem os vãos) e peça 30 x 60. Com junta 2: 3,6 kg, "2 latas de 2 kg (R$ 36,00)" | R$ 36,00 |

### Teste C: erros de digitação

Base: Teste B. Mude só o indicado.

| # | O que mudar | Esperado na tela |
|---|---|---|
| C1 | Área vazia | Por favor, digite números válidos nos campos! |
| C2 | Junta vazia | (mesma mensagem) |
| C3 | Área = quarenta | (mesma mensagem) |
| C4 | Área = 0 | Erro: Área, tamanho da peça e junta devem ser maiores que zero. |
| C5 | Área = -40 | (mesma do C4) |
| C6 | Junta = 0 | (mesma do C4) |
| C7 | Junta = -3 | (mesma do C4) |
| C8, C9, C10 | Área = 40,5, depois 40.5, depois 40 1/2 | Os três: Área 40,50 m², 5,6 kg, 3 latas de 2 kg, R$ 54,00 |
| C11 | Junta = 1,5 | "Junta: 1,5 mm", 2,8 kg, "1 lata de 2 kg e 1 lata de 1 kg (R$ 28,00)" (no singular) |
| C12 | Junta = 1/2 | Janela: "Junta de 0,5 mm: o normal é de 1 mm a 15 mm." Continuar → "Junta: 0,5 mm", 0,9 kg, "1 lata de 1 kg (R$ 10,00)" |
| C13 | Espessura vazia | Igual ao Teste B (usa o padrão de 8 mm) |
| C14 | Espessura = 0 | Erro: A espessura da peça deve ser maior que zero. |
| C15 | Perda = -5 | Erro: A perda não pode ser negativa. |
| C16 | Perda = 2,5 | "Rejunte (com 2,5% de perda): 5,2 kg" |
| C17 | Área = 1-21/2 | Por favor, digite números válidos nos campos! |
| C18 | Área = 1 | 0,1 kg, "1 lata de 1 kg (R$ 10,00)" |
| C19 | Área = 100000 | Janela: "Área de 100.000 m²: o limite é 2.000 m²." Continuar → 13.904,0 kg, 6.952 latas de 2 kg, R$ 125.136,00 |
| C20 | Junta = 30 | Janela: "Junta de 30 mm: o normal é de 1 mm a 15 mm." Continuar → Consumo 1,264 kg/m², 55,6 kg, 28 latas, R$ 504,00 |

**Limites com aviso** (janela "Confira os valores", com Cancelar e Continuar): área até 2.000 m² e junta de 1 a 15 mm (junta de 30 mm é quase certeza de quem digitou em cm) (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Rejunte)

- Botões: Limpar, Anterior (volta pro Azulejo), Próximo (vai pra Pintura) e Finalizar.
- Limpar: área, peça e junta vazias, espessura 8 e perda 10.
- Os botões "Usar dados do Piso (40 m², peça 60x60 cm)" e "Usar dados do Azulejo (26 m², peça 30x60 cm)" só aparecem se essas abas estiverem preenchidas.
- O "?" fala dos botões "Usar dados", da espessura padrão de 8 mm e das latinhas de 1 kg e 2 kg. Termina com a nota dos valores padrão.

---

# PINTURA

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

Custo Estimado da Etapa: R$ 1.825,00
```

Pra entender: parede 100 × 3 demãos ÷ 10 × 1,15 = 34,5 L. Os complementos são uma demão sobre parede + teto (140 m²): selador 140 ÷ 8 × 1,15 = 20,1 L; fundo 140 ÷ 10 × 1,15 = 16,1 L; massa 140 × 0,5 kg × 2 demãos × 1,15 = 161 kg ÷ 25 = 6,4 → 7 baldes. No fundo, 16,1 L precisaria de 5 galões (18 L), que é o mesmo que 1 lata, então o app leva 1 lata.

### Teste B: só os obrigatórios

Área de parede 100. O resto como vem (teto vazio, demãos 2, rendimento 12, selador Não, massa Não, fundo Não, perda 10).

```
Parede: 100,00 m²
Demãos: 2
Rendimento: 12 m²/L
• Tinta de parede (com 10% de perda): 18,3 L = 1 lata de 18 L e 1 galão de 3,6 L (R$ 390,00)

Custo Estimado da Etapa: R$ 390,00
```

Pra conferir o resto, use o Teste B e mude só o indicado:

| # | Mudar | O que muda no resultado | Custo |
|---|---|---|---|
| B2 | Parede vazia + Teto 40 | Só a linha "Teto: 40,00 m²"; "• Tinta de teto (com 10% de perda): 7,3 L = 3 galões de 3,6 L (R$ 225,00)" | R$ 225,00 |
| B3 | Teto: 40 (com a parede 100) | As duas tintas | R$ 615,00 |
| B4 | Selador: Sim | "• Selador (com 10% de perda): 13,8 L = 4 galões de 3,6 L (R$ 180,00)" | R$ 570,00 |
| B5 | Massa: Massa acrílica | "• Massa acrílica (com 10% de perda): 110,0 kg = 5 baldes de 25 kg (R$ 650,00)" (100 m² × 0,5 kg × 2 demãos × 1,10) | R$ 1.040,00 |
| B6 | Fundo preparador: Sim | "• Fundo preparador (com 10% de perda): 11,0 L = 4 galões de 3,6 L (R$ 200,00)" | R$ 590,00 |
| B7 | Parede: 180 | "33,0 L = 2 latas de 18 L (R$ 600,00)" (1 lata + 5 galões vira 2 latas) | R$ 600,00 |
| B8 | Parede: 10 | "1,8 L = 1 galão de 3,6 L (R$ 90,00)" (no singular) | R$ 90,00 |

### Teste C: erros de digitação

Base: Teste B (parede 100). Mude só o indicado.

| # | O que mudar | Esperado na tela |
|---|---|---|
| C1 | Parede e teto vazios | Por favor, digite números válidos nos campos! |
| C2 | Demãos vazia | (mesma mensagem) |
| C3 | Parede = cem | (mesma mensagem) |
| C4 | Parede = 0 | Erro: Informe a área de parede ou a área de teto. |
| C5 | Parede = -100 | Erro: As áreas não podem ser negativas. |
| C6 | Demãos = 0 | Erro: Demãos e rendimento devem ser maiores que zero. |
| C7 | Demãos = -2 | (mesma do C6) |
| C8 | Demãos = 2,5 | Por favor, digite números válidos nos campos! (demão é número inteiro) |
| C9 | Demãos = 5 | 45,8 L = 2 latas de 18 L e 3 galões de 3,6 L, R$ 870,00 |
| C10 | Demãos = 6 | Janela: "6 demãos: o limite é 5 (normalmente são 2 ou 3)." Cancelar não calcula; Continuar → 55,0 L = 3 latas de 18 L e 1 galão de 3,6 L, R$ 990,00 |
| C11 | Demãos = 22 | Janela: "22 demãos: o limite é 5 (normalmente são 2 ou 3)." Continuar → 201,7 L = 11 latas de 18 L e 2 galões de 3,6 L, R$ 3.480,00 |
| C12, C13, C14 | Parede = 100,5, depois 100.5, depois 100 1/2 | Os três: Parede 100,50 m², 18,4 L, R$ 390,00 |
| C15 | Rendimento = 0 | (mesma do C6) |
| C16 | Rendimento vazio | Igual ao Teste B (usa o padrão de 12) |
| C17 | Rendimento = 12,5 | "Rendimento: 12,5 m²/L", 17,6 L = 1 lata de 18 L, R$ 300,00 |
| C18 | Perda = -5 | Erro: A perda não pode ser negativa. |
| C19 | Perda = 2,5 | "Tinta de parede (com 2,5% de perda): 17,1 L = 1 lata de 18 L", R$ 300,00 |
| C20 | Parede = 1-21/2 | Por favor, digite números válidos nos campos! |
| C21 | Parede = 100000 | Janela: "Área de parede de 100.000 m²: o limite é 5.000 m²." Continuar → 18.333,3 L = 1.018 latas e 3 galões, R$ 305.670,00 |

**Limites com aviso** (janela "Confira os valores", com Cancelar e Continuar): demãos até 5 (antes era erro) e área de parede e de teto até 5.000 m² cada (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir).

### Visual (Pintura)

- Botões: Limpar, Anterior (volta pro Rejunte), Próximo (vai pra Esquadrias) e Finalizar.
- Limpar: parede e teto vazios, demãos 2, rendimento 12, perda 10, selador Não, massa Não e fundo Não.
- O "?" explica que dá para preencher só parede ou só teto, o que é o rendimento, a diferença entre massa corrida e acrílica e que a massa é contada em 2 demãos. Termina com a nota dos valores padrão.
- Menu da massa: Não, Massa corrida, Massa acrílica.

---

# ESQUADRIAS

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

Portas e janelas: use esta lista para pedir orçamento ao fornecedor.
```

Pra entender: o contorno da porta é os dois lados + a parte de cima (2 × 2,10 + 0,80 = 5,0 m); o da janela, os quatro lados (2 × (1,20 + 1,00) = 4,4 m). Tudo somado dá 40,1 m. Espuma: 40,1 ÷ 6 = 6,7 → 7 tubos. Parafusos: 40,1 ÷ 0,4 = 100,25 → 101. Argamassa: 40,1 × 1,5 = 60,2 kg → 4 sacos.

### Teste B: só os obrigatórios

Adicione: Porta, 3, 80, 210 e Janela, 2, 120, 100 (material como vem: Não informado). Insumos todos em Não.

```
Portas:
• 3x Porta 80 x 210 cm: 1,68 m² cada

Janelas:
• 2x Janela 120 x 100 cm: 1,20 m² cada

Total: 3 portas e 2 janelas
Área total dos vãos: 7,44 m²

Portas e janelas: use esta lista para pedir orçamento ao fornecedor.
```

Pra conferir o resto, use o Teste B e mude só o indicado:

| # | Mudar | O que muda no resultado | Custo |
|---|---|---|---|
| B2 | Espuma: Sim | Aparecem "Insumos de fixação:" e "• Espuma expansiva: 4 tubos de 500 ml (R$ 140,00)" | R$ 140,00 |
| B3 | Parafusos: Sim | "• Parafusos com bucha: 60 un (R$ 48,00)" | R$ 48,00 |
| B4 | Argamassa: Sim | "• Argamassa de fixação: 35,7 kg = 2 sacos de 20 kg (R$ 50,00)" | R$ 50,00 |
| B5 | Adicione de novo: Porta, 2, 80, 210 | Não cria linha nova: vira "5x Porta 80 x 210 cm"; "Total: 5 portas e 2 janelas"; área 10,80 m² | Sem custo: "Portas e janelas: use esta lista para pedir orçamento ao fornecedor." |
| B6 | Toque no X da janela | A janela sai da lista; o resultado antigo some | — |

### Teste C: erros de digitação

| # | O que fazer | Esperado na tela |
|---|---|---|
| C1 | Lista vazia + Calcular | Nenhuma porta ou janela na lista ainda. |
| C2 | Quantidade vazia + Adicionar à lista | Por favor, digite números válidos nos campos! (nada entra na lista) |
| C3 | Quantidade = três + Adicionar | (mesma do C2) |
| C4 | Quantidade = 0 + Adicionar | (mesma do C2) |
| C5 | Quantidade = -3 + Adicionar | (mesma do C2) |
| C6 | Quantidade = 2,5 + Adicionar | (mesma do C2) (quantidade é número inteiro) |
| C7 | Largura = 0 + Adicionar | (mesma do C2) |
| C8 | Largura = 1-21/2 + Adicionar | (mesma do C2) |
| C9 | Digitar uma porta (3, 80, 210) e tocar em Calcular sem Adicionar | Você digitou uma porta ou janela, mas não tocou em "Adicionar à lista". |
| C10 | Janela 1, 120,5, 100 (depois 120.5, depois 120 1/2) | Os três: "1x Janela 120,5 x 100 cm: 1,21 m² cada" |
| C11 | Só 1 porta 80 x 210 com os 3 insumos em Sim | "1 tubo de 500 ml (R$ 35,00)" e "7,5 kg = 1 saco de 20 kg (R$ 25,00)" (no singular), 13 parafusos, R$ 70,40 |
| C12 | Porta, 1000, 80, 210 com os 3 insumos | Janela no Adicionar: "Quantidade de 1.000: o limite é 100 de cada item." Continuar → 834 tubos, 12.500 parafusos, 375 sacos, R$ 48.565,00 |
| C13 | Porta, 3, 8000, 210 | Janela no Adicionar: "Largura de 8.000 cm: o limite é 500 cm." Continuar → "3x Porta 8.000 x 210 cm: 168,00 m² cada", área 504,00 m² |

**Limites com aviso** (janela "Confira os valores", com Cancelar e Continuar): até 100 de cada item, largura até 500 cm e altura até 400 cm (criados pelo Leo em 03/11/2026; o engenheiro ainda vai conferir). Na Esquadrias, a janela aparece no "Adicionar à lista", antes de o item entrar na lista.

### Visual (Esquadrias)

- Esquadrias é a última aba do app. Botões: Limpar, Anterior (volta pra Pintura) e Finalizar. **Não tem Próximo nem Avançar.**
- Limpar: lista vazia, Tipo Porta, Material Não informado e os 3 insumos em Não.
- Depois de Adicionar à lista, os campos de quantidade, largura e altura ficam vazios para a próxima.
- Cada item da lista tem um X à direita, sem cortar o texto (teste com "3x Porta 80 x 210 cm (Vidro temperado)").
- O "?" explica como usar a lista (tipo, quantidade, medidas, Adicionar), que itens iguais são somados e que o material é só para a cotação. Termina com a nota dos valores padrão.
- Menus: Tipo (Porta, Janela) e Material (Não informado, Alumínio, Madeira, Vidro temperado).

---

Quando terminar cada aba, me manda "ok" ou os prints. 😉
