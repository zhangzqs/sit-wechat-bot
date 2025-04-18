from pydantic import BaseModel
from wcferry import Wcf
from typing import Dict


class WcfClientConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 10086


class WcfClient(Wcf):
    def __init__(self, cfg: WcfClientConfig):
        super().__init__(
            host=cfg.host,
            port=cfg.port,
        )


from functools import lru_cache


class WcfClientEx:
    def __init__(self, wcf: Wcf):
        self._wcf = wcf

    @lru_cache(maxsize=128, typed=True)
    def query_room_member(self, room_id: str) -> Dict[str, str]:
        return self._wcf.get_chatroom_members(roomid=room_id)
