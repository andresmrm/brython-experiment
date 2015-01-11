# from urllib.parse import urljoin
# from browser import document as doc
from browser import window

from amoamo.websocket import WebSocket
from amoamo.game import Game


window.console.log("1")
GAME = Game()
window.console.log("2")

ws_addr = "ws://" + window.location.host + "/websocket"
WS = WebSocket(ws_addr, GAME.process_msg)
