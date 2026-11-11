# HouseSynk: O que já foi feito

Cópia das partes já feitas da especificação (claude/especificacao_housesynk.md, atualizada em Nov 9, 2026). O texto é o mesmo da especificação; ficaram de fora só o que ainda falta fazer, as ideias para o futuro, o Suporte e as decisões em aberto. A especificação do projeto não foi alterada.

## Visão geral

App de calculadora de materiais e custos para obras, em Python, preparado para a App Store. Nome do app: **HouseSynk** (decidido em Oct 26, 2026; é o nome do app, não de uma empresa). A refatoração das telas que já existiam, as abas novas, o fluxo por etapas, o Resumo, o PDF e a reserva para imprevistos estão concluídos (faltam alguns testes no app e a conferência final). Agora seguem as funcionalidades extras.

**Nome HouseSynk em tudo (Nov 8, 2026):** o repositório no GitHub é **Gabrielazk/HouseSynk** (até Nov 6, 2026 se chamava BuildCalc), a pasta nos dois PCs é **C:\HouseSynk\HouseSynk** (a pasta do app, com o main.py) e o projeto do Visual Studio é **HouseSynk.slnx** / **HouseSynk.pyproj**. O PC do serviço (antes C:\Calc\Calculadora) mudou em Nov 9, 2026 (1055 passed). Os scripts e os testes acham a pasta do app sozinhos e não têm caminho fixo escrito.

**Repositório público (Nov 9, 2026):** a Gabriela deixou o repositório **público**, como portfólio (para o GitHub e o LinkedIn). Ele não tem licença de propósito: sem licença, todos os direitos ficam com ela (as pessoas podem ver o código, mas não têm permissão para copiar, usar ou vender). Conferido em Nov 9, 2026: nada pessoal vai para o GitHub (o orcamentos.db, o env311 e os arquivos do Visual Studio ficam fora pelo .gitignore).

**Tecnologias**

- Python 3.11
- Kivy + KivyMD 2.x (interface)
- ReportLab (PDF)
- SQLite (banco local, arquivo orcamentos.db, gerenciado pelo database.py)

**Estrutura de arquivos** (pasta HouseSynk, a pasta do app)

- main.py: inicia o app
- src/views/: telas da versão nova (KivyMD 2.x), um arquivo por tela (separadas em Oct 23, 2026):
  - comum.py: o que todas as telas usam (textos PT/EN, configurações, preços, orçamento, formatação). O usuário logado fica em comum.USUARIO_LOGADO; nas telas, sempre ler e trocar por comum.USUARIO_LOGADO. Também tem sistema_unidades() (métrico ou imperial, pelo país) e o txt(), que nos EUA procura primeiro no textos_eua.py.
  - textos_eua.py: os textos que mudam quando o país é EUA (unidades e exemplos americanos), em português e inglês, e a legenda das siglas.
  - rolagem.py: a classe RolagemComBarra, a barra de rolagem usada em todas as telas que rolam (Nov 5, 2026; regra 20).
  - login_screen.py, home_screen.py, calculator_screen.py (todas as abas de cálculo), summary_screen.py (Resumo), history_screen.py (Histórico), settings_screen.py (Configurações).
  - main_screen.py: só o MainScreenManager, que junta as telas.
- src/calculators/: só as contas de cada aba, sem nada de tela (brocas.py, baldrame.py, paredes.py, laje.py, telhado.py, eletrica.py, hidraulica.py, contrapiso.py, reboco.py, revestimento.py com Piso e Azulejo, rejunte.py, pintura.py, esquadrias.py, reserva.py com a reserva para imprevistos, tracos.py com os traços e a conta da massa, unidades.py com a conversão de unidades e a leitura de números com fração, embalagens.py com a conta de embalagens grandes e pequenas)
- src/services/: lista_compras.py (monta a lista de compras somada e por loja, usada pelo Resumo e pelo PDF) e pdf_generator.py (gera o PDF com ReportLab)
- assets/: logo.png (logo com cantos arredondados: janela, login, tela inicial e PDF), icone_app.png (ícone 1024 x 1024 para a App Store) e fonts/ (fonte Liberation Sans do PDF, licença SIL OFL, com o arquivo da licença). O caminho da logo e o nome do app ficam no comum.py (LOGO_APP, NOME_APP).
- database.py: banco, cadastro e login
- requirements.txt: Kivy 2.3.1, KivyMD 2.x (vem do GitHub, não do PyPI) e reportlab 4.2.5
- tests/ (só no PC e no GitHub): tests/abas/ (um test_<aba>.py por aba) e tests/rodadas/ (test_rodada1.py, test_rodada2.py e test_rodada3.py); testes_manuais/ com os roteiros e scripts das rodadas.
- Fora do git (cada PC tem o seu, pelo .gitignore): env311/ (o Python 3.11 e as bibliotecas; quebra se a pasta mudar de lugar e é criado de novo com o requirements.txt), orcamentos.db (os dados de teste), .vs/, __pycache__/ e o HouseSynk.pyproj.user.
- A versão antiga (Calculadora.py, KivyMD 1.x) foi excluída em Nov 8, 2026, porque todas as abas já foram refeitas; ela continua no histórico do git, se for preciso consultar.

**Etapas concluídas da ordem de trabalho**

1. CONCLUÍDO: refatorar as abas que já existiam, no padrão da tela de Brocas: Brocas, Baldrame, Paredes, Contrapiso, Reboco e Revestimento (já dividido em Piso e Azulejo).
2. CONCLUÍDO (Oct 23, 2026): criar as abas novas: Rejunte, Laje, Telhado, Elétrica, Hidráulica, Pintura e Esquadrias.
3. CONCLUÍDO (Oct 23, 2026): fluxo por etapas (etapas clicáveis no topo, Avançar para a próxima etapa).
4. Resumo e PDF (CONCLUÍDO em Oct 26, 2026); reserva para imprevistos e lista por loja feitas.
5. CONCLUÍDO (Oct 28, 2026): ajustes do Brasil com as respostas do engenheiro (Oct 27, 2026), em 5 partes: 1) Brocas e Baldrame; 2) Contrapiso e massa; 3) Piso e Azulejo; 4) Laje com tela soldada; 5) Chuveiros na Elétrica. Todas testadas no app pela Gabriela (Oct 28, 2026).
6. Versão EUA: a camada de unidades está FEITA (Oct 27, 2026) e a Parte 1 (Piso, Azulejo, Rejunte, Pintura e impermeabilização do Baldrame) também (Oct 28, 2026), testada na rodada 3 (Nov 6, 2026). Na Parte A, feitos: o Contrapiso fora dos EUA, as Brocas, o resto do Baldrame e as Paredes (conferidos no app pela Gabriela em Nov 9, 2026) e a Laje (no código em Nov 9, 2026; falta a Gabriela colar e testar no app).
7. Testes gerais: **Rodada 1 (Brasil, português) CONCLUÍDA em Nov 4, 2026**, com as correções de visual (as regras que saíram delas estão nas Regras gerais 12 a 17 e em cada aba). **Rodada 2 (Brasil, inglês) CONCLUÍDA em Nov 5, 2026**, com as 17 pendências corrigidas (as regras que saíram dela estão nas Regras gerais 18 a 20 e em cada aba; resumo em claude/plano_testes.md). **Rodada 3 (EUA, português, as 5 abas da Parte 1) CONCLUÍDA em Nov 6, 2026**: 162 casos OK, com as 9 pendências (P1 a P9, e a P10 pedida pela Gabi) corrigidas; o pytest confere 1055 testes (resumo em claude/plano_testes.md). Em Nov 9, 2026, 18 casos do Baldrame da rodada 3 foram atualizados para o concreto e o ferro dos EUA (Parte A).
   - **Entre a rodada 3 e a Parte A (Nov 6 a 8, 2026):** conferência do GitHub, do projeto do Claude e dos dois PCs (tudo igual) e troca do nome para HouseSynk em tudo.

**Status das abas (Oct 23, 2026)**

- Prontas e testadas: Brocas, Baldrame, Paredes, Contrapiso, Reboco.
- Prontas e conferidas no app pela Gabriela: Rejunte, Laje, Telhado, Elétrica, Hidráulica, Pintura.
- Piso, Azulejo e Esquadrias: prontas e testadas no código; falta Gabriela testar no app.
- Conferência das abas contra este documento feita em Oct 23, 2026; as diferenças decididas estão registradas em cada aba.
- Telas prontas fora do fluxo: Login, Histórico e Resumo. O card do Histórico tem: Visualizar, Resumo (vai direto para o Resumo daquele orçamento), Editar, Duplicar, Renomear e Excluir.
- Testes gerais (rodada 1, Brasil em português): as 14 abas certas nas contas (Nov 3, 2026) e no visual (correções feitas e testadas no app em Nov 3 e 4, 2026). O testes_manuais/rodada1.py tem o resultado esperado de cada caso dentro e diz OK ou DIFERENTE. Ver claude/plano_testes.md.
- Testes gerais (rodada 2, Brasil em inglês): as 14 abas certas nos textos e no visual (Nov 4 e 5, 2026). O testes_manuais/rodada2.py também tem o resultado esperado dos 353 casos dentro. O pytest confere tudo: 893 testes (Nov 5, 2026).
- Testes gerais (rodada 3, EUA em português, Nov 5 e 6, 2026): as 5 abas da Parte 1 certas nas contas e no visual, com 162 casos (roteiro testes_rodada3.md). O testes_manuais/rodada3.py tem o resultado esperado dos 162 casos dentro. O pytest confere tudo: **1055 testes** (Nov 6, 2026).

## Regras gerais

Nenhuma aba é obrigatória: o cliente preenche só o que quiser, e o app nunca trava por falta de dado.

1. **Abas opcionais.** Aba em branco é ignorada, nunca vira zero. Os campos obrigatórios só valem se a pessoa começar a preencher aquela aba.
2. **Valores padrão.** Todo campo opcional já vem preenchido (perda, traço, rendimento). A pessoa altera só se quiser. A nota "Os campos opcionais já vêm com valores padrão..." aparece dentro do diálogo do "?", não solta na tela.
3. **O código atual manda.** Nas abas que já existem, nada que funciona hoje pode sumir na refatoração. Esta especificação é um checklist do que acrescentar.
4. **Massa x argamassa.** Na tela e nos textos, usar os termos populares:
   - **Massa**: preparada na obra (cimento, areia e às vezes cal) para assentar tijolo e para o reboco. O contrapiso é feito de concreto (cimento, areia e brita), não de massa.
   - **Argamassa**: a pronta, de saco, para colar piso e azulejo (AC-I, AC-II, AC-III).
   - Em inglês: massa = *mortar*; argamassa colante = *tile adhesive*.
