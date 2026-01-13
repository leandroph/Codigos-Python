import time
import os
import winsound  # Apenas Windows. Para Mac/Linux use print('\a')
from tkinter import messagebox
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURAÇÕES ---
PRECO_ALVO = 3000.00  # Se achar menos que isso, ALERTA!
TERMO_PRODUTO = "Notebook Dell"

# Lista de URLs (Aponta para os arquivos criados no setup)
diretorio_atual = os.getcwd()
URLS_LOJAS = [
    f"file:///{os.path.join(diretorio_atual, 'loja_a.html').replace(os.sep, '/')}",
    f"file:///{os.path.join(diretorio_atual, 'loja_b.html').replace(os.sep, '/')}",
    f"file:///{os.path.join(diretorio_atual, 'loja_c.html').replace(os.sep, '/')}"
]


def limpar_preco(texto_preco):
    """Converte 'R$ 2.890,00' para float 2890.00"""
    limpo = texto_preco.replace("R$", "").replace(".", "").replace(",", ".").strip()
    return float(limpo)


def tocar_alarme():
    """Toca um som de alerta (Beep)"""
    try:
        # Frequência 1000Hz, Duração 500ms (Repete 3x)
        for _ in range(3):
            winsound.Beep(1000, 500)
            time.sleep(0.1)
    except:
        print("\a")  # Fallback para Linux/Mac (Som do sistema)


def mostrar_popup(loja, valor, link):
    """Exibe uma janela na frente de tudo avisando da oportunidade"""
    # É necessário criar uma instância root oculta do Tkinter
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal feia
    root.attributes("-topmost", True)  # Força o popup a ficar no topo de tudo

    mensagem = f"OPORTUNIDADE ENCONTRADA!\n\nLoja: {loja}\nPreço: R$ {valor:,.2f}\n\nO robô recomenda a compra imediata."

    messagebox.showinfo(" ALERTA DE PREÇO BAIXO", mensagem)
    root.destroy()


def monitorar():
    print(f" Iniciando Monitoramento de Preços (Alvo: < R$ {PRECO_ALVO})...")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Roda sem abrir a janela do navegador (invisível)
    options.add_argument("--log-level=3")  # Menos sujeira no terminal

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    melhor_oferta = None
    menor_preco_encontrado = float('inf')

    try:
        for url in URLS_LOJAS:
            driver.get(url)

            # Captura de dados (Baseado nas classes do HTML do setup)
            try:
                nome_loja = driver.title.split("-")[0].strip()
                produto = driver.find_element(By.CLASS_NAME, "product-title").text
                preco_texto = driver.find_element(By.CLASS_NAME, "price-tag").text

                preco_float = limpar_preco(preco_texto)

                print(f"    {nome_loja}: {produto} | Preço: {preco_texto}")

                # Verifica se é o menor preço até agora
                if preco_float < menor_preco_encontrado:
                    menor_preco_encontrado = preco_float
                    melhor_oferta = {
                        "loja": nome_loja,
                        "preco": preco_float,
                        "url": url
                    }

            except Exception as e:
                print(f"    Erro ao ler loja: {e}")

        print("-" * 40)

        # ANÁLISE FINAL
        if melhor_oferta:
            print(f" Melhor preço encontrado: R$ {melhor_oferta['preco']:,.2f} na {melhor_oferta['loja']}")

            if better_price := melhor_oferta['preco'] < PRECO_ALVO:
                print("\n ALERTA: O PREÇO ESTÁ ABAIXO DO ALVO! DISPARANDO NOTIFICAÇÃO...")
                tocar_alarme()
                mostrar_popup(melhor_oferta['loja'], melhor_oferta['preco'], melhor_oferta['url'])
            else:
                print(f"\n Menor preço (R$ {melhor_oferta['preco']}) ainda está acima do alvo (R$ {PRECO_ALVO}).")
                print("   Nenhuma ação tomada.")

    finally:
        driver.quit()


if __name__ == "__main__":
    monitorar()