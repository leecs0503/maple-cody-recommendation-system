class Config:
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
