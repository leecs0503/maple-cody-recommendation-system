import pytest
import os

from src.AvatarServer.server.config import Config


@pytest.fixture
def config_for_test():
    cwd = os.path.dirname(os.path.realpath(__file__))
    return Config(
        wcr_server_host="localhost",
        wcr_server_protocol="https",
        wcr_server_port="7209",
        wcr_caller_retry_num=1,
        wcr_caller_timeout=2,
        wcr_caller_backoff=0.1,
        base_wz_code_path=os.path.join(cwd, 'test_base_wz.json'),
    )
