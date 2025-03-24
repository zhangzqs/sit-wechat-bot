from wcferry import Wcf, WxMsg
from queue import Empty
from pprint import pprint
from common.config import load_config_from_args
from common.wcf import WcfClient
from .config import WcferryMessageHandlerConfig


def main():
    cfg = load_config_from_args(WcferryMessageHandlerConfig)
    cli = WcfClient(cfg.wcferry_client)

    pprint(cli.get_contacts())

    assert cli.enable_receiving_msg()

    while cli.is_receiving_msg():
        try:
            msg = cli.get_msg()
            print(msg)
        except Empty:
            continue
        except Exception as e:
            print(f"processing message error {e}")


if __name__ == "__main__":
    main()
