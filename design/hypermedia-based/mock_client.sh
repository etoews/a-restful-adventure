#!/bin/bash

# requirements: jq (see http://stedolan.github.io/jq/)

set -euo pipefail

HOST=http://localhost:8000

#echo "Create a character"
#curl -s -X POST -H 'Content-type: application/json' -d '{ "name": "Steve" }' $HOST/characters
#
#printf "\n\n"

echo "Get characters"
CHARACTERS=$(http $HOST/characters)
echo $CHARACTERS | jq .
CHARACTER_LINK=$(echo $CHARACTERS | jq -r '.characters[0].links[] | select(.rel == "self").href')
CHARACTER_LOCATION_LINK=$(echo $CHARACTERS | jq -r '.characters[0].links[] | select(.rel == "location").href')
echo "Picked character: $CHARACTER_LINK"
echo "Picked character location: $CHARACTER_LOCATION_LINK"

printf "\n\n"

#echo "Get a character"
#curl -X GET -H 'Accept: application/json' $HOST$CHARACTER_LINK
#
#printf "\n\n"

echo "Get dungeons"
DUNGEONS=$(http $HOST/dungeons)
echo $DUNGEONS | jq .
DUNGEON_LINK=$(echo $DUNGEONS | jq -r '.dungeons[0].links[] | select(.rel == "self").href')
ENTRANCE_ROOM_LINK=$(echo $DUNGEONS | jq -r '.dungeons[0].links[] | select(.rel == "room first").href')
echo "Picked dungeon: $DUNGEON_LINK"
echo "Entrance room: $ENTRANCE_ROOM_LINK"

printf "\n\n"

#echo "Get a dungeon"
#curl -s -X GET -H 'Accept: application/json' $HOST/dungeons/$DUNGEON_ID
#
#printf "\n\n"

echo "Enter the dungeon"
http PUT $HOST$CHARACTER_LOCATION_LINK rel=room href=$ENTRANCE_ROOM_LINK

echo "Get a room"
ROOM=$(http $HOST$ENTRANCE_ROOM_LINK)
echo $ROOM | jq .
ROOM_NAME=$(echo $ROOM | jq -r .name)
NEXT_ROOM_LINK=$(echo $ROOM | jq -r '.links[] | select(.rel == "room east").href')
echo "Room name: $ROOM_NAME"
echo "Next room: $NEXT_ROOM_LINK"

printf "\n\n"

echo "Enter the next room"
http PUT $HOST$CHARACTER_LOCATION_LINK rel=room href=$NEXT_ROOM_LINK

echo "Get a room"
ROOM=$(http $HOST$NEXT_ROOM_LINK)
ROOM_NAME=$(echo $ROOM | jq -r .name)
NEXT_ROOM_LINK=$(echo $ROOM | jq -r '.links[] | select(.rel == "room north").href')
echo "Room name: $ROOM_NAME"
echo "Next room: $NEXT_ROOM_LINK"

printf "\n\n"

echo "Enter the next room"
http PUT $HOST$CHARACTER_LOCATION_LINK rel=room href=$NEXT_ROOM_LINK

echo "Get a room"
ROOM=$(http $HOST$NEXT_ROOM_LINK)
ROOM_NAME=$(echo $ROOM | jq -r .name)
echo "Room name: $ROOM_NAME"
