import websocket
import time
from threading import Thread

BYTE = {
    'LF': '\x0A',
    'NULL': '\x00'
}

VERSIONS = '1.0,1.1'

class Stomp:
    def __init__(self, host, sockjs=False, wss=True):
        """
        Initialize STOMP communication. This is the high level API that is exposed to clients.

        Args:
            host: Hostname
            sockjs: True if the STOMP server is sockjs
            wss: True if communication is over SSL
        """
        websocket.enableTrace(True)
        ws_host = host if sockjs is False else host + "/websocket"
        protocol = "ws://" if wss is False else "wss://"

        self.url = protocol + ws_host

        self.dispatcher = Dispatcher(self)

    def connect(self):
        """
        Connect to the remote STOMP server
        """
        # set flag to false
        self.connected = False

        # attempt to connect
        self.dispatcher.connect()

        # wait until connected
        while self.connected is False:
            time.sleep(.50)

        return self.connected


class Dispatcher:
    def __init__(self, stomp):
        """
        The Dispatcher handles all network I/O and frame marshalling/unmarshalling
        """
        self.stomp = stomp

        self.ws = websocket.WebSocketApp(self.stomp.url)

        # register websocket callbacks
        self.ws.on_open = self._on_open
        self.ws.on_message = self._on_message
        self.ws.on_error = self._on_error
        self.ws.on_close = self._on_close

        # run event loop on separate thread
        Thread(target=self.ws.run_forever).start()

        self.opened = False

        # wait until connected
        while self.opened is False:
            time.sleep(.50)

    def _on_message(self, ws, message):
        """
        Executed when messages is received on WS
        """
        print("<<< " + message)

        command = self._getCommand(message)

        if command.strip() == "CONNECTED":
            self.stomp.connected = True

    def _on_error(self, ws, error):
        """
        Executed when WS connection errors out
        """
        print(error)

    def _on_close(self, ws):
        """
        Executed when WS connection is closed
        """
        print("### closed ###")

    def _on_open(self, ws):
        """
        Executed when WS connection is opened
        """
        self.opened = True

    def _transmit(self, command, headers):
        """
        Marshalls and transmits the marshalled frame
        """
        # Contruct the frame
        lines = []
        lines.append(command + BYTE['LF'])

        for key in headers:
            lines.append(key + ":" + headers[key] + BYTE['LF'])

        frame = ''.join(lines) + BYTE['LF'] + BYTE['NULL']

        # transmit over ws
        print(">>>" + frame)
        self.ws.send(frame)

    def _getCommand(self, frame):
        """
        Returns frame command

        Args:
            frame: raw frame string
        """
        return frame.split(BYTE['LF'])[0]

    def connect(self):
        """
        Transmit a CONNECT frame
        """
        headers = {}

        headers['host'] = self.stomp.url
        headers['accept-version'] = VERSIONS
        headers['heart-beat'] = '10000,10000'

        self._transmit('CONNECT', headers)
