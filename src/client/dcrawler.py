from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Welcome to the Dungeon</h1>'

@app.route('/characters')
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
  return '<h1>Welcome to the Dungeon</h1>'

if __name__ == '__main__':
  app.run(debug=True)
