import socket
import time
from message import createHeader, checkHeader

def startChatting(s,host,port):
    """
     function starts a chat session with a server. It takes in the following parameters:
        s: a socket object representing the connection to the server
        host: a string representing the host IP address
        port: an integer representing the port number of the server
    """
    # The user enters a name, and the server and user's sequence numbers are manually initialized.
    print('Welcome to SIMP')
    username = 'alex'
    seq_user = 0
    seq_server = 100
    message = input(f'{username}: ')
    # Until the user or server quits, an infinite while loop starts to facilitate message exchange.
    while True:
        # The createHeader function from message.py converts the user message into a header if it is not a quit request.
        x = createHeader('chat','send message',seq_user,username,message)
        #send chat message
        s.sendto(x,(host,port))
        s.settimeout(5)             #set timeout to 5 seconds for the ACK control frame
        #wait for chat ACK
        try:
            response, host_from = s.recvfrom(1024)
            print(response[2],' vs ',seq_user)
            while response[2] != seq_user:      #wait for correct seq number
                print('2: Discard frame with seq numb =', response[2])
                response, host_from = s.recvfrom(1024)
        except socket.timeout:
            print('STO: resend' , x , 'with seq = ', x[2])
            continue
        

        s.settimeout(None) #Set the timeout to None in the chat message to permit users to respond after 5 seconds.
        response, host_from = s.recvfrom(1024)
        print(response[2],' vs ',seq_server)
        while response[2] != seq_server: #wait for correct seq number
            print('2: Discard frame with seq numb =', response[2])
            #reject message if seq doesn't match
            response, host_from = s.recvfrom(1024)
        print(checkHeader(response)[3], ': ', checkHeader(response)[5])
        #Using the createHeader function, the user constructed a control frame with ACK.
        y = createHeader('cm','ACK',response[2],username,'')
        # Conserves the incoming server_seq so that it can be increased later and be the acceptance criterion.
        seq_server = response[2]
        time.sleep(11)
        # user sends back an ACK control frame
        s.sendto(y,(host,port))
        message = input(f'{username}: ')
        # sequence numbers are increased by 1
        seq_user = seq_user + 1
        seq_server = seq_server + 1

    return 0

def threeWhandshake(s, host, port):
    """
    function performs a three-way handshake to establish a connection with a server. It takes in the following parameters
        s: a socket object representing the connection to the server
        host: a string representing the host IP address
        port: an integer representing the port number of the server
    """
    while True:
        #User sends server a SYN control frame.
        seq=0           # Initialize sequence number
        t = createHeader('cm','SYN',seq,'name','')
        s.sendto(t, (host, port))
        print('send SYN...')
        #User is waiting for a response frame.
        response, host_from = s.recvfrom(1024)      # Receive response from the server

        # When a response is received, use the message.py checkHeader function to verify it, then choose option 1 to
        # proceed. When the user receives a SYN+ACK and replies with an ACK, the function calls "handshake" and returns 1.
        if checkHeader(response)[1] == 6: #operation SYN+ACK = 6
            seq = seq +1
            w = createHeader('cm','ACK',seq,'name','')
            s.sendto(w, (host, port))   # Send the ACK frame to the server
            return 1

        # Option 2 involves the user receiving a FIN, which signifies the server rejected the request,
        # and the user responding with an ACK and a return value of 0.
        elif checkHeader(response)[1] == 8: #operation FIN = 8
            seq = seq + 1
            z = createHeader('cm', 'ACK', seq, 'name', '')
            s.sendto(z, (host, port))
            print('Chat request rejected')
            return 0
        # If the response is none of the above
        else:
            print('Unknown')
            continue

def show_usage() -> None:
    print("Usage: py/python3 SIMP_client.py <host> <port>")

if __name__ == "__main__":

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

        host = '127.0.0.1'
        port = 8080

        '''
        When the function handshake returns 1, it indicates that the handshake was successful, and the function start 
        chatting is called. The socket is opened, and the function handshake is run with the system's IP address and 
        host. The program ends if fct start chatting returns 0, which happens when a user or the chat server logs off.
        '''

        if threeWhandshake(s, host, port)==1:
            if startChatting(s, host, port)== 0:
                exit()
        else:
            exit()
