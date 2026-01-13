import pandas as pd
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from reportlab.pdfgen import canvas
from pathlib import Path
from datetime import datetime

# --- CONFIGURAÇÕES DO SERVIDOR DE E-MAIL ---
# ATENÇÃO: Para Gmail, você precisa gerar uma "Senha de App" (App Password).
# Não use sua senha normal.
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_REMETENTE = "seu_email@gmail.com"
SENHA_EMAIL = "abcdefghijklmnop"
EMAIL_GERENTE = "gerente_email@gmail.com"



# --- FUNÇÃO 1: GERADOR DE PDF DINÂMICO ---
def gerar_relatorio_pdf(dados_fornecedor):
    """
    Gera um PDF exclusivo para o fornecedor com base nos seus dados.
    Retorna o caminho do arquivo gerado.
    """
    nome_arq = f"Relatorios_PDF/Relatorio_{dados_fornecedor['Fornecedor']}.pdf"

    c = canvas.Canvas(nome_arq)
    c.setTitle(f"Relatório - {dados_fornecedor['Fornecedor']}")

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, f"RELATÓRIO DE PERFORMANCE - {datetime.now().year}")

    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Fornecedor: {dados_fornecedor['Fornecedor']}")
    c.drawString(50, 750, f"ID Interno: {dados_fornecedor['ID']}")
    c.drawString(50, 730, f"Total Vendido: R$ {dados_fornecedor['Total_Vendido']:,.2f}")
    c.drawString(50, 710, f"Status Contratual: {dados_fornecedor['Status']}")

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 650, "Documento gerado automaticamente pelo Sistema Python.")

    c.save()
    return nome_arq


# --- FUNÇÃO 2: ENVIADOR DE E-MAIL ---
def enviar_email(destinatario, assunto, corpo, anexo_path=None):
    """
    Conecta ao servidor SMTP e envia o e-mail com anexo.
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = destinatario
    msg['Subject'] = assunto

    msg.attach(MIMEText(corpo, 'plain'))

    if anexo_path:
        with open(anexo_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=Path(anexo_path).name)
        part['Content-Disposition'] = f'attachment; filename="{Path(anexo_path).name}"'
        msg.attach(part)

    # Conexão com Servidor (Context Manager garante que fecha a conexão)
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Segurança
        server.login(EMAIL_REMETENTE, SENHA_EMAIL)
        server.send_message(msg)


# --- FLUXO PRINCIPAL (MAIN LOOP) ---
def processar_disparos():
    print("Lendo planilha de fornecedores...")
    try:
        df = pd.read_excel("fornecedores.xlsx")
    except FileNotFoundError:
        print("Erro: Arquivo 'fornecedores.xlsx' não encontrado.")
        return

    sucessos = 0
    falhas = []

    print(f"Iniciando processamento de {len(df)} fornecedores...\n")

    for index, row in df.iterrows():
        fornecedor = row['Fornecedor']
        email_dest = row['Email']

        print(f"Processando [{index + 1}/{len(df)}]: {fornecedor}...")

        try:
            # 1. Gerar PDF Personalizado
            caminho_pdf = gerar_relatorio_pdf(row)

            # 2. Configurar E-mail
            assunto = f"Seu Relatório Anual - {fornecedor}"
            corpo = f"""Olá,

Segue em anexo o relatório de performance da {fornecedor}.
Total processado: R$ {row['Total_Vendido']}

Atenciosamente,
Equipe Financeira"""

            # 3. Enviar (Simulação de envio se não tiver senha configurada)
            if SENHA_EMAIL == "sua_senha_de_app_aqui":
                print(f"[Simulação] E-mail enviado para {email_dest} (PDF: {caminho_pdf})")
                time.sleep(1)  # Simula tempo de envio
            else:
                enviar_email(email_dest, assunto, corpo, caminho_pdf)
                print(f"E-mail enviado com sucesso!")

            sucessos += 1

        except Exception as e:
            # O SEGREDO DO ROBÔ: Captura o erro, registra e NÃO PARA.
            erro_msg = f"Erro no fornecedor {fornecedor} ({email_dest}): {str(e)}"
            print(f"FALHA: {erro_msg}")
            falhas.append(erro_msg)

    # --- RELATÓRIO FINAL PARA O GERENTE ---
    print("\nProcessamento Finalizado.")
    print("Gerando resumo para o gerente...")

    resumo_corpo = f"""Resumo do Processamento de Envios:

    Sucessos: {sucessos}
    Falhas: {len(falhas)}

    Detalhe das Falhas:
    """ + "\n".join(falhas)

    try:
        if SENHA_EMAIL != "sua_senha_de_app_aqui":
            enviar_email(EMAIL_GERENTE, "Resumo Diário - Robô de Envios", resumo_corpo)
        else:
            print("\n--- RESUMO QUE SERIA ENVIADO AO GERENTE ---")
            print(resumo_corpo)

    except Exception as e:
        print(f"Erro crítico ao enviar resumo para gerente: {e}")


if __name__ == "__main__":
    processar_disparos()