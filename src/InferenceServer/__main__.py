import kserve
import argparse
import json
from .Model.complement_model import KserveComplementModel


def main():
    parser = argparse.ArgumentParser(description="inference server")

    parser.add_argument("--model_json", type=str, help="model json", default="[]")

    args = parser.parse_args()

    for gender in gender_list:
        for part in item_parts:
            parser.add_argument(f"--{gender}_{part}_model_dir", type=str, help=f"{gender}-{part} model dir", default=f"model/{gender}_{part}/{gender}_{part}_model.pt")
            parser.add_argument(f"--{gender}_{part}_answer_dict_dir", type=str, help=f"{gender}-{part} answer dict dir", default=f"model/{gender}_{part}/{gender}_{part}_answer_dict.json")

    model_list_to_make = json.loads(args.model_json)

    model_list = [
        KserveComplementModel(
            name=f"complement-model-{gender}-{part}",
            model_dir=f"/mnt/models/complement_model/{gender}_{part}_model.pt",
            model_answer_dict_dir=f"/mnt/models/complement_model/{gender}_{part}_answer_dict.json",
        ) for gender, part in model_list_to_make
    ]

    for model in model_list:
        model.load()

    kserve.ModelServer(http_port=9000).start(model_list)


if __name__ == "__main__":
    main()
