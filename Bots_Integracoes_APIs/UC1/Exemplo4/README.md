# 💎 Enriquecedor de Leads (Gateway de APIs)

> **Status:** Funcional ✅ | **Conceito:** Data Enrichment | **Tipo:** API Gateway

Este projeto é uma API Backend que atua como facilitadora para preenchimento de cadastros. Ela recebe dados parciais (apenas chaves primárias como CEP e CNPJ) e consulta múltiplas fontes públicas externas para devolver um objeto de dados completo.

Isso reduz a fricção em formulários de cadastro, pois o usuário precisa digitar menos informações, enquanto o sistema garante a precisão dos dados (endereço oficial dos Correios e Razão Social oficial da Receita).

## 🧩 Arquitetura

O sistema utiliza o padrão **API Gateway Aggregator**:
1.  Recebe a requisição do cliente.
2.  Dispara requisições paralelas (Async) para:
    * **ViaCEP:** Para normalização de endereço.
    * **BrasilAPI:** Para dados cadastrais da empresa (CNPJ).
3.  Consolida as respostas.
4.  Entrega o JSON unificado.

## 🛠️ Tecnologias

- **FastAPI:** Framework principal.
- **HTTPX:** Cliente HTTP Assíncrono (para não travar o servidor enquanto espera as APIs externas).
- **Pydantic:** Para garantir que a saída do JSON seja sempre padronizada, mesmo que uma das APIs falhe.

## ⚙️ Instalação

```bash
pip install fastapi uvicorn httpx pydantic requests
```

## 🚀 Como Executar
Lembre-se da Regra dos Dois Terminais:

Passo 1: Iniciar a API (Terminal 1)
```Bash
uvicorn enriquecedor:app --reload
````
Aguarde o servidor subir na porta 8000.

Passo 2: Testar o Enriquecimento (Terminal 2)
```Bash
python teste_cliente.py
```

## 📊 Exemplo de Retorno
Se você enviar o CEP da Praça da Sé e o CNPJ do Banco do Brasil, receberá:

```JSON

{
    "status": "Sucesso",
    "mensagem": "Dados encontrados.",
    "cnpj_dados": {
        "razao_social": "BANCO DO BRASIL SA",
        "nome_fantasia": "DIRECAO GERAL",
        "situacao_cadastral": "ATIVA"
    },
    "endereco_dados": {
        "logradouro": "Praça da Sé",
        "bairro": "Sé",
        "cidade": "São Paulo",
        "estado": "SP"
    }
}
```

## ⚠️ Nota sobre APIs Públicas
Este projeto depende da disponibilidade da ViaCEP e BrasilAPI. Ambas são gratuitas, mas possuem limites de requisições por minuto. Para uso em produção de alta escala, recomenda-se implementar cache (Redis) ou contratar versões pagas.