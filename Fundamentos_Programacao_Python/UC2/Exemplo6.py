import shutil
import time
from pathlib import Path


def backup_incremental(origem: str, destino: str):
    src = Path(origem)
    dst = Path(destino)

    copiados = 0
    ignorados = 0

    print(f" Sincronizando de {src.name} para {dst.name}...")

    # rglob('*') pega arquivos e pastas recursivamente
    for item in src.rglob("*"):
        if item.is_file():
            # Cria o caminho correspondente no destino
            relativo = item.relative_to(src)
            arquivo_destino = dst / relativo

            deve_copiar = False

            if not arquivo_destino.exists():
                deve_copiar = True
                motivo = "Novo"
            else:
                # Compara Data de Modificação e Tamanho
                src_stat = item.stat()
                dst_stat = arquivo_destino.stat()

                # Se origem for mais nova (maior timestamp) ou tamanho diferente
                if src_stat.st_mtime > dst_stat.st_mtime or src_stat.st_size != dst_stat.st_size:
                    deve_copiar = True
                    motivo = "Atualizado"

            if deve_copiar:
                # Garante que a pasta pai existe no destino
                arquivo_destino.parent.mkdir(parents=True, exist_ok=True)

                # copy2 preserva metadados (datas)
                shutil.copy2(item, arquivo_destino)
                print(f"COPY [{motivo}]: {relativo}")
                copiados += 1
            else:
                ignorados += 1

    print(f"\nResumo: {copiados} copiados, {ignorados} ignorados (já atualizados).")