# 🚨 Monitor de Preços com Alerta (Bot Sniper)

Este projeto é um robô de vigilância de preços. Ele acessa múltiplos e-commerces (simulados), extrai o preço de um produto desejado e compara com um "Preço Alvo".

Se encontrar uma oferta imperdível, ele sai do modo silencioso: **Toca um alarme sonoro** e exibe um **Popup na tela** do usuário.

## 🎯 Funcionalidades
- **Scraping Headless:** Navegação invisível em segundo plano.
- **Lógica de Comparação:** Identifica o menor preço entre várias lojas.
- **Alertas Multimídia:**
  - 🔊 Som (Beep de sistema).
  - 💬 Visual (Popup nativo do Windows/OS).

## 🛠️ Tecnologias
- **Selenium:** Extração de dados web.
- **Tkinter:** Interface gráfica para o Popup de alerta.
- **Winsound:** Alertas sonoros.

## ⚙️ Instalação

```bash
pip install selenium webdriver-manager
```

## 🚀 Como Executar

O projeto utiliza **sites simulados** (arquivos HTML locais) para garantir que você consiga testar o alerta  
sem depender da flutuação real de preços da internet.

---

### 1️⃣ Criar as Lojas (Setup)

Execute este script para gerar os **3 sites de teste** no seu computador:

```bash
python setup_lojas.py
```

**Cenário criado:**
- Loja A → **R$ 4.500,00**
- Loja B → **R$ 3.200,00**
- Loja C → **R$ 2.890,00**

---

### 2️⃣ Rodar o Monitor

O robô irá buscar notebooks **abaixo de R$ 3.000,00**.  
Como a **Loja C** possui esse preço, o alerta será disparado.

```bash
python monitor_precos.py
```

---

## 🧪 Resultado Esperado

Durante a execução, você verá:

- ✔️ Varredura das **3 lojas** exibida no terminal
- 🔊 **3 beeps sonoros** emitidos pelo computador
- 🪟 Uma janela *popup* com a mensagem:

```plaintext
OPORTUNIDADE ENCONTRADA!
Loja: DescontoZone - R$ 2.890,00
```
