import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import sqlite3
import databasenew
import languagepack
from centerscreen import center_screen_geometry

class NewHabitWin(tk.Toplevel):
    def __init__(self,parent) :
        super().__init__()
        self.db=databasenew.FileManager()
        self.parent=parent
        self.selected_language = tk.StringVar(value="en")
        self.selected_language2 = tk.StringVar(value="tr")
        self.i18n = languagepack.I18N(self.selected_language.get())
        self.title(self.i18n.title)
        self.geometry(center_screen_geometry(screen_width=self.winfo_screenwidth(),
                                             screen_height=self.winfo_screenheight(),
                                             window_width=300,
                                             window_height=300))
        self.resizable(height=False,width=False)
        self.configure(bg="#D7C6EE")
        self.name = tk.StringVar()
        self.type = tk.StringVar()
        self.streak = tk.IntVar()
        self.done = tk.IntVar()
        self.create_widgets()
        self.name_entry.focus_set()

    def reload_gui_text(self, language):
        self.i18n = languagepack.I18N(language)
        self.title(self.i18n.title)
        self.name_label.configure(text=self.i18n.name)
        self.type_label.configure(text=self.i18n.type)
        self.streak_label.configure(text=self.i18n.streak)
        self.done_label.configure(text=self.i18n.done)
        self.add_btn.configure(text=self.i18n.add_btn)
        self.habit_message_lbl=self.i18n.habit_message
        self.warning_lbl=self.i18n.warning
        self.added_msg=self.i18n.added_msg
        self.habit_saved=self.i18n.habit_saved
        self.failed_habit_added=self.i18n.failed_habit_added
        self.study=self.i18n.study
        self.work=self.i18n.work
        self.entertainment=self.i18n.entertainment
        self.other=self.i18n.other
        self.error=self.i18n.error
        self.valuenot=self.i18n.valuenot

    def save_data(self):
        try:
            name_cont=self.name_entry.get()
            if not name_cont :
                msg.showwarning(self.i18n.warning,self.i18n.habit_message)
                return
            self.db.add_habit(name=self.name_entry.get(), type=self.type_combo.get(), streak=self.streak_entry.get(),done=self.done_entry.get())
            msg.showinfo(self.i18n.added_msg, self.i18n.habit_saved)
            self.parent.list_habits()
            self.clear_entry()
            
            self.name_entry.focus_set()
            self.destroy()
            
        except (tk.TclError, sqlite3.Error) as err:
            msg.showerror( message=self.i18n.failed_habit_added + str(err))

    def clear_entry(self):
        self.name_entry.delete(0, "end")
        self.type_combo.set("")
        self.streak_entry.delete(0, "end")
        self.done_entry.delete(0, "end") 
        self.done_bar_var.set("")  
        
        
    def create_widgets(self):
        frame=ttk.Frame(self)
        frame2=ttk.Frame(self)
        
        self.name_label=ttk.Label(frame,text=self.i18n.name)
        self.type_label=ttk.Label(frame,text=self.i18n.type)
        self.streak_label=ttk.Label(frame,text=self.i18n.streak)
        self.done_label=ttk.Label(frame,text=self.i18n.done)
        self.name_entry=ttk.Entry(frame,textvariable=self.name)
        types=tk.StringVar()
        self.type_combo=ttk.Combobox(frame,width=17,textvariable=types,state="readonly")
        self.type_combo["values"]=(self.i18n.study,self.i18n.work,self.i18n.entertainment,self.i18n.other)
        
        self.streak_entry=ttk.Entry(frame,textvariable=self.streak)
        self.done_entry=ttk.Entry(frame,textvariable=self.done)
        self.add_btn=ttk.Button(self,text=self.i18n.add_btn,command=(self.save_data))
 
        self.done_bar_var=tk.DoubleVar()
        self.done_bar=ttk.Progressbar(self,orient='horizontal',length=50,mode='determinate',variable=self.done_bar_var)
        
        self.done_bar.pack()
        frame2.pack(padx=10,pady=10,anchor="e")
        frame.pack()
        self.add_btn.pack(padx=10,pady=10)
        

        self.name_label.grid(row=0,column=0)
        self.name_entry.grid(row=0,column=1)
        self.type_label.grid(row=1,column=0)
        self.type_combo.grid(row=1,column=1)
        self.streak_label.grid(row=2,column=0)
        self.streak_entry.grid(row=2,column=1)
        self.done_label.grid(row=3,column=0)
        self.done_entry.grid(row=3,column=1)

        self.done_entry.bind("<KeyRelease>",self.done_pbar)
        
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
            msg.showerror(self.i18n.error,self.i18n.valuenot)
            
    
    def show_context_menu(self, event):
        self.context_menu.tk_popup(x=event.x_root, y=event.y_root)

    def close_window(self):
        self.parent.deiconify()
        self.destroy()    
    