from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from pydantic import BaseModel, field_validator, ValidationError
import csv
import os
import re
from datetime import datetime

app = FastAPI()

ARQUIVO_SUCESSO = "leads_ok.csv"
ARQUIVO_ERRO = "erro.log"


# --- 1. MODELO DE VALIDAÇÃO (REGRA DE NEGÓCIO) ---

class FacebookLead(BaseModel):
    id_lead: str
    nome: str
    email: str
    telefone: str

    @field_validator('telefone')
    def validar_celular_br(cls, v):
        # Remove caracteres não numéricos (espaço, traço, parênteses)
        apenas_numeros = re.sub(r'\D', '', v)

        # REGRA: Deve ter 11 dígitos (2 DDD + 9 + 8 números)
        # E o terceiro dígito deve ser 9 (celular moderno)
        if len(apenas_numeros) != 11:
            raise ValueError('Telefone deve ter 11 dígitos (DDD + Número)')

        if apenas_numeros[2] != '9':
            raise ValueError('Telefone deve começar com 9 após o DDD')

        return apenas_numeros


# --- 2. FUNÇÕES DE PERSISTÊNCIA (BACKGROUND) ---

def salvar_csv_background(dados: dict):
    """Salva no CSV sem travar a resposta da API"""
    arquivo_existe = os.path.exists(ARQUIVO_SUCESSO)

    with open(ARQUIVO_SUCESSO, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=dados.keys())
        if not arquivo_existe:
            writer.writeheader()
        writer.writerow(dados)

    print(f" [Background] Lead {dados['nome']} salvo no CSV.")


def registrar_log_erro(payload_cru: dict, motivo: str):
    """Registra falhas em arquivo de texto"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{timestamp}] ERRO: {motivo} | DADOS: {payload_cru}\n"

    with open(ARQUIVO_ERRO, mode='a', encoding='utf-8') as f:
        f.write(linha)

    print(f" [Log] Erro registrado: {motivo}")


# --- 3. ENDPOINT (A ROTA) ---

@app.post("/webhook/leads")
async def receber_lead(request: Request, background_tasks: BackgroundTasks):
    # 1. Captura o JSON cru (para logar em caso de erro)
    try:
        payload = await request.json()
    except:
        raise HTTPException(status_code=400, detail="JSON Inválido")

    # 2. Tentativa de Validação (Síncrona - Rápida)
    try:
        # Tenta converter o JSON cru para o Modelo Validado
        lead_validado = FacebookLead(**payload)

    except ValidationError as e:
        # SE FALHAR: Loga o erro e retorna HTTP 400 (Bad Request)
        erros = e.errors()[0]['msg']
        registrar_log_erro(payload, erros)

        # O Facebook lerá isso e saberá que o lead foi rejeitado
        raise HTTPException(status_code=400, detail=f"Lead Inválido: {erros}")

    # 3. SE PASSAR: Agenda o salvamento e responde 200 OK
    background_tasks.add_task(salvar_csv_background, lead_validado.model_dump())

    return {"status": "recebido", "mensagem": "Lead aceito e em processamento"}

# Para rodar: uvicorn webhook_facebook:app --reload