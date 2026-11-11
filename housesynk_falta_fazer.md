# HouseSynk: O que ainda falta fazer

Cópia das partes que ainda faltam na especificação (claude/especificacao_housesynk.md, atualizada em Nov 9, 2026). O texto é o mesmo da especificação. A especificação do projeto não foi alterada. O que já foi feito está no arquivo housesynk_ja_feito.md.

## Ordem de trabalho (o que falta)

4. EM ANDAMENTO: funcionalidades extras, na ordem de prioridade da seção Resumo e extras (falta o cronograma, que espera as respostas de produtividade).
6. EM ANDAMENTO: versão EUA. **Agora:** Parte A (as abas que faltam; ver a seção Versão EUA). Laje: falta a Gabriela colar e testar no app. Próxima: Telhado. Depois a Parte B (abas novas só dos EUA); por último a tabela de preços (por país e estado, com as embalagens de cada país).
7. EM ANDAMENTO (desde Oct 28, 2026): **testes gerais** de tudo o que existe, seguindo o plano em claude/plano_testes.md (uma aba por vez, testes A, B e C, resultado esperado calculado com o código real; o esperado é sempre o que o app deve mostrar, nunca a saída do app). O andamento de cada aba e as decisões tomadas nos testes ficam registrados lá.
   - **Ordem nova (decisão da Gabriela, Nov 5, 2026):** rodada 3 → Parte A da versão EUA (as outras 9 abas inteiras e o resto do Baldrame, cada aba já com a lista de compras, o Resumo, o PDF e o WhatsApp em unidades americanas) → rodada 3b (as abas da Parte A nos EUA, em português) → rodada 4 (EUA em inglês, todas as abas dos EUA de uma vez) → rodadas 5 a 8 (troca de país, Histórico, Resumo/PDF, Login e Configurações) → Parte B (abas novas dos EUA) e o teste delas (pode vir antes das rodadas 5 a 8, a decidir) → tabela de preços. Motivo: o app só vai para a App Store com os EUA prontos; assim os EUA são testados uma vez só, já completos, e as rodadas 4, 5 e 7 não precisam de reteste.
8. Conferência final completa antes de publicar: todas as abas contra este documento, o fluxo, os textos em português e inglês, Resumo, Histórico, PDF, as pendências da App Store e um teste em celular de verdade.
9. Preparação para a App Store.

**Testes no app que ainda faltam**

- Piso, Azulejo e Esquadrias: prontas e testadas no código; falta Gabriela testar no app.
- Laje nos EUA: no código em Nov 9, 2026; falta a Gabriela colar e testar no app.

## Custos e tabela de preços (feito por último)

- Preços definidos internamente por país e estado, revisados com pesquisa em sites.
- Todo material novo desta especificação precisa de preço por país e estado, sempre por unidade de compra, e precisa aparecer na tela de edição de preços.
- **A tabela de preços é feita por último.** Fonte de referência para o Brasil: SINAPI (Caixa e IBGE, custos por estado, atualizado todo mês) ou os dados dos Sinduscon de cada estado. Para os EUA, outra fonte (a definir). Nos testes gerais, os valores dos preços não são conferidos, só a quantidade de material e a conta quantidade x preço. Quando a tabela nova entrar, os testes automáticos passam a usar preços de teste fixos (os iniciais de hoje), para não quebrar a cada atualização de preço; o app usa sempre a tabela atualizada (decisão da Gabriela, Nov 5, 2026; ver claude/plano_testes.md).
- Os preços provisórios dentro do código (marcados como PROVISÓRIO em cada arquivo de src/calculators/) precisam ser trocados na tabela final: tijolo e bloco por tipo, impermeabilizante (por litro), arame recozido, laje pré-moldada por m², telhas, cumeeira e madeira, conduíte, fios, caixinhas, tomadas e interruptores, tubos, conexões e registros, piso, azulejo, rodapé, argamassa AC-I, AC-II e AC-III, rejunte em lata, tintas, selador, fundo preparador, massa corrida e acrílica, e os insumos de fixação.
- Nos EUA, os preços ainda são os provisórios do Brasil, só que em dólar (ex.: arame a $ 15/kg). Isso se resolve na tabela de preços. Nas Brocas e no Baldrame dos EUA, o texto da tela de preços muda no passo de preços (o preço do cimento vale por saco de 94 lb).
- Laje pré-moldada: vigota, EPS e lajota separados, e tela ou ferro, ficam para a tabela de preços.
- **Para decidir no passo de preços** (rodada 3, Nov 5, 2026): hoje o piso e o azulejo são cobrados pela área com perda (preço por m²), e não pelas caixas inteiras. Cobrar por caixa mudaria também o Brasil.
- **Problemas conhecidos para o passo de preços:** trocar o estado nas Configurações só muda o nome (a tabela por estado do material.py não é usada); os preços iniciais (cimento R$ 36, brita R$ 120) mudam para outra lista (R$ 32 e R$ 95) depois de trocar o país e voltar.

