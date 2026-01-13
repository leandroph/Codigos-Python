# 💸 Robô de Cobrança Inteligente (Validação Cruzada)

Este projeto é uma automação de **RPA Financeiro** desenvolvida para otimizar o processo de cobrança e eliminar erros críticos, como cobrar clientes que já efetuaram o pagamento.

O sistema realiza uma **validação cruzada** entre o relatório de faturas emitidas (Excel) e o extrato bancário (CSV). Ele identifica automaticamente os inadimplentes e dispara e-mails personalizados com a 2ª via do boleto em anexo.

## 🧠 Lógica do Processo

O robô segue um fluxo rigoroso para garantir segurança na cobrança:

1.  **Leitura de Dados:** Importa a lista de `Faturas_Aberto.xlsx` (Sistema Interno) e `Comprovantes_Recebidos.csv` (Banco).
2.  **Normalização:** Padroniza os IDs das faturas para garantir que a comparação seja exata.
3.  **Filtragem (Anti-Join):** Utiliza a lógica de conjuntos do Pandas (`isin`) para filtrar:
    > *Quem está na lista de Faturas e **NÃO** está na lista de Pagos?*
4.  **Anexação Dinâmica:** Localiza o arquivo PDF correspondente na pasta de boletos.
5.  **Comunicação:** Gera um e-mail em HTML profissional e envia para o cliente.

## 🚀 Funcionalidades

- **Cruzamento de Dados:** Comparação rápida e eficiente usando `pandas`.
- **E-mail HTML:** Envio de mensagens formatadas (não apenas texto puro).
- **Anexos Dinâmicos:** O robô sabe exatamente qual boleto enviar para qual cliente.
- **Segurança:** Evita duplicidade de cobrança.

## 🛠️ Pré-requisitos

Certifique-se de ter o Python instalado. As bibliotecas necessárias são:

- `pandas` (Análise de dados)
- `openpyxl` (Leitura de Excel)
- `reportlab` (Geração dos PDFs de teste)

### Instalação

Execute o comando abaixo no terminal:

```bash
pip install pandas openpyxl reportlab
```

## ⚙️ Configuração (Gmail)

Para enviar e-mails via Gmail, **não é permitido usar a senha padrão de login**.  
É necessário gerar uma **Senha de App**.

### 🔐 Gerando a Senha de App

1. Acesse: https://myaccount.google.com/security
2. Ative a **Verificação em duas etapas**
3. Procure por **Senhas de app** (*App passwords*)
4. Crie uma nova senha com o nome:  
   **`Robo Cobranca`**
5. Copie a senha de **16 dígitos** gerada

### 🧩 Configurando no código

No arquivo `robo_cobranca.py`, atualize as variáveis:

```python
EMAIL_REMETENTE = "seu_email@gmail.com"
SENHA_EMAIL = "cole_sua_senha_de_app_aqui"
```

---

## 📂 Como Executar

O projeto possui **dois scripts**:
- Um para **preparar o cenário de teste**
- Outro para **executar a cobrança automática**

---

### ▶️ Passo 1: Preparar o Ambiente (Setup)

Execute este script para gerar:
- A planilha de faturas
- O CSV do banco
- Os PDFs dos boletos fictícios

```bash
python setup_cobranca.py
```

---

### ▶️ Passo 2: Executar o Robô

Com os arquivos gerados, execute o robô para processar a cobrança:

```bash
python robo_cobranca.py
```

---

## 🌳 Estrutura do Projeto

```plaintext
.
├── setup_cobranca.py           # Gera os dados de teste (Excel, CSV, PDFs)
├── robo_cobranca.py            # Lógica principal de validação e envio
├── Faturas_Aberto.xlsx         # Base de quem devemos cobrar
├── Comprovantes_Recebidos.csv  # Base de quem já pagou
├── Boletos/                    # Pasta contendo os arquivos .pdf
│   ├── Boleto_1001.pdf
│   └── ...
└── README.md                   # Documentação
```

---

## 🧪 Resultado Esperado

Considerando os dados gerados pelo `setup_cobranca.py`:

- **Total de Faturas:** 5  
- **Pagamentos Identificados:** 2  
  - Maria Souza  
  - Padaria Central  
- **Ação:**  
  O robô enviará e-mail **apenas para os 3 clientes restantes**:
  - João Silva
  - Tech Solutions
  - Carlos TI

### 📟 Exemplo de Log no Terminal

```plaintext
📊 Resumo da Análise:
   - Faturas Emitidas: 5
   - Pagamentos Identificados: 2
   - Clientes para Cobrar: 3

🚀 Iniciando disparos de cobrança...
🔄 Processando: João Silva (ID: 1001)...
   ✅ E-mail enviado!
🔄 Processando: Tech Solutions (ID: 1003)...
   ✅ E-mail enviado!
...
```
