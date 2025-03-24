from pydantic import BaseModel
from typing import Optional
from common.logger import LoggerConfig


class WcferryConfig(BaseModel):
    sdk_path: str
    debug: Optional[bool] = False
    port: Optional[int] = 10086


class WcferryAgentConfig(BaseModel):
    logger: LoggerConfig
    wcferry: WcferryConfig
