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

    for part in item_parts:
        parser.add_argument(f"--{part}-model-dir", type=str, help=f"{part} model dir", default=f"./model/{part}")

    parser.add_argument("--model-class-dir", type=str, help="model class dir", default="./src/Trainer/models/complement_model")
    parser.add_argument("--model-class-name", type=str, help="model class name", default="ComplementModel")

    args = parser.parse_args()

    model_list = [
        Model(
            name=part,
            model_dir=getattr(args, f"{part}_model_dir"),
            model_class_dir=args.model_class_dir,
            model_class_name=args.model_class_name,
        ) for part in item_parts
    ]

    for model in model_list:
        model.load()

    kserve.ModelServer().start(model_list)


if __name__ == "__main__":
    main()