## Versão EUA (o que falta)

**Abas nos EUA que faltam (decisão da Gabriela, Nov 9, 2026).** Nos EUA ficam **16 abas**: as 14 do Brasil, menos o Contrapiso, mais as 3 abas novas da Parte B. O Brasil continua com as suas 14.

| Aba | Nos EUA |
| --- | --- |
| Telhado | Fica, mas muda: shingle asfáltico (sem ripa e caibro). |
| Elétrica | Fica: cabo Romex, sem conduíte e sem os campos de chuveiro elétrico. |
| Hidráulica | Fica: PEX e PVC. |
| Reboco | Fica como stucco, só para a área externa (por dentro, usam drywall). |
| Esquadrias | Fica, com as embalagens americanas. |
| Novas (Parte B) | Estrutura de madeira e Fechamento (OSB) na Estrutura; Drywall no Acabamento. |

**A) Abas que já existem, adaptadas ao padrão americano (EM ANDAMENTO)**

- Sobram **5 abas**: Telhado, Elétrica, Hidráulica, Reboco e Esquadrias, nessa ordem. **Cada aba adaptada já leva junto a lista de compras, o Resumo, o PDF e o WhatsApp dela em unidades americanas** (regra 17: o Resumo igual à aba), para a rodada 7 testar tudo pronto (decisão de Nov 5, 2026). Depois, essas abas são testadas nos EUA em português (rodada 3b) e todas as abas dos EUA juntas em inglês (rodada 4).
- Embalagens americanas (a confirmar na pesquisa): tinta em galões de 1 e 5, fio elétrico (Romex 14/2 e 12/2) em rolos de 250 ft, tubos PEX e PVC em barras de 10 ft.
- Equivalências das abas: Telhado → shingle asfáltico (vendido em fardos, 3 fardos = 1 square = 100 sq ft), além de telha cerâmica/concreto e metálica; Reboco → stucco; Elétrica → Romex e caixas americanas; Hidráulica → PEX e PVC; Esquadrias com embalagens e medidas americanas.
- Os campos de bitola de fio e diâmetro de tubo ainda usam mm (hint_fio, hint_tubo_*); trocam para os padrões americanos junto com esta parte.
- **Elétrica nos EUA:** os campos de chuveiro elétrico somem (decidido em Nov 9, 2026). Nos EUA, chuveiro elétrico quase não existe (lá o aquecimento é central).
- **Reboco nos EUA:** vira stucco, só para a área externa (decidido em Nov 9, 2026).
- **Ainda falta:** os resultados das abas da Parte A que ainda não foram adaptadas continuam em métrico (m³, kg, sacos de 50 kg, barras de 12 m). Eles mudam junto com as embalagens americanas, aba por aba.
- **Para rever na Parte A e na rodada 4 (achado na rodada 2, Nov 5, 2026):** o textos_eua.py ainda tem as embalagens na ordem antiga em inglês ("5 gal buckets", "50 lb bags") e "(ex: ...)" nas dicas em inglês (as das Brocas, do Baldrame, das Paredes e da Laje já foram trocadas por "e.g." em Nov 9, 2026; o hint_vaos em inglês vale também para o Reboco e o Azulejo).
- **Também para a rodada 4 (anotado em Nov 9, 2026; a Gabriela decide):** em inglês americano, "ready-mix" é o concreto do caminhão, e o saco de 80 lb é "concrete mix". Hoje as Brocas, o Baldrame e a Laje dizem "Or ready-mix concrete: X bags of 80 lb", e a Laje diz "Or concrete truck (ready-mix)". Trocar o primeiro (ex.: "Or bagged concrete mix") mexe no inglês das Brocas e do Baldrame.
- Testes: os casos do ferro dos EUA (Brocas e Baldrame), as Paredes e a Laje dos EUA entram na rodada 3b. As Brocas, as Paredes e a Laje nos EUA, a faixa sem o Contrapiso e o aviso do Resumo ainda não estão no pytest: o teste oficial é a Gabriela no app, depois a rodada 3b (as abas da Parte A nos EUA) e a rodada 5 (troca de país).

