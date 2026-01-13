import pandas as pd
import os

# 1. Gerar Massa de Dados (CNPJs fictícios mas com formato válido)
# Vamos definir que CNPJs terminados em '0002' estão BAIXADOS para testar o robô.
lista_cnpjs = []
for i in range(1, 51):
    final = f"{i:04d}"
    status_esperado = "BAIXADA" if i % 5 == 0 else "ATIVA"  # A cada 5, um ruim
    cnpj = f"12.345.678/{final}-00"
    lista_cnpjs.append({"Razao_Social": f"Fornecedor {i} Ltda", "CNPJ": cnpj})

df = pd.DataFrame(lista_cnpjs)
df.to_excel("fornecedores_cnpj.xlsx", index=False)

# 2. Criar o Site Simulado (HTML + JS)
html_content = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Consulta Pública de CNPJ</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f0f5; padding: 50px; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 500px; margin: auto; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;}
        button { width: 100%; background-color: #004d99; color: white; padding: 14px 20px; margin: 8px 0; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #003366; }
        #resultado-area { margin-top: 20px; padding: 15px; background: #e6f7ff; border: 1px solid #91d5ff; display: none; }
        .label { font-weight: bold; }
        .status-ativa { color: green; font-weight: bold; }
        .status-baixada { color: red; font-weight: bold; }
        .loader { border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 20px; height: 20px; animation: spin 1s linear infinite; margin: auto; display: none; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
    <script>
        function consultar() {
            var cnpj = document.getElementById('cnpj_input').value;
            var resArea = document.getElementById('resultado-area');
            var loader = document.getElementById('loader');

            // Limpa resultado anterior
            resArea.style.display = 'none';
            loader.style.display = 'block';

            // Simula lentidão do sistema do governo (1.5 segundos)
            setTimeout(function() {
                loader.style.display = 'none';
                resArea.style.display = 'block';

                // Lógica Simulada: A cada 5 CNPJs (final 5, 10...), retorna BAIXADA
                // Extrai apenas os números para checar
                var numeros = cnpj.replace(/[^0-9]/g, '');
                var digitoVerificador = parseInt(numeros.substring(8, 12)); // Pega parte do meio

                var status = "ATIVA";
                var classe = "status-ativa";

                // Lógica simples baseada no input: se terminar em 5 ou 0 antes do hífen
                if (cnpj.includes("5-00") || cnpj.includes("0-00")) {
                     status = "BAIXADA";
                     classe = "status-baixada";
                }

                document.getElementById('res_cnpj').innerText = cnpj;
                document.getElementById('res_status').innerHTML = '<span class="' + classe + '">' + status + '</span>';
                document.getElementById('res_data').innerText = new Date().toLocaleDateString();

            }, 1500); 
        }
    </script>
</head>
<body>
    <div class="container">
        <h2 style="text-align:center; color:#004d99;">Receita Federal (Simulado)</h2>
        <p>Informe o CNPJ para consulta:</p>
        <input type="text" id="cnpj_input" placeholder="XX.XXX.XXX/0001-XX">
        <button onclick="consultar()">CONSULTAR SITUAÇÃO</button>
        <div id="loader" class="loader"></div>

        <div id="resultado-area">
            <p><span class="label">CNPJ:</span> <span id="res_cnpj"></span></p>
            <p><span class="label">SITUAÇÃO CADASTRAL:</span> <span id="res_status"></span></p>
            <p><span class="label">Data da Consulta:</span> <span id="res_data"></span></p>
        </div>
    </div>
</body>
</html>
"""

with open("portal_receita.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(" Setup concluído: Planilha e Portal Receita criados.")