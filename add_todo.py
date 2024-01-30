import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox as msg
import databasenew
import sqlite3
from datetime import datetime
import languagepack

class AddTask(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.db =databasenew.FileManager()
        self.parent = parent
        self.geometry("370x400+710+290")
        self.resizable(False, False)
        self.i18n = languagepack.I18N(language=parent.selected_lang.get())
        self.title(self.i18n.add_task_btn)
        self.task = tk.StringVar()
        self.priority = tk.StringVar()
        self.tags = tk.StringVar()
        self.selected_tags_list = []
        self.selected_tags_str = ""
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def clear_deadline(self):
        #self.deadline.set_date(None)
        self.deadline.delete(0,"end")
        
    def clear_dodate(self):
        self.dodate.delete(0,"end")

    def clear_inputs(self):
        self.txt_task.delete(0,"end")
        self.clear_deadline()
        self.clear_dodate()
        self.priority_combo.set("")
        self.tag_combo.set("")
        self.selected_tags_str = ""
        self.lbl_selected_tags.configure(text=self.selected_tags_str)

    def format_date_str(self, str):
        date = datetime.strptime(str, "%m/%d/%y")
        date = date.strftime("%d/%m/%Y")
        return date


    def save_task(self):
        try:
            cur_task = self.task.get().strip()
            # don't allow empty task name
            if not cur_task:
                msg.showinfo(title=self.i18n.warning, message=self.i18n.msg_enter_task)
                return 

            #format dates
            formatted_deadline = ""
            if self.deadline.get():
                try:
                    formatted_deadline = self.format_date_str(self.deadline.get())
                except ValueError:
                    msg.showinfo(title=self.i18n.error, message=self.i18n.invalid_date_msg)
                    return

            formatted_dodate = ""
            if self.dodate.get():
                try:
                    formatted_dodate = self.format_date_str(self.dodate.get())
                except ValueError:
                    msg.showinfo(title=self.i18n.error, message=self.i18n.invalid_date_msg)
                    return

            # add to database
            new_task_id = self.db.add_task(cur_task, formatted_deadline, formatted_dodate, self.priority.get(), self.selected_tags_str)
            # add task to treeview
            new_task_row = self.db.get_row(new_task_id)
            self.parent.tv.insert(parent="", index="end", values=new_task_row)
            
            msg.showinfo(title=self.i18n.success, message=self.i18n.task_saved)
            self.txt_task.focus_set()
            self.clear_inputs()
            

        except sqlite3.Error as err:
            msg.showerror(title=self.i18n.error, message=f"{self.i18n.failed_task_added}\n" + str(err))

    def select_tag(self):
        current = self.tags.get()
        if current not in self.selected_tags_list:
            self.selected_tags_list.append(current)
            
        self.selected_tags_str = ", ".join(self.selected_tags_list)
        self.lbl_selected_tags.configure(text=self.selected_tags_str)
        

    def create_widgets(self):
        self.lbl_task = ttk.Label(self, text=f"{self.i18n.task}:")
        self.lbl_task.grid(column=0, row=0, padx=(40), pady=20, sticky="w")
        self.txt_task = ttk.Entry(self, textvariable=self.task, width=30)
        self.txt_task.grid(column=1, row=0, padx=(0,10), pady=20, sticky="w", columnspan=2)

        #deadline picker
        self.lbl_deadline = ttk.Label(self, text=f"{self.i18n.deadline}:")
        self.lbl_deadline.grid(column=0, row=1, padx=(40), pady=(0,20), sticky="w")
        self.deadline = DateEntry(self, width=15)
        self.deadline.grid(column=1, row=1, pady=(0,20), sticky="w")
        self.btn_clear_deadline = ttk.Button(self, text=self.i18n.clear, command=self.clear_deadline)
        self.btn_clear_deadline.grid(column=2, row=1, pady=(0,20))

        #do date picker
        self.lbl_dodate = ttk.Label(self, text=f"{self.i18n.dodate}:")
        self.lbl_dodate.grid(column=0, row=2,  padx=(40), pady=(0,20), sticky="w")
        self.dodate = DateEntry(self, width=15)
        self.dodate.grid(column=1, row=2, pady=(0,20), sticky="w")
        self.btn_clear_dodate = ttk.Button(self, text=self.i18n.clear, command=self.clear_dodate)
        self.btn_clear_dodate.grid(column=2, row=2, pady=(0,20))

        #reset calendars
        self.clear_deadline()
        self.clear_dodate()

        #priority
        self.lbl_priority = ttk.Label(self, text=f"{self.i18n.priority}:")
        self.lbl_priority.grid(column=0, row=3, padx=40, pady=(0,20), sticky="w")
        self.priority_combo = ttk.Combobox(self, width=20, textvariable=self.priority, state="readonly")
        self.priority_combo["values"] = ("low", "medium", "high")
        self.priority_combo.grid(column=1, columnspan=2, row=3, pady=(0,20),  sticky="w")
        self.priority.set("low")

        #tag ## TODO change to the listbox or treview or whatever for multi selection
        self.lbl_tag = ttk.Label(self, text=f"{self.i18n.tag}:")
        self.lbl_tag.grid(column=0, row=4, padx=40, pady=(0,20), sticky="w")

        
        self.tag_combo = ttk.Combobox(self, width=15, textvariable=self.tags, state="normal")
        self.tag_combo["values"] = ("school", "work")
        self.tag_combo.grid(column=1, row=4, pady=(0,20),  sticky="w")
        self.btn_tag_add = ttk.Button(self, text=self.i18n.select,command=self.select_tag)
        self.btn_tag_add.grid(column=2, row=4, pady=(0,20))

        #show tags
        self.lbl_selected_tags = ttk.Label(self, text=self.selected_tags_str, wraplength=250)
        self.lbl_selected_tags.grid(column=0, columnspan=3, row=5, pady=(0,20))

        # add button
        self.btn_add = ttk.Button(self, text=self.i18n.add_btn, command=self.save_task)
        self.btn_add.grid(column=0, columnspan=3, row=6)
        
        
      
    def close_window(self):
        self.destroy()
