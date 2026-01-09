import os
import zipfile
import time
from datetime import datetime, timedelta
from pathlib import Path


def faxina_servidor(diretorio_logs: str):
    pasta = Path(diretorio_logs)
    pasta_backup = pasta / "Backup_Logs"
    pasta_backup.mkdir(exist_ok=True)

    agora = datetime.now()
    espaco_liberado_bytes = 0
    arquivos_zipados = 0
    arquivos_deletados = 0

    print(" Iniciando limpeza de logs...")

    for arquivo in pasta.glob("*.log"):
        # Obtém data de modificação
        stats = arquivo.stat()
        data_modificacao = datetime.fromtimestamp(stats.st_mtime)
        tamanho_original = stats.st_size

        idade_dias = (agora - data_modificacao).days

        # Regra 1: Mais de 365 dias -> Deletar direto
        if idade_dias > 365:
            os.remove(arquivo)
            espaco_liberado_bytes += tamanho_original
            arquivos_deletados += 1
            print(f" Deletado (Velho): {arquivo.name}")

        # Regra 2: Entre 30 e 365 dias -> Zipar e Deletar original
        elif idade_dias > 30:
            caminho_zip = pasta_backup / f"{arquivo.stem}.zip"

            with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.write(arquivo, arcname=arquivo.name)

            # Calcula quanto economizou (Tamanho Original - Tamanho Zip)
            tamanho_zip = caminho_zip.stat().st_size
            espaco_liberado_bytes += (tamanho_original - tamanho_zip)

            os.remove(arquivo)
            arquivos_zipados += 1
            print(f" Zipado: {arquivo.name}")

    # Relatório Final
    mb_liberados = espaco_liberado_bytes / (1024 * 1024)
    relatorio = f"""
    --- RELATÓRIO DE FAXINA ---
    Data: {agora}
    Arquivos Deletados (>1 ano): {arquivos_deletados}
    Arquivos Zipados (>30 dias): {arquivos_zipados}
    Espaço em Disco Liberado: {mb_liberados:.2f} MB
    """

    (pasta / "relatorio_faxina.txt").write_text(relatorio, encoding='utf-8')
    print(relatorio)