5. **Unidades de compra.** O resultado sai como se compra: sacos de cimento (50 kg), sacos de cal (20 kg), m³ de areia e brita, milheiro de tijolos, barras de ferro (12 m), caixas de piso, latas e galões de tinta, latas de rejunte.
   - O saco de cimento é sempre de 50 kg e o de cal de 20 kg. As embalagens não são editáveis pelo cliente; o que ele edita é o preço de cada unidade de compra.
   - Os cálculos são feitos sempre em medidas métricas por dentro. Para os EUA, a conversão de unidades e as embalagens locais são uma camada de entrada e saída (ver Versão EUA).
6. **Estimativa.** O app sempre fala em valores estimados, nunca exatos, e mostra o aviso de que não substitui um engenheiro ou arquiteto.
7. **Ajuda em cada aba.** Ícone "?" que abre um MDDialog com o texto de ajuda da aba.
8. **Mão de obra.** Só existe em Brocas e Baldrame (preço por metro, como no app antigo). As outras abas não têm mão de obra.
9. **Concreto.** Densidade do cimento 1500 kg/m³ (fator de volume 1,5, conservador). O traço 1:2:3 dá 7,5 sacos de cimento, 0,50 m³ de areia e 0,75 m³ de brita por m³ de concreto. O contrapiso usa 1:3:3 como padrão (6,4 sacos, 0,64 m³ de areia e 0,64 m³ de brita por m³).
10. **Massa.** Calculada num lugar só (materiais_da_massa, no tracos.py), usada por Paredes, Reboco e chapisco. A areia ganha 25% de inchamento (areia solta e úmida ocupa mais espaço); o cimento e a cal não mudam (decidido com o engenheiro em Oct 27, 2026).
11. **Números digitados.** Os campos aceitam decimal (2,5 ou 2.5) e fração (1/8, 2 1/2 ou 2-1/2), nos dois países. Nos EUA, "1,500" é lido como mil e quinhentos, mas "2,5" continua sendo 2,5. Número inteiro + fração só vale com a fração menor que 1: "2 1/2" vale, "1 21/2" ou "1-21/2" dá a mensagem de erro (é erro de digitação); fração sozinha pode ser maior que 1 ("21/2" = 10,5). Decidido em Oct 28, 2026.
12. **Limites com aviso, nunca com bloqueio** (decidido pela Gabriela em Oct 29, 2026). Pode existir obra de qualquer tamanho (casa, prédio, museu), então passar de um limite não impede a conta. A tela abre a janela "Confira os valores", com o que passou do limite (o valor digitado e o limite) e a pergunta "Deseja continuar mesmo assim?", com os botões Cancelar e Continuar. Continuar guarda o aceite (por aba e com o valor digitado) e calcula; se a pessoa mudar o número, o aviso aparece de novo; o Limpar apaga os aceites da aba. Vale no Calcular e no Finalizar. Os limites ficam como constantes nos arquivos de src/calculators/ (os do engenheiro marcados como confirmados; os outros criados pelo Leo). Zero e número negativo continuam sendo erro. Funções _avisos_pendentes e _pedir_confirmacao no calculator_screen.py, com as ajudantes _aviso_maximo e _aviso_faixa. **Desde Nov 3, 2026, todas as 14 abas têm limites** (ver "Limites com aviso" em cada aba; os criados pelo Leo em Nov 3 o engenheiro ainda vai conferir). A Pintura (demãos acima de 5) deixou de ser erro e também virou aviso. Na Esquadrias, a janela aparece no "Adicionar à lista", antes de o item entrar. Nos EUA, o limite aparece arredondado (ex.: 3 cm = "1 1/8 in") e a conta compara com esse mesmo número (_limite_no_pais), para não aparecer "1 1/8 in: o normal é de 1 1/8 in".
13. **Separador decimal na tela.** No Brasil, todo número quebrado aparece com vírgula, inclusive os traços ("1:0,5:6", "1,5:5:5"); nos EUA, com ponto. Por dentro e no Histórico, o traço continua guardado com ponto ("1:0.5:6"). Perda e espaçamento aparecem sem arredondar, com a função _num_curto. A perda é escrita igual em todas as abas: "(com 2,5% de perda)" (texto label_com_perda, função _txt_perda; em inglês "with 2,5% waste" no Brasil e "with 2.5% waste" nos EUA). No Piso e no Azulejo fica "Área com perda (2,5%, automática)", porque é o nome da área (decidido pela Gabriela em Nov 3, 2026). O separador e a moeda seguem o **país**, não o idioma: no Brasil em inglês continua "2,309 m³" e "R$" (regra 19).
14. **Material com zero não aparece no resultado** (ex.: o traço 1:0:3 não tem cal, então a linha da cal some). Feito em todas as abas em Nov 3, 2026 (funções _linhas_concreto e _linhas_massa). Também somem os zeros do topo da Elétrica e da Hidráulica (ex.: "Pontos de esgoto: 0"), e a Esquadrias mostra "Total: 3 portas e 2 janelas" (com zero, só "Total: 1 porta"). Não tem linha em branco antes dos materiais (a Esquadrias mantém as linhas em branco entre os grupos e, desde Nov 5, 2026, também entre o custo e a frase final).
15. **Menus (dropdowns).** Abrem embaixo do botão, começando na borda esquerda dele, e nunca saem da janela (classe MenuAlinhado no calculator_screen.py, feita em Oct 29, 2026, porque o menu do KivyMD crescia para a esquerda e saía da tela). Menus com largura automática vão até perto da borda da janela, para os nomes compridos não serem cortados. O título de cada menu fica perto do campo de cima e do botão, igual aos títulos de seção.
16. **Números na tela** (correções de Nov 3 e 4, 2026):
   - Separador de milhar em todo número: "2.363 sacos", "100.000,00 m²" (nos EUA "100,000.00"). Funções fmt_num e fmt_int no comum.py.
   - Arredondamento do jeito da escola (5 sobe): função arredondar() no unidades.py, com Decimal (o round() do Python errava: 1,575 virava 1,57). Usada na fmt_num.
   - Plural certo: singular quando a quantidade é maior que 0 e menor que 2 ("1 saco", "0,79 milheiro", "1,58 milheiro"); zero e de 2 para cima, plural. Função _unidade no calculator_screen.py, usada também na lista de compras. Em inglês, as peças ficam "1 pc" e "20 pcs" (chaves un_unidade e un_unidades, un_peca e un_pecas; em português "1 un" e "20 un"), Nov 5, 2026.
   - kg com 1 casa decimal em todos os resultados ("5,6 kg").
   - Número e unidade nunca ficam em linhas diferentes: o Kivy só quebra a linha no espaço comum, e a função sem_quebra() (comum.py) troca o espaço entre o número e a unidade (e entre o "R$" e o valor) por um espaço que não quebra. Só na hora de mostrar (resultado da aba e Resumo); o texto guardado no Histórico, no PDF e no WhatsApp continua normal.
17. **Resumo igual à aba** (regra da Gabriela, Nov 4, 2026): a lista de compras, o PDF e o WhatsApp mostram os materiais com os mesmos nomes e as mesmas casas decimais do resultado da aba. Ex.: "Tijolo baiano (9x19x19): 788 un (0,79 milheiro)" (em inglês, só "788 pcs") e "Argamassa colante AC-I: 13 sacos de 20 kg", com uma linha por tipo (o tipo muda o preço na loja). Orçamento antigo do Histórico, sem o tipo guardado, continua com "Tijolos/Blocos" e "Argamassa colante". No PDF, os títulos das seções nunca ficam sozinhos no fim da página.
18. **Mensagens de erro por chave** (rodada 2, Nov 4, 2026). Os arquivos de src/calculators/ não têm frase de erro: devolvem uma chave (ex.: {"erro": "erro_perda_negativa"}), e a tela mostra a frase no idioma escolhido com o txt() (função _txt_erro no calculator_screen.py). As frases ficam no comum.py, em português e inglês (chaves erro_*); as que só existem nos EUA ficam no textos_eua.py (ex.: erro_espessura_slab, da Laje dos EUA). O "Erro:" (label_erro) e o "c/" dos estribos (label_estribo_cada) também passam pelo txt(): em inglês "Error:" e "@" ("Stirrups 5 mm @ 20 cm"). Os test_<aba>.py conferem a chave, não a frase. Texto novo na tela sempre passa pelo txt(), nunca escrito direto no código.
19. **Inglês do Brasil** (rodada 2, Nov 4 e 5, 2026; vale para os textos "en" do comum.py):
   - Números com vírgula e "R$", porque seguem o país (regra 13), inclusive nos textos fixos (ex.: "5.500 W", "can of 3,6 L").
   - Embalagens na ordem do inglês: "4 rolls of 50 m", "15 bags of 50 kg", "9 lengths of 6 m", "10 panels of 2 x 3 m", "3 tubs of 2 kg". O galão de 3,6 L é "can of 3,6 L" e a lata de 18 L é "pail of 18 L" (em inglês "gallon" tem 3,785 L, parecia erro de conta).
   - Peças: "pc" / "pcs" (regra 16). O milheiro é só do Brasil: em inglês, o tijolo aparece só em peças, sem o parêntese ("788 pcs"; texto un_milheiro vazio e função _txt_milheiros, que só mostra o parêntese quando o idioma tem essa palavra).
   - Nos rótulos dos resultados, só a primeira palavra com maiúscula: "Total volume", "Labor cost", "Estimated stage cost", "Gross area". Botões fora das abas seguem o costume do inglês ("Start Estimate", "Save to History").
   - Nas dicas dos campos, "e.g." no lugar do "ex.:" ("Diameter in cm (e.g. 20)"), decisão da Gabriela.
   - Nomes decididos: "Piles" (Brocas), "Floor screed" (Contrapiso), "Total rebar" (o total do aço), "EPS foam" (o enchimento da laje; Styrofoam é marca), "fittings (estimated)" (Hidráulica), "None" (massa da Pintura). O "?" do Piso e do Azulejo explica que AC-I, AC-II e AC-III são classes brasileiras de argamassa colante.
