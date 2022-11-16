#!bin/bash
#
# avatar server의 /packed_character_look으로의 테스트 콜

curl -X POST -H "Content-Type: application/json" http://0.0.0.0:8080/avatar_image -d \
'{"avatar": {"face": "20100", "cap": "1004999", "longcoat": "1052975", "weapon": "1703238", "cape": "1103204", "coat": "0", "glove": "1082102", "hair": "30000+2*16", "pants": "0", "shield": "0", "shoes": "1073670", "faceAccessory": "1012673", "eyeAccessory": "1022079", "earrings": "1032024", "skin": "12016"}}'