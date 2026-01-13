import pandas as pd
import os

# 1. Criar a Planilha de Dados
dados = {
    'Nome': ['Carlos Drummond', 'Cecília Meireles', 'Machado de Assis', 'Clarice Lispector'],
    'CPF': ['123.456.789-00', '111.222.333-44', '999.888.777-66', '555.444.333-22'],
    'Departamento': ['TI', 'Recursos Humanos', 'Financeiro', 'TI'],  # Dropdown
    'Ativo': ['Sim', 'Não', 'Sim', 'Sim']  # Checkbox
}
df = pd.DataFrame(dados)
df.to_excel("funcionarios.xlsx", index=False)

# 2. Criar o Sistema Web Legado (HTML Local)
html_content = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Sistema RH v1.0 (Legado)</title>
    <style>
        body { font-family: 'Courier New', monospace; background-color: #ccc; padding: 20px; }
        .tela-login, .tela-form { background: #000080; color: white; padding: 20px; width: 400px; border: 4px solid #fff; }
        input, select { margin-bottom: 10px; width: 100%; }
        label { display: block; margin-top: 10px; }
        button { background: #ccc; color: black; font-weight: bold; cursor: pointer; }
        #mensagem_sucesso { background: green; color: white; padding: 10px; display: none; margin-top: 10px; text-align: center;}
    </style>
    <script>
        function logar() {
            document.getElementById('login-screen').style.display = 'none';
            document.getElementById('form-screen').style.display = 'block';
        }
        function salvar() {
            // Simula loading do sistema antigo
            setTimeout(() => {
                document.getElementById('mensagem_sucesso').innerText = "REGISTRO SALVO COM SUCESSO (ID: " + Math.floor(Math.random() * 1000) + ")";
                document.getElementById('mensagem_sucesso').style.display = 'block';
                // Limpa formulário após 2 seg
                setTimeout(() => {
                    document.getElementById('form-cadastro').reset();
                    document.getElementById('mensagem_sucesso').style.display = 'none';
                }, 2000);
            }, 500);
        }
    </script>
</head>
<body>
    <div id="login-screen" class="tela-login">
        <h2>:: ACESSO RESTRITO ::</h2>
        <label>USUARIO:</label> <input type="text" id="user">
        <label>SENHA:</label> <input type="password" id="pass">
        <button onclick="logar()">[ ENTRAR NO SISTEMA ]</button>
    </div>

    <div id="form-screen" class="tela-form" style="display:none;">
        <h2>:: CADASTRO DE FUNCIONARIO ::</h2>
        <form id="form-cadastro" onsubmit="event.preventDefault(); salvar();">
            <label>NOME COMPLETO:</label>
            <input type="text" id="nome">

            <label>CPF:</label>
            <input type="text" id="cpf">

            <label>DEPARTAMENTO:</label>
            <select id="departamento">
                <option value="">-- Selecione --</option>
                <option value="TI">Tecnologia da Informação</option>
                <option value="RH">Recursos Humanos</option>
                <option value="FIN">Financeiro</option>
            </select>

            <label style="display:inline;">CADASTRO ATIVO?</label>
            <input type="checkbox" id="chk_ativo" style="width: auto;">

            <br><br>
            <button type="submit">[ SALVAR REGISTRO ]</button>
        </form>
        <div id="mensagem_sucesso"></div>
    </div>
</body>
</html>
"""

with open("sistema_rh_legado.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(" Setup concluído: Planilha e Sistema Legado criados.")