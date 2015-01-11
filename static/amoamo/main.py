# from urllib.parse import urljoin
# from browser import document as doc
from browser import window

from amoamo.websocket import WebSocket
from amoamo.game import Game


GAME = Game()
window.GAME = GAME

ws_addr = "ws://" + window.location.host + "/websocket"
window.WS = WebSocket(
    ws_addr,
    on_open=GAME.open,
    on_message=GAME.process_msg,
    on_close=GAME.close,
)
