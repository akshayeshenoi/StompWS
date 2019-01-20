from stomp_ws import Stomp

if __name__ == "__main__":
    stomp = Stomp("127.0.0.1:8080/gs-guide-websocket", sockjs=True, wss=False)
    stomp.connect()
