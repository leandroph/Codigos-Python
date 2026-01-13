import pandas as pd
from pathlib import Path

# Cria pasta para salvar os PDFs gerados
Path("Relatorios_PDF").mkdir(exist_ok=True)

# Cria dados fictícios
dados = {
    'ID': [101, 102, 103, 104],
    'Fornecedor': ['Empresa Alpha', 'Beta Comércio', 'Gama Serviços', 'Delta Tech'],
    'Email': [
        'fornecedor_alpha@teste.com',
        'email_errado_sem_arroba',  # Vai gerar erro proposital
        'fornecedor_gama@teste.com',
        'fornecedor_delta@teste.com'
    ],
    'Total_Vendido': [50000.00, 12500.50, 0.00, 32000.00],
    'Status': ['Ativo', 'Ativo', 'Inativo', 'Ativo']
}

df = pd.read_csv('fornecedores.xlsx') if Path('fornecedores.xlsx').exists() else pd.DataFrame(dados)
df.to_excel("fornecedores.xlsx", index=False)

print("Arquivo 'fornecedores.xlsx' e pasta 'Relatorios_PDF' criados!")