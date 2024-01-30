import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import date
from tkinter import messagebox
import databasenew
import addTask
import listtask
import languagepack
from centerscreen import center_screen_geometry


class CalendarTracker(tk.Toplevel):
    def __init__(self,parent) :
        super().__init__()
        self.db=databasenew.FileManager()
        self.parent=parent
        self.selected_language = tk.StringVar(value="en")
        self.selected_language2 = tk.StringVar(value="tr")
        self.i18n = languagepack.I18N(self.selected_language.get())
        self.win5=None
        self.title(self.i18n.title3)
        self.geometry(center_screen_geometry(screen_width=self.winfo_screenwidth(),
                                             screen_height=self.winfo_screenheight(),
                                             window_width=500,
                                             window_height=500))
        self.resizable(height=False,width=False)
        self.configure(bg="#D7C6EE")
        self.lbl_today = tk.StringVar()
        self.add_task_btn = tk.StringVar()
        self.list_btn = tk.StringVar()
        self.lbl_selected = tk.StringVar()
        self.selected_date=None
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def reload_gui_text(self, language):
        self.i18n = languagepack.I18N(language)
        self.title(self.i18n.title3)
        self.lbl_today.configure(text=self.i18n.lbl_today)
        self.add_task_btn.configure(text=self.i18n.add_reminder)
        self.list_btn.configure(text=self.i18n.rem_list)
        self.lbl_selected.configure(text=self.i18n.lbl_selected)
        self.selecting_date=self.i18n.selecting_date
        self.warning=self.i18n.warning
    
    def create_widgets(self):
        frame1=ttk.Frame(self)
        frame2=ttk.Frame(self)
        self.date_today=date.today()
        self.calendar=Calendar(self,selectmode="day")
        self.lbl_today=tk.Label(frame1,text=self.i18n.lbl_today )
        self.date_today=tk.Label(frame1,text=self.date_today.strftime("%m/%d/%Y"))
        self.task_text=tk.Text(self,width=25,height=15)
        self.add_task_btn=tk.Button(self,text=self.i18n.add_task_btn,command=self.double_click_event3)
        self.list_btn=tk.Button(self,text=self.i18n.rem_list,command=self.show_task_list_window)
        self.lbl_selected=tk.Label(frame1,text=self.i18n.lbl_selected)
        self.get_date=tk.Label(frame1,text= self.calendar.get_date())

        self.lbl_today.grid(row=0,column=0,sticky="w")
        self.date_today.grid(row=0,column=1,sticky="w")
        self.lbl_selected.grid(row=1,column=0)
        
        frame2.pack(padx=10,pady=10,anchor="e")
        frame1.pack(anchor="w",pady=10,padx=10)

        self.add_task_btn.pack(anchor="e",padx=10)
        self.list_btn.pack(anchor="e",pady=10,padx=10)
        self.calendar.pack(pady=10)
        self.task_text.pack(pady=20)
        
        self.calendar.bind("<<CalendarSelected>>", self.date_selection)
        
        checkbox1=ttk.Checkbutton(frame2,text="English",variable=self.selected_language,command=lambda: self.reload_gui_text("en"))
        checkbox2=ttk.Checkbutton(frame2,text="Türkçe",variable=self.selected_language2,command=lambda: self.reload_gui_text("tr"))

        checkbox1.pack(side="top", padx=5)
        checkbox2.pack(side="bottom", padx=5)

        self.reload_gui_text(self.selected_language.get())

    def date_selection(self,event):
        self.selected_date=self.calendar.get_date()
        self.lbl_selected.config(text=self.i18n.lbl_selected + self.selected_date)

    def double_click_event3(self):
        if self.selected_date is None:
            messagebox.showwarning(self.i18n.warning,self.i18n.selecting_date)
        else:
            self.win5=addTask.AddTask(self)
            self.win5.grab_set() 

    def add_task(self,task,time):
        self.task_text.insert(tk.END,time+"\t" +task+"\n")

    def show_task_list_window(self):
        self.task_list = listtask.TaskList(self)
        self.task_list.grab_set()

    def close_window(self):
        self.destroy()
        self.parent.win.deiconify()
    