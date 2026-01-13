import os
from pathlib import Path

# Configuração
PASTA_ORIGEM = Path("Downloads_Bagunça")
PASTA_ORIGEM.mkdir(exist_ok=True)

# Lista de arquivos para criar (simulando nomes reais)
arquivos_ficticios = [
    "Contrato_Prestacao_Servicos_Google.pdf",
    "proposta_comercial_versao_final.docx",
    "Fatura_Vivo_Janeiro.pdf",
    "comprovante_pix_aluguel.jpeg",
    "Relatorio_Financeiro_2025.xlsx",
    "Minuta_Contrato_Novo_Cliente.docx",
    "foto_confraternizacao.jpg",
    "logo_empresa_transparente.png",
    "setup_instalador_v1.exe",
    "anotacoes_reuniao.txt",
    "boleto_faculdade.pdf"
]

print("Criando bagunça na pasta 'Downloads_Bagunça'...")

for nome_arquivo in arquivos_ficticios:
    caminho = PASTA_ORIGEM / nome_arquivo
    # Cria um arquivo vazio
    with open(caminho, "w") as f:
        f.write("Conteúdo fictício")
    print(f"   + Criado: {nome_arquivo}")

print("Caos instaurado com sucesso!")