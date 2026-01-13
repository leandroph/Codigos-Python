from fastapi import FastAPI, BackgroundTasks, Request
from pydantic import BaseModel, EmailStr, ValidationError, field_validator
import re
import json
import time
from datetime import datetime

app = FastAPI()


# --- 1. MODELO DE DADOS (PYDANTIC) ---
# Aqui definimos as regras de negócio. Se não passar aqui, é inválido.

class LeadSchema(BaseModel):
    nome: str
    email: EmailStr  # Valida formato de e-mail automaticamente
    telefone: str

    # Validador personalizado para telefone (Apenas dígitos, 10 ou 11 números)
    @field_validator('telefone')
    def validar_telefone(cls, v):
        # Remove tudo que não é numero
        numeros = re.sub(r'\D', '', v)
        if not (10 <= len(numeros) <= 11):
            raise ValueError('Telefone deve ter 10 ou 11 dígitos (com DDD)')
        return numeros


# --- 2. LÓGICA DE NEGÓCIO (BACKEND) ---

def enviar_para_crm(lead: LeadSchema):
    """
    Simula o envio para RD Station ou HubSpot.
    Isso geralmente demora (IO bound).
    """
    print(f" Enviando lead {lead.email} para o CRM...")
    time.sleep(2)  # Simula latência de rede
    print(f" Lead {lead.nome} cadastrado no CRM com Sucesso!")


def salvar_rejeitado(dados_brutos: dict, erro: str):
    """
    Salva leads inválidos em um arquivo de log para auditoria.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = json.dumps({"data": timestamp, "payload": dados_brutos, "motivo": erro})

    with open("leads_rejeitados.txt", "a", encoding="utf-8") as f:
        f.write(linha + "\n")
    print(f" Lead rejeitado salvo em disco. Motivo: {erro}")


def processar_lead_background(dados_brutos: dict):
    """
    Função Orquestradora que roda EM SEGUNDO PLANO.
    """
    print("\n⚙ Processando novo webhook...")

    try:
        # Tenta converter o dicionário bruto para o Schema validado
        lead_validado = LeadSchema(**dados_brutos)

        # Se passou na linha acima, é válido!
        enviar_para_crm(lead_validado)

    except ValidationError as e:
        # Se falhou na validação do Pydantic
        erros_formatados = e.errors()[0]['msg']  # Pega a primeira mensagem de erro
        salvar_rejeitado(dados_brutos, erros_formatados)
    except Exception as e:
        salvar_rejeitado(dados_brutos, f"Erro sistêmico: {str(e)}")


# --- 3. A ROTA (API) ---

@app.post("/webhook/facebook")
async def receber_lead(request: Request, background_tasks: BackgroundTasks):
    """
    Endpoint que o Facebook chama.
    Deve ser EXTREMAMENTE rápido.
    """
    # 1. Receber o JSON cru
    try:
        payload = await request.json()
    except:
        return {"status": "erro", "msg": "JSON inválido"}

    # 2. Agendar processamento (Fire and Forget)
    # O FastAPI responde o return abaixo IMEDIATAMENTE, e depois roda a função
    background_tasks.add_task(processar_lead_background, payload)

    # 3. Responder 200 OK para o Facebook não reenviar
    return {"status": "recebido", "msg": "Processamento iniciado"}

# Para rodar: uvicorn middleware_leads:app --reload