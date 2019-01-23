# StompWS
A Python library that enables simple [STOMP](https://stomp.github.io/) communication over WebSockets. Works on the client-side with any STOMP server.

## Need
WebSockets have grown into an elementary tool that allow applications to exchange data bi-directionally over the web. In most cases, browsers communicate to webservers in interactive websites. However, there might be cases where services communicate with each other in real time.  

For such use-cases, StompWS enables applications written in Python to communicate with STOMP based webservices through a simple API.

## API
STOMP is a frame based protocol. A frame consists of a command, a set of optional headers and an optional body. A STOMP client is a user-agent which can act in two (possibly simultaneous) modes:
- as a producer, sending messages to a destination on the server via a `SEND` frame
- as a consumer, sending a `SUBSCRIBE` frame for a given destination and receiving messages from the server as `MESSAGE` frames.

The API exposed by the library abstracts away most of this.

We instantiate a Stomp object to obtain a reference to the core API:
```py
stomp = Stomp("hostname/endpoint", sockjs=True, wss=False)
```

Below are the APIs that are exposed by the object

### .connect()
Attempts to connect to the server using the information provided while instantiating.

### .send(destination, message)
Sends `message` to `destination` on the server. Refer your STOMP server documentation to find out what that is.

### .subscribe(destination, callback)
Subscribes to a `destination` (think topic) on the STOMP server to receive messages that are published on it.

The `callback` argument must be a function that accepts a `msg` argument:
```py
# define the callback function that should act upon the message
def do_something(msg):
    print(msg)

# subscribe to a destination and pass the callback function
stomp.subscribe('/some-destination', do_something)
```

### .unsubscribe(destination) [to be implemented]
### .disconnect() [to be implemented]


## Todo
- logging
- better message passing bw Stomp and Dispatcher (reduce spaghetti code)
- add trace flag