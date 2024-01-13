import pygame
import sys
import numpy as np
import random
import copy

from constants import *


pygame.init()
screen =pygame.display.set_mode((width,height))
pygame.display.set_caption("Tic Tac Toe for ai project")
screen.fill(bgcolor)

class Board:
    def __init__(self):
        self.squares=np.zeros((rows,cols))
        self.emptysquares=self.squares
        self.marksquares=0
        
    def marksqare(self,row,col,player):
        self.squares[row][col]=player
        self.marksquares+=1
        
    def isemptysq(self,row,col):
        return self.squares[row][col]==0
    
    def isfull(self):
        return self.marksquares==9
    
    def isempty(self):
        return self.marksquares==0
    
    def getemptysqrs(self):
        emptysquares=[]
        for row in range(rows):
            for col in range(cols):
                if(self.isemptysq(row, col)):
                    emptysquares.append((row,col))
        return emptysquares
    
    def finalstate(self,show=False):
        for col in range(cols):
            if self.squares[0][col]==self.squares[1][col]==self.squares[2][col]!=0:
                if show:
                    if self.squares[0][col] ==2:
                         color=crossColor
                    else:
                        color=circleColor
                    winstartpos=(col*sqsize+int(sqsize/2),20)
                    winendpos=(col*sqsize+int(sqsize/2),height-20)
                    
                    pygame.draw.line(screen, color, winstartpos, winendpos,linewidth)
                return self.squares[0][col]
                
            
        for row in range(rows):
            if self.squares[row][0]==self.squares[row][1]==self.squares[row][2]!=0:
                if show:
                    if self.squares[row][0] ==2:
                         color=crossColor
                    else:
                        color=circleColor
                    winstartpos=(20,row*sqsize+int(sqsize/2))
                    winendpos=(width-20,row*sqsize+int(sqsize/2))
                    
                    pygame.draw.line(screen, color, winstartpos, winendpos,linewidth)
                return self.squares[row][0]
            
        if self.squares[0][0]==self.squares[1][1]==self.squares[2][2]!=0:
            if show:
                if self.squares[1][1] ==2:
                     color=crossColor
                else:
                    color=circleColor
                winstartpos=(20,20)
                winendpos=(width-20,height-20)
                
                pygame.draw.line(screen, color, winstartpos, winendpos,linewidth)
            return self.squares[1][1]
        
        if self.squares[2][0]==self.squares[1][1]==self.squares[0][2]!=0:
            if show:
                if self.squares[1][1] ==2:
                     color=crossColor
                else:
                    color=circleColor
                winstartpos=(20,height-20)
                winendpos=(width-20,20)
                
                pygame.draw.line(screen, color, winstartpos, winendpos,linewidth)
            return self.squares[1][1]
        
        return 0
    
    
class Ai:
    def __init__(self,level=1,player=2):
        self.level=level
        self.player=player
    
    def randomalgo(self,board):
        empty_squares=board.getemptysqrs()
        index=random.randrange(0,len(empty_squares))
        return empty_squares[index]
        
    def minimax(self,board,maximuizing):
        case=board.finalstate()
        
        if case==1:
            return 1,None
        
        if case==2:
            return -1,None
        
        elif board.isfull():
            return 0,None
        
        if maximuizing:
            max_eval=-10
            bestmove=None
            emptysquares=board.getemptysqrs()
            
            for(row,col) in emptysquares:#minimizing
                temp_board = copy.deepcopy(board)
                temp_board.marksqare(row, col, 1)
                eval=self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval=eval
                    bestmove=(row,col)
                    
            return max_eval,bestmove
        
        elif not maximuizing:
            min_eval=10
            bestmove=None
            emptysquares=board.getemptysqrs()
            
            for(row,col) in emptysquares:#minimizing
                temp_board = copy.deepcopy(board)
                temp_board.marksqare(row, col, self.player)
                eval=self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval=eval
                    bestmove=(row,col)
                    
            return min_eval,bestmove
        
    def eval(self,main_board):
        if self.level==0:
            move=self.randomalgo(main_board)
        else:
            eval,move=self.minimax(main_board,False)
            
        print(f'Ai choose to mark the square in {move} with an eval of {eval}')
        return move
    
class Game:
    def __init__(self):

        self.player=1
        self.gamemode='ai'
        self.ai=Ai()
        self.running=True
        self.board=Board()
        self.showlines()
        
    
    def showlines(self):
        screen.fill(bgcolor)
        
        #surface, color, start_pos, end_pos
        pygame.draw.line(screen, linecolor, (sqsize,0), (sqsize,height),linewidth)
        pygame.draw.line(screen, linecolor, (sqsize*2,0), (sqsize*2,height),linewidth)
        
        pygame.draw.line(screen, linecolor, (0,sqsize), (width,sqsize),linewidth)
        pygame.draw.line(screen, linecolor, (0,sqsize*2), (width,sqsize*2),linewidth)
        
    def makemove(self,row,col):
        self.board.marksqare(row, col, self.player)
        self.drawfig(row,col)
        self.nextturn()
    def nextturn(self):
        self.player=self.player%2 +1
        
    def drawfig(self,row,col):
        if self.player==1:
            center=(col*sqsize+int(sqsize/2),row*sqsize+int(sqsize/2))
            pygame.draw.circle(screen, circleColor, center, radius,circlewidth)
            
        elif self.player==2:
            #surface, color, center, radius,circlewidth
           
            start_pos1=(col*sqsize+offset,row*sqsize+offset)
            end_pos1=((col+1)*sqsize-offset,(row+1)*sqsize-offset)
            pygame.draw.line(screen, crossColor, start_pos1, end_pos1,crosswidth)
            
            start_pos2=(col*sqsize+offset,(row+1)*sqsize-offset)
            end_pos2=((col+1)*sqsize-offset,row*sqsize+offset)
            pygame.draw.line(screen, crossColor, start_pos2, end_pos2,crosswidth)
            
    def changegamemood(self):
        if self.gamemode=='pvp':
            self.gamemode='ai'
        else:
            self.gamemode = 'pvp'
            
    def reset(self):
        self.__init__()
        
    def isover(self):
        return self.board.finalstate(show=True)!=0 or self.board.isfull()
        
            
def main():
    game=Game()
    ai=game.ai
    board=game.board
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
             
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    game.changegamemood()
                 
                if event.key == pygame.K_r:
                    game.reset()
                    ai=game.ai
                    board=game.board 
                    
            if event.type ==pygame.MOUSEBUTTONDOWN:
                position=event.pos
                row=int(position[1]/sqsize)
                col=int(position[0]/sqsize)
                if board.isemptysq(row, col)and game.running:
                    game.makemove(row,col)
                    
                    if game.isover():
                        game.running=False
                        
                   
        if game.gamemode=='ai' and game.player == ai.player and game.running:
            pygame.display.update()
            row,col= ai.eval(board)
            game.makemove(row,col)
            if game.isover():
                game.running=False
            
        pygame.display.update()

main()
        