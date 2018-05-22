from flask import Flask, jsonify
import json
import os

app = Flask(__name__)


@app.route("/")
def hello():
    return "Facebook Scraper."

@app.route('/actors', methods=['GET'])
def show_actors_collected():
    with open('json/actors.json') as actors:
        return jsonify(json.load(actors)) 


@app.route('/date', methods=['GET'])
def show_date():
    with open('json/date.json') as date:
        return jsonify(json.load(date))

@app.route('/<date>/<actor_name>', methods=['GET'])
def show_data_scraped(date, actor_name):
    with open('json/' + date + '/' + actor_name + '.json') as scraped_data:
        return jsonify(json.load(scraped_data))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
