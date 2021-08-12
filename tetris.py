


import math, copy, random

from cmu_112_graphics import *



def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def appStarted(app):
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.emptyColor= "blue"
    app.board = [ ([app.emptyColor] * app.cols) for row in range(app.rows)]
    app.board[0][0] = "red" # top-left is red
    app.board[0][app.cols-1] = "white" # top-right is white
    app.board[app.rows-1][0] = "green" # bottom-left is green
    app.board[app.rows-1][app.cols-1] = "gray" # bottom-right is gray
    app.score=0
    iPiece = [
        [  True,  True,  True,  True ]
    ]

    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    app.tetrisPieces=[ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [ "red", "yellow", "magenta", "pink",
     "cyan", "green", "orange" ]
    newFallingPiece(app)
    app.isGameOver = False
    

def gameDimensions():
    rows=15
    cols=10
    size=20
    margin=25
    return (rows, cols, size, margin)

def getCellBounds(app, row, col): 
    x0 = app.margin + col * app.cellSize
    x1 = app.margin + (col+1) * app.cellSize
    y0 = app.margin + row * app.cellSize
    y1 = app.margin + (row+1) * app.cellSize
    return (x0, y0, x1, y1)

def drawBoard(app, canvas):
   for i in range(app.rows):
       for j in range(app.cols):
           x0,y0,x1,y1=getCellBounds(app, i, j)
           canvas.create_rectangle(x0,y0,x1,y1, fill= app.board[i][j])

def newFallingPiece(app):
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.color = app.tetrisPieceColors[randomIndex]
    app.piece = app.tetrisPieces[randomIndex]
    app.fallingPieceRow=0
    app.fallingPieceCol=(app.cols//2)-(len(app.piece[0])//2)
    
def keyPressed(app, event):
    
    if (event.key=="Right"):
        moveFallingPiece(app,0,1)
    if (event.key=="Left"):
        moveFallingPiece(app,0,-1)
    if (event.key=="Down"):
        moveFallingPiece(app,1,0)
    if (event.key=="Up"):
        rotateFallingPiece(app)
    
    if (event.key=="r"):
        appStarted(app)
    if (event.key=="Space"):
        hardDrop(app)

    
def drawFallingPiece(app, canvas):
    
    
    x=app.fallingPieceCol
    y=app.fallingPieceRow
    
    for i in app.piece:
        for j in i:
            if j:
                x0,y0,x1,y1= getCellBounds(app, y, x)
                canvas.create_rectangle(x0,y0,x1,y1,fill=app.color)
            x+=1
        x=app.fallingPieceCol
        y+=1
    
def moveFallingPiece(app, drow, dcol):
    app.fallingPieceRow+=drow
    app.fallingPieceCol+=dcol
    if not fallingPieceIsLegal(app):
        app.fallingPieceRow-=drow
        app.fallingPieceCol-=dcol
        return False
    return True

def hardDrop(app):
    for each in range(app.rows):
        app.fallRow = each
        if fallingPieceIsLegal(app)==False:
            app.fallRow -=1
            break
    

def rotateFallingPiece(app):
    piece = app.piece
    oldNumRow = len(app.piece)
    oldNumCol = len(app.piece[0])
    oldRow=app.fallingPieceRow
    oldCol=app.fallingPieceCol
    fallingPiece=[([None] * oldNumRow) for row in range(oldNumCol)]
    for row in range(oldNumCol):
        for col in range(oldNumRow):
            fallingPiece[oldNumCol-1-row][col]=piece[col][row]
    app.piece=fallingPiece
    newNumR = len(fallingPiece)
    newNumC = len(fallingPiece[0])
    newRow = oldRow + oldNumRow//2-newNumR//2
    newCol = oldCol + oldNumCol//2-newNumR//2
    app.fallingPieceRow = newRow
    app.fallingPieceCol = newCol
    if (not fallingPieceIsLegal(app)):
        app.fallingPiece = piece
        app.fallingPieceRow = oldRow
    

def removeFullRows(app):
    board = []
    for i in app.board:
        if app.emptyColor in i:
            board.append(i)
    diff = len(app.board)-len(board)
    
    for i in range(diff):
        board.insert(0,([app.emptyColor] * app.cols))
        
    app.score+=diff**2
    app.board=board

def fallingPieceIsLegal(app):
    x=app.fallingPieceCol
    y=app.fallingPieceRow
    for i in app.piece:
        for j in i:
            if j:
                if (x<0 or x>=app.cols) or (y<0 or y>=app.rows):
                    return False
                if (app.board[y][x]!="blue"):
                    return False
            x+=1
        x=app.fallingPieceCol
        y+=1

    return True
def hardDrop(app):
    for each in range(app.rows):
        app.fallingPieceRow = each
        if fallingPieceIsLegal(app)==False:
            app.fallingPieceRow -=1
            break
def placeFallingPiece(app):
    x=app.fallingPieceCol
    y=app.fallingPieceRow
    
    for i in app.piece:
        for j in i:
            if j:
                app.board[y][x]=app.color
            x+=1
        x=app.fallingPieceCol
        y+=1
    removeFullRows(app)

def timerFired(app):
    if not app.isGameOver:
        if not moveFallingPiece(app, 1, 0):
            placeFallingPiece(app)
            newFallingPiece(app)
            app.score+=1
    if fallingPieceIsLegal(app) == False:
        app.isGameOver=True
    
def drawGameOver(app, canvas):
    if app.isGameOver:
        canvas.create_text(app.width/2, app.height/2,
                        text='Game Over!',
                        fill='Yellow',
                        font='Arial 18 bold'
                        )
        canvas.create_text(app.width/2, app.height/2 + 50,
                        text='Press r to restart',
                        fill='Yellow',
                        font='Arial 16 bold'
                        )
def drawScore(app, canvas):
   
    canvas.create_text(app.width/2, app.margin/2,
                    text='Score: '+str(app.score),
                    fill='Black',
                    font='Arial 18 bold'
                    )
    

def redrawAll(app, canvas):
    drawBoard(app,canvas)
    drawFallingPiece(app,canvas)
    drawGameOver(app,canvas)
    drawScore(app,canvas)
def playTetris():
    rows, cols, size, margin = gameDimensions()
    width=2*margin+size*cols
    height=2*margin+size*rows
    
    runApp(width=width, height=height)



#################################################
# main
#################################################

def main():
    
    playTetris()

if __name__ == '__main__':
    main()
