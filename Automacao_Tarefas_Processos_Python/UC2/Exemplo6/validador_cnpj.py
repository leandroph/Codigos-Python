import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURAÇÕES ---
ARQUIVO_ENTRADA = "fornecedores_cnpj.xlsx"
ARQUIVO_SAIDA = "fornecedores_verificados.xlsx"
URL_PORTAL = f"file:///{os.getcwd()}/portal_receita.html".replace("\\", "/")


def validar_fornecedores():
    print(" Carregando lista de CNPJs...")
    df = pd.read_excel(ARQUIVO_ENTRADA)

    # Cria coluna de status se não existir
    df['Status_Receita'] = ""

    print(" Iniciando navegador...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)  # Tempo máximo de espera: 10s

    try:
        driver.get(URL_PORTAL)

        for index, row in df.iterrows():
            cnpj = row['CNPJ']
            print(f" [{index + 1}/{len(df)}] Consultando: {cnpj}...", end="")

            try:
                # 1. Localizar Elementos
                campo_input = driver.find_element(By.ID, "cnpj_input")
                botao = driver.find_element(By.TAG_NAME, "button")

                # 2. Interagir
                campo_input.clear()
                campo_input.send_keys(cnpj)
                botao.click()

                # 3. Espera Inteligente (O Pulo do Gato)
                # Não use time.sleep(2). E se demorar 3? E se demorar 0.1?
                # Use Wait until visibility_of_element_located
                elemento_resultado = wait.until(
                    EC.visibility_of_element_located((By.ID, "resultado-area"))
                )

                # 4. Extrair Status
                # O status está dentro do span com id 'res_status'
                status_texto = driver.find_element(By.ID, "res_status").text

                # 5. Salvar no DataFrame
                df.at[index, 'Status_Receita'] = status_texto

                print(f"  {status_texto}")

            except Exception as e:
                print(f"  Erro: {e}")
                df.at[index, 'Status_Receita'] = "ERRO / TIMEOUT"

                # Se der erro, tenta dar refresh para limpar a tela para o próximo
                driver.refresh()

    finally:
        driver.quit()
        # Salva o resultado final
        df.to_excel(ARQUIVO_SAIDA, index=False)
        print("\n Validação concluída!")
        print(f" Relatório salvo em: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    validar_fornecedores()