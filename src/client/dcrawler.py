import json
from flask import Flask, jsonify, request

api = Flask(__name__)

gen_character_id = 0
characters = {"characters": []}
dungeons = {
    "dungeons": [
        {
            "id": "1234",
            "name": "Dungeon of Doom",
            "entrance_room_id": "1000"
        },
        {
            "id": "9876",
            "name": "Dungeon of Hope",
            "entrance_room_id": "2000"
        }
    ]
}

@api.route('/')
def index():
    return '<h1>Welcome to the Dungeon</h1>'


def _gen_id():
    global gen_character_id
    gen_character_id += 1

    return gen_character_id

@api.route('/characters')
def get_characters():
    global characters

    return jsonify(characters)


@api.route('/characters', methods=['POST'])
def create_character():
    global characters

    character = {
        "id": str(_gen_id()),
        "name": request.json['name']
    }

    characters['characters'].append(character)

    return jsonify(character)


@api.route('/characters/<character_id>')
def get_character(character_id):
    global characters

    for character in characters['characters']:
        if character['id'] == character_id:
            return jsonify(character)

@api.route('/characters/<character_id>', methods=['PUT'])
def update_character(character_id):
    global characters

    for idx, character in enumerate(characters['characters']):
        if character['id'] == character_id:
            updated_character = request.json
            characters['characters'][idx] = updated_character

    return '', 204

@api.route('/dungeons')
def get_dungeons():
    global dungeons

    return jsonify(dungeons)


@api.route('/dungeons/<dungeon_id>')
def get_dungeon(dungeon_id):
    global dungeons

    for dungeon in dungeons['dungeons']:
        if dungeon['id'] == dungeon_id:
            return jsonify(dungeon)


if __name__ == '__main__':
    api.run(debug=True)
