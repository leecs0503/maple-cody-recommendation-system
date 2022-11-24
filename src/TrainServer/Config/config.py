class Config:
    def __init__(
        self,
        server_host: str,
        server_port: int,
        model_path: str,
        batch_size: int,
        num_workers: int,
        tensorboard_path: str,
    ) -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.model_path = model_path
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.tensorboard_path = tensorboard_path

