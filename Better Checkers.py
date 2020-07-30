import copy
import random
import time
import pygame
import playsound

pygame.init()
screen=pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

class mainProgram:
    def __init__(self):
        self.Done = False
        self.Board = []
        self.BoardX = ''
        self.BoardY = ''
        self.BoardLineNum = ''
        self.BoardLine = []
        self.BoardLoop = 0
        self.ColNum = 0
        self.BoardCol = [(0,0,0), (255,255,255)]
        self.ColX = ''
        self.ColY = ''
        self.CheckerListX = ''
        self.CheckerlistY = ''
        self.Cursor = ''
        self.Pressed = ''
        self.ClickedCursorX = ''
        self.ClickedCursorY = ''
        self.CursorX = ''
        self.CursorY = ''
        self.SquareClicked = False
        self.TimeSincePressed = time.time()
        self.TimeSinceUnpressed = time.time()
        self.ClickedCursor = ''
        self.ColTurn = True
        self.ClickedPosX = ''
        self.ClickedPosY = ''
        self.PossibleMoves = []
        self.MoveWhiteLoop = ''
        self.TakeBlackLoop = ''
        self.CopyFix = ''
        self.MaxFPS = 0
        self.SavedType = ''
        self.RecusionStop = ''
        self.LoopThing = ''

        self.makeCheckers()
        print(self.Board)

        while not self.Done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Done = True
            screen.fill((0,0,0))
            self.drawBoard()
            self.drawCheckers()

            if not self.SquareClicked:
                self.mouseSquare()
                if time.time() - self.TimeSinceUnpressed > 0.5:
                    self.clicked()
                self.TimeSincePressed = time.time()
                    
            if self.SquareClicked:

                screen.blit(PressedSquare,(self.SavedCursor)) 
                self.canMove()   
                if time.time() - self.TimeSincePressed > 0.5:
                    self.unClicked()

                    self.takePiece()
                    
                self.TimeSinceUnpressed = time.time()
            pygame.display.update()
            clock.tick(100000)
            
            #print (clock.get_fps())
            #if clock.get_fps() > self.MaxFPS:
            #     self.MaxFPS = clock.get_fps()
            #     print
            #     print(self.MaxFPS)


        #playsound('Mario Kart.mp3')
        pygame.quit()
    def makeCheckers(self):
        #makes black checkers
        for self.BoardLineNum in range(3):
            if self.BoardLineNum == 1:
                for self.BoardLoop in range(4):
                    self.BoardLine.append(0)
                    self.BoardLine.append(1)
            else:
                for self.BoardLoop in range(4):
                    self.BoardLine.append(1)
                    self.BoardLine.append(0)
            self.Board.append(self.BoardLine)
            self.BoardLine = []

        #makes empty lines of board
        for self.BoardLineNum in range(2):
            self.Board.append([0, 0, 0, 0, 0, 0, 0, 0])
        #makes white checkers
        for self.BoardLineNum in range(3):
            if self.BoardLineNum != 1:
                for self.BoardLoop in range(4):
                    self.BoardLine.append(0)
                    self.BoardLine.append(2)
            else:
                for self.BoardLoop in range(4):
                    self.BoardLine.append(2)
                    self.BoardLine.append(0)
            self.Board.append(self.BoardLine)
            self.BoardLine = []
    def drawCheckers(self):
        for (self.CheckerListY, self.BoardY) in enumerate(self.Board):
            for (self.CheckerListX, self.BoardX) in enumerate(self.BoardY):
                if self.BoardX == 1 or self.BoardX == 3:
                    pygame.draw.circle(screen,(156,139, 86),((((self.CheckerListX)*75)+37.5),(((self.CheckerListY)*75)+37.5)),30)
                elif self.BoardX == 2 or self.BoardX == 4:
                    pygame.draw.circle(screen,(196,196,196),((((self.CheckerListX)*75)+37.5),(((self.CheckerListY)*75)+37.5)),30)
                if self.BoardX > 2:screen.blit(Crown,((self.CheckerListX*75), self.CheckerListY*75))

                    
    def drawBoard(self):
        #colours
        for self.ColY in range(8):
            #draws checker
            pygame.draw.rect(screen,(self.BoardCol[self.ColNum]),pygame.Rect(0,(self.ColY*75),75,75))
            for self.ColX in range(1, 8):
                #alternates colours
                if self.ColNum == 0:
                    self.ColNum += 1
                else:
                    self.ColNum -= 1
                #Draws checkers
                pygame.draw.rect(screen,(self.BoardCol[self.ColNum]),pygame.Rect((self.ColX*75),(self.ColY*75), 75, 75))          
    def mouseSquare(self):
        self.Cursor = (pygame.mouse.get_pos())
        self.CursorX = (round((self.Cursor[0] - 35)/75))* 75
        self.CursorY = (round((self.Cursor[1] - 35)/75))* 75
        screen.blit(Square,(self.CursorX, self.CursorY))
    def clicked(self):
        self.Pressed = pygame.mouse.get_pressed()
        if self.Pressed[0] == 1:
            self.ClickedCursorX = (round((self.Cursor[0] - 35)/75))
            self.ClickedCursorY = (round((self.Cursor[1] - 35)/75))
            if self.ClickedCursorY > 8: self.ClickedCursorY -= 1
            if self.ClickedCursorX > 8: self.ClickedCursorX -= 1
            if ((self.Board[self.ClickedCursorY][self.ClickedCursorX] == 2 or self.Board[self.ClickedCursorY][self.ClickedCursorX] == 4) and self.ColTurn == True) or ((self.Board[self.ClickedCursorY][self.ClickedCursorX] == 1 or self.Board[self.ClickedCursorY][self.ClickedCursorX] == 3) and self.ColTurn == False):
                self.SavedCursor = (self.CursorX,self.CursorY)
                self.SquareClicked = True
    def unClicked(self):
        self.Cursor = (pygame.mouse.get_pos())
        self.Pressed = pygame.mouse.get_pressed()
        self.ClickedPosX = (round((self.Cursor[0] - 35)/75))* 75
        self.ClickedPosY = (round((self.Cursor[1] - 35)/75))* 75
        if self.Pressed[0] == 1:
            if (self.ClickedPosX, self.ClickedPosY) == self.SavedCursor:
                self.SquareClicked = False
                return
        self.SquareClicked = True
    def canMove(self):
        self.SavedType = self.Board[self.ClickedCursorY][self.ClickedCursorX]
        if self.ColTurn:
            self.PossibleMoves = []
            try:
                if self.Board[self.ClickedCursorY-1][self.ClickedCursorX+1] == 0:
                    screen.blit(Highlight,((self.ClickedCursorX+1)*75, (self.ClickedCursorY-1)*75))
                    self.PossibleMoves.append(((self.ClickedCursorX+1), (self.ClickedCursorY-1)))
                elif self.Board[self.ClickedCursorY-1][self.ClickedCursorX+1] == 1 or self.Board[self.ClickedCursorY-1][self.ClickedCursorX+1] == 3:
                    self.multiHop((self.ClickedCursorY-2, self.ClickedCursorX+2), [(self.ClickedCursorY-1, self.ClickedCursorX+1)])
            except: print ('hello')

            try:
                if self.Board[self.ClickedCursorY-1][self.ClickedCursorX-1] == 0:
                    screen.blit(Highlight,((self.ClickedCursorX-1)*75, (self.ClickedCursorY-1)*75))
                    self.PossibleMoves.append(((self.ClickedCursorX-1), (self.ClickedCursorY-1)))

                elif self.Board[self.ClickedCursorY-1][self.ClickedCursorX-1] == 1 or self.Board[self.ClickedCursorY-1][self.ClickedCursorX-1] == 3:
                    self.multiHop((self.ClickedCursorY-2, self.ClickedCursorX-2), [(self.ClickedCursorY-1, self.ClickedCursorX-1)])
            except: print ('hi')

            if self.Board[self.ClickedCursorY][self.ClickedCursorX] == 4:
                try:
                    if self.Board[self.ClickedCursorY+1][self.ClickedCursorX+1] == 0:
                        screen.blit(Highlight,((self.ClickedCursorX+1)*75, (self.ClickedCursorY+1)*75))
                        self.PossibleMoves.append(((self.ClickedCursorX+1), (self.ClickedCursorY+1)))
                    elif self.Board[self.ClickedCursorY+1][self.ClickedCursorX+1] == 1 or self.Board[self.ClickedCursorY+1][self.ClickedCursorX+1] == 3:
                        self.Jumps = 0
                        self.multiHop((self.ClickedCursorY+2, self.ClickedCursorX+2), [(self.ClickedCursorY+1, self.ClickedCursorX+1)])
                except: pass

                try:
                    if self.Board[self.ClickedCursorY+1][self.ClickedCursorX-1] == 0:
                        screen.blit(Highlight,((self.ClickedCursorX-1)*75, (self.ClickedCursorY+1)*75))
                        self.PossibleMoves.append(((self.ClickedCursorX-1), (self.ClickedCursorY+1)))

                    elif self.Board[self.ClickedCursorY+1][self.ClickedCursorX-1] == 1 or self.Board[self.ClickedCursorY+1][self.ClickedCursorX-1] == 3:
                        self.Jumps = 0
                        self.multiHop((self.ClickedCursorY+2, self.ClickedCursorX-2), [(self.ClickedCursorY+1, self.ClickedCursorX-1)])
                except:pass   
                

        #black Pieces
        if not self.ColTurn:
            self.PossibleMoves = []
            try:
                if self.Board[self.ClickedCursorY+1][self.ClickedCursorX+1] == 0:
                    screen.blit(Highlight,((self.ClickedCursorX+1)*75, (self.ClickedCursorY+1)*75))
                    self.PossibleMoves.append(((self.ClickedCursorX+1), (self.ClickedCursorY+1)))
                elif self.Board[self.ClickedCursorY+1][self.ClickedCursorX+1] == 2 or self.Board[self.ClickedCursorY+1][self.ClickedCursorX+1] == 4:
                    self.Jumps = 0
                    self.multiHop((self.ClickedCursorY+2, self.ClickedCursorX+2), [(self.ClickedCursorY+1, self.ClickedCursorX+1)])
            except: pass

            try:
                if self.Board[self.ClickedCursorY+1][self.ClickedCursorX-1] == 0:
                    screen.blit(Highlight,((self.ClickedCursorX-1)*75, (self.ClickedCursorY+1)*75))
                    self.PossibleMoves.append(((self.ClickedCursorX-1), (self.ClickedCursorY+1)))

                elif self.Board[self.ClickedCursorY+1][self.ClickedCursorX-1] == 2 or self.Board[self.ClickedCursorY+1][self.ClickedCursorX-1] == 4:
                    self.Jumps = 0
                    self.multiHop((self.ClickedCursorY+2, self.ClickedCursorX-2), [(self.ClickedCursorY+1, self.ClickedCursorX-1)])
            except:pass     
            if self.Board[self.ClickedCursorY][self.ClickedCursorX] == 3:
                try:
                    if self.Board[self.ClickedCursorY-1][self.ClickedCursorX+1] == 0:
                        screen.blit(Highlight,((self.ClickedCursorX+1)*75, (self.ClickedCursorY-1)*75))
                        self.PossibleMoves.append(((self.ClickedCursorX+1), (self.ClickedCursorY-1)))
                    elif self.Board[self.ClickedCursorY-1][self.ClickedCursorX+1] == 2 or self.Board[self.ClickedCursorY-1][self.ClickedCursorX+1] == 4:
                        self.Jumps = 0
                        self.multiHop((self.ClickedCursorY-2, self.ClickedCursorX+2), [(self.ClickedCursorY-1, self.ClickedCursorX+1)])
                except: pass

                try:
                    if self.Board[self.ClickedCursorY-1][self.ClickedCursorX-1] == 0:
                        screen.blit(Highlight,((self.ClickedCursorX-1)*75, (self.ClickedCursorY-1)*75))
                        self.PossibleMoves.append(((self.ClickedCursorX-1), (self.ClickedCursorY-1)))

                    elif self.Board[self.ClickedCursorY-1][self.ClickedCursorX-1] == 2 or self.Board[self.ClickedCursorY-1][self.ClickedCursorX-1] == 4:
                        self.Jumps = 0
                        self.multiHop((self.ClickedCursorY-2, self.ClickedCursorX-2), [(self.ClickedCursorY-1, self.ClickedCursorX-1)])
                except:pass   
    def multiHop(self, DoubleHopPos, TakenCheckers):
        if self.ColTurn:
            if DoubleHopPos[0] < 8 and DoubleHopPos[0] > -1 and DoubleHopPos[1] < 8 and DoubleHopPos[1] > -1:
                if self.Board[(DoubleHopPos[0])][(DoubleHopPos[1])] == 0:
                    # for self.RecusionStop in self.PossibleMoves:
                    #     if len(self.RecusionStop) >= 2:
                    #         for self.LoopThing in range(1, len(self.RecusionStop)):
                    #             if self.RecusionStop[self.LoopThing] == self.takencheckers[-1]:
                    #                 return
                    screen.blit(Highlight,((DoubleHopPos[1])*75, (DoubleHopPos[0]*75)))
                    self.PossibleMoves.append(((DoubleHopPos[1]), (DoubleHopPos[0]), TakenCheckers))
                    self.CopyFix = copy.deepcopy(TakenCheckers)
                    try:
                        if self.Board[DoubleHopPos[0]-1][DoubleHopPos[1]+1] == 1:
                            self.CopyFix.append((DoubleHopPos[0]-1, DoubleHopPos[1]+1))
                            self.multiHop((DoubleHopPos[0]-2,DoubleHopPos[1]+2),self.CopyFix)    
                    except: pass
                    try:
                        if self.Board[DoubleHopPos[0]-1][DoubleHopPos[1]-1] == 1:
                            self.CopyFix.append((DoubleHopPos[0]-1, DoubleHopPos[1]-1))
                            self.multiHop((DoubleHopPos[0]-2,DoubleHopPos[1]-2), self.CopyFix)
                    except: pass
                    # if self.SavedType == 4:
                    #     try:
                    #         if self.Board[DoubleHopPos[0]+1][DoubleHopPos[1]+1] == 1:
                    #             self.CopyFix.append((DoubleHopPos[0]+1, DoubleHopPos[1]+1))
                    #             self.multiHop((DoubleHopPos[0]+2,DoubleHopPos[1]+2),self.CopyFix)    
                    #     except: pass
                    #     try:
                    #         self.CopyFix = copy.deepcopy(TakenCheckers)
                    #         if self.Board[DoubleHopPos[0]+1][DoubleHopPos[1]-1] == 1:
                    #             self.CopyFix.append((DoubleHopPos[0]+1, DoubleHopPos[1]-1))
                    #             self.multiHop((DoubleHopPos[0]+2,DoubleHopPos[1]-2), self.CopyFix)
                    #     except: pass
               
        elif not self.ColTurn:
            if DoubleHopPos[0] < 8 and DoubleHopPos[0] > -1 and DoubleHopPos[1] < 8 and DoubleHopPos[1] > -1:
                if self.Board[(DoubleHopPos[0])][(DoubleHopPos[1])] == 0:
                    screen.blit(Highlight,((DoubleHopPos[1])*75, (DoubleHopPos[0]*75)))
                    self.PossibleMoves.append(((DoubleHopPos[1]), (DoubleHopPos[0]), TakenCheckers))
                    self.CopyFix = copy.deepcopy(TakenCheckers)
                    try:
                        if self.Board[DoubleHopPos[0]+1][DoubleHopPos[1]+1] == 2:
                            self.CopyFix.append((DoubleHopPos[0]+1, DoubleHopPos[1]+1))
                            self.multiHop((DoubleHopPos[0]+2,DoubleHopPos[1]+2), self.CopyFix)
                        self.CopyFix = copy.deepcopy(TakenCheckers)
                    except: pass
                    try:
                        if self.Board[DoubleHopPos[0]+1][DoubleHopPos[1]-1] == 2:
                            self.CopyFix.append((DoubleHopPos[0]+1, DoubleHopPos[1]-1))
                            self.multiHop((DoubleHopPos[0]+2,DoubleHopPos[1]-2), self.CopyFix)
                    except: pass
        print (self.PossibleMoves)
    def takePiece(self):
        self.SavedType = self.Board[self.ClickedCursorY][self.ClickedCursorX]
        self.Pressed = pygame.mouse.get_pressed()
        self.Cursor = (pygame.mouse.get_pos())
        self.CursorX = (round((self.Cursor[0] - 35)/75))
        self.CursorY = (round((self.Cursor[1] - 35)/75))
        if self.Pressed[0] == 1:
            if self.ClickedCursorY > 8: self.ClickedCursorY -= 1
            if self.ClickedCursorX > 8: self.ClickedCursorX -= 1
            for self.MoveWhiteLoop in (self.PossibleMoves):
                if self.CursorY == self.MoveWhiteLoop[1] and self.CursorX == self.MoveWhiteLoop[0]:
                    if self.ColTurn:
                        if self.MoveWhiteLoop[1] == 0:
                            self.Board[self.MoveWhiteLoop[1]][self.MoveWhiteLoop[0]] = 4
                        else:
                            self.Board[self.MoveWhiteLoop[1]][self.MoveWhiteLoop[0]] = int(self.SavedType)

                            

                    else:
                        if self.MoveWhiteLoop[1] == 7:
                            self.Board[self.MoveWhiteLoop[1]][self.MoveWhiteLoop[0]] = 3
                        else:
                            self.Board[self.MoveWhiteLoop[1]][self.MoveWhiteLoop[0]] = int(self.SavedType)
                    self.Board[self.ClickedCursorY][self.ClickedCursorX] = 0
                    if len(self.MoveWhiteLoop) == 3:
                        for self.TakeBlackLoop in self.MoveWhiteLoop[2]:
                            print(self.TakeBlackLoop)
                            self.Board[self.TakeBlackLoop[0]][self.TakeBlackLoop[1]] = 0
                    self.Pressed = False
                    self.SquareClicked = False
                    if self.ColTurn:
                        self.ColTurn = False
                    else:
                        self.ColTurn = True
                    return


        
Square = pygame.image.load('Square.png').convert()
Square.set_colorkey((255,255,255))  
PressedSquare = pygame.image.load('Pressed.png').convert()
PressedSquare.set_colorkey((255,255,255)) 
Highlight = pygame.image.load('BlueSquare.png').convert()
Highlight.set_colorkey((255,255,255)) 
Crown = pygame.image.load('Crown.png').convert()
Crown.set_colorkey((255,255,255)) 

mainProgram()
