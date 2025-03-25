from pydantic import BaseModel
from common.wcf import WcfClientConfig


class WcferryMessageHandlerConfig(BaseModel):
    wcferry_client: WcfClientConfig
