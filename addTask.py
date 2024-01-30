# GUI for inserting new records into database.

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import sqlite3
import databasenew
import languagepack
from centerscreen import center_screen_geometry


class AddTask(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.db = databasenew.FileManager()
        self.parent = parent
        self.selected_language = tk.StringVar(value="en")
        self.i18n = languagepack.I18N(self.selected_language.get())
        self.geometry(center_screen_geometry(screen_width=self.winfo_screenwidth(),
                                             screen_height=self.winfo_screenheight(),
                                             window_width=330,
                                             window_height=165))
        self.title(parent.selected_date)
        self.resizable(False, False)
        self.task = tk.StringVar()
        self.time = parent.selected_date
        self.create_widgets()
        self.bind_widgets()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def reload_gui_text(self, language):
        self.i18n = languagepack.I18N(language)
        self.lbl_task.configure(text=self.i18n.rem_name)
        self.lbl_time.configure(text=self.i18n.lbl_time)
        self.btn_add.configure(text=self.i18n.add_btn)
        self.done=self.i18n.done
        self.task_saved=self.i18n.task_saved
        self.failed_task_added=self.i18n.failed_task_added
        self.empty_rem_msg=self.i18n.empty_rem_msg
        self.not_added=self.i18n.not_added
        self.warning=self.i18n.warning

    def save_and_add_task(self):
        self.save_task()
        self.add_tasks()

    def save_task(self):
        try:
            task=self.txt_task.get().strip()
            if not task:
                return
            self.db.add_reminder(task=self.txt_task.get(), time=self.parent.selected_date)
            msg.showinfo(self.i18n.done, self.i18n.rem_saved)
            
            self.txt_task.focus_set()
        except (tk.TclError, sqlite3.Error) as err:
            msg.showerror( message=self.i18n.failed_rem_added + str(err))

    def clear_tasks(self):
        self.txt_task.delete(0, "end")
        

    def add_tasks(self):
        try:     
            task=self.txt_task.get().strip()
            if not task:
                msg.showwarning(self.i18n.warning,self.i18n.empty_rem_msg)      
                return  
            task=self.txt_task.get()
            time=self.parent.selected_date
            self.parent.add_task(task,time)
            self.clear_tasks()
            self.destroy()  
        except Exception:
            print(self.i18n.not_added)

    def create_widgets(self):
        frame=ttk.Frame(self)
        
        self.lbl_task = ttk.Label(frame, text=self.i18n.rem_name)
        self.lbl_task.grid(column=0, row=1, padx=15, pady=15)
        self.lbl_time = ttk.Label(frame, text=self.i18n.lbl_time)
        self.lbl_time.grid(column=0, row=0, padx=15, pady=15)

        self.txt_task = ttk.Entry(frame, textvariable=self.task, width=30)
        self.txt_task.grid(column=1, row=1, padx=15, pady=15)
        self.txt_time = ttk.Label(frame, text=self.parent.selected_date, width=35)
        self.txt_time.grid(column=1, row=0, padx=15, pady=15)

        self.btn_add = ttk.Button(frame, text=self.i18n.add_btn, command=self.save_and_add_task)
        self.btn_add.grid(column=0, row=3, columnspan=2, pady=(0, 15))
        

        self.context_menu = tk.Menu(frame, tearoff=False)
        self.context_menu.add_radiobutton(label="English", variable=self.selected_language, value="en",
                                          command=lambda: self.reload_gui_text("en"))
        self.context_menu.add_radiobutton(label="Türkçe", variable=self.selected_language, value="tr",
                                          command=lambda: self.reload_gui_text("tr"))
        frame.pack()


    def bind_widgets(self):
        self.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.tk_popup(x=event.x_root, y=event.y_root)

    def close_window(self):
        self.parent.deiconify()
        self.destroy()
