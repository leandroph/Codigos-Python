import json
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

ARQUIVO_DB = "banco_tarefas.json"


# --- 1. MODELOS DE DADOS (Pydantic) ---

class TarefaInput(BaseModel):
    titulo: str = Field(..., min_length=3, description="O título não pode ser vazio ou muito curto")
    descricao: Optional[str] = None


class TarefaOutput(BaseModel):
    id: int
    titulo: str
    descricao: str | None
    concluida: bool


# --- 2. CAMADA DE PERSISTÊNCIA (Lida com o JSON) ---

def carregar_tarefas() -> List[dict]:
    """Lê o arquivo JSON e retorna a lista. Se não existir, retorna lista vazia."""
    if not os.path.exists(ARQUIVO_DB):
        return []
    try:
        with open(ARQUIVO_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def salvar_tarefas(tarefas: List[dict]):
    """Escreve a lista atualizada no arquivo JSON."""
    with open(ARQUIVO_DB, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)


# --- 3. ENDPOINTS DA API (CRUD) ---

@app.post("/tarefas", response_model=TarefaOutput, status_code=201)
def criar_tarefa(nova_tarefa: TarefaInput):
    db = carregar_tarefas()

    # Gera um ID novo (Pega o último ID + 1, ou 1 se for a primeira)
    novo_id = 1 if not db else db[-1]["id"] + 1

    tarefa_dict = {
        "id": novo_id,
        "titulo": nova_tarefa.titulo,
        "descricao": nova_tarefa.descricao,
        "concluida": False  # Começa sempre pendente
    }

    db.append(tarefa_dict)
    salvar_tarefas(db)
    return tarefa_dict


@app.get("/tarefas", response_model=List[TarefaOutput])
def listar_tarefas():
    return carregar_tarefas()


@app.patch("/tarefas/{tarefa_id}/concluir", response_model=TarefaOutput)
def marcar_como_concluida(tarefa_id: int):
    db = carregar_tarefas()

    for tarefa in db:
        if tarefa["id"] == tarefa_id:
            tarefa["concluida"] = True
            salvar_tarefas(db)
            return tarefa

    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


@app.delete("/tarefas/{tarefa_id}", status_code=204)
def deletar_tarefa(tarefa_id: int):
    db = carregar_tarefas()

    # Filtra mantendo apenas as tarefas que NÃO são a deletada
    novo_db = [t for t in db if t["id"] != tarefa_id]

    if len(novo_db) == len(db):
        raise HTTPException(status_code=404, detail="Tarefa não encontrada para deletar")

    salvar_tarefas(novo_db)
    return  # Retorna 204 No Content (sucesso sem corpo)

# Rodar: uvicorn api_tarefas:app --reload