from flask import Flask, render_template, request, redirect, url_for, flash, session, render_template_string
import sqlite3 as sql
import json
import ast

app=Flask(__name__)
app.config['SECRET_KEY'] = 'PAOLALINDA'
logado = False

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('login.html')

@app.route('/adm')
def adm():
    if logado == True:
        con = sql.connect("users_db.db")
        cur = con.cursor()
        cur.execute("select * from users")
        usuarios = cur.fetchall()
        return render_template('administrador.html',usuarios=usuarios)
    if logado == False:
        return redirect('/')

@app.route('/login', methods=['POST','GET'])
def login():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    con = sql.connect("users_db.db")
    cur = con.cursor()
    cur.execute("select * from users")
    usuariosBD = cur.fetchall()
    cont = 0
    if nome == 'adm' and senha == '0':
        logado = True
        return redirect('/adm')
    for usuario in usuariosBD:
        usuarioNome = str(usuario[1])
        usuarioSenha = str(usuario[2])
        if usuarioNome == nome and usuarioSenha == senha:
            session['nome'] = request.form.get('nome')
            return redirect("/inicio")
        if cont >= len(usuariosBD):
            flash("Usuário ou senha inválida")
            return redirect("/")
    return render_template('login.html')

@app.route('/cadastrarUsuario', methods=['POST','GET'])
def cadastrarUsuario():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    email = request.form.get('email')
    cpf = request.form.get('cpf')
    con = sql.connect("users_db.db")
    cur=con.cursor()
    verificar_usuario = cur.execute("select * from users")
    if cpf in verificar_usuario:
        flash("cadastro inválido")
        return redirect(url_for('adm'))
    try:
        cur.execute("insert into users (NOME,SENHA,EMAIL,CPF) values(?,?,?,?)", (nome,senha,email,cpf))
        con.commit()
        con.close()
    except:
        flash("cadastro inválido")
        return redirect(url_for('adm'))
    logado = True
    flash(f'{nome} cadastrado(a)')
    return redirect(url_for('adm'))
    
@app.route("/inicio")
def inicio():
    con = sql.connect("form_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from produtos")
    data=cur.fetchall()
    for i in data:
        print(i[0])
    con.close()
    nome = session.get('nome')
    session['nome'] = nome
    if session['nome'] == None: # caso a sessão esteja vazia (sem o nome de usuário)
        return render_template_string("""
            <h2>Olá! Por favor faça seu <a href="{{url_for('login')}}">login</a> no site</h2>
        """)
        return redirect(url_for('home'))
    else:
        return render_template ("inicio.html", datas=data)

@app.route("/add_produto", methods=["POST", "GET"])
def add_produto():
    nome = session.get('nome')
    session['nome'] = nome
    if session['nome'] == None: # caso a sessão esteja vazia (sem o nome de usuário)
        return render_template_string("""
            <h2>Olá! Por favor faça seu <a href="{{url_for('login')}}">login</a> no site</h2>
        """)
        return redirect(url_for('home'))
    else:
        if request.method=="POST":
            nome_produto=request.form["nome_produto"]
            quantidade=request.form["quantidade"]
            data_compra=request.form["data_compra"]
            data_validade=request.form["data_validade"]
            valor_compra=request.form["valor_compra"]
            valor_venda=request.form["valor_venda"]
            lucro_porcentagem=request.form["lucro_porcentagem"]
            con=sql.connect("form_db.db")
            cur=con.cursor()
            cur.execute("insert into produtos (NOME_PRODUTO,QUANTIDADE,DATA_DE_COMPRA,DATA_DE_VALIDADE,VALOR_DE_COMPRA,VALOR_DE_VENDA,LUCRO_EM_PORCENTAGEM) values (?,?,?,?,?,?,?)", (nome_produto, quantidade, data_compra, data_validade, valor_compra, valor_venda, lucro_porcentagem))
            con.commit()
            con.close()
            flash("Produto cadastrado", "success")
            return redirect(url_for("inicio"))
        return render_template("add_produto.html")

@app.route("/edit_produto/<string:id>", methods=["POST","GET"])
def edit_produto(id):
    nome = session.get('nome')
    session['nome'] = nome
    if session['nome'] == None: # caso a sessão esteja vazia (sem o nome de usuário)
        return render_template_string("""
            <h2>Olá! Por favor faça seu <a href="{{url_for('login')}}">login</a> no site</h2>
        """)
        return redirect(url_for('home'))
    else:
        if request.method=="POST":
            nome_produto=request.form["nome_produto"]
            quantidade=request.form["quantidade"]
            data_compra=request.form["data_compra"]
            data_validade=request.form["data_validade"]
            valor_compra=request.form["valor_compra"]
            valor_venda=request.form["valor_venda"]
            lucro_porcentagem=request.form["lucro_porcentagem"]
            con=sql.connect("form_db.db")
            cur=con.cursor()
            cur.execute("update produtos set NOME_PRODUTO=?,QUANTIDADE=?,DATA_DE_COMPRA=?,DATA_DE_VALIDADE=?,VALOR_DE_COMPRA=?,VALOR_DE_VENDA=?,LUCRO_EM_PORCENTAGEM=? where ID=?", (nome_produto, quantidade, data_compra, data_validade, valor_compra, valor_venda, lucro_porcentagem,id))
            con.commit()
            flash("Dados atualizados", "success")
            return redirect(url_for("inicio"))
        con=sql.connect("form_db.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from produtos where ID=?", (id,))
        data=cur.fetchone()
        return render_template("edit_produto.html", datas=data)

@app.route("/delete_produto/<string:id>", methods=["GET"])
def delete_produto(id):
    nome = session.get('nome')
    session['nome'] = nome
    if session['nome'] == None: # caso a sessão esteja vazia (sem o nome de usuário)
        return render_template_string("""
            <h2>Olá! Por favor faça seu <a href="{{url_for('login')}}">login</a> no site</h2>
        """)
        return redirect(url_for('home'))
    else:
        con = sql.connect("form_db.db")
        cur = con.cursor()
        cur.execute("delete from produtos where ID=?", (id,))
        con.commit()
        flash("Dados deletados", "warning")
        return redirect(url_for("inicio"))

@app.route('/excluirUsuario', methods=['POST'])
def excluirUsuario():
    global logado
    logado = True
    nome = request.form.get("nome")
    usuarioID = request.form.get('usuarioExcluir')
    con = sql.connect("users_db.db")
    cur = con.cursor()
    cur.execute(f"delete from users where ID='{usuarioID}' ")
    usuarios = cur.fetchall()
    con.commit()
    con.close()
    flash(F'{nome} excluído com sucesso')
    return redirect(url_for('adm'))

@app.route('/sair')
def sair():
    if 'nome' in session:
        session.pop('nome',None)
    return redirect('/')

if __name__=='__main__':
    app.secret_key="admin123"
    app.run(debug=True)

