from copy import deepcopy
import json
import uuid

import falcon


# ===========================================================================
# DAL (backend, storage and entities)
# ===========================================================================

class Controller(object):
    def __init__(self):
        # Store data in MyLDB

        self._characters = {
            # <d1>
        }

        self._dungeons = {
            # <d2>
        }

        self._rooms = {
            # <d3>

            # <d4>
        }

    def list_characters(self):
        # <d5>
        pass

    def add_character(self, name):
        # <d6>
        pass

    def move_character(self, character_id, room_id):
        # <d7>
        pass

    def get_location(self, character_id):
        # <d8>
        pass

    def get_room(self, room_id):
        # <d9>
        pass

    def list_dungeons(self):
        # <d9>
        pass


# ===========================================================================
# API (frontend, resources and representations)
# ===========================================================================

class CharacterBase(object):
    """Base class for character resources.

    This class consolidates the translation logic between backend and
    frontent concepts.
    """

    def _entity_to_resource(self, character):
        # <a1>
        pass

    def _id_to_href(self, character_id):
        # <a2>
        pass

    def _room_href_to_id(self, href):
        # <a3>
        pass

    def _room_id_to_location(self, room_id, dungeon_id):
        # <a4>
        pass


class CharacterLocation(CharacterBase):
    """Resource class for the character location concept."""

    def __init__(self, controller):
        self._controller = controller

    def on_get(self, req, resp, character_id):
        # <a5>
        pass

    def on_put(self, req, resp, character_id):
        # <a6>
        pass


class CharacterList(CharacterBase):
    """Resource class for the character list concept."""

    def __init__(self, controller):
        # Controller instance is shared between resource classes
        self._controller = controller

    def on_get(self, req, resp):
        # <a7>
        pass

    def on_post(self, req, resp):
        # <a8>
        pass


class RoomBase(object):
    """Base class for room resources.

    This class consolidates the translation logic between backend and
    frontent concepts.
    """

    def _entity_to_resource(self, room):
        # <a9>
        pass

    def _id_to_href(self, room_id, dungeon_id):
        # <a10>
        pass


class Room(RoomBase):
    """Resource class for the room concept."""

    def __init__(self, controller):
        self._controller = controller

    def on_get(self, req, resp, dungeon_id, room_id):
        # <a11>
        pass


class DungeonBase(object):
    """Base class for dungeon resources.

    This class consolidates the translation logic between backend and
    frontent concepts.
    """

    def _entity_to_resource(self, dungeon):
        # <a12>
        pass

class DungeonList(DungeonBase):
    """Resource class for the dungeon list concept."""

    def __init__(self, controller):
        # Controller instance is shared between resource classes
        self._controller = controller

    def on_get(self, req, resp):
        # <a13>
        pass


# ===========================================================================
# Routing
# ===========================================================================

# An instance of falcon.API is a WSGI application
api = falcon.API()

controller = Controller()
# <a14>
# <a15>
# <a16>
# <a17>


# ===========================================================================
# WSGI
# ===========================================================================

def application(env, start_response):  # <w1>
    body = 'Hello ' + env['HTTP_X_NAME'] + '\n'

    start_response("200 OK", [('Content-Type', 'text/plain')])
    return [body.encode('utf-8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    server = make_server('127.0.0.1', 8000, application)  # <w2>
    server.serve_forever()
