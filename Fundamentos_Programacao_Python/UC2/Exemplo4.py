import pandas as pd
from pathlib import Path


def etl_regional_vendas(pasta_entrada: str):
    pasta = Path(pasta_entrada)
    dfs = []

    # Dicionário "De -> Para" para padronizar colunas
    mapa_colunas = {
        "vlr": "valor",
        "preco": "valor",
        "total": "valor",
        "amount": "valor",
        "prod": "produto",
        "item": "produto",
        "desc": "produto",
        "date": "data",
        "dt": "data"
    }

    for arquivo in pasta.glob("*.csv"):
        try:
            df = pd.read_csv(arquivo)

            # 1. Padronizar nomes das colunas (strip espaços e lowercase)
            df.columns = [c.strip().lower() for c in df.columns]

            # 2. Renomear usando o mapa
            df.rename(columns=mapa_colunas, inplace=True)

            # 3. Adicionar coluna 'Região' baseada no nome do arquivo
            # Ex: vendas_sul.csv -> 'sul'
            nome_limpo = arquivo.stem.replace("vendas_", "").upper()
            df['regiao'] = nome_limpo

            dfs.append(df)

        except Exception as e:
            print(f"Erro ao ler {arquivo.name}: {e}")

    if dfs:
        df_consolidado = pd.concat(dfs, ignore_index=True)

        # 4. Feature Engineering: Calcular Imposto Estimado (ex: 12%)
        # Garante que 'valor' é numérico
        if 'valor' in df_consolidado.columns:
            df_consolidado['valor'] = pd.to_numeric(df_consolidado['valor'], errors='coerce').fillna(0)
            df_consolidado['imposto_estimado'] = df_consolidado['valor'] * 0.12

        saida = pasta / "Relatorio_Regional_Consolidado.xlsx"
        df_consolidado.to_excel(saida, index=False)
        print(f" ETL concluído! Arquivo gerado: {saida}")