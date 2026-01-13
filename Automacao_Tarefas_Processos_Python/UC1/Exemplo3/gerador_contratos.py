import pandas as pd
import shutil
import os
from docx import Document
from docx2pdf import convert
from pathlib import Path

# Configurações
ARQUIVO_EXCEL = "contratos.xlsx"
ARQUIVO_WORD = "Minuta_Padrao.docx"
PASTA_SAIDA = Path("Contratos_Gerados")


def formatar_moeda(valor):
    """Transforma float 15000.5 em string 'R$ 15.000,50'"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def substituir_texto_docx(doc, de, para):
    """
    Substitui texto preservando a formatação do parágrafo.
    Percorre parágrafos comuns e tabelas.
    """
    # 1. Substituir no corpo do texto
    for paragraph in doc.paragraphs:
        if de in paragraph.text:
            # Uma abordagem simples para iniciantes (pode perder negrito parcial se não for run-by-run,
            # mas funciona bem para templates simples)
            paragraph.text = paragraph.text.replace(de, str(para))

    # 2. Substituir dentro de tabelas (caso o contrato tenha tabelas)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    if de in paragraph.text:
                        paragraph.text = paragraph.text.replace(de, str(para))


def gerar_contratos():
    # Carregar dados
    print("📂 Lendo planilha de contratos...")
    df = pd.read_excel(ARQUIVO_EXCEL)

    # Criar pasta raiz de saída
    PASTA_SAIDA.mkdir(exist_ok=True)

    print(f"Iniciando geração de {len(df)} contratos...\n")

    for index, row in df.iterrows():
        cliente = row['Cliente']
        vendedor = row['Vendedor']

        print(f"Processando: {cliente} (Vendedor: {vendedor})...")

        # 1. Carregar a Minuta Original
        doc = Document(ARQUIVO_WORD)

        # 2. Dicionário de Substituição (De -> Para)
        # Atenção: formatar o valor monetário aqui para ficar bonito no texto
        substituicoes = {
            '{{CLIENTE}}': cliente,
            '{{CNPJ}}': row['CNPJ'],
            '{{VALOR}}': formatar_moeda(row['Valor']),
            '{{PRAZO}}': row['Prazo']
        }

        # 3. Aplicar substituições
        for chave, valor in substituicoes.items():
            substituir_texto_docx(doc, chave, valor)

        # 4. Salvar DOCX temporário
        nome_arquivo = f"Contrato_{cliente.replace(' ', '_')}"
        caminho_docx_temp = PASTA_SAIDA / f"{nome_arquivo}.docx"
        doc.save(caminho_docx_temp)

        # 5. Converter para PDF (Requer MS Word instalado)
        # O arquivo PDF será gerado na mesma pasta do DOCX
        caminho_pdf = PASTA_SAIDA / f"{nome_arquivo}.pdf"
        try:
            convert(str(caminho_docx_temp), str(caminho_pdf))
        except Exception as e:
            print(f"Erro na conversão PDF (Verifique se o Word está fechado): {e}")
            continue

        # 6. Organização por Vendedor (Move File)
        pasta_vendedor = PASTA_SAIDA / vendedor
        pasta_vendedor.mkdir(exist_ok=True)

        # Move o PDF final para a pasta do vendedor
        destino_final = pasta_vendedor / f"{nome_arquivo}.pdf"
        shutil.move(str(caminho_pdf), str(destino_final))

        # Limpeza: Deletar o DOCX temporário (opcional, mas recomendado)
        os.remove(caminho_docx_temp)

        print(f"Contrato gerado e movido para: {destino_final}")

    print("\nProcesso Finalizado!")


if __name__ == "__main__":
    gerar_contratos()