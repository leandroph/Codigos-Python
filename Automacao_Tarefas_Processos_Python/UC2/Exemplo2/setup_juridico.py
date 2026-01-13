import pandas as pd
from pathlib import Path

# Cria pasta para os prints
Path("Evidencias_Processuais").mkdir(exist_ok=True)

# Gera planilha de processos
dados = {
    'Numero_Processo': [
        '0001234-88.2024.8.26.0100',
        '0005678-12.2023.8.26.0000',
        '1112223-44.2025.4.03.6100',
        '9998887-77.2024.5.02.0001', # Vamos simular que este teve movimento
        '5554443-22.2024.8.13.0024'
    ],
    'Ultima_Verificacao': ['10/01/2026', '10/01/2026', '10/01/2026', '10/01/2026', '10/01/2026'],
    'Status_Atual': ['Em Andamento', 'Suspenso', 'Aguardando Sentença', 'Concluso', 'Inicial']
}

df = pd.DataFrame(dados)
df.to_excel("lista_processos.xlsx", index=False)

print("Planilha 'lista_processos.xlsx' criada.")
print("Pasta 'Evidencias_Processuais' criada.")