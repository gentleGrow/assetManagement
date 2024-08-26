import asyncio
import os
import threading
import time

import websocket
from dotenv import find_dotenv, load_dotenv

from app.data.polygon.source.service import on_close, on_error, on_message_sync, on_open

load_dotenv(find_dotenv())

POLYGON_WS_URL = os.getenv("POLYGON_WS_URL")


def start_websocket(loop):
    asyncio.set_event_loop(loop)

    while True:
        ws = websocket.WebSocketApp(
            POLYGON_WS_URL,
            on_message=lambda ws, msg: on_message_sync(ws, msg, loop),
            on_error=on_error,
            on_close=on_close,
        )
        ws.on_open = on_open
        ws.run_forever()

        time.sleep(5)


def main():
    loop = asyncio.get_event_loop()
    websocket_thread = threading.Thread(target=start_websocket, args=(loop,))
    websocket_thread.start()

    loop.run_forever()


if __name__ == "__main__":
    main()
