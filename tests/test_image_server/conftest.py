import pytest

from src.ImageServer.server.config import Config


@pytest.fixture
def config_for_test():
    return Config(
        wcr_server_host="localhost",
        wcr_server_protocol="https",
        wcr_server_port="7209",
        wcr_caller_retry_num=1,
        wcr_caller_timeout=2,
        wcr_caller_backoff=0.1,
        base_wz_code_path="",
    )
