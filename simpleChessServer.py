from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import threading

PORT = 8888
EnableCS = True

class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class ChessFunction:
    
    turnStep = 3
    winner = ""
    whiteLocations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
    blackLocations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
    capturedPiecesWhite = 100
    capturedPiecesBlack = 100
    
    def __init__(self):
        self.sharedVariable = ""
        if(EnableCS):
            self.lock = threading.Lock()
    
    def ResetTurnStep(self):
        
        self.turnStep = 3
    #end of ResetTurnStep
    
    def SaveTurns(self, turn):
        
        self.turnStep = turn
    #end of SaveTurns
    
    def CheckTurns(self, username):
        
        if(EnableCS):
            self.lock.acquire()
            
            try:
                self.sharedVariable = username
                
                if self.sharedVariable == "whiteUser" and self.turnStep == 3:
                    return "white"
                elif self.sharedVariable == "blackUser" and self.turnStep == 0:
                    return "black"
                else:
                    return "not your turn"
            
            finally:
                self.lock.release()
        
    #end of CheckTurns
    
    def ResetWinner(self):
        
        self.winner = ""
    #end of ResetWinner
    
    def SaveWinner(self, winner):
        
        self.winner = winner
    #end of SaveWinner
    
    def CheckWinner(self):
        
        if self.winner == "white":
            return "white"
        elif self.winner == "black":
            return "black"
        else:
            return "no winner"
    #end of CheckWinner
    
    def ResetWhiteLocation(self):
        
        self.whiteLocations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
    #end of ResetWhiteLocation
        
    def ResetBlackLocation(self):
        
        self.blackLocations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
    #end of ResetBlackLocation
    
    def SaveWhiteLocation(self, clientWhiteLocation):
        
        self.whiteLocations = clientWhiteLocation
    #end of SaveWhiteLocation
    
    def SaveBlackLocation(self, clientBlackLocation):
        
        self.blackLocations = clientBlackLocation
    #end of SaveBlackLocation
    
    def CheckWhiteLocation(self):
        
        return self.whiteLocations
    #end of CheckWhiteLocation
    
    def CheckBlackLocation(self):
        
        return self.blackLocations
    #end of CheckBlackLocation
        
    def ResetCapturedPiecesWhite(self):
        
        self.capturedPiecesWhite = 100
    #end of ResetCapturedPiecesWhite
        
    def ResetCapturedPiecesBlack(self):
        
        self.capturedPiecesBlack = 100
    #end of ResetCapturedPiecesBlack
    
    def SaveCapturedPiecesWhite(self, whiteCaptured):
        
        self.capturedPiecesWhite = whiteCaptured
    #end of SaveCapturedPiecesWhite
    
    def SaveCapturedPiecesBlack(self, blackCaptured):
        
        self.capturedPiecesBlack = blackCaptured
    #end of SaveCapturedPiecesBlack
        
    def CheckCapturedPieces(self, username):
        
        if(EnableCS):
            self.lock.acquire()
            
            try:
                self.sharedVariable = username
                
                if self.sharedVariable == "whiteUser":
                    return self.capturedPiecesBlack
                if self.sharedVariable == "blackUser":
                    return self.capturedPiecesWhite
            
            finally:
                self.lock.release()
    #end of serverCheckCapturedPieces

def Main():
    obj = ChessFunction()
    server = ThreadXMLRPCServer(("localhost", PORT), allow_none=True)	
    server.register_instance(obj)
    print("Listen on port  %d" % PORT)
    try:
        print("Use Control-C to exit!")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server exit")
    
if __name__ == "__main__":
	Main()