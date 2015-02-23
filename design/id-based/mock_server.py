from flask import Flask, jsonify, request, url_for

api = Flask(__name__)

gen_character_id = 0
characters = {}
dungeons = {
    "1234": {
        "id": "1234",
        "name": "Dungeon of Doom",
        "entrance_room_id": "1000"
    },
    "9876": {
        "id": "9876",
        "name": "Dungeon of Hope",
        "entrance_room_id": "2000"
    }
}
rooms = {
    "1000": {
        "id": "1000",
        "name": "Entrance",
        "dungeon_id": "1234",
        "is_exit": False,
        "doors": [
            {
                "room_id": "1001",
                "direction": "east"
            }
        ]},
    "1001": {
        "id": "1001",
        "name": "Hallway",
        "dungeon_id": "1234",
        "is_exit": False,
        "doors": [
            {
                "room_id": "1002",
                "direction": "east"
            },
            {
                "room_id": "1000",
                "direction": "west"
            }
        ]},
    "1002": {
        "id": "1002",
        "name": "Exit",
        "dungeon_id": "1234",
        "is_exit": True,
        "doors": [
            {
                "room_id": "1001",
                "direction": "west"
            }
        ]}
}


@api.route('/')
def index():
    return '<h1>Welcome to the Dungeon</h1>'


def _gen_id():
    global gen_character_id
    gen_character_id += 1

    return str(gen_character_id)


@api.route('/characters')
def get_characters():
    global characters

    return jsonify({"characters": list(characters.values())})


@api.route('/characters', methods=['POST'])
def create_character():
    global characters

    new_id = _gen_id()
    character = {
        "id": new_id,
        "name": request.json['name']
    }
    characters[new_id] = character
    location = {'Location': url_for('.get_character', character_id=new_id, _external=True)}

    return jsonify(character), 201, location


@api.route('/characters/<character_id>')
def get_character(character_id):
    global characters

    return jsonify(characters[character_id])


@api.route('/characters/<character_id>', methods=['PUT'])
def update_character(character_id):
    global characters

    characters[character_id] = request.json

    return '', 204


@api.route('/dungeons')
def get_dungeons():
    global dungeons

    return jsonify({"dungeons": list(dungeons.values())})


@api.route('/dungeons/<dungeon_id>')
def get_dungeon(dungeon_id):
    global dungeons

    return jsonify(dungeons[dungeon_id])


# TODO: dungeon_id isn't strictly necessary but do we keep it for the pretty URL?
@api.route('/dungeons/<dungeon_id>/rooms/<room_id>')
def get_room(dungeon_id, room_id):
    global rooms

    return jsonify(rooms[room_id])


if __name__ == '__main__':
    api.run(debug=True)
