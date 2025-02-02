# Place your creative task here!

''' 1. Dual rotation (both clockwise and counterclockwise rotation).
    3. More attractive pieces and a more attractive board. (The game & pieces of the colors are Taylor Swift themed :)'''

# Be clever, be creative, have fun!

from cmu_graphics import * 
import random

def onAppStart(app):
    app.rows = 15
    app.cols = 10
    app.boardLeft = 95
    app.boardTop = 50
    app.boardWidth = 210
    app.boardHeight = 280
    app.cellBorderWidth = 2
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.piece = None
    app.pieceColor = None 
    app.nextPieceIndex = 0
    app.paused = False
    app.stepsPerSecond = 2
    app.scores = [0, 40, 100, 300, 1200]
    app.playerScore = 0
    app.gameOver = False
    loadTetrisPieces(app)
    loadNextPiece(app)
    app.url = 'https://i.redd.it/eo2hdnuqbzc51.png' #Lover themed background.
            
def onKeyPress(app, key):
    if app.gameOver: 
        #Reset the original board.
        app.gameOver = False
        app.score = 0
        app.board = [([None] * app.cols) for row in range(app.rows)]
        loadNextPiece(app)
        
    else: #Key functionality. 
        if key == 'p':
            app.paused = not app.paused
            return 
        
        if not app.paused: 
            if key == 'left':
                movePiece(app, 0, -1)
    
            if key == 'right':
                movePiece(app, 0, 1)
        
            if key == 'down':
                movePiece(app, 1, 0)
        
            if key == 'space':
                hardDropPiece(app)
        
            if key == 'up':
                rotatePieceClockwise(app)
                
            if key == 'j':
                rotatePieceCounterClockwise(app)
        
            if key == 's':
                takeStep(app)
        
        if key in ['a','b','c','d','e','f','g','h']:
            loadTestBoard(app, key)
        
def onStep(app):
    if not app.paused:
        takeStep(app)
        
def loadTestBoard(app, key):
    # DO NOT EDIT THIS FUNCTION
    # We are providing you with this function to set up the board
    # with some test cases for clearing the rows.
    # To use this: press 'a', 'b', through 'h' to select a test board.
    # Then press 'space' for a hard drop of the red I,
    # and then press 's' to step, which in most cases will result
    # in some full rows being cleared.

    # 1. Clear the board and load the red I piece 
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.nextPieceIndex = 0
    loadNextPiece(app)
    # 2. Move and rotate the I piece so it is vertical, in the
    #    top-left corner
    for keyName in ['down', 'down', 'up', 'left', 'left', 'left']:
        onKeyPress(app, keyName)
    # 3. Add a column of alternating plum and lavender cells down
    #    the rightmost column
    for row in range(app.rows):
        app.board[row][-1] = 'plum' if (row % 2 == 0) else 'lavender'
    # 4. Now almost fill some of the bottom rows, leaving just the
    #    leftmost column empty
    indexesFromBottom = [ [ ], [0], [0,1], [0,1,2], [0,2],
                          [1,2,3], [1,2,4], [0,2,3,5] ]
    colors = ['moccasin', 'aqua', 'khaki', 'aquamarine',
              'darkKhaki', 'peachPuff']
    for indexFromBottom in indexesFromBottom[ord(key) - ord('a')]:
        row = app.rows - 1 - indexFromBottom
        color = colors[indexFromBottom]
        for col in range(1, app.cols):
            app.board[row][col] = color
        
def rotatePieceClockwise(app):
    oldPiece = app.piece
    oldTopRow = app.pieceTopRow
    oldLeftCol = app.pieceLeftCol
    oldRows = len(oldPiece)
    oldCols = len(oldPiece[0])
    
    #Calling rotate2dListClockwise
    app.piece = rotate2dListClockwise(app.piece)
    #Adjusting the top row and left col of the new piece. 
    centerRow = oldTopRow + oldRows // 2
    newRows = len(app.piece)
    app.pieceTopRow = centerRow - newRows // 2

    centerCol = oldLeftCol + oldCols // 2
    newCols = len(app.piece[0])
    app.pieceLeftCol = centerCol - newCols // 2
    
    #If move is not legal, reset to oldTopRow and oldLeftCol.
    if not pieceIsLegal(app):
        app.piece = oldPiece 
        app.pieceTopRow = oldTopRow 
        app.pieceLeftCol = oldLeftCol 
         
def rotate2dListClockwise(L):
    oldRows = len(L)
    oldCols = len(L[0])
    newRows = oldCols
    newCols = oldRows
    M = []
    
    for oldCol in range(oldCols):
        newList = []
        for oldRow in range(oldRows):
            newList.append(L[oldRow][oldCol])
        M.append(newList)
            
    for oldRow in range(oldRows):
        for oldCol in range(oldCols):
            newRow = oldCol
            newCol = oldRows - oldRow - 1
            M[newRow][newCol] = L[oldRow][oldCol]
    return M
  
def rotatePieceCounterClockwise(app):
    oldPiece = app.piece
    oldTopRow = app.pieceTopRow
    oldLeftCol = app.pieceLeftCol
    oldRows = len(oldPiece)
    oldCols = len(oldPiece[0])
    
    app.piece = rotate2dListCounterClockwise(app.piece)
   
    #Adjust col. 
    centerCol = oldLeftCol + oldCols // 2
    newCols = len(app.piece[0])
    app.pieceLeftCol = centerCol - newCols // 2
   
    #Adjusting the top row. 
    centerRow = oldTopRow + oldRows // 2
    newRows = len(app.piece)
    app.pieceTopRow = centerRow - newRows // 2

    
    
    #If move is not legal, reset to oldTopRow and oldLeftCol.
    if not pieceIsLegal(app):
        app.piece = oldPiece 
        app.pieceTopRow = oldTopRow 
        app.pieceLeftCol = oldLeftCol

