import tkinter as tk
from tkinter import ttk
import FileBookPage
import sqlite3
import databasenew
import os
from tkinter import messagebox as msg
import languagepack
from centerscreen import center_screen_geometry
import treeview
import calendar_win
import todolist



class Profile:
    def __init__(self):
        self.win = tk.Tk()
        self.db = databasenew.FileManager()
        self.selected_language = tk.StringVar(value="en")
        self.i18n = languagepack.I18N(language=self.selected_language.get())
        self.window_title = self.i18n.title_profile
        self.win.title(self.window_title)
        self.win.geometry(center_screen_geometry(screen_width=self.win.winfo_screenwidth(),
                                                 screen_height=self.win.winfo_screenheight(),
                                                 window_width=500,
                                                 window_height=500))
        self.win.resizable(False, False)
        self.win.configure(bg="#D7C6EE")
        self.create_widgets()
        self.bind_widgets()
        self.win.protocol("WM_DELETE_WINDOW", self.close_window)


    def reload_gui_text(self, language):
        self.i18n = languagepack.I18N(language)
        self.win.title(self.i18n.title_profile)
        self.btn1.configure(text=self.i18n.create_profile_database)
        self.btn2.configure(text=self.i18n.title_filebook)
        self.btn3.configure(text=self.i18n.clear_profile_database)
        self.habitTrackerLabel.configure(text=self.i18n.habitTrackerLabel) #alıskanlık takibi
        self.calendarLabel.configure(text=self.i18n.calendarLabel) # takvim
        self.ToDoList.configure(text=self.i18n.ToDoList)   # yapılacaklar listesi

        self.database_exist = self.i18n.database_exist
        self.database_created = self.i18n.database_created
        self.database_failed = self.i18n.database_failed
        self.database_cleared = self.i18n.database_cleared
        self.cleared_failed = self.i18n.cleared_failed
        self.exit_title = self.i18n.exit_title
        self.sure_exit = self.i18n.sure_exit


    def create_widgets(self):
        self.btn1 = ttk.Button(self.win, text=self.i18n.create_profile_database, command=self.create_profil_database)
        self.btn2 = ttk.Button(self.win, text=self.i18n.title_filebook, command=self.show_files_window)
        self.btn3 = ttk.Button(self.win, text=self.i18n.clear_profile_database,  command=self.clear_db)
        self.habitTrackerLabel=ttk.Button(self.win,text=self.i18n.habitTrackerLabel,command=self.double_click_event)
        self.calendarLabel=ttk.Button(self.win,text=self.i18n.calendarLabel,command=self.double_click_event2)
        self.ToDoList=ttk.Button(self.win,text=self.i18n.ToDoList, command=self.open_todo_list)
        self.win.columnconfigure(0, weight=1)
        self.btn1.grid(row=0, column=0,sticky="nsew", pady=10, padx=10,ipady=18)
        self.btn3.grid(row=1, column=0,sticky="nsew", pady=10, padx=10,ipady=18)
        self.btn2.grid(row=2, column=0,sticky="nsew", pady=10, padx=10,ipady=18)
        self.habitTrackerLabel.grid(row=3, column=0,sticky="nsew", pady=10, padx=10,ipady=18)
        self.calendarLabel.grid(row=4,column=0,sticky="nsew", pady=10, padx=10,ipady=18)
        self.ToDoList.grid(row=5,column=0,sticky="nsew", pady=10, padx=10,ipady=18)

        self.context_menu = tk.Menu(self.win, tearoff=False)
        self.context_menu.add_radiobutton(label="English", variable=self.selected_language, value="en",
                                          command=lambda: self.reload_gui_text("en"))
        self.context_menu.add_radiobutton(label="Türkçe", variable=self.selected_language, value="tr",
                                          command=lambda: self.reload_gui_text("tr"))

    def create_database(self):
        db_file = "filebook.db"
        if os.path.exists(db_file):
            return msg.showinfo(title=self.i18n.title_profile, message=self.i18n.database_exist)
        try:
            self.db.create_database()
            msg.showinfo(title=self.i18n.title_profile, message=self.i18n.database_created)
        except sqlite3.Error as err:
            msg.showerror(title=self.i18n.title_profile, message=self.i18n.database_failed + "\n" + str(err))

    def clear_db(self):
        try:
            self.db.clear_database()
            msg.showinfo(title=self.i18n.title_profile, message=self.i18n.database_cleared)
        except sqlite3.Error as err:
            msg.showerror(title=self.i18n.title_profile, message=self.i18n.cleared_failed + "\n" + str(err))

    def show_files_window(self):
        self.win.withdraw()
        self.win_files = FileBookPage.FileBookPage(self)
        self.win_files.grab_set()

    def create_profil_database(self):
        self.create_database()

    def close_window(self):
        message = msg.askyesno(title=self.i18n.exit_title, message=self.i18n.sure_exit)
        if message:
            self.win.destroy()

    def bind_widgets(self):
        self.win.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.tk_popup(x=event.x_root, y=event.y_root)

    def double_click_event(self):
        self.win.withdraw()
        self.win2=treeview.HabitTracker(self)
        self.win2.title("Habit Tracker Window")
        self.win2.grab_set()

    def double_click_event2(self):
        self.win.withdraw()
        self.win4=calendar_win.CalendarTracker(self)
        self.win4.title("Calendar")
        self.win4.grab_set()

    def open_todo_list(self):
        self.win.withdraw()
        self.todo = todolist.TodoList(parent=self)
        self.todo.grab_set()


app = Profile()
app.win.mainloop()
