from flask import Flask, jsonify
import json
import os
import sys
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from server.service import DBService

app = Flask(__name__)
access_db = DBService()


@app.route("/")
def hello():
    return """Facebook Scraper.<br/><br/><br/>
            Endpoints:<br/>
                    /actors - lista todos os atores<br/>
                    /date - lista as datas de coleta<br/>
                    /&ltdate&gt;/&ltactor&gt; - lista os dados coletados
                        do ator na determinada data<br/>
                    /latest/&ltactor&gt; - lista os dados dos atores
                        na ultima data coletada"""


@app.route('/actors', methods=['GET'])
def show_actors_collected():
    return jsonify(json.loads(access_db.get_actors_from_db()))


@app.route('/date', methods=['GET'])
def show_date():
    try:
        return jsonify(json.loads(access_db.get_all_date()))
    except Exception:
        return 'Ocorreu um erro ao tentar pegar as datas'


@app.route('/<date>/<actor_name>', methods=['GET'])
def show_basic_data(date, actor_name):
    try:
        if(date == 'latest'):
            data = json.loads(access_db.get_all_date())
            date = data['latest']
            print(date)
        return jsonify(
            json.loads(access_db.get_basic_actor_data(actor_name, date))
        )
    except Exception:
        return 'Data nao encontrada, verifique o nome do ator e a data'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
