import json
import pandas as pd
from pathlib import Path


def converter_batch_json(pasta_jsons: str):
    pasta = Path(pasta_jsons)
    lista_dados = []

    print(" Lendo arquivos JSON...")

    arquivos = list(pasta.glob("*.json"))
    if not arquivos:
        print("Nenhum arquivo .json encontrado.")
        return

    for arquivo in arquivos:
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)

                # Se o JSON for um dicionário simples, adiciona à lista
                if isinstance(dados, dict):
                    dados['arquivo_origem'] = arquivo.name  # Rastreabilidade
                    lista_dados.append(dados)

                # Se o JSON for uma lista de dicionários (vários registros num arquivo)
                elif isinstance(dados, list):
                    for item in dados:
                        if isinstance(item, dict):
                            item['arquivo_origem'] = arquivo.name
                            lista_dados.append(item)

        except json.JSONDecodeError:
            print(f" Erro ao ler JSON: {arquivo.name}")

    if lista_dados:
        print(" Gerando Excel...")
        df = pd.DataFrame(lista_dados)

        saida = pasta / "Consolidado_Clientes.xlsx"
        df.to_excel(saida, index=False)
        print(f" Conversão concluída! {len(lista_dados)} registros salvos em {saida.name}")
    else:
        print("Nenhum dado válido extraído.")