class Config:
    def __init__(
        self,
        server_host: str,
        server_port: int,
        train_data_path: str,
        model_save_path: str,
    ) -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.train_data_path = train_data_path
        self.model_save_path = model_save_path

