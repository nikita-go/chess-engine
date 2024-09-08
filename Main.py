# actual game

import pygame as p
import Engine, MoveFinder

WIDTH = HEIGHT = 512
PANEL_HEIGHT = 512
PANEL_WIDTH = 250
DIMENSION = 8
CELL_SIZE = 64
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wB", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (CELL_SIZE, CELL_SIZE))
    
def main():
    p.init()

    screen = p.display.set_mode((WIDTH + PANEL_WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gameState = Engine.GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True
    cellSelected = ()
    playerClicks = []
    gameOver = False
    playerOne = True # white
    playerTwo = True # black
    moveLogFont = p.font.SysFont("Helvetica", 16, True, False)

    while running:
        humanTurn = (gameState.whiteToMove and playerOne) or (not gameState.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0]//CELL_SIZE
                    row = location[1]//CELL_SIZE
                    if cellSelected == (row, col)or col >= 8:
                        cellSelected = ()
                        playerClicks = []
                    else:
                        cellSelected = (row, col)
                        playerClicks.append(cellSelected)
                    if len(playerClicks)==2:
                        move = Engine.Move(playerClicks[0], playerClicks[1], gameState.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move==validMoves[i]:
                                gameState.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                cellSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [cellSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gameState.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r:
                    gameState = Engine.GameState()
                    validMoves = gameState.getValidMoves()
                    cellSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        if not gameOver and not humanTurn:
            AIMove = MoveFinder.findBestMove(gameState, validMoves)

            if AIMove is None:
                AIMove = MoveFinder.findRandomMove(validMoves)
            
            gameState.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gameState.previousMoves[-1], screen, gameState.board, clock)
            validMoves = gameState.getValidMoves()
            moveMade = False
            animate = False
        drawGameState(screen, gameState, validMoves, cellSelected, moveLogFont)
        if gameState.checkmate or gameState.stalemate:
            gameOver = True
            if gameState.stalemate:
                gameOver = True
                drawEndGameText(screen, "Draw by stalemate")
            else:
                drawEndGameText(screen, "Black wins by checkmate" if gameState.whiteToMove else "White wins by checkmate")

        clock.tick(MAX_FPS)
        p.display.flip()

def highlightSquares(screen, gameState, validMoves, cellSelected):
    if cellSelected != ():
        r, c = cellSelected
        if gameState.board[r][c][0] == ("w" if gameState.whiteToMove else "b"):
            s = p.Surface((CELL_SIZE, CELL_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s, (c*CELL_SIZE, r*CELL_SIZE))
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*CELL_SIZE, move.endRow*CELL_SIZE))

def drawGameState(screen, gameState, validMoves, cellSelected, moveLogFont):
    drawBoard(screen)
    highlightSquares(screen, gameState, validMoves, cellSelected)
    drawPieces(screen, gameState.board)
    drawMoveLog(screen, gameState, moveLogFont)

def drawBoard(screen):
    global colors
    colors = [p.Color(238,238,212,255), p.Color(125,148,92,255)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece!="--":
                screen.blit(IMAGES[piece], p.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def drawMoveLog(screen, gameState, font):
    moveLogRect = p.Rect(WIDTH, 0, PANEL_WIDTH, PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    previousMoves = gameState.previousMoves
    moveTexts = []
    for i in range(0, len(previousMoves), 2):
        moveString = str(i//2 + 1) + ". " + str(previousMoves[i]) + " "
        if i + 1 < len(previousMoves):
            moveString += str(previousMoves[i+1]) + " "
        moveTexts.append(moveString)
    movesPerRow = 3
    padding = 5
    textY = padding
    lineSpace = 2
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i + j]
        textObject = font.render(text, True, p.Color("white"))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpace

def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR)+abs(dC))*framesPerSquare
    for frame in range(frameCount+1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow+move.endCol)%2]
        endSquare = p.Rect(move.endCol*CELL_SIZE, move.endRow*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured!="--":
            if move.isEnpassantMove:
                enpassantRow = move.endRow + 1 if move.pieceCaptured[0]=="b" else move.endRow - 1
                endSquare = p.Rect(move.endCol*CELL_SIZE, enpassantRow*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        p.display.flip()
        clock.tick(60)

def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0, p.Color("Gray"))
    textLocation = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__=="__main__":
    main()
