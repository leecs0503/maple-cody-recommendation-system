#!bin/bash
#
# avatar server의 /packed_character_look으로의 테스트 콜
curl -X POST -H "Content-Type: application/json" http://0.0.0.0:7000/v1/character-info -d \
"{ \
    \"user_name\": \"인품\"\
}"


# curl -X POST -H "Content-Type: application/json" http://0.0.0.0:8080/packed_character_look -d \
# "{ \
#     \"packed_character_look\": \"JMOABMIKLNNJIBGJPJFMBNOOLEHFGILCMPOJHJCENAAEAEHKDECPGEMJEMMFKLAFFPBBGGNGNLIENCMODMCEGLBCEEPOHHPCHHLJJKAANDADBMOMCBGEBFAPIKIKJDFIIDEDKJLGPLDBLBJFCCHDLDNEFCGDPANLNKKPFCAOBGJMEHMKJAHBMANPHKFBEMGODHDPFGGEKLDAJOMGNMJGPHAIDKKALGAHCLFDGDJHFFDCIJFMMFKJDABNMMEGPHLM\"\
# }"
