import pandas as pd
from pathlib import Path
from reportlab.pdfgen import canvas

# 1. Configurar Pastas
pasta_boletos = Path("Boletos")
pasta_boletos.mkdir(exist_ok=True)

# 2. Criar Base de Faturas (O que esperamos receber)
dados_faturas = {
    'ID_Fatura': [1001, 1002, 1003, 1004, 1005],
    'Cliente': ['João Silva', 'Maria Souza', 'Tech Solutions', 'Padaria Central', 'Carlos TI'],
    'Email': [
        'joao@teste.com',
        'maria@teste.com', # Este vai pagar
        'financeiro@tech.com',
        'padaria@teste.com', # Este vai pagar
        'carlos@teste.com'
    ],
    'Valor': [150.00, 2500.00, 4500.50, 120.00, 800.00],
    'Vencimento': ['10/01/2026', '10/01/2026', '15/01/2026', '11/01/2026', '12/01/2026']
}
df_faturas = pd.DataFrame(dados_faturas)
df_faturas.to_excel("Faturas_Aberto.xlsx", index=False)

# 3. Criar Base de Comprovantes (Quem JÁ pagou)
# Vamos dizer que a Maria (1002) e a Padaria (1004) já pagaram.
dados_banco = {
    'ID_Fatura': [1002, 1004],
    'Data_Pagamento': ['09/01/2026', '11/01/2026'],
    'Valor_Pago': [2500.00, 120.00]
}
df_banco = pd.DataFrame(dados_banco)
df_banco.to_csv("Comprovantes_Recebidos.csv", index=False, sep=';')

# 4. Gerar Boletos PDFs Fictícios para TODOS (mesmo quem pagou, o arquivo existe)
for id_fatura in dados_faturas['ID_Fatura']:
    nome_arquivo = pasta_boletos / f"Boleto_{id_fatura}.pdf"
    c = canvas.Canvas(str(nome_arquivo))
    c.drawString(100, 750, f"BOLETO REFERENTE FATURA {id_fatura}")
    c.drawString(100, 730, "PAGÁVEL EM QUALQUER BANCO")
    c.save()

print("Ambiente Prontinho!")
print("1. Faturas_Aberto.xlsx (5 clientes)")
print("2. Comprovantes_Recebidos.csv (2 pagos)")
print("3. Pasta 'Boletos' com 5 PDFs.")