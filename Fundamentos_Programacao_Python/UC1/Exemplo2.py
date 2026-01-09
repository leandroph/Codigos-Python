import re


def limpar_documento(doc: str) -> str:
    """Remove tudo que não for número do documento."""
    return re.sub(r'[^0-9]', '', str(doc))


def calcular_dv(digitos: str, pesos: list[int]) -> str:
    """Calcula um dígito verificador usando a lógica de Módulo 11."""
    soma = sum(int(d) * p for d, p in zip(digitos, pesos))
    resto = soma % 11
    return '0' if resto < 2 else str(11 - resto)


def validar_cpf(doc_limpo: str) -> bool:
    # 1. Verifica tamanho
    if len(doc_limpo) != 11:
        return False

    # 2. Verifica se todos os dígitos são iguais (ex: 111.111.111-11)
    # Isso é matematicamente válido no algoritmo, mas inválido na Receita.
    if doc_limpo == doc_limpo[0] * len(doc_limpo):
        return False

    # 3. Calcula DVs
    pesos1 = list(range(10, 1, -1))
    dv1 = calcular_dv(doc_limpo[:9], pesos1)

    pesos2 = list(range(11, 1, -1))
    dv2 = calcular_dv(doc_limpo[:10], pesos2)

    return doc_limpo[-2:] == dv1 + dv2


def validar_cnpj(doc_limpo: str) -> bool:
    if len(doc_limpo) != 14:
        return False

    # Bloqueia sequências repetidas também para CNPJ
    if doc_limpo == doc_limpo[0] * len(doc_limpo):
        return False

    # Pesos do CNPJ: [5,4,3,2,9,8,7,6,5,4,3,2]
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    dv1 = calcular_dv(doc_limpo[:12], pesos1)

    pesos2 = [6] + pesos1
    dv2 = calcular_dv(doc_limpo[:13], pesos2)

    return doc_limpo[-2:] == dv1 + dv2


def validar_documento(documento: str) -> str:
    """Função principal que detecta se é CPF ou CNPJ e valida."""
    doc_limpo = limpar_documento(documento)

    if len(doc_limpo) == 11:
        return "CPF Válido" if validar_cpf(doc_limpo) else "CPF Inválido"

    elif len(doc_limpo) == 14:
        return "CNPJ Válido" if validar_cnpj(doc_limpo) else "CNPJ Inválido"

    else:
        return f"Documento Inválido (Tamanho incorreto: {len(doc_limpo)} dígitos)"


# --- Testes ---
if __name__ == "__main__":
    testes = [
        "123.456.789-00",  # CPF Inválido (Real)
        "111.111.111-11",  # CPF Inválido (Dígitos repetidos - O seu código aceitava este)
        "52.668.666/0001-83",  # CNPJ Exemplo (Formatação)
        "123",  # Tamanho errado
    ]

    for t in testes:
        print(f"Testando '{t}': {validar_documento(t)}")