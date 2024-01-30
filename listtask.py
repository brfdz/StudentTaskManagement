import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import databasenew
import languagepack
from centerscreen import center_screen_geometry

class TaskList(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.db = databasenew.FileManager()
        self.parent = parent
        self.selected_language = tk.StringVar(value="en")
        self.i18n = languagepack.I18N(self.selected_language.get())
        self.geometry(center_screen_geometry(screen_width=self.winfo_screenwidth(),
                                             screen_height=self.winfo_screenheight(),
                                             window_width=450,
                                             window_height=200))
        self.title(self.i18n.rem_list)
        self.create_widgets()
        self.bind_widgets()
        self.list_tasks()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def reload_gui_text(self, language):
        self.i18n = languagepack.I18N(language)
        self.title(self.i18n.rem_list)
        self.tree.heading('#1',text=self.i18n.id)
        self.tree.heading('#2',text=self.i18n.reminders)
        self.tree.heading('#3',text=self.i18n.lbl_time)
        self.confirm_delete_title = self.i18n.confirm_delete_title
        self.sure=self.i18n.sure

    def selection(self,event):
        for i in self.tree.selection():
            print(self.tree.item(i)["values"]) 

    def list_tasks(self):
        for g in self.db.list_reminders():
            self.tree.insert(parent="", index="end", values=g)
    
    def delete_task(self, event):
        answer = msg.askyesno(title=self.i18n.confirm_delete_title, message=self.i18n.sure)
        if answer:
            for i in self.tree.selection():
                selected_row = self.tree.item(i)["values"]
                self.db.delete_reminder(selected_row[0])
                self.tree.delete(i)

    def create_widgets(self):
       
        self.tree = ttk.Treeview(self, height=10, show="headings", selectmode="extended")
        self.tree["columns"] = ("id", "task", "time")
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("id", text=self.i18n.id, anchor="center")
        self.tree.heading("task", text=self.i18n.reminders, anchor="center")
        self.tree.heading("time", text=self.i18n.lbl_time, anchor="center")

        self.tree.column("id", anchor="center", width=45, stretch="no")
        self.tree.column("task", anchor="w", width=135)
        self.tree.column("time", anchor="w", width=135)
    
        self.tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.place(relx=1, rely=0, relheight=1, anchor="ne")

        self.context_menu = tk.Menu(self, tearoff=False)
        self.context_menu.add_radiobutton(label="English", variable=self.selected_language, value="en",
                                          command=lambda: self.reload_gui_text("en"))
        self.context_menu.add_radiobutton(label="Türkçe", variable=self.selected_language, value="tr",
                                          command=lambda: self.reload_gui_text("tr"))
    
    def bind_widgets(self):
        self.tree.bind("<Delete>", self.delete_task)  
        self.tree.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.tk_popup(x=event.x_root, y=event.y_root)
    

    def close_window(self):
        self.destroy()
