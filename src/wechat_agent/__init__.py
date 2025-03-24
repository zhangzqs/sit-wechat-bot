from .config import WeChatAgentConfig, load_yaml_config
from .wcferry_sdk_loader import WcferrySDKLoader
import argparse
import signal
import time

def main():
    parser = argparse.ArgumentParser(description="Load configuration from a YAML file.")
    parser.add_argument("--config", type=str, required=True, help="Path to the YAML configuration file")
    args = parser.parse_args()

    # 加载配置文件
    cfg = load_yaml_config(args.config)

    with WcferrySDKLoader(
        sdk_path=cfg.wcferry.sdk_path,
        debug=cfg.wcferry.debug,
        port=cfg.wcferry.port,
    ) as _:
        print("Load SDK Successful")
        loop_forever = True
        while loop_forever:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                loop_forever = False
                
if __name__ == "__main__":
    main()