**B) Abas novas, só nos EUA (casas de madeira, comuns fora do sul)**

- Estrutura de madeira (wood framing): montantes (studs) 2x4 / 2x6, guias (plates), vergas (headers), espaçamento padrão de 16 in.
- Fechamento (sheathing): chapas de OSB 4x8 ft.
- Drywall: chapas 4x8 ou 4x12 ft, massa (joint compound), fita e parafusos.
- Posição (sugestão do Leo, Nov 9, 2026): Estrutura de madeira e Fechamento na etapa Estrutura; Drywall no Acabamento.
- A lista de abas já depende do país (regra 21, feita em Nov 9, 2026): as abas novas entram numa lista parecida com a ABAS_SO_BRASIL (as abas do Brasil continuam iguais).
- Cada aba nova também já entra com a lista de compras, o Resumo, o PDF e o WhatsApp, e com o teste dela nos dois idiomas.

**Antes de codar:** pesquisar as embalagens, os consumos e os padrões americanos (calculadoras de lojas como Home Depot e Lowe's, fabricantes e o código residencial IRC) e marcar como provisório o que não for confirmado. O engenheiro (irmão) conhece o padrão brasileiro; os valores americanos vêm dessa pesquisa.

**Ordem (atualizada em Nov 9, 2026, decisão da Gabriela):** 3) Parte A (EM ANDAMENTO): Telhado, Elétrica, Hidráulica, Reboco e Esquadrias, cada uma com o Resumo, a lista, o PDF e o WhatsApp em unidades americanas; e a rodada 3b; 4) rodada 4 (inglês, todas as abas dos EUA) e rodadas 5 a 8 dos testes; 5) Parte B: abas novas, com o teste delas (pode vir antes das rodadas 5 a 8, a decidir); 6) tabela de preços em dólar (passo de preços).

## Extras que faltam

**PDF e WhatsApp no iPhone:** no iPhone, em vez de abrir o PDF e o WhatsApp, vai usar o botão de compartilhar do sistema.

5. **Cronograma estimado.** Prazo por etapa com base na produtividade média. Deixar por último e sempre marcado como estimativa aproximada. Decidido em Oct 26, 2026: esperar o engenheiro responder as perguntas de produtividade antes de fazer (número errado aqui passa impressão ruim). Ideia: dias de trabalho por aba (quantidade ÷ produtividade), equipe informada pelo cliente (padrão 1 pedreiro + 1 ajudante), resultado por etapa e total em dias úteis e semanas, no Resumo e no PDF.

Respostas do engenheiro para o cronograma (Oct 29, 2026; os números são estimativa):

