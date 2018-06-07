from flask import Flask, jsonify
import json
import os
from service import DBService

app = Flask(__name__)

@app.route("/")
def hello():
    return "Facebook Scraper."

@app.route('/actors', methods=['GET'])
def show_actors_collected():
    access_db = DBService()
    # with open('json/actors.json') as actors:
    return jsonify(json.loads(access_db.get_actors_from_db()))


@app.route('/date', methods=['GET'])
def show_date():
    access_db = DBService()
    return jsonify(json.loads(access_db.get_all_date()))

@app.route('/basic/<date>/<actor_name>', methods=['GET'])
def show_basic_data(date, actor_name):
    access_db = DBService()
    if(date == 'latest'):
        data = json.loads(access_db.get_all_date())
        date = data['latest']
        print(date)
    return jsonify(json.loads(access_db.get_basic_actor_data(actor_name, date)))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
