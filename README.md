# SIMP_Client

This repository contains the code for a simple chat application called "SIMP". The code allows a user to start a chat session with a server, and exchange messages with the server.

## Requirements

-   Python 3.x
-   `message` module from [message.py](https://github.com/OpenAI/message)

## Functionality

The code contains two main functions:

-   `startChatting(s,host,port)` - starts a chat session with a server
-   `threeWayHandshake(s,host,port)` - performs a three-way handshake to establish a connection with a server

### startChatting(s,host,port)

This function starts a chat session with a server. It takes in the following parameters:

-   `s`: a socket object representing the connection to the server
-   `host`: a string representing the host IP address
-   `port`: an integer representing the port number of the server

### threeWayHandshake(s,host,port)

This function performs a three-way handshake to establish a connection with a server. It takes in the following parameters:

-   `s`: a socket object representing the connection to the server
-   `host`: a string representing the host IP address
-   `port`: an integer representing the port number of the server

# Chat Room Server

This is a Python implementation of a chat room server using the User Datagram Protocol (UDP). The server can accept multiple clients and facilitates the exchange of messages between them. The code includes features such as a 3-way handshake and error checking.

## Functionality

-   Starts a chat session with a user by allowing the user to enter a username and initializing the sequence numbers for both the user and the server
-   Enters an infinite loop to facilitate the exchange of messages until either the user or the server decides to quit
-   Initializes a server socket and waits for incoming SYN control frames from clients
-   If the chat request is accepted, the server will send a SYN+ACK control frame and wait for an ACK response from the client
-   If the connection is successful, the server will exchange messages with the client
-   The server will continuously wait for incoming messages from clients

## Usage

1.  Run `python3 server.py` in terminal to start the server
2.  A client can connect to the server by running the client code
3.  The server will prompt the user to accept or deny the connection request
4.  If the connection request is accepted, the server will exchange messages with the client until either the user or the server decides to quit

## Note

-   The `startChatting` and `waitAndReceive` functions should be used together in the `server.py` file to create the full functionality of the server.
- 
# Message
## Description

This code consists of two functions that are used to create and check a bytearray header for a messaging system. The first function, `createHeader()`, takes five input parameters and returns a bytearray header. The second function, `checkHeader()`, takes a bytearray header as input and returns the separated components of the header, including message type, operation, sequence number, username, message length, and message.

## Usage

`import string as s` 

### createHeader(type: s,operation: s,sequence_number: int,username: s,message: s)

This function creates a bytearray header with the given parameters.

-   type: Message type, either 'cm' for control message or 'chat' for conversation message.
-   operation: The operation type, including "send message", "error", "SYN", "ACK", "SYN+ACK", "FIN".
-   sequence_number: The sequence number of the message.
-   username: The username of the sender.
-   message: The message to be sent.

### checkHeader(header: bytearray)

This function takes a bytearray header as input and separates its components into message type, operation, sequence number, username, message length, and message. The separated components are returned as a tuple.

## Note

The code assumes a default username `'uname'` if not specified, and a message length of 0 for control messages. The username has a fixed length of 32 bytes, with leading zeros added if the username is shorter.