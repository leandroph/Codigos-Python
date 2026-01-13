import os
import random
from datetime import datetime, timedelta

# Configurações
EMPRESA = "TechCorp"
TOTAL_PAGINAS = 5
NOTICIAS_POR_PAGINA = 3


def gerar_data_recente():
    dias_atras = random.randint(0, 30)
    data = datetime.now() - timedelta(days=dias_atras)
    return data.strftime("%d/%m/%Y")


manchetes = [
    f"{EMPRESA} anuncia lucro recorde no trimestre",
    f"Nova polêmica envolve o CEO da {EMPRESA}",
    f"Ações da {EMPRESA} sobem após fusão",
    f"Review: O novo gadget da {EMPRESA} vale a pena?",
    f"Funcionários da {EMPRESA} protestam por home office",
    f"Concorrente processa {EMPRESA} por patente",
    f"{EMPRESA} investe milhões em IA",
    f"Entenda a crise de reputação da {EMPRESA}",
    f"{EMPRESA} lança iniciativa sustentável",
    f"Mercado reage bem aos anúncios da {EMPRESA}"
]

print(" Criando Portal de Notícias Simulado...")

diretorio_base = os.getcwd()

for i in range(1, TOTAL_PAGINAS + 1):
    nome_arquivo = f"busca_page_{i}.html"

    # Lógica do Botão Próximo
    if i < TOTAL_PAGINAS:
        link_proximo = f"busca_page_{i + 1}.html"
        html_botao = f'<a href="{link_proximo}" class="btn-next">Próxima Página &gt;</a>'
    else:
        html_botao = '<span class="btn-disabled">Fim dos Resultados</span>'

    # Gerar Notícias Aleatórias para a página
    html_noticias = ""
    for _ in range(NOTICIAS_POR_PAGINA):
        titulo = random.choice(manchetes)
        data = gerar_data_recente()
        link_ficticio = f"https://portal-noticias.com/artigo/{random.randint(1000, 9999)}"

        html_noticias += f"""
        <div class="news-card">
            <h3 class="news-title"><a href="{link_ficticio}">{titulo}</a></h3>
            <span class="news-date">{data}</span>
            <p class="news-snippet">Lorem ipsum dolor sit amet, consectetur adipiscing elit sobre a {EMPRESA}...</p>
        </div>
        """

    html_completo = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Busca: {EMPRESA} - Página {i}</title>
        <style>
            body {{ font-family: 'Georgia', serif; background: #f9f9f9; padding: 40px; }}
            .container {{ max-width: 800px; margin: auto; background: white; padding: 30px; border: 1px solid #ddd; }}
            h1 {{ border-bottom: 2px solid #333; padding-bottom: 10px; }}
            .news-card {{ border-bottom: 1px solid #eee; padding: 20px 0; }}
            .news-title a {{ text-decoration: none; color: #003366; font-size: 20px; }}
            .news-title a:hover {{ text-decoration: underline; }}
            .news-date {{ color: #666; font-size: 12px; }}
            .pagination {{ margin-top: 30px; text-align: right; }}
            .btn-next {{ background: #c00; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; }}
            .btn-disabled {{ color: #ccc; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Resultados para: "{EMPRESA}" (Pág {i})</h1>
            <div id="lista-resultados">
                {html_noticias}
            </div>
            <div class="pagination">
                {html_botao}
            </div>
        </div>
    </body>
    </html>
    """

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(html_completo)

    print(f"    Página {i} criada: {nome_arquivo}")

print("\n Setup concluído!")