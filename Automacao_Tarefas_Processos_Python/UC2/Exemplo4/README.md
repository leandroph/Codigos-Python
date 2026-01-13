# 📸 Downloader de Mídia Competitiva (Modo Universal/Offline)



Este projeto é um robô de **Inteligência de Mercado** que automatiza a coleta de imagens de produtos de sites concorrentes. 

Esta versão específica foi desenhada com uma arquitetura **Offline-First**: ela cria um site simulado localmente (com imagens geradas via Python) e utiliza um crawler capaz de baixar arquivos tanto da Web (`http://`) quanto do Sistema de Arquivos local (`file:///`), contornando bloqueios de proxy, firewall ou erros de DNS comuns em redes corporativas.

## 🎯 Objetivo
Acessar um catálogo de produtos, identificar imagens relevantes (ignorando logos e ícones de layout), baixá-las e renomeá-las automaticamente com o SKU (Código do Produto).

## 🛡️ Diferenciais desta Versão
1.  **Imune a Bloqueios de Rede:** O setup gera as imagens `.jpg` localmente usando a biblioteca `Pillow`, eliminando a dependência de sites externos (como placeholder.com) que podem estar bloqueados.
2.  **Download Híbrido (`urllib`):** Substituímos a biblioteca `requests` pela `urllib.request`. Isso permite que o robô baixe arquivos locais como se estivessem na internet, ideal para ambientes de teste e desenvolvimento seguro.
3.  **Seleção Contextual:** O robô sabe diferenciar o que é foto de produto e o que é "lixo" (banners, ícones) analisando a estrutura HTML.

## 🛠️ Tecnologias

- **Selenium:** Navegação e extração de dados no DOM.
- **Pillow (PIL):** Geração de imagens falsas para o ambiente de teste.
- **Urllib:** Biblioteca padrão do Python para downloads universais (Web/Local).

## ⚙️ Instalação

Execute o comando abaixo para instalar as dependências necessárias:

```bash
pip install selenium webdriver-manager pillow
```

## 🚀 Como Executar

O processo é dividido em **duas etapas** para garantir que funcione perfeitamente na sua máquina.

---

### ▶️ Passo 1: Criar o Ambiente Local (Setup)

Execute este script para gerar:
- As **imagens de teste**
- O arquivo HTML do site **"concorrente"** na sua pasta local

```bash
python setup_catalogo_offline.py
```

**Saída esperada:**
- Criação da pasta `Site_Local`
- Arquivo `catalogo_concorrente.html`
- 3 imagens JPG geradas automaticamente

---

### ▶️ Passo 2: Executar o Crawler

Execute o robô crawler. Ele irá:
- Abrir o navegador em modo **oculto (headless)**
- Ler o site local
- Baixar as imagens encontradas
- Renomeá-las com base no **SKU**
- Salvar tudo na pasta de destino

```bash
python downloader_universal.py
```

---

## 📂 Estrutura do Projeto

```plaintext
.
├── setup_catalogo_offline.py   # Gera o site e as imagens locais
├── downloader_universal.py     # O Robô Crawler
├── Site_Local/                 # O "Servidor" simulado
│   ├── catalogo_concorrente.html
│   ├── img_tenis.jpg
│   ├── img_camisa.jpg
│   └── img_bone.jpg
├── Imagens_Concorrente/        # SAÍDA (Imagens baixadas e renomeadas)
│   ├── SKU-RUN-001.jpg
│   ├── SKU-DRY-099.jpg
│   └── SKU-CAP-555.jpg
└── README.md                   # Documentação
```

---

## 🧠 Lições Aprendidas (Conceitos-Chave)

### 🔍 Busca Aninhada (*Nested Find*)

Em vez de buscar **todas** as imagens da página:

```python
driver.find_elements(By.TAG_NAME, 'img')
```

O robô:
1. Busca primeiro os **cards de produto** (`class="card-produto"`)
2. Dentro de cada card, localiza apenas a imagem do produto

➡️ Isso evita baixar:
- Logos
- Ícones de redes sociais
- Imagens irrelevantes

---

### 📁 Protocolo `FILE` vs `HTTP`

- A biblioteca **`requests`** é excelente para a web (`http://` / `https://`)
- Porém, falha ao acessar arquivos locais (`file:///`)

Neste projeto, utilizamos:

```python
urllib.request.urlretrieve()
```

➡️ Essa função é **agnóstica ao protocolo**, funcionando tanto para:
- URLs HTTP/HTTPS
- Arquivos locais (`file:///`)

Isso torna o script **mais versátil e ideal para testes offline**.
