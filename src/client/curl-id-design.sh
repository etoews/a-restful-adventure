HOST=http://api.dungeoncrawler.io

# Create a character
curl -X POST -H 'Content-type: application/json' -d '{ "name": "$NAME" }'

# Pick a character (just grab the first one for simplicity sake)
CHARACTER_ID=$(curl -X GET -H 'Accept: application/json' $HOST/characters | jq -r .characters[0].id)

