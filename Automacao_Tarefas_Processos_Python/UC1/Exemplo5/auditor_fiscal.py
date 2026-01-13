import pdfplumber
import re
import pandas as pd
from pathlib import Path

# Configurações
PASTA_NF = Path("Notas_Fiscais")
ARQUIVO_RELATORIO = "Relatorio_Divergencias_Fiscais.xlsx"


def limpar_valor_monetario(texto_valor):
    """
    Recebe 'R$ 1.250,50' e retorna float 1250.50
    """
    # Remove 'R$', espaços e pontos de milhar
    limpo = re.sub(r'[R$\s.]', '', texto_valor)
    # Troca vírgula decimal por ponto
    limpo = limpo.replace(',', '.')
    return float(limpo)


def auditar_notas():
    print("Iniciando Auditoria Fiscal...")

    notas_com_erro = []
    arquivos_processados = 0

    # Regex para capturar os valores
    # Explicação: Procura "Valor Total da Nota:" seguido de qualquer coisa até achar números e vírgulas
    regex_total = r"Valor Total da Nota:\s+(R\$\s?[\d\.,]+)"
    regex_iss = r"Valor do ISS \(10%\):\s+(R\$\s?[\d\.,]+)"

    # Listar todos os PDFs
    arquivos_pdf = list(PASTA_NF.glob("*.pdf"))

    if not arquivos_pdf:
        print("Nenhuma nota fiscal encontrada. Rode o setup primeiro.")
        return

    for arquivo in arquivos_pdf:
        with pdfplumber.open(arquivo) as pdf:
            # Pega o texto da primeira página
            texto = pdf.pages[0].extract_text()

            if not texto:
                print(f"Aviso: Não foi possível ler texto de {arquivo.name}")
                continue

            # Extração via Regex
            match_total = re.search(regex_total, texto)
            match_iss = re.search(regex_iss, texto)

            if match_total and match_iss:
                try:
                    # Converter string para float
                    valor_total = limpar_valor_monetario(match_total.group(1))
                    valor_iss_lido = limpar_valor_monetario(match_iss.group(1))

                    # CÁLCULO DE AUDITORIA (A Prova Real)
                    valor_iss_calculado = round(valor_total * 0.10, 2)

                    # Comparação com tolerância (para evitar erro de float 0.0000001)
                    diferenca = abs(valor_iss_lido - valor_iss_calculado)

                    if diferenca > 0.01:
                        print(
                            f"DIVERGÊNCIA: {arquivo.name} | Lido: {valor_iss_lido} | Correto: {valor_iss_calculado}")
                        notas_com_erro.append({
                            "Arquivo": arquivo.name,
                            "Valor Total": valor_total,
                            "ISS Destacado (Errado)": valor_iss_lido,
                            "ISS Calculado (Correto)": valor_iss_calculado,
                            "Diferença": valor_iss_lido - valor_iss_calculado
                        })
                    else:
                        # Opcional: printar sucessos
                        # print(f"{arquivo.name} OK")
                        pass

                except Exception as e:
                    print(f"Erro ao converter valores em {arquivo.name}: {e}")
            else:
                print(f"Padrão não encontrado em {arquivo.name}")

        arquivos_processados += 1

    # Gerar Relatório Final
    print("\n" + "=" * 40)
    print(f"AUDITORIA CONCLUÍDA: {arquivos_processados} notas analisadas.")

    if notas_com_erro:
        print(f"FORAM ENCONTRADAS {len(notas_com_erro)} DIVERGÊNCIAS!")
        df = pd.DataFrame(notas_com_erro)
        df.to_excel(ARQUIVO_RELATORIO, index=False)
        print(f"Relatório salvo em: {ARQUIVO_RELATORIO}")
    else:
        print("Parabéns! Nenhuma divergência fiscal encontrada.")


if __name__ == "__main__":
    auditar_notas()