import tkinter as tk
from tkinter import ttk
import addnewfile
import databasenew
from tkinter import messagebox as msg
import editfile
import os
import languagepack
from centerscreen import center_screen_geometry



class FileBookPage(tk.Toplevel):
    def __init__(self,parent):
        super().__init__()
        self.db = databasenew.FileManager()
        self.parent = parent
        self.selected_language = tk.StringVar(value="tr")
        self.i18n = languagepack.I18N(self.selected_language.get())
        self.window_title=self.i18n.title_filebook
        self.title(self.window_title)
        self.geometry(center_screen_geometry(screen_width=self.winfo_screenwidth(),
                                                 screen_height=self.winfo_screenheight(),
                                                 window_width=500,
                                                 window_height=500))
        self.resizable(False, False)
        self.configure(bg="#D7C6EE")
        self.create_widgets()
        self.bind_widgets()
        self.list_files()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def reload_gui_text(self, language):
        self.i18n = languagepack.I18N(language)
        self.title(self.i18n.title_filebook)
        self.tk.call("destroy", self.menubar)
        self.menubar = tk.Menu(self)
        self.configure(menu=self.menubar)
        self.file_menu = tk.Menu(self.menubar, tearoff=False)
        self.file_menu.add_command(label=self.i18n.file_menu, command=self.show_add_new_window)
        self.menubar.add_cascade(label=self.i18n.menubar, menu=self.file_menu)
        self.tv.heading("file_id",text=self.i18n.file_id,anchor="center")
        self.tv.heading("file_name",text=self.i18n.file_name,anchor="center")
        self.tv.heading("file_type",text=self.i18n.file_type,anchor="center")
        self.tv.heading("file_link", text=self.i18n.file_link, anchor="center")
        self.confirm_delete=self.i18n.confirm_delete
        self.message_delete=self.i18n.message_delete


    def list_files(self):
        db_file = "filebook.db"
        if os.path.exists(db_file):
            files=self.db.list_files()
            if files==[]:
                return
            for f in files:
                self.tv.insert(parent="", index="end", values=f)

    def add_file(self):
        files=self.db.list_files()
        last_item=files[-1]
        self.tv.insert(parent="", index="end", values=last_item)

    def close_window(self):
        self.parent.win.deiconify()
        self.destroy()

    def create_widgets(self):
        self.menubar = tk.Menu(self)
        self.configure(menu=self.menubar)

        self.file_menu = tk.Menu(self.menubar, tearoff=False)
        self.file_menu.add_command(label=self.i18n.file_menu, command=self.show_add_new_window)
        self.menubar.add_cascade(label=self.i18n.menubar, menu=self.file_menu)



        self.tv=ttk.Treeview(self,height=10,show="headings",selectmode="extended")
        self.tv["columns"]=("file_id","file_name","file_type", "file_link")
        #self.tv.pack(fill="both",expand="True")
        self.tv.heading("file_id",text=self.i18n.file_id,anchor="center")
        self.tv.heading("file_name",text=self.i18n.file_name,anchor="center")
        self.tv.heading("file_type",text=self.i18n.file_type,anchor="center")
        self.tv.heading("file_link", text=self.i18n.file_link, anchor="center")

        self.tv.column("file_id", anchor="center", width=70, stretch="no")
        self.tv.column("file_name", anchor="center", width=200)
        self.tv.column("file_type", anchor="center", width=200)
        self.tv.column("file_link", anchor="center", width=500)

        self.tv_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=self.tv_scroll.set)
        self.tv_scroll.place(relx=1, rely=0, relheight=1, anchor="ne")

        self.tv_scroll_x = ttk.Scrollbar(self, orient="horizontal", command=self.tv.xview)
        self.tv.configure(xscrollcommand=self.tv_scroll_x.set)
        self.tv_scroll_x.place(relx=0, rely=1, relwidth=1, anchor="sw")

        self.tv.pack(expand=True, fill="both")

        # Add a context menu
        self.context_menu = tk.Menu(self, tearoff=False)
        self.context_menu.add_radiobutton(label="English", variable=self.selected_language, value="en",
                                          command=lambda: self.reload_gui_text("en"))
        self.context_menu.add_radiobutton(label="Türkçe", variable=self.selected_language, value="tr",
                                          command=lambda: self.reload_gui_text("tr"))




    def delete_file(self, event):
        answer = msg.askyesno(title=self.i18n.title_filebook, message=self.i18n.confirm_delete)
        if answer:
            for i in self.tv.selection():
                selected_row = self.tv.item(i)["values"]
                self.db.delete_file(selected_row[0])
                self.tv.delete(i)
        msg.showinfo(title=self.i18n.title_filebook, message=self.i18n.message_delete)

    def show_add_new_window(self):
        self.add_new= addnewfile.AddNewFile(parent=self)
        self.add_new.grab_set()


    def show_edit_window(self, event):
        # Find the region that is double-clicked.
        # If the region is not a cell, do nothing.
        region = self.tv.identify("region", event.x, event.y)
        if region != "cell":
            return

        selected_row_id = self.tv.selection()[0]
        selected_file_row = self.tv.item(selected_row_id)["values"]
        self.edit_selected = editfile.EditFile(parent=self,
                                                 rowid=selected_row_id,
                                                 file_id=selected_file_row[0],
                                                 file_name=selected_file_row[1],
                                                 file_type=selected_file_row[2],
                                                 file_link=selected_file_row[3])
        self.edit_selected.grab_set()
    def bind_widgets(self):
        self.tv.bind("<Delete>", self.delete_file)  # Delete the selected Treeview item.
        self.tv.bind("<Double-1>", self.show_edit_window)  # Open the edit window for the selected item.
        self.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.tk_popup(x=event.x_root, y=event.y_root)









