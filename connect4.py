import random

class Board:

    def __init__( self, width, height ): 
        self.width = width 
        self.height = height 
        self.data = [] # this will be the board 
         
        for row in range( self.height ): 
            boardRow = [] 
            for col in range( self.width ): 
                boardRow += [' '] 
            self.data += [boardRow] 
        return                
                
    def __repr__(self): 
        #print out rows & cols 
        s = '' # the string to return 
        for row in range( self.height ): 
            s += '|' # add the spacer character 
            for col in range( self.width ): 
                s += self.data[row][col] + '|' 
            s += '\n' 
    
        s += '--'*self.width + '-\n'
     
        for col in range(self.width):
            s += ' ' + str(col % 10)
        s += '\n'
            
        return s
    
    def addMove(self, col, ox):
        if self.allowsMove(col):
            for row in range (self.height):
                if self.data[row][col] != ' ':
                    self.data[row-1][col] = ox
                    return
            self.data[self.height-1][col] = ox
    
    def clear(self):      
        for row in range( self.height ):
            for col in range( self.width ):
                if self.data[row][col] != ' ' :
                    self.data[row][col] = ' '           
                        
    def delMove( self, col ):
        for row in range (self.height):
            if self.data[row][col] != ' ':
                self.data[row][col] = ' '
                return
            
            
    def setBoard( self, moveString ): 
             
        nextCh = 'X' 
        for colString in moveString: 
            col = int(colString) 
            if 0 <= col <= self.width: 
                self.addMove(col, nextCh) 
            if nextCh == 'X': 
                nextCh = 'O' 
            else: 
                nextCh = 'X'
        return             
    
    def fillBoard( self ): 
        for rows in range (self.height):
            for col in range (self.width):
                self.data[rows][col] = 'X'
        return
    
    def allowsMove(self,col):
        ans = True
        #for rows in range (self.height):
        if col < 0 or col >= self.width:
            ans = False
            
        if ans:    
            if self.data[0][col] != ' ':
                ans = False
        return ans
    
    def ifFull(self):
        ans = True
        for rows in range (self.height):
            for col in range (self.width):
                if self.data[rows][col] == ' ':
                    ans = False
        return ans
                
    def winsFour(self, ox):
        status = False
        # check for horizontal wins
        for row in range(0,self.height):
            for col in range(0,self.width-3):
                if self.data[row][col] == ox and \
                self.data[row][col+1] == ox and \
                self.data[row][col+2] == ox and \
                self.data[row][col+3] == ox:
                    status = True    
        # check for vertical wins
        for row in range(0,self.height-3):
            for col in range(0,self.width):
                if self.data[row][col] == ox and \
                self.data[row+1][col] == ox and \
                self.data[row+2][col] == ox and \
                self.data[row+3][col] == ox:
                    status = True
        # check for Diagonally NE ï¿½ SW wins
        for row in range(0,self.height-3):
            for col in range(0,self.width-3):
                if self.data[row][col] == ox and \
                self.data[row+1][col+1] == ox and \
                self.data[row+2][col+2] == ox and \
                self.data[row+3][col+3] == ox:
                    status = True          
        # check for Diagonally NW ï¿½ SE wins
        for row in range(3,self.height):
            for col in range(0,self.width-3):
                if self.data[row][col] == ox and \
                self.data[row-1][col+1] == ox and \
                self.data[row-2][col+2] == ox and \
                self.data[row-3][col+3] == ox:
                    status = True  
                
        return status
    
    def myInput(self, ox):
        while True:
            play = input(ox + "'s turn:  ")
            play = int(play)
            if self.allowsMove(play):
                return play
         
    def hostGame(self):
        print (self)
        print ("please input a valid number of column")
        while True:
            play = self.myInput('X')
            self.addMove(play, 'X')
            print (self)
            if self.winsFour('X'):
                print ("Player X wins.")
                break
            play = self.myInput('O')
            self.addMove(play, 'O')
            print (self)
            if self.winsFour('O'):
                print ("Player O wins.")
                break
            if self.ifFull():
                print ("Game is a tie.")
                break 
            
    def playGameWith(self, aiPlayer):
        print (self)
        print ("please input a valid number of column")
        while True:
            play = self.myInput('X')
            self.addMove(play, 'X')
            print (self)
            if self.winsFour('X'):
                print ("Player X wins.")
                break
            game = aiPlayer.nextMove(self)
            #play = self.myInput('O')
            self.addMove(game, 'O')
            print (self)
            if self.winsFour('O'):
                print ("Player O wins.")
                break
            if self.ifFull():
                print ("Game is a tie.")
                break         
    
class Player:
    def __init__(self, checker, ply):
            self.checker = checker
            self.ply = ply
            
    def nextMove(self,board):
        scores = self.scoresFor(board,self.checker,self.ply)
        #board.allowsMove(scores)
        best = max(scores)
        #for col in range(board.width):
         #   if best == scores[col]:
          #      return col
        bestmoves = []
        for m in scores:
            if m[0] == best[0]:
                bestmoves += [m]
        moves = random.choice(bestmoves)
        print moves,bestmoves
        return moves[1]
            
    def scoresFor(self,board,ox,depth):
        scoresList = []
        for col in range(board.width):
            if board.allowsMove(col):
                board.addMove(col, ox)
                if board.winsFour(ox):
                    scoresList += [[100.0,col]]
                elif depth < 1:
                    scoresList += [[50.0,col]]
                else:
                    if ox == 'X':
                        opponent = 'O'
                    else:
                        opponent = 'X'
                    opponentList = self.scoresFor(board,opponent,depth-1)
                    bestOpponent = max(opponentList)
                    invOpponentScore = 100.0 - bestOpponent[0]
                    scoresList+= [[invOpponentScore,col]]
                board.delMove(col)
            else:
                scoresList += [-1.0]
        return scoresList      
        
b = Board(7,6)
aiPlayer = Player('O', 3)
b.playGameWith(aiPlayer)
