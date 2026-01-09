def caixa_eletronico():
    try:
        valor_inicial = int(input("Valor do saque: R$ "))
        valor = valor_inicial  # Cópia para manipular

        if valor <= 0:
            print("Erro: Valor inválido.")
            return

        # Lista de cédulas disponíveis (fácil de adicionar R$ 200 ou R$ 5 aqui)
        cedulas_disponiveis = [100, 50, 20, 10]

        # Verifica se é possível sacar com as notas disponíveis (Mínimo R$ 10)
        if valor % 10 != 0:
            print("Erro: Notas disponíveis apenas de 10, 20, 50 e 100.")
            return

        print(f"\nSacando R$ {valor_inicial:.2f}...")

        # A mágica acontece aqui: um loop resolve tudo
        for cedula in cedulas_disponiveis:
            qtd_notas = valor // cedula

            if qtd_notas > 0:
                print(f"{qtd_notas} nota(s) de R$ {cedula},00")
                valor %= cedula

    except ValueError:
        print("Erro: Digite apenas números inteiros.")


# Executar
caixa_eletronico()