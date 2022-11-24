import argparse

from .server.app_runner import AppRunner


def main():
    parser = argparse.ArgumentParser(description="train server")

    parser.add_argument("--server-host", type=str, help="server host", default="localhost")
    parser.add_argument("--server-port", type=int, help="server port", default=3125)

    args = parser.parse_args()

    AppRunner(
        server_host=args.server_host,
        server_port=args.server_port,
    ).run()


if __name__ == "__main__":
    main()
