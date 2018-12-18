# StompWS
A Python library that enables simple [STOMP](https://stomp.github.io/) communication over WebSockets. Works on the client-side with any STOMP server.

## Need
WebSockets have grown into an elementary tool that allow applications to exchange data bi-directionally over the web. In most cases, browsers communicate to webservers in interactive websites. However, there might be cases where services communicate with each other in real time.  

For such use-cases, StompWS enables applications written in Python to communicate with STOMP based webservices through a simple API.

## API
The application is callback driven.

STOMP is a frame based protocol. A frame consists of a command, a set of optional headers and an optional body. A STOMP client is a user-agent which can act in two (possibly simultaneous) modes:
- as a producer, sending messages to a destination on the server via a `SEND` frame
- as a consumer, sending a `SUBSCRIBE` frame for a given destination and receiving messages from the server as `MESSAGE` frames.

To use the library, a dictionary of callbacks needs to be constructed and passed to the `Stomp()` constructor.  
The dictionary is a key-value pair of strings mapped to functions. The key is the type of frame received from the webserver and the function is the callback that needs to be executed to act upon the response.

```
# register callbacks based on type of response
# e.x: if response from the server is a CONNECTED frame, execute subscribe function

callbacks = {
    'INIT' : connect_callback,
    'CONNECTED' : subscribe_callback
}
```


The callback signature itself looks like this:
```
def connect_callback(stomp):
  pass
```

The `stomp` argument is a reference to the object that offers the core library APIs that interact with the webserver.
- connect()
- subscribe()
- send()

