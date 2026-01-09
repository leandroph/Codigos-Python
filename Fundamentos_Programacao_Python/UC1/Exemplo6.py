from datetime import datetime


def calcular_meses_trabalhados(inicio: datetime, fim: datetime) -> int:
    """
    Calcula a quantidade de meses trabalhados considerando a regra da CLT:
    15 dias ou mais trabalhados no mês contam como mês cheio (1/12 avos).
    """
    meses = 0
    data_atual = inicio

    # Itera ano a ano/mês a mês (lógica simplificada para fins didáticos)
    # Uma abordagem matemática seria: (ano_fim - ano_inicio) * 12 + mes_fim - mes_inicio
    # Mas precisamos validar a fração de 15 dias nos meses de ponta.

    # Cálculo simplificado focado em "avos":
    # 1. Diferença bruta de meses
    diferenca_meses = (fim.year - inicio.year) * 12 + (fim.month - inicio.month)

    # 2. Ajuste do mês de entrada (se trabalhou < 15 dias, não conta)
    # Ex: Admitido dia 20/01. Janeiro não conta.
    if (30 - inicio.day) + 1 < 15:
        diferenca_meses -= 1

    # 3. Ajuste do mês de saída (se trabalhou >= 15 dias, conta)
    # Ex: Saiu dia 20/05. Maio conta. O diff já considera o mês cheio, então
    # só removemos se NÃO trabalhou 15 dias.
    if fim.day < 15:
        diferenca_meses -= 1

    # Garante que contamos o próprio mês se for o mesmo
    return max(0, diferenca_meses + 1)  # +1 para incluir o mês corrente se válido


def calcular_rescisao(admissao_str: str, demissao_str: str, salario: float) -> dict:
    """
    Calcula as verbas rescisórias proporcionais (Saldo, 13º e Férias).
    Retorna um dicionário com os valores calculados.
    """
    admissao = datetime.strptime(admissao_str, "%d/%m/%Y")
    demissao = datetime.strptime(demissao_str, "%d/%m/%Y")

    # 1. Saldo de Salário (Dias trabalhados no mês da demissão)
    # Divisor padrão comercial é 30 dias
    dias_trabalhados_mes = demissao.day
    saldo_salario = (salario / 30) * dias_trabalhados_mes

    # 2. Cálculo do 13º Salário Proporcional (Ano Civil: Jan a Dez)
    # Início da contagem: O maior valor entre (01/Jan do ano da saída) OU (Data Admissão)
    inicio_ano_civil = datetime(demissao.year, 1, 1)
    data_inicio_13 = max(admissao, inicio_ano_civil)

    avos_13 = calcular_meses_trabalhados(data_inicio_13, demissao)
    decimo_terceiro = (salario / 12) * avos_13

    # 3. Cálculo de Férias Proporcionais (Ano Aquisitivo: Aniversário da Admissão)
    # Precisamos encontrar o início do último período aquisitivo
    # Se o aniversário da admissão no ano da demissão já passou, o início é neste ano.
    # Se não, o início foi no ano passado.
    aniversario_neste_ano = datetime(demissao.year, admissao.month, admissao.day)

    if demissao >= aniversario_neste_ano:
        inicio_periodo_aquisitivo = aniversario_neste_ano
    else:
        inicio_periodo_aquisitivo = datetime(demissao.year - 1, admissao.month, admissao.day)

    avos_ferias = calcular_meses_trabalhados(inicio_periodo_aquisitivo, demissao)

    valor_ferias = (salario / 12) * avos_ferias
    terco_ferias = valor_ferias / 3
    total_ferias = valor_ferias + terco_ferias

    return {
        "saldo_salario": saldo_salario,
        "dias_trabalhados": dias_trabalhados_mes,
        "decimo_terceiro": decimo_terceiro,
        "avos_13": avos_13,
        "total_ferias": total_ferias,
        "avos_ferias": avos_ferias
    }


# --- Simulação de Uso ---
dados = calcular_rescisao("05/03/2023", "20/05/2024", 3000.00)

print("-" * 30)
print("RESUMO DA RESCISÃO")
print("-" * 30)
print(f"Saldo de Salário ({dados['dias_trabalhados']} dias): \tR$ {dados['saldo_salario']:,.2f}")
print(f"13º Proporcional ({dados['avos_13']}/12 avos): \tR$ {dados['decimo_terceiro']:,.2f}")
print(f"Férias + 1/3 ({dados['avos_ferias']}/12 avos): \tR$ {dados['total_ferias']:,.2f}")
print("-" * 30)
print(f"TOTAL BRUTO: \t\t\tR$ {(dados['saldo_salario'] + dados['decimo_terceiro'] + dados['total_ferias']):,.2f}")