20. **Barra de rolagem** (pedido da Gabriela, Nov 5, 2026). Todas as telas que rolam (as 14 abas, o Resumo, o Histórico e as Configurações) usam a classe RolagemComBarra (src/views/rolagem.py), que herda do MDScrollView: barra de 6dp que dá para clicar e arrastar com o mouse (scroll_type ["bars", "content"], então continua rolando com o dedo no celular), na cor principal do tema. Parada, a barra fica quase transparente (15%); rolando, aparece forte (90%). O tema vem de App.get_running_app().theme_cls (a rolagem não tem theme_cls no KivyMD 2.x). As Configurações e o Histórico têm 8dp à direita no conteúdo, para a barra não cobrir a borda dos campos. As faixas de etapas e de abas (que rolam de lado) continuam sem barra.
21. **Abas por país** (Nov 9, 2026). Cada país mostra só as abas dele. A lista ETAPAS (calculator_screen.py) continua sendo a do Brasil, completa; ABAS_SO_BRASIL diz o que não existe nos EUA (hoje, só o Contrapiso), e a função etapas_do_pais() monta as etapas do país escolhido (abas_ordem() dá a sequência do Anterior / Próximo e do Finalizar). Uma aba que não existe no país fica guardada (trocar de país e voltar traz os dados de volta), mas não aparece nas faixas, não entra no Finalizar e não entra no Resumo; se a pessoa estava nela ao trocar de país, abre a próxima que existe (Contrapiso → Reboco). Quando uma aba preenchida fica de fora (ex.: orçamento do Histórico com Contrapiso, aberto com o país nos EUA), o Resumo (Orçamento e Lista de compras) avisa no topo: "Atenção: Contrapiso ficou fora deste orçamento, porque essa aba não existe no país escolhido." (texto resumo_abas_fora; em inglês "Note: Floor screed was left out of this estimate, because this tab is not used in the selected country."). O orçamento salvo no Histórico não muda (o Salvar sempre cria um orçamento novo).

**Custos (já existe no app)**

- O cliente pode editar os preços.
- Ao clicar em Calcular, cada aba mostra o seu custo.
- A moeda acompanha o país escolhido (Brasil: real; EUA: dólar). Não converter preços pela cotação. O idioma é escolhido separado do país.
- Enquanto a tabela de preços final não é feita, vários materiais usam preços provisórios dentro do código (marcados como PROVISÓRIO em cada arquivo de src/calculators/): tijolo e bloco por tipo, impermeabilizante (por litro), arame recozido, laje pré-moldada por m², telhas, cumeeira e madeira, conduíte, fios, caixinhas, tomadas e interruptores, tubos, conexões e registros, piso, azulejo, rodapé, argamassa AC-I, AC-II e AC-III, rejunte em lata, tintas, selador, fundo preparador, massa corrida e acrílica, e os insumos de fixação.
- Nos EUA, os preços ainda são os provisórios do Brasil, só que em dólar (ex.: arame a $ 15/kg). Nas Brocas e no Baldrame dos EUA, o preço do cimento (cimento_50kg) vale por saco de 94 lb; areia e brita continuam com preço por m³, e o aço e o arame por kg. Nas Paredes dos EUA, o bloco CMU custa $ 6.00 (o mesmo número do bloco 19x19x39 do Brasil, no paredes.py) e o saco de massa pronta de 80 lb usa o preço do cimento do país (cimento_50kg); a alternativa do cimento de alvenaria não tem preço. Na Laje dos EUA, o cimento e a areia e a brita seguem as Brocas, a base de brita usa o preço da brita por m³, o painel de tela de 5 x 10 ft custa $ 95.00 (o mesmo número do painel de 2 x 3 m do Brasil) e o rolo de lona $ 90.00 (os dois PROVISÓRIOS, no laje.py); o concreto pronto e o concreto usinado não têm preço.

## Fluxo por etapas

Um único fluxo em três etapas, na ordem natural da obra. As etapas ficam clicáveis no topo, então o cliente pode pular qualquer uma.

| Etapa | Abas que já existiam (refatoradas) | Abas novas |
| --- | --- | --- |
| 1. Estrutura | Brocas, Baldrame, Paredes | Laje, Telhado |
| 2. Instalações | (nenhuma) | Elétrica, Hidráulica |
| 3. Acabamento | Contrapiso, Reboco, Piso, Azulejo | Rejunte, Pintura, Esquadrias |

Nos EUA, o Contrapiso não aparece (regra 21).

**Topo da calculadora**

- Linha das etapas ("1. Estrutura", "2. Instalações", "3. Acabamento"): a etapa atual fica destacada (botão preenchido). Tocar numa etapa abre a primeira aba dela.
- Linha das abas: mostra só as abas da etapa atual, com a aba aberta destacada. A faixa rola sozinha até a aba aberta.
- No código, a lista ETAPAS (início do calculator_screen.py) define as etapas e a ordem das abas; aba nova entra na etapa dela e as barras e os botões se ajustam sozinhos. As faixas e os botões usam etapas_do_pais() (regra 21).

**Botões**

- **Calcular** (em cada aba): mostra materiais e custo daquela aba.
- **Próximo**: em todas as abas, menos na última de cada etapa.
- **Anterior**: em todas as abas, menos na primeira (Brocas). Na primeira aba de uma etapa, volta para a última aba da etapa anterior.
- **Limpar** (em cada aba): apaga só aquela aba, com confirmação.
- **Avançar para a próxima etapa**: na última aba de cada etapa (Telhado e Hidráulica), no lugar do Próximo, numa linha própria acima do Finalizar. Esquadrias (última aba do app) não tem Próximo nem Avançar.
- **Finalizar** (em todas as abas): vai direto para o Resumo com o que foi preenchido até ali. Aba em branco é ignorada.

## Abas prontas

Cada aba segue o mesmo modelo: campos obrigatórios, campos opcionais com valor padrão, resultado em unidade de compra e materiais que precisam de preço. Os valores marcados como confirmados vieram do engenheiro (irmão da Gabriela) em Oct 27, 2026; o resto continua provisório.

### Etapa 1: Estrutura

**Brocas** (pronta; aprovada nos testes gerais em Oct 28, 2026)

- Em inglês, a aba se chama **"Piles"** (Nov 5, 2026: antes "Drilled Shafts", que misturava com o "pile" do resultado).
- Obrigatórios: quantidade de brocas; diâmetro (cm); profundidade média (m).
- Opcionais: traço do concreto (padrão 1:2:3); perda (padrão 10%); armadura: quantidade de ferros, bitola e espaçamento dos estribos; mão de obra por metro.
- Armadura (confirmado): bitolas 6,3, 8, 10, 12,5 e 16 mm (padrão 8 mm); barras de 12 m; estribo de 5 mm a cada 20 cm, em **espiral** (um fio contínuo; cada volta = hipotenusa entre a circunferência interna e o passo, mais um gancho em cada ponta); cobrimento de **3 cm** (resposta do engenheiro de Oct 29, 2026: de 3 a 5 cm; a Gabriela escolheu 3 cm; COBRIMENTO_CM = 3.0 no brocas.py, já no app; o Baldrame usa o mesmo); gancho de **5 cm**; **4 barras** longitudinais (é o exemplo do campo); perda do ferro de **10%**.
- **A gaiola de ferro vai até a metade da profundidade** (confirmado; FRACAO_GAIOLA_BROCA = 0,5 no brocas.py). O concreto continua sendo a broca inteira; só o ferro em pé e o estribo usam a metade. O resultado mostra a linha "Gaiola de ferro: X m de cada broca".
- Arame recozido (só com armadura): 2% do peso do aço (confirmado).
- **Limite com aviso (regra 12):** profundidade acima de 30 m (confirmado pelo engenheiro em Oct 28, 2026; PROFUNDIDADE_MAXIMA_M no brocas.py).
- Resultado: volume total das brocas m³ de concreto, sacos de cimento, m³ de areia, m³ de brita, barras de ferro, kg de arame. O total do aço é "Aço/Ferragem" / "Total rebar".
- Preço: cimento, areia, brita, ferro por bitola, arame.
- **Nos EUA** (Parte A, Nov 9, 2026; conferido no app pela Gabriela): ver "Brocas nos EUA" na seção Versão EUA.

**Baldrame** (pronta; aprovada nos testes gerais em Oct 29, 2026)

- Obrigatórios: comprimento total das vigas (m); largura (cm); altura (cm).
- Opcionais: traço (padrão 1:2:3); perda (padrão 5%, confirmado); armadura: quantidade de barras, bitola e espaçamento dos estribos (no lugar de "taxa de aço"); impermeabilização (sim ou não); mão de obra por metro.
- Armadura: estribos retangulares de 5 mm; cobrimento de 3 cm, gancho de 5 cm e perda do ferro de 10% (os mesmos valores das Brocas). Quantidade de estribos: um a cada espaçamento, mais o da ponta (com a mesma folguinha das barras desde Nov 9, 2026: 100 ft com estribo a cada 6 in dava 200, e não 201; o Brasil não mudou).
- **Traspasse (emenda):** quando a viga passa de 12 m, cada barra ganha uma emenda a cada 12 m, de 40 vezes a bitola (ferro de 8 mm = 32 cm). O engenheiro deixou a escolha com a gente; 40 vezes é a regra mais usada. O resultado do ferro mostra "(inclui X m de emendas)".
- **Impermeabilização:** tinta asfáltica (o engenheiro usa Neutrol). Área = comprimento x (largura + 2 x altura), 2 demãos de 0,4 L/m² (o fabricante indica de 0,4 a 0,5 L/m²). Resultado em litros e em baldes de 18 L e galões de 3,6 L (do jeito que sobra menos, igual à tinta). Preço por litro (provisório), sobre os litros das embalagens compradas.
- Arame recozido (só com armadura): igual à Broca.
- **Limite com aviso (regra 12):** viga com largura menor que 20 cm ou altura menor que 30 cm (confirmado pelo engenheiro em Oct 28, 2026; LARGURA_MINIMA_CM e ALTURA_MINIMA_CM no baldrame.py). O comprimento não tem máximo ("depende da obra", resposta do engenheiro). Nos EUA continua o mínimo do Brasil convertido, 8 x 12 in (decisão da Gabriela, Nov 9, 2026).
- Zero ou número negativo: "Comprimento, largura e altura devem ser maiores que zero." (chave erro_valores_zero; antes "Valores devem ser maiores que zero.", que não dizia o campo; Nov 5, 2026).
- Resultado: volume total do baldrame m³ de concreto, sacos de cimento(50kg), m³ de areia e brita, barras de ferro, arame, impermeabilizante.
- Preço: os da Broca + impermeabilizante por litro.
- **Nos EUA** (Parte A, Nov 9, 2026; conferido no app pela Gabriela): ver "Baldrame nos EUA" na seção Versão EUA.

