import sys
import pygame
import threading
import xmlrpc.client

PORT = 8888

class ChessThread(threading.Thread):
    
    def __init__(self, userColor):
        super().__init__()
        self.chessColor = userColor
        self.serverStoredTurn = 3
        self.serverStoredWinner = ""
        self.serverStoredWhiteLocations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
        self.serverStoredBlackLocations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
        self.serverStoredCapturedPiecesWhite = 100
        self.serverStoredCapturedPiecesBlack = 100
        self.start()
    #end of __init__
    
    def drawBoard(self):
        
        for i in range (32):
            column = i % 4
            row = i // 4
            if row % 2 == 0:
                pygame.draw.rect(self.gameScreen, "light gray", [600 - (column * 200), row * 100, 100, 100])
            else:
                pygame.draw.rect(self.gameScreen, "light gray", [700 - (column * 200), row * 100, 100, 100])
                
            pygame.draw.rect(self.gameScreen, "gray", [0, 800, 1000, 100])
            pygame.draw.rect(self.gameScreen, "gold", [0, 800, 1000, 100], 5)
            pygame.draw.rect(self.gameScreen, "gold", [800, 0, 200, 900], 5)
            statusText = ["White: Select a piece to move!", "White: Select a destination!", "Waiting player to move!", "Black: Select a piece to move!", "Black: Select a destination!"]
            self.gameScreen.blit(self.bigFont.render(statusText[self.turnStep], True, "black"), (20, 827))
            
            for i in range (9):
                pygame.draw.line(self.gameScreen, "black", (0, 100 * i), (800, 100 * i), 2)
                pygame.draw.line(self.gameScreen, "black", (100 * i, 0), (100 * i, 800), 2)
                
            self.gameScreen.blit(self.mediumFont.render("Surrender", True, "black"), (813, 833))
    #end of drawBoard
    
    def drawPieces(self):
        
        for i in range (len(self.whitePieces)):
            index = self.pieceList.index(self.whitePieces[i])
            self.gameScreen.blit(self.whiteImages[index], (self.whiteLocations[i][0] * 100 + 10, self.whiteLocations[i][1] * 100 + 10))
            
            if self.turnStep < 2:
                if self.selection == i:
                    pygame.draw.rect(self.gameScreen, "red", [self.whiteLocations[i][0] * 100 + 1, self.whiteLocations[i][1] * 100 + 1, 100, 100], 2)
                
        for i in range (len(self.blackPieces)):
            index = self.pieceList.index(self.blackPieces[i])
            self.gameScreen.blit(self.blackImages[index], (self.blackLocations[i][0] * 100 + 10, self.blackLocations[i][1] * 100 + 10))
            
            if self.turnStep >= 2:
                if self.selection == i:
                    pygame.draw.rect(self.gameScreen, "blue", [self.blackLocations[i][0] * 100 + 1, self.blackLocations[i][1] * 100 + 1, 100, 100], 2)
    #end of drawPieces
    
    def checkOptions(self, pieces, locations, turn):
        moveList = []
        allMoveList = []
        
        for i in range(len(pieces)):
            location = locations[i]
            piece = pieces[i]
            
            match piece:
                case "pawn":
                    moveList = self.checkPawnMoves(location, turn)
                case "rook":
                    moveList = self.checkRookMoves(location, turn)
                case "knight":
                    moveList = self.checkKnightMoves(location, turn)
                case "bishop":
                    moveList = self.checkBishopMoves(location, turn)
                case "king":
                    moveList = self.checkKingMoves(location, turn)
                case _:
                    moveList = self.checkQueenMoves(location, turn)
            
            allMoveList.append(moveList)
            
        return allMoveList
    #end of checkOptions
    
    def checkPawnMoves(self, position, color):
        moveList = []
        
        if color == "white":
            if (position[0], position[1] + 1) not in self.whiteLocations and (position[0], position[1] + 1) not in self.blackLocations and position[1] < 7:
                moveList.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in self.whiteLocations and (position[0], position[1] + 2) not in self.blackLocations and \
                (position[0], position[1] + 1) not in self.whiteLocations and (position[0], position[1] + 1) not in self.blackLocations and position[1] == 1:
                moveList.append((position[0], position[1] + 2))
            if (position[0] + 1, position[1] + 1) in self.blackLocations:
                moveList.append((position[0] + 1, position[1] + 1))
            if (position[0] - 1, position[1] + 1) in self.blackLocations:
                moveList.append((position[0] - 1, position[1] + 1))
        else:
            if (position[0], position[1] - 1) not in self.whiteLocations and (position[0], position[1] - 1) not in self.blackLocations and position[1] > 0:
                moveList.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in self.whiteLocations and (position[0], position[1] - 2) not in self.blackLocations and \
                (position[0], position[1] - 1) not in self.whiteLocations and (position[0], position[1] - 1) not in self.blackLocations and position[1] == 6:
                moveList.append((position[0], position[1] - 2))
            if (position[0] + 1, position[1] - 1) in self.whiteLocations:
                moveList.append((position[0] + 1, position[1] - 1))
            if (position[0] - 1, position[1] - 1) in self.whiteLocations:
                moveList.append((position[0] - 1, position[1] - 1))
                
        return moveList
    #end of checkPawnMoves
    
    def checkRookMoves(self, position, color):
        moveList = []
        
        if color == "white":
            enemyList = self.blackLocations
            friendList = self.whiteLocations
        else:
            enemyList = self.whiteLocations
            friendList = self.blackLocations
            
        for i in range (4):
            path = True
            chain = 1
            
            match i:
                case 0:
                    x = 0
                    y = 1
                case 1:
                    x = 0
                    y = -1
                case 2:
                    x = 1
                    y = 0
                case _:
                    x = -1
                    y = 0
                
            while path:
                
                if (position[0] + (chain * x), position[1] + (chain * y)) not in friendList and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                    moveList.append((position[0] + (chain * x), position[1] + (chain * y)))
                    
                    if (position[0] + (chain * x), position[1] + (chain * y)) in enemyList:
                        path = False
                        
                    chain += 1
                else:
                    path = False
                
        return moveList
    #end of checkRookMoves
    
    def checkKnightMoves(self, position, color):
        moveList = []
        
        if color == "white":
            friendList = self.whiteLocations
        else:
            friendList = self.blackLocations
            
        targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        
        for i in range (8):
            target = (position[0] + targets[i][0], position[1] + targets[i][1])
            
            if target not in friendList and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                moveList.append(target)
                
        return moveList
    #end of checkKnightMoves
    
    def checkBishopMoves(self, position, color):
        moveList = []
        
        if color == "white":
            enemyList = self.blackLocations
            friendList = self.whiteLocations
        else:
            enemyList = self.whiteLocations
            friendList = self.blackLocations
            
        for i in range (4):
            path = True
            chain = 1
            
            match i:
                case 0:
                    x = 1
                    y = -1
                case 1:
                    x = -1
                    y = -1
                case 2:
                    x = 1
                    y = 1
                case _:
                    x = -1
                    y = 1
                
            while path:
                
                if (position[0] + (chain * x), position[1] + (chain * y)) not in friendList and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                    moveList.append((position[0] + (chain * x), position[1] + (chain * y)))
                    
                    if (position[0] + (chain * x), position[1] + (chain * y)) in enemyList:
                        path = False
                        
                    chain += 1
                else:
                    path = False
        
        return moveList
    #end of checkBishopMoves
    
    def checkKingMoves(self, position, color):
        moveList = []
        
        if color == "white":
            friendList = self.whiteLocations
        else:
            friendList = self.blackLocations
            
        targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
        
        for i in range (8):
            target = (position[0] + targets[i][0], position[1] + targets[i][1])
            
            if target not in friendList and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                moveList.append(target)
        
        return moveList
    #end of checkKingMoves
    
    def checkQueenMoves(self, position, color):
        moveList = self.checkBishopMoves(position, color)
        secondList = self.checkRookMoves(position, color)
        
        for i in range (len(secondList)):
            moveList.append(secondList[i])
        
        return moveList
    #end of checkQueenMoves
    
    def checkValidMoves(self):
        
        if self.turnStep < 2:
            optionsList = self.whiteOptions
        else:
            optionsList = self.blackOptions
        
        validOptions = optionsList[self.selection]
        
        return validOptions
    #end of checkValidMoves

    def serverResetStoredTurns(self):
        
        self.serverStoredTurn = 3
    #end of serverResetStoredTurns
    
    def serverSaveTurns(self, turn):
        
        self.serverStoredTurn = turn
    #end of serverSaveTurns
    
    def serverCheckTurns(self): #通常情況client必須發送username，但是爲了單機測試這裏就不寫
        
        if self.serverStoredTurn == 3:
            return "white"
        elif self.serverStoredTurn == 0:
            return "black"
        else:
            return "not your turn"
    #end of serverCheckTurns
    
    def serverResetStoredWinner(self):
        
        self.serverStoredWinner = ""
    #end of serverResetStoredTurns
    
    def serverSaveWinner(self, winner):
        
        self.serverStoredWinner = winner
    #end of serverSaveTurns
    
    def serverCheckWinner(self):
        
        if self.serverStoredWinner == "white":
            return "white"
        elif self.serverStoredWinner == "black":
            return "black"
        else:
            return "no winner"
    #end of serverCheckWinner
    
    def serverResetWhiteLocation(self):
        
        self.serverStoredWhiteLocations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
    #end of serverResetWhiteLocation
        
    def serverResetBlackLocation(self):
        
        self.serverStoredBlackLocations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
    #end of serverResetBlackLocation
        
    def serverResetCapturedPiecesWhite(self):
        
        self.serverStoredCapturedPiecesWhite = 100
    #end of serverResetCapturedPiecesWhite
        
    def serverResetCapturedPiecesBlack(self):
        
        self.serverStoredCapturedPiecesBlack = 100
    #end of serverResetCapturedPiecesBlack
    
    def serverSaveWhiteLocation(self, clientWhiteLocation):
        
        self.serverStoredWhiteLocations = clientWhiteLocation
    #end of serverSaveWhiteLocation
    
    def serverSaveBlackLocation(self, clientBlackLocation):
        
        self.serverStoredBlackLocations = clientBlackLocation
    #end of serverSaveBlackLocation
    
    def serverSaveCapturedPiecesWhite(self, whiteCaptured):
        
        self.serverStoredCapturedPiecesWhite = whiteCaptured
    #end of serverSaveCapturedPiecesWhite
    
    def serverSaveCapturedPiecesBlack(self, blackCaptured):
        
        self.serverStoredCapturedPiecesBlack = blackCaptured
    #end of serverSaveCapturedPiecesBlack
    
    def serverCheckWhiteLocation(self):
        
        return self.serverStoredWhiteLocations
    #end of serverCheckWhiteLocation
    
    def serverCheckBlackLocation(self):
        
        return self.serverStoredBlackLocations
    #end of serverCheckBlackLocation
        
    def serverCheckCapturedPieces(self): #通常情況client必須發送username，但是爲了單機測試這裏就不寫
    
        #if username == "whiteUser":
            return self.serverStoredCapturedPiecesBlack
        #if username == "blackUser":
            return self.serverStoredCapturedPiecesWhite
    #end of serverCheckCapturedPieces
    
    def drawValid(self, moves):
        
        if self.turnStep < 2:
            color = "red"
        else:
            color = "blue"
        
        for i in range (len(moves)):
            pygame.draw.circle(self.gameScreen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)
    #end of drawValid
    
    def drawCaptured(self):
        
        for i in range (len(self.capturedPiecesWhite)):
            capturedPiece = self.capturedPiecesWhite[i]
            index = self.pieceList.index(capturedPiece)
            self.gameScreen.blit(self.blackImagesSmall[index], (825, 5 + 50 * i))
            
        for i in range (len(self.capturedPiecesBlack)):
            capturedPiece = self.capturedPiecesBlack[i]
            index = self.pieceList.index(capturedPiece)
            self.gameScreen.blit(self.whiteImagesSmall[index], (925, 5 + 50 * i))
    #end of drawCaptured
    
    def drawCheck(self):
        
        if "king" in self.whitePieces:
            kingIndex = self.whitePieces.index("king")
            kingLocation = self.whiteLocations[kingIndex]
            
            for i in range (len(self.blackOptions)):
                if kingLocation in self.blackOptions[i]:
                    if self.counter < 15:
                        pygame.draw.rect(self.gameScreen, "dark red", [self.whiteLocations[kingIndex][0] * 100 + 1, self.whiteLocations[kingIndex][1] * 100 + 1, 100, 100], 5)

        if "king" in self.blackPieces:
            kingIndex = self.blackPieces.index("king")
            kingLocation = self.blackLocations[kingIndex]
                
            for i in range (len(self.whiteOptions)):
                if kingLocation in self.whiteOptions[i]:
                    if self.counter < 15:
                        pygame.draw.rect(self.gameScreen, "dark blue", [self.blackLocations[kingIndex][0] * 100 + 1, self.blackLocations[kingIndex][1] * 100 + 1, 100, 100], 5)
    #end of drawCheck
    
    def drawGameOver(self):
        pygame.draw.rect(self.gameScreen, "black", [200, 200, 400, 70])
        self.gameScreen.blit(self.font.render(f'{self.winner} won the game!', True, "white"), (210, 210))
        self.gameScreen.blit(self.font.render("Press enter to replay!", True, "white"), (210, 240))
    #end of drawGameOver
    
    def run(self):
        pygame.init()
        self.gameScreen = pygame.display.set_mode([1000,900])
        pygame.display.set_caption("網路程式設計專題")
        self.pygameIcon = pygame.image.load("assets/images/black_queen.png")
        pygame.display.set_icon(self.pygameIcon)
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.bigFont = pygame.font.Font("freesansbold.ttf", 50)
        self.mediumFont = pygame.font.Font("freesansbold.ttf", 35)
        self.timer = pygame.time.Clock()
        self.counter = 0
        self.fps = 60
        self.winner = ""
        self.gameOver = False
        
        self.whitePieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
        self.whiteLocations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
        self.blackPieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
        self.blackLocations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
        self.capturedPiecesWhite = []
        self.capturedPiecesBlack = []
        self.turnStep = 2
        self.selection = 100
        self.validMoves = []
        self.returnCheck = "not your turn"
        
        self.whiteQueen = pygame.transform.scale(pygame.image.load("assets/images/white_queen.png"), (80, 80))
        self.whiteQueenSmall = pygame.transform.scale(self.whiteQueen, (45, 45))
        self.whiteKing = pygame.transform.scale(pygame.image.load("assets/images/white_king.png"), (80, 80))
        self.whiteKingSmall = pygame.transform.scale(self.whiteKing, (45, 45))
        self.whiteRook = pygame.transform.scale(pygame.image.load("assets/images/white_rook.png"), (80, 80))
        self.whiteRookSmall = pygame.transform.scale(self.whiteRook, (45, 45))
        self.whiteKnight = pygame.transform.scale(pygame.image.load("assets/images/white_knight.png"), (80, 80))
        self.whiteKnightSmall = pygame.transform.scale(self.whiteKnight, (45, 45))
        self.whiteBishop = pygame.transform.scale(pygame.image.load("assets/images/white_bishop.png"), (80, 80))
        self.whiteBishopSmall = pygame.transform.scale(self.whiteBishop, (45, 45))
        self.whitePawn = pygame.transform.scale(pygame.image.load("assets/images/white_pawn.png"), (80, 80))   
        self.whitePawnSmall = pygame.transform.scale(self.whitePawn, (45, 45))
        
        self.blackQueen = pygame.transform.scale(pygame.image.load("assets/images/black_queen.png"), (80, 80))
        self.blackQueenSmall = pygame.transform.scale(self.blackQueen, (45, 45))
        self.blackKing = pygame.transform.scale(pygame.image.load("assets/images/black_king.png"), (80, 80))
        self.blackKingSmall = pygame.transform.scale(self.blackKing, (45, 45))
        self.blackRook = pygame.transform.scale(pygame.image.load("assets/images/black_rook.png"), (80, 80))
        self.blackRookSmall = pygame.transform.scale(self.blackRook, (45, 45))
        self.blackKnight = pygame.transform.scale(pygame.image.load("assets/images/black_knight.png"), (80, 80))
        self.blackKnightSmall = pygame.transform.scale(self.blackKnight, (45, 45))
        self.blackBishop = pygame.transform.scale(pygame.image.load("assets/images/black_bishop.png"), (80, 80))
        self.blackBishopSmall = pygame.transform.scale(self.blackBishop, (45, 45))
        self.blackPawn = pygame.transform.scale(pygame.image.load("assets/images/black_pawn.png"), (80, 80))
        self.blackPawnSmall = pygame.transform.scale(self.blackPawn, (45, 45))
        
        self.whiteImages = [self.whitePawn, self.whiteQueen, self.whiteKing, self.whiteKnight, self.whiteRook, self.whiteBishop]
        self.whiteImagesSmall = [self.whitePawnSmall, self.whiteQueenSmall, self.whiteKingSmall, self.whiteKnightSmall, self.whiteRookSmall, self.whiteBishopSmall]
        self.blackImages = [self.blackPawn, self.blackQueen, self.blackKing, self.blackKnight, self.blackRook, self.blackBishop]
        self.blackImagesSmall = [self.blackPawnSmall, self.blackQueenSmall, self.blackKingSmall, self.blackKnightSmall, self.blackRookSmall, self.blackBishopSmall]
        
        self.blackOptions = self.checkOptions(self.blackPieces, self.blackLocations, "black")
        self.whiteOptions = self.checkOptions(self.whitePieces, self.whiteLocations, "white")
        
        self.pieceList = ["pawn", "queen", "king", "knight", "rook", "bishop"]
        self.running = True
        
        while(self.running):
            self.timer.tick(self.fps)
            
            if self.counter < 30:
                self.counter += 1
            else:
                self.counter = 0
                
            self.gameScreen.fill("dark gray")
            self.drawBoard()
            self.drawPieces()
            self.drawCaptured()
            self.drawCheck()
            
            if self.selection != 100:
                self.validMoves = self.checkValidMoves()
                self.drawValid(self.validMoves)
                
            if self.turnStep == 2:
                self.whiteLocations = self.serverCheckWhiteLocation()
                self.blackLocations = self.serverCheckBlackLocation()
                self.updatedCapturedPieces = self.serverCheckCapturedPieces()
                self.returnCheck = self.serverCheckTurns()
            
            if self.updatedCapturedPieces != 100 and self.chessColor == "white":
                self.capturedPiecesBlack.append(self.whitePieces[self.updatedCapturedPieces])
                self.whitePieces.pop(self.updatedCapturedPieces)
                self.serverResetCapturedPiecesBlack()
            elif self.updatedCapturedPieces != 100 and self.chessColor == "black":
                self.capturedPiecesWhite.append(self.blackPieces[self.updatedCapturedPieces])
                self.blackPieces.pop(self.updatedCapturedPieces)
                self.serverResetCapturedPiecesWhite() 
                
            self.blackOptions = self.checkOptions(self.blackPieces, self.blackLocations, "black")
            self.whiteOptions = self.checkOptions(self.whitePieces, self.whiteLocations, "white")
                
            if self.returnCheck == "white":
                self.turnStep = 0
            elif self.returnCheck == "black":
                self.turnStep = 3
                
            if self.winner == "":
                self.returnWinCheck = self.serverCheckWinner()
                
            if self.returnWinCheck == "white":
                self.winner = "white"
            elif self.returnWinCheck == "black":
                self.winner = "black"
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.gameOver:
                    xCord = event.pos[0] // 100
                    yCord = event.pos[1] // 100
                    clickCords = (xCord, yCord)
                    if self.turnStep <= 1:
                        if clickCords == (8, 8) or clickCords == (9, 8):
                            self.winner = "black"
                            self.serverSaveWinner("black")
                        if clickCords in self.whiteLocations:
                            self.selection = self.whiteLocations.index(clickCords)
                            if self.turnStep == 0:
                                self.turnStep = 1
                        if clickCords in self.validMoves and self.selection != 100:
                            self.whiteLocations[self.selection] = clickCords
                            if clickCords in self.blackLocations:
                                blackPiece = self.blackLocations.index(clickCords)
                                self.capturedPiecesWhite.append(self.blackPieces[blackPiece])
                                self.serverSaveCapturedPiecesWhite(blackPiece)
                                if self.blackPieces[blackPiece] == "king":
                                    self.winner = "white"
                                    self.serverSaveWinner("white")
                                self.blackPieces.pop(blackPiece)
                                self.blackLocations.pop(blackPiece)
                            self.serverSaveWhiteLocation(self.whiteLocations)
                            self.serverSaveBlackLocation(self.blackLocations)
                            self.blackOptions = self.checkOptions(self.blackPieces, self.blackLocations, "black")
                            self.whiteOptions = self.checkOptions(self.whitePieces, self.whiteLocations, "white")
                            self.serverSaveTurns(self.turnStep)
                            self.turnStep = 2
                            self.selection = 100
                            self.validMoves = []
                    
                    if self.turnStep > 2:
                        if clickCords == (8, 8) or clickCords == (9, 8):
                            self.winner = "white"
                            self.serverSaveWinner("white")
                        if clickCords in self.blackLocations:
                            self.selection = self.blackLocations.index(clickCords)
                            if self.turnStep == 3:
                                self.turnStep = 4
                        if clickCords in self.validMoves and self.selection != 100:
                            self.blackLocations[self.selection] = clickCords
                            if clickCords in self.whiteLocations:
                                whitePiece = self.whiteLocations.index(clickCords)
                                self.capturedPiecesBlack.append(self.whitePieces[whitePiece])
                                self.serverSaveCapturedPiecesBlack(whitePiece)
                                if self.whitePieces[whitePiece] == "king":
                                    self.winner = "black"
                                    self.serverSaveWinner("black")
                                self.whitePieces.pop(whitePiece)
                                self.whiteLocations.pop(whitePiece)
                            self.serverSaveBlackLocation(self.blackLocations)
                            self.serverSaveWhiteLocation(self.whiteLocations)
                            self.blackOptions = self.checkOptions(self.blackPieces, self.blackLocations, "black")
                            self.whiteOptions = self.checkOptions(self.whitePieces, self.whiteLocations, "white")
                            self.serverSaveTurns(self.turnStep)
                            self.turnStep = 2
                            self.selection = 100
                            self.validMoves = []
                            
                if event.type == pygame.KEYDOWN and self.gameOver:
                    if event.key == pygame.K_RETURN:
                        self.gameOver = False
                        self.winner = ""
                        self.whitePieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
                        self.whiteLocations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                        self.blackPieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
                        self.blackLocations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                        self.capturedPiecesWhite = []
                        self.capturedPiecesBlack = []
                        self.turnStep = 2
                        self.selection = 100
                        self.validMoves = []
                        self.blackOptions = self.checkOptions(self.blackPieces, self.blackLocations, "black")
                        self.whiteOptions = self.checkOptions(self.whitePieces, self.whiteLocations, "white")
                        self.serverResetStoredTurns()
                        self.serverResetStoredWinner()
                        self.serverResetWhiteLocation()
                        self.serverResetBlackLocation()
                            
            if self.winner != "":
                self.gameOver = True
                self.drawGameOver()
                    
            pygame.display.flip()
        pygame.quit()
    #end of run
#end of ChessThread

def Main():
    chessColor = "white"
    gameThread = ChessThread(chessColor)
#end of Main

if __name__ == '__main__':
    Main()