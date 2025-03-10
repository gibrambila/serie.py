from flask import Flask, jsonify, request
from main import app, con
from flask_bcrypt import generate_password_hash, check_password_hash
import jwt


app.config.from_pyfile('config.py')

senha_secreta = app.config['SECRET_KEY']


def generate_token(user_id):
    payload = {'id_usuario': user_id}
    token = jwt.encode(payload, senha_secreta, algorithm='HS256')
    return token

def remover_bearer(token):
    if token.starteith('Bearer'):
        return token [len('Bearer'):]
    else:
        return token






@app.route('/livro', methods=['GET'])
def livro():
    cur = con.cursor()
    cur.execute("SELECT id_livro, titulo, autor, ano_publicacao FROM livros")
    livros = cur.fetchall()
    livros_dic = []
    for livro in livros:
        livros_dic.append({
            'id_livro': livro [0],
            'titulo': livro[1],
            'autor': livro[2],
            'ano_publicacao': livro[3]

        })
    return jsonify(mensagem='lista de livros', livros=livros_dic)



@app.route('/livro', methods=['POST'])
def livros_post():
    data = request.get_json()
    titulo = data.get('titulo')
    autor = data.get('autor')
    ano_publicacao = data.get('ano_publicacao')

    cursor = con.cursor()

    cursor.execute("SELECT 1 FROM LIVROS WHERE TITULO = ?", (titulo,))
    if cursor.fetchone():
        return jsonify('Livro já cadastrado')
    cursor.execute("INSERT INTO LIVROS(TITULO, AUTOR, ANO_PUBLICACAO) VALUES (?, ?, ?)",
                   (titulo, autor, ano_publicacao))

    con.commit()
    cursor.close()

    return jsonify({
     'message':'Livro cadastrado com sucesso!',
     'livro': {
         'titulo': titulo,
         'autor': autor,
         'ano_publicacao': ano_publicacao
        }
    })





#Rota delete

@app.route('/livro/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    cursor = con.cursor()

    # Verificar se o livro existe
    cursor.execute("SELECT 1 FROM LIVROS WHERE ID_LIVRO = ?", (id,))
    if not cursor.fetchone():
        cursor.close()
        return jsonify({"error": "Livro não encontrado"}), 404

    # Excluir o livro
    cursor.execute("DELETE FROM LIVROS WHERE ID_LIVRO = ?", (id,))
    con.commit()
    cursor.close()

    return jsonify({
        'message': "Livro excluído com sucesso!",
        'id_livro': id
    })





#Rotas de usuário:


@app.route('/usuario', methods=['GET'])
def usuario():
    cur = con.cursor()
    cur.execute("SELECT id_usuario, nome, email, senha FROM usuario")
    usuario = cur.fetchall()
    usuario_dic = []
    for usuario in usuario:
        usuario_dic.append({
            'id_usuario': usuario[0],
            'nome': usuario[1],
            'email': usuario[2],
            'senha': usuario[3]
        })
    return jsonify(mensagem='Lista de usuarios', usuario=usuario_dic)

@app.route('/usuario', methods=['POST'])
def usuario_post():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    cursor = con.cursor()

    cursor.execute("SELECT 1 FROM usuario WHERE nome = ?", (nome,))

    if cursor.fetchone():
        return jsonify("Usuario já cadastrado")

    senha = generate_password_hash(senha).decode('utf-8')

    cursor.execute("INSERT INTO usuario(nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))

    con.commit()
    cursor.close()

    return jsonify({
        'menssage': 'Usuario cadastrado',
        'usuario': {
            'nome': nome,
            'email': email,
            'senha': senha
        }
    })

@app.route('/usuario/<int:id>', methods=['PUT'])
def usuario_put(id):
    cursor = con.cursor()
    cursor.execute(" select id_usuario, nome, email, senha from usuario where id_usuario = ?", (id,))
    usuario_data = cursor.fetchone()

    if not usuario_data:
        cursor.close()
        return jsonify({'Usuario não foi encontrado'})

    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    cursor.execute("update usuario set nome = ?, email = ?, senha = ? where id_usuario = ?", (nome, email, senha, id))

    con.commit()
    cursor.close()

    return jsonify({
        'menssage': 'Usuario cadastrado',
        'usuario': {
            'nome': nome,
            'email': email,
            'senha': senha
        }
    })

@app.route('/usuario/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    cursor = con.cursor()

    cursor.execute("SELECT 1 FROM usuario WHERE ID_usuario = ?", (id,))
    if not cursor.fetchone():
        cursor.close()
        return jsonify({"error": "Usuario não encontrado"})

    cursor.execute("DELETE FROM usuario WHERE ID_usuario = ?", (id,))
    con.commit()
    cursor.close()

    return jsonify({
        'message': "Usuario excluído com sucesso!",
        'id_usuario': id
    })




#login

    @app.route('/login', methods=['POST'])
    def login():
    data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')
        cursor = con.cursor()

        cursor.execute("SELECT senha, id_usuario FROM usuario WHERE email = ?", (email,))
        resultado = cursor.fetchone()
        cursor.close()
        if not resultado:
            return jsonify({"error": "Usuário não encontrado"}), 404
        senha_hash = resultado[0]
        id_usuario = resultado[1]

        if email and check_password_hash(senha_hash, senha):
            # Gera um token JWT para o usuário autenticado
            token = generate_token(id_usuario)
            return jsonify({'mensagem': 'Login com sucesso', 'token': token}), 200
        else:
            # Se as credenciais estiverem incorretas, retorna uma mensagem de erro
            return jsonify({'mensagem': 'Email ou senha inválido'}), 401


@app.route('/livro_imagem', methods=['POST'])
def livro_imagem():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'mensagem': 'Token de autenticação necessário'}), 401

    token = remover_bearer(token)
    try:
        payload = jwt.decode(token, senha_secreta, algorithms=['HS256'])
        id_usuario = payload['id_usuario']
    except jwt.ExpiredSignatureError:
        return jsonify({'mensagem': 'Token expirado'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'mensagem': 'Token inválido'}), 401

    # Recebendo os dados do formulário (não JSON)
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    ano_publicacao = request.form.get('ano_publicacao')
    imagem = request.files.get('imagem')  # Arquivo enviado

    cursor = con.cursor()

    # Verifica se o livro já existe
    cursor.execute("SELECT 1 FROM livros WHERE TITULO = ?", (titulo,))
    if cursor.fetchone():
        cursor.close()
        return jsonify({"error": "Livro já cadastrado"}), 400

    # Insere o novo livro e retorna o ID gerado
    cursor.execute(
        "INSERT INTO livros (TITULO, AUTOR, ANO_PUBLICACAO) VALUES (?, ?, ?) RETURNING ID_livro",
        (titulo, autor, ano_publicacao)
    )
    livro_id = cursor.fetchone()[0]
    con.commit()

    # Salvar a imagem se for enviada
    imagem_path = None
    if imagem:
        nome_imagem = f"{livro_id}.jpeg"  # Define o nome fixo com .jpeg
        pasta_destino = os.path.join(app.config['UPLOAD_FOLDER'], "Livros")
        os.makedirs(pasta_destino, exist_ok=True)
        imagem_path = os.path.join(pasta_destino, nome_imagem)
        imagem.save(imagem_path)

    cursor.close()

    return jsonify({
        'message': "Livro cadastrado com sucesso!",
        'livro': {
            'id': livro_id,
            'titulo': titulo,
            'autor': autor,
            'ano_publicacao': ano_publicacao,
            'imagem_path': imagem_path
        }
    }), 201