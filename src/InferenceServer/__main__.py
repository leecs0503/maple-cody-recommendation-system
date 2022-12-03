import kserve
import argparse
import json
from .Model.complement_model import KserveComplementModel


def main():
    parser = argparse.ArgumentParser(description="inference server")

    parser.add_argument("--model_json", type=str, help="model json", default="[]")

    args = parser.parse_args()

    model_list_to_make = json.loads(args.model_json)

    model_list = [
        KserveComplementModel(
            name=f"{gender}-{part}",
            model_dir=getattr(args, f"{gender}_{part}_model_dir"),
            model_answer_dict_dir=getattr(args, f"{gender}_{part}_answer_dict_dir"),
        ) for gender, part in model_list_to_make
    ]

    for model in model_list:
        model.load()

    kserve.ModelServer(http_port=9000).start(model_list)


if __name__ == "__main__":
    main()
