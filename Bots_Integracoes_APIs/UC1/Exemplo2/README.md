# 📨 Middleware de Validação de Leads (Webhook Assíncrono)

> **Status:** Funcional ✅ | **Framework:** FastAPI | **Foco:** Performance & Background Tasks

Este projeto é uma **API Gateway** desenhada para receber dados de campanhas de anúncios (como Facebook Leads ou Google Forms), validar a qualidade dos dados em tempo real e encaminhá-los para o CRM apenas se estiverem corretos.

O diferencial desta aplicação é o uso de **Processamento Assíncrono (Background Tasks)**: a API responde instantaneamente à plataforma de anúncios (evitando erros de *timeout*), enquanto processa, valida e salva os dados em segundo plano.



## 🎯 O Problema Resolvido
Plataformas como o Facebook exigem que seu servidor responda em menos de **1 ou 2 segundos**. Se você tentar validar e salvar o lead no CRM (que é lento) durante a requisição, o Facebook assume que houve erro e reenvia o lead, criando duplicidade.

**Nossa Solução:**
1. Recebemos o JSON.
2. Respondemos `200 OK` em milissegundos.
3. Validamos e enviamos para o CRM em uma "thread" separada.

## 🛠️ Tecnologias

- **FastAPI:** Para criar a API de alta performance.
- **Uvicorn:** Servidor ASGI para rodar a aplicação.
- **Pydantic:** Para validação rigorosa de dados (Schema).
- **Requests:** Para simular o envio dos webhooks (lado do cliente).

## ⚙️ Instalação

Certifique-se de ter o Python instalado e execute:

```bash
pip install fastapi uvicorn pydantic email-validator requests
```

## 🚀 Como Executar (Importante!)

Para que este projeto funcione, você precisa operar com **DOIS TERMINAIS abertos simultaneamente**.  
Um terminal mantém o servidor ativo e o outro dispara os testes.

---

### ▶️ Passo 1: Iniciar o Servidor (Terminal 1)

Neste terminal, a API ficará rodando e **“ouvindo” requisições**.

```bash
uvicorn middleware_leads:app --reload
```

Aguarde aparecer a mensagem:

Uvicorn running on http://127.0.0.1:8000


👉 Não feche este terminal.

### ▶️ Passo 2: Disparar os Testes (Terminal 2)

Abra uma nova janela de terminal (sem fechar a anterior) e execute o script que simula o Facebook enviando leads.

```bash
python teste_disparos.py
```

## 📊 Estrutura de Arquivos
```
.
├── middleware_leads.py    # O SERVIDOR (Lógica da API e Validação)
├── teste_disparos.py      # O CLIENTE (Simulador de Webhooks)
├── leads_rejeitados.txt   # LOG (Gerado automaticamente com leads inválidos)
└── README.md              # Documentação
```

## 🕵️‍♂️ Validando os Resultados
1. ✅ Leads Válidos: Aparecerão no Terminal 1 Mensagem exibida:
`✅ Lead cadastrado no CRM com Sucesso!`

2. ❌ Leads Inválidos: Serão salvos no arquivo: `leads_rejeitados.txt` Com o motivo do erro, por exemplo:
E-mail sem @ Telefone com poucos dígitos

## 🆘 Solução de Problemas Comuns
1. Erro: `[WinError 10061] Nenhuma conexão pôde ser feita...`

    * Causa: Você executou teste_disparos.py sem ter iniciado o servidor (uvicorn) ou fechou o terminal do servidor.

    * Solução:
Volte ao Passo 1 e garanta que o servidor está rodando em uma janela separada.

2. `Erro: 405 Method Not Allowed`

    * Causa:
Você tentou acessar a URL pelo navegador (GET), mas a rota é um Webhook (POST).

    * Solução: Use o script teste_disparos.py.
Ou ferramentas como Postman / Insomnia para enviar uma requisição POST.
