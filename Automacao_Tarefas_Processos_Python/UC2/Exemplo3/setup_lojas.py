import os

html_template = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>{loja} - Eletrônicos</title>
    <style>
        .product-card {{ border: 1px solid #ddd; padding: 20px; font-family: Arial; width: 300px; }}
        .product-title {{ font-size: 18px; font-weight: bold; color: #333; }}
        .price-tag {{ font-size: 24px; color: #e63946; font-weight: bold; margin-top: 10px; }}
        .buy-btn {{ background-color: #2a9d8f; color: white; padding: 10px; border: none; cursor: pointer; }}
    </style>
</head>
<body>
    <h1>Bem-vindo à {loja}</h1>
    <div class="product-card">
        <div class="product-title">Notebook Dell Inspiron 15 i5 8GB SSD</div>
        <p>O melhor para seu escritório.</p>
        <div class="price-tag">{preco}</div>
        <br>
        <button class="buy-btn">Comprar Agora</button>
    </div>
</body>
</html>
"""

lojas = [
    {"nome": "MegaShop", "arquivo": "loja_a.html", "preco": "R$ 4.500,00"},
    {"nome": "EletroFast", "arquivo": "loja_b.html", "preco": "R$ 3.200,50"},
    {"nome": "DescontoZone", "arquivo": "loja_c.html", "preco": "R$ 2.890,00"}  # Alvo!
]

diretorio_atual = os.getcwd()

print(" Construindo a 'Internet Fictícia' para testes...")

for loja in lojas:
    conteudo = html_template.format(loja=loja['nome'], preco=loja['preco'])
    with open(loja['arquivo'], "w", encoding="utf-8") as f:
        f.write(conteudo)

    # Gera o link local para usar no Selenium
    caminho_completo = f"file:///{os.path.join(diretorio_atual, loja['arquivo']).replace(os.sep, '/')}"
    print(f"    {loja['nome']} criada: {caminho_completo}")

print("\n Setup concluído! Agora rode o robô.")