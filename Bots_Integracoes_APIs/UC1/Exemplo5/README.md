# 📝 API de Gestão de Tarefas (CRUD Persistente)


Este projeto é um backend completo para um aplicativo To-Do List. Ele demonstra os quatro pilares do desenvolvimento de APIs RESTful:
1.  **Create (POST):** Criar novos registros.
2.  **Read (GET):** Ler registros.
3.  **Update (PATCH):** Atualizar status de registros.
4.  **Delete (DELETE):** Remover registros.

Diferente de APIs que guardam dados na memória RAM (e perdem tudo ao reiniciar), esta API implementa uma **Camada de Persistência em Arquivo**. Ela gerencia um arquivo `banco_tarefas.json` localmente, funcionando como um banco de dados leve e portátil.

## 🛠️ Tecnologias

- **FastAPI:** Roteamento e tratamento HTTP.
- **Pydantic:** Validação de dados (impede tarefas sem título).
- **JSON:** Armazenamento de dados.

## ⚙️ Instalação

```bash
pip install fastapi uvicorn pydantic requests
```

## 🚀 Como Executar
* Passo 1: Iniciar o Backend (Terminal 1)
```Bash
uvicorn api_tarefas:app --reload
```
O arquivo banco_tarefas.json será criado automaticamente na primeira execução.
* Passo 2: Testar o Ciclo de Vida (Terminal 2)
```Bash
python teste_crud.py
```

## 📊 Endpoints Disponíveis

```
Método	URL	                Descrição
GET	/tarefas	        Retorna todas as tarefas salvas.
POST	/tarefas	        Cria uma nova tarefa. Requer JSON com titulo.
PATCH	/tarefas/{id}/concluir	Marca a tarefa como concluida: true.
DELETE	/tarefas/{id}	        Remove a tarefa do arquivo permanentemente.
```
## 🧪 Exemplo de Armazenamento (JSON)
Ao usar a API, o arquivo banco_tarefas.json ficará assim:
```JSON
[
    {
        "id": 2,
        "titulo": "Comprar Café",
        "descricao": "Essencial para programar",
        "concluida": false
    }
]
```
## 🧠 Desafios Resolvidos
* **Validação**: Tente enviar um título vazio "". O Pydantic rejeitará com erro 422 automaticamente.
* **Tratamento de Erros**: Tente deletar o ID 999. A API retornará erro 404 (Not Found) em vez de quebrar o código.
* **Persistência**: Pode parar o servidor (Ctrl+C) e iniciar de novo. Suas tarefas continuarão lá.