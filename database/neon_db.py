import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class NeonDatabase:
    def __init__(self):
        self.connection_string = os.getenv("DATABASE_URL", "postgresql://username:password@hostname:port/database")
        
        if self.connection_string == "postgresql://username:password@hostname:port/database":
            print("WARNING: Please update your Neon database connection string in .env file")
            print("Set DATABASE_URL environment variable with your Neon connection string")
            raise Exception("Neon database connection string not configured")
        
        try:
            self.test_connection()
            print("Connected to Neon database successfully")
        except Exception as e:
            print(f"Failed to connect to Neon database: {str(e)}")
            raise e
    
    def get_connection(self):
        return psycopg2.connect(self.connection_string, cursor_factory=RealDictCursor)
    
    def test_connection(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    nama TEXT NOT NULL,
                    nim TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bottles (
                    id SERIAL PRIMARY KEY,
                    user_nim TEXT NOT NULL REFERENCES users(nim) ON DELETE CASCADE,
                    bottle_count INTEGER NOT NULL,
                    sensor1 INTEGER DEFAULT 0,
                    sensor2 INTEGER DEFAULT 0,
                    sensor3 INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_nim ON users(nim)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_bottles_user_nim ON bottles(user_nim)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_bottles_created_at ON bottles(created_at)")
            
            conn.commit()
            print("Database tables initialized successfully")
            
        except Exception as e:
            conn.rollback()
            print(f"Failed to initialize database: {str(e)}")
            raise e
        finally:
            conn.close()
    
    def register_user(self, nama, nim):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO users (nama, nim) VALUES (%s, %s)", (nama, nim))
            conn.commit()
            return True, "User registered successfully"
            
        except psycopg2.IntegrityError:
            conn.rollback()
            return False, "NIM already exists. Please use a different NIM."
        except Exception as e:
            conn.rollback()
            return False, f"Registration failed: {str(e)}"
        finally:
            conn.close()
    
    def login_user(self, nim):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT nama, nim FROM users WHERE nim = %s", (nim,))
            user = cursor.fetchone()
            
            if user:
                return True, f"Welcome {user['nama']}!", user['nama']
            else:
                return False, "NIM not found. Please register first.", None
                
        except Exception as e:
            return False, f"Login failed: {str(e)}", None
        finally:
            conn.close()
    
    def add_bottles(self, user_nim, bottle_count, sensor1=0, sensor2=0, sensor3=0):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO bottles (user_nim, bottle_count, sensor1, sensor2, sensor3) 
                VALUES (%s, %s, %s, %s, %s)
            """, (user_nim, bottle_count, sensor1, sensor2, sensor3))
            
            conn.commit()
            return True, "Bottles added successfully"
            
        except Exception as e:
            conn.rollback()
            return False, f"Failed to add bottles: {str(e)}"
        finally:
            conn.close()
    
    def get_user_bottles(self, user_nim):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT SUM(bottle_count) as total FROM bottles WHERE user_nim = %s", (user_nim,))
            result = cursor.fetchone()
            return result['total'] if result['total'] else 0
            
        except Exception as e:
            print(f"Error getting user bottles: {str(e)}")
            return 0
        finally:
            conn.close()
    
    def get_user_bottle_history(self, user_nim):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT bottle_count, sensor1, sensor2, sensor3, created_at 
                FROM bottles 
                WHERE user_nim = %s 
                ORDER BY created_at DESC
            """, (user_nim,))
            
            results = cursor.fetchall()
            return [(row['bottle_count'], row['sensor1'], row['sensor2'], row['sensor3'], row['created_at']) for row in results]
            
        except Exception as e:
            print(f"Error getting bottle history: {str(e)}")
            return []
        finally:
            conn.close()
    
    def get_latest_sensor_data(self, user_nim=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if user_nim:
                cursor.execute("""
                    SELECT user_nim, sensor1, sensor2, sensor3, created_at 
                    FROM bottles 
                    WHERE user_nim = %s 
                    ORDER BY created_at DESC 
                    LIMIT 10
                """, (user_nim,))
            else:
                cursor.execute("""
                    SELECT user_nim, sensor1, sensor2, sensor3, created_at 
                    FROM bottles 
                    ORDER BY created_at DESC 
                    LIMIT 10
                """)
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            print(f"Error getting sensor data: {str(e)}")
            return []
        finally:
            conn.close()
    
    def get_all_users(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id, nama, nim, created_at FROM users ORDER BY created_at DESC")
            results = cursor.fetchall()
            return [(row['id'], row['nama'], row['nim'], row['created_at']) for row in results]
            
        except Exception as e:
            print(f"Error fetching users: {str(e)}")
            return []
        finally:
            conn.close()
    
    def get_all_bottles(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT b.id, b.user_nim, u.nama, b.bottle_count, 
                       b.sensor1, b.sensor2, b.sensor3, b.created_at 
                FROM bottles b
                JOIN users u ON b.user_nim = u.nim
                ORDER BY b.created_at DESC
            """)
            
            results = cursor.fetchall()
            return [(row['id'], row['user_nim'], row['nama'], row['bottle_count'], 
                    row['sensor1'], row['sensor2'], row['sensor3'], row['created_at']) for row in results]
            
        except Exception as e:
            print(f"Error fetching bottles: {str(e)}")
            return []
        finally:
            conn.close()
    
    def get_database_stats(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) as count FROM users")
            total_users = cursor.fetchone()['count']
            
            cursor.execute("SELECT SUM(bottle_count) as total FROM bottles")
            result = cursor.fetchone()
            total_bottles = result['total'] if result['total'] else 0
            
            cursor.execute("SELECT COUNT(*) as count FROM bottles")
            total_transactions = cursor.fetchone()['count']
            
            return {
                'total_users': total_users,
                'total_bottles': total_bottles,
                'total_transactions': total_transactions
            }
            
        except Exception as e:
            print(f"Error fetching stats: {str(e)}")
            return {'total_users': 0, 'total_bottles': 0, 'total_transactions': 0}
        finally:
            conn.close()
    
    def delete_user(self, nim):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM users WHERE nim = %s", (nim,))
            conn.commit()
            return True, "User and all associated data deleted successfully"
            
        except Exception as e:
            conn.rollback()
            return False, f"Failed to delete user: {str(e)}"
        finally:
            conn.close()
    
    def clear_all_data(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM bottles")
            cursor.execute("DELETE FROM users")
            conn.commit()
            return True, "All data cleared successfully"
            
        except Exception as e:
            conn.rollback()
            return False, f"Failed to clear data: {str(e)}"
        finally:
            conn.close()
