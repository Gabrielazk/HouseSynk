### Rodada 2 (Brasil, inglês): começada em 04/11/2026

**Parte 0, antes de testar (04/11/2026), código pronto e conferido pelo Leo, falta a Gabi colar e testar:**
- **Jeito B (escolha da Gabi):** os arquivos de src/calculators/ não têm mais frase de erro: devolvem uma chave (ex.: `{"erro": "erro_perda_negativa"}`), e a tela mostra a frase no idioma com o txt() (função `_txt_erro` no calculator_screen.py; 37 chaves `erro_*`, mais `label_erro` e `label_estribo_cada`, no comum.py, em PT e EN).
- "Erro:" e o "c/" dos estribos passam pelo txt(): em inglês "Error:" e "@" ("Stirrups 5 mm @ 20 cm").
- Inglês do Brasil (só textos do "en" no comum.py): embalagens na ordem do inglês ("4 rolls of 50 m", "1 can of 18 L", "9 lengths of 6 m", "10 panels of 2 x 3 m", "3 tubs of 2 kg"); "un" virou "pcs"; "peça" da cumeeira e do rodapé virou "piece"; "(ex: 10)" virou "(e.g. 10)"; "3.6 L" virou "3,6 L" (no Brasil a vírgula segue o país).
- Conferido: rodada1.py 353 OK (português não mudou nada) e pytest 540 passed com os 14 test_<aba>.py atualizados (a mensagem de erro esperada virou a chave).
- 29 arquivos: 13 de src/calculators, calculator_screen.py, comum.py e 14 test_<aba>.py.

**Roteiro:** testes_rodada2.md (o mesmo roteiro da rodada 1, com o resultado esperado em inglês tirado do código real e a lista de como cada campo aparece em inglês). O rodada2.py é feito pelo Leo do terminal, a partir do rodada1.py, com o app em inglês.

**Não é erro:** em BR + inglês os números ficam com vírgula e R$ ("2,309 m³"), porque o separador e a moeda seguem o país (regra 13).

**Para a rodada 4 (EUA, inglês):** o textos_eua.py ainda tem embalagens na ordem antiga ("5 gal buckets", "50 lb bags") e "(ex: ...)" nas dicas em inglês dos EUA. Rever lá.