**Paredes (alvenaria)** (pronta; aprovada nos testes gerais em Oct 29, 2026)

- Obrigatórios: área bruta das paredes, sem descontos (m²); tipo e tamanho do tijolo ou bloco (uma lista só, com o tamanho no nome: tijolo baiano 9x19x19, tijolo baiano 9 furos 9x14x19, bloco de concreto 9x19x39, 14x19x39 e 19x19x39); assentamento (em pé ou deitado: é só a direção em que o tijolo é assentado).
- Opcionais: desconto de vãos de portas e janelas (m²); espessura da junta (padrão 1 cm); quebra de tijolos (padrão 5%); traço da massa (padrão 1:2:8, cimento, cal e areia; as opções de traço vêm do app antigo).
- A massa é calculada pela geometria: tijolos por m² considerando a junta, e o volume de massa é o espaço que sobra entre os tijolos. Os materiais da massa vêm da mesma conta do Reboco (regra 10), com a areia +25%.
- **Perda da massa de assentar: 10%** (decidido pela Gabriela em Oct 29, 2026, igual ao reboco; PERDA_MASSA_PERCENTUAL no paredes.py). Não é um campo da tela: entra sempre, igual à perda do ferro.
- **Limites com aviso (regra 12),** criados pelo Leo em Oct 29, 2026 (o engenheiro não tinha um número): área até 2000 m²; junta de 0,5 a 3 cm; quebra até 20% (no paredes.py).
- Desconto de vãos igual ou maior que a área: "O desconto de vãos deve ser menor que a área." (o mesmo texto no Reboco e no Azulejo, Nov 4, 2026).
- Resultado: área total da parede m² (a "Área líquida" só aparece quando tem vãos, igual ao Reboco e ao Azulejo), tijolos (unidades e milheiros; em inglês só as peças, "788 pcs", regra 19), sacos de cimento(50kg) e de cal(20kg), m³ de areia (o que der zero não aparece, regra 14).
- Preço: tijolo ou bloco por tipo, cimento, cal, areia.
- A quantidade de tijolos tem a mesma folguinha das barras desde Nov 9, 2026 (math.ceil(... - 1e-9)); o Brasil não mudou.
- **Nos EUA** (Parte A, Nov 9, 2026; conferido no app pela Gabriela): ver "Paredes nos EUA" na seção Versão EUA.

**Laje** (pronta; tela soldada feita em Oct 28, 2026)

- Obrigatórios: área (m²); tipo (pré-moldada treliçada ou maciça; padrão pré-moldada).
- Pré-moldada, opcionais: tipo de enchimento (EPS/isopor ou lajota cerâmica; padrão isopor; em inglês "EPS foam"); espessura da capa de concreto (padrão 4 cm).
- Maciça, obrigatório: espessura total (cm).
- Opcionais: traço (padrão 1:2:3); perda (padrão 5%).
- Ao trocar o tipo, a aba mostra os campos daquele tipo, sem perder o que já foi digitado.
- Pré-moldada (confirmado): concreto = capa + 1,2 cm por m² entre as vigotas; lajotas: 12 por m².
- **Tela soldada na capa** (só na pré-moldada; sim ou não, padrão não): a família do engenheiro usa mais a tela soldada; outros usam ferro. Resultado em painéis de 2 x 3 m (o tamanho vendido nas lojas, ex.: Malha POP Gerdau, tipos Leve ou Médio para laje de casa), com 10% a mais para a sobreposição (confirmado pelo engenheiro em Oct 29, 2026). Ex.: 50 m² = 55 m² = 10 painéis. Preço provisório por painel. Aparece na lista de compras (Material básico).
- Não incluir "carga de projeto": é cálculo estrutural, trabalho de engenheiro.
- **Limites com aviso (regra 12),** criados pelo Leo em Nov 3, 2026 (o engenheiro ainda vai conferir): área até 2000 m²; capa de 3 a 8 cm (só na pré-moldada); espessura da maciça de 8 a 20 cm (no laje.py).
- Resultado: área m², volume total de concreto m³, m² de laje pré-moldada (vigotas + enchimento) e quantidade de lajotas, painéis de tela soldada (se marcada), sacos de cimento(50kg), m³ de areia e brita.
- Preço: por enquanto a laje pré-moldada tem preço por m² (vigotas + enchimento, como as lojas costumam vender), além de cimento, areia e brita.
- **Nos EUA** (Parte A, no código em Nov 9, 2026; falta a Gabriela testar no app): vira o piso de concreto no chão (slab-on-grade). Ver "Laje nos EUA" na seção Versão EUA.

**Telhado** (pronta)

- Obrigatórios: área do telhado em planta (m², vista de cima, com os beirais); tipo de telha (cerâmica, concreto ou fibrocimento; padrão cerâmica).
- Opcionais: inclinação (%, padrão conforme o tipo de telha: 30% cerâmica e concreto, 15% fibrocimento; muda sozinha ao trocar a telha, se a pessoa não tiver mexido); cumeeira (m); madeiramento (sim ou não, padrão não); perda (padrão 5%).
- O app corrige a área pela inclinação (área real = área em planta x √(1 + inclinação²)).
- Telhas por m² (confirmado): cerâmica 16 (tipo romana), concreto 10,5, fibrocimento 1 telha de 2,44 x 1,10 m a cada 2,4 m². Cumeeira: 3 peças por metro (1 no fibrocimento).
- Madeiramento por m² (confirmado): 3 m de ripa, 2 m de caibro e 0,6 m de terça; fibrocimento só terças (0,8 m/m²).
- O "?" explica o que é a cumeeira (linha do alto, onde as águas se encontram; no telhado de quatro águas, somar as quinas; telhado de uma água não tem).
- **Limites com aviso (regra 12),** criados pelo Leo em Nov 3, 2026 (o engenheiro ainda vai conferir): área até 2000 m²; inclinação até 100% (no telhado.py).
- Resultado: área do telhado, quantidade de telhas, peças de cumeeira, metros de ripas, caibros e terças. Em inglês, "Timber framing (estimate)" ficou como está (a Gabriela decide se troca para "(estimated)").
- Preço: telha por tipo, cumeeira, madeiramento (por metro de ripa, caibro e terça).

### Etapa 2: Instalações (sempre como estimativa)

**Elétrica** (pronta; chuveiros feitos em Oct 28, 2026)

- Obrigatórios: quantidade de tomadas, interruptores, pontos de luz e chuveiros elétricos (pelo menos um maior que zero).
- Opcionais ("Metragens do projeto"): conduíte (m) e fios de 1,5, 2,5, 4 e 6 mm² (m), para quem já tem o projeto; perda (padrão 10%). Campo vazio é estimado pelo app; cada linha do resultado diz "(estimado)" ou "(do projeto)".
- Estimativa por ponto (confirmado): 5 m de conduíte por ponto; tomada 15 m de fio 2,5 mm²; interruptor e ponto de luz 10 m de fio 1,5 mm².
- **Chuveiros elétricos** (campo aprovado pelo engenheiro): cada chuveiro tem um circuito só dele, saindo do quadro de luz. 30 m de fio por chuveiro (3 fios de uns 10 m: 2 fases ou fase e neutro, mais o terra) e 10 m de conduíte (confirmado pelo engenheiro em Oct 29, 2026). Dois campos: "acima de 5.500 W" (fio de 6 mm²) e "até 5.500 W" (fio de 4 mm²). Se o fio ou o conduíte vierem do projeto, o projeto manda. Ex.: 2 chuveiros acima de 5.500 W = 66 m de fio de 6 mm² e 22 m de conduíte, com 10% de perda. Em inglês também com ponto no milhar no Brasil (regra 19).
- **Limites com aviso (regra 12),** criados pelo Leo em Nov 3, 2026 (o engenheiro ainda vai conferir): até 300 tomadas, 300 interruptores e 300 pontos de luz; até 10 chuveiros, somando os dois campos (no eletrica.py).
- Resultado: conduítes (m e rolos de 50 m), fios por bitola (m e rolos de 100 m), caixinhas 4x2 (uma por tomada ou interruptor), caixas octogonais (uma por ponto de luz), tomadas e interruptores. No topo, as quantidades com zero não aparecem.
- Preço: conduíte, fio por bitola, caixinha, caixa octogonal, tomada, interruptor.

**Hidráulica** (pronta)

- Obrigatórios: pontos de água fria, água quente e esgoto (pelo menos um maior que zero; ponto é cada saída: torneira, chuveiro, vaso, ralo, máquina).
- Opcionais ("Metragens do projeto"): metragem de cada tubo (m), para quem já tem o projeto; perda (padrão 10%). Campo vazio é estimado pelo app. As dicas dos campos de tubo terminam com "(opcional)", igual às da Elétrica (Nov 4, 2026).
- Tubos: água fria PVC 25 mm (barras de 6 m), água quente CPVC 22 mm (barras de 3 m; o engenheiro confirmou CPVC), esgoto PVC 40 mm e 100 mm (barras de 6 m).
- Estimativa por ponto (confirmado): água fria 4 m; água quente 5 m; esgoto 3 m de 40 mm + 2 m de 100 mm. Conexões: 4 por ponto de água, 3 por ponto de esgoto. Registros de gaveta: 1 a cada 4 pontos de água.
- **Limite com aviso (regra 12),** criado pelo Leo em Nov 3, 2026 (o engenheiro ainda vai conferir): até 200 pontos de cada tipo (no hidraulica.py).
- Resultado: tubos por diâmetro (m e barras; em inglês "lengths of 6 m"), conexões estimadas (em inglês "fittings (estimated)"), registros. No topo, os pontos com zero não aparecem.
- Preço: tubo por diâmetro (por barra), conexão, registro.

### Etapa 3: Acabamento

**Contrapiso** (pronta; só no Brasil desde Nov 9, 2026, regra 21)

