import json

from flask import Flask
from flask import abort
from flask import jsonify
from flask import make_response
from flask import request

from ultidate.entities import Tournament

app = Flask(__name__)


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


app.json_encoder = CustomEncoder

users = dict()


@app.route('/tournaments', methods=['GET'])
def list_tournaments():
    return jsonify(tournaments=list(users.values()))


@app.route('/tournaments', methods=['DELETE'])
def delete_tournaments():
    users.clear()
    return "OK"


@app.route('/tournaments', methods=['POST'])
def add_tournaments():
    # TODO validation
    # TODO json deserialization
    request_json = request.get_json()
    print('Adding tournament: ' + str(request_json))
    users[request_json['name']] = Tournament(request_json['name'], request_json['description'])
    return "OK"


@app.route('/tournaments/<tournament>')
def get_tournament(tournament):
    tournament = users.get(tournament)
    if tournament is None:
        abort(404)
    return jsonify(tournament)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run()
