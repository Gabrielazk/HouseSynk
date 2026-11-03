# Pendências de visual (arrumar por último)

## Baldrame
- "1 sacos" (plural) — C18
- "2363 sacos" sem ponto de milhar — C17
- Linhas com zero aparecem: "Areia: 0,00 m³ (R$ 0,00)" e "Brita: 0,00 m³ (R$ 0,00)" — C18

## Paredes
- "1 sacos" (plural) — casos B, C5, C6, C7, C12, C13 e C17
- Janela do C16 diz "o limite é 2 m²" em vez de "2000 m²"
- Plural de milheiro: aparece "0,79 milheiros" e "1,16 milheiros"; abaixo de 2 o certo é singular ("0,79 milheiro")
- "1575 un (1,57 milheiros)": deveria arredondar para 1,58
- Números grandes sem ponto de milhar: "2625000 un", "2625,00 milheiros", "100000,00 m²" e "Área de 100000 m²" na janela (C16)

## Laje
- Perda sem casa decimal: 2,5% aparece "2%" (C9)

## Telhado
- "1 peças" (plural) — C18
- Perda sem casa decimal: 2,5% aparece "2%" (C9)

## Elétrica
- Perda sem casa decimal: 2,5% aparece "2%" (C7)
- Arredondamento para baixo: 215,25 m aparece "215,2 m" (C7)
- Números grandes sem ponto de milhar: "11121,0 m", "33000,0 m", "2010 un", "Tomadas: 2000" (C16)
- Tomadas e Interruptores aparecem duas vezes: no topo (quantos pontos a obra tem) e na lista com • (as peças a comprar). Decidido: fica assim, são coisas diferentes

## Hidráulica
- Perda sem casa decimal: 2,5% aparece "2%" (C7)
- Números grandes sem ponto de milhar: "4400,0 m", "4000 un", "Pontos de água fria: 1000" (C15)
- Dicas dos campos de tubo diferentes da Elétrica: "Água fria 25 mm, em metros" não tem "(opcional)" nem exemplo; na Elétrica é "Fio 1,5 mm² em metros (opcional)" e "Conduíte em metros (opcional, ex: 150)". Decidir se acrescenta "(opcional)" (textos no comum.py)

## Contrapiso
- Perda sem casa decimal: 2,5% aparece "2%" (C13)
- Números grandes sem ponto de milhar: "100000,00 m²", "5250,000 m³", "33750 sacos", "3375,00 m³" (C16)

## Piso
- Perda sem casa decimal: 2,5% aparece "2%" (C11)
- Números grandes sem ponto de milhar: "100000,00 m²", "110000,00 m²", "305556 peças", "27500 sacos", "550000,0 kg" (C20)

## Azulejo
- Perda sem casa decimal: 2,5% aparece "2%" (C13)
- Arredondamento para baixo: 153,75 kg aparece "153,7 kg" (C13); no C6, 167,75 vira 167,8 (certo), então não acontece sempre
- Números grandes sem ponto de milhar: "100000,00 m²", "110000,00 m²", "611112 peças", "27500 sacos", "550000,0 kg" (C16)

## Rejunte
- Perda sem casa decimal: 2,5% aparece "2%" (C16)
- Números grandes sem ponto de milhar: "100000,00 m²", "13904,00 kg", "6952 latas" (C19)
- Linha das latas sem nome: aparece "• Rejunte (com 10% de perda): 5,56 kg" e embaixo "• 3 latas de 2 kg (R$ 54,00)", com o • sozinho na frente da quantidade. Nas outras abas, toda linha com • começa com o nome do material. Sugestão do Leo: juntar numa linha só, igual à Pintura ("• Rejunte (com 10% de perda): 5,56 kg = 3 latas de 2 kg (R$ 54,00)"). Decidir. Muda o testes_rodada1.md