- Em inglês, a aba se chama **"Floor screed"** (Nov 5, 2026: "Subfloor" lembra a base de madeira compensada, não contrapiso de cimento).
- **Não existe nos EUA** (decisão da Gabriela, Nov 9, 2026): na casa americana, o piso vai direto sobre a slab ou sobre o OSB do piso, e o contrapiso de concreto como no Brasil é raro (pesquisa de embalagens, item 8). No Brasil em inglês continua aparecendo como "Floor screed".
- Obrigatórios: área (m²); espessura média (cm; normalmente 5 a 7 cm).
- Opcionais: traço do concreto (**padrão 1:3:3**, cimento, areia e brita, confirmado; constante TRACO_PADRAO_CONTRAPISO no contrapiso.py); perda (padrão 5%).
- **Limites com aviso (regra 12),** criados pelo Leo em Nov 3, 2026 (o engenheiro ainda vai conferir): área até 2000 m²; espessura de 3 a 10 cm (no contrapiso.py).
- Resultado: área m², espessura média (ex.: "Espessura média: 5 cm", Nov 4, 2026), volume total de contrapiso m³ de concreto, sacos de cimento(50kg), m³ de areia e brita.
- Preço: cimento, areia, brita.

**Reboco** (pronta)

- Obrigatórios: área (m²); espessura (padrão 2 cm); traço da massa (padrão 1:2:8, cimento, cal e areia).
- Opcionais: desconto de vãos (m²); rebocar os dois lados (sim ou não, dobra a área); chapisco (sim ou não, traço 1:3 de cimento e areia, camada de 0,5 cm, confirmado); perda (padrão 10%).
- Cimento: cerca de 2,7 kg/m² num reboco de 2 cm no traço 1:2:8 (confirmado). A areia ganha +25% (regra 10).
- **Limites com aviso (regra 12),** criados pelo Leo em Nov 3, 2026 (o engenheiro ainda vai conferir): área até 2000 m²; espessura de 0,5 a 4 cm (no reboco.py).
- Resultado: área m² (a "Área líquida" só com vãos), espessura (ex.: "Espessura: 2 cm", Nov 4, 2026), volume total do reboco m³, sacos de cimento(50kg) e de cal(20kg), m³ de areia.

**Piso** (pronta no código; Parte 3 feita em Oct 28, 2026)

- Obrigatórios: área (m²); tamanho da peça em dois campos, largura e altura (cm).
- Opcionais: m² por caixa; assentamento com desenho (sim ou não); perda (vazia = automática); tipo de argamassa (padrão AC-I); rodapé (m); tamanho de cada peça do rodapé (m).
- Resultado: peças (ex.: "Peças: 123"), caixas de piso (só se os m² por caixa forem informados; escrito "Caixas: 21 (2,16 m² por caixa)", sem repetir a palavra, Nov 5, 2026), sacos de argamassa (20 kg), metros e peças de rodapé. Quando o assentamento é com desenho, aparece "Assentamento: com desenho" (Nov 4, 2026).
- A argamassa é resultado, não entrada. O tipo (AC-I, AC-II ou AC-III) só muda o preço. Em inglês, o "?" explica que são classes brasileiras de argamassa colante (AC-III para áreas molhadas).
- Argamassa colante (confirmado): **3,5 kg/m² para qualquer tamanho de peça** (antes: 5 kg/m², ou 8 kg/m² acima de 0,9 m²), mais a perda.
- Perda pelo tamanho da peça (confirmado; maior lado): até 70 cm, 10%; de 70 a 90 cm, 15%; acima de 90 cm, 20%; assentamento com desenho (diagonal ou paginado), 25%. O campo de perda começa vazio: vazio = automática (o resultado mostra "automática"); se o cliente digitar, vale o que ele digitou. Função perda_automatica no revestimento.py. Nos EUA, o "?" mostra essas faixas em polegadas: até 27 1/2 in, até 35 3/8 in e acima disso (rodada 3, P2, Nov 5, 2026).
- Rodapé: o tamanho da peça varia, então é um campo do cliente (m). Se ficar vazio, o app mostra só os metros. O rodapé usa 10% de perda (ou a perda digitada).
- Dica: se a área do Contrapiso já foi digitada, aparece um botão "Usar a área do Contrapiso" para preencher a área do Piso. Nos EUA o botão não aparece, porque lá não tem Contrapiso (Nov 9, 2026).
- O rejunte não é mais calculado aqui; ele fica na aba Rejunte.
- **Limites com aviso (regra 12),** criados pelo Leo em Nov 3, 2026 (o engenheiro ainda vai conferir), iguais no Piso e no Azulejo: área até 2000 m²; peça de 5 a 300 cm em cada lado (existe porcelanato de 120 x 240; no revestimento.py).
- Preço: piso por m² ou caixa, argamassa por tipo, rodapé.

**Azulejo** (pronta no código; Parte 3 feita em Oct 28, 2026)

- Obrigatórios: área de parede (m²); tamanho da peça em dois campos, largura e altura (cm).
- Opcionais: desconto de vãos (m²); m² por caixa; assentamento com desenho (sim ou não); perda (vazia = automática); tipo de argamassa (padrão AC-II; AC-III para áreas molhadas).
- Resultado: peças, caixas de azulejo (só se os m² por caixa forem informados; "Caixas: 21 (2,16 m² por caixa)", igual ao Piso), sacos de argamassa. Com desenho, aparece "Assentamento: com desenho".
- Mesmas regras de argamassa, de perda e de limites do Piso. O rejunte fica na aba Rejunte.
- Preço: azulejo, argamassa por tipo.

**Rejunte** (pronta)

- Se Piso ou Azulejo já foram preenchidos, aparecem no topo da aba os botões "Usar dados do Piso" e "Usar dados do Azulejo" (área, já sem os vãos no Azulejo, e tamanho da peça); ao tocar, a área e a peça são preenchidas. O cliente também pode preencher do zero (ex.: refazer o rejunte de um piso existente).
- Obrigatórios: área (m²); tamanho da peça (largura e altura, cm); largura da junta (mm, sem valor padrão).
- Opcionais: espessura da peça (padrão 8 mm, confirmado); perda (padrão 10%).
- Cálculo: fórmula dos fabricantes, kg/m² = ((C + L) / (C x L)) x junta x espessura x densidade (C e L da peça em mm; densidade 1,58 kg/dm³, confirmada). Decidido usar a fórmula, e não a tabela consumo_rejunte do app antigo.
- Embalagem: latas de 1 kg e 2 kg; o app usa o máximo de latas de 2 kg e completa com uma de 1 kg se sobrar.
- **Limites com aviso (regra 12),** criados pelo Leo em Nov 3, 2026 (o engenheiro ainda vai conferir): área até 2000 m²; junta de 1 a 15 mm (junta de 30 mm é quase certeza de quem digitou em cm; no rejunte.py).
- Resultado: numa linha só, igual à Pintura: "• Rejunte (com 10% de perda): 5,6 kg = 3 latas de 2 kg (R$ 54,00)" (Nov 4, 2026).
- Preço: rejunte em lata de 1 kg e de 2 kg.

**Pintura** (pronta)

- Obrigatórios: área de parede (m²) e/ou área de teto (m²), basta uma das duas (regra 1: o app nunca trava); número de demãos (padrão 2).
- Opcionais: rendimento da tinta (padrão 12 m² por litro por demão, confirmado, editável); complementos: selador (sim ou não), massa (não, massa corrida para área interna seca, ou massa acrílica para área externa ou úmida; em inglês "None · Wall putty · Acrylic putty"), fundo preparador (sim ou não); perda (padrão 10%).
- Complementos (confirmado): uma demão sobre a área total (parede + teto). Selador 8 m²/L, fundo preparador 10 m²/L, massa 0,5 kg/m² por demão, em 2 demãos (1,0 kg/m² no total), em baldes de 25 kg.
- Compra: latas de 18 L + galões de 3,6 L, do jeito que sobra menos; com 5 galões ou mais, o app troca por mais uma lata. Em inglês: "pail of 18 L" e "can of 3,6 L" (regra 19).
- **Limites com aviso (regra 12):** demãos até 5 (antes era erro; virou aviso em Nov 3, 2026, confirmado pela Gabriela); área de parede e de teto até 5000 m² cada (criado pelo Leo; a pintura conta os dois lados da parede e o teto). No pintura.py. **Rendimento** (rodada 3, P8, aprovado pela Gabriela em Nov 5, 2026; criado pelo Leo, a Gabriela vai mandar para o engenheiro): de 4 a 20 m²/L no Brasil e de 150 a 800 sq ft/gal nos EUA (pega quem digita 12, o número do Brasil, nos EUA). Texto: "Rendimento de {valor}: o normal é de {min} a {max}." (feito em Nov 6, 2026).
- Resultado: latas (18 L) e galões (3,6 L) de tinta de parede e de teto, selador e fundo; baldes de massa. "Demãos" e "Rendimento" do topo valem só para as tintas; quando tem complemento, aparece a nota "Complementos (sobre parede + teto): Selador 1 demão, Fundo preparador 1 demão, Massa corrida 2 demãos" (só os marcados; Nov 4, 2026).
- Preço: tinta de parede, tinta de teto, selador, massa corrida, massa acrílica, fundo preparador.

**Esquadrias** (pronta)

- Obrigatórios: lista de portas e janelas, com quantidade, largura e altura do vão (cm). O cliente escolhe o tipo e o material, digita as medidas e toca em "Adicionar à lista"; cada item tem um X para remover; itens iguais são somados. Se digitar e não adicionar, o app avisa.
- Opcionais: material (não informado, alumínio, madeira, vidro temperado), só como informação; insumos de fixação, cada um sim ou não: espuma expansiva, parafusos com bucha, argamassa de fixação.
- Insumos pelo contorno dos vãos (porta: dois lados + parte de cima; janela: os quatro lados): espuma 1 tubo de 500 ml a cada 6 m e parafusos 1 a cada 40 cm (os dois aprovados pelo engenheiro em Oct 29, 2026); argamassa 1,5 kg/m em sacos de 20 kg (provisório: o engenheiro não sabe).
- As medidas da lista ficam guardadas sempre em cm; nos EUA aparecem em polegadas.
- **Limites com aviso (regra 12),** criados pelo Leo em Nov 3, 2026 (o engenheiro ainda vai conferir): até 100 de cada item; largura até 500 cm; altura até 400 cm (8000 é quase certeza de quem digitou em mm). A janela aparece no "Adicionar à lista", antes de o item entrar; Continuar adiciona.
- Resultado: lista organizada para cotação (portas e janelas, com área de cada uma, "Total: 3 portas e 2 janelas" e área total dos vãos), insumos de fixação. O app não tem preço de porta e janela (varia muito): no fim aparece "Portas e janelas: use esta lista para pedir orçamento ao fornecedor.", separada do custo por uma linha em branco (Nov 5, 2026). Sem insumo, essa frase fica no lugar do "Custo Estimado da Etapa: R$ 0,00" (que parecia que as portas eram de graça); no WhatsApp, a Esquadrias sem custo aparece "peça orçamento ao fornecedor" (Nov 4, 2026).
- Preço: insumos de fixação.

