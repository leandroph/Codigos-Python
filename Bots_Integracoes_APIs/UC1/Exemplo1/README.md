
# ⚡ Agregador de Investimentos Assíncrono (FastAPI)


Este projeto é uma **API de Alta Performance** desenvolvida com **FastAPI**. Ela demonstra o poder do `async/await` do Python para realizar múltiplas consultas externas simultaneamente, reduzindo drasticamente o tempo de resposta para o usuário final.

O sistema simula um dashboard financeiro que precisa buscar cotações em 3 fontes diferentes (Ações, Cripto e Tesouro Direto) antes de responder ao cliente.

---

## 🧠 O Conceito: Síncrono vs Assíncrono

A grande lição deste projeto é a diferença de arquitetura. Imagine que temos 3 tarefas que levam os seguintes tempos:
1.  API Ações: **1.5s**
2.  API Cripto: **1.0s**
3.  API Tesouro: **2.0s**

### 🐢 Abordagem Tradicional (Síncrona)
O sistema faz uma requisição, espera ela voltar, faz a próxima, espera...
* **Cálculo:** 1.5s + 1.0s + 2.0s
* **Tempo Total:** **4.5 segundos** (Muito lento para o usuário).

### 🐇 Abordagem Deste Projeto (Assíncrona)
O sistema dispara as 3 requisições ao mesmo tempo e aguarda todas retornarem.
* **Cálculo:** O tempo total é determinado apenas pela tarefa mais lenta.
* **Tempo Total:** **~2.0 segundos** (Mais de 50% de ganho de performance).

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função |
| :--- | :--- |
| **Python 3.x** | Linguagem base. |
| **FastAPI** | Framework web moderno, rápido e nativamente assíncrono. |
| **HTTPX** | Cliente HTTP que suporta requisições não-bloqueantes (diferente do `requests`). |
| **Asyncio** | Biblioteca padrão para gerenciar o Event Loop e tarefas concorrentes. |
| **Uvicorn** | Servidor ASGI para rodar a aplicação. |

---

## ⚙️ Instalação

Siga os passos abaixo para rodar o projeto localmente.

### 1. Pré-requisitos
Tenha o Python instalado.

### 2. Instalar Dependências
```bash
pip install fastapi uvicorn httpx
```

## 🚀 Como Executar

No terminal, navegue até a pasta do projeto e execute:

```bash
python agregador.py
```

Você verá a mensagem: Uvicorn running on http://0.0.0.0:8000

Abra seu navegador ou Postman e acesse: 👉 http://localhost:8000/carteira

## 📊 Entendendo o Resultado
Ao acessar a rota /carteira, você receberá um JSON. Preste atenção no campo tempo_processamento.

```json
    {
  "status": "Sucesso",
  "tempo_processamento": "2.02 segundos",
  "mensagem": "Note que o tempo total foi ditado apenas pela requisição mais lenta (2s)!",
  "carteira_consolidada": {
    "Acoes": { "PETR4": 30.50, ... },
    "Criptomoedas": { "BTC": 250000.00, ... },
    "Renda_Fixa": { "Selic": "11.75%", ... }
  }
}
```

> Nota: O campo tempo_processamento: "2.02 segundos" é a PROVA DO PARALELISMO. Se o código fosse sequencial, esse tempo seria superior a 4.5 segundos.


## 📂 Estrutura do Código
O arquivo agregador.py contém duas partes principais:

1. Endpoints Mock (/mock/*)

   * Simulam as APIs externas lentas usando await asyncio.sleep(x).

   * Na vida real, seriam substituídos por URLs reais da B3, Binance, etc.

2. Endpoint Agregador (/carteira)

    * É onde a mágica acontece.

    * Usa httpx.AsyncClient() para criar um cliente não-bloqueante.

    * Usa asyncio.gather(tarefa1, tarefa2...) para disparar tudo junto.