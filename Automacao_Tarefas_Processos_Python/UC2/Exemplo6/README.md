# 🏛️ Validador Automático de Situação Cadastral (RPA de Compliance)



Este projeto é uma solução de **RPA (Robotic Process Automation)** desenvolvida para otimizar processos de **Compliance e Compras**. O robô automatiza a consulta em massa da situação cadastral de fornecedores (CNPJ), eliminando o trabalho manual de verificação individual.

O sistema lê uma base de dados Excel, acessa um portal de consulta governamental (simulado para fins didáticos), resolve o fluxo de interação e enriquece a planilha original com o status atual ("ATIVA", "BAIXADA", etc.).

## 🎯 Problema de Negócio Resolvido
Verificar manualmente 50, 500 ou 5.000 fornecedores é uma tarefa:
1.  **Lenta:** Um humano leva cerca de 2 minutos por consulta.
2.  **Propensa a Erros:** Risco de digitar errado ou pular linhas.
3.  **Monótona:** Baixo valor agregado para o analista.

**Este robô realiza a mesma tarefa em segundos, com 100% de precisão.**

## ⚡ Destaques Técnicos (A Diferença de um Robô Profissional)

Diferente de scripts básicos que usam pausas fixas (`time.sleep`), este projeto implementa **Esperas Explícitas (`WebDriverWait`)**.

* **Espera Inteligente:** O robô aguarda dinamicamente o elemento aparecer na tela. Se o site responder em 0.5s, ele segue. Se demorar 10s, ele espera. Isso torna o script **muito mais rápido** e imune a lentidões de rede.
* **Tratamento de Exceções:** Se um CNPJ falhar ou o site cair momentaneamente, o robô registra o erro, dá *refresh* na página e continua para o próximo, sem travar o processo inteiro.
* **Ambiente Controlado:** Utiliza um portal simulado (HTML/JS local) para garantir que a lógica de extração funcione sem bloqueios de IP ou CAPTCHAs complexos durante a demonstração.

## 🛠️ Stack Tecnológica

| Tecnologia | Função |
| :--- | :--- |
| **Python 3.x** | Linguagem principal. |
| **Selenium WebDriver** | Navegação e interação com elementos DOM. |
| **Pandas** | Leitura, manipulação e exportação de Excel (`.xlsx`). |
| **OpenPyXL** | Engine para escrita de arquivos Excel. |
| **WebDriver Manager** | Gestão automática dos drivers do navegador. |

## ⚙️ Instalação e Configuração

### 1. Pré-requisitos
Certifique-se de ter o Python e o Google Chrome instalados.

### 2. Instalar Dependências
No terminal, execute:

```bash
pip install pandas selenium openpyxl webdriver-manager
```

## 🚀 Como Executar

O projeto é dividido em **Setup (preparação)** e **Execução (robô)**.

---

### ▶️ Passo 1: Preparar o Cenário (Setup)

Execute o script abaixo para:
- Gerar a planilha `fornecedores_cnpj.xlsx` com **50 registros**
- Criar o arquivo `portal_receita.html` (sistema simulado)

```bash
python setup_receita.py
```

---

### ▶️ Passo 2: Executar o Validador

Execute o robô validador.  
Ele irá:
- Abrir o navegador
- Iterar sobre a lista de fornecedores
- Consultar o status do CNPJ
- Preencher o resultado na planilha final

```bash
python validador_cnpj.py
```

---

## 📊 Resultados Esperados

Ao final da execução, será gerado o arquivo:

- **`fornecedores_verificados.xlsx`**

### 🧪 Comportamento Simulado

- A **maioria dos fornecedores** retornará como **ATIVA**
- **A cada 5 registros**, um CNPJ retornará como **BAIXADA**  
  (simulando uma empresa irregular)

---

## 📟 Exemplo de Log no Terminal

```plaintext
📂 Carregando lista de CNPJs...
🤖 Iniciando navegador...
🔄 [1/50] Consultando: 12.345.678/0001-00... ✅ ATIVA
🔄 [2/50] Consultando: 12.345.678/0002-00... ✅ ATIVA
...
🔄 [5/50] Consultando: 12.345.678/0005-00... ✅ BAIXADA
```

---

## 📂 Estrutura do Projeto

```plaintext
.
├── setup_receita.py               # Gera os dados e o site simulado
├── validador_cnpj.py              # O Robô (Lógica Principal)
├── fornecedores_cnpj.xlsx         # Input (Gerado pelo setup)
├── fornecedores_verificados.xlsx  # Output (Resultado Final)
├── portal_receita.html            # Sistema web local (simulado)
└── README.md                      # Documentação
```

---

## ⚠️ Nota sobre CAPTCHAs e Sites Reais

Este projeto utiliza um **portal simulado** (`portal_receita.html`)  
por motivos **pedagógicos e éticos**.

Para aplicar esta lógica no site oficial da Receita Federal, seriam necessários passos adicionais:

- 🔐 **Serviços de quebra de CAPTCHA**  
  Integração com APIs pagas (ex: *2Captcha*, *Anti-Captcha*) para resolver desafios de imagem ou hCaptcha.

- 🌐 **Rotação de IP**  
  Uso de proxies para evitar bloqueios por excesso de requisições.

- ✅ **APIs Oficiais (Recomendado)**  
  Em cenários corporativos reais, recomenda-se o uso de APIs oficiais como:
  - `receitaws`
  - `CNPJ.ws`

Essas abordagens garantem **estabilidade, legalidade e segurança**.
