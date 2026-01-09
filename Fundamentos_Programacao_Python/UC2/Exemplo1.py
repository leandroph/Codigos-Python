import hashlib
import shutil
import csv
from pathlib import Path
from datetime import datetime


def calcular_hash(arquivo: Path) -> str:
    """Calcula o hash MD5 de um arquivo de forma eficiente (em blocos)."""
    hash_md5 = hashlib.md5()
    try:
        with open(arquivo, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except OSError:
        return ""


def auditar_duplicados(diretorio_raiz: str):
    pasta_raiz = Path(diretorio_raiz)
    pasta_quarentena = pasta_raiz / "Quarentena_Duplicados"
    pasta_quarentena.mkdir(exist_ok=True)

    # Dicionário para guardar {HASH: Caminho_do_Original}
    arquivos_unicos = {}
    log_movimentacao = []

    print(f" Auditando: {pasta_raiz}...")

    # rglob('*') percorre todas as subpastas
    for arquivo in pasta_raiz.rglob("*"):
        if arquivo.is_file() and "Quarentena_Duplicados" not in str(arquivo):

            file_hash = calcular_hash(arquivo)
            if not file_hash: continue  # Pula arquivos com erro de leitura

            if file_hash in arquivos_unicos:
                # É duplicata! Mover para quarentena
                destino = pasta_quarentena / arquivo.name

                # Tratamento se já existir arquivo com mesmo nome na quarentena
                if destino.exists():
                    timestamp = datetime.now().strftime("%H%M%S")
                    destino = pasta_quarentena / f"{arquivo.stem}_{timestamp}{arquivo.suffix}"

                shutil.move(str(arquivo), str(destino))

                log_movimentacao.append({
                    "Arquivo Original": arquivos_unicos[file_hash],
                    "Duplicata Movida": arquivo.name,
                    "Hash": file_hash,
                    "Data": datetime.now()
                })
                print(f"⚠️ Duplicata detectada e movida: {arquivo.name}")
            else:
                # É o primeiro arquivo com esse conteúdo. Registrar.
                arquivos_unicos[file_hash] = str(arquivo)

    # Gerar Log CSV
    if log_movimentacao:
        csv_path = pasta_quarentena / "relatorio_movimentacao.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=log_movimentacao[0].keys())
            writer.writeheader()
            writer.writerows(log_movimentacao)
        print(f" Auditoria concluída. Relatório salvo em {csv_path}")
    else:
        print(" Nenhuma duplicata encontrada.")