## Pintura
- Perda sem casa decimal: 2,5% aparece "2%" (C19)
- Números grandes sem ponto de milhar: "100000,00 m²", "18333,3 L", "1018 latas" (C21)
- "Demãos" e "Rendimento" do topo valem só pras tintas, mas o resultado não diz isso. No Teste A o topo mostra "Demãos: 3" e "Rendimento: 10 m²/L", mas o selador usa 1 demão (8 m²/L), o fundo 1 demão (10 m²/L) e a massa 2 demãos (0,5 kg/m² cada). Quem lê pode achar que o selador foi feito com 3 demãos. Decidir se coloca uma nota (ex.: "Selador e fundo: 1 demão; massa: 2 demãos, sobre parede + teto"). Parecido com os itens da espessura e do desenho. Muda o testes_rodada1.md

## Reboco
- Linha com zero aparece: "Cal: 0 sacos de 20 kg (R$ 0,00)" — B5 (já marcado no roteiro)
- Perda sem casa decimal: 2,5% aparece "2%" (C14)
- Números grandes sem ponto de milhar: "100000,00 m²", "2200,000 m³", "6000 sacos", "22000 sacos", "2000,00 m³" (C17)

## Elétrica, Hidráulica e Esquadrias (decidir junto com as correções)
- Linhas do topo com zero aparecem: "Tomadas: 0", "Interruptores: 0", "Pontos de luz: 0" (Elétrica B7) e "Pontos de água quente: 0", "Pontos de esgoto: 0" (Hidráulica B2), "Pontos de água fria: 0" e "Pontos de água quente: 0" (Hidráulica B4); na Esquadrias, a contagem "Portas: 1 | Janelas: 0". Decidir se somem também

## Esquadrias
- As linhas em branco entre "Portas:", "Janelas:" e "Insumos de fixação:" ficam: elas separam grupos (lembrete)
- Contagem com zero: com só portas ou só janelas aparece "Portas: 1 | Janelas: 0" (C11, B6) ou "Portas: 0 | Janelas: 1" (C10). Decidir junto com os zeros do topo da Elétrica e da Hidráulica
- "Portas:" aparece duas vezes com sentidos diferentes: como título do grupo (com os • embaixo) e na contagem ("Portas: 4 | Janelas: 5"). Sugestão: trocar a contagem por algo como "Total: 4 portas e 5 janelas". Decidir
- Números grandes sem ponto de milhar: "1000x Porta", "Portas: 1000", "1680,00 m²", "12500 un", "7500,0 kg" (C12)
- "Custo Estimado da Etapa: R$ 0,00" no Teste B (portas e janelas não têm preço, são só pra cotação). Decidir se fica assim ou vira uma frase (ex.: "Portas e janelas: peça orçamento ao fornecedor"). Já marcado no roteiro

