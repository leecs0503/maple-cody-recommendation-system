#!/bin/bash

python -m src.InferenceServer \
    --model_json " \
        [ \
            [\"male\", \"weapon\"], \
            [\"female\", \"weapon\"], \
            [\"male\", \"cap\"], \
            [\"female\", \"cap\"], \
            [\"male\", \"cape\"], \
            [\"female\", \"cape\"] \
        ]"