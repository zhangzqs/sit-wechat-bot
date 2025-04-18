from pydantic import BaseModel
from common.wcf import WcfClientConfig
from common.logger import LoggerConfig
from typing import List



class MessageHandler(BaseModel):
    chains: List


class WcferryMessageHandlerConfig(BaseModel):
    logger: LoggerConfig
    wcferry_client: WcfClientConfig
    handlers: List[MessageHandler]  # 收到一份消息后会复制n份发送到列表中的每个Handler
