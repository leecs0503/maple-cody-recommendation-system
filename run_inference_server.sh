#!/bin/bash

python -m src.InferenceServer \
    --model_json " \
        [ \
            [\"male\", \"hair\"], \
            [\"male\", \"cap\"], \
            [\"male\", \"faceAccessory\"], \
            [\"male\", \"face\"], \
            [\"male\", \"eyeAccessory\"], \
            [\"male\", \"earrings\"], \
            [\"male\", \"weapon\"], \
            [\"male\", \"longcoat\"], \
            [\"male\", \"shield\"], \
            [\"male\", \"pants\"], \
            [\"male\", \"glove\"], \
            [\"male\", \"cape\"],  \
            [\"male\", \"shoes\"], \
            [\"female\", \"hair\"], \
            [\"female\", \"cap\"], \
            [\"female\", \"faceAccessory\"], \
            [\"female\", \"face\"], \
            [\"female\", \"eyeAccessory\"], \
            [\"female\", \"earrings\"], \
            [\"female\", \"weapon\"], \
            [\"female\", \"longcoat\"], \
            [\"female\", \"shield\"], \
            [\"female\", \"pants\"], \
            [\"female\", \"glove\"], \
            [\"female\", \"cape\"], \
            [\"female\", \"shoes\"] \
        ]"