import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 2, 4, 3, 3, 4, 2, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 2, 4, 3, 3, 4, 2, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 2, 2, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]


blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8]]

piecePosScores = {"N": knightScores, "B": bishopScores, "Q": queenScores, "R": rookScores, "wp": whitePawnScores, "bp": blackPawnScores}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4 # number of ply to search

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(gameState, validMoves, returnQueue):
    global nextMove, counter
    nextMove = None
    counter = 0
    random.shuffle(validMoves)
    findMoveNegaMaxAlphaBeta(gameState, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gameState.whiteToMove else -1)
    returnQueue.put(nextMove)

def findMoveNegaMaxAlphaBeta(gameState, validMoves, depth, alpha, beta, turnFlag):
    global nextMove

    if depth == 0:
        return turnFlag * scoreBoard(gameState)
    
    maxScore = -CHECKMATE

    for move in validMoves:
        gameState.makeMove(move)
        nextMoves = gameState.getValidMoves()

        score = -findMoveNegaMaxAlphaBeta(gameState, nextMoves, depth - 1, -beta, -alpha, -turnFlag)

        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move

        gameState.undoMove()

        if maxScore > alpha:
            alpha = maxScore

        if alpha >= beta:
            break

    return maxScore
    
def scoreBoard(gameState):
    if gameState.checkmate:
        if gameState.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gameState.stalemate:
        return STALEMATE
    
    score = 0

    for row in range(len(gameState.board)):
        for col in range(len(gameState.board[row])):
            cell = gameState.board[row][col];
            if cell != "--":
                piecePosScore = 0
                if (cell[1] != "K"):
                    if (cell == "wp" or cell == "bp"):
                        if cell == "wp":
                            piecePosScore = piecePosScores["wp"][row][col]
                            score += pieceScore[cell[1]] + piecePosScore * 0.1
                        elif cell == "bp":
                            piecePosScore = piecePosScores["bp"][row][col];
                            score -= pieceScore[cell[1]] + piecePosScore * 0.1
                    else:
                        piecePosScore = piecePosScores[cell[1]][row][col]
                        if cell[0] == "w":
                            score += pieceScore[cell[1]] + piecePosScore * 0.1
                        elif cell[0] == "b":
                            score -= pieceScore[cell[1]] + piecePosScore * 0.1
                
    
    return score

def scoreMaterial(board):
    score = 0

    for row in board:
        for cell in row:
            if cell[0] == "w":
                score += pieceScore[cell[1]]
            elif cell[0] == "b":
                score -= pieceScore[cell[1]]
    
    return score
