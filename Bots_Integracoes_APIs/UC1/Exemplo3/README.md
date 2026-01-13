# 📊 Dashboard Financeiro Multi-API (Terminal)

Este projeto é um painel de monitoramento de ativos em tempo real. Ele agrega dados de **3 fontes distintas** (Cripto, Moedas e Ações), converte tudo para Reais (BRL) e calcula o patrimônio estimado do usuário.

A principal característica técnica é o uso da biblioteca **Rich**, que permite criar interfaces bonitas e dinâmicas no terminal, evitando aquela sensação de "script travado" enquanto aguarda a atualização.

## 📡 APIs Utilizadas

1.  **Binance API (Pública):** Para cotação do Bitcoin. Não requer chave de API para dados públicos.
2.  **AwesomeAPI (Economia):** Interface amigável para dados oficiais de câmbio (Dólar/Euro).
3.  **Yahoo Finance (`yfinance`):** Para cotação de ações da B3 (PETR4, VALE3).

## 🛠️ Tecnologias

- **Python 3.x**
- **Requests:** Para chamadas HTTP.
- **Yfinance:** Wrapper para dados de mercado de ações.
- **Rich:** Para renderização visual (Tabelas e Painéis) no terminal.

## ⚙️ Instalação

```bash
pip install requests yfinance rich
```

## 🚀 Como Executar
Basta rodar o script principal:

```Bash
python dashboard_financeiro.py
```

## 🖥️ Preview do Resultado
O terminal exibirá um painel que se atualiza automaticamente a cada 30 segundos:

```Plaintext

╭────── Dashboard Financeiro ──────╮
│     📊 MONITOR DE MERCADO        │
│                                  │
│ Ativo         Preço (R$)  Saldo  │
│ ──────────────────────────────── │
│ Bitcoin (BTC) R$ 350.000  R$ ... │
│ Dólar (USD)   R$ 5,15     R$ ... │
│ Ação PETR4    R$ 35,40    R$ ... │
╰──────────────────────────────────╯
```

## ⚠️ Nota sobre Performance
O script faz chamadas sequenciais para as APIs. Se a internet estiver muito lenta, pode haver um pequeno atraso na atualização. Em versões futuras, recomenda-se o uso de asyncio para paralelizar as chamadas (ver Exemplo do Agregador Assíncrono).

### 👨‍🏫 O que ensinar (Pontos Chave):

1.  **Tratamento de Falhas (Resiliência):**
    * Observe que cada função de API tem seu próprio `try/except`. Se o Yahoo Finance cair, o painel **não** trava; ele mostra "Indisponível" na linha das ações, mas continua mostrando o Bitcoin. Isso é crucial para dashboards: uma parte não pode derrubar o todo.
2.  **APIs Wrapper (`yfinance`):**
    * Às vezes não precisamos chamar a API "na mão" (requests). Existem bibliotecas (wrappers) que facilitam o trabalho. O `yfinance` é o padrão ouro para dados de ações gratuitos em Python.
3.  **UX de Terminal (`rich`):**
    * Mostre como o uso do `Rich` transforma um script "preto e branco" chato em uma ferramenta que parece profissional. A classe `Live` evita que você tenha que ficar limpando a tela com `cls` manualmente, o que causa aquele efeito de "piscar".
