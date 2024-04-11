# 默認預設值為 -1

import xmlrpc.client
import datetime
import unicodedata
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import pygame
from PIL import Image, ImageTk

w = None
game = None
port = 8888
user = None
opponent = None
room = False
battle = False
rooms = []


class window():
    refresh_lobby_flag = False
    update_opponent_flag = False
    check_start_flag = False

    login_window = None
    register_window = None

    lobby = None
    l_frame = None
    l_title_label = None
    l_room_box = None
    reset_button = None
    logout_button = None
    create_button = None

    create_window = None

    room_window = None
    rule_label = None
    versus_label = None
    black_image = None
    white_image = None
    random_image = None
    black_label = None
    white_label = None
    random1_label = None
    random2_label = None
    player1_label = None
    player2_label = None
    player1_stats_label = None
    player2_stats_label = None
    exit_button = None

    preparation_button = None
    preparation_label = None
    preparation_frame = None

    start_button = None

    def __init__(self):
        super().__init__()
        self.open_login_window()

    def refresh_lobby(self):
        if self.refresh_lobby_flag == True:
            print("Refreshing lobby...")
            self.w_subject()
            if self.refresh_lobby_flag == True:
                self.lobby.after(1000, self.refresh_lobby)
        else:
            print("Stop refreshing lobby!")

    def display_message(self, msg, position):
        position.config(state=tk.NORMAL)
        position.delete(1.0, tk.END)
        position.insert(tk.END, msg)
        position.config(state=tk.DISABLED)

    def open_login_window(self):


        self.login_window = tk.Tk()
        self.login_window.title("登入")

        window_width = 350
        window_height = 250

        screen_width = self.login_window .winfo_screenwidth()
        screen_height = self.login_window .winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2


        self.login_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.login_window.resizable(False, False)

        username_label = tk.Label(self.login_window, text="用戶名:")
        username_label.pack()
        username_entry = tk.Entry(self.login_window)
        username_entry.pack()

        password_label = tk.Label(self.login_window, text="密碼:")
        password_label.pack()
        password_entry = tk.Entry(self.login_window, show="*")
        password_entry.pack()

        login_button = tk.Button(self.login_window, text="確定登入", command=lambda : self.w_login(username_entry.get(), password_entry.get(), message_text))
        login_button.pack(pady=20)


        message_label = tk.Label(self.login_window, text="提示訊息:")
        message_label.pack(pady=10)

        message_text = tk.Text(self.login_window, height=1, width=30)
        message_text.pack()
        message_text.config(state=tk.DISABLED)


        register_button = tk.Button(self.login_window, text="註冊", command=self.open_register_window)
        register_button.pack(pady=5)




    def w_login(self, a_username, a_password, a_position):
            global user

            if len(a_username) == 0:
                msg = "請輸入使用者名稱"
                self.display_message(msg, a_position)
                return

            if len(a_password) == 0:
                msg = "請輸入密碼"
                self.display_message(msg, a_position)
                return

            try:
                if not server.is_in_usernames(a_username):
                    msg = "不存在該使用者"
                    self.display_message(msg, a_position)
                    return
            except ConnectionRefusedError:
                messagebox.showinfo("提示", "無法連接伺服器，請稍後重新登入！")
                return

            try:
                msg = server.login(a_username, a_password)
            except ConnectionRefusedError:
                messagebox.showinfo("提示", "無法連接伺服器，請稍後重新登入！")
                return
            if msg == "登入成功":
                user = a_username
                self.login_window.destroy()
                self.open_lobby_window()
            else:
                self.display_message(msg, a_position)

    def open_register_window(self):

        self.register_window = tk.Toplevel(self.login_window)
        self.register_window.title("註冊")

        window_width = 350
        window_height = 250

        screen_width = self.register_window .winfo_screenwidth()
        screen_height = self.register_window .winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2


        self.register_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.register_window.resizable(False, False)


        username_label = tk.Label(self.register_window, text="用戶名(至多為16個字元):")
        username_label.pack()
        username_entry = tk.Entry(self.register_window)
        username_entry.pack()

        password_label = tk.Label(self.register_window, text="密碼:")
        password_label.pack()
        password_entry = tk.Entry(self.register_window, show="*")
        password_entry.pack()

        register_button = tk.Button(self.register_window, text="確定註冊", command=lambda : self.w_register(username_entry.get(), password_entry.get(), message_text))
        register_button.pack(pady=20)

        message_label = tk.Label(self.register_window, text="提示訊息:")
        message_label.pack(pady=10)

        message_text = tk.Text(self.register_window, height=1, width=40)
        message_text.pack()
        message_text.config(state=tk.DISABLED)

    def w_register(self, a_username, a_password, a_position):

        if len(a_username) == 0:
            msg = "請輸入使用者名稱"
            self.display_message(msg, a_position)
            return

        if not a_username.isalnum():
            msg = "使用者名稱只限輸入中文或字母或數字"
            self.display_message(msg, a_position)
            return

        if len(a_username) > 8:
           msg = "使用者名稱至多為8個字元"
           self.display_message(msg, a_position)
           return

        try:
            check_username = server.is_in_usernames(a_username)
        except ConnectionRefusedError:
            messagebox.showinfo("提示", "無法連接伺服器，請稍後重新注冊！")
            return

        if not check_username:

            if len(a_password) == 0:
                msg = "請輸入密碼"
                self.display_message(msg, a_position)
                return


            if len(a_password) < 8:
                msg = "密碼至少為8個字元"
                self.display_message(msg, a_position)
                return
            elif len(a_password) > 16:
                msg = "密碼至多為16個字元"
                self.display_message(msg, a_position)
                return

            try:
                server.register(a_username, a_password)
            except ConnectionRefusedError:
                messagebox.showinfo("提示", "無法連接伺服器，請稍後重新注冊！")
                return
            msg = "註冊成功!"
            messagebox.showinfo("提示", msg)
            self.register_window.destroy()
            return
        else:
            msg = "該使用者名稱已經被註冊"
            self.display_message(msg, a_position)
            return

    def open_lobby_window(self):

        global user
        self.refresh_lobby_flag = True
        self.lobby = tk.Tk()
        self.lobby.title("大廳")

        window_width = 950
        window_height = 500

        screen_width = self.lobby.winfo_screenwidth()
        screen_height = self.lobby.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.lobby.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.lobby.resizable(False, False)

        self.l_frame = tk.Frame(self.lobby)
        self.l_frame.pack(padx=10, pady=10)

        self.l_title_label = tk.Label(self.l_frame, text=f"您好! {user}", font=("Helvetica", 12, "bold"))
        self.l_title_label.pack()


        self.reset_button = tk.Button(self.l_frame, text="重新整理", command=self.refresh_lobby)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.logout_button = tk.Button(self.l_frame, text="登出", command=self.w_logout)
        self.logout_button.pack(side=tk.LEFT)

        self.l_room_box = scrolledtext.ScrolledText(self.lobby, wrap=tk.NONE, width=300, height=22)
        self.l_room_box.pack(padx=10, pady=0)

        self.create_button = tk.Button(self.lobby, text="建立房間", command=self.open_create_window)
        self.create_button.pack(pady=10)

        self.message_label = tk.Label(self.lobby, text="提示訊息:")
        self.message_label.pack(pady=10)

        self.message_text = tk.Text(self.lobby, height=1, width=100)
        self.message_text.pack()
        self.message_text.config(state=tk.DISABLED)

        self.w_subject()
        self.refresh_lobby()


    def w_logout(self):

        global user
        try:
            server.logout(user)
        except ConnectionRefusedError:
            messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
            self.lobby.destroy()
            w.open_lobby_window()
            return
        user = None
        msg = "登出成功!"
        messagebox.showinfo("提示", msg)
        self.lobby.destroy()

    def open_create_window(self):

        try:
            server.update_online_status(user)
        except ConnectionRefusedError:
            messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
            self.room_window.destroy()
            w.open_login_window()
            return

        self.create_window = tk.Toplevel(self.lobby)
        self.create_window.title("建立房間")

        window_width = 350
        window_height = 300

        screen_width = self.create_window.winfo_screenwidth()
        screen_height = self.create_window.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.create_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.create_window.resizable(False, False)

        thought_time_frame = tk.Frame(self.create_window)
        thought_time_frame.pack(side=tk.TOP, pady=10)

        thought_time_label = tk.Label(thought_time_frame, text="思考時間:")
        thought_time_label.pack(side=tk.LEFT)

        thought_time_box = ttk.Combobox(thought_time_frame, values=["%-3d" % 1, "%-3d" % 3, "%-3d" % 5, "%-3d" % 10, "%-3d" % 15, "%-3d" % 30, "%-3d" % 60, "%-3d" % 120, "%-3d" % 150, "%-3d" % 180], width=3, state="readonly")
        thought_time_box.set("%-3d" % 30)
        thought_time_box.pack(side=tk.LEFT)

        extra_time_frame = tk.Frame(self.create_window)
        extra_time_frame.pack(side=tk.TOP, pady=15)

        extra_time_label = tk.Label(extra_time_frame, text="時間獎勵:")
        extra_time_label.pack(side=tk.LEFT)

        extra_second_spinbox = tk.Spinbox(extra_time_frame, from_=0, to=30, width=2, wrap=True, state="readonly")
        extra_second_spinbox.pack(side=tk.LEFT)
        tk.Label(extra_time_frame, text="秒").pack(side=tk.LEFT)


        color_frame = tk.Frame(self.create_window)
        color_frame.pack(side=tk.TOP, pady=15)

        color_label = tk.Label(color_frame, text="對弈方:")
        color_label.pack(side=tk.LEFT)


        color_box = ttk.Combobox(color_frame, values=["隨機", "黑色", "白色"], width=5, state="readonly")
        color_box.set("隨機")
        color_box.pack(side=tk.LEFT)

        confirm_button = tk.Button(self.create_window, text="確定", command=lambda: self.w_create(color_box.get(), thought_time_box.get(), extra_second_spinbox.get(), message_text))
        confirm_button.pack(pady=10)

        message_label = tk.Label(self.create_window, text="提示訊息:")
        message_label.pack(pady=10)

        message_text = tk.Text(self.create_window, height=1, width=30)
        message_text.pack()
        message_text.config(state=tk.DISABLED)

    def w_create(self, a_color, a_thought_time, a_extra_second, a_position):

        current_datetime = datetime.datetime.now()
        try:
            server.update_active_status(user)
            server.create(a_color, a_thought_time, a_extra_second, user, current_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        except ConnectionRefusedError:
            messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
            self.create_window.destroy()
            self.lobby.destroy()
            w.open_lobby_window()
            return
        self.create_window.destroy()
        self.refresh_lobby_flag = False
        self.lobby.destroy()
        self.open_room_window(a_color, a_thought_time, a_extra_second)

    def w_subject(self):
        global user, rooms

        self.l_room_box.config(state=tk.NORMAL)
        self.l_room_box.delete(1.0, tk.END)
        try:
            server.update_online_status(user)

            rooms = server.subject()
        except ConnectionRefusedError:
            messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
            self.lobby.destroy()
            w.open_login_window()
            return

        for i, room_data in enumerate(rooms):



            if room_data["game_state"] == False:
                formatted_text = "   思考時間: %3s 分鐘   |   獎勵時間: %2s 秒   |   對弈者(%s): %s                             %s" % (room_data["thought_time"].strip(), room_data["extra_second"], room_data["color"], align_text(room_data["user"], 8), room_data["datetime"])
                if room_data["opponent"] == "":
                    join_button = tk.Button(self.l_room_box, text="等待", bd=0, fg="green", font=("Helvetica", 12), command=lambda opponent=room_data["user"]: self.w_enter(opponent))
                    self.l_room_box.window_create(tk.END, window=join_button)
                else:
                    full_button = tk.Button(self.l_room_box, text="已滿", bd=0, fg="orange", font=("Helvetica", 12))
                    self.l_room_box.window_create(tk.END, window=full_button)

            else:
                if room_data["color"] == "白色":
                    formatted_text = "   思考時間: %3s 分鐘   |   獎勵時間: %2s 秒   |   白色: %s   |   黑色: %s                %s" % (room_data["thought_time"].strip(), room_data["extra_second"], align_text(room_data["user"], 8), align_text(room_data["opponent"], 8), room_data["datetime"])
                else:
                    formatted_text = "   思考時間: %3s 分鐘   |   獎勵時間: %2s 秒   |   黑色: %s   |   白色: %s                %s" % (room_data["thought_time"].strip(), room_data["extra_second"], align_text(room_data["user"], 8), align_text(room_data["opponent"], 8), room_data["datetime"])

                battle_button = tk.Button(self.l_room_box, text="對弈", bd=0, fg="red", font=("Helvetica", 12))
                self.l_room_box.window_create(tk.END, window=battle_button)

            self.l_room_box.insert(tk.END, formatted_text)
            self.l_room_box.insert(tk.END, "\n")

        self.l_room_box.config(state=tk.DISABLED)

    def open_room_window(self, a_color, a_thought_time, a_extra_second):

        global user, room
        room = True
        self.room_window = tk.Tk()
        self.room_window.title("等待其他人加入...")

        window_width = 1200
        window_height = 400

        screen_width = self.room_window.winfo_screenwidth()
        screen_height = self.room_window.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.room_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.room_window.resizable(False, False)

        self.rule_label = tk.Label(self.room_window, text="思考時間: %3s + %-2s" % (a_thought_time.strip(), a_extra_second), font=("Arial", 24))
        self.rule_label.grid(row=6, column=1)

        self.versus_label = tk.Label(self.room_window, text="VS")
        self.versus_label.config(font=("Arial", 45))


        self.black_image = Image.open("assets/images/black_player.png")
        self.black_image = self.black_image.resize((280, 250))
        self.black_image = ImageTk.PhotoImage(self.black_image)

        self.white_image = Image.open("assets/images/white_player.png")
        self.white_image = self.white_image.resize((280, 250))
        self.white_image = ImageTk.PhotoImage(self.white_image)

        self.random_image = Image.open("assets/images/random_player.png")
        self.random_image = self.random_image.resize((280, 250))
        self.random_image = ImageTk.PhotoImage(self.random_image)

        self.black_label = tk.Label(self.room_window, image= self.black_image)
        self.white_label = tk.Label(self.room_window, image=self.white_image)

        self.random1_label = tk.Label(self.room_window, image=self.random_image)
        self.random2_label = tk.Label(self.room_window, image=self.random_image)

        if a_color == "黑色":
            self.black_label.grid(row=3, column=0)
            self.versus_label.grid(row=3, column=1)
            self.white_label.grid(row=3, column=2)
        elif a_color == "白色":
            self.white_label.grid(row=3, column=0)
            self.versus_label.grid(row=3, column=1)
            self.black_label.grid(row=3, column=2)
        else:
            self.random1_label.grid(row=2, column=0)
            self.versus_label.grid(row=2, column=1)
            self.random2_label.grid(row=2, column=2)

        self.player1_label = tk.Label(self.room_window, text=user)
        self.player1_label.config(font=("Arial", 24))
        self.player1_label.grid(row=4, column=0)

        self.player2_label = tk.Label(self.room_window, text="等待對手...")
        self.player2_label.config(font=("Arial", 24))
        self.player2_label.grid(row=4, column=2)

        player2_stats_text = "勝率:   -   |   Win: - / Lose: - / Draw: -"
        self.player2_stats_label = tk.Label(self.room_window, text=player2_stats_text, font=("Arial", 14), justify='center', anchor='n', padx=20, fg="green")
        self.player2_stats_label.grid(row=5, column=2)

        try:
            player1_stats = server.get_user_stats(user)
        except ConnectionRefusedError:
            messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
            self.room_window.destroy()
            w.open_login_window()
            return
        player1_game_sum = int(player1_stats["win"]) + int(player1_stats["lose"]) + int(player1_stats["draw"])
        try:
            player1_win_rate = int(player1_stats["win"]) / float(player1_game_sum) * 100
        except ZeroDivisionError:
            player1_win_rate = 0.0

        player1_stats_text = "勝率: %.2f%s   |   Win: %s / Lose: %s / Draw: %s" % (player1_win_rate, '%', player1_stats["win"], player1_stats["lose"], player1_stats["draw"])
        self.player1_stats_label = tk.Label(self.room_window, text=player1_stats_text, font=("Arial", 14), justify='center', anchor='n', padx=20, fg="green")
        self. player1_stats_label.grid(row=5, column=0)



        self.exit_button = tk.Button(self.room_window, text="離開", bd=0, fg="red", font=("Helvetica", 12), command=lambda : self.host_exit_room(user))
        self.exit_button.grid(row=7, column=1)
        self.update_opponent_flag = True
        self.room_window.after(1000, self.update_opponent)

        self.preparation_frame = tk.Frame(self.room_window)
        self.preparation_frame.grid(row=6, column=2)

        self.preparation_label = tk.Label(self.preparation_frame, text="準備中", font=("Arial", 14), justify='center', anchor='n', padx=20, fg="red")
        self.preparation_label.pack(side=tk.LEFT)

        self.start_button = tk.Button(self.room_window, text="開始!", font=("TkDefaultFont", 14, "bold"), command=self.start_game)
        self.start_button.grid(row=4, column=1)

    def host_exit_room(self, a_user):
        global room
        room = False
        self.room_window.destroy()
        try:
            server.update_active_status(a_user)
            server.delete_room(a_user)
        except ConnectionRefusedError:
            messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
            self.lobby.destroy()
            w.open_login_window()
            return
        self.open_lobby_window()

    def update_opponent(self):
        try:
            server.update_online_status(user)
        except ConnectionRefusedError:
            messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
            self.room_window.destroy()
            w.open_login_window()
            return
        if self.update_opponent_flag == True:
            print("Refreshing opponent...")
            try:
                a_room = server.get_user_room(user)
            except ConnectionRefusedError:
                messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
                self.room_window.destroy()
                w.open_login_window()
                return

            if(a_room["opponent"] != ""):
                self.room_window.title("%s進入房間" % a_room["opponent"])
                try:
                    player2_stats = server.get_user_stats(a_room["opponent"])
                except ConnectionRefusedError:
                    messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
                    self.room_window.destroy()
                    w.open_login_window()
                    return
                player2_game_sum = int(player2_stats["win"]) + int(player2_stats["lose"]) + int(player2_stats["draw"])
                try:
                    player2_win_rate = int(player2_stats["win"]) / float(player2_game_sum) * 100
                except ZeroDivisionError:
                    player2_win_rate = 0.0

                player2_stats_text = "勝率: %.2f%s   |   Win: %s / Lose: %s / Draw: %s" % (player2_win_rate, '%', player2_stats["win"], player2_stats["lose"], player2_stats["draw"])
                self.player2_stats_label.config(text=player2_stats_text)
                self.player2_label.config(text=a_room["opponent"])

                if a_room["opponent_state"] == True:
                    self.preparation_label.config(text="準備完成", fg="green")
                else:
                    self.preparation_label.config(text="準備中", fg="red")

            else:
                if a_room["opponent_state"] == True:
                    try:
                        server.update_preparation(user)
                    except ConnectionRefusedError:
                        messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
                        self.room_window.destroy()
                        w.open_login_window()
                        return

                player2_stats_text = "勝率:   -   |   Win: - / Lose: - / Draw: -"
                self.player2_stats_label.config(text=player2_stats_text)
                self.player2_label.config(text="等待對手...")
                self.room_window.title("等待其他人加入...")
                self.preparation_label.config(text="準備中", fg="red")

            if self.update_opponent_flag == True:
                self.room_window.after(100, self.update_opponent)
        else:
            print("Stop refreshing opponent!")

    def w_enter(self, a_opponent):

        global user, opponent

        self.refresh_lobby_flag = False
        self.lobby.destroy()

        try:
            server.update_active_status(user)
            a_room = server.enter_opponent_room(a_opponent)
        except ConnectionRefusedError:
            messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
            w.open_login_window()
            return
        if len(a_room) == 0:
            msg = "房主已退出房間!"
            messagebox.showinfo("提示", msg)
            self.open_lobby_window()
            opponent = None
        else:
            opponent = a_room["user"]
            self.room_window = tk.Tk()
            self.room_window.title("%s的房間" % a_room["user"])


            window_width = 1200
            window_height = 400

            screen_width = self.room_window.winfo_screenwidth()
            screen_height = self.room_window.winfo_screenheight()

            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

            self.room_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

            self.room_window.resizable(False, False)

            self.rule_label = tk.Label(self.room_window, text="思考時間: %3s + %-2s" % (a_room["thought_time"].strip(), a_room["extra_second"]), font=("Arial", 24))
            self.rule_label.grid(row=6, column=1)

            self.versus_label = tk.Label(self.room_window, text="VS")
            self.versus_label.config(font=("Arial", 45))

            self.black_image = Image.open("assets/images/black_player.png")
            self.black_image = self.black_image.resize((280, 250))
            self.black_image = ImageTk.PhotoImage(self.black_image)

            self.white_image = Image.open("assets/images/white_player.png")
            self.white_image = self.white_image.resize((280, 250))
            self.white_image = ImageTk.PhotoImage(self.white_image)

            self.random_image = Image.open("assets/images/random_player.png")
            self.random_image = self.random_image.resize((280, 250))
            self.random_image = ImageTk.PhotoImage(self.random_image)

            self.black_label = tk.Label(self.room_window, image= self.black_image)
            self.white_label = tk.Label(self.room_window, image=self.white_image)

            self.random1_label = tk.Label(self.room_window, image=self.random_image)
            self.random2_label = tk.Label(self.room_window, image=self.random_image)

            if a_room["color"] == "白色":
                self.black_label.grid(row=3, column=0)
                self.versus_label.grid(row=3, column=1)
                self.white_label.grid(row=3, column=2)
            elif a_room["color"] == "黑色":
                self.white_label.grid(row=3, column=0)
                self.versus_label.grid(row=3, column=1)
                self.black_label.grid(row=3, column=2)
            else:
                self.random1_label.grid(row=2, column=0)
                self.versus_label.grid(row=2, column=1)
                self.random2_label.grid(row=2, column=2)

            self.player1_label = tk.Label(self.room_window, text=user)
            self.player1_label.config(font=("Arial", 24))
            self.player1_label.grid(row=4, column=0)

            self.player2_label = tk.Label(self.room_window, text=a_opponent)
            self.player2_label.config(font=("Arial", 24))
            self.player2_label.grid(row=4, column=2)

            try:
                player1_stats = server.get_user_stats(user)
            except ConnectionRefusedError:
                messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
                self.room_window.destroy()
                w.open_login_window()
                return
            player1_game_sum = int(player1_stats["win"]) + int(player1_stats["lose"]) + int(player1_stats["draw"])
            try:
                player1_win_rate = int(player1_stats["win"]) / float(player1_game_sum) * 100
            except ZeroDivisionError:
                player1_win_rate = 0.0

            player1_stats_text = "勝率: %.2f%s   |   Win: %s / Lose: %s / Draw: %s" % (player1_win_rate, '%', player1_stats["win"], player1_stats["lose"], player1_stats["draw"])
            self.player1_stats_label = tk.Label(self.room_window, text=player1_stats_text, font=("Arial", 14), justify='center', anchor='n', padx=20, fg="green")
            self. player1_stats_label.grid(row=5, column=0)

            try:
                player2_stats = server.get_user_stats(a_opponent)
            except ConnectionRefusedError:
                messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
                self.room_window.destroy()
                w.open_login_window()
                return
            player2_game_sum = int(player2_stats["win"]) + int(player2_stats["lose"]) + int(player2_stats["draw"])
            try:
                player2_win_rate = int(player2_stats["win"]) / float(player2_game_sum) * 100
            except ZeroDivisionError:
                player2_win_rate = 0.0

            player2_stats_text = "勝率: %.2f%c   |   Win: %s / Lose: %s / Draw: %s" % (player2_win_rate, '%', player2_stats["win"], player2_stats["lose"], player2_stats["draw"])
            self.player2_stats_label = tk.Label(self.room_window, text=player2_stats_text, font=("Arial", 14), justify='center', anchor='n', padx=20, fg="green")
            self.player2_stats_label.grid(row=5, column=2)
            try:
                server.update_opponent(a_opponent, user)
            except ConnectionRefusedError:
                messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
                self.room_window.destroy()
                w.open_login_window()
                return


            self.preparation_frame = tk.Frame(self.room_window)
            self.preparation_frame.grid(row=6, column=0)

            self.preparation_label = tk.Label(self.preparation_frame, text="準備中", font=("Arial", 14), justify='center', anchor='n', padx=20, fg="red")
            self.preparation_label.pack(side=tk.LEFT)

            self.preparation_button = tk.Button(self.preparation_frame, text="準備", font=("TkDefaultFont", 14, "bold"), command=lambda : self.update_preparation(a_opponent))
            self.preparation_button.pack(side=tk.LEFT)

            self.exit_button = tk.Button(self.room_window, text="離開", bd=0, fg="red", font=("Helvetica", 12), command=lambda : self.exit_room(a_opponent))
            self.exit_button.grid(row=7, column=1)
            self.check_start_flag = True
            self.check_start(a_opponent)

    def update_preparation(self, a_opponent):
        try:
            server.update_online_status(user)
            server.update_preparation(a_opponent)
            a_room = server.get_opponent_room(a_opponent, user)
        except ConnectionRefusedError:
            messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
            self.room_window.destroy()
            w.open_login_window()
            return

        if a_room["opponent_state"] == True:
            self.preparation_label.config(text="準備完成", fg="green")
        else:
            self.preparation_label.config(text="準備中", fg="red")


    def check_start(self, a_opponent):

        global game, opponent, battle
        try:
            server.update_online_status(user)
        except ConnectionRefusedError:
            messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
            self.room_window.destroy()
            w.open_login_window()
            return
        if self.check_start_flag == True:
            try:
                a_room = server.get_opponent_room(a_opponent, user)
            except ConnectionRefusedError:
                messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
                self.room_window.destroy()
                w.open_login_window()
                return
            if len(a_room) == 0:
                msg = "房主已退出房間!"
                messagebox.showinfo("提示", msg)
                self.exit_room(a_opponent)
                opponent = None

            else:
                if a_room["game_state"] == True:
                    self.room_window.destroy()
                    try:
                        a_room = server.get_opponent_room(a_opponent, user)
                    except ConnectionRefusedError:
                        messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
                        w.open_login_window()
                        return
                    battle = True
                    self.check_start_flag = False
                    try:
                        game = Chess("guest", a_room["user"], a_room["opponent"], a_room["color"], a_room["thought_time"], a_room["extra_second"], a_room["id"])
                    except Exception:
                        pass
                if self.check_start_flag == True:
                    self.room_window.after(100, lambda : self.check_start(a_opponent))



    def exit_room(self, a_opponent):
        global  opponent
        opponent = None
        try:
            server.update_active_status(user)
            a_room = server.get_opponent_room(a_opponent, user)
        except ConnectionRefusedError:
            messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
            self.room_window.destroy()
            w.open_login_window()
            return
        if len(a_room) != 0:
            if a_room["opponent_state"] == True:
                try:
                    server.update_preparation(a_opponent)
                except ConnectionRefusedError:
                    messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
                    self.room_window.destroy()
                    w.open_login_window()
                    return

            try:
                server.delete_opponent(a_opponent)
            except ConnectionRefusedError:
                messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
                self.room_window.destroy()
                w.open_login_window()
                return
        self.room_window.destroy()
        self.open_lobby_window()

    def start_game(self):
        global game, battle

        try:
            a_room = server.get_user_room(user)
        except ConnectionRefusedError:
            messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
            self.room_window.destroy()
            w.open_login_window()
            return
        if a_room["opponent_state"] == True and a_room["opponent"] != "":
            my_opponent = a_room["opponent"]
            if a_room["color"] == "隨機":  # 抽顏色
                try:
                    server.decide_color_for_random(user)
                except ConnectionRefusedError:
                    messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
                    self.room_window.destroy()
                    w.open_login_window()
                    return
            try:
                server.start(user)
            except ConnectionRefusedError:
                messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
                self.room_window.destroy()
                w.open_login_window()
                return
            self.update_opponent_flag = False

            self.room_window.destroy()
            try:
                a_room = server.get_ready_room(user, my_opponent)
            except ConnectionRefusedError:
                messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
                w.open_login_window()
                return

            if a_room["color"] == "白色":
                try:
                    server.create_battle_info(a_room["id"], a_room["user"], a_room["opponent"], a_room["thought_time"])
                except ConnectionRefusedError:
                    messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
                    w.open_login_window()
                    return
            elif a_room["color"] == "黑色":
                try:
                    server.create_battle_info(a_room["id"], a_room["opponent"], a_room["user"], a_room["thought_time"])
                except ConnectionRefusedError:
                    messagebox.showinfo("提示", "無法連接伺服器，請重新登入！")
                    w.open_login_window()
                    return

            battle = True
            game = Chess("host", a_room["user"], a_room["opponent"], a_room["color"], a_room["thought_time"], a_room["extra_second"], a_room["id"])
        else:
            if a_room["opponent"] == "":
                msg = "正在等待對手加入!"
                messagebox.showinfo("提示", msg)
            else:
                msg = "對手尚在準備中!"
                messagebox.showinfo("提示", msg)

class Chess:

    # 成員變數
    user = ""
    opponent = ""
    color = ""
    thought_time = ""
    extra_second = ""
    side = ""  #host or guest
    room_id = ""
    my_color = ""
    opponent_color = ""


    game_screen = None
    background = None
    screen_size = None
    game_icon = None
    piece_font = None

    left_padding = None
    top_padding = None

    white_king_text = "k"
    white_queen_text = "q"
    white_rook_text = "r"
    white_bishop_text = "b"
    white_knight_text = "n"
    white_pawn_text = "p"

    black_king_text = "l"
    black_queen_text = "w"
    black_rook_text = "t"
    black_bishop_text = "v"
    black_knight_text = "m"
    black_pawn_text = "o"

    piece_types = ["pawn", "queen", "king", "knight", "rook", "bishop"]
    white_piece_images = []
    black_piece_images = []
    black_locations = []
    white_locations = []
    white_options = []
    black_options = []
    valid_moves = [] # 合法的移動路徑

    turn_step = -1     # 整個程式運作的核心，該參數控制大部分運行。
    selection = -1 # 記錄玩家選擇之棋子的index

    timer = None
    fps = 60

    game_over = False  # True代表遊戲結束

    is_my_turn = "not your turn" # server回傳的值，確認現在對方是否結束回合
    updated_captured_pieces = -1

    winner = "" # 紀錄勝者是white或black
    win_reason = -1 # 紀錄是因為哪一種情況獲勝

    opponent_thought_time = 0  # 對方的思考時間

    flash_counter = 0  # 國王即將被吃的時候格子會閃爍，該參數控制格子閃爍的時機
    # 成員變數

    def __init__(self, side, user, opponent, color, thought_time, extra_second, room_id):
        self.side = side
        self.user = user  # 玩家、遊戲資訊
        self.opponent = opponent
        self.color = color
        self.thought_time = int(thought_time.strip()) * 60
        self.opponent_thought_time = self.thought_time
        self.extra_second = int(extra_second)
        self.room_id = room_id

        if self.side == "host":
            if self.color == "白色":
                self.my_color = "white"
                self.opponent_color = "black"
            else:
                self.my_color = "black"
                self.opponent_color = "white"
        else:
            if self.color == "白色":
                self.my_color = "black"
                self.opponent_color = "white"
            else:
                self.my_color = "white"
                self.opponent_color = "black"

        if self.my_color == "black":
            self.white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
            self.black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
        else:
            self.white_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
            self.black_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

        pygame.init() # 啟動Pygame環境
        self.create_root()
        self.create_board()
        self.create_pieces()
        self.run_game()

    def create_root(self):
        self.game_screen = pygame.display.set_mode([1150, 750])
        self.game_screen.fill((255, 255, 255))
        if self.side == "host":
            pygame.display.set_caption("%s VS %s!!!" % (self.user, self.opponent))
        else:
            pygame.display.set_caption("%s VS %s!!!" % (self.opponent, self.user))
        self.background = pygame.image.load("assets/images/background.jpg")
        self.game_screen.blit(self.background, (0, 0))
        self.game_icon = pygame.image.load("assets/images/game_icon.png")
        pygame.display.set_icon(self.game_icon)

        self.draw_player_info()

    def create_board(self):

        self.piece_font = pygame.font.Font("assets/merid_tt/MERIFONT.TTF", 75)
        self.draw_board()

    def create_pieces(self):

        width = 45
        high = 45

        # 白棋
        self.white_king = self.piece_font.render(self.white_king_text, True, "black")
        self.white_queen = self.piece_font.render(self.white_queen_text, True, "black")
        self.white_rook  = self.piece_font.render(self.white_rook_text, True, "black")
        self.white_knight = self.piece_font.render(self.white_knight_text, True, "black")
        self.white_bishop = self.piece_font.render(self.white_bishop_text, True, "black")
        self.white_pawn = self.piece_font.render(self.white_pawn_text, True, "black")
        # 白棋

        # 黑棋
        self.black_queen = self.piece_font.render(self.black_queen_text, True, "black")
        self.black_king = self.piece_font.render(self.black_king_text, True, "black")
        self.black_rook = self.piece_font.render(self.black_rook_text, True, "black")
        self.black_knight = self.piece_font.render(self.black_knight_text, True, "black")
        self.black_bishop = self.piece_font.render(self.black_bishop_text, True, "black")
        self.black_pawn = self.piece_font.render(self.black_pawn_text, True, "black")
        # 黑棋


        self.white_king_small = pygame.transform.scale(self.white_king, (width, high))
        self.white_queen_small = pygame.transform.scale(self.white_queen, (width, high))
        self.white_rook_small = pygame.transform.scale(self.white_rook, (width, high))
        self.white_bishop_small = pygame.transform.scale(self.white_bishop, (width, high))
        self.white_knight_small = pygame.transform.scale(self.white_knight, (width, high))
        self.white_pawn_small = pygame.transform.scale(self.white_pawn, (width, high))



        self.black_queen_small = pygame.transform.scale(self.black_queen, (width, high))
        self.black_king_small = pygame.transform.scale(self.black_king, (width, high))
        self.black_rook_small = pygame.transform.scale(self.black_rook, (width, high))
        self.black_knight_small = pygame.transform.scale(self.black_knight, (width, high))
        self.black_bishop_small = pygame.transform.scale(self.black_bishop, (width, high))
        self.black_pawn_small = pygame.transform.scale(self.black_pawn, (width, high))


        self.white_piece_images = [self.white_pawn, self.white_queen, self.white_king, self.white_knight, self.white_rook, self.white_bishop]
        self.black_piece_images = [self.black_pawn, self.black_queen, self.black_king, self.black_knight, self.black_rook, self.black_bishop]
        self.white_piece_images_small = [self.white_pawn_small, self.white_queen_small, self.white_king_small, self.white_knight_small, self.white_rook_small, self.white_bishop_small]
        self.black_piece_images_small = [self.black_pawn_small, self.black_queen_small, self.black_king_small, self.black_knight_small, self.black_rook_small, self.black_bishop_small]

    # draw_board Start
    def draw_board(self):

        self.left_padding = 200
        self.top_padding = (750 - 640) / 2

        x = 0
        y = self.top_padding
        color_flag = True

        for i in range(64):

            width = 80
            high = 80
            if i % 8 == 0:
                x = self.left_padding
                if i != 0:
                    y += high
            else:
                x += width
                color_flag = not color_flag

            if color_flag:
                pygame.draw.rect(self.game_screen, (255, 228, 196), [x, y, width, high])
            else:
                pygame.draw.rect(self.game_screen, (205, 102, 29), [x, y, width, high])

        my_thought_time = (self.thought_time // 60, self.thought_time % 60)
        opponent_thought_time = (self.opponent_thought_time // 60, self.opponent_thought_time % 60)

        my_font = pygame.font.Font("assets/FreeSans/FreeSansBold.ttf", 40)

        formatted_time = "{:02d}:{:02d}".format(my_thought_time[0], my_thought_time[1])
        self.game_screen.blit(my_font.render(formatted_time, True, "black"), (50, 438))

        formatted_time = "{:02d}:{:02d}".format( opponent_thought_time[0],  opponent_thought_time[1])
        self.game_screen.blit(my_font.render(formatted_time, True, "black"), (50, 267))

        my_font = pygame.font.Font("assets/fonts/kaiu.ttf", 80)
        self.game_screen.blit(my_font.render("投降!", True, "black"), (920, 500))

    # draw_board End

    # draw_pieces Start    
    def draw_pieces(self):

        width = 80
        high = 80

        for i in range(len(self.white_pieces)):
            x = self.white_locations[i][0] * width + 2.5 + self.left_padding
            y = self.white_locations[i][1] * width + 2.5 + self.top_padding
            index = self.piece_types.index(self.white_pieces[i])
            self.game_screen.blit(self.white_piece_images[index], (x, y))

            if self.turn_step < 2:
                if self.selection == i:
                    pygame.draw.rect(self.game_screen, "red", [x-2.5, y-2.5, width,  high], 3)

        for i in range(len(self.black_pieces)):
            x = self.black_locations[i][0] * width + 2.5 + self.left_padding
            y = self.black_locations[i][1] * width + 2.5 + self.top_padding
            index = self.piece_types.index(self.black_pieces[i])
            self.game_screen.blit(self.black_piece_images[index], (x, y))

            if self.turn_step >= 2:
                if self.selection == i:
                    pygame.draw.rect(self.game_screen, "blue", [x-2.5, y-2.5, width,  high], 3)



    # draw_pieces End

    # draw_player_info Start
    def draw_player_info(self):
        width = 80
        height = 80
        font = pygame.font.Font("assets/fonts/kaiu.ttf", 30)
        if self.side == "host":
            if self.color == "白色":
                white_image = pygame.image.load("assets/images/white_player.png")
                white_image = pygame.transform.scale(white_image, (width, height))
                x = 50
                y = 570
                self.game_screen.blit(white_image, (x, y))

                user_surface = font.render(self.user, True, (0, 0, 0))
                user_rect = user_surface.get_rect()
                user_text_width, user_text_height = user_surface.get_size()
                x = x + (width - user_text_width) // 2
                y = y + height + 10
                user_rect.topleft = (x, y)
                self.game_screen.blit(user_surface, user_rect)

                my_leaves_image = pygame.image.load("assets/images/my_leaves.png")
                my_leaves_image = pygame.transform.scale(my_leaves_image, (200, 107))
                x =  x + (user_text_width - 200) // 2
                y =  y - 250
                self.game_screen.blit(my_leaves_image, (x, y))

                black_image = pygame.image.load("assets/images/black_player.png")
                black_image = pygame.transform.scale(black_image, (width, height))
                x = 50
                y = 80
                self.game_screen.blit(black_image, (x, y))

                opponent_surface = font.render(self.opponent, True, (0, 0, 0))
                opponent_rect = opponent_surface.get_rect()
                opponent_text_width, opponent_text_height = opponent_surface.get_size()
                x = x + (width - opponent_text_width) // 2
                y = y + height + 10
                opponent_rect.topleft = (x, y)
                self.game_screen.blit(opponent_surface, opponent_rect)

                opponent_leaves_image = pygame.image.load("assets/images/opponent_leaves.png")
                opponent_leaves_image = pygame.transform.scale(opponent_leaves_image, (200, 107))
                x =  x + (opponent_text_width - 200) // 2
                y =  y + 75
                self.game_screen.blit(opponent_leaves_image, (x, y))






            else:
                white_image = pygame.image.load("assets/images/white_player.png")
                white_image = pygame.transform.scale(white_image, (width, height))
                x = 50
                y = 80
                self.game_screen.blit(white_image, (x, y))

                opponent_surface = font.render(self.opponent, True, (0, 0, 0))
                opponent_rect = opponent_surface.get_rect()
                opponent_text_width, opponent_text_height = opponent_surface.get_size()
                x = x + (width - opponent_text_width) // 2
                y = y + height + 10
                opponent_rect.topleft = (x, y)
                self.game_screen.blit(opponent_surface, opponent_rect)

                opponent_leaves_image = pygame.image.load("assets/images/opponent_leaves.png")
                opponent_leaves_image = pygame.transform.scale(opponent_leaves_image, (200, 107))
                x =  x + (opponent_text_width - 200) // 2
                y =  y + 75
                self.game_screen.blit(opponent_leaves_image, (x, y))


                black_image = pygame.image.load("assets/images/black_player.png")
                black_image = pygame.transform.scale(black_image, (width, height))
                x = 50
                y = 570
                self.game_screen.blit(black_image, (x, y))

                user_surface = font.render(self.user, True, (0, 0, 0))
                user_rect = user_surface.get_rect()
                user_text_width, user_text_height = user_surface.get_size()
                x = x + (width - user_text_width) // 2
                y = y + height + 10
                user_rect.topleft = (x, y)
                self.game_screen.blit(user_surface, user_rect)

                my_leaves_image = pygame.image.load("assets/images/my_leaves.png")
                my_leaves_image = pygame.transform.scale(my_leaves_image, (200, 107))
                x =  x + (user_text_width - 200) // 2
                y =  y - 250
                self.game_screen.blit(my_leaves_image, (x, y))


        else:
            if self.color == "黑色":
                white_image = pygame.image.load("assets/images/white_player.png")
                white_image = pygame.transform.scale(white_image, (width, height))
                x = 50
                y = 570
                self.game_screen.blit(white_image, (x, y))

                opponent_surface = font.render(self.opponent, True, (0, 0, 0))
                opponent_rect = opponent_surface.get_rect()
                opponent_text_width, opponent_text_height = opponent_surface.get_size()
                x = x + (width - opponent_text_width) // 2
                y = y + height + 10
                opponent_rect.topleft = (x, y)
                self.game_screen.blit(opponent_surface, opponent_rect)

                my_leaves_image = pygame.image.load("assets/images/my_leaves.png")
                my_leaves_image = pygame.transform.scale(my_leaves_image, (200, 107))
                x =  x + (opponent_text_width - 200) // 2
                y =  y - 250
                self.game_screen.blit(my_leaves_image, (x, y))


                black_image = pygame.image.load("assets/images/black_player.png")
                black_image = pygame.transform.scale(black_image, (width, height))
                x = 50
                y = 80
                self.game_screen.blit(black_image, (x, y))



                user_surface = font.render(self.user, True, (0, 0, 0))
                user_rect = user_surface.get_rect()
                user_text_width, user_text_height = user_surface.get_size()
                x = x + (width - user_text_width) // 2
                y = y + height + 10
                user_rect.topleft = (x, y)
                self.game_screen.blit(user_surface, user_rect)

                opponent_leaves_image = pygame.image.load("assets/images/opponent_leaves.png")
                opponent_leaves_image = pygame.transform.scale(opponent_leaves_image, (200, 107))
                x =  x + (user_text_width - 200) // 2
                y =  y + 75
                self.game_screen.blit(opponent_leaves_image, (x, y))


            else:
                white_image = pygame.image.load("assets/images/white_player.png")
                white_image = pygame.transform.scale(white_image, (width, height))
                x = 50
                y = 80
                self.game_screen.blit(white_image, (x, y))

                user_surface = font.render(self.user, True, (0, 0, 0))
                user_rect = user_surface.get_rect()
                user_text_width, user_text_height = user_surface.get_size()
                x = x + (width - user_text_width) // 2
                y = y + height + 10
                user_rect.topleft = (x, y)
                self.game_screen.blit(user_surface, user_rect)

                opponent_leaves_image = pygame.image.load("assets/images/opponent_leaves.png")
                opponent_leaves_image = pygame.transform.scale(opponent_leaves_image, (200, 107))
                x =  x + (user_text_width - 200) // 2
                y =  y + 75
                self.game_screen.blit(opponent_leaves_image, (x, y))

                black_image = pygame.image.load("assets/images/black_player.png")
                black_image = pygame.transform.scale(black_image, (width, height))
                x = 50
                y = 570
                self.game_screen.blit(black_image, (x, y))

                opponent_surface = font.render(self.opponent, True, (0, 0, 0))
                opponent_rect = opponent_surface.get_rect()
                opponent_text_width, opponent_text_height = opponent_surface.get_size()
                x = x + (width - opponent_text_width) // 2
                y = y + height + 10
                opponent_rect.topleft = (x, y)
                self.game_screen.blit(opponent_surface, opponent_rect)

                my_leaves_image = pygame.image.load("assets/images/my_leaves.png")
                my_leaves_image = pygame.transform.scale(my_leaves_image, (200, 107))
                x =  x + (opponent_text_width - 200) // 2
                y =  y - 250
                self.game_screen.blit(my_leaves_image, (x, y))


    # draw_player_info End

    # check_options Start
    def check_options(self, pieces, locations, color):
        move_list = []
        all_move_list = []

        for i in range(len(pieces)):
            location = locations[i]
            piece = pieces[i]
            match piece:
                case "pawn":
                    move_list = self.check_pawn_moves(location, color)
                case "knight":
                    move_list = self.check_knight_moves(location, color)
                case "bishop":
                    move_list = self.check_bishop_moves(location, color)
                case "rook":
                    move_list = self.check_rook_moves(location, color)
                case "queen":
                    move_list = self.check_queen_moves(location, color)
                case "king":
                    move_list = self.check_king_moves(location, color)


            all_move_list.append(move_list)

        return all_move_list
    # check_options End

    # check_pawn_moves Start
    def check_pawn_moves(self, position, color):
        move_list = []

        if self.my_color == "black":
            if color == "white":
                if (position[0], position[1] + 1) not in self.white_locations and (position[0], position[1] + 1) not in self.black_locations and position[1] < 7:
                    move_list.append((position[0], position[1] + 1))
                if (position[0], position[1] + 2) not in self.white_locations and (position[0], position[1] + 2) not in self.black_locations and (position[0], position[1] + 1) not in self.white_locations and (position[0], position[1] + 1) not in self.black_locations and position[1] == 1:
                    move_list.append((position[0], position[1] + 2))
                if (position[0] + 1, position[1] + 1) in self.black_locations:
                    move_list.append((position[0] + 1, position[1] + 1))
                if (position[0] - 1, position[1] + 1) in self.black_locations:
                    move_list.append((position[0] - 1, position[1] + 1))
            else:
                if (position[0], position[1] - 1) not in self.white_locations and (position[0], position[1] - 1) not in self.black_locations and position[1] > 0:
                    move_list.append((position[0], position[1] - 1))
                if (position[0], position[1] - 2) not in self.white_locations and (position[0], position[1] - 2) not in self.black_locations and (position[0], position[1] - 1) not in self.white_locations and (position[0], position[1] - 1) not in self.black_locations and position[1] == 6:
                    move_list.append((position[0], position[1] - 2))
                if (position[0] + 1, position[1] - 1) in self.white_locations:
                    move_list.append((position[0] + 1, position[1] - 1))
                if (position[0] - 1, position[1] - 1) in self.white_locations:
                    move_list.append((position[0] - 1, position[1] - 1))
        else:
            if color == "black":
                if (position[0], position[1] + 1) not in self.white_locations and (position[0], position[1] + 1) not in self.black_locations and position[1] < 7:
                    move_list.append((position[0], position[1] + 1))
                if (position[0], position[1] + 2) not in self.white_locations and (position[0], position[1] + 2) not in self.black_locations and (position[0], position[1] + 1) not in self.white_locations and (position[0], position[1] + 1) not in self.black_locations and position[1] == 1:
                    move_list.append((position[0], position[1] + 2))
                if (position[0] + 1, position[1] + 1) in self.white_locations:
                    move_list.append((position[0] + 1, position[1] + 1))
                if (position[0] - 1, position[1] + 1) in self.white_locations:
                    move_list.append((position[0] - 1, position[1] + 1))
            else:
                if (position[0], position[1] - 1) not in self.white_locations and (position[0], position[1] - 1) not in self.black_locations and position[1] > 0:
                    move_list.append((position[0], position[1] - 1))
                if (position[0], position[1] - 2) not in self.white_locations and (position[0], position[1] - 2) not in self.black_locations and (position[0], position[1] - 1) not in self.white_locations and (position[0], position[1] - 1) not in self.black_locations and position[1] == 6:
                    move_list.append((position[0], position[1] - 2))
                if (position[0] + 1, position[1] - 1) in self.black_locations:
                    move_list.append((position[0] + 1, position[1] - 1))
                if (position[0] - 1, position[1] - 1) in self.black_locations:
                    move_list.append((position[0] - 1, position[1] - 1))

        return move_list

    # check_pawn_moves End

    # check_knight_moves Start
    def check_knight_moves(self, position, color):
        move_list = []

        if color == "white":
            friend_list = self.white_locations
        else:
            friend_list = self.black_locations

        targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]

        for i in range (8):
            target = (position[0] + targets[i][0], position[1] + targets[i][1])

            if target not in friend_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                move_list.append(target)

        return move_list
    # check_knight_moves End

    # check_bishop_moves Start
    def check_bishop_moves(self, position, color):
        move_list = []

        if color == "white":
            enemy_list = self.black_locations
            friend_list = self.white_locations
        else:
            enemy_list = self.white_locations
            friend_list = self.black_locations

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
                case 3:
                    x = -1
                    y = 1

            while path:

                if (position[0] + (chain * x), position[1] + (chain * y)) not in friend_list and 0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                    move_list.append((position[0] + (chain * x), position[1] + (chain * y)))

                    if (position[0] + (chain * x), position[1] + (chain * y)) in enemy_list:
                        path = False

                    chain += 1
                else:
                    path = False

        return move_list
    # check_bishop_moves End

    # check_rook_moves Start
    def check_rook_moves(self, position, color):
        move_list = []

        if color == "white":
            enemy_list = self.black_locations
            friend_list = self.white_locations
        else:
            enemy_list = self.white_locations
            friend_list = self.black_locations

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
                case 3:
                    x = -1
                    y = 0

            while path:

                if (position[0] + (chain * x), position[1] + (chain * y)) not in friend_list and 0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                    move_list.append((position[0] + (chain * x), position[1] + (chain * y)))

                    if (position[0] + (chain * x), position[1] + (chain * y)) in enemy_list:
                        path = False

                    chain += 1
                else:
                    path = False

        return move_list
    # check_rook_moves End

    # check_queen_moves Start
    def check_queen_moves(self, position, color):
        move_list = self.check_bishop_moves(position, color)
        second_list = self.check_rook_moves(position, color)

        for i in range (len(second_list)):
            move_list.append(second_list[i])

        return move_list
    # check_queen_moves End

    def check_king_moves(self, position, color):

        move_list = []

        if color == "white":
            friendList = self.white_locations
        else:
            friendList = self.black_locations

        targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]

        for i in range (8):
            target = (position[0] + targets[i][0], position[1] + targets[i][1])

            if target not in friendList and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                move_list.append(target)

        return move_list
    # check_king_moves End

    # check_valid_moves Start
    def check_valid_moves(self):

        if self.turn_step < 2:
            options_list = self.white_options
        else:
            options_list = self.black_options

        valid_options = options_list[self.selection]

        return valid_options
    # check_valid_moves End

    # draw_captured Start
    def draw_captured(self):
        x = self.left_padding + 700
        y = self.top_padding
        my_board_image = pygame.image.load("assets/images/board.jpg")
        my_board_image = pygame.transform.scale(my_board_image, (240, 400))
        self.game_screen.blit(my_board_image, (x, y))

        for i in range(len(self.white_captured_pieces)):
            captured_piece = self.white_captured_pieces[i]
            index = self.piece_types.index(captured_piece)
            if i < 8:
                self.game_screen.blit(self.black_piece_images_small[index], (x + 5, y + 15 + 45 * i))
            else:
                self.game_screen.blit(self.black_piece_images_small[index], (x + 60, y + 15 + 45 * (i - 8)))

        for i in range(len(self.black_captured_pieces)):
            captured_piece = self.black_captured_pieces[i]
            index = self.piece_types.index(captured_piece)
            if i < 8:
                self.game_screen.blit(self.white_piece_images_small[index], (x + 125, y + 15 + 45 * i))
            else:
                self.game_screen.blit(self.white_piece_images_small[index], (x + 190, y + 15 + 45 * (i - 8)))
    # draw_captured End

    # build_surrender_button Start
    def build_surrender_button(self):
        my_surrender_image = pygame.image.load("assets/images/surrender.png")
        my_surrender_image = pygame.transform.scale(my_surrender_image, (250, 228))
        x = self.left_padding + 700
        y = self.top_padding + 410
        self.game_screen.blit(my_surrender_image, (x, y))
    # build_surrender_button End

    # draw_valid Start
    def draw_valid(self, moves):

        color = "green"
        for i in range(len(moves)):
            pygame.draw.circle(self.game_screen, color, (self.left_padding + moves[i][0] * 80 + 40, self.top_padding + moves[i][1] * 80 + 40), 5)
    # draw_valid End

    # draw_gameover Start
    def draw_gameover(self):
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        x = 300
        y = 340
        pygame.draw.rect(self.game_screen, "black", [x, y, 550, 70])

        if self.winner == "white":
            match self.win_reason:
                case 1:
                    self.game_screen.blit(
                        self.font.render('BLACK king has been captured, WHITE won the game!', True, "white"),
                        (x+10, y+10))
                case 2:
                    self.game_screen.blit(self.font.render('BLACK ran out of time, WHITE won the game!', True, "white"),
                                         (x+10, y+10))
                case 3:
                    self.game_screen.blit(self.font.render('BLACK surrendered, WHITE won the game!', True, "white"),
                                         (x+10, y+10))
                case 4:
                    self.game_screen.blit(
                        self.font.render('BLACK has quit the game, WHITE won the game!', True, "white"), (x+10, y+10))
                case 5:
                    self.game_screen.blit(
                        self.font.render('BLACK has disconnected, WHITE won the game!', True, "white"), (x+10, y+10))
        elif self.winner == "black":
            match self.win_reason:
                case 1:
                    self.game_screen.blit(
                        self.font.render('WHITE king has been captured, BLACK won the game!', True, "white"),
                        (x+10, y+10))
                case 2:
                    self.game_screen.blit(self.font.render('WHITE ran out of time, BLACK won the game!', True, "white"),
                                         (x+10, y+10))
                case 3:
                    self.game_screen.blit(self.font.render('WHITE surrendered, BLACK won the game!', True, "white"),
                                         (x+10, y+10))
                case 4:
                    self.game_screen.blit(
                        self.font.render('WHITE has quit the game, BLACK won the game!', True, "white"), (x+10, y+10))

                case 5:
                    self.game_screen.blit(
                        self.font.render('WHITE has disconnected, BLACK won the game!', True, "white"), (x+10, y+10))
        else:
            self.game_screen.blit(self.font.render('30 turn passed and no chess captured, GAME DRAW!', True, "white"),
                                 (x+10, y+10))
        self.game_screen.blit(self.font.render("Press enter to quit!", True, "white"), (x+10, y+30))

    # draw_gameover End

    # draw_check Start
    def draw_check(self):

        if "king" in self.white_pieces:
            king_index = self.white_pieces.index("king")
            king_location = self.white_locations[king_index]

            for i in range(len(self.black_options)):
                if king_location in self.black_options[i]:
                    if self.flash_counter < 15:
                        pygame.draw.rect(self.game_screen, "red", [self.left_padding + self.white_locations[king_index][0] * 80 + 1, self.top_padding + self.white_locations[king_index][1] * 80 + 1, 80, 80], 5)

        if "king" in self.black_pieces:
            king_index = self.black_pieces.index("king")
            king_location= self.black_locations[king_index]

            for i in range(len(self.white_options)):
                if king_location in self.white_options[i]:
                    if self.flash_counter < 15:
                        pygame.draw.rect(self.game_screen, "dark blue", [self.left_padding + self.black_locations[king_index][0] * 80 + 1, self.top_padding + self.black_locations[king_index][1] * 80 + 1, 80, 80], 5)
    # draw_check End

    def run_game(self):
        self.white_pieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
        self.black_pieces = ["rook", "knight", "bishop", "king", "queen", "bishop", "knight", "rook", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
        self.white_captured_pieces = []
        self.black_captured_pieces = []
        running = True
        msg = "無法連接伺服器，關閉游戲！"
        self.build_surrender_button()
        self.timer = pygame.time.Clock()
        self.white_options = self.check_options(self.white_pieces, self.white_locations, "white") # 檢查白方所有棋子的合法路徑，該參數是所有合法路徑的集合
        self.black_options = self.check_options(self.black_pieces, self.black_locations, "black") # 檢查黑方所有棋子的合法路徑，該參數是所有合法路徑的集合
        self.turn_step = 2
        start_time = pygame.time.get_ticks()

        counter = 0
        while running:
            self.timer.tick(self.fps)
            self.flash_counter = (self.flash_counter + 1) % 30  # 國王即將被吃的時候格子會閃爍，當counter<15畫出邊框
            self.game_screen.fill((255, 255, 255))
            self.game_screen.blit(self.background, (0, 0))
            self.build_surrender_button()
            self.draw_player_info()
            self.draw_board()
            self.draw_pieces()
            self.draw_captured()
            self.draw_check()

            if self.winner:
                self.draw_gameover()

            counter = (counter + 1) % 300

            if counter % 10 == 0:
                try:
                    server.update_online_status(user)
                except ConnectionRefusedError:
                    messagebox.showinfo("提示", msg)
                    pygame.quit()
                    w.open_login_window()
                    return

            if counter % 30 == 0:
                try:
                    server.update_connect_status(self.room_id, self.my_color)
                except ConnectionRefusedError:
                    messagebox.showinfo("提示", msg)
                    pygame.quit()
                    w.open_login_window()
                    return

            if ((self.my_color == "black" and counter == 149) or (self.my_color == "white" and counter == 299)) and not self.game_over:
                try:
                    server.check_opponent_status(self.room_id, self.my_color)
                except ConnectionRefusedError:
                    messagebox.showinfo("提示", msg)
                    pygame.quit()
                    w.open_login_window()
                    return

            if self.winner == "" and (counter % 10 == 0):
                if (self.turn_step == 0 or self.turn_step == 1) and self.my_color == "white":
                    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
                    if elapsed_time > 0:  # 每秒-1
                        self.thought_time -= 1
                        start_time = pygame.time.get_ticks()  # 重置起始時間
                        try:
                            server.update_time(self.room_id, "white", self.thought_time)
                        except ConnectionRefusedError:
                            messagebox.showinfo("提示", msg)
                            pygame.quit()
                            w.open_login_window()
                            return

                elif (self.turn_step == 3 or self.turn_step == 4) and self.my_color == "black":
                    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
                    if elapsed_time > 0:  # 每秒-1
                        self.thought_time -= 1
                        start_time = pygame.time.get_ticks()  # 重置起始時間
                        try:
                            server.update_time(self.room_id, "black", self.thought_time)
                        except ConnectionRefusedError:
                            messagebox.showinfo("提示", msg)
                            pygame.quit()
                            w.open_login_window()
                            return

            if self.selection != -1:     # 當有棋手選擇棋子的時候，在螢幕上畫出該棋子可以移動的路徑
                self.valid_moves = self.check_valid_moves()
                self.draw_valid(self.valid_moves)

            if self.turn_step == 2 and (counter % 10 == 0):  # 當棋手處於等待狀態
                try:
                    self.is_my_turn = server.check_turn(self.room_id, user)  # 詢問server是否輪到己方移動的回合
                except ConnectionRefusedError:
                    messagebox.showinfo("提示", msg)
                    pygame.quit()
                    w.open_login_window()
                    return

                if self.my_color == "black":
                    try:
                        self.white_locations = list(map(tuple, server.check_white_location(self.room_id)))  # 詢問server白棋子的最新位置
                    except ConnectionRefusedError:
                        messagebox.showinfo("提示", msg)
                        pygame.quit()
                        w.open_login_window()
                        return
                    try:
                        self.black_locations = list(map(tuple, server.check_black_location(self.room_id)))  # 詢問server黑棋子的最新位置
                    except ConnectionRefusedError:
                        messagebox.showinfo("提示", msg)
                        pygame.quit()
                        w.open_login_window()
                        return
                    try:
                        self.opponent_thought_time = server.get_time(self.room_id, "black")
                    except ConnectionRefusedError:
                        messagebox.showinfo("提示", msg)
                        pygame.quit()
                        w.open_login_window()
                        return
                else:
                    try:
                        white_temp = list(map(tuple, server.check_white_location(self.room_id)))
                    except ConnectionRefusedError:
                        messagebox.showinfo("提示", msg)
                        pygame.quit()
                        w.open_login_window()
                        return

                    for i in range(len(white_temp)):
                        temp = list(white_temp[i])
                        temp[0] = 7 - temp[0]
                        temp[1] = 7 - temp[1]
                        white_temp[i] = tuple(temp)
                    self.white_locations = white_temp

                    try:
                        black_temp = list(map(tuple, server.check_black_location(self.room_id)))
                    except ConnectionRefusedError:
                        messagebox.showinfo("提示", msg)
                        pygame.quit()
                        w.open_login_window()
                        return

                    for i in range(len(black_temp)):
                        temp = list(black_temp[i])
                        temp[0] = 7 - temp[0]
                        temp[1] = 7 - temp[1]
                        black_temp[i] = tuple(temp)
                    self.black_locations = black_temp
                    try:
                        self.opponent_thought_time = server.get_time(self.room_id, "white")
                    except ConnectionRefusedError:
                        messagebox.showinfo("提示", msg)
                        pygame.quit()
                        w.open_login_window()
                        return
                try:
                    self.updated_captured_pieces = server.check_captured_pieces(self.room_id, user)  # 詢問server被捕獲的棋子
                except ConnectionRefusedError:
                    messagebox.showinfo("提示", msg)
                    pygame.quit()
                    w.open_login_window()
                    return

            if self.updated_captured_pieces != -1 and self.my_color == "white":  # 默認參數代表沒棋子被捕獲
                self.black_captured_pieces.append(self.white_pieces[self.updated_captured_pieces])  # 把被捕獲到的棋子加進被捕獲的list，註：white_captured_pieces表示白方吃掉的棋子
                self.white_pieces.pop(self.updated_captured_pieces)  # 己方的棋子list剔除被捕獲的棋子
                try:
                    server.reset_white_captured_pieces(self.room_id)  # 讓server重置被捕獲的棋子的參數。爲了確保client有收到參數，所以是在client重置，而不是server自己重置
                except ConnectionRefusedError:
                    messagebox.showinfo("提示", msg)
                    pygame.quit()
                    w.open_login_window()
                    return
                self.updated_captured_pieces = -1  # 重置client的被捕獲棋子參數
            elif self.updated_captured_pieces != -1 and self.my_color == "black":
                self.white_captured_pieces.append(self.black_pieces[ self.updated_captured_pieces])
                self.black_pieces.pop( self.updated_captured_pieces)
                try:
                    server.reset_black_captured_pieces(self.room_id)
                except ConnectionRefusedError:
                    messagebox.showinfo("提示", msg)
                    pygame.quit()
                    w.open_login_window()
                    return
                self.updated_captured_pieces = -1

            self.white_options = self.check_options(self.white_pieces, self.white_locations, "white")  # 因爲剛剛可能有棋子被剔除，所以這邊重新檢查合法路徑。
            self.black_options = self.check_options(self.black_pieces, self.black_locations, "black")

            if self.is_my_turn == "white":  # 當server回傳棋手可以移動。註：白方永遠不會收到"black"，黑方永遠不會收到"white"
                self.is_my_turn = "not your turn"  # 重置參數
                self.turn_step = 0  # turnStep=0表示白方可以開始操作棋子，turnStep=3則黑方可以操作棋子

            elif self.is_my_turn == "black":
                self.is_my_turn = "not your turn"
                self.turn_step = 3


            if self.thought_time == 0 and not self.game_over:  # 當though_time=0，遊戲結束

                if self.my_color == "white":  # 如果己方是白方，發送勝利者是黑方給server
                    self.winner = "black"
                    try:
                        server.save_winner(self.room_id, "black")
                    except ConnectionRefusedError:
                        messagebox.showinfo("提示", msg)
                        pygame.quit()
                        w.open_login_window()
                        return
                elif self.my_color == "black":
                    self.winner = "white"
                    try:
                        server.save_winner(self.room_id, "white")
                    except ConnectionRefusedError:
                        messagebox.showinfo("提示", msg)
                        pygame.quit()
                        w.open_login_window()
                        return
                try:
                    server.save_win_reason(self.room_id, 2)  # 發送遊戲結束原因給server，2代表棋手用完思考時間
                except ConnectionRefusedError:
                    messagebox.showinfo("提示", msg)
                    pygame.quit()
                    w.open_login_window()
                    return
                self.win_reason = 2

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    try:
                        server.update_active_status(user)
                    except ConnectionRefusedError:
                        messagebox.showinfo("提示", msg)
                        pygame.quit()
                        w.open_login_window()
                        return
                    if self.winner == "" and self.my_color == "white":  # 如果己方是白方，發送勝利者是黑方給server
                        try:
                            server.save_winner(self.room_id, "black")
                        except ConnectionRefusedError:
                            messagebox.showinfo("提示", msg)
                            pygame.quit()
                            w.open_login_window()
                            return
                    elif self.winner == "" and self.my_color  == "black":
                        try:
                            server.save_winner(self.room_id, "white")
                        except ConnectionRefusedError:
                            messagebox.showinfo("提示", msg)
                            pygame.quit()
                            w.open_login_window()
                            return
                    try:
                        server.save_win_reason(self.room_id, 4)  # 發送遊戲結束原因給server，4代表棋手退出游戲
                    except ConnectionRefusedError:
                        messagebox.showinfo("提示", msg)
                        pygame.quit()
                        w.open_login_window()
                        return
                    self.win_reason = 4
                    
                    try:
                        server.exit_battle(self.room_id)  # 刪除 battle
                    except ConnectionRefusedError:
                        messagebox.showinfo("提示", msg)
                        pygame.quit()
                        w.open_login_window()
                        return
                    except Exception:
                        pass
                    
                    if self.winner == "":
                        try:
                            server.update_lose(user)  # 更新敗績
                        except ConnectionRefusedError:
                            messagebox.showinfo("提示", msg)
                            pygame.quit()
                            w.open_login_window()
                            return
                    else:
                        if self.winner == "draw":
                            try:
                                server.update_draw(user)
                            except ConnectionRefusedError:
                                messagebox.showinfo("提示", msg)
                                pygame.quit()
                                w.open_login_window()
                                return
                        elif self.winner == self.my_color:
                            try:
                                server.update_win(user)
                            except ConnectionRefusedError:
                                messagebox.showinfo("提示", msg)
                                pygame.quit()
                                w.open_login_window()
                                return
                        elif self.winner != self.my_color:
                            try:
                                server.update_lose(user)
                            except ConnectionRefusedError:
                                messagebox.showinfo("提示", msg)
                                pygame.quit()
                                w.open_login_window()
                                return
                    running = False

                if event.type == pygame.KEYDOWN and self.game_over:
                    if event.key == pygame.K_RETURN:  # enter
                        try:
                            server.exit_battle(self.room_id)
                            server.update_active_status(user)
                        except ConnectionRefusedError:
                            messagebox.showinfo("提示", msg)
                            pygame.quit()
                            w.open_login_window()
                            return
                        except Exception:
                            pass
                        running = False
                        if self.winner == "draw":
                            try:
                                server.update_draw(user)
                            except ConnectionRefusedError:
                                messagebox.showinfo("提示", msg)
                                pygame.quit()
                                w.open_login_window()
                                return
                        elif self.winner == self.my_color:
                            try:
                                server.update_win(user)
                            except ConnectionRefusedError:
                                messagebox.showinfo("提示", msg)
                                pygame.quit()
                                w.open_login_window()
                                return
                        elif self.winner != self.my_color:
                            try:
                                server.update_lose(user)
                            except ConnectionRefusedError:
                                messagebox.showinfo("提示", msg)
                                pygame.quit()
                                w.open_login_window()
                                return

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over:  # 使用者按左鍵
                    x_cord = (event.pos[0] - self.left_padding) // 80     #獲取鼠標x坐標，然後除以80
                    y_cord = (event.pos[1] - int(self.top_padding)) // 80 #獲取鼠標y坐標，然後除以80
                    click_cord = (x_cord, y_cord) # 坐標除以80，然後xy集合成tuple，當點擊棋子時這個參數會和white/black_locations的成員參數一樣

                    if self.turn_step <= 1:
                        if (event.pos[0] >= 921 and event.pos[0] <= 1131) and (event.pos[1] >= 494 and event.pos[1] <= 597): # 點擊投降
                            self.winner = "black"
                            try:
                                server.save_winner(self.room_id, "black")  # 發送勝利者是黑方給server，註：現在是白方回合
                            except ConnectionRefusedError:
                                messagebox.showinfo("提示", msg)
                                pygame.quit()
                                w.open_login_window()
                                return
                            try:
                                server.save_win_reason(self.room_id, 3)  # 發送遊戲結束原因給server，3代表棋手投降
                            except ConnectionRefusedError:
                                messagebox.showinfo("提示", msg)
                                pygame.quit()
                                w.open_login_window()
                                return
                            self.win_reason = 3

                        if click_cord in self.white_locations:     # 當鼠標點擊的坐標和white_locations中的某個座標一樣
                            self.selection = self.white_locations.index(click_cord)     #白方選擇了一個棋子
                            if self.turn_step == 0:
                                self.turn_step = 1     # turn_step=1 表示白方選擇了一個棋子，現在可以開始放置棋子
                        if click_cord in self.valid_moves and self.selection != -1:
                            self.white_locations[self.selection] = click_cord    #更新選擇的棋子的位置
                            self.thought_time += self.extra_second
                            try:
                                server.update_time(self.room_id, "white", self.thought_time)
                            except ConnectionRefusedError:
                                messagebox.showinfo("提示", msg)
                                pygame.quit()
                                w.open_login_window()
                                return
                            if click_cord in self.black_locations:  # 當白方放置棋子的位置有黑方的棋子
                                black_piece = self.black_locations.index(click_cord)  # 從滑鼠坐標獲取黑方棋子的信息
                                self.white_captured_pieces.append(self.black_pieces[black_piece])  # 把被捕獲到的黑方棋子加進白方的捕獲list
                                try:
                                    server.save_white_captured_pieces(self.room_id, black_piece)  # 發送被捕獲的黑方棋子給server
                                except ConnectionRefusedError:
                                    messagebox.showinfo("提示", msg)
                                    pygame.quit()
                                    w.open_login_window()
                                    return

                                if self.black_pieces[black_piece] == "king":
                                    self.winner == "white"
                                    try:
                                        server.save_winner(self.room_id, "white")
                                    except ConnectionRefusedError:
                                        messagebox.showinfo("提示", msg)
                                        pygame.quit()
                                        w.open_login_window()
                                        return
                                    try:
                                        server.save_win_reason(self.room_id, 1)
                                    except ConnectionRefusedError:
                                        messagebox.showinfo("提示", msg)
                                        pygame.quit()
                                        w.open_login_window()
                                        return
                                    self.win_reason = 1
                                self.black_pieces.pop(black_piece)  # 黑方棋子list剔除被捕獲到的棋子
                                self.black_locations.pop(black_piece)  # 黑方棋子位置同樣要剔除被捕獲到的棋子。註：black_pieces和black_locations是聯動的
                                try:
                                    server.reset_draw_step(self.room_id)  # 因爲有捕獲到黑方棋子，所以讓server重置記錄的和棋回合
                                except ConnectionRefusedError:
                                    messagebox.showinfo("提示", msg)
                                    pygame.quit()
                                    w.open_login_window()
                                    return
                            elif click_cord not in self.black_locations:  # 如果這次移動沒有捕獲到黑方棋子，讓server計算一次合棋回合
                                try:
                                    server.add_draw_step(self.room_id)
                                except ConnectionRefusedError:
                                    messagebox.showinfo("提示", msg)
                                    pygame.quit()
                                    w.open_login_window()
                                    return
                            try:
                                server.save_white_location(self.room_id, self.white_locations, self.my_color)  # 發送最新的白方位置給server
                                server.save_black_location(self.room_id, self.black_locations, self.my_color)  # 發送最新的黑方位置給server
                            except ConnectionRefusedError:
                                messagebox.showinfo("提示", msg)
                                pygame.quit()
                                w.open_login_window()
                                return
                            self.white_options = self.check_options(self.white_pieces, self.white_locations, "white")  # 重新檢查所有棋子的合法路徑。
                            self.black_options = self.check_options(self.black_pieces, self.black_locations, "black")
                            try:
                                server.save_turn(self.room_id, 0)  # 通知server回合結束
                            except ConnectionRefusedError:
                                messagebox.showinfo("提示", msg)
                                pygame.quit()
                                w.open_login_window()
                                return
                            self.turn_step = 2  # 進入等待狀態
                            self.selection = -1  # 重置玩家選擇的棋子的index
                            self.valid_moves = []  # 重置螢幕顯示之合法路徑的參數

                    if self.turn_step > 2:  # 和上面那一段一樣，但是這回輪到黑方操作
                        if (event.pos[0] >= 921 and event.pos[0] <= 1131) and (event.pos[1] >= 494 and event.pos[1] <= 597): # 點擊投降
                            self.winner = "white"
                            try:
                                server.save_winner(self.room_id, "white")  # 發送勝利者是白方給server，註：現在是黑方回合
                                server.save_win_reason(self.room_id, 3)  # 發送遊戲結束原因給server，3代表棋手投降
                            except ConnectionRefusedError:
                                messagebox.showinfo("提示", msg)
                                pygame.quit()
                                w.open_login_window()
                                return
                            self.win_reason = 3

                        if click_cord in self.black_locations:     # 當鼠標點擊的坐標和black_locations中的某個座標一樣
                            self.selection = self.black_locations.index(click_cord)     #黑方選擇了一個棋子
                            if self.turn_step == 3:
                                self.turn_step = 4     # turn_step=3 表示黑方選擇了一個棋子，現在可以開始放置棋子
                        if click_cord in self.valid_moves and self.selection != -1:
                            self.black_locations[self.selection] = click_cord    #更新選擇的棋子的位置
                            self.thought_time += + self.extra_second
                            try:
                                server.update_time(self.room_id, "black", self.thought_time)
                            except ConnectionRefusedError:
                                messagebox.showinfo("提示", msg)
                                pygame.quit()
                                w.open_login_window()
                                return
                            if click_cord in self.white_locations:  # 當黑方放置棋子的位置有白方的棋子
                                white_piece = self.white_locations.index(click_cord)  # 從滑鼠坐標獲取白方棋子的信息
                                self.black_captured_pieces.append(self.white_pieces[white_piece])  # 把被捕獲到的白方棋子加進黑方的捕獲list
                                try:
                                    server.save_black_captured_pieces(self.room_id, white_piece)  # 發送被捕獲的白方棋子給server
                                except ConnectionRefusedError:
                                    messagebox.showinfo("提示", msg)
                                    pygame.quit()
                                    w.open_login_window()
                                    return

                                if self.white_pieces[white_piece] == "king":
                                    self.winner == "black"
                                    try:
                                        server.save_winner(self.room_id, "black")
                                        server.save_win_reason(self.room_id, 1)
                                    except ConnectionRefusedError:
                                        messagebox.showinfo("提示", msg)
                                        pygame.quit()
                                        w.open_login_window()
                                        return
                                    self.win_reason = 1
                                self.white_pieces.pop(white_piece)  # 白方棋子list剔除被捕獲到的棋子
                                self.white_locations.pop(white_piece)  # 白方棋子位置同樣要剔除被捕獲到的棋子。註：white_pieces和white_locations是聯動的
                                try:
                                    server.reset_draw_step(self.room_id)  # 因爲有捕獲到白方棋子，所以讓server重置記錄的和棋回合
                                except ConnectionRefusedError:
                                    messagebox.showinfo("提示", msg)
                                    pygame.quit()
                                    w.open_login_window()
                                    return
                            elif click_cord not in self.white_locations:  # 如果這次移動沒有捕獲到白方棋子，讓server計算一次合棋回合
                                try:
                                    server.add_draw_step(self.room_id)
                                except ConnectionRefusedError:
                                    messagebox.showinfo("提示", msg)
                                    pygame.quit()
                                    w.open_login_window()
                                    return

                            try:
                                server.save_black_location(self.room_id, self.black_locations, self.my_color)  # 發送最新的黑方位置給server
                                server.save_white_location(self.room_id, self.white_locations, self.my_color)  # 發送最新的白方位置給server
                            except ConnectionRefusedError:
                                messagebox.showinfo("提示", msg)
                                pygame.quit()
                                w.open_login_window()
                                return

                            self.black_options = self.check_options(self.black_pieces, self.black_locations, "black")
                            self.white_options = self.check_options(self.white_pieces, self.white_locations, "white")  # 重新檢查所有棋子的合法路徑。
                            try:
                                server.save_turn(self.room_id, 3)  # 通知server回合結束
                            except ConnectionRefusedError:
                                messagebox.showinfo("提示", msg)
                                pygame.quit()
                                w.open_login_window()
                                return
                            self.turn_step = 2  # 進入等待狀態
                            self.selection = -1  # 重置玩家選擇的棋子的index
                            self.valid_moves = []  # 重置螢幕顯示之合法路徑的參數

            if self.game_over is False and self.winner != "":
                global battle
                self.game_over = True
                battle = False
            elif self.game_over is False and (counter % 10 == 0):
                try:
                    return_win_check = server.check_winner(self.room_id)
                    return_win_reason = server.check_win_reason(self.room_id)
                except ConnectionRefusedError:
                    messagebox.showinfo("提示", msg)
                    pygame.quit()
                    w.open_login_window()
                    return


                if return_win_check != "":
                    self.winner = return_win_check

                if return_win_reason != 0:
                    self.win_reason = return_win_reason

            pygame.display.flip()
        pygame.quit()
        w.open_lobby_window()

def align_text(text, width):
    text_width = sum(1 + (unicodedata.east_asian_width(char) in ['W', 'F']) for char in text)
    padding = max(0, width - text_width)
    return text + " " * padding


def is_wide_character(char):
    width = unicodedata.east_asian_width(char)
    return width in ('W', 'F', 'A')


if __name__ == "__main__":

    # if len(sys.argv) < 2:
    #         print("Usage: Client.py ServerIP")
    #         exit(1)
    #server = xmlrpc.client.ServerProxy("http://" + sys.argv[1] + ":" + str(port))
    server = xmlrpc.client.ServerProxy("http://" + "127.0.0.1" + ":" + str(port))
    w = window()
    w.login_window.mainloop()

    if user:
        try:
            server.logout(user)
        except ConnectionRefusedError:
            pass
        try:
            if opponent:
                server.delete_opponent(opponent)
        except ConnectionRefusedError:
            pass
        except Exception:
            pass

        try:
            if room:
                server.delete_room(user)
        except ConnectionRefusedError:
            pass
        except Exception:
            pass