10. Equipe de 1 pedreiro + 1 ajudante: sim.
11. Brocas: não tem como saber; eles cavam com máquina, não na mão. Ideia do Leo: deixar Brocas fora do prazo, com uma frase explicando (falta a Gabriela decidir).
12. Baldrame: a mesma da 11 (sem número). Mesma ideia: fora do prazo, com uma frase explicando (falta a Gabriela decidir).
13. Paredes: mais ou menos 15 m² por dia.
14. Laje: 3 m² por dia; escoras: no mínimo 21 dias. (O Leo achou baixo; a Gabriela decidiu usar assim mesmo.)
15. Telhado: 2 m² por dia. (O Leo achou baixo; a Gabriela decidiu usar assim mesmo.)
16. Elétrica: talvez uns 10 pontos por dia (ele não sabe muito).
17. Hidráulica: 7 a 8 pontos por dia (usar 7, o menor).
18. Contrapiso: 20 m² por dia.
19. Reboco: 20 m² por dia.
20. Piso e azulejo: 10 m² por dia, já com o rejunte.
21. Pintura: uns 40 m² por dia.
22. Portas e janelas: 7 portas e 7 janelas por dia.
23. Esperas: o reboco espera uns 30 dias antes da pintura. O concreto do baldrame não tem espera (faz o concreto e já assenta o tijolo).
24. Dá pra fazer etapas juntas (ex.: elétrica e hidráulica ao mesmo tempo).
25. 5 dias úteis por semana (sem sábado): sim.

## Suporte (não feito)

Um botão "Fale conosco" com duas opções, sem precisar de servidor. A Apple exige um contato de suporte para publicar.

- **WhatsApp:** número exclusivo do app (WhatsApp Business), nunca o pessoal. Abre com mensagem pronta e já inclui a versão do app e o modelo do celular.
- **E-mail:** abre o app de e-mail do celular com o assunto já preenchido conforme a categoria: Dúvida, Sugestão ou Erro.
- O formulário interno fica para o futuro: como o banco é local (SQLite), a mensagem ficaria no celular do cliente e nunca chegaria até você.

| Onde | Português | Inglês |
| --- | --- | --- |
| Botão | Fale conosco | Contact us |
| Mensagem pronta do WhatsApp | Olá! Uso o HouseSynk (versão \[versão\], \[modelo do celular\]) e quero falar sobre: | Hi! I use HouseSynk (version \[version\], \[device model\]) and I'd like to talk about: |
| Assunto do e-mail: dúvida | Dúvida - HouseSynk | Question - HouseSynk |
| Assunto do e-mail: sugestão | Sugestão - HouseSynk | Suggestion - HouseSynk |
| Assunto do e-mail: erro | Erro - HouseSynk | Bug report - HouseSynk |

## Antes de publicar na App Store (fazer só quando pedir)

- [ ] Mudar o local do orcamentos.db para o user\_data\_dir do Kivy (no iPhone a pasta do app não permite gravação).
- [ ] Trocar o hash das senhas de SHA-256 simples para pbkdf2\_hmac.
- [ ] Escrever a Política de Privacidade (exigida pela Apple, já que o app tem login e guarda dados).
- [ ] Configurar o contato de suporte (WhatsApp exclusivo e e-mail).
- [ ] Assinaturas Plus e Pro pelo sistema de compras da Apple.
- [ ] Gerar a versão final num Mac com Xcode (kivy-ios).
- [ ] PDF no iPhone: trocar o "abrir arquivo" pelo botão de compartilhar do sistema e salvar na pasta de dados do app; conferir se o reportlab funciona no kivy-ios.
- [ ] Conferência final completa (ver a Ordem de trabalho).

Repositório: se quiser deixar a falta de licença explícita, dá para criar um arquivo LICENSE com "Todos os direitos reservados".

## Testes automáticos (o que falta)

- No fim das rodadas, um comando só confere tudo o que dá para testar por código (o visual continua no app).
- Quando uma conta mudar de propósito (ex.: o engenheiro muda um valor), atualizar o esperado em todos os lugares: o test_<aba>.py, o rodada1.py e o rodada2.py (+ testes_rodada1.md e testes_rodada2.md). Texto só do inglês muda o rodada2.py e o testes_rodada2.md. Conta ou texto dos EUA muda o rodada3.py e o testes_rodada3.md.
- **Os arquivos de teste (tests\, pytest.ini, testes_manuais\) ficam só no PC e no GitHub, não no projeto do Claude** (decisão da Gabriela, Nov 4, 2026). Toda mudança de código que mude um resultado: avisar a Gabriela quais testes atualizar (ver claude/plano_testes.md).

