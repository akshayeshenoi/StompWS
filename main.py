from stomp_ws import Stomp
import time

def do_thing_a(msg):
    print("MESSAGE: " + msg)

if __name__ == "__main__":
    stomp = Stomp("127.0.0.1:8080/gs-guide-websocket", sockjs=True, wss=False)
    stomp.connect()
    stomp.subscribe("/topic/greetings", do_thing_a)
    time.sleep(2)
    stomp.send("/app/hello", '{"name":"akshaye"}')
