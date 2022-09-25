import argparse
from .server.AppRunner import AppRunner


def main():
    parser = argparse.ArgumentParser(description="image server")

    parser.add_argument("--wcr-server-host", type=str, help="wcr server host", default="localhost")
    parser.add_argument("--wcr-server-port", type=int, help="wcr server host", default=80)
    parser.add_argument("--wcr-server-protocol", type=str, help="wcr server host", default="http")
    parser.add_argument("--base-wz-code-path", type=str, help="base", default="./src/ImageServer/base_wz_code.json")

    args = parser.parse_args()

    AppRunner(
        wcr_server_host=args.wcr_server_host,
        wcr_server_port=args.wcr_server_port,
        wcr_server_protocol=args.wcr_server_protocol,
        base_wz_code_path=args.base_wz_code_path,
    ).run()


if __name__ == "__main__":
    main()
