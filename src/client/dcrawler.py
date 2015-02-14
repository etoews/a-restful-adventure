from flask import Flask, jsonify

api = Flask(__name__)


@api.route('/')
def index():
    return '<h1>Welcome to the Dungeon</h1>'


@api.route('/characters', methods=['POST'])
def create_character():
    character = {
        "id": "1234",
        "name": "Knox Thunderbane"
    }

    return jsonify(character)


@api.route('/characters')
def get_characters():
    characters = {
        "characters": [
            {
                "id": "1234",
                "name": "Knox Thunderbane",
                "dungeon_id": "2345",
                "room_id": "3456"
            }
        ]
    }

    return jsonify(characters)


@api.route('/characters/<id>')
def get_character(id):
    character = {
        "id": "1234",
        "name": "Knox Thunderbane"
    }

    return jsonify(character)


@api.route('/dungeons')
def get_dungeons():
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

    return jsonify(dungeons)


@api.route('/dungeons/<id>')
def get_dungeon(id):
    dungeon = {
        "id": "1234",
        "name": "Dungeon of Doom",
        "entrance_room_id": "1000"
    }

    return jsonify(dungeon)


if __name__ == '__main__':
    api.run(debug=True)
