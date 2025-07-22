class User:
    def __init__(self, nama=None, nim=None):
        self.nama = nama
        self.nim = nim
        self.total_bottles = 0
    
    def __str__(self):
        return f"User: {self.nama} (NIM: {self.nim}) - Total Bottles: {self.total_bottles}"