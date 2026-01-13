# 🔨 Scraper de Leilões (Selenium)

Este robô simula a automação de arremate em leilões. Ele navega por múltiplas páginas de resultados, entra no detalhe de cada lote e faz o download das fotos dos produtos para análise offline.

## 🎯 Desafios Técnicos Resolvidos
- **Paginação:** Loop infinito até que o botão "Próximo" desapareça.
- **Deep Scraping:** Entrar no detalhe (Nível 2) e voltar para a lista (Nível 1).
- **Download de Mídia:** Uso integrado de `requests` para salvar imagens.
- **Prevenção de Erros:** Estratégia para evitar *StaleElementReferenceException*.

## ⚙️ Instalação

```bash
pip install selenium webdriver-manager requests
```

## 🚀 Como Executar

Execute o script principal:

```bash
python scraper_leilao.py
```

O script irá:
- Abrir o **Google Chrome**
- Navegar pelo site de testes **WebScraper.io**
- Buscar por notebooks **"Macbook"** (ou termos similares)
- Salvar as imagens encontradas na pasta `Fotos_Leilao`,  
  nomeadas com **IDs fictícios de lote**

---

## ⚠️ Nota Ética

Este código foi configurado **exclusivamente para fins educacionais**  
e para rodar no site **WebScraper.io**, que foi criado especificamente para testes de scraping.

> 🚫 **Não utilize este script** em:
- Sites governamentais (ex: Receita Federal)
- Sites privados ou comerciais sem autorização

O uso indevido pode resultar em:
- Bloqueio permanente do seu IP
- Violação de termos de uso
- Consequências legais
```
