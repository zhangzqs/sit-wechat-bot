from pydantic import BaseModel
from wcferry import Wcf


class WcfClientConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 10086


class WcfClient(Wcf):
    def __init__(self, cfg: WcfClientConfig):
        super().__init__(
            host=cfg.host,
            port=cfg.port,
        )
