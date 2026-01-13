import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime

# --- CONFIGURAÇÃO ---
ARQUIVO_PDF = "Extrato_Banco.pdf"
ARQUIVO_EXCEL = "Relatorio_Sistema.xlsx"


def gerar_pdf_banco():
    c = canvas.Canvas(ARQUIVO_PDF, pagesize=A4)
    c.setFont("Courier", 10)  # Fonte monoespaçada para simular sistema legado

    # Cabeçalho
    c.drawString(50, 800, "BANCO TECH - EXTRATO MENSAL")
    c.drawString(50, 780, "DATA       HISTORICO                  VALOR (R$)")
    c.line(50, 775, 550, 775)

    # Transações (Texto não estruturado)
    # Formato: DD/MM | Descrição Variável | Valor (com , e . e sinal)
    lancamentos = [
        (760, "10/01/2024 PGTO FORNECEDOR XYZ          -1.500,00"),  # Bate
        (745, "12/01/2024 RECEBIMENTO CLIENTE A         5.000,00"),  # Bate
        (730, "15/01/2024 TARIFA MANUTENCAO CTA           -45,90"),  # SÓ NO BANCO (Erro)
        (715, "20/01/2024 TED 123.456 DESTINATARIO B     -300,00"),  # Bate
    ]

    for y, texto in lancamentos:
        c.drawString(50, y, texto)

    c.save()
    print(f"PDF '{ARQUIVO_PDF}' gerado.")


def gerar_excel_sistema():
    # Dados do sistema interno
    # Note que a descrição nunca é igual a do banco, por isso cruzamos por Data + Valor
    dados = {
        'Data_Lancamento': [
            datetime(2024, 1, 10),
            datetime(2024, 1, 12),
            datetime(2024, 1, 20),
            datetime(2024, 1, 25)  # SÓ NO SISTEMA (Erro)
        ],
        'Descricao_Interna': [
            'Pagamento Forn. XYZ (NF 1020)',
            'Recebimento Cliente A',
            'Pagamento Serviço B',
            'Pagamento Consultoria (Não compensado)'
        ],
        'Valor_Liquido': [
            -1500.00,
            5000.00,
            -300.00,
            -1000.00
        ]
    }

    df = pd.read_csv("dummy.csv") if False else pd.DataFrame(dados)  # Trick para IDE
    df = pd.DataFrame(dados)
    df.to_excel(ARQUIVO_EXCEL, index=False)
    print(f"Excel '{ARQUIVO_EXCEL}' gerado.")


if __name__ == "__main__":
    gerar_pdf_banco()
    gerar_excel_sistema()