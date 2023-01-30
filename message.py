import string as s

def createHeader(type: s,operation: s,sequence_number: int,username: s,message: s):
    '''
    Creates a bytearray with 5 input/output parameters and returns a bytearray
    for message type cm, a default username 'uname' and since the parameters "message length" and "chat message"
    are not present, the array is shorter.
    '''
    
    #Assign 2 for "control message" message types and 1 for "conversation" message types.
    if type == 'cm':
        by_arr = bytearray(3)
        by_arr[0] = 2
    elif type == 'chat':
        by_arr = bytearray(3)
        by_arr[0] = 1

    #Depending on the function's input, assign operation at index 1.
    if operation == 'send message':
        by_arr[1] = 1
    elif operation == "error":
        by_arr[1] = 1
    elif operation == "SYN":
        by_arr[1] = 2
    elif operation == "ACK":
        by_arr[1] = 4
    elif operation == "SYN+ACK":
        by_arr[1] = 6
    elif operation == "FIN":
        by_arr[1] = 8
    else:
        print('Unknown operation!')
        pass

    #At index 2, assign a sequence number.
    by_arr[2] = sequence_number

    #At index 3, assign a username.
    username_bytes = 32
    leading_zeros = username_bytes-len(username)
    by_arr = by_arr + (str(leading_zeros*'0')+username).encode('ASCII')

    if type == 'chat':
        #At index 4, assign payload len.
        by_arr = by_arr + (len(message)).to_bytes(1,byteorder ='little')

        #At index 5, assign payload.
        by_arr = by_arr + message.encode('ASCII')
    #print(f'send {operation}')
    else:
        #At index 4, assign payload len.
        by_arr = by_arr + (0).to_bytes(1,byteorder ='little')

        #At index 5, assign payload.
        by_arr = by_arr + message.encode('ASCII')

    return by_arr


def checkHeader(header: bytearray):
    '''
    Using a bytearray as input, this function separates the components into:
    type:int , operation: int, sequence_number: int, username: string , message_length: int , message: string.
    Then the following parameters are returned: mestype, operation, sequence_nb, username, message_length, chat_mess.
    '''
    mestype = header[0]
    if mestype == 1: #chat message
        operation = header[1]
        chat_mess = header[36:].decode('ASCII')
        message_length = header[35]
        username = header[5:35].decode('ASCII').replace('0', '')
        sequence_nb = header[2]
        return (mestype, operation, sequence_nb, username, message_length, chat_mess)

    else: #control message
        operation = header[1]
        username = header[5:35].decode('ASCII').replace('0', '')
        sequence_nb = header[2]
        return (mestype, operation, sequence_nb, username, 0, '')





