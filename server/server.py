from flask import Flask, jsonify
import json
import os

app = Flask(__name__)


@app.route("/")
def hello():
    return "Facebook Scraper."

@app.route('/actor/<actor_name>', methods=['GET'])
def actor_name(actor_name):
    with open('json/actors.json') as actors:
        return jsonify(json.load(actors)) 

# @app.route('/actorjson/<actor_name>', methods=['GET'])
# def actor_name_json(actor_name):
#     return jsonify({'actor_name' : actor_name})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=True)