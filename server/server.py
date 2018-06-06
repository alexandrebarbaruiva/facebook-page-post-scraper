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
    return jsonify(access_db.get_actors_from_db())


@app.route('/date', methods=['GET'])
def show_date():
    with open('json/'+'date.json') as date:
        return jsonify(json.load(date))

@app.route('/basic/<date>/<actor_name>', methods=['GET'])
def show_basic_data(date, actor_name):
    if(date == 'latest'):
        with open('json/date.json', 'r', encoding='utf8') as date_file:
            data = json.load(date_file)
        date = data['latest']
    actor_name.replace(" ","")
    with open('json/' + date + '/' + actor_name + '.json') as scraped_data:
        return jsonify(json.load(scraped_data))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
