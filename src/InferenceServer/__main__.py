import kserve
import argparse
from .Model.model import Model


def main():
    parser = argparse.ArgumentParser(description="inference server")

    item_parts = [
        "face",
        "cap",
        "longcoat",
        "weapon",
        "cape",
        "coat",
        "glove",
        "hair",
        "pants",
        "shield",
        "shoes",
        "faceAccessory",
        "eyeAccessory",
        "earrings",
        "skin",
    ]

    gender_list = ["male", "female"]

    for gender in gender_list:
        for part in item_parts:
            parser.add_argument(f"--{gender}_{part}_model_dir", type=str, help=f"{gender}-{part} model dir", default=f"model/{gender}_{part}/{gender}_{part}_model.pt")
            parser.add_argument(f"--{gender}_{part}_answer_dict_dir", type=str, help=f"{gender}-{part} answer dict dir", default=f"model/{gender}_{part}/{gender}_{part}_answer_dict_dir.json")

    parser.add_argument("--model_class_dir", type=str, help="model class dir", default="src.Trainer.models.complement_model.model")
    parser.add_argument("--model_class_name", type=str, help="model class name", default="ComplementModel")

    args = parser.parse_args()

    model_list = [
        Model(
            name=f"{gender}-{part}",
            model_dir=getattr(args, f"{gender}_{part}_model_dir"),
            model_class_dir=args.model_class_dir,
            model_class_name=args.model_class_name,
            model_answer_dict_dir=getattr(args, f"{gender}_{part}_answer_dict_dir"),
        ) for gender in gender_list for part in item_parts
    ]

    for model in model_list:
        model.load()

    kserve.ModelServer().start(model_list)


if __name__ == "__main__":
    main()
