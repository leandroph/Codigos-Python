# 🌎 Tradutor Automático de Comentários (Batch Processing)



Este projeto automatiza a tradução de grandes volumes de texto (Comentários, Reviews, Logs) de Inglês para Português.

O diferencial deste script é a implementação de **Mecanismos de Resiliência**. APIs públicas de tradução possuem limites de requisições por minuto. Se o script tentar traduzir tudo de uma vez, será bloqueado. Este robô implementa "Exponential Backoff" (pausa incremental) para lidar com erros automaticamente.

## 🛡️ Engenharia de Resiliência

O script utiliza duas estratégias para não ser banido pela API:
1.  **Jitter (Pausa Aleatória):** Entre cada tradução bem-sucedida, espera entre 0.5s e 1.5s.
2.  **Exponential Backoff:** Se a API retornar erro (HTTP 429 - Too Many Requests), o script:
    * Espera 1s e tenta de novo.
    * Se falhar, espera 2s.
    * Se falhar, espera 4s.
    * Até o limite de 5 tentativas.

## 🛠️ Tecnologias

- **Python 3.x**
- **Pandas:** Manipulação de CSV em massa.
- **Deep-Translator:** Biblioteca que abstrai o acesso ao Google Translate.

## ⚙️ Instalação

```bash
pip install pandas deep-translator openpyxl
```

## 🚀 Como Executar
**Passo 1: Gerar Massa de Teste**
Crie o arquivo CSV com comentários em inglês.

```Bash
python setup_comentarios.py
```

**Passo 2: Executar Tradutor**
O script lerá o arquivo linha a linha, traduzirá e gerará um novo arquivo.

```Bash
python tradutor_batch.py
```

## 📊 Resultado
Será gerado o `arquivo comentarios_pt_br.csv` com a seguinte estrutura:

```text
ID	Comentario_EN	                Comentario_PT	                Data_Processamento
1	The product arrived late...	O produto chegou atrasado...	2023-10-27
2	Excellent quality!...	        Qualidade excelente!...	        2023-10-27
```

# ⚠️ Nota Importante
Este exemplo usa a versão gratuita/web do Google Translate via biblioteca. Para volumes massivos (milhões de linhas) em produção, recomenda-se usar a API Oficial do Google Cloud (Paid) ou DeepL API, bastando alterar a linha de inicialização do tradutor no código.