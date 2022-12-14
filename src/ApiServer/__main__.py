from .server.app_runner import AppRunner
from .server.config import Config
import argparse


def main():
    parser = argparse.ArgumentParser(description="api server server")

    parser.add_argument("--logging-path", type=str, help="api server loggin path", default='logs/api_server_log.log')

    parser.add_argument("--wcr-server-host", type=str, help="wcr server host", default="localhost")
    parser.add_argument("--wcr-server-port", type=int, help="wcr server port", default=7209)
    parser.add_argument("--wcr-server-protocol", type=str, help="wcr server protocol", default="https")
    parser.add_argument("--base-wz-code-path", type=str, help="base", default="./data/base_wz.json")
    parser.add_argument("--wcr-caller-retry-num", type=int, help="wcr server retry num", default=-1)
    parser.add_argument("--wcr-caller-timeout", type=float, help="wcr server caller timeout", default=2.5)
    parser.add_argument("--wcr-caller-backoff", type=float, help="wcr server caller backoff", default=1)

    parser.add_argument("--avatar-server-host", type=str, help="avatar server host", default="0.0.0.0")
    parser.add_argument("--avatar-server-protocol", type=str, help="avatar server protocol", default="http")
    parser.add_argument("--avatar-server-port", type=int, help="avatar server port", default=8080)
    parser.add_argument("--avatar-caller-retry-num", type=int, help="avatar server retry num", default=-1)
    parser.add_argument("--avatar-caller-timeout", type=float, help="avatar server caller timeout", default=2.5)
    parser.add_argument("--avatar-caller-backoff", type=float, help="avatar server caller backoff", default=1)
    parser.add_argument("--inference-server-host", type=str, help="inference server host", default="0.0.0.0")
    parser.add_argument("--inference-server-protocol", type=str, help="inference server protocol", default="http")
    parser.add_argument("--inference-server-port", type=int, help="inference server port", default=9000)
    parser.add_argument("--inference-caller-retry-num", type=int, help="inference server retry num", default=5)
    parser.add_argument("--inference-caller-timeout", type=float, help="inference server caller timeout", default=2.5)
    parser.add_argument("--inference-caller-backoff", type=float, help="inference server caller backoff", default=1)

    args = parser.parse_args()

    config = Config(
        wcr_server_host=args.wcr_server_host,
        wcr_server_port=args.wcr_server_port,
        wcr_server_protocol=args.wcr_server_protocol,
        base_wz_code_path=args.base_wz_code_path,
        wcr_caller_retry_num=args.wcr_caller_retry_num,
        wcr_caller_timeout=args.wcr_caller_timeout,
        wcr_caller_backoff=args.wcr_caller_backoff,
        avatar_server_host=args.avatar_server_host,
        avatar_server_protocol=args.avatar_server_protocol,
        avatar_server_port=args.avatar_server_port,
        avatar_caller_retry_num=args.avatar_caller_retry_num,
        avatar_caller_timeout=args.avatar_caller_timeout,
        avatar_caller_backoff=args.avatar_caller_backoff,
        inference_server_host=args.inference_server_host,
        inference_server_protocol=args.inference_server_protocol,
        inference_server_port=args.inference_server_port,
        inference_caller_retry_num=args.inference_caller_retry_num,
        inference_caller_timeout=args.inference_caller_timeout,
        inference_caller_backoff=args.inference_caller_backoff,
    )

    AppRunner(
        config=config,
        logging_path=args.logging_path,
    ).run()


if __name__ == "__main__":
    main()
