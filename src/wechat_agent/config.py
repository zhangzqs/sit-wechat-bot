from pydantic import BaseModel
from typing import Optional
import yaml

class WcferryConfig(BaseModel):
    sdk_path: str
    debug: Optional[bool] = False
    port: Optional[int] = 10086


class WeChatAgentConfig(BaseModel):
    wcferry: WcferryConfig
    
def load_yaml_config(config_file: str) -> WeChatAgentConfig:
    with open(config_file, 'r') as f:
        config_data = yaml.safe_load(f)
    return WeChatAgentConfig(**config_data)