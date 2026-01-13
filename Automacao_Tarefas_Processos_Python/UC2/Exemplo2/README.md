# ⚖️ Monitor Automatizado de Processos Judiciais (RPA)


Este projeto é uma solução de **RPA (Robotic Process Automation)** desenvolvida para otimizar a rotina de departamentos jurídicos. O robô acessa portais de tribunais, realiza login seguro, monitora uma lista de processos e gera evidências visuais (screenshots) automaticamente caso detecte novas movimentações.

Diferente de scrapers comuns, este projeto implementa técnicas avançadas de **"Humanização"** para evitar bloqueios de segurança (WAF) e detecção de bots.

---

## 🎯 Funcionalidades Principais

* **🔐 Login Automatizado:** Realiza autenticação em portais restritos.
* **🕵️‍♂️ Humanização (Anti-Bloqueio):** Utiliza *Jitter* (espera aleatória) entre ações para simular o comportamento biológico humano e evitar *IP Ban*.
* **📸 Evidência Visual:** Tira um *Print Screen* automático da tela do processo apenas quando há novidades.
* **📊 Gestão via Excel:** Lê a lista de processos de uma planilha e atualiza o status/data da última verificação no próprio arquivo.
* **🛡️ Detecção de Rate Limit:** Identifica se o site retornou erro "429 Too Many Requests" e entra em modo de espera (Cooldown).

---

## 🛠️ Stack Tecnológica

| Tecnologia | Função no Projeto |
| :--- | :--- |
| **Python 3** | Linguagem base da automação. |
| **Selenium WebDriver** | Navegação e interação com o navegador Chrome. |
| **Pandas** | Leitura e escrita de dados em Excel (`.xlsx`). |
| **Random** | Geração de números aleatórios para pausas variáveis (Humanização). |
| **Webdriver Manager** | Gerenciamento automático do driver do Google Chrome. |

---

## ⚙️ Instalação e Configuração

Siga os passos abaixo para preparar o ambiente.

### 1. Pré-requisitos
* Python 3 instalado.
* Google Chrome instalado.

### 2. Instalar Dependências
Abra o terminal na pasta do projeto e execute:

```bash
pip install pandas selenium webdriver-manager openpyxl
```

### 3️. Preparar o Cenário (Setup)

Como não podemos utilizar dados reais de processos ou acessar tribunais oficiais para testes  
(devido a restrições legais e de segurança), execute o script de configuração.

Ele irá criar a **planilha de controle** e as **pastas necessárias**.

```bash
python setup_juridico.py
```

**Saída esperada:**
- Criação do arquivo `lista_processos.xlsx`
- Criação da pasta `Evidencias_Processuais`

---

## 🚀 Como Executar

Após o setup, inicie o **robô advogado**:

```bash
python monitor_tribunal.py
```

### 🤖 O que o robô fará

- Abrirá o navegador **Google Chrome** (controlado pelo Selenium)
- Acessará a página de login (simulada via **The Internet Herokuapp**)
- Fará o login automaticamente
- Lerá a planilha `lista_processos.xlsx`
- Para cada processo:
  - Simulará uma consulta processual
  - Aplicará a regra de negócio

**Regra de Negócio:**  
Se o número do processo terminar com **`0001`** (simulação), o robô irá:
- Detectar **"Nova Movimentação"**
- Salvar um **print da tela** na pasta de evidências
- Atualizar o status no Excel

---

## 🧠 Engenharia do Robô (Deep Dive)

Abaixo estão as estratégias usadas para tornar o robô **robusto, seguro e mais humano**.

---

### 1️⃣ Técnica de *Jitter* (Espera Humana)

Robôs mal implementados utilizam tempos fixos  
(ex: sempre esperar exatamente 2 segundos).

Servidores detectam esse padrão matematicamente exato e bloqueiam o acesso.

Este projeto utiliza a função `espera_humana()`:

```python
def espera_humana(minimo=2, maximo=5):
    tempo = random.uniform(minimo, maximo)
    time.sleep(tempo)
```

Isso gera tempos variáveis como:
- 2.13s
- 4.87s
- 3.05s  

➡️ Tornando o tráfego praticamente indistinguível de um usuário humano.

---

### 2️⃣ Tratamento de CAPTCHA

Embora este exemplo utilize um **mock (simulação)**, a arquitetura já está preparada para:

- Resolver CAPTCHAs simples (texto ou matemática)
- Extrair o desafio diretamente do HTML
- Processar a resposta via Python
- Enviar o resultado automaticamente

---

### 3️⃣ Persistência de Dados

O robô não apenas **lê**, mas também **escreve** no Excel.

Ao final da execução, é gerado o arquivo:

- `lista_processos_atualizada.xlsx`

Esse arquivo contém:
- Data exata da verificação
- Novo status do processo

➡️ Garantindo **rastreabilidade** e **segurança jurídica** para o advogado responsável.

---

## 📂 Estrutura de Arquivos

```plaintext
.
├── setup_juridico.py                 # Script: Gera dados de teste e pastas
├── monitor_tribunal.py               # Script: O Robô Principal (Main)
├── lista_processos.xlsx              # Input: Planilha com os processos
├── lista_processos_atualizada.xlsx   # Output: Relatório final
├── Evidencias_Processuais/           # Folder: Prints das movimentações
│   ├── Movim_9998887-77...png
│   └── ...
└── README.md                         # Documentação do Projeto
```

---

## ⚠️ Aviso Legal e Ético

Este software foi desenvolvido **exclusivamente para fins educacionais e de demonstração**.

🚫 **Não utilize este script** em:
- Sites governamentais reais (e-SAJ, PJe, Projudi, Receita Federal)
- Sistemas judiciais sem autorização explícita
- Ambientes fora de homologação ou APIs públicas

O excesso de requisições automatizadas (*flood*) pode:
- Configurar crime cibernético
- Resultar em bloqueio permanente do IP

✔️ Este projeto utiliza o site **The Internet Herokuapp**  
para simular login e navegação de forma **segura, legal e ética**.
