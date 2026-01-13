import time
import requests
import yfinance as yf
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel

# --- CONFIGURAÇÕES ---
# Simulação de carteira (Quantas unidades você tem)
MEUS_ATIVOS = {
    "BTC": 0.05,  # 0.05 Bitcoin
    "PETR4": 100,  # 100 Ações da Petrobras
    "VALE3": 50,  # 50 Ações da Vale
    "USD": 500  # 500 Dólares
}

console = Console()


def get_crypto_binance():
    """Consulta API da Binance para Bitcoin (BTCBRL)"""
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCBRL"
        response = requests.get(url, timeout=5)
        dados = response.json()
        return float(dados['price'])
    except Exception as e:
        return None


def get_moedas_economia():
    """
    Consulta Dólar e Euro.
    Usamos a AwesomeAPI (que espelha o Banco Central) pois é JSON direto e mais estável.
    """
    try:
        url = "https://lb.awesomeapi.com.br/last/USD-BRL,EUR-BRL"
        response = requests.get(url, timeout=5)
        dados = response.json()
        return {
            "USD": float(dados['USDBRL']['bid']),
            "EUR": float(dados['EURBRL']['bid'])
        }
    except:
        return {"USD": 0.0, "EUR": 0.0}


def get_acoes_b3(tickers):
    """Consulta Yahoo Finance para ações brasileiras"""
    try:
        # Adiciona .SA para identificar bolsa brasileira
        tickers_sa = [f"{t}.SA" for t in tickers]
        dados = yf.Tickers(" ".join(tickers_sa))

        precos = {}
        for t in tickers:
            # Tenta pegar o preço atual com segurança
            info = dados.tickers[f"{t}.SA"].info
            # currentPrice ou regularMarketPrice dependendo da versão
            preco = info.get('currentPrice') or info.get('regularMarketPreviousClose')
            precos[t] = preco
        return precos
    except:
        return {t: 0.0 for t in tickers}


def gerar_tabela():
    """Monta a Tabela Visual com os dados atualizados"""

    # 1. Coleta de Dados (Ocorre em tempo real)
    preco_btc = get_crypto_binance()
    moedas = get_moedas_economia()
    acoes = get_acoes_b3(["PETR4", "VALE3"])

    # 2. Criação da Tabela Rich
    table = Table(title=f" MONITOR DE MERCADO | {datetime.now().strftime('%H:%M:%S')}")

    table.add_column("Ativo", justify="left", style="cyan", no_wrap=True)
    table.add_column("Preço Unit. (R$)", justify="right", style="green")
    table.add_column("Variação", justify="right", style="magenta")  # (Simulada para layout)
    table.add_column("Meu Saldo (R$)", justify="right", style="gold1")

    # --- LINHA 1: CRIPTO ---
    saldo_btc = (preco_btc * MEUS_ATIVOS["BTC"]) if preco_btc else 0
    txt_btc = f"R$ {preco_btc:,.2f}" if preco_btc else "Erro API"
    table.add_row("Bitcoin (BTC)", txt_btc, "---", f"R$ {saldo_btc:,.2f}")

    # --- LINHA 2: MOEDAS ---
    saldo_usd = (moedas["USD"] * MEUS_ATIVOS["USD"])
    table.add_row("Dólar (USD)", f"R$ {moedas['USD']:.2f}", "---", f"R$ {saldo_usd:,.2f}")
    table.add_row("Euro (EUR)", f"R$ {moedas['EUR']:.2f}", "---", "-")

    # --- LINHA 3: AÇÕES ---
    for ticker, preco in acoes.items():
        if preco:
            saldo = preco * MEUS_ATIVOS.get(ticker, 0)
            table.add_row(f"Ação {ticker}", f"R$ {preco:.2f}", "---", f"R$ {saldo:,.2f}")
        else:
            table.add_row(f"Ação {ticker}", "Indisponível", "-", "-")

    return Panel(table, title="Dashboard Financeiro", border_style="blue")


def main():
    print("Iniciando Dashboard... (Pressione Ctrl+C para sair)")

    # Live do Rich permite atualizar o terminal sem 'piscar' a tela (flicker)
    with Live(gerar_tabela(), refresh_per_second=1) as live:
        while True:
            # Atualiza os dados
            painel = gerar_tabela()
            live.update(painel)

            # Espera 30 segundos (mostrando contagem regressiva seria possível,
            # mas aqui vamos apenas dormir para simplificar)
            time.sleep(30)


if __name__ == "__main__":
    main()