import argparse
import ctypes
import os
import signal
from http.server import HTTPServer, SimpleHTTPRequestHandler


class Wcf:
    DEFAULT_SDK_PATH = "binary/sdk.dll"

    def __init__(self):
        self.sdk = None

    def load(self, debug: bool = False, port: int = 10086):
        if not os.path.exists(self.DEFAULT_SDK_PATH):
            print("SDK 不存在！")

        self.sdk = ctypes.cdll.LoadLibrary(self.DEFAULT_SDK_PATH)
        # 初始化 SDK. 出现错误时，SDK 会调用 MessageBox 弹窗提示错误信息并返回 -1
        if self.sdk.WxInitSDK(debug, port) != 0:
            exit(-1)

    def cleanup(self):
        if self.sdk.WxDestroySDK() != 0:
            print("退出失败！")


class UploadHandler(SimpleHTTPRequestHandler):
    def do_PUT(self):
        # 获取路径并转换为本地路径
        path = self.translate_path(self.path)

        # 检查路径是否为目录（不允许覆盖目录）
        if os.path.isdir(path):
            self.send_error(405, "Method Not Allowed")
            return

        # 确保父目录存在
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # 读取请求内容
        content_length = int(self.headers["Content-Length"])
        content = self.rfile.read(content_length)

        # 写入文件
        with open(path, "wb") as f:
            f.write(content)

        # 发送响应
        self.send_response(201)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"File uploaded successfully")

    def do_POST(self):
        # 让 POST 和 PUT 使用相同逻辑
        self.do_PUT()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wcf SDK Loader")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "--wcf-port", type=int, default=10086, help="Port number for WCF to use"
    )
    parser.add_argument(
        "--web-port", type=int, default=8000, help="Port number for HTTP server to use"
    )
    args = parser.parse_args()

    wcf = Wcf()
    wcf.load(debug=args.debug, port=args.wcf_port)
    print("WCF SDK loaded.")

    def signal_handler(_sig, _frame):
        print("Ctrl+C pressed. Exit.")
        wcf.cleanup()
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    print("Listening on port", args.web_port)
    server_address = ("", args.web_port)
    httpd = HTTPServer(server_address, UploadHandler)
    httpd.serve_forever()
