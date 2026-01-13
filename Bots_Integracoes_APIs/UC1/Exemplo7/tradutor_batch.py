import pandas as pd
import time
import random
from deep_translator import GoogleTranslator
from datetime import datetime

# --- CONFIGURAÇÕES ---
ARQUIVO_ENTRADA = "comentarios_en.csv"
ARQUIVO_SAIDA = "comentarios_pt_br.csv"
MAX_TENTATIVAS = 5  # Quantas vezes insistir antes de desistir


def traduzir_com_backoff(texto, linha_atual, total_linhas):
    """
    Tenta traduzir. Se der erro (Rate Limit), espera e tenta de novo.
    Usa Backoff Exponencial (1s, 2s, 4s, 8s...).
    """
    tradutor = GoogleTranslator(source='en', target='pt')
    tempo_espera = 1  # Começa esperando 1 segundo se der erro

    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            # Tenta traduzir
            traducao = tradutor.translate(texto)

            # Sucesso! Imprime log bonito
            print(f" [{linha_atual}/{total_linhas}] Traduzido com sucesso.")
            return traducao

        except Exception as e:
            # Se der erro (provavelmente bloqueio de IP ou Timeout)
            print(
                f"    [Tentativa {tentativa}/{MAX_TENTATIVAS}] Erro na API. Esperando {tempo_espera}s... (Erro: {e})")

            # A MÁGICA: Dorme o tempo necessário
            time.sleep(tempo_espera)

            # Dobra o tempo de espera para a próxima (Backoff Exponencial)
            tempo_espera *= 2

    # Se esgotou as tentativas
    print(f"    FALHA FINAL: Não foi possível traduzir a linha {linha_atual}.")
    return "ERRO_TRADUCAO"


def processar_arquivo():
    print("📂 Lendo arquivo de comentários...")
    try:
        df = pd.read_csv(ARQUIVO_ENTRADA)
    except FileNotFoundError:
        print(" Arquivo de entrada não encontrado. Rode o setup primeiro.")
        return

    total = len(df)
    print(f" Iniciando tradução de {total} linhas...")
    print("   Nota: Pausas aleatórias serão inseridas para evitar bloqueio.\n")

    # Lista para guardar as traduções
    traducoes = []

    for index, row in df.iterrows():
        texto_original = row['Comentario_EN']

        # Chama nossa função inteligente
        texto_pt = traduzir_com_backoff(texto_original, index + 1, total)
        traducoes.append(texto_pt)

        # --- PAUSA ESTRATÉGICA (HUMANIZAÇÃO) ---
        # Mesmo se deu certo, espera um pouquinho entre requisições
        # para não sobrecarregar o servidor (Rate Limiting preventivo)
        time.sleep(random.uniform(0.5, 1.5))

    # Adiciona a coluna nova no DataFrame
    df['Comentario_PT'] = traducoes
    df['Data_Processamento'] = datetime.now().strftime("%Y-%m-%d")

    # Salva o resultado
    df.to_csv(ARQUIVO_SAIDA, index=False, encoding='utf-8-sig')
    print("\n" + "=" * 40)
    print(f" Processo finalizado!")
    print(f" Arquivo salvo: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    processar_arquivo()