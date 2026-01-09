import re
from pathlib import Path


def extrair_emails_dump(arquivo_entrada: str):
    entrada = Path(arquivo_entrada)
    if not entrada.exists():
        print("Arquivo não encontrado.")
        return

    texto = entrada.read_text(encoding='utf-8', errors='ignore')

    # Regex robusto para e-mails
    regex_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    # findall devolve uma lista. set() remove duplicatas automaticamente.
    emails_encontrados = set(re.findall(regex_email, texto))

    # Ordenar por domínio (o que vem depois do @)
    # x.split('@')[1] pega o domínio
    emails_ordenados = sorted(list(emails_encontrados), key=lambda x: x.split('@')[1])

    # Salvar resultado
    saida = entrada.parent / "mailing_limpo.txt"
    with open(saida, 'w', encoding='utf-8') as f:
        f.write(f"Total Encontrado: {len(emails_ordenados)}\n")
        f.write("-" * 30 + "\n")
        for email in emails_ordenados:
            f.write(f"{email}\n")

    print(f" Extração concluída. {len(emails_ordenados)} e-mails únicos salvos.")