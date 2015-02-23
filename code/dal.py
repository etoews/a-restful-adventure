from copy import deepcopy
import uuid


# ===========================================================================
# DAL (backend, storage and entities)
# ===========================================================================

class Controller(object):
    def __init__(self):
        # Store data in MyLDB

        self._characters = {
            uuid.UUID('c1a008bc-105f-4793-bfa6-a54fbc9ce6b1') : {
                'name': 'Knox Thunderbane',
                'room_id': uuid.UUID('4e99416c-f018-4636-b81d-06853163fe9a')
            }
        }

        self._dungeons = {
            # Special "dungeon" that represents a location outside any dungeon
            uuid.UUID('aeac18ba-9323-455b-a20d-453cf28d5caa') : {
                'name': '*',
                'entry_id': uuid.UUID('4e99416c-f018-4636-b81d-06853163fe9a')
            },

            uuid.UUID('5a024cd8-2db3-446e-b777-bdc60185a117') : {
                'name': 'Dungeon of Doom',
                'entry_id': uuid.UUID('8f726efc-5e3e-4332-ab24-243a1d3e0b27')
            }
        }

        self._rooms = {
            # Special "room" that represents a location outside any dungeon
            uuid.UUID('4e99416c-f018-4636-b81d-06853163fe9a'): {
                'name': '*',
                'is_exit': False,
                'dungeon_id': uuid.UUID('aeac18ba-9323-455b-a20d-453cf28d5caa'),
                'doorways': []
            },

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
                'name': 'Armory',
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
                'name': 'Gaurd Room',
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
        if room_id is None:
            return None

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
