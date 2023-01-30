import socket
import time
from message import createHeader, checkHeader

def startChatting(s, host, port):
    """
    This function starts the chat session by allowing the user to enter a username and initializing the sequence numbers
    for both the user and the server.
    It then enters an infinite loop to facilitate the exchange of messages until either the user or the server decides
    to quit.
    """
    username = 'server'
    seq_server = 100            # initialize the sequence number for the server
    seq_user = 0                # initialize the sequence number for the user
    while True:
        # receive data from the host
        response, host_from = s.recvfrom(1024)
        print(response[2],' vs ',seq_user)

        # wait for the correct sequence number
        while response[2] != seq_user:
            #Message is rejected if the seq doesn't match.
            response, host_from = s.recvfrom(1024)

        # print the server's name and message
        print(checkHeader(response)[3], ': ', checkHeader(response)[5])
        #The createHeader function send an ACK control frame.
        x = createHeader('cm', 'ACK', response[2], username, '')
        seq_user = response[2]
        time.sleep(7) #changes to delay ACKs
        # An ACK control frame is sent back by the server.
        s.sendto(x, host_from)

        # prompt the user to enter their message
        message = input(f'{username}: ')

        # If an ACK control frame is not received after waiting for five seconds, this while loop continues to
        # broadcast chat messages.
        while True:
            y = createHeader('chat', 'send message', seq_server, username, message)
            s.sendto(y,host_from)
            s.settimeout(5)
            try:
                response, host_from = s.recvfrom(1024)
                print(response[2],' vs ',seq_server)
                # wait for the correct sequence number
                while response[2] != seq_server:
                    print('2: discard frame with seq numb =', response[2])
                    response, host_from = s.recvfrom(1024)
            except socket.timeout:
                print('STO: resend' , y , 'with seq = ', y[2])
                # if the timeout is reached, continue to the next iteration of the loop
                continue
            break
        # set the timeout to None to allow for messages to be sent after 5 seconds
        s.settimeout(None)
        #The number 1 is added to the sequence numbers.
        seq_server = seq_server + 1
        seq_user = seq_user + 1
        

    return 0


def waitAndReceive(s,host,port):
    """
    This function initializes a server socket and waits for incoming SYN control frames from clients.
    When a SYN is received, the server can choose to accept or deny the connection request.
    If accepted, the server will send a SYN+ACK control frame and wait for an ACK response from the client,
    indicating a successful 3-way handshake. The function then returns a value of 1 to indicate success.
    """
    s.bind((host,port))      # bind the socket to the specified host and port
    while True:
        #A SYN frame is received by the server from the user.
        data, host_from = s.recvfrom(1024)
        # get the sequence number from the received data
        seq = data[2]
        #Utilizing the checkHeader function, verifying the received data and proceed.
        if checkHeader(data)[1] == 2: #operation SYN = 2
            # The chat request may be approved or denied by the server.
            answer = input(f'Accept connection request from {host_from}? Press [y] to continue: ')
            if answer == 'y': # if the server accepts the chat request
                # create and send a SYN+ACK control frame
                p = createHeader('cm', 'SYN+ACK', seq, 'name', '')
                # control frame is sent
                s.sendto(p, host_from)
                seq = seq + 1

                # receive data from the host
                data, host_from = s.recvfrom(1024)

                # check if the received data is an ACK control frame with the correct sequence number
                if checkHeader(data)[1] == 4 and checkHeader(data)[2] == seq: #operation ACK = 4
                    print('Handshake is succesfull')
                    return 1
                else:
                    print(data)
                    continue # We continue if the sequence number remains zero.
            else: # create and send a FIN control frame
                pass # not implemented

                # check if the received data is an ACK control frame with the correct sequence number
                if checkHeader(data)[1] == 4 and checkHeader(data)[2] == seq: #operation ACK = 4
                    print('The connection is cut')
                    exit(0)
                else:
                    continue
            # The code will continue to run until the while loop is broken by a return or exit statement.

def show_usage() -> None:
    print("Usage: py/python3 SIMP_server.py <host> <port>")

if __name__ == "__main__":
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        host = '127.0.0.1'
        port = 8080

        '''
        When the fct handshake returns 1 indicating a successful handshake, the socket is opened and the function wait 
        and receive with the system's IP address is called. The program ends if fct start chatting returns 0,
        which happens when a user or the chat server logs off.
        '''

        if waitAndReceive(s, host, port)==1:
            print('Welcome to SIMP')
            if startChatting(s, host, port)==0:
                exit()
        else:
            exit(0)

 