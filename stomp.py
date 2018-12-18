# Library to allow STOMP communication over Websockets
BYTE = {
    'LF': '\x0A',
    'NULL': '\x00'
}

VERSIONS = '1.0,1.1'

class Stomp:
    def __init__(self, ws, host, callbacks):
        self.ws = ws
        self.host = host

        Listener(ws, callbacks, self)

    def marshall(self, command, headers):
        lines = []
        lines.append(command + BYTE['LF'])

        for key in headers:
            lines.append(key + ":" + headers[key] + BYTE['LF'])

        return ''.join(lines) + BYTE['LF'] + BYTE['NULL']

    def transmit(self, command, headers):
        out = self.marshall(command, headers)
        print ">>> " + out
        self.ws.send(out)

    def connect(self):
        headers = {}

        headers['host'] = self.host
        headers['accept-version'] = VERSIONS
        headers['heart-beat'] = '10000,10000'

        self.transmit('CONNECT', headers)

    def subscribe(self, destination):
        headers = {}

        headers['id'] = 'sub-0'
        headers['ack'] = 'client'
        headers['destination'] = destination

        self.transmit('SUBSCRIBE', headers)

    def getCommand(self, data):
        command = data.split(BYTE['LF'])[0]
        return command


class Listener:
    def __init__(self, ws, callbacks, stomp):
        self.stomp = stomp

        #registering callbacks
        self.callbacks = callbacks

        ws.on_open = self.on_open
        ws.on_message = self.on_message
        ws.on_error = self.on_error
        ws.on_close = self.on_close

        ws.run_forever()

    def on_message(self, ws, message):
        print "<<< " + message

        command = self.stomp.getCommand(message)

        if command.strip() == "CONNECTED":
            callback = self.callbacks['CONNECTED']
            callback(self.stomp)

    def on_error(self, ws, error):
        print error

    def on_close(self, ws):
        print "### closed ###"

    def on_open(self, ws):
        # if method to be executed on init is defined
        if self.callbacks['INIT']:
            callback = self.callbacks['INIT']
            callback(self.stomp)

        else:
            self.stomp.connect()
