# 📄 Gerador Automático de Contratos (Mail Merge via Python)

Este projeto é uma solução de **RPA (Robotic Process Automation)** desenvolvida para eliminar o trabalho manual de preenchimento de contratos. 

O script lê uma base de dados em Excel, preenche automaticamente uma minuta padrão no Word (substituindo marcadores como `{{CLIENTE}}`), converte o documento para PDF e organiza os arquivos finais em pastas separadas por vendedor.

## 🚀 Funcionalidades

- **Leitura de Dados:** Importa clientes, valores e prazos de uma planilha Excel (`pandas`).
- **Manipulação de Word:** Substitui marcadores de texto em um arquivo `.docx` preservando a formatação original (`python-docx`).
- **Conversão PDF:** Converte automaticamente os contratos gerados para PDF (`docx2pdf`).
- **Organização Inteligente:** Cria pastas automaticamente com o nome de cada vendedor e move os contratos para o local correto.
- **Formatação Brasileira:** Converte valores numéricos (ex: `15000.5`) para o padrão de moeda Real (ex: `R$ 15.000,50`).

## 🛠️ Pré-requisitos

Para que a conversão de PDF funcione, é necessário ter o **Microsoft Word** instalado na máquina (Windows ou macOS), pois a biblioteca `docx2pdf` utiliza a automação nativa do Office.

Bibliotecas Python necessárias:
- `pandas` & `openpyxl` (Excel)
- `python-docx` (Word)
- `docx2pdf` (Conversão PDF)

### Instalação das Dependências

Execute o comando abaixo no terminal:

```bash
pip install pandas openpyxl python-docx docx2pdf
```

## ⚙️ Como Executar

O projeto funciona em duas etapas: **preparação do ambiente** e **execução da automação**.

---

### ▶️ Passo 1: Gerar Arquivos de Teste (Setup)

Se você ainda não tem a planilha e a minuta, execute o script de configuração.  
Ele criará o arquivo `contratos.xlsx` e o modelo `Minuta_Padrao.docx`.

```bash
python setup_contratos.py
```

---

### ▶️ Passo 2: Rodar a Automação

Com os arquivos de entrada prontos, execute o script principal:

```bash
python gerador_contratos.py
```

---

## 📂 Estrutura do Projeto

Após a execução, a estrutura de pastas ficará assim:

```plaintext
.
├── setup_contratos.py      # Cria os dados fictícios
├── gerador_contratos.py    # Script principal da automação
├── contratos.xlsx          # Base de dados (Entrada)
├── Minuta_Padrao.docx      # Modelo do contrato (Entrada)
├── Contratos_Gerados/      # PASTA DE SAÍDA
│   ├── Ana/
│   │   ├── Contrato_Tech_Solutions.pdf
│   │   └── Contrato_Advocacia_Silva.pdf
│   └── Carlos/
│       ├── Contrato_Mercado_Do_Bairro.pdf
│       └── Contrato_Startup_Inova.pdf
└── README.md
```

---

## ⚠️ Solução de Problemas Comuns

### ❌ Erro na conversão para PDF

Se o script travar ou apresentar erro ao converter para PDF, verifique:

- Se o **Microsoft Word** está instalado
- Se **não há nenhuma janela de diálogo** do Word aberta  
  (ex: *"Ativar Produto"* ou *"Salvar como"*)
- Feche todas as janelas do Word antes de rodar o robô novamente

---

## 📝 Personalização

Para usar com seus próprios documentos:

1. Edite o arquivo `Minuta_Padrao.docx` e insira os marcadores desejados  
   (ex: `{{NOME}}`, `{{CPF}}`, `{{VALOR}}`)
2. Atualize o arquivo `contratos.xlsx` com colunas que correspondam aos marcadores
3. No script `gerador_contratos.py`, ajuste o dicionário `substituicoes`  
   para mapear corretamente:
   - Colunas do Excel → Tags do Word
