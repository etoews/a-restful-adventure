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
        # ID will be the last part of the URL.
        return uuid.UUID(href.split('/')[-1])

    def _room_id_to_location(self, room_id, dungeon_id):
        return {
            'rel': 'room',
            'allow': ['GET'],
            'href': 'dungeons/{0}/rooms/{1}'.format(dungeon_id, room_id)
        }


class CharacterLocation(CharacterBase):
    """Resource class for the character location concept."""

    def __init__(self, controller):
        self._controller = controller

    def on_get(self, req, resp, character_id):
        # TODO: Handle the case that character_id is not a valid UUID
        character_id = uuid.UUID(character_id)

        # TODO: If an error is raised, convert it to an instance
        #       of falcon.HTTPError
        room_id, dungeon_id = self._controller.get_location(character_id)

        # Define the resource. We have to translate the DAL's notion
        # of a "location" to the API's concept of a "location".
        # TODO: If an error is raised, convert it to an instance
        #       of falcon.HTTPError
        resource = self._room_id_to_location(room_id, dungeon_id)

        # Create a JSON representation of the resource
        # TODO: Use functools.partial to create a version of json.dumps that
        #       defaults to ensure_ascii=False
        resp.body = json.dumps(resource, ensure_ascii=False)

    def on_put(self, req, resp, character_id):
        # TODO: Validate against a schema
        representation = req.stream.read().decode('utf-8')
        representation = json.loads(representation)

        # TODO: Raise falcon.HTTPError if ID is not a UUID
        character_id = uuid.UUID(character_id)

        # TODO: Raise falcon.HTTPError if ID is not a UUID
        room_href = representation['href']
        room_id = self._room_href_to_id(room_href)

        # TODO: If an error is raised, convert it to an instance
        #       of falcon.HTTPError
        self._controller.move_character(character_id, room_id)

        # Success!
        resp.status = falcon.HTTP_204


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
        # Parse the incoming representation. This can be factored out into
        # Falcon hooks or middleware, but we'll keep it inline for now.
        # TODO: Validate against a schema
        representation = req.stream.read().decode('utf-8')
        representation = json.loads(representation)

        # Create a new entity from the representation
        # TODO: If an error is raised, convert it to an instance
        #       of falcon.HTTPError
        character = self._controller.add_character(representation['name'])

        # Map the entity to the resource. Again, this sort of thing
        # could be factored out into a Falcon hook (DRY).
        resource = self._entity_to_resource(character)

        resp.location = self._id_to_href(character['id'])
        resp.body = json.dumps(resource, ensure_ascii=False)


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
        base_href = '/dungeons/{0}'.format(dungeon['id'])
        links = [
            {
                'rel': 'self',
                'allow': ['GET'],
                'href': base_href
            },
            {
                'rel': 'room first',
                'allow': ['GET'],
                'href': '{0}/rooms/{1}'.format(base_href, dungeon['entry_id'])
            }
        ]

        return {
            'name': dungeon['name'],
            'links': links
        }


class DungeonList(DungeonBase):
    """Resource class for the dungeon list concept."""

    def __init__(self, controller):
        # Controller instance is shared between resource classes
        self._controller = controller

    def on_get(self, req, resp):
        # Ask the DAL for a list of entities
        dungeons = self._controller.list_dungeons()

        # Map the entities to the resource
        resource = {
            'dungeons': [self._entity_to_resource(d) for d in dungeons],
            'links': [
                {
                    'rel': 'self',
                    'allow': ['GET'],
                    'href': '/dungeons'
                }
            ]
        }

        # Create a JSON representation of the resource
        resp.body = json.dumps(resource, ensure_ascii=False)


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
# api.add_route('/', HelloResource())  # <w4>

controller = dal.Controller()
api.add_route('/characters', CharacterList(controller))
api.add_route('/characters/{character_id}/location', CharacterLocation(controller))
# <a16>
api.add_route('/dungeons', DungeonList(controller))


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
