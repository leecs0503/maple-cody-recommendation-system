import pytest
import os

from src.AvatarServer.server.config import Config

class ConfigForTest:
    def __init__(
        self,
        wcr_server_host: str,
        wcr_server_port: int,
        wcr_server_protocol: str,
        base_wz_code_path: str,
        wcr_caller_retry_num: int,
        wcr_caller_timeout: float,
        wcr_caller_backoff: float,
    ) -> None:
        self.wcr_server_host = wcr_server_host
        self.wcr_server_port = wcr_server_port
        self.wcr_server_protocol = wcr_server_protocol
        self.base_wz_code_path = base_wz_code_path
        self.wcr_caller_retry_num = wcr_caller_retry_num
        self.wcr_caller_timeout = wcr_caller_timeout
        self.wcr_caller_backoff = wcr_caller_backoff

    def to_json(self) -> dict:
        return {
            "wcr_server_host": self.wcr_server_host,
            "wcr_server_port": self.wcr_server_port,
            "wcr_server_protocol": self.wcr_server_protocol,
            "base_wz_code_path": self.base_wz_code_path,
            "wcr_caller_retry_num": self.wcr_caller_retry_num,
            "wcr_caller_timeout": self.wcr_caller_timeout,
            "wcr_caller_backoff": self.wcr_caller_backoff,
        }


@pytest.fixture
def config_for_test():
    cwd = os.path.dirname(os.path.realpath(__file__))
    return ConfigForTest(
        wcr_server_host="localhost",
        wcr_server_protocol="https",
        wcr_server_port="7209",
        wcr_caller_retry_num=1,
        wcr_caller_timeout=2,
        wcr_caller_backoff=0.1,
        base_wz_code_path=os.path.join(cwd, "test_base_wz.json"),
    )
