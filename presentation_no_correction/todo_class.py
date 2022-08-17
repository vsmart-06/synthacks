import tkinter as tk
import sqlite3


class todo:
    def __init__(self, username, db):
        self.username = username
        self.db = db
        self.window = tk.Tk()
        self.window.title = "To Do List"
        self.on = []
        self.rows = []
        self.check_states = []
        t = self.db.pull_tasks(self.username)
        self.tasks = []
        for i in t:
            self.tasks.append(i[1])
            self.check_states.append(i[2])
        self.num_rows = len(self.tasks)+1
        for x in range(self.num_rows):
            self.on.append(tk.IntVar())
            checkbox = tk.Checkbutton(self.window, variable = self.on[x], command = lambda m = self.on[x], n = x: self.onCheck(m, n))
            entry = tk.Entry(self.window)
            button_tick = tk.Button(self.window, text = "✔", command = lambda m = x: self.onTick(m))
            button_cross = tk.Button(self.window, text = "❌", command = lambda m = x: self.onCross(m))
            self.rows.append([checkbox, entry, button_tick, button_cross])
        self.tasks.append("Enter a task")
        self.check_states.append(0)
        for i in range(len(self.rows)):
            row = self.rows[i]
            checkbox = row[0]
            entry = row[1]
            button_tick = row[2]
            button_cross = row[3]
            checkbox.grid(row=i, column=0)
            entry.grid(row=i, column=1)
            entry.insert(0, self.tasks[i])
            entry.bind("<FocusIn>", lambda event, m = i: self.rem_text_temp(event, m))
            entry.bind("<FocusOut>", lambda event, m = i: self.insert_text_temp(event, m))
            button_tick.grid(row=i, column=2)
            button_cross.grid(row=i, column=3)
            if i == len(self.rows) - 1:
                button_cross.grid_remove()
                checkbox.grid_remove()
            else:
                self.onCheck(t[i][2], i)
                if self.check_states[i] == 1:
                    checkbox.select()

        self.window.mainloop()
    
    def rem_text_temp(self, e, i):
        row = self.rows[i]
        entry = row[1]
        content = entry.get()
        if content == "Enter a task" and row == self.rows[-1]:
            entry.delete(0, "end")
    
    def insert_text_temp(self, e, i):
        row = self.rows[i]
        entry = row[1]
        content = entry.get()
        if content == "" and row == self.rows[-1]:
            entry.insert(0, "Enter a task")
    
    def onTick(self, index):
        checkbox = self.rows[index][0]
        button_tick = self.rows[index][2]
        button_cross = self.rows[index][3]
        entry = self.rows[index][1]
        self.tasks[index] = entry.get()
        checkbox.grid()
        button_cross.grid()
        try:
            self.rows[index+1][1]
            self.tasks[index] = entry.get()
        except IndexError:
            self.num_rows += 1
            self.on.append(tk.IntVar())
            checkbox = tk.Checkbutton(self.window, variable = self.on[self.num_rows-1], command = lambda m = self.on[self.num_rows-1], n = self.num_rows - 1: self.onCheck(m, n))
            entry = tk.Entry(self.window)
            button_tick = tk.Button(self.window, text = "✔", command = lambda m = self.num_rows-1: self.onTick(m))
            button_cross = tk.Button(self.window, text = "❌", command = lambda m = self.num_rows-1: self.onCross(m))
            self.rows.append([checkbox, entry, button_tick, button_cross])
            self.tasks.append("Enter a task")
            self.check_states.append(0)
            i = self.num_rows - 1
            row = self.rows[i]
            checkbox = row[0]
            entry = row[1]
            button_tick = row[2]
            button_cross = row[3]
            checkbox.grid(row=i, column=0)
            checkbox.grid_remove()
            entry.grid(row=i, column=1)
            entry.insert(0, self.tasks[i])
            entry.bind("<FocusIn>", lambda event, m = i: self.rem_text_temp(event, m))
            entry.bind("<FocusOut>", lambda event, m = i: self.insert_text_temp(event, m))
            button_tick.grid(row=i, column=2)
            button_cross.grid(row=i, column=3)
            button_cross.grid_remove()
        self.db.push_tasks(self.username, self.tasks, self.check_states)
    
    def onCross(self, index):
        checkbox = self.rows[index][0]
        entry = self.rows[index][1]
        self.db.del_task(self.username, self.tasks[index])
        checkbox.destroy()
        entry.destroy()
        self.rows[index][2].destroy()
        self.rows[index][3].destroy()
        self.tasks.pop(index)
        self.on.pop(index)
        self.check_states.pop(index)
        self.rows = []
        self.num_rows -= 1
        for widget in self.window.winfo_children():
            widget.destroy()
        for x in range(self.num_rows):
            self.on.append(tk.IntVar())
            checkbox = tk.Checkbutton(self.window, variable = self.on[x], command = lambda m = self.on[x], n = x: self.onCheck(m, n))
            entry = tk.Entry(self.window)
            button_tick = tk.Button(self.window, text = "✔", command = lambda m = x: self.onTick(m))
            button_cross = tk.Button(self.window, text = "❌", command = lambda m = x: self.onCross(m))
            self.rows.append([checkbox, entry, button_tick, button_cross])
        self.tasks.append("Enter a task")
        self.check_states.append(0)
        for i in range(len(self.rows)):
            row = self.rows[i]
            checkbox = row[0]
            entry = row[1]
            button_tick = row[2]
            button_cross = row[3]
            checkbox.grid(row=i, column=0)
            entry.grid(row=i, column=1)
            entry.insert(0, self.tasks[i])
            entry.bind("<FocusIn>", lambda event, m = i: self.rem_text_temp(event, m))
            entry.bind("<FocusOut>", lambda event, m = i: self.insert_text_temp(event, m))
            button_tick.grid(row=i, column=2)
            button_cross.grid(row=i, column=3)
            if i == len(self.rows) - 1:
                button_cross.grid_remove()
                checkbox.grid_remove()
            else:
                self.onCheck(self.check_states[i], i)
                if self.check_states[i] == 1:
                    checkbox.select()
    
    def onCheck(self, t, index):
        row = self.rows[index]
        entry = row[1]
        try:
            var = t.get()
        except AttributeError:
            var = t
        if var == 1:
            self.check_states[index] = 1
            contents = entry.get()
            loc = entry.grid_info()
            entry.destroy()
            label = tk.Label(self.window, text = contents, fg = "green")
            row[1] = label
            row[2].grid_remove()
            self.rows[index] = row
            self.tasks[index] = contents
            label.grid(row=loc["row"], column=loc["column"])
        else:
            if type(t) != int:
                self.check_states[index] = 0
                contents = entry["text"]
                loc = entry.grid_info()
                entry.destroy()
                entry = tk.Entry(self.window)
                row[1] = entry
                row[2].grid()
                self.rows[index] = row
                self.tasks[index] = contents
                entry.grid(row=loc["row"], column=loc["column"])
                entry.insert(0, contents)
        self.db.push_tasks(self.username, self.tasks, self.check_states)