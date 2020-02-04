import Cards
import socket  # socket programming
from threading import Thread

# create a socket object
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

# host ip
host = socket.gethostname()

# port
port = 9999

# bind to the port
serversocket.bind(("157.89.73.36", port))

# queue up to 5 requests
serversocket.listen(20)

players = []  # max 2
header_max_length = 15
message_max_size = 10


# creates a meta data header to request/send info from/to server
def create_header(request_type, message):
    # get the length of the message
    len_message = str(len(message))

    # make sure there are no spaces (because of formatting)
    requestType = request_type.replace(' ', '')

    # make the header, should be 23 bytes exactly
    header = request_type.ljust(header_max_length) + '|' + len_message.zfill(message_max_size)

    # return header
    return header


def send_data(request_type, message, socket, newline):
    if newline:
        message += "\n--------------------------------------------------"
    header = create_header(request_type, message)
    socket.sendall(header.encode())
    socket.sendall(message.encode())


def send_card_info(player, game, player_socket):
    send_data("message", str(player) + "\n\n" + "Top of discard: " + str(game.discard.peekTop()) + "\nCurrent Suit: " + str(game.currentSuit), player_socket, True)


def play_turn(player, playerSocket):
    send_data("requestSel", "Select the card (by index) or d to draw or q to quit.", playerSocket, False)
    send_data("message", str(player.size), playerSocket, False)
    selection = playerSocket.recv(2).decode()
    selection = selection.replace(' ', '')
    if selection == "d":
        return ("d", "")
    elif selection == "q":
        return ("q", "")
    elif player.cards[int(selection)].rank == "Eight":
        send_data("requestSuit", "Select a new suit. 0. Hearts, 1. Clubs, 2. Diamonds, 3. Spades", playerSocket, False)
        suit = int(playerSocket.recv(1).decode())
        newSuit = ["Hearts", "Clubs", "Diamonds", "Spades"][suit]
        send_data("message", "Waiting for opponent to play a card...", playerSocket, True)
        return (int(selection), newSuit)
    send_data("message", "Waiting for opponent to play a card...", playerSocket, True)
    return (int(selection), "")


def play_game(player_sockets):
    game = Cards.Game()

    game.startGame()
    player1 = player_sockets[0]
    player2 = player_sockets[1]

    for idx, player in enumerate(player_sockets):
        send_data("message", "The game is now beginning!", player, True)
        send_data("message", "You are player " + str(idx+1), player, True)

    send_card_info(game.player1, game, player1)
    send_card_info(game.player2, game, player2)

    playing = True

    while playing:
        if game.turn == 1:
            send_card_info(game.player1, game, player1)
            selection, suit = play_turn(game.player1, player1)
            if selection == 'q':
                send_data("message", "You will be disconnected.", player1, True)
                player1.close()
                send_data("message", "Opponent has left.\nYou win!\nYou will be disconnected.", player2, True)
                player2.close()
                return None
            result = game.makeMove(game.turn, selection, suit)
            print(result)
        elif game.turn == 2:
            send_card_info(game.player2, game, player2)
            selection, suit = play_turn(game.player2, player2)
            if selection == 'q':
                send_data("message", "You will be disconnected", player2, True)
                player2.close()
                send_data("message", "Opponent has left.\nYou win!\nYou will be disconnected.", player1, True)
                player1.close()
                return None
            result = game.makeMove(game.turn, selection, suit)
            print(result)


while True:
    # found a connection
    clientsocket, addr = serversocket.accept()
    # if len(players) < 2:
    players.append(clientsocket)
    if len(players) == 1:
        message = "Welcome to the Crazy Eights server!\nPlease wait for another player to connect."
        send_data("message", message, clientsocket, True)

    elif len(players) == 2:
        message = "Welcome to the Crazy Eights server!\nThe game is about to begin!"
        send_data("message", message, clientsocket, True)
        thread = Thread(target=play_game, args=(players,))
        thread.start()
        players = []
