#!/bin/bash

# requirements: jq (see http://stedolan.github.io/jq/)

set -euo pipefail

HOST=http://localhost:5000

echo "Create a character"
curl -s -X POST -H 'Content-type: application/json' -d '{ "name": "Steve" }' $HOST/characters

printf "\n\n"

echo "Get characters"
CHARACTERS=$(curl -s -X GET -H 'Accept: application/json' $HOST/characters)
echo $CHARACTERS
CHARACTER_ID=$(echo $CHARACTERS | jq -r .characters[0].id)
echo "Picked character id: $CHARACTER_ID"

printf "\n\n"

echo "Get a character"
curl -s -X GET -H 'Accept: application/json' $HOST/characters/$CHARACTER_ID

printf "\n\n"

echo "Get dungeons"
DUNGEONS=$(curl -s -X GET -H 'Accept: application/json' $HOST/dungeons)
echo $DUNGEONS
DUNGEON_ID=$(echo $DUNGEONS | jq -r .dungeons[0].id)
ENTRANCE_ROOM_ID=$(echo $DUNGEONS | jq -r .dungeons[0].entrance_room_id)
echo "Picked dungeon id: $DUNGEON_ID"
echo "Entrance room id: $ENTRANCE_ROOM_ID"

printf "\n\n"

echo "Get a dungeon"
curl -s -X GET -H 'Accept: application/json' $HOST/dungeons/$DUNGEON_ID

