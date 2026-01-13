import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select  # Importante para Dropdowns!
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURAÇÕES ---
ARQUIVO_EXCEL = "funcionarios.xlsx"
URL_SISTEMA = f"file:///{os.getcwd()}/sistema_rh_legado.html".replace("\\", "/")

# Dicionário para mapear o Excel ("Recursos Humanos") para o VALUE do HTML ("RH")
MAPA_DEPARTAMENTOS = {
    "TI": "TI",
    "Recursos Humanos": "RH",
    "Financeiro": "FIN"
}


def preencher_sistemas():
    print(" Lendo planilha de funcionários...")
    df = pd.read_excel(ARQUIVO_EXCEL)

    print(" Iniciando Data Entry...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # 1. ABRIR SISTEMA E LOGAR (Fazemos isso apenas uma vez)
        driver.get(URL_SISTEMA)

        # Preencher Login
        driver.find_element(By.ID, "user").send_keys("admin")
        driver.find_element(By.ID, "pass").send_keys("123456")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)  # Espera a tela mudar (Sistemas legados são lentos)

        # 2. LOOP PELAS LINHAS DO EXCEL
        for index, row in df.iterrows():
            print(f" Processando: {row['Nome']}...", end="")

            # --- Mapeamento de Elementos ---
            campo_nome = driver.find_element(By.ID, "nome")
            campo_cpf = driver.find_element(By.ID, "cpf")
            dropdown_depto = Select(driver.find_element(By.ID, "departamento"))
            checkbox_ativo = driver.find_element(By.ID, "chk_ativo")
            botao_salvar = driver.find_element(By.XPATH, "//button[@type='submit']")

            # A. Preencher Texto (Sempre limpar antes em sistemas legados)
            campo_nome.clear()
            campo_nome.send_keys(row['Nome'])

            campo_cpf.clear()
            campo_cpf.send_keys(row['CPF'])

            # B. Selecionar Dropdown (Select)
            # Precisamos converter "Recursos Humanos" do Excel para "RH" do HTML
            valor_html = MAPA_DEPARTAMENTOS.get(row['Departamento'])
            dropdown_depto.select_by_value(valor_html)

            # C. Lidar com Checkbox (A Lógica Chata)
            # Regra: Se Excel diz "Sim" e Checkbox NÃO está marcado -> Clica.
            #        Se Excel diz "Não" e Checkbox ESTÁ marcado -> Clica.
            deve_estar_marcado = (row['Ativo'] == 'Sim')
            esta_marcado = checkbox_ativo.is_selected()

            if deve_estar_marcado != esta_marcado:
                checkbox_ativo.click()

            # D. Salvar
            botao_salvar.click()

            # E. Capturar Mensagem de Sucesso (Validação)
            # Esperamos até a mensagem aparecer
            time.sleep(1)
            msg_elemento = driver.find_element(By.ID, "mensagem_sucesso")

            if "SUCESSO" in msg_elemento.text.upper():
                print(f"  OK! Msg: {msg_elemento.text}")
            else:
                print(f"  Erro: Mensagem de sucesso não apareceu.")

            # F. Esperar o sistema limpar para o próximo (Simulado no HTML)
            time.sleep(2)

    finally:
        driver.quit()
        print("\n Data Entry finalizado.")


if __name__ == "__main__":
    preencher_sistemas()