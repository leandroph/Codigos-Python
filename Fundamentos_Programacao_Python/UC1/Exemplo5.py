import os


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


# Dicionário acumulador
votos = {
    "candidato_1": 0,
    "candidato_2": 0,
    "candidato_3": 0,
    "nulo": 0,
    "branco": 0
}

# Loop de Votação
while True:
    limpar_tela()
    print("=== URNA ELETRÔNICA ===")
    print("1. Candidato A")
    print("2. Candidato B")
    print("3. Candidato C")
    print("4. Nulo")
    print("5. Branco")
    print("'FIM' para encerrar")

    voto = input("\nDigite seu voto: ").strip().upper()

    if voto == 'FIM':
        break

    # Processamento do Voto
    if voto == '1':
        votos['candidato_1'] += 1
        print(">> Voto registrado para Candidato A!")
    elif voto == '2':
        votos['candidato_2'] += 1
        print(">> Voto registrado para Candidato B!")
    elif voto == '3':
        votos['candidato_3'] += 1
        print(">> Voto registrado para Candidato C!")
    elif voto == '4':
        votos['nulo'] += 1
        print(">> Voto NULO registrado!")
    elif voto == '5':
        votos['branco'] += 1
        print(">> Voto EM BRANCO registrado!")
    else:
        print(">> Opção inválida! Tente novamente.")

    input("Pressione Enter para continuar...")

# --- Apuração (Boletim de Urna) ---
limpar_tela()
print("=== BOLETIM DE URNA ===\n")

total_validos = votos['candidato_1'] + votos['candidato_2'] + votos['candidato_3']
total_geral = total_validos + votos['nulo'] + votos['branco']

# Exibe resultados individuais
for candidato, qtd in votos.items():
    print(f"{candidato.replace('_', ' ').title()}: {qtd} votos")

print("-" * 30)
print(f"Total Geral: {total_geral}")
print(f"Votos Válidos: {total_validos}")

if total_validos > 0:
    porcentagem_nulos = ((votos['nulo'] + votos['branco']) / total_geral) * 100
    print(f"Brancos/Nulos: {porcentagem_nulos:.1f}% do total")
    print("-" * 30)

    # Lógica do Vencedor (Apenas entre candidatos)
    # Filtra apenas as chaves que começam com 'candidato'
    candidatos_apenas = {k: v for k, v in votos.items() if k.startswith('candidato')}

    # Acha quem teve mais votos entre os candidatos
    lider = max(candidatos_apenas, key=candidatos_apenas.get)
    votos_lider = candidatos_apenas[lider]

    # Regra: Precisa de 50% + 1 dos votos VÁLIDOS para vencer no 1º turno
    limite_vitoria = total_validos / 2

    if votos_lider > limite_vitoria:
        print(f"RESULTADO: {lider.replace('_', ' ').title()} ELEITO no 1º Turno!")
    else:
        print(f"RESULTADO: Haverá SEGUNDO TURNO.")
        print(f"(O líder {lider} não atingiu 50% + 1 dos votos válidos)")

else:
    print("\nNenhum voto válido registrado.")