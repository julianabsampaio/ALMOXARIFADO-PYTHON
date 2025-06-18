from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

ESTOQUE_FILE = 'estoque.json'

def carregar_estoque():
    if os.path.exists(ESTOQUE_FILE):
        with open(ESTOQUE_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def salvar_estoque(estoque):
    with open(ESTOQUE_FILE, 'w') as f:
        json.dump(estoque, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/entrada', methods=['GET', 'POST'])
def entrada():
    if request.method == 'POST':
        produto = request.form['produto']
        quantidade = int(request.form['quantidade'])
        cidade = request.form['cidade']

        estoque = carregar_estoque()

        if produto not in estoque:
            estoque[produto] = {'quantidade': 0, 'movimentacoes': []}

        estoque[produto]['quantidade'] += quantidade
        estoque[produto]['movimentacoes'].append({
            'tipo': 'entrada',
            'quantidade': quantidade,
            'cidade': cidade
        })

        salvar_estoque(estoque)
        return redirect('/')

    return render_template('entrada.html')

@app.route('/saida', methods=['GET', 'POST'])
def saida():
    if request.method == 'POST':
        produto = request.form['produto']
        quantidade = int(request.form['quantidade'])
        cidade = request.form['cidade']

        estoque = carregar_estoque()

        if produto in estoque and estoque[produto]['quantidade'] >= quantidade:
            estoque[produto]['quantidade'] -= quantidade
            estoque[produto]['movimentacoes'].append({
                'tipo': 'saida',
                'quantidade': quantidade,
                'cidade': cidade
            })
            salvar_estoque(estoque)
        else:
            return "Erro: Produto não existe ou quantidade insuficiente no estoque."

        return redirect('/')

    return render_template('saida.html')

@app.route('/consulta')
def consulta():
    estoque = carregar_estoque()
    return render_template('consulta.html', estoque=estoque)

if __name__ == '__main__':
    app.run(debug=True)
