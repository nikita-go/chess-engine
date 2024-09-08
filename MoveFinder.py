import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(gameState, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveNegaMaxAlphaBeta(gameState, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gameState.whiteToMove else -1)
    return nextMove

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

    for row in gameState.board:
        for cell in row:
            if cell[0] == "w":
                score += pieceScore[cell[1]]
            elif cell[0] == "b":
                score -= pieceScore[cell[1]]
    
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
