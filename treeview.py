import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import EditWindow
import addHabit
import databasenew
import languagepack
from centerscreen import center_screen_geometry

class HabitTracker(tk.Toplevel):
    def __init__(self,parent) :
        super().__init__()
        self.db=databasenew.FileManager()
        self.parent=parent
        self.selected_language = tk.StringVar(value="en")
        self.selected_language2 = tk.StringVar(value="tr")
        self.i18n = languagepack.I18N(self.selected_language.get())
        self.title(self.i18n.title1)
        self.geometry(center_screen_geometry(screen_width=self.winfo_screenwidth(),
                                             screen_height=self.winfo_screenheight(),
                                             window_width=900,
                                             window_height=500))
        self.resizable(height=False,width=False)
        self.configure(bg="#D7C6EE")
        self.name = tk.StringVar()
        self.type = tk.StringVar()
        self.streak = tk.IntVar()
        self.done = tk.IntVar()
        self.create_widgets()
        self.list_habits()
        self.open_progress_window()
        self.protocol("WM_DELETE_WINDOW", self.close_window)
    
    def reload_gui_text(self, language):
        self.i18n = languagepack.I18N(language)
        self.title(self.i18n.title1)
        self.tree.heading('#1',text=self.i18n.id)
        self.tree.heading('#2',text=self.i18n.name)
        self.tree.heading('#3',text=self.i18n.type)
        self.tree.heading('#4',text=self.i18n.streak)
        self.tree.heading('#5',text=self.i18n.done)
        self.new_btn.configure(text=self.i18n.new_btn)
        self.delete_btn.configure(text=self.i18n.delete_btn)
        self.edit_btn.configure(text=self.i18n.edit_btn)
        self.confirm_delete_title=self.i18n.confirm_delete_title
        self.sure=self.i18n.sure
        self.warning=self.i18n.warning
        self.should_select=self.i18n.should_select
        self.monthly_progress=self.i18n.monthly_progress
        self.done_month=self.i18n.done_month
    
    def selection(self,event):
        for i in self.tree.selection():
            print(self.tree.item(i)["values"])

    def list_habits(self): 
        for item in self.tree.get_children():
            self.tree.delete(item)
        for h in self.db.list_habits():
            self.tree.insert(parent="", index="end", values=h)

    def delete_habit(self):
        confirm = msg.askyesno(title=self.i18n.confirm_delete_title, message=self.i18n.sure)
        if confirm:
            for i in self.tree.selection():
                selected_item = self.tree.item(i)["values"]
                self.db.delete_habit(selected_item[0])
                self.tree.delete(i)

    def open_new_window(self):
        self.win3=addHabit.NewHabitWin(self)
        self.win3.grab_set()

    def open_edit_window(self):
        try:
            selected_row_id = self.tree.selection()[0]
            print(selected_row_id)
            selected_habit_row = self.tree.item(selected_row_id)["values"]
            print(selected_habit_row)
            self.win4=EditWindow.EditWin(parent=self,
                                                rowid=selected_row_id,
                                                 hid=selected_habit_row[0],
                                                 name=selected_habit_row[1],
                                                 type=selected_habit_row[2],
                                                 streak=selected_habit_row[3],
                                                 done=selected_habit_row[4])
            print(selected_habit_row[3])
            self.win4.grab_set()  
        except:
            msg.showinfo(self.i18n.warning,self.i18n.should_select)


    def create_widgets(self):
        frame2=ttk.Frame(self)
        
        self.tree=ttk.Treeview(self,columns=("id","Name", "Type", "Streak", "Done"),
                                 show="headings")
        
        self.tree.heading("id", text=self.i18n.id, anchor="center")
        self.tree.heading("Name", text=self.i18n.name, anchor="center")
        self.tree.heading("Type", text=self.i18n.type, anchor="center")
        self.tree.heading("Streak", text=self.i18n.streak, anchor="center")
        self.tree.heading("Done", text=self.i18n.done, anchor="center")

        self.tree.column("id", anchor="center", width=50)
        self.tree.column("Name", anchor="center", width=200)
        self.tree.column("Type", anchor="center", width=100)
        self.tree.column("Streak", anchor="center", width=50)
        self.tree.column("Done", anchor="center", width=50)
        
        self.new_btn=ttk.Button(self,text=self.i18n.new_btn,command=self.open_new_window)
        self.edit_btn=ttk.Button(self,text=self.i18n.edit_btn,command=self.open_edit_window)
        self.delete_btn=ttk.Button(self,text=self.i18n.delete_btn,command=self.delete_habit)
        
        frame2.pack(padx=10,pady=10,anchor="e")
        self.new_btn.pack(padx=10,pady=10,anchor="e")
        self.delete_btn.pack(padx=10,anchor="e")
        self.tree.pack(padx=35,pady=15,fill="both", expand=True)
        self.edit_btn.pack(padx=15,pady=15,anchor="s")
        
        self.scroll=ttk.Scrollbar(self,orient='vertical',command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scroll.set)
        self.scroll.place(relx=1,rely=0,relheight=1,anchor='ne')

        self.tree.bind("<<TreeviewSelect>>", self.selection)
        self.tree.bind("<Double-Button-1>", self.open_progress_window)  
  
        checkbox1=ttk.Checkbutton(frame2,text="English",variable=self.selected_language,command=lambda: self.reload_gui_text("en"))
        checkbox2=ttk.Checkbutton(frame2,text="Türkçe",variable=self.selected_language2,command=lambda: self.reload_gui_text("tr"))

        checkbox1.pack(side="top", padx=5)
        checkbox2.pack(side="bottom", padx=5)

        self.reload_gui_text(self.selected_language.get())   
    

    def open_progress_window(self,event=None):
        self.done_bar_var=tk.DoubleVar()
        self.done_bar=ttk.Progressbar(self,orient='horizontal',length=50,mode='determinate',variable=self.done_bar_var)
        selected_item=self.tree.selection()
        try:
            if selected_item:
                selected_row_id=selected_item[0]    
                print(selected_row_id)
                selected_habit_row = self.tree.item(selected_row_id)["values"]
                value=selected_habit_row[4]
                if value>=0 & value<=30:
                    value=value/30
                self.done_bar_var.set(value*100)
                print(value)
                msg.showinfo(self.i18n.monthly_progress,f"{self.i18n.done_month} {self.done_bar_var.get():.2f}%",parent=self)
        except ValueError:
                return self.i18n.should_select
        
         
    def add_habit(self,name,type,streak,done):
        self.habits.append((name,type,streak,done))
        self.tree.insert("","end",values=(name,type,streak,done))

    def close_window(self):
        self.parent.win.deiconify()
        self.destroy()