## Versão EUA: o que já foi feito

**País e idioma são escolhas separadas.** "EUA" é o país: ele decide as unidades (ft, lb, sq ft), as embalagens e as abas. O idioma (português ou inglês) é outra escolha, nos dois países. As abas dos EUA são as mesmas nos dois idiomas.

**Abas nos EUA já resolvidas (decisão da Gabriela, Nov 9, 2026)**

| Aba | Nos EUA |
| --- | --- |
| Brocas | Fica (piers, muito usados). Feita em Nov 9, 2026. |
| Baldrame | Fica (grade beam / footing), com o ferro e as embalagens americanas. Feito em Nov 9, 2026. |
| Paredes | Fica, só com bloco de concreto (CMU) 8x8x16, comum no sul e na fundação. Feita em Nov 9, 2026. |
| Laje | Fica, mas muda: a pré-moldada com isopor não existe lá; vira o piso de concreto no chão (slab-on-grade). Feita no código em Nov 9, 2026. |
| Contrapiso | **Sai** (quase não se faz lá; regra 21). Feito em Nov 9, 2026. |
| Piso, Azulejo, Rejunte, Pintura | Ficam (já adaptadas na Parte 1). |

**Camada de unidades (FEITA, Oct 27, 2026)**

- src/calculators/unidades.py: conversões com fatores exatos (para_metrico, do_metrico, nome_unidade), leitura de números com fração (ler_numero) e polegadas escritas em fração (texto_polegadas, até 1/16 in).
- Na tela, as unidades aparecem só com a sigla americana (ft, in, sq ft, cu yd, lb, gal), nos dois idiomas, para o campo ficar curto.
- Os textos que mudam nos EUA (unidades e exemplos americanos) ficam em src/views/textos_eua.py, no dicionário TEXTOS_EUA. O txt() do comum.py procura nele primeiro quando o país é EUA; o Brasil não muda.
- Quando o país for EUA e o idioma português, o "?" de cada aba mostra no fim a legenda: "Siglas: ft = pés · in = polegadas · sq ft = pés quadrados · cu yd = jardas cúbicas · lb = libras · gal = galões".
- No calculator_screen.py, UNIDADE_CAMPO diz a unidade de cada campo (ft no lugar de m; in no lugar de cm e mm; sq ft no lugar de m²; sq ft/gal no lugar de m²/L; $ por ft na mão de obra). Antes da conta, _estado_metrico converte o que foi digitado para métrico. Quantidades, perdas, barras, inclinação, demãos e pontos não mudam.
- Valores padrão aparecem arredondados nas unidades de lá: estribo 8 in, junta 3/8 in, reboco 3/4 in, capa 1 5/8 in, espessura da laje dos EUA 4 in, espessura da peça 5/16 in, rendimento 400 sq ft/gal.
- No Histórico, as medidas são salvas sempre em métrico e voltam convertidas ao abrir nos EUA.
- Trocar o país com abas preenchidas converte o que já foi digitado (ex.: 3 m vira 9.843 ft) e apaga os resultados antigos.
- Os avisos de limite (regra 12) mostram o valor e o limite nas unidades do país (ex.: viga mínima 8 in x 12 in).
- Testado em Oct 27, 2026: 10 brocas de 12 in com 10 ft dão 2,446 m³ (com 10% de perda) e $ 8 por ft em 100 ft dão $ 800.
- **Medidas digitadas repetidas no resultado** (rodada 3, feito em Nov 6, 2026): o que a pessoa digitou volta na unidade do país e em fração: peça "12 x 12 in" (com espaço só nos EUA; no Brasil continua "60x60 cm"), junta e espessura em fração até 1/32 in, "Mão de Obra: 40.0 ft", "Estribos 5 mm c/ 8 in" (pendências P6 e P7 da rodada 3, corrigidas no Baldrame, no Piso, no Azulejo e no Rejunte).

**Parte 1 (FEITA, Oct 28, 2026):** Piso, Azulejo, Rejunte, Pintura e a impermeabilização do Baldrame, com as embalagens da pesquisa (claude/pesquisa_embalagens_eua.md). Testada na rodada 3 (concluída em Nov 6, 2026).

**Parte A: abas já feitas**

