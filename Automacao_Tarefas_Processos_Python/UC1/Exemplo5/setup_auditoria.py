import os
import random
from reportlab.pdfgen import canvas
from pathlib import Path

# Configuração
PASTA_NF = Path("Notas_Fiscais")
PASTA_NF.mkdir(exist_ok=True)


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


print("Gerando 50 Notas Fiscais fictícias...")

for i in range(1, 51):
    num_nota = f"{i:03d}"  # Ex: 001, 002...

    # Valores aleatórios entre R$ 100 e R$ 5000
    valor_total = round(random.uniform(100, 5000), 2)

    # Lógica do ERRO PROPOSITAL
    # Nas notas múltiplas de 10 (10, 20, 30...), vamos calcular o imposto errado (5% em vez de 10%)
    if i % 10 == 0:
        iss_destacado = round(valor_total * 0.05, 2)  # Errado!
        status = "ERRO INTENCIONAL"
    else:
        iss_destacado = round(valor_total * 0.10, 2)  # Correto (10%)
        status = "Correto"

    # Criar PDF
    c = canvas.Canvas(str(PASTA_NF / f"NF_{num_nota}.pdf"))

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 800, f"NOTA FISCAL DE SERVIÇO ELETRÔNICA - Nº {num_nota}")

    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Prestador: Tech Solutions LTDA")
    c.drawString(50, 730, f"Tomador: Cliente Exemplo S.A.")

    # Aqui está o texto que o robô precisará ler
    c.line(50, 700, 500, 700)
    c.drawString(50, 680, f"Descrição: Consultoria em TI")
    c.drawString(50, 650, f"Valor Total da Nota: {formatar_moeda(valor_total)}")
    c.drawString(50, 630, f"Valor do ISS (10%):  {formatar_moeda(iss_destacado)}")
    c.line(50, 610, 500, 610)

    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, 50, "Documento sem valor fiscal - Gerado por Python")
    c.save()

    if status == "ERRO INTENCIONAL":
        print(f"NF_{num_nota} gerada com erro de cálculo para teste.")

print("Todas as 50 notas foram geradas na pasta 'Notas_Fiscais'.")