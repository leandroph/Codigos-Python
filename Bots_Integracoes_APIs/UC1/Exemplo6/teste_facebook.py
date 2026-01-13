import requests
import json

URL = "http://localhost:8000/webhook/leads"

leads_teste = [
    {
        "cenario": "LEAD PERFEITO (SP)",
        "dados": {
            "id_lead": "1001",
            "nome": "Ana Clara",
            "email": "ana@teste.com",
            "telefone": "(11) 98888-7777"  # Válido (DDD 11 + 9 + 8 digitos)
        }
    },
    {
        "cenario": "ERRO: TELEFONE FIXO",
        "dados": {
            "id_lead": "1002",
            "nome": "Empresa Velha",
            "email": "contato@loja.com",
            "telefone": "(11) 3333-4444"  # Inválido (Falta o 9, tem 10 digitos)
        }
    },
    {
        "cenario": "ERRO: FALTANDO DIGITO",
        "dados": {
            "id_lead": "1003",
            "nome": "João Curto",
            "email": "joao@teste.com",
            "telefone": "1198888777"  # Inválido (Tem 10 digitos)
        }
    }
]

print("📡 Simulando disparos do Facebook Ads...\n")

for caso in leads_teste:
    print(f"🔹 Enviando: {caso['cenario']}")

    response = requests.post(URL, json=caso['dados'])

    print(f"   Status HTTP: {response.status_code}")
    print(f"   Resposta: {response.json()}")
    print("-" * 40)

print("\n Teste finalizado. Verifique 'leads_ok.csv' e 'erro.log'.")