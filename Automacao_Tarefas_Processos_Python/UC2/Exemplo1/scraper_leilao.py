import time
import os
import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURAÇÕES ---
TERMO_BUSCA = "Aspire"
PASTA_IMAGENS = Path("Fotos_Leilao")
PASTA_IMAGENS.mkdir(exist_ok=True)

# URL de exemplo (Como a Receita tem CAPTCHA, usaremos um site de treino de e-commerce
# que simula perfeitamente a estrutura de lista/detalhe de um leilão)
URL_ALVO = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"


def baixar_imagem(url_imagem, nome_arquivo):
    """Faz o download da imagem via HTTP (Requests) para não depender do browser."""
    try:
        # Sites de leilão as vezes usam caminhos relativos (/img/foto.jpg)
        if not url_imagem.startswith("http"):
            url_imagem = "https://webscraper.io" + url_imagem

        resposta = requests.get(url_imagem, stream=True)
        if resposta.status_code == 200:
            caminho_final = PASTA_IMAGENS / f"{nome_arquivo}.jpg"
            with open(caminho_final, 'wb') as f:
                f.write(resposta.content)
            return True
    except Exception as e:
        print(f"    Erro ao baixar imagem: {e}")
    return False


def iniciar_robo():
    print(" Iniciando Robô de Leilão...")

    # Setup do Chrome
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Descomente para rodar em segundo plano
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(URL_ALVO)
        print(f" Acessando site e buscando por: {TERMO_BUSCA}")

        # --- SIMULAÇÃO DA BUSCA (Se fosse um site real) ---
        # No site de treino, já vamos direto para a categoria, mas a lógica seria:
        # campo_busca = driver.find_element(By.ID, "search_box")
        # campo_busca.send_keys(TERMO_BUSCA)
        # campo_busca.send_keys(Keys.RETURN)

        pagina_atual = 1
        MAX_PAGINAS = 3  # Limitando para teste (o exemplo pedia 15)

        while pagina_atual <= MAX_PAGINAS:
            print(f"\n Processando PÁGINA {pagina_atual}...")

            # 1. PEGAR OS LINKS (Estratégia Anti-Stale)
            # Não clique nos itens direto. Pegue os LINKS (href) primeiro.
            # Se você clicar, o Selenium perde a referência da lista quando voltar.
            cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "thumbnail")))

            urls_lotes = []
            for card in cards:
                # Filtrando apenas o que queremos (Simulação da busca "Macbook")
                titulo = card.find_element(By.CLASS_NAME, "title").text
                if TERMO_BUSCA.lower() in titulo.lower():  # Validação simples
                    link = card.find_element(By.CLASS_NAME, "title").get_attribute("href")
                    urls_lotes.append(link)

            print(f"   Encontrados {len(urls_lotes)} lotes pertinentes nesta página.")

            # 2. ITERAR SOBRE OS DETALHES (Deep Scraping)
            for url in urls_lotes:
                driver.get(url)  # Entra no detalhe

                # --- EXTRAÇÃO DE DADOS ---
                try:
                    # Seletores específicos da página de detalhe
                    nome_produto = driver.find_element(By.XPATH, "//div[@class='caption']/h4[2]").text
                    valor_minimo = driver.find_element(By.CLASS_NAME, "pull-right").text

                    # Pegar URL da imagem
                    elemento_img = driver.find_element(By.CLASS_NAME, "img-responsive")
                    url_img = elemento_img.get_attribute("src")

                    # Gerar um ID Fictício (No site real, pegaria o ID do lote)
                    id_lote = f"LOTE_{int(time.time() * 1000) % 10000}"

                    print(f"    Lote {id_lote}: {nome_produto} | Lance: {valor_minimo}")

                    # --- DOWNLOAD DA FOTO ---
                    if baixar_imagem(url_img, id_lote):
                        print(f"       Foto salva: {id_lote}.jpg")

                except Exception as e:
                    print(f"       Erro ao ler detalhe: {e}")

                # Voltar para a lista (ou apenas seguir o loop que carrega a URL de novo)
                # Como estamos carregando URL por URL, não precisamos clicar em "Voltar"

            # 3. PAGINAÇÃO (Clicar em Próximo)
            # No site de teste webscraper.io, a paginação é chata, vamos simular a lógica padrão:
            try:
                # Tenta achar o botão "Next" ou o número da próxima página
                # XPath genérico para "botão que contém texto >" ou class 'next'
                # Aqui vamos forçar a URL da próxima página para fins didáticos do loop

                # LÓGICA REAL SERIA ASSIM:
                # btn_proximo = driver.find_element(By.XPATH, "//a[@rel='next']")
                # if "disabled" in btn_proximo.get_attribute("class"): break
                # btn_proximo.click()

                # Como o site de teste usa URLs fixas, simulamos o clique:
                pagina_atual += 1
                if pagina_atual <= MAX_PAGINAS:
                    # Voltamos para a listagem da página seguinte
                    # (Em sites reais com AJAX, você clicaria no botão. Em sites estáticos, muda URL)
                    print("    Indo para próxima página...")
                    # Simulação de clique no botão "Próximo" que carrega página nova
                    driver.get(
                        f"https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page={pagina_atual}")
                else:
                    print("    Limite de páginas atingido.")
                    break

            except Exception as e:
                print("    Não há mais páginas (Botão 'Próximo' não encontrado).")
                break

    except Exception as e:
        print(f"Erro Crítico: {e}")
    finally:
        driver.quit()
        print("Scraping finalizado.")


if __name__ == "__main__":
    iniciar_robo()