def validar_senha(senha: str) -> tuple[bool, list[str]]:
    """
    Valida uma senha com base em critérios de segurança (CIS Controls).

    Critérios:
    1. Mínimo 8 caracteres.
    2. Pelo menos uma letra maiúscula.
    3. Pelo menos um número.
    4. Pelo menos um caractere especial (!@#$%).

    Retorna:
        tuple[bool, list[str]]: (True se válida, Lista de erros encontrados)
    """
    erros = []
    caracteres_especiais_permitidos = "!@#$%"

    # 1. Validação de Tamanho
    if len(senha) < 8:
        erros.append(f"Mínimo de 8 caracteres (Atual: {len(senha)}).")

    # 2. Validação de Complexidade
    if not any(c.isupper() for c in senha):
        erros.append("Pelo menos uma letra maiúscula.")

    if not any(c.isdigit() for c in senha):
        erros.append("Pelo menos um número.")

    if not any(c in caracteres_especiais_permitidos for c in senha):
        erros.append(f"Pelo menos um caractere especial ({caracteres_especiais_permitidos}).")

    # Lógica de Retorno: Se a lista de erros estiver vazia, é True.
    eh_valida = len(erros) == 0
    return eh_valida, erros


# --- Simulação de Uso (Frontend / Interface) ---
# Aqui simulamos o usuário digitando a senha
senha_teste = "senha123"

# Chamada da função capturando os DOIS retornos
valida, lista_erros = validar_senha(senha_teste)

if valida:
    print(f"Sucesso: A senha '{senha_teste}' foi aprovada!")
else:
    print(f"Erro: A senha '{senha_teste}' é insegura.")
    print("Correções necessárias:")
    for erro in lista_erros:
        print(f"  - {erro}")