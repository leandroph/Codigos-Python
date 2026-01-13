# 📰 Scraper de Notícias com Paginação (Crawling)



Este projeto simula um robô de **Monitoramento de Marca (Clipping)**. Ele acessa um portal de notícias, busca por menções a uma empresa específica e percorre múltiplas páginas de resultados para construir uma base de dados analítica.

O diferencial deste script é a capacidade de realizar **Paginação**: ele não lê apenas a página inicial, mas identifica o botão "Próximo", clica (ou navega) e repete o processo de extração até esgotar os resultados ou atingir um limite seguro.

## 🎯 Funcionalidades
- **Crawling Profundo:** Percorre até 5 páginas de resultados automaticamente.
- **Extração Estruturada:** Captura Título, Data e Link de cada matéria.
- **Exportação:** Salva os dados em CSV formatado (compatível com Excel português).

## 🛠️ Tecnologias
- **Selenium:** Para navegação e interação com a paginação.
- **Pandas:** Para estruturação e salvamento dos dados (CSV).

## ⚙️ Instalação

```bash
pip install selenium pandas webdriver-manager
```

## 🚀 Como Executar

O projeto simula um **portal de notícias** local para evitar bloqueios, CAPTCHAs e mudanças frequentes de sites reais.

---

### ▶️ Passo 1: Criar o Portal de Notícias (Setup)

Como portais de notícias reais normalmente:
- bloqueiam robôs,
- alteram estrutura com frequência,
- utilizam paywalls,

execute o script abaixo para criar **5 páginas HTML locais**, simulando um resultado de busca paginado.

```bash
python setup_portal.py
```

#### 🧪 Saída Esperada
Serão criados os seguintes arquivos:

```plaintext
busca_page_1.html
busca_page_2.html
busca_page_3.html
busca_page_4.html
busca_page_5.html
```

---

### ▶️ Passo 2: Executar o Scraper

Agora execute o robô de coleta.  
Ele irá:

- Iniciar na **página 1**
- Navegar automaticamente até a **página 5**
- Extrair todas as notícias encontradas
- Consolidar os dados em um único arquivo

```bash
python scraper_noticias.py
```

---

## 📊 Resultado Esperado

Ao final da execução, será gerado o arquivo:

- **`clipping_techcorp.csv`**

### 📄 Exemplo de Conteúdo do CSV

```plaintext
Data,Titulo,Link,Origem
13/01/2026,TechCorp anuncia lucro recorde...,https://portal...,Portal Simulado
10/01/2026,Concorrente processa TechCorp...,https://portal...,Portal Simulado
...
```

---

## 🧠 Conceito Chave: Loop de Paginação

A lógica central deste robô é o **controle de paginação**, que transforma um simples scraper em um **crawler completo**.

### 🔁 Lógica do Algoritmo

```python
while tem_botao_proximo:
    1. Extrair notícias da página atual
    2. Procurar botão "Próxima Página"
    3. Se encontrar:
         - Clicar
         - Repetir o processo
    4. Se não encontrar:
         - Parar o loop (break)
```

### 📌 Por que isso é importante?

- Permite varrer **sites inteiros**
- Evita hardcode de número de páginas
- Torna o robô mais **robusto e escalável**
- Simula comportamento humano de navegação

---


