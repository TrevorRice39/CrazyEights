import socket
import sys

header_max_length = 15
message_max_size = 10

# creates a meta data header to request/send info from/to server
def create_header(request_type, message):
    # get the length of the message
    len_message = str(len(message))

    # make the header, should be 23 bytes exactly
    header = request_type.ljust(header_max_length) + '|' + len_message.zfill(message_max_size)

    # return header
    return header

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ("157.89.73.36", 9999)
sock.connect(server_address)


def receive_data():
    data = sock.recv(header_max_length + message_max_size + 1).decode()
    if len(data) != 26:
        return None, None
    requestType, size = data.split('|')

    # make sure there are no spaces (because of formatting)
    requestType = requestType.replace(' ', '')
    # get the size of the requests
    size = int(size)

    # receive the message
    message = sock.recv(size).decode()
    return [requestType, message]

def process_requests():
    requestType, message = receive_data()

    if requestType == None:
        return False
    if requestType == "requestSel":
        print(message)
        hand_size = int(receive_data()[1])

        selection = input()
        while not (selection.isdigit() and int(selection) < hand_size) and selection != 'q' and selection != 'd' :
            print(message)
            selection = input()
        sock.sendall(selection.ljust(2).encode())
    elif requestType == "requestSuit":
        print(message)
        selection = input()
        while (selection.isdigit() and int(selection) >= 4) or not (selection.isdigit()):
            print(message)
            selection = input()
        sock.sendall(selection.encode())
    elif requestType == "message":
        print(message)
    elif requestType == "playAgain":
        print(message)
        selection = input()

        while selection != 'y' and selection != 'n':
            print(message)
            selection = input()
        sock.sendall(selection.encode())
    elif requestType == "dc":
        print(message)
        sys.exit(0)


while True:
    process_requests()