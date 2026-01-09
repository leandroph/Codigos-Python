import pandas as pd
from pathlib import Path


def consolidar_vendas_complexas(pasta_entrada: str):
    pasta = Path(pasta_entrada)
    lista_dfs = []
    taxa_dolar = 5.50  # Taxa fixa para exemplo

    print(" Iniciando consolidação de dados...")

    for arquivo in pasta.glob("*.csv"):
        try:
            # Tenta ler detectando o separador automaticamente (engine python)
            # Ou força leitura com tratamento de erros
            try:
                df = pd.read_csv(arquivo, sep=',')
                if df.shape[1] < 2:  # Se ler tudo numa coluna só, tenta ponto-e-vírgula
                    df = pd.read_csv(arquivo, sep=';')
            except:
                continue

            # Padronizar colunas para minúsculo
            df.columns = [c.lower().strip() for c in df.columns]

            # Verificar se tem coluna de moeda e valor
            if 'valor' in df.columns:
                # Se tiver coluna moeda, converte onde for USD
                if 'moeda' in df.columns:
                    mask_usd = df['moeda'].str.upper() == 'USD'
                    df.loc[mask_usd, 'valor'] = df.loc[mask_usd, 'valor'] * taxa_dolar
                    df['moeda'] = 'BRL'  # Agora tudo é Real

                # Adiciona coluna de origem para rastreio
                df['arquivo_origem'] = arquivo.name
                lista_dfs.append(df)

        except Exception as e:
            print(f" Erro ao ler {arquivo.name}: {e}")

    if lista_dfs:
        df_final = pd.concat(lista_dfs, ignore_index=True)

        # Cria tabela dinâmica (Soma de valor por Produto e Data)
        if 'produto' in df_final.columns:
            pivot = df_final.pivot_table(
                index='produto',
                values='valor',
                aggfunc=['sum', 'count']
            )

            saida = pasta / "Mestre_Vendas_Consolidado.xlsx"

            # Salva com duas abas: Dados Brutos e Resumo
            with pd.ExcelWriter(saida) as writer:
                df_final.to_excel(writer, sheet_name='Dados Brutos', index=False)
                pivot.to_excel(writer, sheet_name='Analise Dinamica')

            print(f" Arquivo Mestre gerado: {saida}")
        else:
            print(" Coluna 'produto' não encontrada para gerar tabela dinâmica.")
    else:
        print("Nenhum dado válido encontrado.")