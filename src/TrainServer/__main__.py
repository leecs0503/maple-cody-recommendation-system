import argparse

from .server.app_runner import AppRunner
from .Config.config import Config


def main():
    parser = argparse.ArgumentParser(description="train server")

    parser.add_argument("--server-host", type=str, help="server host", default="localhost")
    parser.add_argument("--server-port", type=int, help="server port", default=3125)
    parser.add_argument("--model_path", type=str, help="model path", default="./model_result.pth")
    parser.add_argument("--batch_size", type=int, help="data loader batch size", default=32)
    parser.add_argument("--num_workers", type=str, help="number of workers", default=8)
    parser.add_argument("--tensorboard_path", type=str, help="tensorboard path", default="runs/")

    args = parser.parse_args()

    config = Config(
        server_host=args.server_host,
        server_port=args.server_port,
        model_path=args.model_path,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        tensorboard_path=args.tensorboard_path,
    )

    AppRunner(
        config=config,
    ).run()


if __name__ == "__main__":
    main()
