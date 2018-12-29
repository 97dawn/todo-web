import psycopg2

class DB:
    def __init__(self):
        self.con = psycopg2.connect("dbname=todo host=localhost user=postgres password=postgres")
        self.cursor = self.con.cursor()
    
    def select_user_info(self, data):
        self.cursor.callproc('sp_select_user_info', data)
        return self.cursor.fetchone()
    
    def insert_user_info(self, data):
        try:
            self.cursor.callproc('sp_insert_user_info', data)
            self.con.commit()
        except Exception:
            self.con.rollback()
    
    def select_todos(self, data):
        self.cursor.callproc('sp_select_todos', data)
        return self.cursor.fetchall() 

    def select_todo(self, data):
        self.cursor.callproc('sp_select_todo', data)
        return self.cursor.fetchone() 

    def insert_todo(self, data):
        try:
            self.cursor.callproc('sp_insert_todo', data)
            self.con.commit()
        except Exception:
            self.con.rollback()
    
    def remove_todo(self, data):
        try:
            self.cursor.callproc('sp_remove_todo', data)
            self.con.commit()
        except Exception:
            self.con.rollback()
    
    def update_todo(self, data):
        try:
            self.cursor.callproc('sp_update_todo', data)
            self.con.commit()
        except Exception:
            self.con.rollback()
    
    def increase_priority_todo(self, data):
        try:
            self.cursor.callproc('sp_increase_priority_todo', data)
            self.con.commit()
        except Exception:
            self.con.rollback()
    
    def decrease_priority_todo(self, data):
        try:
            self.cursor.callproc('sp_decrease_priority_todo', data)
            self.con.commit()
        except Exception:
            self.con.rollback()

    def completed_todo(self, data):
        try:
            self.cursor.callproc('sp_completed_todo', data)        
            self.con.commit()
        except Exception:
            self.con.rollback()

    def select_completed_todos(self, data):
        self.cursor.callproc('sp_select_completed_todos', data)
        return self.cursor.fetchall() 
    
    def free(self):
        self.cursor.close()
        self.con.close()
    
