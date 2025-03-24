from wcferry import Wcf, WxMsg
from queue import Empty


def main():
    w = Wcf(
        host="localhost",
        port=10086,
        debug=True,
    )
    w.enable_receiving_msg()
    while w.is_receiving_msg():
        try:
            msg = w.get_msg()
            print(msg)
        except Empty:
            continue
        except Exception as e:
            print(f"processing message error {e}")


if __name__ == "__main__":
    main()
