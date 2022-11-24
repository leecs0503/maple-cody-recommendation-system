import argparse

from .server.app_runner import AppRunner
from .Config.config import Config


def main():
    parser = argparse.ArgumentParser(description="train server")

    parser.add_argument("--server-host", type=str, help="server host", default="localhost")
    parser.add_argument("--server-port", type=int, help="server port", default=3125)
    parser.add_argument("--train_data_path", type=str, help="train data path", default="./json_data_result1.json")
    parser.add_argument("--model_save_path", type=str, help="model save path", default="./model_result.pth")
    parser.add_argument("--batch_size", type=int, help="data loader batch size", default=32)
    parser.add_argument("--num_workers", type=str, help="number of workers", default=8)

    args = parser.parse_args()

    config = Config(
        server_host=args.server_host,
        server_port=args.server_port,
        train_data_path=args.train_data_path,
        model_save_path=args.model_save_path,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
    )

    AppRunner(
        config=config,
    ).run()


if __name__ == "__main__":
    main()
