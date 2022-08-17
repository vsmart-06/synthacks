import tkinter as tk
import sqlite3

class database:
    def __init__(self):
        self.db = sqlite3.connect("synthacks/vdv_hacks.db")
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS user_credentials (username TEXT PRIMARY KEY, password TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS user_tasks (id INTEGER PRIMARY KEY, username TEXT, password TEXT, done INTEGER, date TEXT)")
    
    def new_user(self, username, password):
        self.cursor.execute(f"INSERT INTO user_credentials VALUES ('{username}', '{password}')")
    
    def is_user(self, username, password):
        result1 = self.cursor.execute(f"SELECT * FROM user_credentials WHERE username = '{username}' AND password = '{password}'").fetchone()
        result2 = self.cursor.execute(f"SELECT * FROM user_credentials WHERE username = '{username}'").fetchone()
        if result1 == None or result2 == None:
            return False
        return True
        

db = database()

class login:
    def __init__(self, db):
        self.db = db
        self.window = tk.Tk()
        self.window.title = "Login"
        username_label = tk.Label(self.window, text = "Username: ")
        password_label = tk.Label(self.window, text = "Password: ")
        username_label.grid(row=0, column=0)
        password_label.grid(row=1, column=0)
        self.username_entry = tk.Entry(self.window)
        self.password_entry = tk.Entry(self.window)
        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        login_button = tk.Button(self.window, text = "Login", command = self.login)
        signup_button = tk.Button(self.window, text = "Sign Up", command = self.signup)
        login_button.grid(row = 2, column = 0)
        signup_button.grid(row = 3, column = 0)
        self.window.mainloop()
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.result.destroy()
        except AttributeError:
            pass
        if self.db.is_user(username, password):
            self.result = tk.Label(self.window, text = "Success!", fg = "green")
        else:
            self.result = tk.Label(self.window, text = "Username or password is invalid", fg = "red")
        self.result.grid(row = 4, column = 0)


    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.result.destroy()
        except AttributeError:
            pass
        if self.db.is_user(username, password):
            self.result = tk.Label(self.window, text = "There is already an account with this username", fg = "red")
        else:
            self.db.new_user(username, password)
            self.result = tk.Label(self.window, text = "Account created", fg = "green")
        self.result.grid(row = 4, column = 0)

object = login(db)