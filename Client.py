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
server_address = (socket.gethostname(), 9999)
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
    requestType, message = receive_data() # receive data from server

    if requestType == None: # if there is no request, return false
        return False
    if requestType == "requestSel": # if they need to request a selection from the user
        print(message) # print the request message
        hand_size = int(receive_data()[1]) # get the hand size

        selection = input() # get their selection
        # has to be 'q', 'd', or a card in their hand which is a digit for the position
        while not (selection.isdigit() and int(selection) < hand_size) and selection != 'q' and selection != 'd' :
            print(message)
            selection = input()
        # send it to the server
        sock.sendall(selection.ljust(2).encode())
    # request a new suit
    elif requestType == "requestSuit":
        print(message) # print the request message
        # get their input
        selection = input()
        # select a suit 0-3
        while (selection.isdigit() and int(selection) >= 4) or not (selection.isdigit()):
            print(message)
            selection = input()
        # send choice to server
        sock.sendall(selection.encode())
    # if the server just wants to display something
    elif requestType == "message":
        print(message) # print message
    # ask the client if they want to play again
    elif requestType == "playAgain":
        print(message) # print message
        selection = input()
        # they choose yes or no
        while selection != 'y' and selection != 'n':
            print(message)
            selection = input()
        # send it to the server
        sock.sendall(selection.encode())
    # if they're being disconnected
    elif requestType == "dc":
        print(message)
        sys.exit(0) # close app

while True:
    process_requests()