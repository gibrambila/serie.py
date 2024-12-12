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

@app.route('/abrir_editar/<int:id>')
def abrir_editar(id):

    cursor = con.cursor()

    cursor.execute('SELECT * FROM AGENDAMENTO WHERE ID_AGENDAMENTO = ?', (id,))

    info_user = cursor.fetchall()

    return render_template('editar.html', info_user=info_user)

@app.route('/agendamento')
def agendamento():

    cursor = con.cursor()

    cursor.execute("SELECT * FROM agendamento")

    agendamentos = cursor.fetchall()

    return render_template('agendamento.html', agendamentos=agendamentos)


@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    # Recebe os dados do formulário
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    horario = request.form['horario']
    observacoes = request.form['observacoes']

    cursor = con.cursor()

    try:
        cursor.execute('''
            UPDATE AGENDAMENTO
            SET NOME = ?, EMAIL = ?, TELEFONE = ?, HORARIO = ?, OBSERVACOES = ?
            WHERE ID_AGENDAMENTO = ?
        ''', (nome, email, telefone, horario, observacoes, id))

        con.commit()

    except Exception as e:
        con.rollback()
        print(f"Erro ao atualizar agendamento: {e}")
    finally:
        cursor.close()

    return redirect(url_for('agendamento'))


@app.route('/agendar_consulta', methods=['POST'])
def agendar_consulta():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    horario = request.form['horario']
    observacoes = request.form['observacoes']

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

@app.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['password']

    cursor = con.cursor()

    try:
        cursor.execute("SELECT 1 FROM veterinario WHERE email = ?", (email,))
        if cursor.fetchone():
            flash("Cadastro já realizado.", "error")
            return redirect(url_for('abrir_tela_cadastro'))

        cursor.execute("INSERT INTO veterinario (nome, email, senha) VALUES (?, ?, ?)",
                       (nome, email, senha))
        con.commit()
    finally:
        cursor.close()

    flash("Conta cadastrada com sucesso!", "success")
    return redirect(url_for('abrir_tela_login'))

@app.route('/abrir_tela_login')
def abrir_tela_login():  # put application's code here
    return render_template('login_veterinario.html')

@app.route('/abrir_tela_cadastro')
def abrir_tela_cadastro():  # put application's code here
    return render_template('cadastro.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        email = request.form['email']
        senha = request.form['password']

        cursor = con.cursor()

        if email == '' or senha == '':
            return redirect(url_for('abrir_tela_login'))

        cursor.execute("SELECT 1 FROM veterinario WHERE email  = ? AND senha = ?", (email, senha,))
        if not cursor.fetchone():
            flash("O email ou a senha estão incorretos.", "error")
            return redirect(url_for('abrir_tela_login'))

        con.commit()
    finally:
        cursor.close()
    flash("Login realizado com sucesso!", "success")
    return redirect(url_for('agendamento'))









if __name__ == '__main__':
    app.run(debug=True)
