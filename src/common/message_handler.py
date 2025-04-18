from typing import Optional, Dict, Any, Callable, List
from abc import abstractmethod, ABCMeta
from dataclasses import dataclass


@dataclass
class Message:
    is_group: bool  # 是否是群消息
    room_id: Optional[str]  # 群ID
    sender_id: str  # 发送人ID
    content: str  # 文本消息


HandlerFunc = Callable[["Context"], None]


class Context:
    def __init__(
        self,
        receive_message: Message,
    ):
        self._store: Dict[str, Any] = {}
        self._request = receive_message
        self._response: Optional[Message] = None
        self._handlers: List[HandlerFunc] = []
        self._index: int = 0

    def set(self, key: str, value: Any):
        self._store[key] = value

    def get(self, key: str) -> Any:
        return self._store.get(key)

    def get_request(self) -> Message:
        "获取接收到的消息"
        return self._request

    def set_response(self, msg: Message):
        self._response = msg

    def get_response(self):
        return self._response

    def abort(self):
        """中止后续中间件和处理器执行"""
        self._index = len(self._handlers)

    def next(self):
        self._index += 1
        if self._index < len(self._handlers):
            self._handlers[self._index](self)


class Engine:
    # 使用全局中间件
    def use(self, middleware: List[HandlerFunc]):
        pass

    # 执行函数
    def handle(self, handler: HandlerFunc):
        pass
    
    

    def execute(self, message: Message):
        pass
