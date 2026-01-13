import requests
import json

BASE_URL = "http://localhost:8000/tarefas"

def imprimir_passo(titulo):
    print(f"\n🔹 {titulo} " + "-"*30)

# 1. CRIAR (POST)
imprimir_passo("1. CRIANDO TAREFAS")
tarefas_teste = [
    {"titulo": "Aprender FastAPI", "descricao": "Estudar rotas e pydantic"},
    {"titulo": "Comprar Café", "descricao": "Essencial para programar"},
    {"titulo": "", "descricao": "Teste Erro"} # Deve falhar (título vazio)
]

ids_criados = []

for t in tarefas_teste:
    resp = requests.post(BASE_URL, json=t)
    if resp.status_code == 201:
        dado = resp.json()
        print(f" Criado: ID {dado['id']} - {dado['titulo']}")
        ids_criados.append(dado['id'])
    else:
        print(f"⚠ Erro Esperado (Validação): {resp.text}")

# 2. LISTAR (GET)
imprimir_passo("2. LISTANDO TUDO")
resp = requests.get(BASE_URL)
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))

if not ids_criados:
    print(" Nenhuma tarefa criada. Abortando teste.")
    exit()

id_alvo = ids_criados[0] # Vamos manipular a primeira tarefa criada

# 3. ATUALIZAR (PATCH)
imprimir_passo(f"3. CONCLUINDO TAREFA ID {id_alvo}")
resp = requests.patch(f"{BASE_URL}/{id_alvo}/concluir")
print(f"Status: {resp.status_code}")
print(f"Retorno: {resp.json()}")

# 4. DELETAR (DELETE)
imprimir_passo(f"4. DELETANDO TAREFA ID {id_alvo}")
resp = requests.delete(f"{BASE_URL}/{id_alvo}")
if resp.status_code == 204:
    print(" Tarefa deletada com sucesso!")
else:
    print(f" Erro ao deletar: {resp.status_code}")

# 5. PROVA FINAL
imprimir_passo("5. PROVA DA PERSISTÊNCIA")
print("Verifique o arquivo 'banco_tarefas.json' na pasta. Os dados estão salvos lá!")