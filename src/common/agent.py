from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class MessageType(str, Enum):
    TEXT = "TEXT"
    "纯文本消息"


class WechatMessage(BaseModel):
    is_self: bool
    "这是自己发的消息"

    is_group: bool
    "这是一个群消息"

    is_at: bool
    "是否被别人at了"

    time: datetime
    "消息产生时间"

    sender_id: str
    "消息发送人的ID"

    content: str
    "消息的具体内容"

    type: MessageType
    "消息类型"