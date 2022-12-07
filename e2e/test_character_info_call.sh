#!bin/bash

curl -X POST -H "Content-Type: application/json" http://0.0.0.0:7000/v1/character-info -d \
"{ \
    \"user_name\": \"인품\"\
}"
