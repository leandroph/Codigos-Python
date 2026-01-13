# 📠 Preenchedor de Sistemas Legados (Data Entry)

Este robô automatiza a tarefa repetitiva de transferir dados de uma planilha Excel para um formulário web antigo que não possui API de integração.

Ele lida com os desafios comuns de interfaces legadas: menus dropdown, checkboxes de estado e captura de mensagens de confirmação.

## 🎯 Funcionalidades
- **Leitura de Excel:** Itera linha a linha da base de dados.
- **Interação Complexa:**
  - ✨ **Dropdowns:** Mapeia nomes do Excel para códigos do sistema (`TI` -> `TI`, `Recursos Humanos` -> `RH`).
  - ☑️ **Checkboxes:** Verifica o estado atual antes de clicar (evita desmarcar o que já estava certo).
- **Validação:** Lê a mensagem de "Sucesso" na tela antes de prosseguir para o próximo registro.

## 🛠️ Tecnologias
- **Selenium:** Para interagir com o formulário Web.
- **Pandas:** Para ler os dados do Excel.

## ⚙️ Instalação

```bash
pip install selenium pandas openpyxl webdriver-manager
```

## 🚀 Como Executar

O projeto cria um **"Sistema Legado" simulado** (arquivo HTML local) para garantir que o teste funcione  
sem depender de sistemas externos reais.

---

### ▶️ Passo 1: Criar o Sistema e os Dados

Execute o script de setup para gerar:
- A planilha `funcionarios.xlsx`
- O sistema legado simulado `sistema_rh_legado.html`

```bash
python setup_legado.py
```

---

### ▶️ Passo 2: Executar o Robô

Execute o robô de **data entry**.  
Ele irá:
- Abrir o navegador
- Realizar o login no sistema
- Preencher automaticamente os dados dos funcionários

```bash
python robo_data_entry.py
```

---

## 🧪 Resultado Esperado

Durante a execução, o terminal exibirá o progresso do robô:

```plaintext
🤖 Iniciando Data Entry...
🔄 Processando: Carlos Drummond... ✅ OK! Msg: REGISTRO SALVO COM SUCESSO (ID: 823)
🔄 Processando: Cecília Meireles... ✅ OK! Msg: REGISTRO SALVO COM SUCESSO (ID: 102)
...
```
