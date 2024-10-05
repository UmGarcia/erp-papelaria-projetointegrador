from flask import render_template, request, redirect, url_for
from app import db
from app.models import Produto, Categoria, Fornecedor, MovimentoEstoque

@app.route('/')
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

@app.route('/produto/novo', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = float(request.form['preco'])
        quantidade = int(request.form['quantidade'])
        categoria_id = int(request.form['categoria_id'])
        fornecedor_id = int(request.form['fornecedor_id'])
        
        produto = Produto(nome=nome, descricao=descricao, preco=preco, quantidade=quantidade,
                          categoria_id=categoria_id, fornecedor_id=fornecedor_id)
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('index'))
    
    categorias = Categoria.query.all()
    fornecedores = Fornecedor.query.all()
    return render_template('produto/novo.html', categorias=categorias, fornecedores=fornecedores)

@app.route('/movimento/novo', methods=['GET', 'POST'])
def novo_movimento():
    if request.method == 'POST':
        produto_id = int(request.form['produto_id'])
        quantidade = int(request.form['quantidade'])
        tipo = request.form['tipo']
        
        movimento = MovimentoEstoque(produto_id=produto_id, quantidade=quantidade, tipo=tipo)
        db.session.add(movimento)
        
        produto = Produto.query.get(produto_id)
        if tipo == 'entrada':
            produto.quantidade += quantidade
        elif tipo == 'saida':
            produto.quantidade -= quantidade
        
        db.session.commit()
        return redirect(url_for('index'))
    
    produtos = Produto.query.all()
    return render_template('movimento/novo.html', produtos=produtos)