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
serversocket.bind(("127.0.0.1", port))

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


# sends a header and some data to the client
def send_data(request_type, message, socket, newline):
    # if we want a new line
    if newline:
        message += "\n--------------------------------------------------"

    # make the header
    header = create_header(request_type, message)
    # send header
    socket.sendall(header.encode())
    # send data
    socket.sendall(message.encode())


# sends the card info to the player so they can see their current hand
def send_card_info(player, game, player_socket):
    send_data("message", str(player) + "\n\n" + "Top of discard: " + str(game.discard.peekTop()) + "\nCurrent Suit: " + str(game.currentSuit), player_socket, True)

# receiving data from client
def recv_data(playerSocket, size, listOfMessages):
    # this try except prevents the server from crashing when client closes app
    try:
        # send all the messages
        for message in listOfMessages:
            send_data(message[0], message[1], playerSocket, message[2])
        # get the data
        data = playerSocket.recv(size).decode()
        # did we get the correct amount?
        if data != size:
            recv_data(playerSocket, size, listOfMessages)
        return data
    except: # they closed or done something wrong
        print("error occured")
        return "q"

# plays a turn for a given player
def play_turn(player, playerSocket):

    # prepare list of messages to be sent to client
    # one is a request message
    # one is a regular message to be displayed
    listOfMessages = [["requestSel", "Select the card (by index) or d to draw or q to quit.", False], ["message", str(player.size), False]]

    # receive the data
    selection = recv_data(playerSocket, 2, listOfMessages)

    # clean spaces
    selection = selection.replace(' ', '')

    # if they wanted to draw
    if selection == "d":
        return ("d", "")
    elif selection == "q": # if they wanted to quit
        return ("q", "")
    # try to parse an integer out of the selection
    try:
        if player.cards[int(selection)].rank == "Eight":
            send_data("requestSuit", "Select a new suit. 0. Hearts, 1. Clubs, 2. Diamonds, 3. Spades", playerSocket, False)
            suit = int(playerSocket.recv(1).decode())
            newSuit = ["Hearts", "Clubs", "Diamonds", "Spades"][suit]
            #send_data("message", "Waiting for opponent to play a card...", playerSocket, True)
            return (int(selection), newSuit)
        else:
            return (int(selection), "")
    except:
        print("error occured")
    return ("q", "") # if nothing could be parsed, quit game


# restarts the game
def restart_game(game, playerSockets):
    # tell them their score
    send_data("message", "Your score is {0}\nYour opponent's score is {1}".format(game.player1Score, game.player2Score),
              playerSockets[0], True)
    send_data("message", "Your score is {0}\nYour opponent's score is {1}".format(game.player2Score, game.player1Score),
              playerSockets[1], True)

    # ask them if they want to play again
    send_data("playAgain", "Would you like to play again? (y or n)", playerSockets[0], False)
    p1choice = playerSockets[0].recv(1).decode()
    send_data("playAgain", "Would you like to play again? (y or n)", playerSockets[1], False)
    p2choice = playerSockets[1].recv(1).decode()

    # if both said yes, start anothe rgame
    if p1choice == p2choice and p2choice == 'y':
        game.newGame()
        play_game(playerSockets)
    else: # if not, show final score and close clients
        send_data("message",
                  "FINAL SCORE!\nYour score is {0}\nYour opponent's score is {1}".format(game.player1Score, game.player2Score),
                  playerSockets[0], True)
        send_data("message",
                  "FINAL SCORE!\nYour score is {0}\nYour opponent's score is {1}".format(game.player2Score, game.player1Score),
                  playerSockets[1], True)

        send_data("message", "You will be disconnected", playerSockets[0], True)
        send_data("dc", "", playerSockets[0], False) # disconnect message so client can properly close
        playerSockets[0].close()
        send_data("message", "You will be disconnected.", playerSockets[1], True)
        send_data("dc", "", playerSockets[1], False)
        playerSockets[1].close()


# main game entry
def play_game(player_sockets):
    game = Cards.Game() # make a new game

    game.startGame() # start it
    player1 = player_sockets[0] # get the sockets
    player2 = player_sockets[1]

    # tell them both the game is beginning
    for idx, player in enumerate(player_sockets):
        send_data("message", "The game is now beginning!", player, True)

    while True:
        # if player 1 is going
        if game.turn == 1:
            # tell other player to wait
            send_data("message", "Wait for opponents turn...", player2, True)
            # send the card info to player 1
            send_card_info(game.player1, game, player1)
            # get their selection from play_turn
            selection, suit = play_turn(game.player1, player1)
            # if it is quit, dc both players
            if selection == 'q':
                try:
                    send_data("dc", "You will be disconnected.", player1, True)
                    player1.close()
                except:
                    print("error")
                try:
                    send_data("dc", "Opponent has left.\nYou win!\nYou will be disconnected.", player2, True)
                    player2.close()
                except:
                    print("error")
                return None
            # get the result from the game when they make the move
            result = game.makeMove(game.turn, selection, suit)[1]
            # if player 1's move is invalid, try again
            if result == "p1i":
                send_data("message", "Invalid move. Try again.", player1, True)
            elif result == "p1w": # if player 1 wins
                send_data("message", "Congratulations! You win this round", player1, True)
                restart_game(game, player_sockets)
                return
            send_data("message", "", player2, True)
        elif game.turn == 2: # same as player 1, just reversed
            send_data("message", "Wait for opponents turn...", player1, True)
            send_card_info(game.player2, game, player2)
            selection, suit = play_turn(game.player2, player2)
            if selection == 'q':
                try:
                    send_data("dc", "You will be disconnected", player2, True)
                    player2.close()
                except:
                    print("error")
                try:
                    send_data("dc", "Opponent has left.\nYou win!\nYou will be disconnected.", player1, True)
                    player1.close()
                except:
                    print("error")
                return None
            result = game.makeMove(game.turn, selection, suit)[1]
            if result == "p2i":
                send_data("message", "Invalid move. Try again.", player2, True)
            elif result == "p2w":
                send_data("message", "Congratulations! You win this round", player2, True)
                restart_game(game, player_sockets)
                return
            send_data("message", "", player1, True)

while True:
    # found a connection
    clientsocket, addr = serversocket.accept()

    # add socket to current list
    players.append(clientsocket)
    # if we have 1 player, welcome them and tell them to wait for another player
    if len(players) == 1:
        message = "Welcome to the Crazy Eights server!\nPlease wait for another player to connect."
        send_data("message", message, clientsocket, True)

    # if we have 2 players connected
    elif len(players) == 2:
        # tell them the game is about to begin
        message = "Welcome to the Crazy Eights server!\nThe game is about to begin!"
        send_data("message", message, clientsocket, True)

        # start new thread for the game
        thread = Thread(target=play_game, args=(players,))
        thread.start()
        # reset player list so more players can connect and play their own games
        players = []
