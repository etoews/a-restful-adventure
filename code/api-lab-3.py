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
        base_href = self._id_to_href(character['id'])
        links = [
            {
                'rel': 'self',
                'allow': [
                    'GET', 'PUT'
                ],
                'href': base_href
            },
            {
                'rel': 'location',
                'allow': [
                    'GET', 'PUT'
                ],
                'href': base_href + '/location'
            }
        ]

        return {
            'name': character['name'],
            'links': links
        }

    def _id_to_href(self, character_id):
        return '/characters/{0}'.format(character_id)

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
        # Ask the DAL for a list of entities
        # TODO: If an error is raised, convert it to an instance
        #       of falcon.HTTPError
        characters = self._controller.list_characters()

        # Map the entities to the resource
        resource = {
            'characters': [self._entity_to_resource(c) for c in characters],
            'links': [
                {
                    'rel': 'self',
                    'allow': ['GET', 'POST'],
                    'href': '/characters'
                }
            ]
        }

        # Create a JSON representation of the resource
        resp.body = json.dumps(resource, ensure_ascii=False)

        # Falcon defaults to the JSON media type for the content
        # resp.content_type = 'application/json'

        # Falcon defaults to 200 OK
        # resp.status = falcon.HTTP_200

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
        resp.body = 'Hello ' + req.get_header('x-name') + '\n'
        resp.content_type = 'text/plain'

        # Falcon defaults to 200 OK
        # resp.status = falcon.HTTP_200


# ===========================================================================
# Routing
# ===========================================================================

# An instance of falcon.API is a WSGI application
api = falcon.API()
# api.add_route('/', HelloResource())  # <w4>

controller = dal.Controller()
api.add_route('/characters', CharacterList(controller))
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

    host = '127.0.0.1'
    port = 8000
    server = make_server(host, port, application)  # <w2>

    print('Listening on {0}:{1}'.format(host, port))
    server.serve_forever()
