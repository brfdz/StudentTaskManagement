import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox as msg
import databasenew
import sqlite3
from datetime import datetime
import languagepack

class EditTask(tk.Toplevel):
    def __init__(self, parent, row_id, task_id, task, deadline, dodate, priority, tags):
        super().__init__()
        self.db =databasenew.FileManager()
        self.parent = parent
        self.geometry("370x400+710+290")
        self.resizable(False, False)
        self.i18n = languagepack.I18N(language=parent.selected_lang.get())
        self.title(self.i18n.update_task)
        self.task = tk.StringVar(value= task)
        self.priority = tk.StringVar(value=priority)
        self.tags = tk.StringVar(value=tags)
        self.selected_tags = tags
        self.task_id = task_id
        self.row_id = row_id
        self.create_widgets()
        self.set_dates(deadline, dodate)
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def clear_deadline(self):
        #self.deadline.set_date(None)
        self.deadline_entry.delete(0,"end")
        
    def clear_dodate(self):
        self.dodate_entry.delete(0,"end")

    def format_date_str(self, str):
        date = datetime.strptime(str, "%m/%d/%y")
        date = date.strftime("%d/%m/%Y")
        return date

   
    def update_task(self):
        try:
            cur_task = self.task.get().strip()
            # don't allow empty task name
            if not cur_task:
                msg.showinfo(title=self.i18n.warning, message=self.i18n.msg_enter_task)
                return 

            #format dates
            formatted_deadline = ""
            if self.deadline_entry.get():
                try:
                    formatted_deadline = self.format_date_str(self.deadline_entry.get())
                except ValueError:
                    msg.showinfo(title=self.i18n.error, message=self.i18n.invalid_date_msg)
                    return

            formatted_dodate = ""
            if self.dodate_entry.get():
                try:
                    formatted_dodate = self.format_date_str(self.dodate_entry.get())
                except ValueError:
                    msg.showinfo(title=self.i18n.error, message=self.i18n.invalid_date_msg)
                    return

            # update task in database
            self.db.update_task(self.task_id, task=cur_task, deadline=formatted_deadline, dodate=formatted_dodate, priority=self.priority.get(), tags=self.selected_tags)
            #  update task in treeview
            updated_task_row = self.db.get_row(self.task_id)
            self.parent.tv.item(self.row_id, values=updated_task_row)
            msg.showinfo(title=self.i18n.success, message=self.i18n.msg_update_success)
            self.close_window()
            
        except sqlite3.Error as err:
            msg.showerror(title=self.i18n.error, message=f"{self.i18n.failed_update}\n" + str(err))

    def select_tag(self):
        if self.selected_tags != "":
            self.selected_tags += ", "
        self.selected_tags += self.tags.get()
        self.lbl_selected_tags.configure(text=self.selected_tags)

    def set_dates(self, deadline, dodate):
        if deadline.strip():
            self.deadline_entry.set_date(datetime.strptime(deadline, "%d/%m/%Y"))
        else:
            self.clear_deadline()
        if dodate.strip():
            self.dodate_entry.set_date(datetime.strptime(dodate, "%d/%m/%Y"))
        else:
            self.clear_dodate()
        

    def create_widgets(self):
        self.lbl_task = ttk.Label(self, text=f"{self.i18n.task}:")
        self.lbl_task.grid(column=0, row=0, padx=(40), pady=20, sticky="w")
        self.txt_task = ttk.Entry(self, textvariable=self.task, width=30)
        self.txt_task.grid(column=1, row=0, padx=(0,10), pady=20, sticky="w", columnspan=2)

        #deadline picker
        self.lbl_deadline = ttk.Label(self, text=f"{self.i18n.deadline}:")
        self.lbl_deadline.grid(column=0, row=1, padx=(40), pady=(0,20), sticky="w")
        self.deadline_entry = DateEntry(self, width=15)
        self.deadline_entry.grid(column=1, row=1, pady=(0,20), sticky="w")
        self.btn_clear_deadline = ttk.Button(self, text=self.i18n.clear, command=self.clear_deadline)
        self.btn_clear_deadline.grid(column=2, row=1, pady=(0,20))
        

        #do date picker
        self.lbl_dodate = ttk.Label(self, text=f"{self.i18n.dodate}:")
        self.lbl_dodate.grid(column=0, row=2,  padx=(40), pady=(0,20), sticky="w")
        self.dodate_entry = DateEntry(self, width=15)
        self.dodate_entry.grid(column=1, row=2, pady=(0,20), sticky="w")
        self.btn_clear_dodate = ttk.Button(self, text=self.i18n.clear, command=self.clear_dodate)
        self.btn_clear_dodate.grid(column=2, row=2, pady=(0,20))

        #priority
        self.lbl_priority = ttk.Label(self, text=f"{self.i18n.priority}:")
        self.lbl_priority.grid(column=0, row=3, padx=40, pady=(0,20), sticky="w")
        self.priority_combo = ttk.Combobox(self, width=20, textvariable=self.priority, state="readonly")
        self.priority_combo["values"] = ("low", "medium", "high")
        self.priority_combo.grid(column=1, columnspan=2, row=3, pady=(0,20),  sticky="w")
        self.priority.set("low")

        #tag
        self.lbl_tag = ttk.Label(self, text=f"{self.i18n.tag}:")
        self.lbl_tag.grid(column=0, row=4, padx=40, pady=(0,20), sticky="w")
        self.tag_combo = ttk.Combobox(self, width=15, textvariable=self.tags, state="normal")
        self.tag_combo["values"] = ("school", "work")
        self.tag_combo.grid(column=1, row=4, pady=(0,20),  sticky="w")
        self.btn_tag_add = ttk.Button(self, text=self.i18n.select,command=self.select_tag)
        self.btn_tag_add.grid(column=2, row=4, pady=(0,20))

        #show tags
        self.lbl_selected_tags = ttk.Label(self, text=self.selected_tags, wraplength=250)
        self.lbl_selected_tags.grid(column=0, columnspan=3, row=5, pady=(0,20))

        # add button
        self.btn_add = ttk.Button(self, text=self.i18n.update_btn, command=self.update_task)
        self.btn_add.grid(column=0, columnspan=3, row=6)
         
        
      
    def close_window(self):
        self.destroy()
