from copy import deepcopy
import json
import uuid

import falcon

import dal


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
# Hello world
# ===========================================================================

class HelloResource(object):  # <w3>
    def on_get(self, req, resp):
        resp.body = 'Hello ' + req.get_header('x-name') + '!\n'

        # Falcon defaults to 'application/json'
        resp.content_type = 'text/plain'

        # Falcon defaults to 200 OK
        # resp.status = falcon.HTTP_200


# ===========================================================================
# Routing
# ===========================================================================

# An instance of falcon.API is a WSGI application
api = falcon.API()
api.add_route('/', HelloResource())  # <w4>

controller = dal.Controller()
# <a14>
# <a15>
# <a16>
# <a17>


# ===========================================================================
# WSGI
# ===========================================================================

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    host = '127.0.0.1'
    port = 8000
    server = make_server(host, port, api)  # <w2>

    print('Listening on {0}:{1}'.format(host, port))
    server.serve_forever()
