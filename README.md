<p align="center">
  <img src="Calculadora/assets/logo.png" alt="HouseSynk" width="120">
</p>

<h1 align="center">HouseSynk</h1>

<p align="center">
  Calculadora de materiais e custos para obras: do alicerce ao acabamento, com lista de compras e orçamento em PDF.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9-3776AB?logo=python&logoColor=white" alt="Python 3.9">
  <img src="https://img.shields.io/badge/Kivy-2.3.1-2E5E7E" alt="Kivy 2.3.1">
  <img src="https://img.shields.io/badge/KivyMD-2.x-2E5E7E" alt="KivyMD 2.x">
  <img src="https://img.shields.io/badge/status-em%20desenvolvimento-orange" alt="Em desenvolvimento">
</p>

---

## 📱 Sobre

O **HouseSynk** ajuda quem vai construir ou reformar a saber **quanto material comprar e quanto vai gastar**. A pessoa preenche só as partes da obra que quiser, e o app calcula os materiais na unidade em que são vendidos (sacos, latas, barras, rolos, caixas), mostra o custo de cada etapa e monta a lista de compras separada por loja.

O app está sendo preparado para a **App Store**.

---

## 🚀 Funcionalidades

### 🧮 14 calculadoras, organizadas em 3 etapas

| Etapa | Abas |
| --- | --- |
| 🏗️ **Estrutura** | Brocas · Baldrame · Paredes · Laje · Telhado |
| 🔌 **Instalações** | Elétrica · Hidráulica |
| 🎨 **Acabamento** | Contrapiso · Reboco · Piso · Azulejo · Rejunte · Pintura · Esquadrias |

- Nenhuma aba é obrigatória: abas em branco são ignoradas.
- Campos opcionais já vêm com valores padrão (perda, traço, rendimento...).
- Etapas e abas clicáveis no topo, com destaque na etapa e na aba abertas.
- Botões **Anterior**, **Próximo**, **Avançar para a próxima etapa**, **Limpar** (só a aba aberta) e **Finalizar**.
- Ajuda **"?"** em cada aba, explicando os campos.

### 📊 Resumo da obra

- **Orçamento:** custo de cada etapa, subtotal de materiais e de mão de obra e total da obra.
- **Reserva para imprevistos:** obra tranquila (+10%) ou reforma antiga (+15%), sempre numa linha separada.
- **Lista de compras:** os materiais de todas as abas somados e separados por loja: material básico, acabamento, elétrica, hidráulica e esquadrias (para cotação).

### 📄 PDF

- Orçamento, lista de compras ou os dois juntos.
- Cabeçalho com logo, responsável, data e região; tabelas com os materiais e custos.
- Lista de compras com um quadradinho para marcar o que já foi comprado.

### 👤 Conta e histórico

- Login e cadastro, ou uso como visitante.
- Histórico de orçamentos: visualizar, editar, renomear, duplicar e excluir.

### 🌎 Idioma e região

- Português e inglês.
- Brasil (R$) e Estados Unidos (US$), com preços por região editáveis.

---

## 🛠️ Tecnologias

- **Python 3.9**
- **Kivy 2.3.1** e **KivyMD 2.x** (interface)
- **SQLite** (banco local: usuários e orçamentos)
- **ReportLab** (geração do PDF)

---

## 📸 Telas

### 🏠 Entrada

<table>
  <tr>
    <td align="center" valign="top" width="33%"><img src="assets/images/inicio.png" width="230" alt="Tela inicial"><br><sub>Tela inicial</sub></td>
    <td align="center" valign="top" width="33%"><img src="assets/images/login.png" width="230" alt="Login"><br><sub>Login</sub></td>
    <td align="center" valign="top" width="33%"><img src="assets/images/cadastro.png" width="230" alt="Cadastro"><br><sub>Cadastro</sub></td>
  </tr>
</table>

### 🏗️ Estrutura

<table>
  <tr>
    <td align="center" valign="top" width="33%"><img src="assets/images/calculadora.png" width="230" alt="Etapas e abas no topo"><br><sub>Etapas e abas no topo</sub></td>
    <td align="center" valign="top" width="33%"><img src="assets/images/armadura.png" width="230" alt="Campos opcionais (armadura)"><br><sub>Campos opcionais (armadura)</sub></td>
    <td align="center" valign="top" width="33%"><img src="assets/images/resultado.png" width="230" alt="Resultado com custo da etapa"><br><sub>Resultado com custo da etapa</sub></td>
  </tr>
