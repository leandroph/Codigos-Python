import pandas as pd
import time
import random
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURAÇÕES ---
ARQUIVO_PROCESSOS = "lista_processos.xlsx"
PASTA_PRINTS = Path("Evidencias_Processuais")
# URL Fictícia de teste que exige login (The Internet Herokuapp)
URL_TRIBUNAL = "https://the-internet.herokuapp.com/login"


def espera_humana(minimo=2, maximo=5):
    """
    Técnica Anti-Bloqueio: Nunca espere um tempo fixo (ex: 2s).
    O servidor detecta padrões. Espere tempos aleatórios (ex: 2.1s, 4.8s, 3.2s).
    """
    tempo = random.uniform(minimo, maximo)
    print(f"    Esperando {tempo:.2f}s (Humanização)...")
    time.sleep(tempo)


def resolver_captcha_simples_mock(driver):
    """
    Simula a resolução de um captcha matemático simples (Ex: '5 + 3 = ?').
    Em um site real, você leria o texto do elemento HTML.
    """
    try:
        # Exemplo teórico de como pegar o texto do desafio
        # desafio = driver.find_element(By.ID, "lbl_desafio").text  # "Quanto é 5 + 3?"
        # resposta = eval(desafio.replace("Quanto é", "").replace("?", ""))

        # Como estamos no site de teste, vamos apenas imprimir a lógica
        print("    CAPTCHA detectado: 'Resolvido via Lógica Matemática'")
        return True
    except:
        return False


def detectar_bloqueio(driver):
    """
    Verifica se o site retornou erro 429 (Too Many Requests) ou mensagem de bloqueio.
    """
    if "Too Many Requests" in driver.page_source or "bloqueio temporário" in driver.page_source.lower():
        print("    ALERTA: Bloqueio detectado! Entrando em modo de espera longo...")
        time.sleep(60)  # Espera 1 minuto
        return True
    return False


def monitorar_processos():
    print("  Iniciando Monitoramento Jurídico...")
    df = pd.read_excel(ARQUIVO_PROCESSOS)

    # Opções para ocultar automação (Evita detecção básica)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # 1. LOGIN
        driver.get(URL_TRIBUNAL)
        print(" Realizando Login no Portal...")

        # Preenchimento simulado
        driver.find_element(By.ID, "username").send_keys("tomsmith")
        espera_humana(1, 2)
        driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")

        # Resolver Captcha (Se houvesse)
        resolver_captcha_simples_mock(driver)

        driver.find_element(By.TAG_NAME, "button").click()
        espera_humana(2, 4)

        # 2. ITERAÇÃO SOBRE PROCESSOS
        for index, row in df.iterrows():
            processo = row['Numero_Processo']
            print(f"\n Verificando Processo: {processo}")

            # Checagem de segurança antes de navegar
            if detectar_bloqueio(driver):
                driver.refresh()

            # Simulando a busca (Em site real, buscaria o input de pesquisa)
            # Como o site de teste não tem busca de processo, vamos simular a navegação
            # driver.get(f"https://tribunal.jus.br/consulta?proc={processo}")

            # Simulacro: Vamos assumir que chegamos na página do processo
            espera_humana(3, 6)  # Tempo maior para simular leitura humana

            # 3. VERIFICAR MOVIMENTAÇÃO (Lógica Simulada)
            # Vamos dizer que o processo terminado em "0001" tem novidade (Regra do exemplo)
            tem_movimentacao = "0001" in processo

            if tem_movimentacao:
                print("    NOVA MOVIMENTAÇÃO DETECTADA!")

                # Salvar Print
                timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                nome_print = PASTA_PRINTS / f"Movim_{processo}_{timestamp}.png"

                driver.save_screenshot(str(nome_print))
                print(f"    Evidência salva: {nome_print}")

                # Atualiza planilha (em memória)
                df.at[index, 'Ultima_Verificacao'] = datetime.now().strftime("%d/%m/%Y")
                df.at[index, 'Status_Atual'] = "Movimentação Recente"
            else:
                print("    Nenhuma novidade nas últimas 24h.")

    except Exception as e:
        print(f" Erro durante execução: {e}")
    finally:
        driver.quit()
        # Salvar relatório atualizado
        df.to_excel("lista_processos_atualizada.xlsx", index=False)
        print("\n Monitoramento finalizado. Planilha atualizada.")


if __name__ == "__main__":
    monitorar_processos()