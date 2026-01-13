import pandas as pd
import smtplib
import os
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# --- CONFIGURAÇÕES ---
PASTA_BOLETOS = Path("Boletos")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_REMETENTE = "seu_email@gmail.com"
SENHA_EMAIL = "cole_sua_senha_de_app_aqui"


def enviar_email_cobranca(destinatario, nome, valor, arquivo_boleto):
    """
    Envia um e-mail HTML bonito com o boleto em anexo.
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = destinatario
    msg['Subject'] = f"Aviso de Vencimento - Fatura Pendente"

    # Corpo em HTML (Fica muito mais profissional)
    html_body = f"""
    <html>
      <body>
        <h2 style="color: #2E86C1;">Olá, {nome}!</h2>
        <p>Verificamos em nosso sistema que a fatura no valor de <strong>R$ {valor:.2f}</strong> consta em aberto.</p>
        <p>Sabemos que imprevistos acontecem. Segue em anexo a 2ª via do boleto para regularização.</p>
        <p>Caso já tenha efetuado o pagamento, por favor desconsidere este aviso.</p>
        <hr>
        <p style="font-size: 10px; color: gray;">Mensagem automática do Sistema Financeiro.</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_body, 'html'))

    # Anexar Boleto
    path_anexo = PASTA_BOLETOS / arquivo_boleto

    if path_anexo.exists():
        with open(path_anexo, "rb") as f:
            part = MIMEApplication(f.read(), Name=arquivo_boleto)
            part['Content-Disposition'] = f'attachment; filename="{arquivo_boleto}"'
            msg.attach(part)
    else:
        print(f"Alerta: Boleto {arquivo_boleto} não encontrado na pasta.")
        return False

    # Enviar
    if SENHA_EMAIL == "sua_senha_de_app_aqui":
        print(f"[Simulação] Enviando para {destinatario} | Anexo: {arquivo_boleto}")
        return True
    else:
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_REMETENTE, SENHA_EMAIL)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Erro de conexão: {e}")
            return False


def main():
    print("Lendo bases de dados...")

    # 1. Carregar Bases
    # Dica: Sempre converta IDs para string para garantir que o cruzamento funcione
    df_faturas = pd.read_excel("Faturas_Aberto.xlsx")
    df_faturas['ID_Fatura'] = df_faturas['ID_Fatura'].astype(str)

    df_banco = pd.read_csv("Comprovantes_Recebidos.csv", sep=';')
    df_banco['ID_Fatura'] = df_banco['ID_Fatura'].astype(str)

    # 2. LÓGICA DE CRUZAMENTO (O pulo do gato)
    # Queremos quem está em FATURAS e NÃO está no BANCO
    # O til (~) significa negação. "Faturas ONDE ID NÃO ESTÁ em Banco"
    devedores = df_faturas[~df_faturas['ID_Fatura'].isin(df_banco['ID_Fatura'])]

    total_aberto = len(df_faturas)
    total_pagos = len(df_banco)
    total_cobrar = len(devedores)

    print(f"Resumo da Análise:")
    print(f"   - Faturas Emitidas: {total_aberto}")
    print(f"   - Pagamentos Identificados: {total_pagos}")
    print(f"   - Clientes para Cobrar: {total_cobrar}\n")

    print("Iniciando disparos de cobrança...")

    for index, row in devedores.iterrows():
        nome = row['Cliente']
        email = row['Email']
        valor = row['Valor']
        id_fatura = row['ID_Fatura']
        nome_boleto = f"Boleto_{id_fatura}.pdf"

        print(f"Processando: {nome} (ID: {id_fatura})...")

        sucesso = enviar_email_cobranca(email, nome, valor, nome_boleto)

        if sucesso and SENHA_EMAIL != "sua_senha_de_app_aqui":
            print("E-mail enviado!")

    print("\nProcesso Finalizado.")


if __name__ == "__main__":
    main()