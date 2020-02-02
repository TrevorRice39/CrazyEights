import Cards

game = Cards.Game()

game.startGame()
while True:
    print("Top of discard: {0}:".format(game.discard.peekTop()))
    if game.turn == 1:
        print(game.player1)
    else:
        print(game.player2)
    print("Player {0}, make your move: ".format(game.turn), end = '')
    move = input()
    if move.isdigit():
        move = int(move)
    else:
        if move != "d":
            while not (move.isdigit()) and move != "d":
                print("Invalid move")
                print("Player {0}, make your move: ".format(game.turn), end = '')
                move = input()
            if move.isdigit():
                move = int(move)
    game.makeMove(game.turn, move, "")
