import requests
import time

URL = "http://localhost:8000/webhook/facebook"

# Cenários de Teste
leads_teste = [
    # Cenário 1: Lead Perfeito
    {
        "nome": "João Sucesso",
        "email": "joao@empresa.com",
        "telefone": "(11) 99999-8888"
    },
    # Cenário 2: E-mail Inválido
    {
        "nome": "Maria Erro Email",
        "email": "maria#empresa.com",  # Falta @
        "telefone": "11999998888"
    },
    # Cenário 3: Telefone Curto
    {
        "nome": "Carlos Erro Fone",
        "email": "carlos@empresa.com",
        "telefone": "123"  # Inválido
    }
]

print("📡 Disparando Webhooks simulados...")

for lead in leads_teste:
    inicio = time.time()
    response = requests.post(URL, json=lead)
    fim = time.time()

    tempo_resposta = (fim - inicio) * 1000  # ms

    print(f" Enviado: {lead['nome']}")
    print(f"   🔙 Status API: {response.status_code} | Tempo: {tempo_resposta:.2f}ms")
    print("-" * 30)

print(" Disparos concluídos. Verifique o terminal do servidor e o arquivo de rejeitados.")