## Perguntas para o engenheiro com código ainda para colar

5. A argamassa colante de 3,5 kg por m² vale também para peça grande? Os fabricantes falam em 4 a 5 kg/m² no normal e uns 8 kg/m² em peça grande, porque passa argamassa na peça e no chão (dupla colagem).
   - **Resposta (Oct 29, 2026):** pode usar os números dos fabricantes. **Decisão da Gabriela:** 5 kg/m² na peça normal e 8 kg/m² na peça grande (maior lado acima de 60 cm; confirmar esse tamanho com o engenheiro). Só no Brasil (os EUA continuam pela desempenadeira). Código pronto (revestimento.py e o "?" no comum.py), falta colar no app e testar.

## Decisões em aberto

- Quais abas e recursos cada plano libera (Gratuito, Plus, Pro). Até lá, não implementar nenhuma restrição por plano. Ideia inicial: Gratuito com a Estrutura, Plus com mais etapas, Pro com tudo, PDF e gráficos. Referência de preço (ideia de Nov 2, 2026): assinatura barata, por volta de R$ 19,90 por mês, pensando em profissionais autônomos (MEI); o valor de cada plano ainda vai ser decidido.
- Nome do produto "colinha" usado com o rejunte (fora do app por enquanto, junto com o rejunte em saquinho).
- Valores de referência de preços, a partir da pesquisa no SINAPI (ver Custos).
- Limites criados pelo Leo em Nov 3, 2026 (Laje, Telhado, Elétrica, Hidráulica, Contrapiso, Reboco, Piso, Azulejo, Rejunte, Pintura e Esquadrias) e o do rendimento da Pintura (Nov 5, 2026): a Gabriela mandou (ou vai mandar) para o engenheiro olhar; se ele pedir mudança, é só trocar a constante no arquivo da aba (e o esperado dos testes).
- Parte B dos EUA antes ou depois das rodadas 5 a 8 (decidir quando a rodada 4 acabar).
- Telhado: em inglês, "Timber framing (estimate)" ficou como está (a Gabriela decide se troca para "(estimated)").
- **Mensagens de erro que dizem o campo** (ideia da rodada 2, Nov 5, 2026; a Gabriela decide se vale): "Os valores não podem ser negativos." no Telhado, Elétrica, Hidráulica, Piso e Azulejo não diz qual campo; e o mesmo erro de vãos negativos tem mensagens diferentes em Paredes, Reboco e Azulejo. Mudar mexe em várias abas e nos arquivos das rodadas 1 e 2.

## Ideias para o futuro (depois de publicar)

