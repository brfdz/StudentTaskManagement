import tkinter as tk
from tkinter import ttk
import add_todo
import databasenew
from tkinter import messagebox as msg
from datetime import datetime
import edit_todo
import languagepack
from centerscreen import center_screen_geometry

class TodoList(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.db =databasenew.FileManager()
        self.parent = parent
        self.geometry(center_screen_geometry(screen_width=self.winfo_screenwidth(),
                                                 screen_height=self.winfo_screenheight(),
                                                 window_width=900,
                                                 window_height=500))
        self.selected_lang = tk.StringVar(value="en")
        self.i18n = languagepack.I18N(language=self.selected_lang.get())
        self.title(self.i18n.ToDoList)
        self.current_status = tk.StringVar()
        self.create_widgets()
        self.bind_widgets()
        self.list_tasks()
        self.protocol("WM_DELETE_WINDOW", self.close_window)


    def change_lang(self, event):
        language = self.lang_combo.get()
        self.i18n = languagepack.I18N(language)
        self.title(self.i18n.ToDoList)
        self.add_new.configure(text=self.i18n.add_task_btn)
        self.tv.heading("status", text=self.i18n.status)
        self.tv.heading("task", text=self.i18n.task)
        self.tv.heading("deadline", text=self.i18n.deadline)
        self.tv.heading("dodate", text=self.i18n.dodate)
        self.tv.heading("priority", text=self.i18n.priority)
        self.tv.heading("tags", text=self.i18n.tags)
        self.stat_menu.entryconfig(0, label=self.i18n.not_started)
        self.stat_menu.entryconfig(1, label=self.i18n.in_progress)
        self.stat_menu.entryconfig(2, label=self.i18n.done)

    def format_date_str(self, str):
        date = datetime.strptime(str, "%m/%d/%y")
        date = date.strftime("%d/%m/%Y")
        return date
        
    def list_tasks(self):
        for task in self.db.list_tasks():
            self.tv.insert(parent="", index="end", values=task)

    def add_task(self):
        self.add = add_todo.AddTask(parent=self)
        self.add.grab_set()

    def edit_selected_task(self, event):
        self.item_id = self.tv.identify_row(event.y)
        if self.item_id:
            selected_row = self.tv.item(self.item_id)["values"]
            self.edit = edit_todo.EditTask(parent = self,
                                        row_id=self.item_id,
                                        task_id=selected_row[0],
                                        task=selected_row[2],
                                        deadline=selected_row[3],
                                        dodate=selected_row[4],
                                        priority=selected_row[5],
                                        tags=selected_row[6])
            
            self.edit.grab_set()
        

    def delete_task(self, event):
        answer = msg.askyesno(title=self.i18n.confirm_delete_title, message=self.i18n.confirm_delete)
        if answer:
            for i in self.tv.selection():
                selected_row = self.tv.item(i)["values"]
                self.db.delete_task(selected_row[0])
                self.tv.delete(i)

    def show_context_menu(self, event):
        self.item_id = self.tv.identify_row(event.y)
        if self.item_id:
            # select the status of the current task
            self.task_id = self.tv.item(self.item_id)["values"][0]
            self.selected_task = self.db.get_row(self.task_id)
            self.current_status.set(self.selected_task[1])
            #show menu
            self.stat_menu.post(event.x_root, event.y_root)

    def on_radiobutton_selected(self):
        # Change status in database
        self.db.change_status(self.current_status.get(), self.selected_task[0])
        # change status in treeview
        self.tv.set(self.item_id, column="status", value=self.current_status.get())


    def create_widgets(self):
        self.frame = tk.Frame(self)
        self.frame.pack(fill="both")
        self.add_new = ttk.Button(self.frame, text=self.i18n.add_task_btn, command=self.add_task)
        self.add_new.grid(column= 0, row=0, padx=40, pady=20, sticky="w")

        #Change language
        self.lang_combo = ttk.Combobox(self.frame, textvariable=self.selected_lang, values=["en", "tr"], state="readonly", width=5)
        self.lang_combo.grid(column= 1, row=0, sticky="e")

        #Create treeview
        self.tv = ttk.Treeview(self, show="headings")
        self.tv["columns"] = ("id", "status", "task", "deadline", "dodate", "priority", "tags")
        self.tv.pack(fill="both", expand=True, padx=50)

        #headings
        self.tv.heading("status", text=self.i18n.status)
        self.tv.heading("task", text=self.i18n.task)
        self.tv.heading("deadline", text=self.i18n.deadline)
        self.tv.heading("dodate", text=self.i18n.dodate)
        self.tv.heading("priority", text=self.i18n.priority)
        self.tv.heading("tags", text=self.i18n.tags)

        #configure columns TODO
        self.tv.column("id", width=0, stretch="no")
        self.tv.column("status", width=100, stretch="no", anchor="center")
        self.tv.column("task", minwidth=150)
        self.tv.column("deadline", width=120, stretch="no", anchor="center")
        self.tv.column("dodate", width=120, stretch="no", anchor="center")
        self.tv.column("priority", width=100, stretch="no", anchor="center")
        self.tv.column("tags", minwidth= 100, width=100, anchor="center")

        #vertical scrollbar
        self.tv_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=self.tv_scroll.set)
        self.tv_scroll.place(relx=1, rely=0, relheight=1, anchor="ne")

        # Context menu 
        # Change status with radiobuttons
        self.stat_menu = tk.Menu(self, tearoff=False)
        self.stat_menu.add_radiobutton(label=self.i18n.not_started, variable=self.current_status, value=self.i18n.not_started, command=self.on_radiobutton_selected)
        self.stat_menu.add_radiobutton(label=self.i18n.in_progress, variable=self.current_status, value=self.i18n.in_progress, command=self.on_radiobutton_selected)
        self.stat_menu.add_radiobutton(label=self.i18n.done, variable=self.current_status, value=self.i18n.done, command=self.on_radiobutton_selected)



    def bind_widgets(self):
        self.tv.bind("<Delete>", self.delete_task)
        self.tv.bind("<Button-3>", self.show_context_menu)
        self.tv.bind("<Double-1>", self.edit_selected_task)
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_lang)


    def close_window(self):
        self.destroy()
        self.parent.win.deiconify() 
       
        

