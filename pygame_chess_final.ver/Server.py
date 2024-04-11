from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import threading
import json
import uuid
import time
import random

port = 8888
EnableCS = True
ReadFlag = False
WriteFlag = False
ThreadRun = True

class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class ChessServer:

    users = []
    usernames = []
    rooms = []
    battles = []
  
    def __init__(self):
        self.reset_users_status()
        self.reset_rooms()
        self.reset_battles()
        self.load_users()
        if(EnableCS):
            self.lock = threading.Lock()
            
    def get_usernames_length(self):
        return len(self.usernames)
        
    def is_in_usernames(self, a_username):
        if a_username in self.usernames:
            return True
        else:
            return False
        
    def reset_users_status(self):
        self.load_users()
        for i in range(len(self.users)):
            self.users[i]["online_state"] = False
            self.users[i]["active_status"] = False
        self.save_users()
        
    def reset_rooms(self):
        self.save_rooms()
        
    def reset_battles(self):
        self.save_battles()
            
    def load_users(self):
        try:
            with open("assets/database/users.json", "r") as file:
                data = json.load(file)
                self.users = data["users"]
                self.usernames = data["usernames"]
        except FileNotFoundError as e:
            print("Error: %s" % e)
            self.users = []
            self.usernames = []
            exit(1)
            
    def save_users(self):
        data = {
            "usernames": self.usernames,
            "users": self.users
        }
        with open("assets/database/users.json", 'w') as file:
            json.dump(data, file)
            
    def save_rooms(self):
        data = {
            'rooms': self.rooms
        }
        with open("assets/database/rooms.json", 'w') as file:
            json.dump(data, file)
            
    def load_rooms(self):
        try:
            with open("assets/database/rooms.json", "r") as file:
                data = json.load(file)
                self.rooms = data["rooms"]
        except FileNotFoundError as e:
            print("Error: %s" % e)
            self.rooms = []
            exit(1)  
            
    def get_user_stats(self, a_user):
        if(EnableCS):
            with self.lock:
                self.load_users()
                a_index = self.usernames.index(a_user) 
                    
        return {"win": self.users[a_index]["win"], "lose": self.users[a_index]["lose"], "draw": self.users[a_index]["draw"]}
        
    def enter_opponent_room_index(self, a_opponent):
        for i in range(len(self.rooms)):
            if self.rooms[i]["user"] == a_opponent and self.rooms[i]["opponent"] == "":
                return i
        return -1
        
    def enter_opponent_room(self, a_opponent):
        if(EnableCS):
            with self.lock:
                self.load_rooms()
                a_index = self.enter_opponent_room_index(a_opponent)

        if a_index != -1:
            return self.rooms[a_index]
        else:
            return {}

    def get_opponent_room_index(self, a_opponent, user):
        for i in range(len(self.rooms)):
            if self.rooms[i]["user"] == a_opponent and self.rooms[i]["opponent"] == user:
                return i
        return -1

    def get_opponent_room(self, a_opponent, user):
        if (EnableCS):
            with self.lock:
                self.load_rooms()
                a_index = self.get_opponent_room_index(a_opponent, user)

        if a_index != -1:
            return self.rooms[a_index]
        else:
            return {}
    
    def get_user_room_index(self, user):
        for i in range(len(self.rooms)):
            if self.rooms[i]["user"] == user and not self.rooms[i]["game_state"]:
                return i
        return False

    def get_ready_room_index(self, user, opponent):
        for i in range(len(self.rooms)):
            if self.rooms[i]["user"] == user and self.rooms[i]["opponent"] == opponent and self.rooms[i]["game_state"]:
                return i
        return False

    def get_user_room(self, a_user):
        if(EnableCS):
            with self.lock:
                self.load_rooms()
                a_index = self.get_user_room_index(a_user)
        
        return self.rooms[a_index]

    def get_ready_room(self, a_user, a_opponent):
        if (EnableCS):
            with self.lock:
                self.load_rooms()
                a_index = self.get_ready_room_index(a_user, a_opponent)

        return self.rooms[a_index]
          
    def update_opponent(self, a_user, a_opponent):
        global WriteFlag
        if(EnableCS):
            while ReadFlag:
                pass
            WriteFlag = True
            with self.lock:
                self.load_rooms()
                a_index = self.get_user_room_index(a_user)
                self.rooms[a_index]["opponent"] = a_opponent
                self.save_rooms()
            WriteFlag = False
        return True
        
    def update_preparation(self, a_user):
        global WriteFlag
        if(EnableCS):
            while ReadFlag:
                pass
            WriteFlag = True
            with self.lock:
                self.load_rooms()
                a_index = self.get_user_room_index(a_user)
                self.rooms[a_index]["opponent_state"] = not self.rooms[a_index]["opponent_state"]
                self.save_rooms()
            WriteFlag = False
        return True
        
    def delete_opponent(self, a_user):
        global WriteFlag
        if(EnableCS):
            while ReadFlag:
                pass
            WriteFlag = True
            with self.lock:
                self.load_rooms()
                a_index = self.get_user_room_index(a_user)
                if not self.rooms[a_index]["game_state"]:
                    self.rooms[a_index]["opponent"] = ""
                self.save_rooms()
            WriteFlag = False
                
        return self.rooms
        
    def decide_color_for_random(self, a_user):
        global WriteFlag
        if(EnableCS):
            while ReadFlag:
                pass
            WriteFlag = True
            with self.lock:
                self.load_rooms()
                a_index = self.get_user_room_index(a_user)
                if random.random() % 2 == 0:
                    self.rooms[a_index]["color"] = "白色"
                else:
                    self.rooms[a_index]["color"] = "黑色"
                self.save_rooms()
            WriteFlag = False
                
        return self.rooms
            
    #register Start           
    def register(self, a_username, a_password):
        global WriteFlag
        if(EnableCS):
            while ReadFlag:
                pass
            WriteFlag = True
            with self.lock:
                self.usernames.append(a_username)
                self.users.append({"username": a_username, "password": a_password, "online_state": False, "online_status": 0, "active_status": False, "win": '0', "lose": '0', "draw": '0'})
                self.save_users()
            WriteFlag = False

        return True
    #register  End

    #login  Start
    def login(self, a_username, a_password):
        global WriteFlag
        if(EnableCS):
            while ReadFlag:
                pass
            WriteFlag = True
            with self.lock:
                self.load_users()
                index = self.usernames.index(a_username)
                if self.users[index]["password"] != a_password:
                    WriteFlag = False
                    return "密碼錯誤!"
                elif self.users[index]["online_state"]:
                    WriteFlag = False
                    return "該帳號已被其他使用者登入!"
                else:
                    self.users[index]["online_state"] = True
                    self.save_users()
            WriteFlag = False
        return "登入成功"
    #login  End

    def update_active_status(self, a_username):
        global WriteFlag
        if (EnableCS):
            while ReadFlag:
                pass
            WriteFlag = True
            with self.lock:
                index = self.usernames.index(a_username)
                if not self.users[index]["active_status"]:
                    self.users[index]["active_status"] = True
                else:
                    self.users[index]["active_status"] = False
                self.save_users()
            WriteFlag = False

    #logout Start
    def logout(self, a_username):
        global WriteFlag
        if(EnableCS):
            while ReadFlag:
                pass
            WriteFlag = True
            with self.lock:
                index = self.usernames.index(a_username)
                self.users[index]["online_state"] = False
                self.save_users()
            WriteFlag = False
        return True
    #logout End
    
    #update_online_status Start
    def update_online_status(self, a_username):
        global WriteFlag
        if(EnableCS):
            while ReadFlag :
                pass
            WriteFlag = True
            with self.lock:
                self.load_users()
                index = self.usernames.index(a_username)
                self.users[index]["online_status"] = 1
                self.save_users()
            WriteFlag = False
    #update_online_status End
    
    #create Start          
    def create(self, a_color, a_thought_time, a_extra_second, user, a_datetime):
        global WriteFlag
        if(EnableCS):
            while ReadFlag:
                pass
            WriteFlag = True
            with self.lock:
                self.rooms.append({"id": str(uuid.uuid4()), "color": a_color, "thought_time": a_thought_time, "extra_second": a_extra_second, "user": user, "datetime": a_datetime, "opponent": "", "opponent_state": False, "game_state": False})
                self.save_rooms()
            WriteFlag = False
        return True
    #create End
    
    #subject Start
    def subject(self):
        if(EnableCS):
            with self.lock:
                self.load_rooms()
                    
        return self.rooms
    #subject End
    
    #start Start
    def start(self, a_user):
        global WriteFlag
        if(EnableCS):
            while ReadFlag:
                pass
            WriteFlag = True
            with self.lock:
                self.load_rooms()
                a_index = self.get_user_room_index(a_user)
                self.rooms[a_index]["game_state"] = True
                self.save_rooms()
            WriteFlag = False

            with self.lock:
                self.load_battles()
                    
        return self.rooms
    #start End



    # delete_room Start
    def delete_room(self, a_room_user):
        global WriteFlag
        with self.lock:
            while ReadFlag:
                pass
            WriteFlag = True
            self.load_rooms()
            a_index = self.get_user_room_index(a_room_user)
            if not self.rooms[a_index]["game_state"]:
                del self.rooms[a_index]
            self.save_rooms()
            WriteFlag = False

    # delete_room End
    
    ######ChessFunction######
    
    #load_battles Start
    def load_battles(self):

        try:
            with open("assets/database/battles.json", "r") as file:
                data = json.load(file)
                self.battles = data["battles"]
        except FileNotFoundError as e:
            print("Error: %s" % e)
            self.battles = []
            exit(1)
    #load_battles End
    
    #save_battles Start
    def save_battles(self):

        data = {
            "battles": self.battles
        }
        with open("assets/database/battles.json", 'w') as file:
            json.dump(data, file)
    #save_battles End
    
    #create_battle_info Start
    def create_battle_info(self, a_room_id, a_white_player, a_black_player, a_thought_time):
        data = {
            "room_id": a_room_id,
            "white_player": a_white_player,
            "black_player": a_black_player,

            "turn_step": 3,
            "winner": "",
            "white_locations": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],
            "black_locations": [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)],
            "white_captured_pieces": -1,
            "black_captured_pieces": -1,
            "win_reason": 0,
            "check_draw_step": 0,
            "white_thought_time": int(a_thought_time.strip()) * 60,
            "black_thought_time": int(a_thought_time.strip()) * 60,
            "caller": "",  # 可能是白方或黑方
            "white_connect_status": 0,
            "black_connect_status": 0,
            "stay": 2
        }

        if(EnableCS):
            with self.lock:
                self.battles.append(data)
                self.save_battles()
        return True
    #create_battle_info End

    # get_battle_index Start
    def get_battle_index(self, a_room_id):
        for i in range(len(self.battles)):
            if self.battles[i]["room_id"] == a_room_id:
                return i
        return False
    # get_battle_index End

    #reset_turn_step Start
    def reset_turn_step(self, a_room_id):
        if(EnableCS):
            with self.lock:
                self.load_battles()
                a_index = self.get_battle_index(a_room_id)
                self.battles[a_index]["turn_step"] = 3
                self.save_battles()
        return True
    #reset_turn_step End

    # save_turn Start
    def save_turn(self, a_room_id, turn):
        if (EnableCS):
            with self.lock:
                self.load_battles()
                a_index = self.get_battle_index(a_room_id)
                self.battles[a_index]["turn_step"] = turn
                self.save_battles()
        return True
    # save_turn End

    # check_turn Start
    def check_turn(self, a_room_id, a_user):

        if (EnableCS):
            with self.lock:
                self.load_battles()
                a_index = self.get_battle_index(a_room_id)
                self.battles[a_index]["caller"] = a_user
            if self.battles[a_index]["caller"] == self.battles[a_index]["white_player"] and self.battles[a_index]["turn_step"] == 3:
                return "white"
            elif self.battles[a_index]["caller"] == self.battles[a_index]["black_player"] and self.battles[a_index]["turn_step"] == 0:
                return "black"
            else:
                return "not your turn"
    # check_turn End

    # check_white_location Start
    def check_white_location(self, a_room_id):
        with self.lock:
            self.load_battles()
            a_index = self.get_battle_index(a_room_id)

        return self.battles[a_index]["white_locations"]
    # check_white_location End

    # check_black_location Start
    def check_black_location(self, a_room_id):
        with self.lock:
            self.load_battles()
            a_index = self.get_battle_index(a_room_id)

        return self.battles[a_index]["black_locations"]
    # check_black_location End

    # check_captured_pieces Start
    def check_captured_pieces(self, a_room_id, a_user):
        with self.lock:
            self.load_battles()
            a_index = self.get_battle_index(a_room_id)
            self.battles[a_index]["caller"] = a_user

            if self.battles[a_index]["caller"] == self.battles[a_index]["white_player"]:
                print("Return captured pieces to white: " + str(self.battles[a_index]["white_captured_pieces"]))
                return self.battles[a_index]["black_captured_pieces"]
            if self.battles[a_index]["caller"] == self.battles[a_index]["black_player"]:
                return self.battles[a_index]["white_captured_pieces"]
    # check_captured_pieces End

    # reset_white_captured_pieces Start
    def reset_white_captured_pieces(self, a_room_id):
        with self.lock:
            self.load_battles()
            a_index = self.get_battle_index(a_room_id)
            self.battles[a_index]["black_captured_pieces"] = -1
            self.save_battles()
    # reset_white_captured_pieces End

    # reset_black_captured_pieces Start
    def reset_black_captured_pieces(self, a_room_id):
        with self.lock:
            self.load_battles()
            a_index = self.get_battle_index(a_room_id)
            self.battles[a_index]["white_captured_pieces"] = -1
            self.save_battles()
    # reset_black_captured_pieces End

    # save_winner Start
    def save_winner(self, a_room_id, a_winner):
        with self.lock:
            self.load_battles()
            a_index = self.get_battle_index(a_room_id)
            self.battles[a_index]["winner"] = a_winner
            self.save_battles()
    # save_winner End

    # save_win_reason Start
    def save_win_reason(self, a_room_id, a_win_reason_code):
        with self.lock:
            self.load_battles()
            a_index = self.get_battle_index(a_room_id)
            self.battles[a_index]["win_reason"] = a_win_reason_code
            self.save_battles()
    # save_win_reason End
    
    #check_winner Start
    def check_winner(self, a_room_id):
        with self.lock:
            self.load_battles()
            a_index = self.get_battle_index(a_room_id)
            
        return self.battles[a_index]["winner"]
    #check_winner End
    
    #check_win_reason Start
    def check_win_reason(self, a_room_id):
        with self.lock:
            self.load_battles()
            a_index = self.get_battle_index(a_room_id)

        return self.battles[a_index]["win_reason"]
    #check_win_reason End

    # save_white_captured_pieces Start
    def save_white_captured_pieces(self, a_room_id, a_black_piece):
        with self.lock:
            self.load_battles()
            a_index = self.get_battle_index(a_room_id)
            self.battles[a_index]["white_captured_pieces"] = a_black_piece
            self.save_battles()
    # save_white_captured_pieces End

    # save_black_captured_pieces Start
    def save_black_captured_pieces(self, a_room_id, a_white_piece):
        with self.lock:
            self.load_battles()
            a_index = self.get_battle_index(a_room_id)
            self.battles[a_index]["black_captured_pieces"] = a_white_piece
            print("Received black captured pieces from server: " + str(a_white_piece))
            self.save_battles()
    # save_black_captured_pieces End

    # reset_draw_step Start
    def reset_draw_step(self, a_room_id):
        with self.lock:
            self.load_battles()
            a_index = self.get_battle_index(a_room_id)
            self.battles[a_index]["check_draw_step"] = 0
            self.save_battles()
    # reset_draw_step End

    # add_draw_step Start
    def add_draw_step(self, a_room_id):
        with self.lock:
            self.load_battles()
            a_index = self.get_battle_index(a_room_id)
            self.battles[a_index]["check_draw_step"] += 1
            if self.battles[a_index]["check_draw_step"]== 30:
                self.battles[a_index]["winner"] = "draw"
            self.save_battles()
    # add_draw_step End

    # save_white_location Start
    def save_white_location(self, a_room_id, a_white_locations, a_color):
        if a_color == "black":
            with self.lock:
                self.load_battles()
                a_index = self.get_battle_index(a_room_id)
                self.battles[a_index]["white_locations"] = a_white_locations
                self.save_battles()
        else:
            for i in range(len(a_white_locations)):
                temp = list(a_white_locations[i])
                temp[0] = 7 - temp[0]
                temp[1] = 7 - temp[1]
                a_white_locations[i] = tuple(temp)
            with self.lock:
                self.load_battles()
                a_index = self.get_battle_index(a_room_id)
                self.battles[a_index]["white_locations"] = a_white_locations
                self.save_battles()
    # save_white_location End

    # save_black_location Start
    def save_black_location(self, a_room_id, a_black_locations, a_color):
        if a_color == "black":
            with self.lock:
                self.load_battles()
                a_index = self.get_battle_index(a_room_id)
                self.battles[a_index]["black_locations"] = a_black_locations
                self.save_battles()
        else:
            for i in range(len(a_black_locations)):
                temp = list(a_black_locations[i])
                temp[0] = 7 - temp[0]
                temp[1] = 7 - temp[1]
                a_black_locations[i] = tuple(temp)
            with self.lock:
                self.load_battles()
                a_index = self.get_battle_index(a_room_id)
                self.battles[a_index]["black_locations"] = a_black_locations
                self.save_battles()
    # save_black_location End

    # update_time Start
    def update_time(self, a_room_id, a_color, a_thought_time):
        with self.lock:
            self.load_battles()
            a_index = self.get_battle_index(a_room_id)
            if a_color == "white":
                self.battles[a_index]["white_thought_time"] = a_thought_time
            elif a_color == "black":
                self.battles[a_index]["black_thought_time"] = a_thought_time
            self.save_battles()
    # update_time End

    # get_time Start
    def get_time(self, a_room_id, a_color):
        with self.lock:
            self.load_battles()
            a_index = self.get_battle_index(a_room_id)
        if a_color == "white":
            return self.battles[a_index]["black_thought_time"]
        elif a_color == "black":
            return self.battles[a_index]["white_thought_time"]
    # get_time End

    # update_win Start
    def update_win(self, a_winner):
        global WriteFlag
        while(ReadFlag):
            pass
        WriteFlag = True
        with self.lock:
            self.load_users()
            a_index = self.usernames.index(a_winner)
            self.users[a_index]["win"] =  str(int(self.users[a_index]["win"]) + 1)
            self.save_users()
        WriteFlag = False
    # update_win End

    # update_draw Start
    def update_draw(self, a_drawer):
        global WriteFlag
        while(ReadFlag):
            pass
        WriteFlag = True
        with self.lock:
            self.load_users()
            a_index = self.usernames.index(a_drawer)
            self.users[a_index]["draw"] =  str(int(self.users[a_index]["draw"]) + 1)
            self.save_users()
        WriteFlag = False
    # update_draw End

    # update_lose Start
    def update_lose(self, a_loser):
        global WriteFlag
        while(ReadFlag):
            pass
        WriteFlag = True
        with self.lock:
            self.load_users()
            a_index = self.usernames.index(a_loser)
            self.users[a_index]["lose"] =  str(int(self.users[a_index]["lose"]) + 1)
            print(self.users[a_index]["username"], self.users[a_index]["lose"])
            self.save_users()
        WriteFlag = False
    # update_lose End

    # update_connect_status Start
    def update_connect_status(self, a_room_id, a_color):
        if a_color == "black":
            with self.lock:
                self.load_battles()
                a_index = self.get_battle_index(a_room_id)
                self.battles[a_index]["black_connect_status"] = 1
                self.save_battles()
        else:
            with self.lock:
                self.load_battles()
                a_index = self.get_battle_index(a_room_id)
                self.battles[a_index]["white_connect_status"] = 1
                self.save_battles()
    # update_connect_status End

    # check_opponent_status Start
    def check_opponent_status(self, a_room_id, a_color):
        if a_color == "black":
            with self.lock:
                self.load_battles()
                a_index = self.get_battle_index(a_room_id)
                if self.battles[a_index]["white_connect_status"] == 1:
                    self.battles[a_index]["white_connect_status"] = 0
                else:
                    self.battles[a_index]["winner"] = "black"
                    self.battles[a_index]["win_reason"] = 5
                self.save_battles()
        else:
            with self.lock:
                self.load_battles()
                a_index = self.get_battle_index(a_room_id)
                if self.battles[a_index]["black_connect_status"] == 1:
                    self.battles[a_index]["black_connect_status"] = 0
                else:
                    self.battles[a_index]["winner"] = "white"
                    self.battles[a_index]["win_reason"] = 5
                self.save_battles()
        # check_opponent_status End

    # exit_battle Start
    def exit_battle(self, a_room_id):
        with self.lock:
            self.load_battles()
            a_index = self.get_battle_index(a_room_id)
            self.battles[a_index]["stay"] -= 1
            if self.battles[a_index]["stay"] == 0:
                self.load_rooms()
                for i in range(len(self.rooms)):
                    if self.rooms[i]["id"] == self.battles[a_index]["room_id"]:
                        del self.rooms[i]
                        break
                self.save_rooms()
                del self.battles[a_index]
            self.save_battles()
    # exit_battle End
    
