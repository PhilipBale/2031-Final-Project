        ORG     0
Start:  
        JUMP MainLoop

MainLoop:
        Call IsFinished

        Call CheckSonar #Store object positions from sonar here

        Load Zero
        STORE HasMoved

        CALL CheckRight
        JPOS MoveRight

        Load HasMoved #Check if we just moved
        JPOS MainLoop

        CALL CheckForward
        JPOS MoveForward

        Load HasMoved #Check if we just moved
        JPOS MainLoop

        CALL CheckLeft
        JPOS MoveLeft

        Load HasMoved #Check if we just moved
        JPOS MainLoop

        #If we got here, we never moved
        Call MoveBackward

        JUMP MainLoop


IsFinished:
        # Check if all grid positions have been examined
        #If finished, stay here, otherwise return

        RETURN


MoveRight:
        CALL LoadPosition

        # Check if right position is in valid grid bounds

        CALL HasVisited
        JPOS EarlyReturn

        # Actual rotate and move right if empty

        CALL StorePosition

        CALL MarkVisited

        RETURN

MoveForward:
        CALL LoadPosition

        # Check if forward position is in valid grid bounds

        CALL HasVisited
        JPOS EarlyReturn

        # Actual rotate and move forward if empty

        CALL StorePosition

        CALL MarkVisited

        RETURN


MoveLeft:
        CALL LoadPosition

        # Check if left position is in valid grid bounds

        CALL HasVisited
        JPOS EarlyReturn

        # Actual rotate and move left if empty

        CALL StorePosition

        CALL MarkVisited

        RETURN

MoveBackward:
        CALL DecrementPosition

        # Actual rotate and move backward



StorePosition:
        #Store current position in array

        RETURN

LoadPosition:
        #Load current position from array

        RETURN

DecrementPosition:
        #Decrement position stack

        RETURN

MarkVisited:
        #Use VARX, VARY

        RETURN

HasVisited:
        #Use VARX, VARY, return 0 if no, positive if yes

        RETURN

EarlReturn:
    RETURN

VARX:   DW      &H0000
VARY:   DW      &H0000