- Decisões da Gabriela para a Parte A (Nov 9, 2026): usar o padrão americano da pesquisa no ferro (cobrimento de 3 in, bitolas #3, #4 e #5, barras de 20 ft, arame em rolos de 3,5 lb) e mostrar também a linha "Ou concreto pronto: X sacos de 80 lb" nas abas de concreto. A Gabriela já tinha autorizado (out/2026) aplicar tudo o que vem da pesquisa, desde que fique igual às fontes.
- **Brocas nos EUA (feito em Nov 9, 2026; conferido no app pela Gabriela):**
  - A conta é a mesma do Brasil (em métrico por dentro), com o padrão americano no ferro: cobrimento de **3 in** (7,62 cm, código IRC R403.1.3, concreto contra a terra), bitolas **#3, #4 e #5** (padrão #4; o número é o diâmetro em oitavos de polegada), barras de **20 ft**, estribo **#3** (o de 5 mm não existe lá; PROVISÓRIO, pesquisa ⚠️). Constantes no brocas.py (BITOLAS_EUA, COBRIMENTO_EUA_CM, BARRA_COMERCIAL_EUA_M, BITOLA_ESTRIBO_EUA_MM); a função calcular_brocas recebe sistema=IMPERIAL.
  - Embalagens: cimento em sacos de **94 lb** (os kg do traço ÷ 42,64 kg), areia e brita em **cu yd**, volume em cu yd, ferro em **lb**, arame em lb e rolos de **3,5 lb**. Mais a linha **"Ou concreto pronto: X sacos de 80 lb (no lugar de cimento, areia e brita)"** (cada saco rende 0,60 cu ft; 45 sacos por cu yd, igual à Quikrete), sem preço e fora do custo, porque é uma alternativa. Desde Nov 9, 2026, essas embalagens ficam numa função só, embalagens_eua() no brocas.py, usada pelas Brocas, pelo Baldrame e pela Laje.
  - Exemplo (10 brocas de 12 in com 10 ft, 4 barras #4, estribo #3 a cada 8 in, mão de obra $ 8/ft): 3.20 cu yd; 22 sacos de 94 lb; areia 1.60 cu yd; brita 2.40 cu yd; ou 144 sacos de concreto pronto; gaiola de 5.00 ft; ferro #4 147.0 lb (11 barras de 20 ft); estribos #3 c/ 8 in 54.3 lb (8 barras de 20 ft); aço 201.3 lb; arame 4.0 lb = 2 rolos de 3.5 lb; mão de obra 100.0 ft ($ 800.00).
  - O menu de bitola mostra #3, #4 e #5 nos EUA (ABAS_FERRO_EUA no calculator_screen.py diz quais abas já usam o ferro americano: Brocas e Baldrame, Nov 9, 2026), com o título "Bitola do ferro" / "Rebar size" (sem "(mm)"). Ao trocar de país, a bitola vira a mais parecida (6,3, 8 e 10 mm ↔ #3; 12,5 mm ↔ #4; 16 mm ↔ #5); se ainda era o padrão do país antigo, vira o padrão do novo (8 mm ↔ #4).
  - Lista de compras (Resumo, PDF e WhatsApp): as Brocas e o Baldrame dos EUA guardam as embalagens americanas em chaves próprias (cimento_94lb, areia_cuyd, pedra_cuyd, concreto_80lb, aco_lb, barras_20ft, arame_lb), separadas das do Brasil, porque saco de 94 lb não soma com saco de 50 kg. As duas abas (e a Laje) somam nas mesmas chaves (um "Cimento" só, em sacos de 94 lb; a mistura temporária com o Baldrame em 50 kg acabou em Nov 9, 2026). Os rolos de arame saem do total somado.
  - Mão de obra em ft e estribo em in (corrige o que estava anotado aqui: na Brocas dos EUA a mão de obra aparecia em m e o estribo em cm, igual à P6 do Baldrame na rodada 3).
  - Correção que vale para os dois países: as barras de ferro são arredondadas com uma folguinha (math.ceil(metros / barra - 1e-9), função barras_comerciais no brocas.py, antes _barras; o Baldrame usa a mesma desde Nov 9, 2026), porque 220 ft de ferro em barras de 20 ft davam 11,0000000001 e viravam 12 barras. O Brasil não mudou (os 1055 testes continuam passando).
  - O "?" das Brocas nos EUA explica o padrão americano; as dicas em inglês trocaram "ex:" por "e.g.".
- **Baldrame nos EUA (feito em Nov 9, 2026; conferido no app pela Gabriela):**
  - Igual às Brocas: a conta é a do Brasil (em métrico por dentro), com cobrimento de 3 in, bitolas #3, #4 e #5 (padrão #4), barras de 20 ft, estribo #3 (retangular) e as mesmas embalagens (volume em cu yd, sacos de 94 lb, areia e brita em cu yd, "Ou concreto pronto: X sacos de 80 lb", ferro em lb e barras de 20 ft, arame em lb e rolos de 3.5 lb). A função calcular_baldrame recebe sistema=IMPERIAL; a tela usa _resultado_baldrame_eua (calculator_screen.py).
  - **Emendas:** a cada 20 ft de viga (o tamanho da barra), com os mesmos 40 diâmetros (#4 = 20 in; PROVISÓRIO, pesquisa ⚠️: o IRC manda para uma tabela). O resultado mostra "(inclui X ft de emendas)" (texto label_traspasse dos EUA).
  - A impermeabilização (Parte 1) não mudou. A mão de obra continua em ft e o estribo em in (rodada 3, P6). A viga mínima continua 8 x 12 in (decisão da Gabriela, Nov 9, 2026).
  - Exemplo (conferido no app: 40 ft de viga 8 x 12 in, 4 barras #4, estribo #3 a cada 8 in): 1.04 cu yd; 7 sacos de 94 lb; areia 0.52 cu yd; brita 0.78 cu yd; ou 47 sacos de concreto pronto; ferro #4 122.5 lb (10 barras de 20 ft, inclui 6.67 ft de emendas); estribos #3 c/ 8 in 37.8 lb (6 barras de 20 ft); aço 160.3 lb; arame 3.2 lb = 1 rolo de 3.5 lb; custo $ 329.07.
  - O "?" do Baldrame nos EUA ganhou um parágrafo sobre o padrão americano do ferro e do concreto pronto; as dicas em inglês trocaram "ex:" por "e.g.".
  - Testes: 18 casos do Baldrame da rodada 3 mudaram (testes_rodada3.md e rodada3.py, ver claude/plano_testes.md); os casos do ferro dos EUA entram na rodada 3b.
- **Paredes nos EUA (feito em Nov 9, 2026; conferido no app pela Gabriela e commitado):**
  - Decisões da Gabriela (Nov 9, 2026): só o bloco **CMU 8x8x16** no menu; a massa em **massa pronta tipo S de 80 lb**, com a alternativa do cimento de alvenaria; os campos **Assentamento** e **Traço da massa** somem nos EUA (o bloco vai sempre do mesmo jeito e a massa já vem pronta).
  - Bloco: medida real 7 5/8 x 7 5/8 x 15 5/8 in; com a junta padrão de 3/8 in fica 8 x 16 in = **1,125 bloco por sq ft** (pesquisa ✅). A conta dos blocos é a mesma do Brasil (pela geometria, com a quebra). Constantes no paredes.py (TIJOLOS_EUA, TIJOLO_PADRAO_EUA e tijolos_do_pais(); calcular_paredes recebe sistema=IMPERIAL).
  - Massa: pelos números do fabricante (Quikrete), sobre os blocos assentados (sem a quebra) mais os 10% de perda da massa, igual ao Brasil: **massa pronta tipo S, 13 blocos por saco de 80 lb**; e a linha **"Ou: X sacos de cimento de alvenaria tipo S de 70 lb + Y lb de areia (no lugar da massa pronta)"** (46 blocos e 240 lb de areia por saco), sem preço e fora do custo, igual ao concreto pronto. O Brasil continua com cimento, cal e areia pelo traço.
  - Resultado: áreas em sq ft (a área digitada, sem o arredondamento em m²), blocos só em peças (sem milheiro, também na lista de compras), "Massa pronta tipo S: X sacos de 80 lb" e a alternativa. Lista de compras: chaves próprias (massa_80lb, cimento_alv_70lb, areia_alv_lb), função _linhas_massa_eua no lista_compras.py.
  - Exemplo: 320 sq ft → 378 blocos ($ 2,268.00); 31 sacos de 80 lb ($ 372.00); ou 9 sacos de 70 lb + 2,160 lb de areia; custo $ 2,640.00.
  - Ao trocar de país, o tijolo que não existe no país novo vira o padrão de lá (baiano ↔ CMU 8x8x16; função _trocar_tijolo_de_pais no calculator_screen.py).
  - O "?" das Paredes nos EUA explica o bloco CMU e a massa pronta; as dicas em inglês trocaram "ex:" por "e.g.".
  - Testes: nenhum arquivo de rodada muda; as Paredes dos EUA entram na rodada 3b.
- **Laje nos EUA (no código em Nov 9, 2026; falta a Gabriela colar e testar no app):**
  - A laje pré-moldada com isopor ou lajota não é usada na casa americana: nos EUA a aba é o **piso de concreto no chão (slab-on-grade, código IRC R506)**. Decisões da Gabriela (Nov 9, 2026): **tela soldada Sim/Não** (padrão Não), em painéis de **5 x 10 ft** (50 sq ft, malha 6x6 W1.4/W1.4, pesquisa ✅), com os mesmos 10% a mais para a sobreposição; **lona plástica** por baixo (vapor retarder, o IRC exige) e **base de brita de 4 in** (IRC ✅), cada uma Sim/Não, as duas com padrão **Sim**; o concreto igual às Brocas, mais a linha **"Ou concreto usinado (caminhão): X cu yd (no lugar de cimento, areia e brita)"**; limite com aviso da espessura **de 3 1/2 in** (o mínimo do IRC) **a 8 in**.
  - Campos nos EUA: área (sq ft, obrigatória); espessura (in, opcional, já vem com **4 in**; campo esp_slab, separado do "esp" da laje maciça do Brasil, para não contar como aba preenchida pela regra 1); tela, lona e base (Sim/Não); traço; perda. O menu "Tipo de laje", o enchimento e a capa somem nos EUA; o resultado mostra "Tipo de laje: Piso de concreto no chão (slab-on-grade)".
  - Contas (função calcular_laje_eua no laje.py; a tela usa _calcular_laje_eua no calculator_screen.py): concreto = área x espessura, com a perda; as embalagens do concreto vêm da embalagens_eua() do brocas.py (sacos de 94 lb, areia e brita em cu yd, concreto pronto em sacos de 80 lb). **Concreto usinado:** o volume com perda em cu yd, arredondado para cima de **1/4 em 1/4 cu yd** (PROVISÓRIO ⚠️; é como as concreteiras costumam vender), sem preço e fora do custo, igual ao concreto pronto. **Lona:** área + 10% (emendas de 6 in e as bordas que sobem na forma; PROVISÓRIO ⚠️), em rolos de **10 x 100 ft** (1.000 sq ft, o mais vendido na Home Depot, em 6 mil e 10 mil). **Base de brita:** área x 4 in, com a mesma perda do concreto, em cu yd.
  - Preços PROVISÓRIOS (no laje.py): painel de tela $ 95.00 (o mesmo número do painel de 2 x 3 m do Brasil), rolo de lona $ 90.00; a base de brita usa o preço da brita por m³.
  - Exemplo (500 sq ft, 4 in, tela Sim, lona e base Sim, traço 1:2:3, perda 5%): volume 6.48 cu yd; brita da base 6.48 cu yd ($ 198.20); lona 550.00 sq ft = 1 rolo de 10 x 100 ft ($ 90.00); tela 550.00 sq ft = 11 painéis de 5 x 10 ft ($ 1,045.00); cimento 44 sacos de 94 lb ($ 528.00); areia 3.24 cu yd ($ 111.60); brita 4.86 cu yd ($ 148.80); ou 292 sacos de concreto pronto; ou 6.50 cu yd de concreto usinado; custo $ 2,121.60.
  - Lista de compras (Resumo, PDF e WhatsApp): o concreto soma nas chaves das Brocas (cimento_94lb, areia_cuyd, pedra_cuyd, concreto_80lb); chaves novas concreto_caminhao_cuyd, base_brita_cuyd, lona_rolos e tela_paineis_eua (função _linhas_laje_eua no lista_compras.py). A tela dos EUA fica separada da do Brasil (painel de 5 x 10 ft não soma com o de 2 x 3 m).
  - Histórico: salva tipo_laje "slab", esp_slab, tela, lona e base_brita; orçamento do Brasil aberto nos EUA (ou antigo) vem com lona e base em Sim e a espessura de 4 in. Ao trocar de país, a espessura dos EUA é guardada e volta (4 in ↔ 10,16 cm). Erro de espessura zero: "A espessura da laje deve ser maior que zero." (chave erro_espessura_slab, no textos_eua.py).
  - O "?" da Laje nos EUA explica o slab-on-grade, a base, a lona, a tela e as duas alternativas do concreto; as dicas em inglês usam "e.g.".
  - Testes: nenhum arquivo de rodada muda; a Laje dos EUA entra na rodada 3b.

## Resumo e extras prontos

**Resumo (pronto, Oct 26, 2026).** No topo, o botão Voltar (volta para as abas, se veio do Finalizar, ou para o Histórico, se veio do botão Resumo do card) e dois botões: **Orçamento** e **Lista de compras** (o aberto fica destacado). O cabeçalho mostra o responsável (nome e e-mail, só se estiver logado), a data e a região. O Orçamento mostra as etapas com o custo de cada uma, o resumo financeiro (o subtotal de mão de obra só aparece se houver), o seletor da reserva para imprevistos e o aviso de estimativa no final. Valores com separador de milhar (R$ 4.902,70; nos EUA, US$ 4,902.70). Os textos do Resumo estão em português e inglês. O que aparece no Resumo é sempre igual ao resultado da aba (regra 17). O botão Resumo do card do Histórico também passa pelo Finalizar, então mostra só as abas do país escolhido, com o aviso da regra 21 quando alguma ficou de fora.

**PDF (pronto, Oct 26, 2026).** O botão Gerar / Exportar PDF pergunta: Orçamento, Lista de compras ou Os dois juntos; o PDF é salvo na pasta Downloads e abre direto (só aparece mensagem se der erro). Cabeçalho com a logo, o nome HouseSynk, responsável, data e região; etapas em faixas azuis com tabela de materiais e custo; resumo financeiro com o total em destaque; lista de compras por loja com um quadradinho para marcar cada item; rodapé em todas as páginas com o aviso de estimativa e "HouseSynk · página / total". Os títulos "Etapas incluídas" e "Resumo financeiro final" nunca ficam sozinhos no fim da página: pulam junto com o conteúdo (Nov 4, 2026).

O Resumo e o PDF mostram só as abas preenchidas, com o custo de cada uma e o total da obra. A lista de compras soma os materiais de todas as abas (tijolos, cimento, cal, areia, brita, aço, arame, impermeabilizante em baldes de 18 L e galões de 3,6 L, laje pré-moldada, telhas e madeiramento, materiais elétricos e hidráulicos, piso, azulejo, argamassa, rodapé, rejunte, tintas e complementos, esquadrias e insumos de fixação), mostrando só o que for maior que zero. Tijolos e argamassa colante aparecem por tipo, com o mesmo nome da aba (regra 17).

**Funcionalidades extras prontas**

1. **Reserva para imprevistos** (pronta, Oct 26, 2026). No Resumo (aba Orçamento), o cliente escolhe: Sem reserva (padrão), Obra tranquila (+10%) ou Reforma antiga (+15%). A reserva é calculada sobre o total da obra e aparece como linha separada, seguida do "Total com reserva", no Resumo e no PDF; nunca embutida nos materiais. Os percentuais ficam em src/calculators/reserva.py. É salva junto com o orçamento (campo reserva_perfil em cada etapa salva) e volta ao abrir pelo Histórico; orçamentos antigos e orçamentos novos começam em Sem reserva.
2. **Lista de compras somada e por loja** (pronta no Resumo e no PDF, Oct 26, 2026). Soma o mesmo material de todas as abas (ex.: "Cimento: 47 sacos") e agrupa por loja: Material básico (depósito de construção, inclui telhas, madeiramento e insumos de fixação), Acabamento, Elétrica, Hidráulica e Esquadrias (para cotação). Grupo vazio não aparece. **WhatsApp (pronto, Oct 26, 2026):** botão "Enviar pelo WhatsApp" nas duas abas do Resumo; abre o WhatsApp (link wa.me) com o texto já escrito: na Lista de compras, a lista por loja; no Orçamento, um resumo curto (custo de cada etapa, subtotais, total e reserva). O detalhe completo fica no PDF.
3. **Moeda pelo país** (conferido, Oct 26, 2026). A moeda segue o país escolhido, sem conversão por cotação (R$ 4.902,70 no Brasil; $ 4,902.70 nos EUA). O idioma agora é escolhido separado do país, num botão próprio nas Configurações (antes, trocar o país trocava o idioma).
4. **Gráficos no PDF** (pronto, Oct 26, 2026). Seção "Onde vai o dinheiro" no fim do orçamento: uma barra por aba, da mais cara para a mais barata, com o valor e a porcentagem; a mais cara em destaque. Só aparece com 2 abas ou mais. Feito com o ReportLab.

## Itens da App Store já feitos

- [x] Preencher o requirements.txt (feito em Oct 21, 2026: Kivy 2.3.1 e KivyMD 2.x do GitHub; o reportlab entra quando o PDF for refeito).
- [x] Ícone da App Store: assets/icone_app.png (1024 x 1024, sem transparência), feito em Oct 26, 2026.

## Erros já corrigidos

- [x] Plural errado nos resultados quando a quantidade é 1 (ex.: "1 sacos de 50 kg"). Corrigido em todas as abas em Nov 3, 2026 (regra 16).
- [x] Números grandes sem separador de milhar no resultado (ex.: "Área bruta: 100000,00 m²"). Corrigido em Nov 3, 2026 (regra 16).
- [x] "perda" escrito direto no código (ex.: "10% perda"): agora passa pelo txt() ("com 10% de perda" / "with 10% waste"), Nov 3, 2026.
- [x] Textos escritos direto no código, que apareciam em português no inglês: o "c/" dos estribos e as mensagens de erro dos arquivos de src/calculators/ (ex.: "Quantidade, profundidade e diâmetro devem ser maiores que zero.", "O desconto de vãos deve ser menor que a área."). Corrigido na rodada 2 (Nov 4, 2026): as mensagens viraram chaves traduzidas pela tela e o "c/" passa pelo txt() (regra 18).
- [x] Textos estranhos no inglês do Brasil (17 pendências da rodada 2: nomes das abas, embalagens, "pcs", maiúsculas, milheiro, galão, entre outros). Corrigidos e testados em Nov 5, 2026 (regra 19; resumo em claude/plano_testes.md).
- [x] Sem barra de rolagem para clicar e arrastar (no Resumo com todas as abas era quase impossível chegar no fim). Feita em Nov 5, 2026 (regra 20).
- [x] Pendências da rodada 3 (EUA, Nov 5, 2026): P1 a P9 (custo do piso e do impermeabilizante sem arredondar antes, textos do "?", espessura do rejunte vazia, aviso da viga, medidas digitadas voltando na unidade do país e em fração, limite do rendimento), mais a P10 pedida pela Gabriela ("ANSI A118.4" e frações sem quebrar a linha). Corrigidas e testadas em Nov 6, 2026 (resumo em claude/plano_testes.md).
- [x] Barras de ferro a mais quando a conta dava um número exato (220 ft em barras de 20 ft davam 12 barras, e não 11): folguinha no arredondamento (função barras_comerciais no brocas.py, antes _barras), Nov 9, 2026; o Baldrame usa a mesma função desde Nov 9, 2026.
- [x] Estribo a menos no Baldrame quando o comprimento dividido pelo espaçamento dava um número exato (100 ft com estribo a cada 6 in davam 200, e não 201): mesma folguinha (baldrame.py), Nov 9, 2026. O Brasil não mudou.
- [x] Mesma folguinha na quantidade de tijolos e blocos das Paredes (paredes.py), Nov 9, 2026. O Brasil não mudou.

## Testes automáticos já feitos

- **Decisão da Gabriela (Nov 4, 2026):** começar o pytest já, aos poucos, com a rodada 1 completa; cada rodada nova entra nele quando fechar.
- Feito: pytest.ini (na pasta do app: procura testes só em tests/, inclusive nas pastas de dentro, e não cria .pytest_cache) e o test_rodada1.py, que LÊ o testes_manuais/rodada1.py (CASOS, ESPERADO e rodar) e transforma cada caso num teste (parametrize). Não repete os casos: o lugar para manter continua sendo o rodada1.py. Rodar: env311\Scripts\python.exe -B -m pytest; uma aba: -k CP-.
- Testes unitários (Nov 4, 2026): um arquivo por aba (test_brocas.py, test_baldrame.py, ..., test_esquadrias.py), chamando a função de conta direto, sem tela: Teste A, Teste B, variações e mensagens de erro (conferindo a chave do erro, regra 18), com os números do testes_rodada1.md. O test_contrapiso.py começou com os 2 primeiros testes escritos pela Gabriela. São 187 testes.
- **Rodada 2 no pytest (Nov 5, 2026):** o testes_manuais/rodada2.py tem o ESPERADO completo dos 353 casos em inglês dentro (igual ao rodada1.py), e o test_rodada2.py lê dele. Como o rodada2.py liga o inglês ao ser carregado, o test_rodada2.py volta o idioma para o português logo depois e liga o inglês só durante cada caso (fixture app_em_ingles, com monkeypatch), para não estragar a rodada 1.
- **Pasta tests organizada (Nov 5, 2026):** tests/abas/ (os 14 test_<aba>.py) e tests/rodadas/ (test_rodada1.py, test_rodada2.py e, desde Nov 6, 2026, test_rodada3.py). As pontes acham a pasta do app com Path(__file__).resolve().parent.parent.parent.
- **Rodada 3 (Nov 5 e 6, 2026):** o testes_manuais/rodada3.py (feito pelo Claude Code do terminal a partir do rodada2.py) troca o país com o próprio alternar_pais e, durante a rodada, lia o esperado do testes_rodada3.md. No fechamento (Nov 6, 2026), o ESPERADO conferido dos 162 casos entrou no rodada3.py e o test_rodada3.py guarda e devolve o CONFIG_APP e a TABELA_PRECOS_GLOBAL (não usa o alternar_pais para voltar, porque ele volta com outros preços). Total: **1055 testes** (187 das abas + 353 da rodada 1 + 353 da rodada 2 + 162 da rodada 3), em uns 2 segundos.
- **Parte A (Nov 9, 2026):** os 1055 testes provam que o Brasil e as abas da rodada 3 não mudaram. As Brocas, as Paredes e a Laje nos EUA, a faixa sem o Contrapiso e o aviso do Resumo foram conferidos pelo Leo com scripts, pelo mesmo caminho do botão Calcular. O Baldrame dos EUA já está no pytest pelos 29 casos BA- da rodada 3 (18 deles atualizados em Nov 9, 2026 para o concreto e o ferro dos EUA; o BA-A passou a usar a bitola #5).
- As rodadas são conferidas com scripts (testes_manuais/rodada1.py, rodada2.py e rodada3.py): eles trocam o Kivy por um falso (mock), rodam cada caso pelo mesmo caminho do botão Calcular (_calcular_aba) e têm o resultado esperado de cada caso dentro (ESPERADO, no fim do arquivo): dizem OK ou DIFERENTE em cada caso e mostram a diferença. Na Esquadrias, eles apertam também o Continuar da janela do Adicionar.

## Respostas do engenheiro já aplicadas no código

Aplicadas nas Partes 1 e 2 (Oct 27, 2026):

- Brocas e Baldrame: estribo de 5 mm a cada 20 cm; cobrimento 2 cm (depois trocado para 3 cm); gancho 5 cm; estribo das Brocas em espiral; 4 barras longitudinais; perda do ferro 10%; arame recozido 2% do peso do aço.
- Brocas: gaiola até a metade da profundidade.
- Baldrame: perda de 5% no concreto; traspasse de 40 vezes a bitola (escolha nossa, ele deixou em aberto); impermeabilizante Neutrol por litro, em baldes de 18 L e galões de 3,6 L.
- Contrapiso: traço 1:3:3, espessura de 5 a 7 cm.
- Reboco: chapisco de 0,5 cm; cimento de cerca de 2,7 kg/m² em 2 cm no traço 1:2:8.
- Massa (Paredes e Reboco): precisava de mais material; decidido aumentar só a areia em 25% (inchamento).

Confirmadas, sem mudança no código: rejunte (densidade 1,58 e espessura 8 mm); laje (1,2 cm entre as vigotas e 12 lajotas por m²); telhado inteiro (inclinações, telhas, cumeeira e madeiramento); elétrica (conduíte e fios por ponto); hidráulica inteira (tubos, conexões, registros e água quente em CPVC); pintura (rendimentos de tinta, selador e fundo, massa 0,5 kg/m², complementos na parede e no teto).

Aplicadas na Parte 3 (Oct 28, 2026): Piso e Azulejo com argamassa colante 3,5 kg/m² para qualquer peça, perda pelo tamanho da peça (10%, 15%, 20% e 25% com desenho) e rodapé com tamanho da peça informado pelo cliente.

Aplicada na Parte 4 (Oct 28, 2026): Laje com opção de tela soldada na capa (painéis de 2 x 3 m).

Aplicada na Parte 5 (Oct 28, 2026): Elétrica com o campo de quantidade de chuveiros.

Respostas durante os testes gerais (Oct 28, 2026), já aplicadas: profundidade máxima das brocas 30 m; baldrame sem comprimento máximo ("depende da obra"); viga mínima de 20 cm de largura e 30 cm de altura (pode ficar assim, confirmado em Oct 29, 2026). Todos como aviso com "Continuar" (regra 12).

Resposta de Oct 29, 2026, já aplicada: cobrimento de 3 cm (COBRIMENTO_CM = 3.0 no brocas.py; o baldrame usa o mesmo), conferido no código do GitHub em Nov 9, 2026.
