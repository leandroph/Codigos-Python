import pdfplumber
import re
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÕES ---
ARQUIVO_PDF = "Extrato_Banco.pdf"
ARQUIVO_EXCEL = "Relatorio_Sistema.xlsx"
RELATORIO_FINAL = "Divergencias_Conciliacao.xlsx"


def limpar_valor_ptbr(valor_str: str) -> float:
    """
    Converte string financeira brasileira ('1.500,00' ou '-1.500,00') para float.
    """
    # Remove espaços
    valor_str = valor_str.strip()

    # Tratamento de sinal (alguns bancos usam 'D' no final para negativo)
    fator = -1 if valor_str.endswith('D') else 1
    if valor_str.startswith('-'):
        fator = -1

    # Remove tudo que não é número ou vírgula
    # Ex: '-1.500,00' -> '1500,00'
    limpo = re.sub(r'[^0-9,]', '', valor_str)

    if not limpo: return 0.0

    # Troca vírgula por ponto
    valor_float = float(limpo.replace(',', '.'))
    return valor_float * fator


def extrair_dados_pdf(caminho_pdf):
    print("Lendo Extrato Bancário (PDF)...")
    transacoes = []

    # Regex Explicado:
    # (\d{2}/\d{2}/\d{4}) -> Captura Data (Grupo 1)
    # (.*?)               -> Captura Descrição (Grupo 2 - lazy)
    # (-?[\d\.]+,\d{2})   -> Captura Valor com ou sem sinal, pontos e vírgula (Grupo 3)
    regex_linha = re.compile(r"(\d{2}/\d{2}/\d{4})\s+(.*?)\s+(-?[\d\.]+,\d{2})")

    with pdfplumber.open(caminho_pdf) as pdf:
        for page in pdf.pages:
            texto = page.extract_text()
            for linha in texto.split('\n'):
                match = regex_linha.search(linha)
                if match:
                    transacoes.append({
                        'Data': match.group(1),  # Mantém string por enquanto
                        'Descricao_Banco': match.group(2).strip(),
                        'Valor': limpar_valor_ptbr(match.group(3)),
                        'Origem': 'Banco'
                    })

    return pd.DataFrame(transacoes)


def conciliar():
    # 1. Carregar Extrato (PDF)
    df_banco = extrair_dados_pdf(ARQUIVO_PDF)

    # 2. Carregar Sistema (Excel)
    print("Lendo Relatório do Sistema (Excel)...")
    df_sistema = pd.read_excel(ARQUIVO_EXCEL)

    # 3. Normalização de Datas para Cruzamento
    # O Excel lê como datetime, o PDF como string. Vamos padronizar tudo para String DD/MM/AAAA
    df_sistema['Data_Str'] = pd.to_datetime(df_sistema['Data_Lancamento']).dt.strftime('%d/%m/%Y')

    # Criar colunas de controle
    df_banco['Conciliado'] = False
    df_sistema['Conciliado'] = False

    divergencias = []

    print("Cruzando dados...")

    # 4. Lógica de Conciliação (Iterando sobre o Banco)
    for idx_banco, row_banco in df_banco.iterrows():
        # Busca correspondência no Sistema: Mesma Data, Mesmo Valor (aprox), Não conciliado
        # Usamos abs(a-b) < 0.01 porque float tem imprecisão (floating point error)
        match = df_sistema[
            (df_sistema['Data_Str'] == row_banco['Data']) &
            (abs(df_sistema['Valor_Liquido'] - row_banco['Valor']) < 0.01) &
            (df_sistema['Conciliado'] == False)
            ]

        if not match.empty:
            # Encontrou! Marca o primeiro match como conciliado nos dois lados
            idx_sistema = match.index[0]
            df_sistema.at[idx_sistema, 'Conciliado'] = True
            df_banco.at[idx_banco, 'Conciliado'] = True
        else:
            # Não encontrou no sistema
            divergencias.append({
                "Data": row_banco['Data'],
                "Valor": row_banco['Valor'],
                "Descricao": row_banco['Descricao_Banco'],
                "Tipo": "SOBRA NO BANCO (Não lançado no sistema)"
            })

    # 5. Verificar o que sobrou no Sistema (Não estava no banco)
    sobras_sistema = df_sistema[df_sistema['Conciliado'] == False]

    for idx, row in sobras_sistema.iterrows():
        divergencias.append({
            "Data": row['Data_Str'],
            "Valor": row['Valor_Liquido'],
            "Descricao": row['Descricao_Interna'],
            "Tipo": "SOBRA NO SISTEMA (Não compensado no banco)"
        })

    # 6. Gerar Relatório
    if divergencias:
        df_final = pd.DataFrame(divergencias)
        df_final.to_excel(RELATORIO_FINAL, index=False)
        print(f"Divergências encontradas! Relatório salvo em: {RELATORIO_FINAL}")
        print(df_final[['Data', 'Valor', 'Tipo']])
    else:
        print("Conciliação Perfeita! Todos os valores batem.")


if __name__ == "__main__":
    conciliar()