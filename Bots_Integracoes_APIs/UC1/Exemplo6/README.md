# 🛡️ Middleware de Validação de Leads (Facebook Ads Webhook)


Este projeto é um **API Gateway de Alta Performance** projetado para processar leads vindos de campanhas de publicidade (Facebook Ads, Google Forms, TikTok).

O objetivo principal é atuar como uma **Barreira de Qualidade (Quality Gate)**: o sistema intercepta os dados em tempo real, valida se o telefone é um celular brasileiro válido (com DDD e 9 dígitos) e decide o destino do lead instantaneamente.

---

## 📉 O Problema de Negócio

Em campanhas de Marketing Digital, é comum receber dados "sujos":
1.  Usuários digitam telefones fixos em formulários que exigem WhatsApp.
2.  Usuários esquecem dígitos ou o DDD.
3.  **O Custo:** Enviar leads inválidos para o time de vendas (SDRs) desperdiça tempo e dinheiro.
4.  **O Requisito Técnico:** O Facebook exige uma resposta HTTP em **menos de 2 segundos**, caso contrário, ele considera falha e reenvia o lead (duplicidade).

## 💡 A Solução (Arquitetura)

Implementamos uma estratégia de **Validação Síncrona** com **Processamento Assíncrono**:

1.  **Entrada:** Recebemos o JSON do Facebook.
2.  **Gatekeeper (Síncrono):** O Pydantic valida o formato do telefone (Regex).
    * ❌ **Se inválido:** Retornamos `HTTP 400 Bad Request` imediatamente. O Facebook é notificado do erro e o dado ruim é logado para auditoria.
    * ✅ **Se válido:** Retornamos `HTTP 200 OK` imediatamente.
3.  **Persistência (Assíncrono):** Uma *Background Task* assume o controle e salva o lead no banco de dados (simulado por CSV) sem bloquear a resposta para o Facebook.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função no Projeto |
| :--- | :--- |
| **FastAPI** | Framework Web assíncrono de alta performance. |
| **Pydantic** | Validação de dados rigorosa e sanitização (limpeza de strings). |
| **BackgroundTasks** | Gerenciamento de tarefas em segundo plano (evita timeout). |
| **Python 3.10+** | Linguagem base com Type Hints. |

---

## ⚙️ Instalação e Configuração

### 1. Clonar e Instalar Dependências
Certifique-se de ter o Python instalado. No terminal, execute:

```bash
pip install fastapi uvicorn pydantic aiofiles requests
```

## 🚀 Como Executar (Guia Passo a Passo)
Para simular o ambiente real (Servidor vs. Cliente), utilizaremos a Regra dos Dois Terminais.

**Passo 1: Subir o Servidor (API)**
Abra o primeiro terminal e inicie o middleware. Ele ficará aguardando os webhooks.

```Bash
uvicorn webhook_facebook:app --reload
```

Saída esperada: `Uvicorn running on http://127.0.0.1:8000`

**Passo 2: Disparar Simulação (Facebook)**
Abra um segundo terminal (não feche o primeiro). Execute o script que simula o envio de 3 leads com qualidades diferentes.
```Bash
python teste_facebook.py
```

## 📊 Análise dos Resultados
Após a execução, o sistema terá tomado decisões diferentes para cada tipo de dado. Verifique os arquivos gerados na pasta:

**1. Leads Aceitos (leads_ok.csv)**
Apenas leads prontos para o time de vendas.
```text
id_lead,nome,email,telefone
1001,Ana Clara,ana@teste.com,11988887777
```

_Note que o telefone foi "limpo" (sem parênteses/traços) antes de salvar._

**2. Leads Rejeitados (erro.log)**
Leads que falharam na validação. O arquivo registra o motivo e o JSON original para auditoria (caso o marketing queira tentar contato via e-mail).
```text
[Data/Hora] ERRO: Telefone deve ter 11 dígitos | DADOS: {'nome': 'João Curto', ...}
[Data/Hora] ERRO: Telefone deve começar com 9 | DADOS: {'nome': 'Empresa Velha', ...}
```


