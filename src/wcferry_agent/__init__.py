from pydantic import BaseModel
from wcferry import Wcf, WxMsg
from common.config import load_config_from_args
from common.agent import WechatMessage
import logging
from queue import Empty
import httpx
import threading
from typing import Optional
import uvicorn
from fastapi import FastAPI, Depends
from datetime import datetime

class WcferryClientConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 10086


class WcferryAgentConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 18090
    wcferry: WcferryClientConfig
    http_callback_url: Optional[str] = None


def convert_message(msg: WxMsg) -> WechatMessage:
    return WechatMessage(
        is_self=msg.from_self(),
        is_group=msg.from_group(),
    )


def message_callback(wcf: Wcf, callback_url: str):
    assert wcf.enable_receiving_msg()

    while wcf._is_receiving_msg:
        try:
            msg = convert_message(wcf.get_msg())
            httpx.post(
                url=callback_url,
                json=msg.model_dump(),
            )
        except Empty:
            continue
        except Exception as e:
            logging.error(f"receive message error: {e}")


app = FastAPI()


def get_wcf_client():
    cli: Wcf = app.state.wcf_client
    try:
        yield cli
    finally:
        cli.cleanup()

class GetMessageCountInput(BaseModel):
    begin_time: datetime
    "查询的起始时间"
    
    end_time: datetime
    "查询的终止时间"
    
    talker_id: str
    "消息会话的ID，可以是群消息，也可以是私聊消息"

class GetMessageCountOutput(BaseModel):
    count: int # 返回消息统计数量

@app.post(
    path="/message_count",
)
def get_message_count(
    wcf: Wcf = Depends(get_wcf_client),
):
    pass


def main():
    cfg = load_config_from_args(WcferryAgentConfig)
    logging.info('Agent准备启动')
    wcf = Wcf(cfg.wcferry.host, cfg.wcferry.port)
    app.state.wcf_client = wcf

    if cfg.http_callback_url is None:
        threading.Thread(
            name='message_callback',
            target=message_callback,
            args=[wcf, cfg.http_callback_url],
        ).start()

    uvicorn.run(
        app=app,
        host=cfg.host,
        port=cfg.port,
    )
