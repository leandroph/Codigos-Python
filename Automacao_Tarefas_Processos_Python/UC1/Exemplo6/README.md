# 🧹 Organizador de Downloads Contextual

Este projeto automatiza a limpeza de pastas caóticas. Diferente dos organizadores comuns que separam apenas por extensão (.pdf, .docx), este script lê o **nome do arquivo** para entender seu conteúdo e classificá-lo na pasta correta.

## 🧠 Lógica de Classificação

O robô segue uma **hierarquia de decisão**:

1.  **Análise Semântica (Prioridade Alta):**
    * Se o nome contém *"contrato", "proposta", "minuta"* -> Move para **📂 Comercial**.
    * Se o nome contém *"fatura", "boleto", "comprovante"* -> Move para **📂 Financeiro**.
    * Se o nome contém *"relatorio", "dashboard"* -> Move para **📂 Relatórios**.

2.  **Análise de Tipo (Prioridade Média):**
    * Se não atendeu às regras acima, mas é imagem (*.jpg, .png*) -> Move para **📂 Mídia**.

3.  **Triagem (Prioridade Baixa):**
    * Qualquer arquivo que não se encaixe nas regras acima -> Move para **📂 Triagem** (para o usuário revisar manualmente depois).

## 🚀 Como Usar

### 1. Criar o Caos (Simulação)
Execute o script abaixo para criar uma pasta cheia de arquivos desorganizados:
```bash
python setup_downloads.py
```

### 2️. Organizar a Bagunça

Execute o script principal:

```bash
python organizador_contextual.py
```

---

## 📂 Estrutura Resultante

Após a execução, a pasta `Downloads_Bagunça` ficará assim:

```plaintext
Downloads_Bagunça/
├── Comercial/
│   ├── Contrato_Prestacao_Servicos.pdf
│   └── proposta_final.docx
├── Financeiro/
│   ├── Fatura_Vivo.pdf
│   └── boleto_faculdade.pdf
├── Mídia/
│   ├── foto_confraternizacao.jpg
│   └── logo.png
└── Triagem/
    ├── setup_instalador.exe
    └── anotacoes.txt
```
