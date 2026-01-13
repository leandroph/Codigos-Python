import asyncio
import time
import httpx
from fastapi import FastAPI
import uvicorn

app = FastAPI()


# --- PARTE 1: SIMULAÇÃO DAS APIS LENTAS (SERVIÇOS EXTERNOS) ---
# Imagine que estes endpoints estão em servidores diferentes ao redor do mundo.

@app.get("/mock/acoes")
async def api_acoes():
    # Simula demora de 1.5 segundos
    await asyncio.sleep(1.5)
    return {"PETR4": 30.50, "VALE3": 68.20, "ITUB4": 32.10}


@app.get("/mock/cripto")
async def api_cripto():
    # Simula demora de 1.0 segundo
    await asyncio.sleep(1.0)
    return {"BTC": 250000.00, "ETH": 12000.00}


@app.get("/mock/tesouro")
async def api_tesouro():
    # Simula demora de 2.0 segundos (O mais lento de todos)
    await asyncio.sleep(2.0)
    return {"Selic": "11.75%", "IPCA+2045": "6.0%"}


# --- PARTE 2: O AGREGADOR ASSÍNCRONO (NOSSO ROBÔ) ---

@app.get("/carteira")
async def consultar_carteira():
    inicio = time.time()

    print("🚀 Iniciando consultas paralelas...")

    # URL base onde o próprio servidor está rodando
    base_url = "http://localhost:8000"

    async with httpx.AsyncClient() as client:
        # A MÁGICA ACONTECE AQUI: asyncio.gather
        # Ele dispara as 3 requisições ao mesmo tempo e espera todas voltarem.

        tarefa_1 = client.get(f"{base_url}/mock/acoes")
        tarefa_2 = client.get(f"{base_url}/mock/cripto")
        tarefa_3 = client.get(f"{base_url}/mock/tesouro")

        # O await aqui trava apenas para esperar o GRUPO terminar
        respostas = await asyncio.gather(tarefa_1, tarefa_2, tarefa_3)

        # Extraindo os dados dos objetos de resposta
        dados_acoes = respostas[0].json()
        dados_cripto = respostas[1].json()
        dados_tesouro = respostas[2].json()

    fim = time.time()
    tempo_total = fim - inicio

    return {
        "status": "Sucesso",
        "tempo_processamento": f"{tempo_total:.2f} segundos",
        "mensagem": "Note que o tempo total foi ditado apenas pela requisição mais lenta (2s), não pela soma (4.5s)!",
        "carteira_consolidada": {
            "Acoes": dados_acoes,
            "Criptomoedas": dados_cripto,
            "Renda_Fixa": dados_tesouro
        }
    }


# Bloco para rodar via python direto (Opcional, pode rodar via terminal também)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)