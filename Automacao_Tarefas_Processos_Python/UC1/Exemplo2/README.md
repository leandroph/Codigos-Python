# 🤖 Robô de Disparo de E-mails com Anexos Dinâmicos (RPA)

Este projeto é uma automação em Python (RPA) desenvolvida para gerar relatórios de performance personalizados em PDF para uma lista de fornecedores e enviá-los automaticamente por e-mail.

O sistema foi projetado com foco em **resiliência**: caso ocorra erro no envio para um fornecedor específico, o robô registra a falha, continua o processo para os demais e, ao final, envia um resumo da operação para o gerente.

## 🚀 Funcionalidades

- **Geração Dinâmica de PDFs:** Cria arquivos PDF exclusivos para cada fornecedor usando a biblioteca `reportlab`.
- **Envio de E-mails em Massa:** Utiliza `smtplib` para disparos via servidor SMTP (Gmail).
- **Tratamento de Erros (Try/Except):** Garante que o script não pare caso encontre um e-mail inválido.
- **Log de Execução:** Gera um resumo final (Sucessos vs Falhas) enviado para a gestão.

## 🛠️ Pré-requisitos

Certifique-se de ter o Python instalado. As bibliotecas necessárias são:

- `pandas` (Manipulação de dados)
- `openpyxl` (Leitura de Excel)
- `reportlab` (Geração de PDFs)

### Instalação

Execute o comando abaixo no terminal para instalar as dependências:

```bash
pip install pandas openpyxl reportlab
```

## ⚙️ Configuração (Gmail)

Para que o script funcione com o Gmail, é necessário gerar uma **Senha de App**, pois o Google bloqueia o uso da senha padrão em scripts por segurança.

### 🔐 Gerando a Senha de App

1. Acesse sua conta Google: **Gerenciar Conta**
2. Vá em **Segurança** → **Verificação em duas etapas**  
   > Ative, caso esteja desativada
3. Procure por **Senhas de app** (*App passwords*)
4. Crie uma nova senha com o nome:  
   **`Robo Python`**
5. Copie a senha de **16 caracteres** gerada

### 🧩 Configurando no código

No arquivo do robô (`robo_disparador.py`), atualize a variável:

```python
SENHA_EMAIL = "colar_sua_senha_de_app_aqui"
```

> ⚠️ **Atenção:**  
> Nunca suba sua senha real para repositórios públicos (GitHub).  
> Em projetos reais, utilize **variáveis de ambiente** (`.env`).

---

## 📂 Como Executar

O projeto é dividido em **duas etapas**:
1. Geração da massa de dados
2. Execução do robô

---

### ▶️ Passo 1: Gerar Base de Teste

Execute o script de setup para criar a planilha `fornecedores.xlsx` e a pasta de PDFs:

```bash
python cria_arquivo_fornecedores.py
```

📌 Isso criará:
- Um arquivo Excel com **4 fornecedores**
- Um fornecedor com **e-mail inválido propositalmente**, para teste
- A pasta contendo os PDFs de relatório

---

### ▶️ Passo 2: Rodar o Robô

Execute o script principal para iniciar os disparos de e-mail:

```bash
python robo_disparador.py
```

---

## 🌳 Estrutura do Projeto

```plaintext
.
├── cria_arquivo_fornecedores.py       # Script que gera os dados de teste
├── robo_disparador.py                 # Script principal (Lógica do Robô)
├── fornecedores.xlsx                  # Base de dados (Gerada pelo setup)
├── Relatorios_PDF/                    # Pasta onde os PDFs são salvos
│   ├── Relatorio_Empresa A.pdf
│   └── ...
└── README.md                          # Documentação do projeto
```

---

## 🧪 Resultado Esperado

Ao rodar o robô com a base de teste padrão, o log no terminal deve se parecer com este:

```plaintext
Processando [1/4]: Empresa Alpha...
   ✅ E-mail enviado com sucesso!
Processando [2/4]: Beta Comércio...
   ❌ FALHA: Erro no fornecedor Beta Comércio... (Email inválido)
Processando [3/4]: Gama Serviços...
   ✅ E-mail enviado com sucesso!
```
