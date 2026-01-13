import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURAÇÕES ---
# Começamos pela página 1
URL_INICIAL = f"file:///{os.getcwd()}/busca_page_1.html".replace("\\", "/")
ARQUIVO_SAIDA = "clipping_techcorp.csv"
MAX_PAGINAS = 5


def iniciar_scraping():
    print(" Iniciando Monitoramento de Mídia...")

    dados_coletados = []

    # Configuração do Browser
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Descomente para rodar invisível
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(URL_INICIAL)
        pagina_atual = 1

        while pagina_atual <= MAX_PAGINAS:
            print(f"\n Processando PÁGINA {pagina_atual}...")

            # 1. Coletar os artigos da página atual
            artigos = driver.find_elements(By.CLASS_NAME, "news-card")

            if not artigos:
                print("    Nenhum artigo encontrado nesta página.")
                break

            for artigo in artigos:
                try:
                    titulo_el = artigo.find_element(By.CLASS_NAME, "news-title").find_element(By.TAG_NAME, "a")
                    data_el = artigo.find_element(By.CLASS_NAME, "news-date")

                    titulo = titulo_el.text
                    link = titulo_el.get_attribute("href")
                    data = data_el.text

                    # Salva na lista
                    dados_coletados.append({
                        "Data": data,
                        "Titulo": titulo,
                        "Link": link,
                        "Origem": "Portal Simulado"
                    })
                    print(f"   + Capturado: {titulo[:40]}...")

                except Exception as e:
                    print(f"    Erro ao ler artigo: {e}")

            # 2. Lógica de Paginação (Clicar em Próximo)
            try:
                # Tenta achar o botão "Próxima Página"
                # Usamos find_elements (plural) para verificar se existe sem dar erro
                botoes_proximo = driver.find_elements(By.CLASS_NAME, "btn-next")

                if botoes_proximo:
                    link_proximo = botoes_proximo[0]
                    url_destino = link_proximo.get_attribute("href")

                    print("    Indo para próxima página...")

                    # Em sites reais, clicaríamos: link_proximo.click()
                    # Como é arquivo local, navegar direto é mais seguro contra erros de path
                    driver.get(url_destino)

                    pagina_atual += 1
                    time.sleep(1)  # Espera humana/carregamento
                else:
                    print("    Botão 'Próxima' não encontrado. Fim da busca.")
                    break

            except Exception as e:
                print(f"    Erro na paginação: {e}")
                break

    finally:
        driver.quit()

        # 3. Exportar Relatório
        if dados_coletados:
            df = pd.DataFrame(dados_coletados)
            df.to_csv(ARQUIVO_SAIDA, index=False, sep=";", encoding="utf-8-sig")
            print("\n" + "=" * 40)
            print(f" SUCESSO! {len(df)} notícias coletadas.")
            print(f" Arquivo salvo: {ARQUIVO_SAIDA}")
        else:
            print(" Nenhuma notícia foi coletada.")


if __name__ == "__main__":
    iniciar_scraping()