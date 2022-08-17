import tkinter as tk
import pymongo
import os
import dotenv

dotenv.load_dotenv()

LINK = os.getenv("MONGO_LINK")

class mongo:
    def __init__(self, link: str):
        self.client = pymongo.MongoClient(link)
        self.db = self.client.vdv_hacks
        self.user_credentials = self.db.user_credentials
        self.user_tasks = self.db.user_tasks
    
    def new_user(self, username, password):
        self.user_credentials.insert_one({"username": username, "password": password})
    
    def is_user(self, username, password):
        result1 = self.user_credentials.find_one({"username": username, "password": password})
        result2 = self.user_credentials.find_one({"username": username})
        if result1 is None or result2 is None:
            return False
        return True

db = mongo(LINK)
    
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
        if self.db.is_user(username, password):
            result = tk.Label(self.window, text = "Success!", fg = "green")
        else:
            result = tk.Label(self.window, text = "Username of passowrd is invalid", fg = "red")
        result.grid(row = 4, column = 0)


    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.db.is_user(username, password):
            result = tk.Label(self.window, text = "There is already an account with this username", fg = "red")
        else:
            self.db.new_user(username, password)
            result = tk.Label(self.window, text = "Account created", fg = "green")
        result.grid(row = 4, column = 0)

object = login(db)