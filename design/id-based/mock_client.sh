#!/bin/bash

# requirements:
#   jq (see http://stedolan.github.io/jq/)
#   httpie (see http://httpie.org)

set -euo pipefail

HOST=http://localhost:5000

echo "Create a character"
http POST $HOST/characters name=Steve

printf "\n\n"

echo "Get characters"
CHARACTERS=$(http $HOST/characters)
echo $CHARACTERS | jq .
CHARACTER_ID=$(echo $CHARACTERS | jq -r .characters[0].id)
echo "Picked character id: $CHARACTER_ID"

printf "\n\n"

echo "Get a character"
http $HOST/characters/$CHARACTER_ID

printf "\n\n"

echo "Get dungeons"
DUNGEONS=$(http $HOST/dungeons)
echo $DUNGEONS | jq .
DUNGEON_ID=$(echo $DUNGEONS | jq -r .dungeons[0].id)
ENTRANCE_ROOM_ID=$(echo $DUNGEONS | jq -r .dungeons[0].entrance_room_id)
echo "Picked dungeon id: $DUNGEON_ID"
echo "Entrance room id: $ENTRANCE_ROOM_ID"

printf "\n\n"

echo "Get a dungeon"
http $HOST/dungeons/$DUNGEON_ID

printf "\n\n"

echo "Enter the dungeon"
http PUT $HOST/characters/$CHARACTER_ID id=$CHARACTER_ID name=Steve dungeon_id=$DUNGEON_ID room_id=$ENTRANCE_ROOM_ID

echo "Get a room"
ROOM=$(http $HOST/dungeons/$DUNGEON_ID/rooms/$ENTRANCE_ROOM_ID)
ROOM_NAME=$(echo $ROOM | jq -r .name)
NEXT_ROOM_ID=$(echo $ROOM | jq -r .doors[0].room_id)
echo "Room name: $ROOM_NAME"

echo "Get a room"
ROOM=$(http $HOST/dungeons/$DUNGEON_ID/rooms/$NEXT_ROOM_ID)
ROOM_NAME=$(echo $ROOM | jq -r .name)
NEXT_ROOM_ID=$(echo $ROOM | jq -r .doors[0].room_id)
echo "Room name: $ROOM_NAME"

echo "Get a room"
ROOM=$(http $HOST/dungeons/$DUNGEON_ID/rooms/$NEXT_ROOM_ID)
ROOM_NAME=$(echo $ROOM | jq -r .name)
NEXT_ROOM_ID=$(echo $ROOM | jq -r .doors[0].room_id)
echo "Room name: $ROOM_NAME"
