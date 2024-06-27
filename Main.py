# actual game

import pygame as p
import Engine

WIDTH = HEIGHT = 512
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

    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gameState = Engine.GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False

    loadImages()

    running = True
    cellSelected = ()
    playerClicks = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//CELL_SIZE
                row = location[1]//CELL_SIZE
                if cellSelected == (row, col):
                    cellSelected = ()
                    playerClicks = []
                else:
                    cellSelected = (row, col)
                    playerClicks.append(cellSelected)
                if len(playerClicks)==2:
                    move = Engine.Move(playerClicks[0], playerClicks[1], gameState.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gameState.makeMove(move)
                        moveMade = True
                        cellSelected = ()
                        playerClicks = []
                    else:
                        playerClicks = [cellSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gameState.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False
        drawGameState(screen, gameState)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gameState):
    drawBoard(screen)
    drawPieces(screen, gameState.board)

def drawBoard(screen):
    colors = [p.Color(238,238,212,255), p.Color(125,148,92,255)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece!=".":
                screen.blit(IMAGES[piece], p.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))

if __name__=="__main__":
    main()
