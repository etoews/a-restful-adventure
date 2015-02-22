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
            uuid.UUID('c1a008bc-105f-4793-bfa6-a54fbc9ce6b1') : {
                'name': 'Knox Thunderbane',
                'room_id': None
            }
        }

        self._dungeons = {
            uuid.UUID('5a024cd8-2db3-446e-b777-bdc60185a117') : {
                'name': 'Dungeon of Doom',
                'entry_id': uuid.UUID('8f726efc-5e3e-4332-ab24-243a1d3e0b27')
            },
            uuid.UUID('f2e557e6-6b07-417b-b416-17d693f3eadd') : {
                'name': 'Dungeon of Hope',
                'entry_id': uuid.UUID('29cf865c-936e-4dec-8626-9bab41ea619f')
            }
        }

        self._rooms = {
            uuid.UUID('8f726efc-5e3e-4332-ab24-243a1d3e0b27'): {
                'name': 'Super Creepy Entrance',
                'is_exit': False,
                'dungeon_id': uuid.UUID('5a024cd8-2db3-446e-b777-bdc60185a117'),
                'doorways': [
                    {
                        'direction': 'north',
                        'room_id': uuid.UUID('751d5812-144d-40f8-a82d-221dbb3075e2')
                    },
                    {
                        'direction': 'east',
                        'room_id': uuid.UUID('65840050-12d3-4e29-9412-7c3b22fdd52e')
                    }
                ]
            },
            uuid.UUID('751d5812-144d-40f8-a82d-221dbb3075e2'): {
                'name': 'Room',
                'is_exit': False,
                'dungeon_id': uuid.UUID('5a024cd8-2db3-446e-b777-bdc60185a117'),
                'doorways': [
                    {
                        'direction': 'south',
                        'room_id': uuid.UUID('8f726efc-5e3e-4332-ab24-243a1d3e0b27')
                    }
                ]
            },
            uuid.UUID('65840050-12d3-4e29-9412-7c3b22fdd52e'): {
                'name': 'Armory',
                'is_exit': False,
                'dungeon_id': uuid.UUID('5a024cd8-2db3-446e-b777-bdc60185a117'),
                'doorways': [
                    {
                        'direction': 'west',
                        'room_id': uuid.UUID('8f726efc-5e3e-4332-ab24-243a1d3e0b27')
                    },
                    {
                        'direction': 'north',
                        'room_id': uuid.UUID('a7092981-3ceb-401a-9db2-4ed64b08b2bb')
                    }
                ]
            },
            uuid.UUID('a7092981-3ceb-401a-9db2-4ed64b08b2bb'): {
                'name': 'Exit',
                'is_exit': True,
                'dungeon_id': uuid.UUID('5a024cd8-2db3-446e-b777-bdc60185a117'),
                'doorways': [
                    {
                        'direction': 'south',
                        'room_id': uuid.UUID('65840050-12d3-4e29-9412-7c3b22fdd52e')
                    }
                ]
            }
        }

    def list_characters(self):
        # Convert "database" result to an entity

        # TODO: Handle the case that our DB can't be reached
        return [
            {
                'id': character_id,
                'name': details['name'],
                'room_id': details['room_id']
            }

            for character_id, details in self._characters.items()
        ]

    def add_character(self, name):
        character_id = uuid.uuid4()

        # TODO: Handle the case that the name is too long
        character = {
            'name': name,
            'room_id': None
        }

        # TODO: Handle the case that our DB can't be reached
        self._characters[character_id] = character

        character['id'] = character_id
        return character

    def move_character(self, character_id, room_id):
        # TODO: Handle the case that character_id is invalid
        # TODO: Handle the case that our DB can't be reached
        character = self._characters[character_id]

        # TODO: Check that room_id can be reached from the character's
        #       current position (no teleportation allowed!)
        character['room_id'] = room_id

    def get_location(self, character_id):
        # TODO: Handle the case that character_id is invalid
        # TODO: Handle the case that our DB can't be reached
        character = self._characters[character_id]

        room_id = character['room_id']
        room = self._rooms[room_id]

        return room_id, room['dungeon_id']

    def get_room(self, room_id):
        # TODO: Handle the case that room_id is invalid
        # TODO: Handle the case that our DB can't be reached
        room = self._rooms[room_id]

        entity = deepcopy(room)
        entity['id'] = room_id

        return entity

    def list_dungeons(self):
        # Convert the database result to a list of entities

        # TODO: Handle the case that our DB can't be reached
        return [
            {
                'id': dungeon_id,
                'name': details['name'],
                'entry_id': details['entry_id']
            }
            for dungeon_id, details in self._dungeons.items()
        ]


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
        dungeon_id = room['dungeon_id']
        room_id = room['id']

        base_href = 'dungeons/{0}'.format(dungeon_id)

        links = [
            {
                'rel': 'self',
                'allow': ['GET'],
                'href': '{0}/rooms/{1}'.format(base_href, room_id)
            },
            {
                'rel': 'dungeon',
                'allow': ['GET'],
                'href': base_href
            }
        ]

        # Add additional links, one per doorway to another room
        links.extend([
            {
                'rel': 'room ' + doorway['direction'],
                'allow': ['GET'],
                'href': self._id_to_href(doorway['room_id'], dungeon_id)
            }

            for doorway in room['doorways']
        ])

        return {
            'name': room['name'],
            'is_exit': room['is_exit'],
            'links': links
        }

    def _id_to_href(self, room_id, dungeon_id):
        return '/dungeons/{0}/rooms/{1}'.format(dungeon_id, room_id)


class Room(RoomBase):
    """Resource class for the room concept."""

    def __init__(self, controller):
        self._controller = controller

    def on_get(self, req, resp, dungeon_id, room_id):
        # TODO: Handle the case that these are not valid UUIDs
        dungeon_id = uuid.UUID(dungeon_id)
        room_id = uuid.UUID(room_id)

        # Note that we don't actually need the dungeon_id, since
        # the DAL just wants the room_id. We'll just ignore it
        # for now.

        # TODO: If an error is raised, convert it to an instance
        #       of falcon.HTTPError
        room = self._controller.get_room(room_id)

        # Create a resource based on the room entity
        # TODO: If an error is raised, convert it to an instance
        #       of falcon.HTTPError
        resource = self._entity_to_resource(room)

        # Create a JSON representation of the resource
        resp.body = json.dumps(resource, ensure_ascii=False)


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
                'allow': [
                    'GET', 'PUT'
                ],
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

controller = Controller()
api.add_route('/characters', CharacterList(controller))
api.add_route('/characters/{character_id}/location', CharacterLocation(controller))
api.add_route('/dungeons/{dungeon_id}/rooms/{room_id}', Room(controller))
api.add_route('/dungeons', DungeonList(controller))


# ===========================================================================
# WSGI
# ===========================================================================

def application(env, start_response):  # <w1>
    body = 'Hello ' + env['HTTP_X_NAME'] + '\n'

    start_response("200 OK", [('Content-Type', 'text/plain')])
    return [body.encode('utf-8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    server = make_server('127.0.0.1', 8000, api)  # <w2>
    server.serve_forever()
