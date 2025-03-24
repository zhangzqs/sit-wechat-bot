import os
import ctypes
from typing import Optional, NoReturn


class WcferryError(Exception):
    """SDK相关操作的基础异常类"""

    pass


class WcferrySDKLoader:
    def __init__(self, sdk_path: str, debug: bool, port: int):
        """
        初始化WCF SDK控制器
        :param sdk_path: 可选的自定义SDK路径
        """
        self._sdk_path = sdk_path
        self._sdk = None  # type: Optional[ctypes.CDLL]
        self._debug = debug
        self._port = port

        # 提前验证路径合法性
        if not os.path.isfile(self._sdk_path):
            raise FileNotFoundError(f"SDK文件不存在于: {self._sdk_path}")

        try:
            self._sdk = ctypes.CDLL(self._sdk_path)
        except OSError as e:
            raise WcferryError(f"加载SDK失败: {e}") from e

        # 配置函数原型
        self._sdk.WxInitSDK.argtypes = [ctypes.c_bool, ctypes.c_int]
        self._sdk.WxInitSDK.restype = ctypes.c_int

    def __enter__(self):
        if self._sdk.WxInitSDK(self._debug, self._port) != 0:
            raise WcferryError("SDK初始化失败，请检查调试模式和端口配置")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        清理SDK资源
        :return: 是否成功清理
        """
        if not self._sdk:
            return True

        # 配置函数原型
        self._sdk.WxDestroySDK.argtypes = []
        self._sdk.WxDestroySDK.restype = ctypes.c_int

        result = self._sdk.WxDestroySDK()
        self._sdk = None
        if result != 0:
            print("警告：SDK资源释放异常")

    @property
    def sdk(self) -> ctypes.CDLL:
        """获取已加载的SDK实例"""
        if self._sdk is None:
            raise WcferryError("SDK尚未初始化")
        return self._sdk
