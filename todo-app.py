import json
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import messagebox
from datetime import datetime

# style = ttk.Style()
# style.configure("Custom.TButton", foreground="black", background="light blue")

class TodoApp(tk.Tk):
    

    def __init__(self):
        super().__init__()
        self.configure(bg="light blue")
        self.title("To-Do")

        self.todo_items = []
        self.load_todo_items()  # Load todo items from file

        self.todo_listbox = tk.Listbox(self)
        self.todo_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.new_todo_entry = ttk.Entry(self)
        self.new_todo_entry.pack(padx=10, pady=(0, 5), fill=tk.BOTH)

        add_button = ttk.Button(self, text="Add", command=self.add_todo)
        add_button.pack(padx=10, pady=(0, 5), fill=tk.BOTH)

        edit_button = ttk.Button(self, text="Edit", command=self.edit_todo, style=self.configure(bg="sky blue"))
        edit_button.pack(padx=10, pady=(0, 5), fill=tk.BOTH)

        delete_button = ttk.Button(self, text="Delete", command=self.delete_todo)
        delete_button.pack(padx=10, pady=(0, 5), fill=tk.BOTH)

        self.calendar = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.pack(padx=10, pady=(0, 5), fill=tk.BOTH)

        self.time_entry = ttk.Entry(self)
        self.time_entry.insert(0, "00:00")
        self.time_entry.pack(padx=10, pady=(0, 5), fill=tk.BOTH)

        self.update_button = ttk.Button(self, text="Update", command=self.update_todo)
        self.update_button.pack(padx=10, pady=(0, 5), fill=tk.BOTH)

        self.update_todo_list()

    def add_todo(self):
        todo_text = self.new_todo_entry.get()
        if todo_text:
            date = self.calendar.get_date()
            time = self.time_entry.get()
            if not self.validate_datetime(date, time):
                messagebox.showerror("Error", "Please enter a valid date and time.")
                return
            datetime_str = f"{date} {time}"
            self.todo_items.append({"text": todo_text, "datetime": datetime_str})
            self.new_todo_entry.delete(0, tk.END)
            self.update_todo_list()
        self.save_todo_items()

    def edit_todo(self):
        selected_index = self.todo_listbox.curselection()
        if selected_index:
            todo = self.todo_items[selected_index[0]]
            self.new_todo_entry.delete(0, tk.END)
            self.new_todo_entry.insert(0, todo["text"])
            self.calendar.set_date(todo["datetime"].split()[0])
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, todo["datetime"].split()[1])
        self.save_todo_items()

    def update_todo(self):
        selected_index = self.todo_listbox.curselection()
        if selected_index:
            todo = self.todo_items[selected_index[0]]
            todo_text = self.new_todo_entry.get()
            date = self.calendar.get_date()
            time = self.time_entry.get()
            if not self.validate_datetime(date, time):
                messagebox.showerror("Error", "Please enter a valid date and time.")
                return
            datetime_str = f"{date} {time}"
            todo["text"] = todo_text
            todo["datetime"] = datetime_str
            self.new_todo_entry.delete(0, tk.END)
            self.update_todo_list()
        self.save_todo_items()

    def delete_todo(self):
        selected_index = self.todo_listbox.curselection()
        if selected_index:
            del self.todo_items[selected_index[0]]
            self.update_todo_list()
        self.save_todo_items()

    def validate_datetime(self, date, time):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            datetime.strptime(time, "%H:%M")
            return True
        except ValueError:
            return False

    def update_todo_list(self):
        self.todo_listbox.delete(0, tk.END)
        for item in self.todo_items:
            self.todo_listbox.insert(tk.END, f"{item['text']} - {item['datetime']}")
    
    def load_todo_items(self):
        try:
            with open("todo_items.json", "r") as f:
                self.todo_items = json.load(f)
        except FileNotFoundError:
            self.todo_items = []

    def save_todo_items(self):
        with open("todo_items.json", "w") as f:
            json.dump(self.todo_items, f)

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()


# import tkinter as tk
# from tkinter import ttk

# class TodoApp(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Todo App")

#         self.todo_items = []

#         self.todo_listbox = tk.Listbox(self)
#         self.todo_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

#         self.new_todo_entry = ttk.Entry(self)
#         self.new_todo_entry.pack(padx=10, pady=(0, 10), fill=tk.BOTH)

#         add_button = ttk.Button(self, text="Add", command=self.add_todo)
#         add_button.pack(padx=10, pady=(0, 10), fill=tk.BOTH)

#         self.update_todo_list()

#     def add_todo(self):
#         todo_text = self.new_todo_entry.get()
#         if todo_text:
#             self.todo_items.append(todo_text)
#             self.new_todo_entry.delete(0, tk.END)
#             self.update_todo_list()

#     def update_todo_list(self):
#         self.todo_listbox.delete(0, tk.END)
#         for item in self.todo_items:
#             self.todo_listbox.insert(tk.END, item)

# if __name__ == "__main__":
#     app = TodoApp()
#     app.mainloop()


