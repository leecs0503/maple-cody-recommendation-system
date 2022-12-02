class Config:
    def __init__(
        self,
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