def rotate2dListCounterClockwise(L):
    oldRows = len(L)
    oldCols = len(L[0])
    newRows = oldCols
    newCols = oldRows
    M = []
    
    for oldCol in range(oldCols):
        newList = []
        for oldRow in range(oldRows):
            newList.append(L[oldRow][oldCol])
        M.append(newList)
            
    for oldRow in range(oldRows):
        for oldCol in range(oldCols):
            newRow = newRows - oldCol - 1
            newCol = oldRow
            M[newRow][newCol] = L[oldRow][oldCol]
    return M

def movePiece(app, drow, dcol):
    app.pieceTopRow += drow
    app.pieceLeftCol += dcol
    if pieceIsLegal(app):
        return True
    else:
        app.pieceTopRow -= drow
        app.pieceLeftCol -= dcol
        return False
                        
def hardDropPiece(app):
    while movePiece(app, +1, 0):
        pass
    
def pieceIsLegal(app): 
    if app.piece != None:
        #Check boundaries of the board. 
        if (0 <= app.pieceTopRow + len(app.piece) <= app.rows) and (0 <= app.pieceLeftCol + len(app.piece[0]) <= app.cols): 
            if (0 <= app.pieceTopRow < app.rows) and (0 <= app.pieceLeftCol < app.cols): 
                for row in range(len(app.piece)):
                    for col in range(len(app.piece[row])): 
                        if app.piece[row][col] is True: 
                            #Check if empty space.
                            if app.board[app.pieceTopRow+row][app.pieceLeftCol+col] != None: 
                                return False
            else: return False
        else: return False
    return True

def redrawAll(app):
    #Background
    drawImage(app.url, app.width // 2, app.height // 2, align='center')
    drawLabel("Tetris (Taylor's Version)", 200, 30, size=25, font='sacramento')
    drawBoard(app)
    drawPiece(app)
    drawBoardBorder(app)
    if app.gameOver:
        drawGameOverMessage(app)
        return
    drawLabel(f'Karma Points: {app.playerScore}', app.width // 2, 350, size=20, font='sacramento') 
    
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, app.board[row][col])

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

# To start, copy the code from the end of Step 1.
# Then closely follow the instructions.

def loadTetrisPieces(app):
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]] 
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece,
                         sPiece, tPiece, zPiece ]

# Taylor Swift albums and their corresponding theme/color that I used for the Tetris pieces. :)
    #Fearless TV - yellow/golden
    #Speak Now TV - lavender/purple
    #Red TV - red
    #Lover - light pink 
    #Folklore - gray
    #Evermore - brown
    #Midnights - dark blue
    app.tetrisPieceColors = [ 'gold', 'mediumPurple', 'fireBrick', 'lightPink',
                              'gray', 'sienna', 'midnightBlue']
                              
def drawPiece(app):
    if app.piece != None:
        for row in range(len(app.piece)):
            for col in range(len(app.piece[row])):
                if app.piece[row][col] is True:
                    drawCell(app,app.pieceTopRow + row,app.pieceLeftCol + col, app.pieceColor)

def loadRandomPiece(app): 
    pieceIndex = random.randrange(len(app.tetrisPieces))
    loadPiece(app, pieceIndex)

def loadPiece(app, pieceIndex): 
    app.piece = app.tetrisPieces[pieceIndex]
    app.pieceColor = app.tetrisPieceColors[pieceIndex]
    app.pieceTopRow = 0
    pieceCols = len(app.piece[0])
    app.pieceLeftCol = (app.cols // 2) - ((pieceCols + 1) // 2)
    
def loadNextPiece(app):
    if not app.gameOver:
        app.nextPieceIndex = getRandomIndex(app)
        loadPiece(app, app.nextPieceIndex)
    app.nextPieceIndex += 1
    if app.nextPieceIndex > len(app.tetrisPieces):
        #Reset index.
        app.nextPieceIndex = 0
    
    if not pieceIsLegal(app):
        app.gameOver = True

def getRandomIndex(app):
    return random.randrange(len(app.tetrisPieces))

def takeStep(app):
    if not movePiece(app, +1, 0):
        placePieceOnBoard(app)
        removeFullRows(app)
        loadNextPiece(app)

def placePieceOnBoard(app):
    for row in range(len(app.piece)):
        for col in range(len(app.piece[0])):
            if app.piece[row][col] is True:
                app.board[app.pieceTopRow + row][app.pieceLeftCol + col] = app.pieceColor

def removeFullRows(app):
    countRowsRemoved = 0
    newBoard = []
    for row in app.board:
        if None in row:
            newBoard.append(row)
        else:
            countRowsRemoved += 1
    numEmptyRows = app.rows - len(newBoard)
    newBoard = [([None] * app.cols) for i in range(numEmptyRows)] + newBoard
    app.board = newBoard
    
    if countRowsRemoved < len(app.scores):
        app.playerScore += app.scores[countRowsRemoved]

def GameOverMessage(app):
    drawLabel('Game Over!', app.width // 2, 350, size=25, font='sacramento')
    drawLabel('Press any key or click to start a new game.', app.width // 2, 380, size=25, font='sacramento')
    
def main():
    runApp()

main()