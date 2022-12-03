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
        avatar_server_host: str,
        avatar_server_protocol: str,
        avatar_server_port: int,
        avatar_caller_retry_num: int,
        avatar_caller_timeout: float,
        avatar_caller_backoff: float,
        inference_server_host: str,
        inference_server_protocol: str,
        inference_server_port: int,
        inference_caller_retry_num: int,
        inference_caller_timeout: float,
        inference_caller_backoff: float,
    ) -> None:
        self.wcr_server_host = wcr_server_host
        self.wcr_server_port = wcr_server_port
        self.wcr_server_protocol = wcr_server_protocol
        self.base_wz_code_path = base_wz_code_path
        self.wcr_caller_retry_num = wcr_caller_retry_num
        self.wcr_caller_timeout = wcr_caller_timeout
        self.wcr_caller_backoff = wcr_caller_backoff
        self.avatar_server_host = avatar_server_host
        self.avatar_server_protocol = avatar_server_protocol
        self.avatar_server_port = avatar_server_port
        self.avatar_caller_retry_num = avatar_caller_retry_num
        self.avatar_caller_timeout = avatar_caller_timeout
        self.avatar_caller_backoff = avatar_caller_backoff
        self.inference_server_host = inference_server_host
        self.inference_server_protocol = inference_server_protocol
        self.inference_server_port = inference_server_port
        self.inference_caller_retry_num = inference_caller_retry_num
        self.inference_caller_timeout = inference_caller_timeout
        self.inference_caller_backoff = inference_caller_backoff

    def to_json(self) -> dict:
        return {
            "wcr_server_host": self.wcr_server_host,
            "wcr_server_port": self.wcr_server_port,
            "wcr_server_protocol": self.wcr_server_protocol,
            "base_wz_code_path": self.base_wz_code_path,
            "wcr_caller_retry_num": self.wcr_caller_retry_num,
            "wcr_caller_timeout": self.wcr_caller_timeout,
            "wcr_caller_backoff": self.wcr_caller_backoff,
            "avatar_server_host": self.avatar_server_host,
            "avatar_server_protocol": self.avatar_server_protocol,
            "avatar_server_port": self.avatar_server_port,
            "avatar_caller_retry_num": self.avatar_caller_retry_num,
            "avatar_caller_timeout": self.avatar_caller_timeout,
            "avatar_caller_backoff": self.avatar_caller_backoff,
            "inference_server_host": self.inference_server_host,
            "inference_server_protocal": self.inference_server_protocol,
            "inference_server_port": self.inference_server_port,
            "inference_caller_retry_num": self.inference_caller_retry_num,
            "inference_caller_timeout": self.inference_caller_timeout,
            "inference_caller_backoff": self.inference_caller_backoff,
        }
