import pandas as pd
from pathlib import Path
# Adicionamos ImageFont e sys aqui
from PIL import Image, ImageDraw, ImageFont
import sys

# --- CONFIGURAÇÕES ---
PASTA_SAIDA = Path("Certificados_Gerados")
ARQUIVO_DADOS = "participantes_webinar.xlsx"
TEMPLATE_IMAGEM = "template_certificado.png"


def carregar_fonte_sistema(tamanho):
    """
    Tenta encontrar uma fonte do sistema que suporte acentos (Arial no Windows).
    Se falhar, usa a padrão (que pode não ter acentos).
    """
    caminho_fonte = "arial.ttf"  # Tenta na pasta local primeiro

    # Se for Windows, tenta buscar na pasta de fontes do sistema
    if sys.platform == 'win32':
        path_win = Path("C:/Windows/Fonts/arial.ttf")
        if path_win.exists():
            caminho_fonte = str(path_win)

    try:
        # Tenta carregar a fonte TTF
        return ImageFont.truetype(caminho_fonte, tamanho)
    except OSError:
        print(f"Aviso: Não foi possível carregar a fonte '{caminho_fonte}' para o template.")
        print("   Usando fonte padrão (acentos podem falhar no template).")
        # Fallback para a fonte padrão do Pillow
        return ImageFont.load_default()


def setup_ambiente():
    print("Preparando ambiente...")
    PASTA_SAIDA.mkdir(exist_ok=True)

    # 1. Criar dados dos participantes (Adicionei acentos para testar)
    dados = {
        'Nome': ['Ana Souza', 'João Gonçalo da Silva', 'Mariana Oliveira', 'Andréia Costa Júnior'],
        'Email': ['ana@teste.com', 'joao@teste.com', 'mariana@teste.com', 'andreia@teste.com'],
        'Data_Conclusao': ['15 de Janeiro de 2026', '15 de Janeiro de 2026', '16 de Janeiro de 2026', '15/01/2026']
    }
    df = pd.read_excel(ARQUIVO_DADOS) if Path(ARQUIVO_DADOS).exists() else pd.DataFrame(dados)
    df.to_excel(ARQUIVO_DADOS, index=False)
    print(f"Arquivo '{ARQUIVO_DADOS}' criado com nomes acentuados.")

    # 2. Criar uma imagem de template "em branco"
    largura, altura = 1200, 800
    imagem_base = Image.new('RGB', (largura, altura), color='white')
    draw = ImageDraw.Draw(imagem_base)

    draw.rectangle([(20, 20), (largura - 20, altura - 20)], outline="darkblue", width=5)

    # --- CORREÇÃO DOS ACENTOS ---
    # Carregamos fontes TrueType reais para suportar UTF-8
    font_titulo = carregar_fonte_sistema(40)
    font_corpo = carregar_fonte_sistema(25)

    # Desenhando textos fixos usando o objeto 'font='
    # Note que removemos o 'font_size=' daqui, pois já está no objeto da fonte
    draw.text((largura // 2, 150), "CERTIFICADO DE PARTICIPAÇÃO", fill="darkblue", anchor="mm", font=font_titulo)

    # Texto com acentuação para teste ("Conclusão")
    draw.text((largura // 2, 300), "Certificamos a conclusão do curso", fill="black", anchor="mm", font=font_corpo)
    draw.text((largura // 2, 500), "no Webinar de Python Automation.", fill="black", anchor="mm", font=font_corpo)

    imagem_base.save(TEMPLATE_IMAGEM)
    print(f"Imagem base '{TEMPLATE_IMAGEM}' criada (com suporte a acentos).")

    print("\nLembrete: Para o script PRINCIPAL (gerador) rodar, você ainda precisa")
    print("   ter um arquivo de fonte (ex: arial.ttf) na mesma pasta dele.")


if __name__ == "__main__":
    setup_ambiente()