## Geral (afeta várias abas — corrigir junto)
- Plural: "1 sacos", "1 peças" etc. Acontece em toda aba que mostra quantidade (a Laje também, com área bem pequena)
- Ponto de milhar: valores em R$ têm ponto ("R$ 3.150.000,00"), mas quantidades não. Falta em todas as abas testadas até agora (Baldrame, Paredes, Laje, Telhado, Elétrica, Hidráulica, Contrapiso, Reboco, Piso, Azulejo, Rejunte, Pintura e Esquadrias; a Brocas não teve caso com número grande)
- Perda sem casa decimal ("2,5%" vira "2%"): Laje, Telhado, Elétrica, Hidráulica, Contrapiso, Reboco, Piso, Azulejo, Rejunte e Pintura (a Esquadrias não tem perda). Brocas, Baldrame e Paredes já mostram certo
- Texto da perda diferente: Laje, Telhado, Elétrica, Hidráulica, Rejunte e Pintura mostram "(com 5% de perda)"; Brocas, Baldrame, Paredes e Contrapiso mostram "(5% perda)"; o Piso e o Azulejo mostram um terceiro jeito, "Área com perda (12%)" e "(10%, automática)". Escolher um jeito só (ou decidir se o do Piso pode ficar, porque é o nome de uma área)
- Linha com zero: regra 14 já decidida (material com zero não aparece). A Paredes e a Laje já seguem; o Baldrame (C18) e o Reboco (B5) ainda mostram
- Linha em branco antes dos materiais (•): tirar no Telhado, Elétrica, Hidráulica e Pintura, pra ficar igual às outras abas (decidido: sem linha). A linha em branco fica só pra separar o valor de cada aba ("Custo Estimado da Etapa") e, na Esquadrias, os grupos
- Janela "Confira os valores": hoje só existe em Brocas, Baldrame e Paredes. Nas outras abas os valores grandes passam sem aviso (os ⚠️ do roteiro). Decidir os limites de cada aba (as sugestões estão no testes_rodada1.md) e colocar a janela, com Cancelar e Continuar. Na Pintura, as demãos acima de 5 hoje dão erro e também viram a janela. Depois, testar os botões dessas abas no app
- Arredondamento: o computador guarda 1,575 como 1,57499..., por isso arredonda para baixo. Acontece na Paredes (1,575 vira 1,57), na Elétrica (215,25 vira 215,2) e no Azulejo (153,75 vira 153,7). Não acontece sempre (no Azulejo, 167,75 vira 167,8 certo), porque depende de como cada número fica guardado por dentro
- Espessura não aparece no resultado: Contrapiso e Reboco mostram só área, traço e volume (na Laje aparece "Capa de concreto: 4 cm" ou "Espessura: 10 cm"). Decidir se acrescenta a linha da espessura (ex.: "Espessura média: 5 cm" no Contrapiso, "Espessura: 2 cm" no Reboco). Sugestão do Leo: sim, pra quem olha o resultado ou o Resumo saber com que espessura a conta foi feita. Muda o testes_rodada1.md
- Desenho não aparece no resultado do Piso e do Azulejo: no B4 dos dois aparece só "(25%, automática)", sem dizer que os 25% vêm do assentamento com desenho; no Teste A (desenho Sim, perda 12) nada mostra que o desenho foi escolhido. Parecido com o item da espessura: decidir se acrescenta uma linha (ex.: "Assentamento: com desenho"). Muda o testes_rodada1.md
- "Área líquida" diferente: na Paredes aparece sempre, mesmo igual à bruta ("Área bruta: 30,00 m²" e "Área líquida: 30,00 m²"); no Reboco e no Azulejo, "Vãos" e "Área líquida" só aparecem quando tem vãos. Escolher um jeito só. Sugestão do Leo: o do Reboco e do Azulejo (sem repetir a área quando não tem vão)
- Mensagem do desconto igual à área: na Paredes (C9) e no Reboco (C11), com o desconto igual à área, a mensagem diz "não pode ser maior que a área da parede", mas era igual. O Azulejo já usa um texto que serve pros dois casos: "O desconto de vãos deve ser menor que a área." Decidir um texto só
- Casas decimais do kg diferentes: o Rejunte mostra 2 casas ("5,56 kg", "13904,00 kg"); a argamassa do Piso e do Azulejo mostra 1 ("224,0 kg"). Escolher um padrão pra kg
- Quebra de linha estranha nos resultados: acontece em todas as abas, cada uma de um jeito um pouco diferente (ex.: na Brocas, "12 m" quebra separando o número da unidade). Na hora de corrigir: abrir cada aba no app, anotar como está e decidir como deve ficar (conferir abrindo o app, o script não pega isso)
- Modo claro: fundo das telas continua escuro e os textos somem (o pop-up fica certo). Causa: a linha "self.md_bg_color = self.theme_cls.backgroundColor" nas telas de src/views/ pega a cor só uma vez. Correção: apagar essa linha (afeta todas as telas)
- Ao corrigir esses itens, o testes_rodada1.md muda (resultados esperados) e talvez outras rodadas
