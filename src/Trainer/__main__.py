import simple_parsing
import src.Trainer.trainer
import dataclasses


def main():
    parser = simple_parsing.ArgumentParser(description="train server")

    parser.add_argument("--model_name", type=str, help="model name", default="complement_model")
    parser.add_argument("--gender", type=str, help="model name", default="complement_model")
    parser.add_argument("--parts", type=str, help="model name", default="complement_model")
    first_args, unparsed = parser.parse_known_args()
    model_name = first_args.model_name
    gender = first_args.gender
    parts = first_args.parts

    print(model_name)

    trainer_module = getattr(src.Trainer.trainer, model_name)
    args_cls = trainer_module.TrainerArguments
    parser.add_arguments(args_cls, dest="trainer_arguments")
    args = parser.parse_args()

    trainer_module.Trainer(**{
        **dataclasses.asdict(args.trainer_arguments),
        **{
            "parts": parts,
            "gender": gender
        }
    }).train()


if __name__ == "__main__":
    main()
