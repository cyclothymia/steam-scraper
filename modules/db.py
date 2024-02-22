import os
import sqlite3

class Database:
    def __init__(self):
        self.database_dir = "data"
        self.database_file = os.path.join(self.database_dir, "database.db")
        self.conn = None
        if not os.path.exists(self.database_dir):
            os.makedirs(self.database_dir)
        try:
            self.conn = sqlite3.connect(self.database_file)
            self.cursor = self.conn.cursor()
            self.version = sqlite3.version
        except sqlite3.Error as e:
            print(f"An error occurred connecting to the database: {e}")
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def check(self):
        if not self.conn:
            print("Database connection is not established.")
            return
        try:
            self.cursor.execute("SELECT SQLITE_VERSION()")
            print("Current SQLite version:", self.cursor.fetchone()[0])
        except sqlite3.Error as e:
            print(f"An error occurred fetching the SQLite version: {e}")
    
    def create_db(self):
        if os.path.exists(self.database_file):
            print("Database already exists.")
            return
        else:
            try:
                self.conn = sqlite3.connect(self.database_file)
                print("Database created successfully")
            except sqlite3.Error as e:
                print(f"An error occurred creating the database: {e}")
            finally:
                if self.conn:
                    self.conn.close()
        
    def create_table(self, sql):
        if not self.conn:
            print("Database connection is not established.")
            return
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print("Table created successfully")
        except sqlite3.Error as e:
            print(f"[!] An error occurred when creating a table in the database: {e}")
        finally:
            pass
