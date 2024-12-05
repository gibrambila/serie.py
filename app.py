from flask import Flask, render_template

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

host = 'localhost'
database = ''
user = ''
password = ''


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/agendamentos', methods=['GET', 'POST'])
def agendamentos():  # put application's code here
    return render_template('agendamento.html')


@app.route('/login')
def login():  # put application's code here
    return render_template('login_veterinario.html')





if __name__ == '__main__':
    app.run(debug=True)
