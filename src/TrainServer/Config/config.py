class Config:
    def __init__(
        self,
        server_host: str,
        server_port: int,
        train_data_path: str,
        model_save_path: str,
        batch_size: int,
        num_workers: int,
    ) -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.train_data_path = train_data_path
        self.model_save_path = model_save_path
        self.batch_size = batch_size
        self.num_workers = num_workers

