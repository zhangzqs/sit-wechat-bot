from .config import WcferryAgentConfig
from .wcferry_sdk_loader import WcferrySDKLoader
import time
from common.logger import init_logger
from common.config import load_config_from_args
import logging


def main():
    cfg = load_config_from_args(WcferryAgentConfig)
    init_logger(cfg.logger, logging.getLogger())
    logging.info("Agent准备启动!")
    with WcferrySDKLoader(
        sdk_path=cfg.wcferry.sdk_path,
        debug=cfg.wcferry.debug,
        port=cfg.wcferry.port,
    ) as _:
        loop_forever = True
        while loop_forever:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                loop_forever = False


if __name__ == "__main__":
    main()
