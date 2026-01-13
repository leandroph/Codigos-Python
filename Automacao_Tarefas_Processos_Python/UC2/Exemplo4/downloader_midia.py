import os
# Mudança chave: Usaremos urllib em vez de requests
from urllib.request import urlretrieve
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURAÇÕES ---
PASTA_DOWNLOAD = Path("Imagens_Concorrente")
PASTA_DOWNLOAD.mkdir(exist_ok=True)

# Aponta para o novo site local dentro da pasta Site_Local
caminho_base = os.getcwd()
URL_ALVO = f"file:///{caminho_base}/Site_Local/catalogo_concorrente.html".replace("\\", "/")


def baixar_arquivo_universal(url, nome_salvar):
    """
    Função robusta que baixa tanto da Web quanto de arquivos Locais.
    """
    try:
        caminho_final = PASTA_DOWNLOAD / nome_salvar

        # urlretrieve baixa o arquivo (seja online ou offline) e salva no destino
        urlretrieve(url, caminho_final)
        return True
    except Exception as e:
        print(f"       Erro no download: {e}")
    return False


def iniciar_crawler():
    print(" Iniciando Crawler (Modo Universal)...")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(URL_ALVO)
        print(" Acessando catálogo...")

        cards = driver.find_elements(By.CLASS_NAME, "card-produto")
        print(f" Encontrados {len(cards)} produtos.\n")

        for produto in cards:
            try:
                sku = produto.find_element(By.CLASS_NAME, "sku").text

                # O Selenium vai retornar algo como: "file:///C:/.../Site_Local/img_tenis.jpg"
                elemento_img = produto.find_element(By.TAG_NAME, "img")
                url_img = elemento_img.get_attribute("src")

                nome_arquivo = f"{sku}.jpg"

                print(f"    Processando: {sku}")

                # A nova função lida com o "file:///" automaticamente
                if baixar_arquivo_universal(url_img, nome_arquivo):
                    print(f"       Imagem salva em: {PASTA_DOWNLOAD}/{nome_arquivo}")

            except Exception as e:
                print(f"    Erro ao ler card: {e}")

    finally:
        driver.quit()
        print("\n Processo Finalizado.")


if __name__ == "__main__":
    iniciar_crawler()