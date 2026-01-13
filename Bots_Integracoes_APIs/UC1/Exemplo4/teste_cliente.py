import requests
import json

URL = "http://localhost:8000/enriquecer-lead"

# Cenário: Cliente preencheu só isso no formulário
payload = {
    "cep": "01001-000",  # Praça da Sé (SP)
    "cnpj": "00.000.000/0001-91"  # Banco do Brasil (Primeiro CNPJ do Brasil)
}

print(f"📤 Enviando dados parciais: {payload}")

try:
    response = requests.post(URL, json=payload)

    if response.status_code == 200:
        dados = response.json()
        print("\n✅ RETORNO DO ENRIQUECEDOR:")
        print(json.dumps(dados, indent=4, ensure_ascii=False))

        print("\n📝 O que o CRM faria agora:")
        if dados['cnpj_dados'].get('razao_social'):
            print(f"   -> Preencher Razão Social com: {dados['cnpj_dados']['razao_social']}")
        if dados['endereco_dados'].get('logradouro'):
            print(f"   -> Preencher Endereço com: {dados['endereco_dados']['logradouro']}")

    else:
        print(f"❌ Erro na API: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Erro de conexão (O servidor está rodando?): {e}")