import websocket
from stomp import Stomp

def connect(stomp):
    stomp.connect()

def subscribe(stomp):
    endpoint = '/endpoint'
    stomp.subscribe(endpoint)

if __name__ == "__main__":
    # websocket.enableTrace(True)

    ws = websocket.WebSocketApp("wss://host.com/websocket") # the /websocket endpoint needs to be added if using a SockJS server

    # register callbacks based on type of response
    # e.x: if response from the server is a CONNECTED frame, execute subscribe function
    # if INIT is not provided, default action will be connect() (implement)

    callbacks = {
        'INIT' : connect,
        'CONNECTED' : subscribe
    }

    Stomp(ws, config.HOST, callbacks)
    
