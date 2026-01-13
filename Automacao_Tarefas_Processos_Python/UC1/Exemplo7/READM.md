# 🎨 Gerador de Certificados em Massa (Processamento de Imagem)

Este projeto utiliza a biblioteca **Pillow (PIL)** para automatizar a personalização de imagens. Ele lê uma lista de participantes em Excel e, para cada um, gera um certificado em PNG escrevendo o nome e a data nas coordenadas exatas de um template base, utilizando fontes personalizadas.

## 🎯 Objetivo
Demonstrar como o Python pode interagir com elementos visuais, manipulando pixels e desenhando texto dinâmico sobre imagens estáticas, essencial para marketing, RH e eventos.

## 🛠️ Tecnologias
- **Pillow (PIL):** A biblioteca padrão para manipulação de imagens em Python.
- **Pandas:** Para ler a lista de nomes do Excel.
- **Fontes TrueType (.ttf):** Uso de fontes do sistema ou personalizadas para um visual profissional.

## ⚙️ Instalação
```bash
pip install pandas openpyxl pillow
```

## ⚠️ Requisito Crítico: Fonte (.ttf)

Para que os certificados tenham um bom visual, o script precisa de um arquivo de fonte **TrueType (`.ttf`)**.

### 🖥️ No Windows
- O script tenta localizar automaticamente o arquivo `arial.ttf` em:
  ```
  C:/Windows/Fonts
  ```

### 🌐 Outros sistemas ou fontes personalizadas
- Baixe uma fonte (ex: **Google Fonts**)
- Coloque o arquivo `.ttf` na **mesma pasta do script**
- Atualize no código a variável:
  ```python
  FONTE_NOME_ARQUIVO = "nome_da_fonte.ttf"
  ```

---

## 🚀 Como Usar

### 1️. Preparar o Cenário

Execute o script de setup para:
- Criar o arquivo Excel com os dados dos participantes
- Gerar uma imagem de template base (`template_certificado.png`) para teste

```bash
python setup_certificados.py
```

---

### 2️. Gerar os Certificados

O robô irá:
- Ler os dados do Excel
- Abrir o template do certificado
- Desenhar o **nome** e a **data**, centralizados automaticamente
- Salvar um novo arquivo para cada participante

```bash
python gerador_certificados.py
```

---

## 📂 Estrutura Resultante

```plaintext
.
├── setup_certificados.py       # Cria os dados e imagem de teste
├── gerador_certificados.py     # O robô desenhista
├── participantes_webinar.xlsx  # Lista de nomes
├── template_certificado.png    # Imagem em branco
├── arial.ttf                   # Arquivo de fonte (necessário)
└── Certificados_Gerados/       # PASTA DE SAÍDA
    ├── Certificado_ana_souza.png
    ├── Certificado_carlos_pereira_silva.png
    └── ...
```

---

## 🖼️ Exemplo Visual

O script calcula automaticamente o **centro da imagem** para garantir que:
- Nomes curtos (ex: *"Ana"*)
- Nomes longos (ex: *"Roberto Costa Júnior"*)

fiquem **perfeitamente alinhados no meio do certificado**, mantendo um layout profissional.
