# 🕵️‍♂️ Auditor Fiscal de PDFs (OCR/Regex)

Este projeto simula uma auditoria contábil automatizada. O script lê um lote de 50 Notas Fiscais em PDF, extrai os valores usando reconhecimento de texto e verifica matematicamente se o imposto (ISS) foi calculado corretamente (10%).

## 🎯 Objetivo
Identificar erros de cálculo em documentos fiscais que passariam despercebidos numa análise manual.

## 🛠️ Tecnologias
- **pdfplumber:** Extração de texto de PDFs (mais preciso que o PyPDF2).
- **RegEx (re):** Localização de padrões de texto (valores monetários).
- **Pandas:** Geração do relatório Excel final.

## ⚙️ Instalação
```bash
pip install pdfplumber pandas openpyxl reportlab
```

## 🚀 Como Usar

### 1️⃣ Gerar as Notas Fiscais

Como não podemos utilizar notas reais (dados sensíveis), execute o script de setup para criar **50 PDFs fictícios**.

> **Nota:**  
> O script gera **erros propositais em 5 notas** (múltiplos de 10) para testar a auditoria.

```bash
python setup_auditoria.py
```

---

### 2️⃣ Rodar a Auditoria

O robô irá ler arquivo por arquivo e comparar:
- O **valor escrito na nota**
- Com o **valor calculado corretamente**

```bash
python auditor_fiscal.py
```

---

## 📊 Resultado Esperado

O script deve:
- Processar **50 notas fiscais**
- Encontrar exatamente **5 divergências**:
  - `NF_010`
  - `NF_020`
  - `NF_030`
  - `NF_040`
  - `NF_050`

Ao final, será gerado o arquivo:

- **`Relatorio_Divergencias_Fiscais.xlsx`**

contendo a prova completa da auditoria.

---

## 📟 Exemplo de Log

```plaintext
🔍 Iniciando Auditoria Fiscal...
❌ DIVERGÊNCIA: NF_010.pdf | Lido: 125.0 | Correto: 250.0
❌ DIVERGÊNCIA: NF_020.pdf | Lido: 50.0 | Correto: 100.0
...
🚨 FORAM ENCONTRADAS 5 DIVERGÊNCIAS!
📄 Relatório salvo em: Relatorio_Divergencias_Fiscais.xlsx
```
