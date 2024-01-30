import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import sqlite3
import databasenew
import languagepack
from centerscreen import center_screen_geometry

class EditWin(tk.Toplevel):
    def __init__(self,parent,rowid,hid,name,type,streak,done) :
        super().__init__()
        self.db= databasenew.FileManager()
        self.parent=parent
        self.selected_language = tk.StringVar(value="en")
        self.selected_language2 = tk.StringVar(value="tr")
        self.i18n = languagepack.I18N(self.selected_language.get())
        self.title(self.i18n.title2 )
        self.geometry(center_screen_geometry(screen_width=self.winfo_screenwidth(),
                                             screen_height=self.winfo_screenheight(),
                                             window_width=300,
                                             window_height=300))
        self.resizable(height=False,width=False)
        self.configure(bg="#D7C6EE")
        self.name = tk.StringVar(value=name)
        self.types=tk.StringVar(value=type)
        self.streak = tk.IntVar(value=streak)
        self.done = tk.IntVar(value=done)
        self.hid = hid
        self.rowid = rowid
        self.create_widgets()
        self.name_entry.focus_set()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def reload_gui_text(self, language):
        self.i18n = languagepack.I18N(language)
        self.title(self.i18n.title2 +": "+ self.name.get() )
        self.name_label.configure(text=self.i18n.name)
        self.type_label.configure(text=self.i18n.type)
        self.streak_label.configure(text=self.i18n.streak)
        self.done_label.configure(text=self.i18n.done)
        self.update_btn.configure(text=self.i18n.update_btn)
        self.study=self.i18n.study
        self.work=self.i18n.work
        self.entertainment=self.i18n.entertainment
        self.other=self.i18n.other
        self.success=self.i18n.success
        self.updated_success=self.i18n.updated_success
        self.failed_update=self.i18n.failed_update
        self.error=self.i18n.error

    def update_habits(self):
        try:
            self.db.edit_habit(hid=self.hid, name=self.name.get(), type=self.types.get(), streak=self.streak.get(),done=self.done.get())
            self.parent.tree.item(self.rowid,values=(self.hid, self.name.get(), self.types.get(), self.streak.get(),self.done.get()))
            msg.showinfo(self.i18n.success, self.i18n.updated_success)
            self.close_window()
                
        except (tk.TclError, sqlite3.Error) :
            msg.showerror(title=self.i18n.error, message=self.i18n.failed_update)

    def create_widgets(self):

        frame=ttk.Frame(self)
        frame2=ttk.Frame(self)
        
        self.name_label=ttk.Label(frame,text=self.i18n.name)
        self.type_label=ttk.Label(frame,text=self.i18n.type)
        self.streak_label=ttk.Label(frame,text=self.i18n.streak)
        self.done_label=ttk.Label(frame,text=self.i18n.done)
        self.name_entry=ttk.Entry(frame, textvariable=self.name)
        
        self.type_combo=ttk.Combobox(frame,width=17,textvariable=self.types,state="readonly")
        self.type_combo["values"]=(self.i18n.study,self.i18n.work,self.i18n.entertainment,self.i18n.other)
        
        self.streak_entry=ttk.Entry(frame, textvariable=self.streak)
        self.done_entry=ttk.Entry(frame, textvariable=self.done)
        self.update_btn=ttk.Button(self,text=self.i18n.update_btn,command=self.update_habits)
 
        self.done_bar_var=tk.DoubleVar()
        self.done_bar=ttk.Progressbar(self,orient='horizontal',length=50,mode='determinate',variable=self.done_bar_var)
        
        self.done_bar.pack()
        frame2.pack(padx=10,pady=10,anchor="e")
        frame.pack()
        self.update_btn.pack(pady=10)
        
        self.name_label.grid(row=0,column=0)
        self.name_entry.grid(row=0,column=1)
        self.type_label.grid(row=1,column=0)
        self.type_combo.grid(row=1,column=1)
        self.streak_label.grid(row=2,column=0)
        self.streak_entry.grid(row=2,column=1)
        self.done_label.grid(row=3,column=0)
        self.done_entry.grid(row=3,column=1)

        checkbox1=ttk.Checkbutton(frame2,text="English",variable=self.selected_language,command=lambda: self.reload_gui_text("en"))
        checkbox2=ttk.Checkbutton(frame2,text="Türkçe",variable=self.selected_language2,command=lambda: self.reload_gui_text("tr"))
        checkbox1.pack(side="top", padx=5)
        checkbox2.pack(side="bottom", padx=5)

        self.reload_gui_text(self.selected_language.get())

    def done_pbar(self,event):
        try:
            value=int(self.done_entry.get())
            if value>=0 & value<=30:
                value=value/30
            self.done_bar_var.set(value*100)

        except ValueError:
            pass

    def close_window(self):
        self.destroy()    




