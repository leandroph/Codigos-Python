import os
from typing import Dict, List, Union, Any

# Definição de Tipo para facilitar a leitura (Alias)
# Um Produto é um dicionário com chaves string e valores variados
Produto = Dict[str, Union[int, str, float]]

# Lista global para armazenar os dados em memória
estoque: List[Produto] = []


def limpar_tela() -> None:
    """
    Limpa o console do terminal dependendo do Sistema Operacional.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def cadastrar_produto() -> None:
    """
    Solicita dados ao usuário e adiciona um novo dicionário à lista de estoque.
    Gera ID automático baseado no último item da lista.
    """
    print("--- NOVO PRODUTO ---")
    nome = input("Nome do Produto: ").strip()

    # Validação para não cadastrar nome vazio
    if not nome:
        print("Erro: O nome do produto não pode ser vazio.")
        return

    try:
        qtd = int(input("Quantidade: "))
        preco = float(input("Preço Unitário (R$): "))

        if qtd < 0 or preco < 0:
            print("Erro: Valores não podem ser negativos.")
            return

    except ValueError:
        print("Erro: Quantidade deve ser inteiro e Preço deve ser número (ex: 10.50).")
        return

    # Lógica de Auto-incremento do ID
    # Se a lista tiver itens, pega o ID do último e soma 1. Se vazia, é 1.
    novo_id = estoque[-1]['id'] + 1 if estoque else 1

    produto: Produto = {
        "id": novo_id,
        "nome": nome,
        "qtd": qtd,
        "preco": preco
    }

    estoque.append(produto)
    print(f"\n✅ Produto '{nome}' cadastrado com sucesso! ID: {novo_id}")


def buscar_produto() -> None:
    """
    Solicita um ID e busca o produto correspondente na lista.
    Exibe os detalhes se encontrar.
    """
    print("--- BUSCAR PRODUTO ---")
    try:
        id_busca = int(input("Digite o ID do produto: "))
    except ValueError:
        print("Erro: O ID deve ser um número inteiro.")
        return

    # Busca linear na lista
    encontrado: Union[Produto, None] = None

    for item in estoque:
        if item['id'] == id_busca:
            encontrado = item
            break

    if encontrado:
        print(f"\n{' DETALHES DO PRODUTO ':=^30}")
        print(f"ID:    {encontrado['id']}")
        print(f"Nome:  {encontrado['nome']}")
        print(f"Qtd:   {encontrado['qtd']}")
        print(f"Preço: R$ {encontrado['preco']:.2f}")
        print("=" * 30)
    else:
        print(f"\n❌ Produto com ID {id_busca} não encontrado.")


def remover_produto() -> None:
    """
    Solicita um ID, busca o índice na lista e remove o item.
    """
    print("--- REMOVER PRODUTO ---")
    try:
        id_remove = int(input("Digite o ID do produto para remover: "))
    except ValueError:
        print("Erro: O ID deve ser um número inteiro.")
        return

    indice_para_remover = -1

    # Enumerate fornece o índice (i) e o objeto (item)
    for i, item in enumerate(estoque):
        if item['id'] == id_remove:
            indice_para_remover = i
            break

    if indice_para_remover != -1:
        # pop(indice) remove o item naquela posição e o retorna
        removido = estoque.pop(indice_para_remover)
        print(f"\n🗑️  Produto '{removido['nome']}' removido com sucesso!")
    else:
        print(f"\n❌ Produto com ID {id_remove} não encontrado.")


def relatorio_geral() -> None:
    """
    Itera sobre toda a lista de estoque e imprime uma tabela formatada.
    Calcula o valor total do patrimônio em estoque.
    """
    print("\n--- RELATÓRIO DE ESTOQUE ---")
    # Formatação de string:
    # < alinha à esquerda, > alinha à direita, números indicam o tamanho do espaço
    print(f"{'ID':<5} {'NOME':<25} {'QTD':<8} {'PREÇO':<12} {'TOTAL ITEM':<12}")
    print("-" * 65)

    valor_total_estoque = 0.0

    if not estoque:
        print("Estoque vazio.")
    else:
        for item in estoque:
            # Type casting para garantir que o linter entenda que são números
            qtd = int(item['qtd'])
            preco = float(item['preco'])

            total_item = qtd * preco
            valor_total_estoque += total_item

            print(f"{item['id']:<5} {item['nome']:<25} {qtd:<8} R$ {preco:<9.2f} R$ {total_item:<9.2f}")

    print("-" * 65)
    print(f"VALOR TOTAL EM ESTOQUE: R$ {valor_total_estoque:.2f}")


def menu_principal() -> None:
    """
    Função controladora que exibe o menu e gerencia o loop principal.
    """
    while True:
        limpar_tela()
        print("=== GESTÃO DE ESTOQUE (MEMÓRIA) ===")
        print("1. Cadastrar Produto")
        print("2. Buscar Produto por ID")
        print("3. Remover Produto")
        print("4. Relatório Geral")
        print("5. Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == '1':
            cadastrar_produto()
        elif opcao == '2':
            buscar_produto()
        elif opcao == '3':
            remover_produto()
        elif opcao == '4':
            relatorio_geral()
        elif opcao == '5':
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida!")

        input("\nPressione Enter para continuar...")


# Execução do programa
if __name__ == "__main__":
    menu_principal()