import os
from PIL import Image, ImageDraw

# Cria pasta para os arquivos do site
if not os.path.exists("Site_Local"):
    os.mkdir("Site_Local")

def criar_imagem_falsa(nome, cor, texto):
    """Cria um JPG localmente usando Pillow"""
    img = Image.new('RGB', (300, 300), color=cor)
    d = ImageDraw.Draw(img)
    d.text((10, 140), texto, fill=(255, 255, 255))
    caminho = os.path.join("Site_Local", nome)
    img.save(caminho)
    return nome

print(" Gerando imagens locais...")
img1 = criar_imagem_falsa("img_tenis.jpg", "blue", "TENIS")
img2 = criar_imagem_falsa("img_camisa.jpg", "red", "CAMISA")
img3 = criar_imagem_falsa("img_bone.jpg", "green", "BONE")

html_conteudo = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Loja Concorrente (Offline)</title>
    <style>
        body {{ font-family: sans-serif; background-color: #f4f4f4; }}
        .grid-produtos {{ display: flex; gap: 20px; padding: 20px; justify-content: center; }}
        .card-produto {{ background: white; border: 1px solid #ddd; padding: 15px; width: 200px; text-align: center; }}
        .card-produto img {{ width: 100%; height: auto; border-radius: 5px; }}
        .sku {{ color: #888; font-size: 12px; display: block; margin-top: 5px; }}
        .preco {{ color: green; font-weight: bold; font-size: 18px; }}
    </style>
</head>
<body>
    <h1 style="text-align:center">Catálogo Offline</h1>
    <div class="grid-produtos">
        <div class="card-produto">
            <img src="{img1}" alt="Tênis">
            <h3>Tênis Runner</h3>
            <span class="sku">SKU-RUN-001</span>
            <p class="preco">R$ 299,90</p>
        </div>
        <div class="card-produto">
            <img src="{img2}" alt="Camiseta">
            <h3>Camiseta Dry Fit</h3>
            <span class="sku">SKU-DRY-099</span>
            <p class="preco">R$ 59,90</p>
        </div>
        <div class="card-produto">
            <img src="{img3}" alt="Boné">
            <h3>Boné Tático</h3>
            <span class="sku">SKU-CAP-555</span>
            <p class="preco">R$ 89,90</p>
        </div>
    </div>
</body>
</html>
"""

caminho_html = os.path.join("Site_Local", "catalogo_concorrente.html")
with open(caminho_html, "w", encoding="utf-8") as f:
    f.write(html_conteudo)

print(f" Site offline criado em: {caminho_html}")