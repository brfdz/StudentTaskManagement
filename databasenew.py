import sqlite3



class FileManager:
    def __init__(self):
        self.conn = None
        self.cur = None

    @staticmethod
    def get_connection():
        return sqlite3.connect("filebook.db")

    def create_database(self):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("""
        create table if not exists FileBook (
            file_id integer primary key autoincrement,
            file_name text,
            file_type text,
            file_link text
        )
        """)

        self.cur.execute("""
              create table if not exists Habits (
                         hid integer primary key autoincrement,
                         name text,
                        type text,
                        streak integer,
                         done integer);
                         """)

        self.cur.execute("""
        create table if not exists Calendar (
            cid   integer primary key autoincrement,
            task text,
            time text
        );
        """)

        self.cur.execute("""
        create table if not exists TodoList (
            id integer primary key autoincrement,
            status text,
            task text,
            deadline date,
            dodate date,
            priority text,
            tags text             
        );
        """)

        self.conn.commit()
        self.conn.close()

    def fill_database(self):
        self.conn=self.get_connection()
        self.cur=self.conn.cursor()
        data=[
            ('Python GUI Course','Study','3','20'),
            ('JAVA OOP Course','Study','6','12')]
        for i in data:
            self.cur.execute("insert into Habits(name, type, streak, done) values(?, ?, ? ,?)", i)
        self.conn.commit()
        self.conn.close()

    def fill_database2(self):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        data = [('Go abroad', '12/12/23'),
                ('Study Python', '10/12/24'),
                ]

        for item in data:
            self.cur.execute("insert into Calendar(task, time) values(?, ?)", item)

        self.conn.commit()
        self.conn.close()


    def clear_database(self):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("delete from FileBook")
        self.cur.execute("delete from Habits")
        self.cur.execute("delete from Calendar")
        self.cur.execute("delete from TodoList")
        self.conn.commit()
        self.conn.close()

    def add_file(self, file_name, file_type,file_link):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("insert into FileBook(file_name, file_type, file_link) values(:file_name, :file_type , :file_link)",
                         {"file_name": file_name,
                          "file_type": file_type ,
                          "file_link" : file_link})

        self.conn.commit()
        self.conn.close()

    def add_habit(self,name,type,streak,done):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("insert into Habits(name,type,streak,done) values(:name,:type,:streak,:done)",
                         {"name": name,
                          "type": type,
                          "streak": streak,
                          "done": done})
        self.conn.commit()
        self.conn.close()

    #calendar
    def add_reminder(self, task, time):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("insert into Calendar(task, time) values(:task, :time)",
                         {"task": task,
                          "time": time})
        self.conn.commit()
        self.conn.close()


    #todo list
    def add_task(self, task, deadline, dodate, priority, tags):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("insert into Todolist(status, task, deadline, dodate, priority, tags) values(:status, :task, :deadline, :dodate, :priority, :tags)",
                         {
                             "status": "Not started",
                             "task": task,
                             "deadline": deadline,
                             "dodate": dodate,
                             "priority": priority,
                             "tags": tags
                         })
        self.conn.commit()
        last_row_id = self.cur.lastrowid
        self.conn.close()
        return last_row_id

    def list_files(self):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("select * from FileBook")
        filebook = self.cur.fetchall()
        self.conn.close()
        if not filebook:
            return []

        return filebook

    def list_habits(self):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("select * from Habits")
        habits = self.cur.fetchall()
        self.conn.close()
        return habits

    #calendar
    def list_reminders(self):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("select * from Calendar")
        tasks = self.cur.fetchall()
        self.conn.close()
        return tasks
    

    #todo list
    def list_tasks(self):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("select * from Todolist")
        tasks = self.cur.fetchall()
        self.conn.close()
        return tasks
    

    def delete_file(self, file_id):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("delete from FileBook where file_id=?", [file_id])
        self.conn.commit()

    def delete_habit(self, hid):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("delete from Habits where hid=?", [hid])
        self.conn.commit()

    #calendar
    def delete_reminder(self, cid):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("delete from Calendar where cid=?", [cid])
        self.conn.commit()

    #todo 
    def delete_task(self, id):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("delete from Todolist where id=?", [id])
        self.conn.commit()
        self.conn.close()

    def edit_file(self,file_id,file_name,file_type,file_link):
        self.conn=self.get_connection()
        self.cur=self.conn.cursor()
        self.cur.execute("update FileBook set file_name=?, file_type=?, file_link=? where file_id=?",
                         [file_name, file_type, file_link, file_id])
        self.conn.commit()

    def edit_habit(self,hid, name,type,streak,done):
        try:
            self.conn = self.get_connection()
            self.cur = self.conn.cursor()
            self.cur.execute("update Habits set name=?, type=?, streak=?, done=? where hid=?",
                             [name,type,streak,done,hid])
            self.conn.commit()

        except sqlite3.Error as e:
            print("Error updating habit:", e)

    def edit_task(self, cid, task, time):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("update Calendar set task=?, time=? where cid=?",
                         [task, time,cid])
        self.conn.commit()

    #todo list
    def get_row(self, id):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("select * from Todolist where id=?", [id])

        selected_row = self.cur.fetchone()
        self.conn.close()
        return selected_row
    
    #todo list
    def change_status(self, status, id):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("update Todolist set status=? where id=?",
                         [status, id])
        self.conn.commit()
        self.conn.close()

    #todo 
    def update_task(self, id, task, deadline, dodate, priority, tags):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("update Todolist set task=?, deadline=?, dodate=?, priority=?, tags=? where id=?",
                         [task, deadline, dodate, priority, tags, id])
        self.conn.commit()
        self.conn.close()


databasenew=FileManager()
databasenew.create_database()