</table>

### 🔌 Instalações

<table>
  <tr>
    <td align="center" valign="top" width="33%"><img src="assets/images/eletrica.png" width="230" alt="Elétrica: quantidades"><br><sub>Elétrica: quantidades</sub></td>
    <td align="center" valign="top" width="33%"><img src="assets/images/eletrica_metragens.png" width="230" alt="Metragens do projeto (opcional)"><br><sub>Metragens do projeto (opcional)</sub></td>
    <td align="center" valign="top" width="33%"><img src="assets/images/eletrica_resultado.png" width="230" alt="Estimado x do projeto"><br><sub>Estimado x do projeto</sub></td>
  </tr>
</table>

### 🎨 Acabamento

<table>
  <tr>
    <td align="center" valign="top" width="33%"><img src="assets/images/contrapiso.png" width="230" alt="Contrapiso"><br><sub>Contrapiso</sub></td>
    <td align="center" valign="top" width="33%"><img src="assets/images/contrapiso_resultado.png" width="230" alt="Resultado do contrapiso"><br><sub>Resultado do contrapiso</sub></td>
    <td align="center" valign="top" width="33%"><img src="assets/images/configuracoes.png" width="230" alt="Configurações e preços"><br><sub>Configurações e preços</sub></td>
  </tr>
</table>

### 📊 Resumo

<table>
  <tr>
    <td align="center" valign="top" width="33%"><img src="assets/images/resumo.png" width="230" alt="Orçamento com reserva para imprevistos"><br><sub>Orçamento com reserva para imprevistos</sub></td>
    <td align="center" valign="top" width="33%"><img src="assets/images/resumo_total.png" width="230" alt="Total da obra"><br><sub>Total da obra</sub></td>
    <td align="center" valign="top" width="33%"><img src="assets/images/lista.png" width="230" alt="Lista de compras por loja"><br><sub>Lista de compras por loja</sub></td>
  </tr>
</table>

### 📂 Histórico

<table>
  <tr>
    <td align="center" valign="top" width="33%"><img src="assets/images/salvar.png" width="230" alt="Salvar no histórico"><br><sub>Salvar no histórico</sub></td>
    <td align="center" valign="top" width="33%"><img src="assets/images/historico.png" width="230" alt="Histórico de orçamentos"><br><sub>Histórico de orçamentos</sub></td>
  </tr>
</table>

### 📄 PDF

<p align="center"><img src="assets/images/pdf.png" width="700" alt="PDF do orçamento"></p>

---

## ▶️ Como rodar

```bash
# 1. Baixe o projeto
git clone https://github.com/Gabrielazk/BuildCalc.git
cd BuildCalc/Calculadora

# 2. (Opcional) crie um ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. Instale as bibliotecas
python -m pip install -r requirements.txt

# 4. Abra o app
python main.py
```

O PDF é salvo na pasta **Downloads**.

---

## 📁 Estrutura do projeto

```
Calculadora/
├── main.py                  # inicia o app
├── requirements.txt
├── assets/                  # logo, ícone do app e fonte do PDF
└── src/
    ├── calculators/         # as contas de cada aba (sem nada de tela)
    ├── models/              # banco de dados, cadastro e login
    ├── services/            # lista de compras e geração do PDF
    └── views/               # as telas (uma por arquivo)
```

As contas ficam separadas das telas: a mesma conta pode ser usada no app, no PDF e, no futuro, em outras versões.

---

## 🗺️ Próximos passos

- [ ] Compartilhar a lista de compras pelo WhatsApp
- [ ] Gráficos de custo por etapa no PDF
- [ ] Versão para os Estados Unidos (unidades e embalagens locais)
- [ ] Tabela de preços atualizada por estado (referência SINAPI)
- [ ] Publicação na App Store

---

## ⚠️ Aviso

Os valores são **estimativas** e não substituem o projeto de um engenheiro ou arquiteto.

---

## 👩‍💻 Autora

**Gabriela Salviatto**

---

## 📄 Licença

© 2026 Gabriela Salviatto. Todos os direitos reservados.

A fonte usada no PDF (Liberation Sans) é distribuída sob a licença SIL Open Font License; o texto da licença está em `Calculadora/assets/fonts`.
