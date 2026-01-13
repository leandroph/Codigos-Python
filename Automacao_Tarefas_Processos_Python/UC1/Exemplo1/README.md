# 🏦 Robô de Conciliação Bancária (PDF vs Excel)

Este projeto é uma solução de **RPA Financeiro** desenvolvida para automatizar o processo de conferência entre extratos bancários e relatórios internos. 

O script elimina a necessidade de ticagem manual ("caneta marca-texto"), lendo o PDF do banco linha a linha, normalizando os dados e cruzando com a planilha do sistema para identificar discrepâncias automaticamente.

## 🎯 Objetivo
Identificar erros financeiros como:
- Tarifas bancárias lançadas no extrato mas não no sistema.
- Pagamentos registrados no sistema que ainda não foram compensados no banco.
- Divergências de datas ou valores.

## 🛠️ Tecnologias Utilizadas

- **pdfplumber:** Extração de texto de PDFs (superior ao PyPDF2 para tabelas não estruturadas).
- **Pandas:** Manipulação de dados e geração de relatórios Excel.
- **RegEx (Expressões Regulares):** Identificação de padrões de data e valores monetários (R$) dentro de textos desorganizados.
- **ReportLab:** Geração de massa de dados (PDFs fictícios) para testes.

## ⚙️ Pré-requisitos

Certifique-se de ter o Python instalado. As bibliotecas necessárias são:

```bash
pip install pandas openpyxl pdfplumber reportlab
```

## 🚀 Como Executar

O projeto foi desenhado para ser **autossuficiente**.  
Você **não precisa de dados reais** para realizar os testes.

---

### ▶️ Passo 1: Gerar Massa de Dados (Setup)

Execute o script de configuração para criar:
- Um **Extrato Bancário (PDF)**
- Um **Relatório de Sistema (Excel)**  
ambos com **divergências propositais** para fins de teste.

```bash
python setup_conciliacao.py
```

Isso criará os arquivos:
- `Extrato_Banco.pdf`
- `Relatorio_Sistema.xlsx`

---

### ▶️ Passo 2: Rodar o Robô Conciliador

Execute o script principal para realizar a auditoria de conciliação:

```bash
python conciliador.py
```

## 🚀 Como Executar

O projeto foi desenhado para ser **autossuficiente**.  
Você **não precisa de dados reais** para realizar os testes.

---

### ▶️ Passo 1: Gerar Massa de Dados (Setup)

Execute o script de configuração para criar:
- Um **Extrato Bancário (PDF)**
- Um **Relatório de Sistema (Excel)**  
ambos com **divergências propositais** para fins de teste.

```bash
python setup_conciliacao.py
```

Isso criará os arquivos:
- `Extrato_Banco.pdf`
- `Relatorio_Sistema.xlsx`

---

### ▶️ Passo 2: Rodar o Robô Conciliador

Execute o script principal para realizar a auditoria de conciliação:

```bash
python conciliador.py
```

---

## 📊 Resultado Esperado

O robô irá processar as transações e gerar o arquivo:

- **`Divergencias_Conciliacao.xlsx`**

Considerando os dados de teste padrão, o relatório apontará:

- **SOBRA NO BANCO:**  
  Uma tarifa de manutenção (**R$ 45,90**) que não foi lançada no sistema.

- **SOBRA NO SISTEMA:**  
  Um pagamento de consultoria (**R$ 1.000,00**) que consta no sistema, mas não caiu no banco.

---

## 📟 Exemplo de Log no Terminal

```plaintext
📖 Lendo Extrato Bancário (PDF)...
📊 Lendo Relatório do Sistema (Excel)...
⚖️  Cruzando dados...
❌ Divergências encontradas! Relatório salvo em: Divergencias_Conciliacao.xlsx
         Data   Valor                                      Tipo
0  15/01/2024  -45.90  SOBRA NO BANCO (Não lançado no sistema)
1  25/01/2024 -1000.0  SOBRA NO SISTEMA (Não compensado no banco)
```

---

## 🧠 Lógica de Negócio Aplicada

- **Normalização de Valores**  
  O script converte formatações brasileiras  
  (ex: `1.500,00 D`) para `float` padrão (`-1500.00`).

- **Chave Composta**  
  O cruzamento não depende de um ID único (raro entre banco e ERP).  
  É utilizada a combinação:
  ```
  DATA + VALOR
  ```

- **Tolerância Matemática**  
  Comparações monetárias usam margem de segurança:
  ```python
  abs(a - b) < 0.01
  ```
  evitando erros de ponto flutuante.

- **Controle de Duplicidade**  
  Transações já conciliadas são marcadas, impedindo que:
  - Um pagamento de R$ 50,00 no banco
  - Valide dois pagamentos de R$ 50,00 no sistema por engano.

---

## 📂 Estrutura do Projeto

```plaintext
.
├── setup_conciliacao.py          # Gerador de arquivos de teste
├── conciliador.py                # Lógica principal do robô
├── Extrato_Banco.pdf             # Entrada (Gerado pelo setup)
├── Relatorio_Sistema.xlsx        # Entrada (Gerado pelo setup)
├── Divergencias_Conciliacao.xlsx # SAÍDA (Relatório Final)
└── README.md                     # Documentação
```
