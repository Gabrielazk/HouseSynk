# Visual da rodada 3b (EUA, português): para testar tudo junto no fim

Arquivo temporário, criado em 15/11/2026 (pedido da Gabi). Fica na pasta testes_manuais, junto com o roteiro.

**Como funciona:**
1. Durante a 3b, o Leo do terminal testa as contas aba por aba (rodada3.py) e **não precisa listar o visual**: ele já está aqui. Cada aba nova que o Leo do chat monta no roteiro ganha os itens dela aqui.
2. No fim, com todas as 13 abas testadas no terminal, a Gabi abre o app (Configurações → País **EUA ($)**, idioma **Português**) e confere tudo desta lista de uma vez, marcando [x].
3. O que der diferente vai para o pendencias_rodada3b.md (a Gabi traz para o Leo do chat). Depois de corrigir, a Gabi confere de novo só o que mudou.
4. Quando a rodada 3 fechar, este arquivo é apagado junto com o de pendências.

Os números citados (ex.: "BR-B3") são casos do testes_rodada3.md: é só digitar o que o caso pede (dê **Limpar** antes de cada um).

## Em toda aba

- [ ] **Medidas digitadas em ft, in e sq ft** convertem certo, inclusive com fração ("2 1/2", "3/8", "11 3/4") e com o milhar americano ("1,500" = mil e quinhentos; "2,5" continua 2.5).
- [ ] **Números com ponto e milhar com vírgula:** "1,000.00 sq ft", "$ 2,197.16". Nenhuma vírgula decimal e nenhum "R$".
- [ ] **Embalagens americanas:** sacos de 50 lb (thinset), caixas de 10 lb, sacos de 25 lb e caixas de 7 lb (rejunte), baldes de 5 gal e galões de 1 gal (tinta, primer e impermeabilizante).
- [ ] **Nenhum texto do Brasil** em nenhuma aba: m, cm, mm, m², kg, L, "lata", "AC-I", vírgula decimal (desde 09/11/2026, também no concreto e no ferro do Baldrame).
- [ ] **Polegadas em fração:** "12 x 12 in", "1/8 in", "5/16 in", "11 3/4 x 12 in" (nunca "11.75" nem "0.031").
- [ ] **Avisos de limite** com as unidades dos EUA: "Área de 21,529 sq ft: o limite é 21,528 sq ft.", "Junta de 5/8 in: o normal é de 1/16 in a 9/16 in.".
- [ ] **"?"** de cada aba com a legenda das siglas no fim (só em português).
- [ ] O que já valia nas rodadas 1 e 2 continua: Limpar, Anterior, Próximo, Finalizar, tema claro e escuro, barra de rolagem, número e unidade sem quebra de linha.

## Brocas

