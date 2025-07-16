import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_name="trashlink.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                nim TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bottles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_nim TEXT NOT NULL,
                bottle_count INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_nim) REFERENCES users (nim)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def register_user(self, nama, nim):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO users (nama, nim) VALUES (?, ?)", (nama, nim))
            conn.commit()
            conn.close()
            return True, "User registered successfully"
        except sqlite3.IntegrityError:
            return False, "NIM already exists. Please use a different NIM."
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def login_user(self, nim):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("SELECT nama, nim FROM users WHERE nim = ?", (nim,))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return True, f"Welcome {user[0]}!", user[0]
            else:
                return False, "NIM not found. Please register first.", None
        except Exception as e:
            return False, f"Login failed: {str(e)}", None
    
    def add_bottles(self, user_nim, bottle_count):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO bottles (user_nim, bottle_count) VALUES (?, ?)", 
                         (user_nim, bottle_count))
            conn.commit()
            conn.close()
            return True, "Bottles added successfully"
        except Exception as e:
            return False, f"Failed to add bottles: {str(e)}"
    
    def get_user_bottles(self, user_nim):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("SELECT SUM(bottle_count) FROM bottles WHERE user_nim = ?", (user_nim,))
            total = cursor.fetchone()[0]
            conn.close()
            
            return total if total else 0
        except Exception as e:
            return 0
    
    def get_user_bottle_history(self, user_nim):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT bottle_count, created_at 
                FROM bottles 
                WHERE user_nim = ? 
                ORDER BY created_at DESC
            """, (user_nim,))
            
            history = cursor.fetchall()
            conn.close()
            return history
        except Exception as e:
            return []