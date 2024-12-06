from flask import Flask, render_template, request, flash, redirect, url_for
import fdb

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

host = 'localhost'
database = r'C:\Users\Aluno\Downloads\BANCO (3)\BANCO.FDB'
user = 'sysdba'
password = 'sysdba'

#Conexão

con = fdb.connect( host=host, database=database, user=user, password=password )


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/agendamentos', methods=['POST'])
def agendamentos():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    horario = request.form['horario']
    observacoes = request.form['observacoes']


    # Criando o cursor
    cursor = con.cursor()

    try:
        cursor.execute("SELECT 1 FROM agendamento WHERE email = ? AND  horario =?", (email,horario))
        if cursor.fetchone():  # Se existir algum registro
            flash("Erro: Já possui agendamento.", "error")
            return redirect(url_for('agendamentos'))

        # Inserir o novo cadastro (sem capturar o ID)
        cursor.execute("INSERT INTO agendamento (nome, email, telefone, horario, observacoes  ) VALUES (?, ?, ?, ?, ?)",
                           (nome, email, telefone, horario, observacoes))
        con.commit()
    finally:
        # Fechar o cursor manualmente, mesmo que haja erro
        cursor.close()

    flash("Agendamento cadastrado com sucesso!", "success")
    return redirect(url_for('index'))
    #buscar agendamentos
    # Rota para exibir a lista de livros em um layout HTML

@app.route('/abrir_tela_cadastro')
def abrir_tela_cadastro():  # put application's code here
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['password']


    # Criando o cursor
    cursor = con.cursor()

    try:
        # Verificar se o livro já existe
        cursor.execute("SELECT 1 FROM veterinario WHERE nome  = ? AND email = ? AND senha = ?", (nome, email, senha,))
        if cursor.fetchone():  # Se existir algum registro
            flash("Erro: cadastro já realizado.", "error")
            return redirect(url_for('novo'))

        # Inserir o novo livro (sem capturar o ID)
        cursor.execute("INSERT INTO veterinario (nome, email, senha) VALUES (?, ?, ?)",
                       (nome, email, senha))
        con.commit()
    finally:
        # Fechar o cursor manualmente, mesmo que haja erro
        cursor.close()
    flash("Conta cadastrada com sucesso!", "success")
    return redirect(url_for('index'))

@app.route('/abrir_tela_login')
def abrir_tela_login():  # put application's code here
    return render_template('login_veterinario.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        email = 'giovana@gmail.com'
        senha = '5555'

        # Criando o cursor
        cursor = con.cursor()
        # Verificar se o livro já existe
        cursor.execute("SELECT 1 FROM veterinario WHERE nome  = ? AND senha = ?", (email, senha,))
        if cursor.fetchone():  # Se existir algum registro
            flash("Erro: O email não existe", "error")
            return redirect(url_for('login'))

    # Inserir o novo livro (sem capturar o ID)
        con.commit()
    finally:
    # Fechar o cursor manualmente, mesmo que haja erro
        cursor.close()
    flash("Conta cadastrada com sucesso!", "success")
    return redirect('login')













if __name__ == '__main__':
    app.run(debug=True)