- [ ] Perda vem com **10**, estribo com **8** (in) e bitola **#4**; o título é "Bitola do ferro", sem "(mm)".
- [ ] No resultado, nenhum m³, kg, m, cm, "sacos de 50 kg", "barras de 12 m" ou vírgula decimal; o estribo aparece em fração ("c/ 4 1/2 in", BR-C19).
- [ ] "?" das Brocas: fala do padrão americano (#3, #4 e #5, barras de 20 ft, estribo #3, 3 in de cobrimento, sacos de 94 lb e concreto pronto de 80 lb) e termina com a legenda das siglas.
- [ ] **Lista de compras** (Finalizar com o BR-B3, botão Lista de compras do Resumo), igual à aba (regra 17), no grupo MATERIAL BÁSICO:
  - Cimento: 22 sacos de 94 lb
  - Areia: 1.60 cu yd
  - Brita: 2.40 cu yd
  - Ou concreto pronto: 144 sacos de 80 lb (no lugar de cimento, areia e brita)
  - Aço/Ferragem: 201.3 lb (19 barras de 20 ft)
  - Arame recozido: 4.0 lb = 2 rolos de 3.5 lb
- [ ] No Orçamento do Resumo, as Brocas com **$ 1,447.78** (Mão de obra $ 800.00).

## Baldrame

- [ ] Estribo vem com **8** (in) e perda com **5**.
- [ ] **P9:** o "?" diz "baldes de 5 gal (com 4,75 gal de produto)": nos EUA o certo é **"4.75 gal"** (com ponto).
- [ ] **Desde 09/11/2026 (Parte A):** o título "Bitola do ferro" (sem "(mm)") com #3, #4 e #5; o "?" fala do padrão americano do ferro e do concreto pronto; nenhum m³, kg, "sacos de 50 kg", "barras de 12 m" ou "mm" no resultado.
- [ ] **Rodada 3b, lista de compras com Brocas e Baldrame juntos** (BR-B3 nas Brocas + BA-B6 no Baldrame, depois Finalizar e Lista de compras): um "Cimento" só, somando as duas abas, no grupo MATERIAL BÁSICO:
  - Cimento: 29 sacos de 94 lb
  - Areia: 2.12 cu yd
  - Brita: 3.18 cu yd
  - Ou concreto pronto: 191 sacos de 80 lb (no lugar de cimento, areia e brita)
  - Aço/Ferragem: 361.6 lb (35 barras de 20 ft)
  - Arame recozido: 7.2 lb = 3 rolos de 3.5 lb (os rolos saem do total somado: 4.0 + 3.2 lb = 7.2 lb, e não 2 + 1 rolos)
- [ ] No Orçamento do Resumo: Brocas $ 1,447.78 e Baldrame $ 329.07.

## Paredes

- [ ] Os campos **Assentamento** e **Traço da massa não aparecem** nos EUA (o bloco vai sempre do mesmo jeito e a massa vem pronta).
- [ ] O menu do bloco só tem **"Bloco de concreto CMU (8x8x16)"**.
- [ ] Junta vem com **3/8** e quebra com **5**.
- [ ] No resultado, nenhum m², m³, kg, "milheiro", "un (0,38 milheiro)", "cimento", "cal" ou vírgula decimal; os blocos só em peças ("378 un").
- [ ] "?" das Paredes: fala do bloco CMU 8x8x16 (7 5/8 x 7 5/8 x 15 5/8 in, 1.125 bloco por sq ft), da massa pronta tipo S de 80 lb (13 blocos por saco), da opção com cimento de alvenaria de 70 lb e areia, dos 10% de perda da massa, e termina com a legenda das siglas.
- [ ] **Lista de compras** (Finalizar com o PA-B, botão Lista de compras do Resumo), no grupo MATERIAL BÁSICO:
  - Bloco de concreto CMU (8x8x16): 378 un
  - Massa pronta tipo S: 31 sacos de 80 lb
  - Ou: 9 sacos de cimento de alvenaria tipo S de 70 lb + 2,160 lb de areia (no lugar da massa pronta)
- [ ] No Orçamento do Resumo, as Paredes com **$ 2,640.00**.

## Laje

- [ ] Nos EUA **não aparecem**: o menu "Tipo de laje", o enchimento (isopor ou lajota), a capa e a espessura da maciça.
- [ ] Espessura vem com **4**, perda com **5**; tela **Não**, lona **Sim**, base **Sim**.
- [ ] No resultado aparece "Tipo de laje: Piso de concreto no chão (slab-on-grade)"; nenhum m², m³, kg, "sacos de 50 kg", "painéis de 2 x 3 m", "lajotas" ou vírgula decimal.
- [ ] "?" da Laje: fala do slab-on-grade, da espessura de 4 in (mínimo de 3 1/2 in do IRC), da base de brita de 4 in, da lona em rolos de 10 x 100 ft, da tela em painéis de 5 x 10 ft, do concreto pronto e do concreto usinado (caminhão), e termina com a legenda das siglas.
- [ ] **Lista de compras** (Finalizar com o LA-B2, botão Lista de compras do Resumo), no grupo MATERIAL BÁSICO:
  - Cimento: 44 sacos de 94 lb
  - Areia: 3.24 cu yd
  - Brita: 4.86 cu yd
  - Ou concreto pronto: 292 sacos de 80 lb (no lugar de cimento, areia e brita)
  - Ou concreto usinado (caminhão): 6.50 cu yd (no lugar de cimento, areia e brita)
  - Brita da base (4 in): 6.48 cu yd
  - Lona plástica (vapor retarder): 1 rolo de 10 x 100 ft
  - Tela soldada: 11 painéis de 5 x 10 ft
- [ ] **Lista de compras com Brocas e Laje juntas** (BR-B3 nas Brocas + LA-B2 na Laje): um "Cimento" só, somando as duas abas:
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
- [ ] No Orçamento do Resumo: Brocas $ 1,447.78 e Laje $ 2,121.60.

## Telhado

- [ ] (o Leo do chat acrescenta quando montar a aba no roteiro)

## Elétrica

- [ ] (o Leo do chat acrescenta quando montar a aba no roteiro)

## Hidráulica

- [ ] (o Leo do chat acrescenta quando montar a aba no roteiro)

## Reboco

- [ ] (o Leo do chat acrescenta quando montar a aba no roteiro)

## Piso

- [ ] O "?" abre a Ajuda com o texto do Piso, a nota dos valores padrão e, no fim, a legenda: "Siglas: ft = pés · in = polegadas · sq ft = pés quadrados · cu yd = jardas cúbicas · lb = libras · gal = galões".
- [ ] O "?" diz **"10% para peças de até 27 1/2 in, 15% até 35 3/8 in e 20% acima disso"**, e o exemplo do começo é "(ex.: 12 x 12 in)" (corrigido na rodada 3, P2).
- [ ] O menu da argamassa mostra os nomes inteiros, sem cortar: "Não modificada (ANSI A118.1)" e "Modificada (ANSI A118.4)".
- [ ] Limpar: perda vazia, A118.1, desenho Não, caixa e rodapé vazios.
- [ ] O botão "Usar a área do Contrapiso" **não aparece** nos EUA (o Contrapiso saiu dos EUA em 09/11/2026).
- [ ] **Faixa das abas:** o Contrapiso não aparece no Acabamento (Reboco → Piso → Azulejo → Rejunte → Pintura → Esquadrias), e o "Avançar para a próxima etapa" da Hidráulica vai para o Reboco.

## Azulejo

- [ ] O "?" do Azulejo: mesmo texto da P2 (27 1/2 in e 35 3/8 in) e a legenda das siglas no fim.
- [ ] Limpar: A118.4 volta a vir escolhida.

## Rejunte

- [ ] Os botões "Usar dados do Piso" e "Usar dados do Azulejo" mostram a peça **em fração e com espaço** (P7): "Usar dados do Piso (430 sq ft, peça 11 3/4 x 11 3/4 in)". Ao tocar, os campos também ficam em fração (11 3/4).
- [ ] O "?" fala do padrão 5/16 in e dos dois tipos (sem areia até 1/8 in, com areia acima), com a legenda no fim.
- [ ] Limpar: espessura volta a 5/16 e perda a 10.

## Pintura

- [ ] Selador e Massa **não aparecem**; Primer aparece.
- [ ] Rendimento já vem 400.
- [ ] O "?" fala de 400 sq ft por galão, de baldes de 5 gal e galões de 1 gal, com a legenda no fim.
- [ ] Limite do rendimento (rodada 3, P8): a janela "Confira os valores" aparece com 12 sq ft/gal (o costume do Brasil, em m²/L) e com 900 sq ft/gal.

## Esquadrias

- [ ] (o Leo do chat acrescenta quando montar a aba no roteiro)
