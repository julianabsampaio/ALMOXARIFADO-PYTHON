import json
from datetime import datetime

ARQUIVO_ESTOQUE = 'estoque.json'

def carregar_estoque():
    try:
        with open(ARQUIVO_ESTOQUE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def salvar_estoque(estoque):
    with open(ARQUIVO_ESTOQUE, 'w') as f:
        json.dump(estoque, f, indent=4)

def registrar_movimento(produto, quantidade, tipo, cidade):
    estoque = carregar_estoque()
    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if produto not in estoque:
        estoque[produto] = {
            'quantidade': 0,
            'movimentacoes': []
        }

    estoque[produto]['quantidade'] += quantidade
    estoque[produto]['movimentacoes'].append({
        'data_hora': data_hora,
        'tipo': tipo,
        'quantidade': quantidade,
        'cidade': cidade
    })

    salvar_estoque(estoque)
    print(f"\nMovimento registrado: {tipo.upper()} de {quantidade} unidades de '{produto}' na cidade '{cidade}'.")

def consultar_estoque():
    estoque = carregar_estoque()
    if not estoque:
        print("\nEstoque vazio.")
    else:
        print("\n--- Estoque Atual ---")
        for produto, dados in estoque.items():
            print(f"{produto}: {dados['quantidade']} unidades")

def relatorio_movimentacoes():
    estoque = carregar_estoque()
    if not estoque:
        print("\nNenhuma movimentação registrada.")
    else:
        print("\n--- Relatório de Movimentações ---")
        for produto, dados in estoque.items():
            print(f"\nProduto: {produto} - Quantidade Atual: {dados['quantidade']}")
            for mov in dados['movimentacoes']:
                print(f"  -> {mov['data_hora']} | {mov['tipo']} | {mov['quantidade']} unidades | Cidade: {mov['cidade']}")

def menu():
    while True:
        print("\n==== SISTEMA DE ALMOXARIFADO ====")
        print("1. Registrar Entrada")
        print("2. Registrar Saída")
        print("3. Consultar Estoque")
        print("4. Relatório de Movimentações")
        print("5. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            produto = input("Produto: ")
            quantidade = int(input("Quantidade: "))
            cidade = input("Cidade: ")
            registrar_movimento(produto, quantidade, 'entrada', cidade)

        elif opcao == '2':
            produto = input("Produto: ")
            quantidade = int(input("Quantidade: "))
            cidade = input("Cidade: ")
            registrar_movimento(produto, -quantidade, 'saida', cidade)

        elif opcao == '3':
            consultar_estoque()

        elif opcao == '4':
            relatorio_movimentacoes()

        elif opcao == '5':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
