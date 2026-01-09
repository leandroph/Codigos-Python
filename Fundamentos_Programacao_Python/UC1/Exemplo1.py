def calcular_salario_liquido(salario_bruto: float, dependentes: int) -> dict:
    """
    Calcula o salário líquido considerando INSS e IRPF (Regras 2024/2025).
    Verifica automaticamente se o Desconto Simplificado é mais vantajoso.
    """

    # --- 1. CÁLCULO DO INSS (Tabela Progressiva 2024) ---
    # Valores de dedução para simular a alíquota progressiva
    inss = 0.0
    if salario_bruto <= 1412.00:
        inss = salario_bruto * 0.075
    elif salario_bruto <= 2666.68:
        inss = (salario_bruto * 0.09) - 21.18
    elif salario_bruto <= 4000.03:
        inss = (salario_bruto * 0.12) - 101.18
    elif salario_bruto <= 7786.02:
        inss = (salario_bruto * 0.14) - 181.18
    else:
        # Teto do INSS (para salários acima de R$ 7.786,02)
        inss = 908.85

    # --- 2. CÁLCULO DO IRPF (Base Legal vs Simplificada) ---

    # A) Método Legal (INSS + Dependentes)
    deducao_dependentes = dependentes * 189.59
    total_deducoes_legais = inss + deducao_dependentes

    # B) Método Simplificado (Desconto fixo de R$ 564,80) - Vigente 2024/25
    desconto_simplificado = 564.80

    # Define qual dedução é maior (mais vantajosa para o trabalhador)
    if desconto_simplificado > total_deducoes_legais:
        base_calculo = salario_bruto - desconto_simplificado
        metodo_usado = "Simplificado"
    else:
        base_calculo = salario_bruto - total_deducoes_legais
        metodo_usado = "Legal"

    # Aplicação da Tabela IRPF sobre a base definida
    irpf = 0.0
    if base_calculo <= 2259.20:
        irpf = 0.0
    elif base_calculo <= 2826.65:
        irpf = (base_calculo * 0.075) - 169.44
    elif base_calculo <= 3751.05:
        irpf = (base_calculo * 0.15) - 381.44
    elif base_calculo <= 4664.68:
        irpf = (base_calculo * 0.225) - 662.77
    else:
        irpf = (base_calculo * 0.275) - 896.00

    # Garantir que não seja negativo (caso base de cálculo seja muito baixa)
    irpf = max(irpf, 0.0)

    # --- 3. RESULTADO FINAL ---
    salario_liquido = salario_bruto - inss - irpf

    # Retorna um dicionário com todos os dados para uso posterior
    return {
        "bruto": salario_bruto,
        "inss": inss,
        "irpf": irpf,
        "liquido": salario_liquido,
        "metodo_irpf": metodo_usado
    }


# --- Bloco de Teste / Exibição ---
# Simulação
resultado = calcular_salario_liquido(5000.00, 1)

print("-" * 30)
print("DEMONSTRATIVO DE PAGAMENTO")
print("-" * 30)
print(f"Salário Bruto:   R$ {resultado['bruto']:,.2f}")
print(f"(-) INSS:        R$ {resultado['inss']:,.2f}")
print(f"(-) IRPF:        R$ {resultado['irpf']:,.2f} ({resultado['metodo_irpf']})")
print("-" * 30)
print(f"(=) LÍQUIDO:     R$ {resultado['liquido']:,.2f}")
print("-" * 30)