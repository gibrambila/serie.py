from flask import Flask, render_template, request

app = Flask(__name__)

series_list = [
    {"serie": 1, "titulo": "Heartland", "genero": "Drama/Comédia/família", "ano": "2007", "descricao": "Em meio a segredos, paixões e rivalidades, a família Heartland se mantém unida para enfrentar os desafios da vida e administrar sua fazenda.", "imagem": "Heartland.jfif"},
    {"serie": 2, "titulo": "Gossip Girl", "genero": "Drama/Romance", "ano": "2007", "descricao": "Explorações de eventos inexplicáveis, romances, moda e enigmas.", "imagem": "gossip_girl.jpg"},
    {"serie": 3, "titulo": "Mako Mermaids", "genero": "Drama/Romance/ficção científica", "ano": "201", "descricao": "Uma série emocionante sobre uma jovem que enfrenta desafios para se adaptar à nova família e descobrir seu passado.", "imagem": "anne_com_e.jpg"},
    {"serie": 4, "titulo": "O verão que mudou minha vida", "genero": "Drama/Romance", "ano": "2019", "descricao": "História de romance sobre um verão que mudou a vida de uma jovem garota.", "imagem": "o_verao_que_mudou_minha_vida.jpg"},
    {"serie": 5, "titulo": "Bridgerton", "genero": "Drama/Romance", "ano": "2022", "descricao": "Uma saga de histórias de romance antigas da realeza.", "imagem": "bridgerton.jpg"},
    {"serie": 6, "titulo": "Stranger Things", "genero": "Ficção Científica/Terror", "ano": "2016", "descricao": "Mistério e terror se misturam em uma pequena cidade com eventos sobrenaturais.", "imagem": "stranger_things.jpg"},
    {"serie": 7, "titulo": "Elite", "genero": "Drama/Romance", "ano": "2018", "descricao": "Drama colegial sobre adolescentes da elite e vários mistérios de uma pequena cidade.", "imagem": "elite.jpg"},
    {"serie": 8, "titulo": "You", "genero": "Suspense/Mistério", "ano": "2018", "descricao": "Trama girada em torno de um homem obcecado que persegue suas vítimas.", "imagem": "you.jpg"}
]

@app.route('/')
def index():
    return render_template('pesquisa.serie.html', series=series_list)

@app.route('/add_series', methods=['GET', 'POST'])
def add_series():
    if request.method == 'POST':
        titulo = request.form['titulo']
        genero = request.form['genero']
        ano = request.form['ano']
        descricao = request.form['descricao']
        imagem = request.form['imagem']
        serie = len(series_list) + 1
        series_list.append({"serie": serie, "titulo": titulo, "genero": genero, "ano": ano, "descricao": descricao})
        return render_template('list_series.html', series=series_list)
    return render_template('add_series.html')

if __name__ == '__main__':
    app.run(debug=True)
