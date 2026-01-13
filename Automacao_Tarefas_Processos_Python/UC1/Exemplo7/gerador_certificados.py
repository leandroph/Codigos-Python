import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import sys

# --- CONFIGURAÇÕES VISUAIS (O "Olhômetro" do Designer) ---
TEMPLATE_PATH = "template_certificado.png"
PASTA_SAIDA = Path("Certificados_Gerados")
ARQUIVO_DADOS = "participantes_webinar.xlsx"

# Tente encontrar uma fonte no sistema. Ajuste o nome conforme necessário.
FONTE_NOME_ARQUIVO = "arial.ttf"
# Alternativa se tiver baixado: "Roboto-Bold.ttf"

# Coordenadas e Estilos
# Dica: Abra a imagem no Paint/Photoshop para descobrir o X,Y exato onde o texto deve ficar.
POSICAO_Y_NOME = 400  # Altura onde o nome vai ficar
TAMANHO_FONTE_NOME = 60  # Tamanho grande para o nome
COR_NOME = "#1a237e"  # Azul escuro hexadecimal

POSICAO_Y_DATA = 650
TAMANHO_FONTE_DATA = 20
COR_DATA = "black"
CENTRO_X_IMAGEM = 600  # Metade da largura da imagem (1200 / 2)


def carregar_fonte(caminho_fonte, tamanho):
    """Tenta carregar a fonte personalizada, usa padrão se falhar."""
    try:
        return ImageFont.truetype(caminho_fonte, tamanho)
    except OSError:
        print(f"Aviso: Fonte '{caminho_fonte}' não encontrada. Usando fonte padrão (feia).")
        # Tenta carregar fonte padrão do Pillow. O tamanho pode não funcionar bem.
        return ImageFont.load_default()


def desenhar_texto_centralizado(draw_obj, texto, y, fonte, cor, centro_x):
    """
    Desenha um texto centralizado horizontalmente em uma coordenada Y.
    Calcula a largura do texto para achar o ponto X inicial exato.
    """
    # textbbox retorna (left, top, right, bottom) da caixa imaginária do texto
    bbox = draw_obj.textbbox((0, 0), texto, font=fonte)
    largura_texto = bbox[2] - bbox[0]

    # Cálculo do ponto X inicial para que o texto fique no meio
    posicao_x = centro_x - (largura_texto / 2)

    draw_obj.text((posicao_x, y), texto, font=fonte, fill=cor)


def gerar_certificados():
    if not Path(TEMPLATE_PATH).exists() or not Path(ARQUIVO_DADOS).exists():
        print("Erro: Template ou dados não encontrados. Rode o 'setup_certificados.py'.")
        return

    print("Lendo lista de participantes...")
    df = pd.read_excel(ARQUIVO_DADOS)

    print(f"Iniciando geração de {len(df)} certificados...\n")

    # Carrega as fontes uma única vez (eficiência)
    font_nome_obj = carregar_fonte(FONTE_NOME_ARQUIVO, TAMANHO_FONTE_NOME)
    font_data_obj = carregar_fonte(FONTE_NOME_ARQUIVO, TAMANHO_FONTE_DATA)

    for index, row in df.iterrows():
        nome_participante = row['Nome'].strip().title()  # Padroniza nome (ex: ana -> Ana)
        data_conclusao = row['Data_Conclusao']
        email = row['Email']

        print(f"Processando: {nome_participante}...")

        # 1. Abre a imagem base (sempre abra uma nova cópia)
        imagem = Image.open(TEMPLATE_PATH)
        draw = ImageDraw.Draw(imagem)

        # 2. Desenha o Nome (Centralizado)
        desenhar_texto_centralizado(
            draw, nome_participante, POSICAO_Y_NOME, font_nome_obj, COR_NOME, CENTRO_X_IMAGEM
        )

        # 3. Desenha a Data
        texto_data = f"Data de emissão: {data_conclusao}"
        desenhar_texto_centralizado(
            draw, texto_data, POSICAO_Y_DATA, font_data_obj, COR_DATA, CENTRO_X_IMAGEM
        )

        # 4. Salvar o resultado
        # Cria um nome de arquivo seguro (sem espaços ou acentos)
        nome_arquivo_safe = nome_participante.replace(" ", "_").lower()
        caminho_final = PASTA_SAIDA / f"Certificado_{nome_arquivo_safe}.png"

        # Salva com alta qualidade
        imagem.save(caminho_final, quality=95)
        print(f"Salvo em: {caminho_final.name}")

        # --- INTEGRAÇÃO COM E-MAIL (OPCIONAL) ---
        # Aqui você chamaria a função de enviar e-mail de exemplos anteriores
        # enviar_email_com_anexo(email, "Seu Certificado Chegou!", caminho_final)
        # print(f"E-mail enviado para {email}")
        # ----------------------------------------

    print("\nProcesso Finalizado! Verifique a pasta 'Certificados_Gerados'.")


if __name__ == "__main__":
    # Verifica se está no Windows para sugerir caminho da fonte Arial
    if sys.platform == 'win32' and not Path(FONTE_NOME_ARQUIVO).exists():
        path_arial_win = Path("C:/Windows/Fonts/arial.ttf")
        if path_arial_win.exists():
            print(f"Usando fonte do sistema: {path_arial_win}")
            FONTE_NOME_ARQUIVO = str(path_arial_win)

    gerar_certificados()