- **Usar a área das Esquadrias nas Paredes, no Reboco e no Azulejo** (ideia de Nov 3, 2026): a Esquadrias já calcula a "Área total dos vãos"; um botão nessas abas (como o "Usar dados do Piso" do Rejunte), tipo "Usar a área das Esquadrias: 12,09 m²", preencheria o campo de portas e janelas. Cuidado: a Esquadrias vem depois no fluxo, então o botão só aparece se ela já estiver preenchida. Hoje as abas não conversam: o campo de vãos é um número só (m² a descontar) e a Esquadrias é a lista para comprar as portas e janelas.
- Mostrar a data dos preços de referência (ex.: "Valores de referência: outubro/2026"; em inglês "Reference prices: [month/year]").
- Baixar a tabela de preços atualizada da internet, sem publicar versão nova na App Store.
- Backup na nuvem para assinantes Plus e Pro.
- Formulário de suporte interno (exige servidor ou serviço de e-mail).
- Rejunte: tipo em saquinho (pó) e o item complementar "colinha" (deixados de fora por enquanto).
- **Versão site, junto com o app** (ideia de Oct 26, 2026): reaproveitar os cálculos de src/calculators num servidor Python (FastAPI ou Flask) com telas em HTML, CSS e JavaScript. Começar como versão gratuita só com as calculadoras, que convida a baixar o app (histórico, PDF, lista de compras). Ganhar dos dois lados: no site, anúncios ou assinatura própria (Mercado Pago ou Stripe); no app, Plus e Pro pela App Store. Para a assinatura valer nos dois, precisa de login único com servidor. Fazer depois de terminar o app.
- **Perfil profissional no cadastro** (ideia da Gabriela, Nov 2, 2026): no cadastro, a pessoa escolhe quem ela é: dono da obra, pedreiro (ou servente), pintor, eletricista ou encanador. Um app só para todos (decidido não fazer um app separado por profissão: seriam 5 apps para manter e publicar). O perfil pode ser trocado nas Configurações. O que muda com o perfil:
  - **Tela inicial e ordem das abas:** cada profissional abre direto nas abas dele (pintor na Pintura, eletricista na Elétrica, encanador na Hidráulica, pedreiro na Estrutura). As outras abas continuam disponíveis, só ficam depois ou recolhidas. Não precisa de valores de nenhum profissional.
  - **Orçamento para o cliente dele** (a parte mais valiosa, candidata ao plano Pro): o profissional monta o orçamento com os materiais **e a mão de obra dele** (por m², por ponto ou por dia, conforme a profissão), com o nome e o contato dele no PDF e no WhatsApp. O preço da mão de obra é digitado pelo próprio profissional, então não depende de pesquisa de valores.
  - **Editar valores e cálculos** (ideia da Gabriela, Nov 2, 2026), só para os perfis profissionais:
    - **Valores:** os preços de material já são editáveis (Configurar Preços da Região). Entra o preço da mão de obra de cada profissão: pintor por m², eletricista e encanador por ponto, pedreiro por m² ou por dia.
    - **Cálculos:** o profissional pode trocar alguns consumos, os que fazem sentido para a profissão dele (ex.: pintor: rendimento da tinta e demãos; eletricista: metros de fio e de conduíte por ponto; azulejista/pedreiro: kg de argamassa por m²). As fórmulas (ex.: rejunte, massa, concreto) ficam fechadas, para a conta não quebrar.
    - Cada valor tem o botão **"Voltar ao padrão"**.
    - Valor personalizado aparece marcado na tela (ex.: com um ícone), e o PDF avisa que o orçamento usa os valores do profissional, e não os padrão do app.
    - Os valores digitados passam pelos limites com aviso (regra 12, janela "Confira os valores"), para pegar erro de digitação.
  - Precisaria de alguém da profissão só para valores padrão de produtividade e para conferir os textos de cada perfil (os do cronograma já vieram do engenheiro).
  - Fazer depois de publicar o app (depois dos testes e da versão EUA), junto com os planos Plus e Pro.
- **Cadastro de clientes** (ideia de Nov 2, 2026): o profissional guarda os clientes dele (nome e telefone, ex.: "seu Zé") e pode ter vários orçamentos por cliente. Hoje o Histórico já guarda cada orçamento com um nome (ex.: "Casa Ana"); a ideia é esse nome virar um cliente, com o Histórico agrupado por cliente.
- **Contato do profissional no orçamento** (ideia de Nov 2, 2026): nome, telefone/WhatsApp do profissional no cabeçalho do PDF e na mensagem do WhatsApp. Hoje o Resumo e o PDF já mostram o responsável (nome e e-mail, se estiver logado); falta o telefone. Faz parte do perfil profissional.
- **Ordem sugerida pelo Leo para estas ideias** (todas depois de publicar, menos o preço): 1) contato do profissional no PDF e no WhatsApp (pequeno, útil para todos); 2) cadastro de clientes no Histórico; 3) perfil profissional (abas por profissão e mão de obra do profissional); 4) editar valores e cálculos. O preço da assinatura entra antes de publicar, junto com os planos (ver Decisões em aberto).
