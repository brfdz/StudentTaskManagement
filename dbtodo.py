import sqlite3

class TodoManager:
    def __init__(self):
        self.conn = None
        self.cur = None

    @staticmethod
    def get_connection():
        return sqlite3.connect("todolist.db")
    
    def create_database(self):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("""
        create table TodoList (
            id integer primary key autoincrement,
            task text,
            status text,
            deadline date,
            dodate date,
            priority text,
            tags text             
        );
        """)
        self.conn.commit()
        self.conn.close()


    def add_task(self, task, deadline, dodate, priority, tags):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("insert into Todolist(task, status, deadline, dodate, priority, tags) values(:task, :status, :deadline, :dodate, :priority, :tags)",
                         {
                             "task": task,
                             "status": "Not started",
                             "deadline": deadline,
                             "dodate": dodate,
                             "priority": priority,
                             "tags": tags
                         })
        self.conn.commit()
        last_row_id = self.cur.lastrowid
        self.conn.close()
        return last_row_id

    def list_tasks(self):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("select * from Todolist")
        tasks = self.cur.fetchall()
        self.conn.close()
        return tasks
    
    def delete_task(self, id):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("delete from Todolist where id=?", [id])
        self.conn.commit()
        self.conn.close()

    def get_row(self, id):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("select * from Todolist where id=?", [id])

        selected_row = self.cur.fetchone()
        self.conn.close()
        return selected_row
    
    def change_status(self, status, id):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("update Todolist set status=? where id=?",
                         [status, id])
        self.conn.commit()
        self.conn.close()

    def update_task(self, id, task, deadline, dodate, priority, tags):
        self.conn = self.get_connection()
        self.cur = self.conn.cursor()
        self.cur.execute("update Todolist set task=?, deadline=?, dodate=?, priority=?, tags=? where id=?",
                         [task, deadline, dodate, priority, tags, id])
        self.conn.commit()
        self.conn.close()