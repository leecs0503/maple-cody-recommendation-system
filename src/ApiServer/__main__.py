from .server.app_runner import AppRunner
import argparse


def main():
    parser = argparse.ArgumentParser(description="api server server")

    parser.add_argument("--wcr-server-host", type=str, help="wcr server host", default="0.0.0.0")
    parser.add_argument("--wcr-server-port", type=int, help="wcr server port", default=7209)
    parser.add_argument("--wcr-server-protocol", type=str, help="wcr server protocol", default="https")
    parser.add_argument("--base-wz-code-path", type=str, help="base", default="./data/base_wz.json")
    parser.add_argument("--wcr-caller-retry-num", type=int, help="wcr server retry num", default=-1)
    parser.add_argument("--wcr-caller-timeout", type=float, help="wcr server caller timeout", default=2.5)
    parser.add_argument("--wcr-caller-backoff", type=float, help="wcr server caller backoff", default=1)
    parser.add_argument("--logging-path", type=str, help="api server loggin path", default='logs/app_runner_log.log')

    args = parser.parse_args()

    AppRunner(
        wcr_server_host=args.wcr_server_host,
        wcr_server_port=args.wcr_server_port,
        wcr_server_protocol=args.wcr_server_protocol,
        base_wz_code_path=args.base_wz_code_path,
        wcr_caller_retry_num=args.wcr_caller_retry_num,
        wcr_caller_timeout=args.wcr_caller_timeout,
        wcr_caller_backoff=args.wcr_caller_backoff,
        logging_path=args.logging_path,
    ).run()


if __name__ == "__main__":
    main()
