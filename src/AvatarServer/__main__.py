import argparse

from .server.app_runner import AppRunner


def main():
    parser = argparse.ArgumentParser(description="image server")

    parser.add_argument("--wcr-server-host", type=str, help="wcr server host", default="localhost")
    parser.add_argument("--wcr-server-port", type=int, help="wcr server host", default=7209)
    parser.add_argument("--wcr-server-protocol", type=str, help="wcr server host", default="https")
    parser.add_argument("--base-wz-code-path", type=str, help="base", default="./src/AvatarServer/base_wz_code.json")
    parser.add_argument("--wcr-caller-retry-num", type=int, help="wcr server host", default=-1)
    parser.add_argument("--wcr-caller-timeout", type=float, help="wcr server host", default=2.5)
    parser.add_argument("--wcr-caller-backoff", type=float, help="wcr server host", default=1)

    args = parser.parse_args()

    AppRunner(
        wcr_server_host=args.wcr_server_host,
        wcr_server_port=args.wcr_server_port,
        wcr_server_protocol=args.wcr_server_protocol,
        base_wz_code_path=args.base_wz_code_path,
        wcr_caller_retry_num=args.wcr_caller_retry_num,
        wcr_caller_timeout=args.wcr_caller_timeout,
        wcr_caller_backoff=args.wcr_caller_backoff,
    ).run()


if __name__ == "__main__":
    main()
