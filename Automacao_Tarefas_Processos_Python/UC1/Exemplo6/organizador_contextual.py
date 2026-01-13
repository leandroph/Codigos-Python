import shutil
from pathlib import Path

# --- CONFIGURAÇÕES ---
PASTA_BASE = Path("Downloads_Bagunça")

# Regras de Contexto (Palavra-chave -> Pasta Destino)
# O script vai procurar essas palavras no NOME do arquivo
REGRAS_SEMANTICAS = {
    "Comercial": ["contrato", "proposta", "minuta", "orçamento", "acordo"],
    "Financeiro": ["fatura", "boleto", "comprovante", "nota fiscal", "recibo", "pagamento"],
    "Relatórios": ["relatorio", "dashboard", "analise"]
}

# Regras de Extensão (Fallback para Mídia)
EXTENSOES_MIDIA = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov']


def organizar_downloads():
    if not PASTA_BASE.exists():
        print("Pasta de origem não encontrada. Rode o setup primeiro.")
        return

    print(f"Iniciando organização em: {PASTA_BASE}\n")

    arquivos_movidos = 0

    # Itera sobre todos os itens da pasta
    for arquivo in PASTA_BASE.iterdir():
        # Ignora se for pasta, queremos mover apenas arquivos
        if arquivo.is_dir():
            continue

        nome_arquivo = arquivo.name.lower()  # Converter para minúsculo para facilitar a busca
        destino_final = None
        categoria = "Desconhecido"

        # --- LÓGICA 1: ANÁLISE SEMÂNTICA (CONTEXTO) ---
        # Verifica se alguma palavra-chave está contida no nome do arquivo
        encontrou_contexto = False

        for pasta_destino, palavras_chave in REGRAS_SEMANTICAS.items():
            # Verifica se QUALQUER uma das palavras chaves está no nome
            if any(palavra in nome_arquivo for palavra in palavras_chave):
                destino_final = PASTA_BASE / pasta_destino
                categoria = pasta_destino
                encontrou_contexto = True
                break  # Parar de procurar outras regras se já achou

        # --- LÓGICA 2: ANÁLISE TÉCNICA (EXTENSÃO) ---
        # Se não caiu em nenhuma regra de texto, verifica se é imagem/mídia
        if not encontrou_contexto:
            if arquivo.suffix.lower() in EXTENSOES_MIDIA:
                destino_final = PASTA_BASE / "Mídia"
                categoria = "Mídia"
                encontrou_contexto = True

        # --- LÓGICA 3: FALLBACK (TRIAGEM) ---
        # Se não é contrato, não é financeiro e não é imagem, vai para Triagem
        if not encontrou_contexto:
            destino_final = PASTA_BASE / "Triagem"
            categoria = "Triagem"

        # --- EXECUÇÃO (MOVER) ---
        if destino_final:
            # Criar a pasta de destino se não existir
            destino_final.mkdir(exist_ok=True)

            # Caminho completo do novo arquivo
            novo_caminho = destino_final / arquivo.name

            # Evitar sobreposição de nomes (se o arquivo já existir no destino)
            if novo_caminho.exists():
                timestamp = arquivo.stat().st_mtime
                novo_caminho = destino_final / f"{arquivo.stem}_{int(timestamp)}{arquivo.suffix}"

            shutil.move(str(arquivo), str(novo_caminho))
            print(f"->{arquivo.name:<40} movido para [{categoria}]")
            arquivos_movidos += 1

    print(f"\nOrganização concluída! {arquivos_movidos} arquivos processados.")


if __name__ == "__main__":
    organizar_downloads()