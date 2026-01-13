import asyncio
import re
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# --- MODELOS DE DADOS ---

class InputDados(BaseModel):
    cep: str
    cnpj: str


class Endereco(BaseModel):
    logradouro: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    estado: str | None = None


class Empresa(BaseModel):
    razao_social: str | None = None
    nome_fantasia: str | None = None
    cnae_principal: str | None = None
    situacao_cadastral: str | None = None


class LeadEnriquecido(BaseModel):
    status: str
    cnpj_dados: Empresa
    endereco_dados: Endereco
    mensagem: str


# --- FUNÇÕES AUXILIARES (CONSULTAS EXTERNAS) ---

def limpar_texto(texto: str) -> str:
    """Remove pontos, traços e barras (deixa apenas números)"""
    return re.sub(r'\D', '', texto)


async def consultar_viacep(cep: str, client: httpx.AsyncClient):
    """Consulta API pública do ViaCEP"""
    cep_limpo = limpar_texto(cep)
    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"

    try:
        resp = await client.get(url, timeout=5)
        if resp.status_code == 200:
            dados = resp.json()
            if "erro" in dados: return None  # CEP não existe
            return {
                "logradouro": dados.get("logradouro"),
                "bairro": dados.get("bairro"),
                "cidade": dados.get("localidade"),
                "estado": dados.get("uf")
            }
    except:
        return None
    return None


async def consultar_brasilapi(cnpj: str, client: httpx.AsyncClient):
    """Consulta API pública BrasilAPI (Dados de CNPJ)"""
    cnpj_limpo = limpar_texto(cnpj)
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"

    try:
        resp = await client.get(url, timeout=5)
        if resp.status_code == 200:
            dados = resp.json()
            return {
                "razao_social": dados.get("razao_social"),
                "nome_fantasia": dados.get("nome_fantasia"),
                "cnae_principal": dados.get("cnae_fiscal_descricao"),
                "situacao_cadastral": dados.get("descricao_situacao_cadastral")
            }
    except:
        return None
    return None


# --- ROTA PRINCIPAL ---

@app.post("/enriquecer-lead", response_model=LeadEnriquecido)
async def enriquecer_dados(lead: InputDados):
    print(f" Enriquecendo dados para: CEP {lead.cep} | CNPJ {lead.cnpj}")

    async with httpx.AsyncClient() as client:
        # Dispara as duas consultas ao mesmo tempo (Paralelismo)
        tarefa_cep = consultar_viacep(lead.cep, client)
        tarefa_cnpj = consultar_brasilapi(lead.cnpj, client)

        # Aguarda ambas terminarem
        resultado_cep, resultado_cnpj = await asyncio.gather(tarefa_cep, tarefa_cnpj)

    # Montagem da resposta
    status_op = "Sucesso"
    msg = "Dados encontrados."

    if not resultado_cep and not resultado_cnpj:
        status_op = "Falha"
        msg = "Não foi possível localizar dados para o CEP nem para o CNPJ informados."
    elif not resultado_cep:
        msg = "CNPJ localizado, mas CEP não encontrado."
    elif not resultado_cnpj:
        msg = "CEP localizado, mas CNPJ não encontrado."

    return {
        "status": status_op,
        "mensagem": msg,
        "cnpj_dados": resultado_cnpj if resultado_cnpj else {},
        "endereco_dados": resultado_cep if resultado_cep else {}
    }

# Para rodar: uvicorn enriquecedor:app --reload