class CheckThread(threading.Thread):
    users = []
    usernames = []
    rooms = []
    battles = []
    
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.start()
        
    def load_users(self):
        try:
            with open("assets/database/users.json", "r") as file:
                data = json.load(file)
                self.users = data["users"]
                self.usernames = data["usernames"]
        except FileNotFoundError as e:
            print("Error: %s" % e)
            self.users = []
            self.usernames = []
            exit(1)
            
    def save_users(self):
        data = {
            "usernames": self.usernames,
            "users": self.users
        }
        with open("assets/database/users.json", 'w') as file:
            json.dump(data, file)
            
    def save_rooms(self):
        data = {
            'rooms': self.rooms
        }
        with open("assets/database/rooms.json", 'w') as file:
            json.dump(data, file)
            
    def load_rooms(self):
        try:
            with open("assets/database/rooms.json", "r") as file:
                data = json.load(file)
                self.rooms = data["rooms"]
        except FileNotFoundError as e:
            print("Error: %s" % e)
            self.rooms = []
            exit(1)
            
    #load_battles Start
    def load_battles(self):

        try:
            with open("assets/database/battles.json", "r") as file:
                data = json.load(file)
                self.battles = data["battles"]
        except FileNotFoundError as e:
            print("Error: %s" % e)
            self.battles = []
            exit(1)
    #load_battles End
    
    #save_battles Start
    def save_battles(self):

        data = {
            "battles": self.battles
        }
        with open("assets/database/battles.json", 'w') as file:
            json.dump(data, file)
    #save_battles End
            
    def check_online_status(self):
        self.load_users()
        print("Checking Status")
        
        for i in range(len(self.users)):

            if self.users[i]["online_status"] == 1 and self.users[i]["online_state"]:
                self.users[i]["online_status"] = 0
            elif self.users[i]["online_status"] == 0 and not self.users[i]["online_state"]:
                self.users[i]["active_status"] = False
            elif (self.users[i]["online_status"] == 0 and self.users[i]["online_state"]) or (self.users[i]["online_status"] == 1 and not self.users[i]["online_state"]):
                self.users[i]["online_state"] = False
                self.users[i]["online_status"] = 0
                if self.users[i]["active_status"]:
                    self.users[i]["active_status"] = False
                    room_index = -1
                    self.load_rooms()
                    for j in range (len(self.rooms)):
                        if self.rooms[j]["opponent"] == self.users[i]["username"] or self.rooms[j]["user"] == self.users[i]["username"]:
                            room_index = j

                    if room_index != -1:
                        if self.rooms[room_index]["opponent"] == self.users[i]["username"]:
                            if not self.rooms[room_index]["game_state"]:
                                self.rooms[room_index]["opponent"] = ""
                                self.rooms[room_index]["opponent_state"] = False
                            elif self.rooms[room_index]["game_state"]:
                                for k in range(len(self.users)):
                                    if self.rooms[room_index]["user"] == self.users[k]["username"]:
                                        if not self.users[k]["online_state"]:
                                            self.load_battles()
                                            for m in range(len(self.battles)):
                                                if self.rooms[room_index]["id"] == self.battles[m]["room_id"]:
                                                    del self.battles[m]
                                                    del self.rooms[room_index]
                                                    break
                                            self.save_battles()
                                            break
                                        elif self.users[k]["online_state"]:
                                            self.load_battles()
                                            for m in range(len(self.battles)):
                                                if self.rooms[room_index]["id"] == self.battles[m]["room_id"]:
                                                    self.battles[m]["stay"] -= 1
                                                    if self.battles[m]["stay"] == 0:
                                                        del self.battles[m]
                                                        del self.rooms[room_index]
                                                    break
                                            self.save_battles()
                                            break

                        elif self.rooms[room_index]["user"] == self.users[i]["username"]:
                            if not self.rooms[room_index]["game_state"]:
                                del self.rooms[room_index]
                            elif self.rooms[room_index]["game_state"]:
                                for k in range(len(self.users)):
                                    if self.rooms[room_index]["opponent"] == self.users[k]["username"]:
                                        if not self.users[k]["online_state"]:
                                            self.load_battles()
                                            for m in range(len(self.battles)):
                                                if self.rooms[room_index]["id"] == self.battles[m]["room_id"]:
                                                    del self.battles[m]
                                                    del self.rooms[room_index]
                                                    break
                                            self.save_battles()
                                            break
                                        elif self.users[k]["online_state"]:
                                            self.load_battles()
                                            for m in range(len(self.battles)):
                                                if self.rooms[room_index]["id"] == self.battles[m]["room_id"]:
                                                    self.battles[m]["stay"] -= 1
                                                    if self.battles[m]["stay"] == 0:
                                                        del self.battles[m]
                                                        del self.rooms[room_index]
                                                    break
                                            self.save_battles()
                                            break
                    self.save_rooms()
        self.save_users()

    def run(self):
        global ReadFlag
        
        while(ThreadRun):
            time.sleep(5)
            while(WriteFlag):
                pass
            ReadFlag = True
            self.check_online_status()
            ReadFlag = False

if __name__ == "__main__":
    chess_server = ChessServer()
    server = ThreadXMLRPCServer(("localhost", port), allow_none=True)
    server.register_instance(chess_server)
    childThread = CheckThread()
    try:
        print("使用Ctrl + c以退出...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("伺服器退出")
        ThreadRun = False