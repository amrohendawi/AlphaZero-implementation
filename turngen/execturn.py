import numpy as np
    

def newStateTargetField(existingPiece, newPiece):
    # if pieces are opposing
    if existingPiece == 0: return newPiece
    if 1 <= existingPiece <=  3 and 4 <= newPiece <= 6 or 1 <= existingPiece <=  3 and 4 <= newPiece <= 6:
        #this is a capture
        #old piece is a single
        if existingPiece == 1 or existingPiece == 4: return newPiece
        #old piece is a tower
        if existingPiece == 2: return 6
        if existingPiece == 3: return 5
        if existingPiece == 5: return 3
        if existingPiece == 6: return 2
    else:
        #making a freindly stack
        return existingPiece + 1        

def newStateStartField(existingPiece):
    if existingPiece == 1 or existingPiece == 4: return 0
    if existingPiece == 5 or existingPiece == 3: return 4
    if existingPiece == 6 or existingPiece == 2: return 1    
    elif existingPiece == 0: return -80085 # instructions: turn your calculator upside-down

def movingPiece(startField):
    if startField == 2 or startField == 3: return 1
    if startField == 5 or startField == 6: return 4  

def getIndicies(pos):
    # pos has the format "xy" (x being a letter from a-h and y being a number from 1-8)
    x = pos[0]
    y = int(pos[1])
    
    if y == 8: y = 1
    elif y == 7: y = 2
    elif y == 6: y = 3
    elif y == 5: y = 4
    elif y == 4: y = 5
    elif y == 3: y = 6
    elif y == 2: y = 7
    else: y = 8

    print("Y = " + str(y))

    if x == "a": x = 1
    if x == "b": x = 2
    if x == "c": x = 3
    if x == "d": x = 4
    if x == "e": x = 5
    if x == "f": x = 6
    if x == "g": x = 7
    if x == "h": x = 8

    return [y - 1, x - 1]

def executeMove(board, move):
    moveSplit = move.split("-") 

    startPos = getIndicies(moveSplit[0]) # Not like this, will google later
    targetPos = getIndicies(moveSplit[1])
    
    print("StartPos = " + str(startPos))

    startField = board[startPos[0]][startPos[1]]
    targetField = board[targetPos[0]][targetPos[1]]

    newTargetField = newStateTargetField(targetField, movingPiece(startField))
    newStartField = newStateStartField(startField)

    newBoard = board
    
    newBoard[startPos[0]][startPos[1]] = newStartField
    newBoard[targetPos[0]][targetPos[1]] = newTargetField

    return newBoard    

if __name__== "__main__":
    # examples

    board = np.array([-1,0,1,1,1,1,1,-1,
								0,2,1,1,1,1,1,0,
								0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,
								0,4,4,4,4,4,4,0,
								-1,4,4,4,4,4,4,-1]).reshape(8,8)

    move = "b7-c5"

    newBoard = executeMove(board, move)

    print(newBoard)